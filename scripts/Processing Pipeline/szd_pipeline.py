#!/usr/bin/env python3
"""
szd_pipeline.py — Unified processing pipeline for the Stefan Zweig Digital Archive.

Run steps in this order:
  1. sort       After Lightroom export: normalize filenames, move TIFF/RAW into subfolders
  2. generate   Generate intermediate XML files from CSV, written directly into each signature folder
                ── MANUAL STEP: open each XML, review and fill in page number ranges ──
  3. transform  Apply XSLT to produce the final METS viewer XML (Result_*.xml)

Additional commands:
  status        Show the current processing stage of every signature folder

Usage:
  python szd_pipeline.py sort      [--root DIR] [--series SZ_AAL_B2] [--folder NAME] [--apply]
  python szd_pipeline.py generate  <csv_file>   --base-dir DIR [--batch N] [--dry-run]
  python szd_pipeline.py transform --base-dir DIR --xslt FILE [--folder NAME] [--no-delete]
  python szd_pipeline.py status    --base-dir DIR [--series SZ_AAL_B2]
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 · SORT
# After Lightroom export: normalize filenames to 3-digit numbering,
# move *.tif/tiff into <signature>_TIFF/ and *_RAW_*.jpg into <signature>_RAW/.
# Regular JPGs stay in the folder root.
# Defaults to dry-run; add --apply to make changes.
# ─────────────────────────────────────────────────────────────────────────────

def _has_unprocessed_files(folder: Path) -> bool:
    """Return True if the folder still contains loose TIFF or RAW JPG files."""
    for f in folder.iterdir():
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        if ext in (".tif", ".tiff"):
            return True
        if ext == ".jpg" and "_RAW_" in f.name.upper():
            return True
    return False


def _normalize_name(name: str, signature: str) -> str:
    """Return the correctly-formatted filename with 3-digit numbering."""
    path = Path(name)
    stem = path.stem
    ext = path.suffix.lower()
    m = re.search(r"_RAW_(\d+)$", stem, re.IGNORECASE)
    if m:
        return f"{signature}_RAW_{int(m.group(1)):03d}{ext}"
    m = re.search(r"_(\d+)$", stem)
    if m:
        return f"{signature}_{int(m.group(1)):03d}{ext}"
    return name


def _process_sort_folder(folder: Path, dry_run: bool) -> None:
    signature = folder.name
    if not _has_unprocessed_files(folder):
        print(f"  skip  {signature}  (already processed)")
        return

    print(f"  {'[DRY RUN] ' if dry_run else ''}process  {signature}")
    tiff_dir = folder / f"{signature}_TIFF"
    raw_dir  = folder / f"{signature}_RAW"

    for sub in (tiff_dir, raw_dir):
        if not sub.exists():
            print(f"    mkdir  {sub.name}/")
            if not dry_run:
                sub.mkdir()

    for f in sorted(folder.iterdir()):
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        new_name = _normalize_name(f.name, signature)

        if ext in (".tif", ".tiff"):
            dest_dir = tiff_dir
        elif ext == ".jpg" and "_RAW_" in new_name.upper():
            dest_dir = raw_dir
        elif ext == ".jpg":
            dest_dir = folder  # regular JPGs stay in root
        else:
            print(f"    skip  {f.name}  (unknown type)")
            continue

        dest = dest_dir / new_name
        if dest_dir == folder:
            if new_name != f.name:
                print(f"    rename  {f.name}  →  {new_name}")
                if not dry_run:
                    f.rename(dest)
        else:
            label = "rename+move" if new_name != f.name else "move"
            print(f"    {label}  {f.name}  →  {dest_dir.name}/{new_name}")
            if not dry_run:
                shutil.move(str(f), str(dest))


def cmd_sort(args) -> None:
    root = Path(args.root)
    dry_run = not args.apply
    pattern = re.compile(rf"^{re.escape(args.series)}\.\d+$")

    if dry_run:
        print("=== DRY RUN — no files will be changed. Add --apply to execute. ===\n")
    else:
        print("=== APPLYING CHANGES ===\n")

    if args.folder:
        target = root / args.folder
        if not target.is_dir():
            print(f"Error: folder not found: {target}")
            return
        folders = [target]
    else:
        folders = sorted(
            d for d in root.iterdir() if d.is_dir() and pattern.match(d.name)
        )

    print(f"Checking {len(folders)} folder(s).\n")
    for folder in folders:
        _process_sort_folder(folder, dry_run=dry_run)
    print("\nDone.")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 · GENERATE XML
# Read a CSV file and produce one intermediate XML per row,
# written directly into the matching signature folder under base-dir.
# ─────────────────────────────────────────────────────────────────────────────

def _sanitize_filename(signatur: str) -> str:
    return signatur.replace('/', '_').replace('\\', '_').replace('-', '_')


def _format_date(date_str) -> str:
    if pd.isna(date_str) or not date_str:
        return ""
    return str(date_str).strip()


def _reverse_name(name: str) -> str:
    """Convert 'Last, First' → 'First Last'."""
    if ', ' in name:
        last, first = name.split(', ', 1)
        return f"{first} {last}"
    return name


def _generate_titel(from_person: str, to_person: str, date_str: str, signatur: str) -> str:
    german_months = {
        1: 'Januar', 2: 'Februar', 3: 'März',  4: 'April',
        5: 'Mai',    6: 'Juni',    7: 'Juli',   8: 'August',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Dezember'
    }
    from_name = _reverse_name(from_person)
    to_name   = _reverse_name(to_person)

    if date_str:
        parts = date_str.split('-')
        try:
            if len(parts) == 3:
                year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                german_date = f"{day}. {german_months[month]} {year}"
            elif len(parts) == 2:
                year, month = int(parts[0]), int(parts[1])
                german_date = f"{german_months[month]} {year}"
            else:
                german_date = parts[0]
            return f"Brief von {from_name} an {to_name} [{german_date}], {signatur}"
        except (ValueError, KeyError):
            pass

    return f"Brief von {from_name} an {to_name}, {signatur}"


def _create_xml_element(row) -> ET.Element:
    root = ET.Element('root')
    signatur    = str(row['Signatur SPÄTER FELD AF!!']).strip() if pd.notna(row['Signatur SPÄTER FELD AF!!']) else ""
    from_person = str(row['Verfasser*in']).strip()              if pd.notna(row['Verfasser*in'])              else ""
    to_person   = str(row['Adressat*in']).strip()               if pd.notna(row['Adressat*in'])               else ""
    date_str    = str(row['Datum normalisiert']).strip()         if pd.notna(row['Datum normalisiert'])         else ""

    ET.SubElement(root, 'author').text      = from_person
    ET.SubElement(root, 'contributor').text = to_person
    ET.SubElement(root, 'titel').text       = _generate_titel(from_person, to_person, date_str, signatur)
    ET.SubElement(root, 'signatur').text    = signatur
    ET.SubElement(root, 'datum').text       = _format_date(date_str)
    ET.SubElement(root, 'filename').text    = _sanitize_filename(signatur) + "_"
    ET.SubElement(root, 'category').text    = ""

    structure = ET.SubElement(root, 'structure')
    for chapter_title in ['Textseiten', 'Farbreferenz']:
        chapter = ET.SubElement(structure, 'chapter')
        ET.SubElement(chapter, 'title').text = chapter_title
        ET.SubElement(chapter, 'from').text  = ""
        ET.SubElement(chapter, 'to').text    = ""

    return root


def _prettify_xml(elem: ET.Element) -> str:
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='UTF-8').decode('utf-8')


def cmd_generate(args) -> None:
    dry_run = args.dry_run
    if dry_run:
        print("=== DRY RUN — no files will be written. Remove --dry-run to execute. ===\n")

    print(f"Reading CSV: {args.csv_file}")
    df = pd.read_csv(args.csv_file)

    expected = ['Signatur SPÄTER FELD AF!!', 'Verfasser*in', 'Adressat*in', 'Datum normalisiert']
    missing  = [col for col in expected if col not in df.columns]
    if missing:
        print(f"Warning: missing columns: {missing}")
        print(f"Available columns: {list(df.columns)}")

    # Drop trailing empty rows
    last_valid = df['Signatur SPÄTER FELD AF!!'].last_valid_index()
    if last_valid is not None:
        df = df.loc[:last_valid]

    if args.batch > 0:
        df = df.head(args.batch)

    generated = 0
    for idx, row in df.iterrows():
        try:
            if pd.isna(row['Signatur SPÄTER FELD AF!!']) or not str(row['Signatur SPÄTER FELD AF!!']).strip():
                print(f"  skip row {idx + 1}: empty Signatur")
                continue

            signatur      = str(row['Signatur SPÄTER FELD AF!!']).strip()
            folder_name   = _sanitize_filename(signatur)
            target_folder = Path(args.base_dir) / folder_name

            if not target_folder.is_dir():
                print(f"  skip row {idx + 1}: folder not found: {target_folder}")
                continue

            filename = folder_name + '.xml'
            filepath = target_folder / filename

            if filepath.exists():
                print(f"  skip  {filename}  (already exists)")
                continue

            if dry_run:
                print(f"  [DRY RUN] would generate: {folder_name}/{filename}")
            else:
                xml_string = _prettify_xml(_create_xml_element(row))
                filepath.write_text(xml_string, encoding='utf-8')
                print(f"  generated: {folder_name}/{filename}")

            generated += 1
        except Exception as e:
            print(f"  error at row {idx + 1}: {e}")

    action = "Would generate" if dry_run else "Generated"
    print(f"\n{action} {generated} XML file(s).")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 · TRANSFORM (XSLT → METS)
# Apply the XSLT stylesheet to each <signature>.xml and write Result_<signature>.xml.
# Source XMLs are deleted after a successful transformation (unless --no-delete).
# Run this AFTER manually reviewing each XML and filling in page number ranges.
# ─────────────────────────────────────────────────────────────────────────────

def _validate_xml(folder_path: Path, folder_name: str) -> list[str]:
    """
    Validate an intermediate XML before transformation. Returns a list of
    error strings; empty list means the XML is ready to transform.

    Checks:
      - All <from> and <to> values are filled in and are valid integers
      - Every JPG referenced by each chapter's page range exists in the folder
    """
    xml_path = folder_path / f"{folder_name}.xml"
    errors = []

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        return [f"XML parse error: {e}"]

    filename_elem = root.find('filename')
    filename_prefix = filename_elem.text.strip() if filename_elem is not None and filename_elem.text else ""

    for chapter in root.findall('.//chapter'):
        title_elem = root.find('.//chapter/title')
        title = chapter.findtext('title') or '(unnamed chapter)'
        from_text = (chapter.findtext('from') or "").strip()
        to_text   = (chapter.findtext('to')   or "").strip()

        if not from_text or not to_text:
            errors.append(f"Chapter '{title}': <from> or <to> is empty — fill in page numbers")
            continue

        try:
            page_from = int(from_text)
            page_to   = int(to_text)
        except ValueError:
            errors.append(f"Chapter '{title}': <from>/{from_text!r} or <to>/{to_text!r} is not an integer")
            continue

        if page_from > page_to:
            errors.append(f"Chapter '{title}': <from> ({page_from}) is greater than <to> ({page_to})")
            continue

        if filename_prefix:
            for page_num in range(page_from, page_to + 1):
                jpg_name = f"{filename_prefix}{page_num:03d}.jpg"
                if not (folder_path / jpg_name).exists():
                    errors.append(f"Chapter '{title}': referenced file not found: {jpg_name}")

    return errors


def cmd_transform(args) -> None:
    try:
        from saxonche import PySaxonProcessor
    except ImportError:
        print("Error: saxonche is not installed. Run: pip install saxonche")
        sys.exit(1)

    base_dir  = Path(args.base_dir)
    xslt_file = args.xslt
    no_delete = args.no_delete

    sig_pattern = re.compile(r"^SZ_AAL_B\d+\.\d+$")

    if args.folder:
        target = base_dir / args.folder
        if not target.is_dir():
            print(f"Error: folder not found: {target}")
            return
        subfolders = [args.folder]
    else:
        subfolders = sorted(
            [f for f in os.listdir(base_dir) if sig_pattern.match(f)],
            key=lambda f: int(f.split(".")[-1])
        )

    if not subfolders:
        print(f"No matching signature folders found in: {base_dir}")
        return

    # ── validation pass ───────────────────────────────────────────────────────
    print("Validating XMLs before transformation...\n")
    invalid = []
    for folder_name in subfolders:
        folder_path = base_dir / folder_name
        input_path  = folder_path / f"{folder_name}.xml"
        result_path = folder_path / f"Result_{folder_name}.xml"

        if result_path.exists() or not input_path.exists():
            continue  # will be skipped in transform pass anyway

        errors = _validate_xml(folder_path, folder_name)
        if errors:
            invalid.append(folder_name)
            print(f"  ✗ {folder_name}")
            for err in errors:
                print(f"      {err}")
        else:
            print(f"  ✓ {folder_name}")

    if invalid:
        print(f"\n{len(invalid)} folder(s) failed validation. Fix the issues above before transforming.")
        sys.exit(1)

    print("\nAll XMLs valid. Starting transformation...\n")

    # ── transform pass ────────────────────────────────────────────────────────
    transformed = []
    with PySaxonProcessor(license=False) as proc:
        xslt_proc  = proc.new_xslt30_processor()
        executable = xslt_proc.compile_stylesheet(stylesheet_file=xslt_file)

        for folder_name in subfolders:
            folder_path = base_dir / folder_name
            input_path  = str(folder_path / f"{folder_name}.xml")
            output_path = str(folder_path / f"Result_{folder_name}.xml")

            if os.path.exists(output_path):
                print(f"  skip  {folder_name}  (result already exists)")
                continue
            if not os.path.exists(input_path):
                print(f"  skip  {folder_name}  (no input XML found)")
                continue

            print(f"  transform  {folder_name} ...")
            try:
                executable.transform_to_file(source_file=input_path, output_file=output_path)
                transformed.append(folder_name)
            except Exception as e:
                print(f"  ERROR at {folder_name}: {e}")

    # ── cleanup pass ──────────────────────────────────────────────────────────
    if no_delete:
        print(f"\nTransformed {len(transformed)} file(s). Source XMLs kept (--no-delete).")
    else:
        print(f"\nTransformed {len(transformed)} file(s). Removing source XMLs...")
        for folder_name in transformed:
            input_path = base_dir / folder_name / f"{folder_name}.xml"
            if input_path.exists():
                input_path.unlink()
                print(f"  deleted  {input_path.name}")

    print("\nAll done.")


# ─────────────────────────────────────────────────────────────────────────────
# STATUS
# Scan base-dir and report the processing stage of every signature folder.
# ─────────────────────────────────────────────────────────────────────────────

# Stage labels and their sort order (lower = earlier in pipeline)
_STAGES = {
    "done":         ("✓ done",         0),
    "ready":        ("◉ ready",        1),
    "needs_review": ("✎ needs review", 2),
    "no_xml":       ("○ no xml",       3),
    "no_jpgs":      ("! no jpgs",      4),
}


def _folder_stage(folder_path: Path, folder_name: str) -> str:
    """Return one of the _STAGES keys for the given signature folder."""
    result_xml = folder_path / f"Result_{folder_name}.xml"
    input_xml  = folder_path / f"{folder_name}.xml"
    jpgs = list(folder_path.glob("*.jpg"))

    if result_xml.exists():
        return "done"

    if not jpgs:
        return "no_jpgs"

    if not input_xml.exists():
        return "no_xml"

    # XML exists — check if page numbers have been filled in
    errors = _validate_xml(folder_path, folder_name)
    if errors:
        return "needs_review"
    return "ready"


def cmd_status(args) -> None:
    base_dir = Path(args.base_dir)
    pattern  = re.compile(rf"^{re.escape(args.series)}\.\d+$")

    folders = sorted(
        [d for d in base_dir.iterdir() if d.is_dir() and pattern.match(d.name)],
        key=lambda d: int(d.name.split(".")[-1])
    )

    if not folders:
        print(f"No matching folders found in: {base_dir}")
        return

    counts = {key: 0 for key in _STAGES}
    rows   = []

    for folder in folders:
        stage = _folder_stage(folder, folder.name)
        counts[stage] += 1
        label, _ = _STAGES[stage]
        rows.append((label, folder.name))

    # Print table grouped by stage
    col_width = max(len(name) for _, name in rows) + 2
    current_stage = None
    for label, name in rows:
        if label != current_stage:
            print(f"\n{label}")
            current_stage = label
        print(f"  {name}")

    # Summary
    print("\n── Summary " + "─" * 30)
    for key, (label, _) in _STAGES.items():
        if counts[key]:
            print(f"  {label:<20}  {counts[key]}")
    print(f"  {'total':<20}  {len(folders)}")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="szd_pipeline.py",
        description="Unified pipeline for the Stefan Zweig Digital Archive.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Steps (run in order):
  1. sort       After Lightroom export: normalize filenames, move TIFF/RAW into subfolders
  2. generate   Generate intermediate XML directly into each signature folder
                ── MANUAL: open each XML and fill in the page number ranges ──
  3. transform  Apply XSLT to produce final METS viewer XML (Result_*.xml)

Additional:
  status        Show the current stage of every signature folder
        """
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ── step 1: sort ──────────────────────────────────────────────────────────
    p_sort = sub.add_parser("sort", help="Step 1: Sort and rename Lightroom output files")
    p_sort.add_argument("--root",   default=".", metavar="DIR",
                        help="Root directory containing the signature folders (default: .)")
    p_sort.add_argument("--series", default="SZ_AAL_B2", metavar="PREFIX",
                        help="Signature series prefix to match (default: SZ_AAL_B2)")
    p_sort.add_argument("--folder", metavar="NAME",
                        help="Process only this subfolder, e.g. SZ_AAL_B2.5")
    p_sort.add_argument("--apply",  action="store_true",
                        help="Apply changes (default: dry-run, no files modified)")

    # ── step 2: generate ──────────────────────────────────────────────────────
    p_gen = sub.add_parser("generate", help="Step 2: Generate intermediate XML directly into signature folders")
    p_gen.add_argument("csv_file", help="Path to the CSV metadata file")
    p_gen.add_argument("--base-dir", required=True, metavar="DIR",
                       help="Root directory containing the signature folders (same as --root in sort)")
    p_gen.add_argument("--batch",   type=int, default=0, metavar="N",
                       help="Process only the first N rows (0 = all rows)")
    p_gen.add_argument("--dry-run", action="store_true",
                       help="Preview which XMLs would be created without writing any files")

    # ── step 3: transform ─────────────────────────────────────────────────────
    p_tr = sub.add_parser("transform",
                           help="Step 3: XSLT transformation → METS viewer XML (run after manual review)")
    p_tr.add_argument("--base-dir",  required=True, metavar="DIR",
                      help="Directory containing the signature subfolders")
    p_tr.add_argument("--xslt",      required=True, metavar="FILE",
                      help="Path to the XSLT stylesheet (szd-JPGtoMETS.xsl)")
    p_tr.add_argument("--folder",    metavar="NAME",
                      help="Transform only this one folder, e.g. SZ_AAL_B2.5")
    p_tr.add_argument("--no-delete", action="store_true",
                      help="Keep source XML after transformation instead of deleting it")

    # ── status ────────────────────────────────────────────────────────────────
    p_st = sub.add_parser("status", help="Show the current processing stage of every signature folder")
    p_st.add_argument("--base-dir", required=True, metavar="DIR",
                      help="Root directory containing the signature folders")
    p_st.add_argument("--series",   default="SZ_AAL_B2", metavar="PREFIX",
                      help="Signature series prefix to match (default: SZ_AAL_B2)")

    args = parser.parse_args()

    dispatch = {
        "sort":      cmd_sort,
        "generate":  cmd_generate,
        "transform": cmd_transform,
        "status":    cmd_status,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
