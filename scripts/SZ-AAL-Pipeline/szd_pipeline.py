#!/usr/bin/env python3
"""
szd_pipeline.py — Unified processing pipeline for the Stefan Zweig Digital Archive (SZ-AAL).

PIPELINE STAGES
---------------
Run these steps in order for each batch of newly digitized items:

  1. sort       Normalize Lightroom export filenames to 3-digit numbering and move
                TIFF/RAW files into per-signature subfolders.

  2. generate   Read the catalog CSV and write one intermediate XML per item directly
                into the matching signature folder. The XML contains all metadata plus
                a <structure> block with empty page-range fields (<from>/<to>).

  2b. autofill  Auto-fill the <from>/<to> page ranges from the JPG count in each folder.
                Farbreferenz → last page, Kuvert → 2 pages before it, Textseiten → rest.
                Review and correct any flagged outliers before the next step.

                ── REVIEW: open flagged XMLs and correct page ranges if needed ──

  3. transform  Validate each reviewed XML (checks page ranges, referenced JPGs), then
                apply the XSLT stylesheet (szd-JPGtoMETS.xsl) to produce the final METS
                viewer file (Result_<signature>.xml). Source XMLs are deleted after a
                successful transformation unless --no-delete is given.

  4. batch      Collect all newly finished Result XMLs into a numbered, dated batch
                folder under _batches/. Batch membership is tracked via manifests;
                re-running only picks up items not yet listed in any batch.

ADDITIONAL COMMANDS
-------------------
  validate      Post-transform audit: XML validity, metadata completeness, image
                references, naming conventions, and numbering gaps.
  status        Show the current pipeline stage of every signature folder, grouped
                by stage. Batched items are listed under their batch name.

USAGE
-----
  python szd_pipeline.py sort      [--root DIR] [--series SZ_AAL_B2] [--folder NAME] [--apply]
  python szd_pipeline.py generate  <csv_file>   --base-dir DIR [--limit N] [--dry-run]
  python szd_pipeline.py autofill  --base-dir DIR [--series SZ_AAL_B] [--folder NAME] [--apply]
  python szd_pipeline.py transform --base-dir DIR --xslt FILE [--series SZ_AAL_B] [--folder NAME] [--no-delete] [--yes]
  python szd_pipeline.py batch     --base-dir DIR [--series SZ_AAL_B] [--limit N] [--name NAME] [--dry-run]
  python szd_pipeline.py validate  --base-dir DIR [--series SZ_AAL_B]
  python szd_pipeline.py status    --base-dir DIR [--series SZ_AAL_B]
"""

import argparse
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom


# ─────────────────────────────────────────────────────────────────────────────
# SHARED HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _folder_sort_key(name: str) -> list:
    """
    Natural numeric sort key for signature folder names.

    Handles all variants: SZ_AAL_B4.1, SZ_AAL_B11, SZ_AAL_B1.109a, SZ_AAL_B5.7.1.
    Returns a list of (int, str) tuples for each dotted component, e.g.
      SZ_AAL_B4.1   → [(4,''), (1,'')]
      SZ_AAL_B11    → [(11,'')]
      SZ_AAL_B1.109a→ [(1,''), (109,'a')]
    """
    result = []
    for part in name.split('.'):
        m = re.search(r'(\d+)([a-z]*)$', part, re.IGNORECASE)
        if m:
            result.append((int(m.group(1)), m.group(2).lower()))
    return result


def _series_pattern(series: str) -> re.Pattern:
    """
    Build a regex matching signature folder names for the given series prefix.

    - Specific series (ends with digit, e.g. 'SZ_AAL_B2'):
        matches SZ_AAL_B2, SZ_AAL_B2.1, SZ_AAL_B2.97
    - Broad prefix (ends with letter, e.g. 'SZ_AAL_B'):
        matches SZ_AAL_B4.1, SZ_AAL_B11, SZ_AAL_B1.109a, SZ_AAL_B5.7.1
    """
    escaped = re.escape(series)
    if re.search(r'\d$', series):
        return re.compile(rf"^{escaped}(\.\d+[a-z]?)*$")
    else:
        return re.compile(rf"^{escaped}\d+(\.\d+[a-z]?)*$")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 · SORT
#
# After Lightroom export: normalize filenames to 3-digit numbering,
# move *.tif/tiff into <signature>_TIFF/ and *_RAW_*.jpg into <signature>_RAW/.
# Regular JPGs stay in the folder root.
# Defaults to dry-run; add --apply to make changes.
# ─────────────────────────────────────────────────────────────────────────────

def _has_unprocessed_files(folder: Path) -> bool:
    """Return True if the folder still contains loose TIFF or RAW JPG files that need sorting."""
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
    """
    Return the correctly-formatted filename with 3-digit zero-padded numbering.

    Examples:
      SZ_AAL_B2.5_3.jpg    → SZ_AAL_B2.5_003.jpg
      SZ_AAL_B2.5_RAW_12.jpg → SZ_AAL_B2.5_RAW_012.jpg
    """
    path = Path(name)
    stem = path.stem
    ext = path.suffix.lower()

    m = re.search(r"_RAW_(\d+)$", stem, re.IGNORECASE)
    if m:
        return f"{signature}_RAW_{int(m.group(1)):03d}{ext}"

    m = re.search(r"_(\d+)$", stem)
    if m:
        return f"{signature}_{int(m.group(1)):03d}{ext}"

    return name  # unrecognized pattern — leave untouched


def _process_sort_folder(folder: Path, dry_run: bool) -> None:
    """
    Sort and rename all files in one signature folder.

    - TIF/TIFF files  → deleted (not part of the JPG-based pipeline)
    - RAW JPGs        → deleted (_RAW_ in filename signals a scanner duplicate)
    - Regular JPGs    → stay in root (renamed in place if numbering needs padding)
    """
    signature = folder.name
    if not _has_unprocessed_files(folder):
        print(f"  skip  {signature}  (already processed)")
        return

    print(f"  {'[DRY RUN] ' if dry_run else ''}process  {signature}")

    for f in sorted(folder.iterdir()):
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        new_name = _normalize_name(f.name, signature)

        if ext in (".tif", ".tiff"):
            print(f"    delete  {f.name}  (TIF not used in pipeline)")
            if not dry_run:
                f.unlink()
        elif ext == ".jpg" and "_RAW_" in new_name.upper():
            print(f"    delete  {f.name}  (RAW duplicate)")
            if not dry_run:
                f.unlink()
        elif ext == ".jpg":
            if new_name != f.name:
                print(f"    rename  {f.name}  →  {new_name}")
                if not dry_run:
                    f.rename(folder / new_name)
        else:
            print(f"    skip  {f.name}  (unknown type)")


def cmd_sort(args) -> None:
    """
    Step 1: Sort and rename Lightroom output files in all signature folders.

    Skips folders that have already been processed (no loose TIFF or RAW files).
    Runs as a dry-run by default; pass --apply to make changes.
    """
    root    = Path(args.root)
    dry_run = not args.apply
    pattern = _series_pattern(args.series)

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
            (d for d in root.iterdir() if d.is_dir() and pattern.match(d.name)),
            key=lambda d: _folder_sort_key(d.name)
        )

    print(f"Checking {len(folders)} folder(s).\n")
    for folder in folders:
        _process_sort_folder(folder, dry_run=dry_run)
    print("\nDone.")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 · GENERATE XML
#
# Read the catalog CSV and produce one intermediate XML per row, written
# directly into the matching signature folder under base-dir.
# The generated XML contains all catalog metadata plus an empty <structure>
# block that the editor must fill in (page number ranges) before transforming.
# ─────────────────────────────────────────────────────────────────────────────

def _sanitize_filename(signatur: str) -> str:
    """Convert a signatur string to a safe filename by replacing path separators and dashes."""
    return signatur.replace('/', '_').replace('\\', '_').replace('-', '_')


def _format_date(date_str) -> str:
    """Return the normalized date string, or an empty string if missing."""
    if pd.isna(date_str) or not date_str:
        return ""
    return str(date_str).strip()


def _reverse_name(name: str) -> str:
    """Convert 'Last, First' to 'First Last'. Returns the name unchanged if no comma is present."""
    if ', ' in name:
        last, first = name.split(', ', 1)
        return f"{first} {last}"
    return name


def _doc_type(art_umfang: str) -> str:
    """
    Extract the document type from 'Art/Umfang', e.g. 'Brief', 'Telegramm', 'Kuvert'.

    The field has the form '1 Brief, Manuskript, 2 Blatt' — the type is the first
    word after the leading count. Falls back to 'Brief' if the field is empty or
    unparseable.
    """
    if not art_umfang:
        return "Brief"
    m = re.match(r'\d+\s+(\w+)', art_umfang.strip())
    return m.group(1) if m else "Brief"


def _generate_titel(from_person: str, to_person: str, date_str: str, signatur: str,
                    art_umfang: str = "") -> str:
    """
    Build the German-language title string for a document.

    The document type is derived from 'Art/Umfang' (defaults to 'Brief').
    Participant string depends on what is available:
      both author and recipient  →  '{type} von {sender} an {recipient}'
      author only                →  '{type} von {author}'
      neither                    →  '{type}'
    The date is formatted in German (e.g. '15. März 1939'). If missing or
    unparseable, the date bracket is omitted.
    """
    german_months = {
        1: 'Januar', 2: 'Februar', 3: 'März',  4: 'April',
        5: 'Mai',    6: 'Juni',    7: 'Juli',   8: 'August',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Dezember'
    }
    doc_type  = _doc_type(art_umfang)
    from_name = _reverse_name(from_person) if from_person else ""
    to_name   = _reverse_name(to_person)   if to_person   else ""

    if from_name and to_name:
        participants = f" von {from_name} an {to_name}"
    elif from_name:
        participants = f" von {from_name}"
    else:
        participants = ""

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
                german_date = parts[0]  # year only
            return f"{doc_type}{participants} [{german_date}], {signatur}"
        except (ValueError, KeyError):
            pass

    return f"{doc_type}{participants}, {signatur}"


def _create_xml_element(row, sig_col: str) -> ET.Element:
    """
    Build the intermediate XML element tree for one CSV row.

    Supports two series modes detected from CSV columns:

    B-series (Briefe/Korrespondenz) — 'Art/Umfang' present:
      author=Verfasser*in, contributor=Adressat*in
      title generated from sender/recipient/date
      chapters: Textseiten, Farbreferenz [, Kuvert if Art/Umfang contains 'Kuvert']

    L-series (Lebensdokumente) — 'Titel (original)' present:
      author=Verfasser*in, contributor=Betroffene Person
      title=Titel (original) [fallback: fingiert → assigned], appended with signatur
      chapters: Textseiten [, Beilagen if Beilagen column non-empty], Farbreferenz
    """
    root = ET.Element('root')

    def _cell(col):
        return str(row[col]).strip() if col in row.index and pd.notna(row[col]) else ""

    signatur = _cell(sig_col)
    date_str = _cell('Datum normalisiert')

    is_lebensdokument = 'Titel (original)' in row.index

    if is_lebensdokument:
        author      = _cell('Verfasser*in')
        contributor = _cell('Betroffene Person')
        titel_raw   = (_cell('Titel (original)') or
                       _cell('Titel (fingiert)')  or
                       _cell('Titel (assigned)')  or "")
        titel        = f"{titel_raw}, {signatur}" if titel_raw else signatur
        has_kuvert   = False
        has_beilagen = bool(_cell('Beilagen'))
    else:
        author      = _cell('Verfasser*in')
        contributor = _cell('Adressat*in')
        art_umfang  = _cell('Art/Umfang')
        titel        = _generate_titel(author, contributor, date_str, signatur, art_umfang)
        has_kuvert   = 'Kuvert' in art_umfang
        has_beilagen = False

    ET.SubElement(root, 'author').text      = author
    ET.SubElement(root, 'contributor').text = contributor
    ET.SubElement(root, 'titel').text       = titel
    ET.SubElement(root, 'signatur').text    = signatur
    ET.SubElement(root, 'datum').text       = _format_date(date_str)
    ET.SubElement(root, 'filename').text    = _sanitize_filename(signatur) + "_"
    ET.SubElement(root, 'category').text    = ""

    # Build chapter list in semantic order
    if is_lebensdokument:
        chapter_titles = ['Textseiten']
        if has_beilagen:
            chapter_titles.append('Beilagen')
        chapter_titles.append('Farbreferenz')
    else:
        chapter_titles = ['Textseiten', 'Farbreferenz']
        if has_kuvert:
            chapter_titles.append('Kuvert')

    structure = ET.SubElement(root, 'structure')
    for chapter_title in chapter_titles:
        chapter = ET.SubElement(structure, 'chapter')
        ET.SubElement(chapter, 'title').text = chapter_title
        ET.SubElement(chapter, 'from').text  = ""
        ET.SubElement(chapter, 'to').text    = ""

    return root


def _prettify_xml(elem: ET.Element) -> str:
    """Return a UTF-8 encoded, indented XML string for the given element."""
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='UTF-8').decode('utf-8')


def cmd_generate(args) -> None:
    """
    Step 2: Generate intermediate XML files from the catalog CSV.

    One XML is written per CSV row, directly into the matching signature folder
    (e.g. SZ_AAL_B2.61/SZ_AAL_B2.61.xml). Rows whose target folder does not
    exist or whose XML already exists are skipped.

    After generation, open each XML and fill in the <from>/<to> page numbers
    in the <structure> block before running the transform step.
    """
    dry_run = args.dry_run
    if dry_run:
        print("=== DRY RUN — no files will be written. Remove --dry-run to execute. ===\n")

    src = args.csv_file
    print(f"Reading metadata: {src}")
    if src.lower().endswith(('.xlsx', '.xls')):
        df = pd.read_excel(src)
    else:
        df = pd.read_csv(src, sep=None, engine='python', encoding='utf-8-sig')

    # ── Resolve signature column ──────────────────────────────────────────────
    if args.sig_col:
        sig_col = args.sig_col
        if sig_col not in df.columns:
            print(f"Error: --sig-col {sig_col!r} not found. Available: {list(df.columns)}")
            return
    else:
        # Auto-detect: first column whose name contains 'signatur' (case-insensitive)
        candidates = [c for c in df.columns if 'signatur' in c.lower()]
        if candidates:
            sig_col = candidates[0]
            if len(candidates) > 1:
                print(f"  Note: multiple signature columns found, using {sig_col!r}")
        else:
            sig_col = df.columns[0]
            print(f"  Warning: no column containing 'signatur' found; "
                  f"falling back to first column: {sig_col!r}")

    for col in ('Verfasser*in', 'Adressat*in', 'Datum normalisiert'):
        if col not in df.columns:
            print(f"  Warning: column {col!r} not found — will be left empty in XMLs")

    # Drop trailing empty rows that appear after the last valid data row
    last_valid = df[sig_col].last_valid_index()
    if last_valid is not None:
        df = df.loc[:last_valid]

    if args.limit > 0:
        df = df.head(args.limit)

    generated = 0
    for idx, row in df.iterrows():
        try:
            if pd.isna(row[sig_col]) or not str(row[sig_col]).strip():
                print(f"  skip row {idx + 1}: empty Signatur")
                continue

            signatur      = str(row[sig_col]).strip()
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

            result_path = target_folder / f"Result_{folder_name}.xml"
            if result_path.exists():
                print(f"  skip  {folder_name}  (already transformed)")
                continue

            if dry_run:
                print(f"  [DRY RUN] would generate: {folder_name}/{filename}")
            else:
                xml_string = _prettify_xml(_create_xml_element(row, sig_col))
                filepath.write_text(xml_string, encoding='utf-8')
                print(f"  generated: {folder_name}/{filename}")

            generated += 1
        except Exception as e:
            print(f"  error at row {idx + 1}: {e}")

    action = "Would generate" if dry_run else "Generated"
    print(f"\n{action} {generated} XML file(s).")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 · TRANSFORM (XSLT → METS)
#
# Validates each intermediate XML (page ranges filled in, JPGs present), then
# applies the XSLT stylesheet to produce Result_<signature>.xml.
# Source XMLs are deleted after a successful transformation (unless --no-delete).
# ─────────────────────────────────────────────────────────────────────────────

def _validate_xml(folder_path: Path, folder_name: str) -> list[str]:
    """
    Validate an intermediate XML before transformation.

    Checks:
      - The XML is well-formed and parseable.
      - Every chapter's <from> and <to> values are present and are valid integers.
      - <from> is not greater than <to>.
      - Every JPG referenced by each chapter's page range exists in the folder.

    Returns a list of error strings. An empty list means the XML is ready to transform.
    """
    xml_path = folder_path / f"{folder_name}.xml"
    errors = []

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        return [f"XML parse error: {e}"]

    filename_elem  = root.find('filename')
    filename_prefix = filename_elem.text.strip() if filename_elem is not None and filename_elem.text else ""

    for chapter in root.findall('.//chapter'):
        title      = chapter.findtext('title') or '(unnamed chapter)'
        from_text  = (chapter.findtext('from') or "").strip()
        to_text    = (chapter.findtext('to')   or "").strip()

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


def _compute_page_assignments(T: int, has_kuvert: bool) -> dict[str, tuple[int, int]]:
    """
    Compute page-range assignments for T total JPGs.

    Semantic order (always):  Textseiten | [Kuvert] | Farbreferenz
      Farbreferenz → last page (T)
      Kuvert       → up to 2 pages immediately before Farbreferenz
                     (capped at min(2, T-2) to leave ≥1 page for Textseiten)
      Textseiten   → pages 1 through the start of Kuvert/Farbreferenz
    """
    assignments: dict[str, tuple[int, int]] = {}
    assignments['Farbreferenz'] = (T, T)

    if has_kuvert:
        kuvert_pages = max(1, min(2, T - 2))   # T-2 leaves 1 page for Textseiten
        kuvert_from  = T - kuvert_pages          # = T-1 or T-2
        kuvert_to    = T - 1
        assignments['Kuvert']     = (kuvert_from, kuvert_to)
        assignments['Textseiten'] = (1, kuvert_from - 1)
    else:
        assignments['Textseiten'] = (1, T - 1)

    return assignments


def _autofill_xml(folder_path: Path, folder_name: str, write: bool = True) -> tuple[bool, str]:
    """
    Compute auto-fill page ranges for one intermediate XML.

    Pages are assigned by semantic role (Farbreferenz=last, Kuvert=just before,
    Textseiten=everything else), not by chapter order in the XML.

    If write=True, the updated XML is written to disk.
    Returns (success: bool, summary: str).
    """
    xml_path = folder_path / f"{folder_name}.xml"
    if not xml_path.exists():
        return False, "no intermediate XML"
    if (folder_path / f"Result_{folder_name}.xml").exists():
        return False, "already transformed — skipping"

    try:
        tree = ET.parse(xml_path)
    except ET.ParseError as e:
        return False, f"XML parse error: {e}"

    root = tree.getroot()

    filename_elem = root.find('filename')
    raw_prefix = filename_elem.text.strip() if filename_elem is not None and filename_elem.text else ""
    prefix = raw_prefix.rstrip('_') or folder_name  # strip trailing _ (sometimes added by generator)

    all_jpgs      = sorted(f for f in folder_path.iterdir() if f.suffix.lower() == '.jpg')
    # Only count standard-format pages: {prefix}_NNN.jpg (exactly 3 digits, no dashes, no _RAW_)
    std_pat       = re.compile(rf"^{re.escape(prefix)}_\d{{3}}\.jpg$", re.IGNORECASE)
    prefix_jpgs   = [f for f in all_jpgs if std_pat.match(f.name)]
    name_mismatch = len(prefix_jpgs) == 0 and len(all_jpgs) > 0

    jpgs = all_jpgs if name_mismatch else prefix_jpgs
    T    = len(jpgs)
    if T == 0:
        return False, "no JPGs found"

    chapters = root.findall('.//chapter')
    if not chapters:
        return False, "no chapters in XML structure"

    titles = [(chapter.findtext('title') or '').strip() for chapter in chapters]
    has_kuvert   = 'Kuvert'   in titles
    has_beilagen = 'Beilagen' in titles

    if T < len(chapters):
        return False, f"only {T} JPG(s) for {len(chapters)} chapter(s) — check manually"

    if has_beilagen:
        # Can't auto-split Textseiten vs Beilagen — assign only Farbreferenz
        # and flag so the user fills in the two ranges manually.
        assignments = {'Farbreferenz': (T, T)}
        flagged_msg = (f"T={T}: Farbreferenz={T}-{T} "
                       f"— set Textseiten and Beilagen page ranges manually")
    else:
        assignments = _compute_page_assignments(T, has_kuvert)
        flagged_msg = None

    for chapter in chapters:
        title = (chapter.findtext('title') or '').strip()
        if title not in assignments:
            continue
        page_from, page_to = assignments[title]
        from_elem = chapter.find('from')
        to_elem   = chapter.find('to')
        if from_elem is not None:
            from_elem.text = str(page_from)
        if to_elem is not None:
            to_elem.text = str(page_to)

    if write:
        xml_path.write_text(_prettify_xml(root), encoding='utf-8')

    if flagged_msg:
        return False, flagged_msg

    summary_order = ['Textseiten', 'Kuvert', 'Farbreferenz']
    parts = [f"{t}={assignments[t][0]}-{assignments[t][1]}"
             for t in summary_order if t in assignments]
    suffix = " [filename mismatch — rename JPGs]" if name_mismatch else ""
    return True, f"T={T}: {', '.join(parts)}{suffix}"


def cmd_autofill(args) -> None:
    """
    Step 2b: Auto-fill page ranges in intermediate XMLs from JPG counts.

    For each folder that has an intermediate XML but no Result XML, counts the
    JPG files and fills in <from>/<to> for every chapter using this rule:
      • Farbreferenz → always the last JPG
      • Kuvert       → the 2 pages before Farbreferenz (1 page if space is tight)
      • Textseiten   → all pages from 1 to the start of the above

    Outliers (e.g. unexpected page counts) are flagged so you can review them.
    Runs as dry-run by default; add --apply to write changes.
    """
    base_dir = Path(args.base_dir)
    pattern  = _series_pattern(args.series)
    dry_run  = not args.apply

    if dry_run:
        print("=== DRY RUN — no files will be changed. Add --apply to write. ===\n")

    if args.folder:
        target = base_dir / args.folder
        if not target.is_dir():
            print(f"Error: folder not found: {target}")
            return
        folders = [target]
    else:
        folders = sorted(
            [d for d in base_dir.iterdir() if d.is_dir() and pattern.match(d.name)],
            key=lambda d: _folder_sort_key(d.name)
        )

    filled = skipped = flagged = 0
    for folder in folders:
        name = folder.name

        if not (folder / f"{name}.xml").exists():
            continue  # not yet at generate stage

        ok, summary = _autofill_xml(folder, name, write=not dry_run)

        if "skipping" in summary or "no intermediate" in summary:
            skipped += 1
        elif not ok:
            print(f"  WARN   {name}: {summary}")
            flagged += 1
        else:
            verb = "would fill" if dry_run else "filled"
            print(f"  {verb}  {name}: {summary}")
            filled += 1

    verb = "Would fill" if dry_run else "Filled"
    print(f"\n{verb} {filled} XML(s). Skipped: {skipped}. Flagged for review: {flagged}.")


def cmd_transform(args) -> None:
    """
    Step 3: Apply the XSLT stylesheet to produce final METS viewer XML files.

    Runs in two passes:
      1. Validation pass — checks all pending XMLs for filled-in page ranges and
         existing JPG files. Aborts if any XML fails validation.
      2. Transform pass  — applies the XSLT to each valid XML via SaxonCHE,
         writing Result_<signature>.xml alongside the source files.
      3. Cleanup pass    — deletes source XMLs that were successfully transformed
         (skipped if --no-delete is given).
    """
    try:
        from saxonche import PySaxonProcessor
    except ImportError:
        print("Error: saxonche is not installed. Run: pip install saxonche")
        sys.exit(1)

    base_dir  = Path(args.base_dir)
    xslt_file = args.xslt
    no_delete = args.no_delete

    sig_pattern = _series_pattern(args.series)

    if args.folder:
        target = base_dir / args.folder
        if not target.is_dir():
            print(f"Error: folder not found: {target}")
            return
        subfolders = [args.folder]
    else:
        subfolders = sorted(
            [d.name for d in base_dir.iterdir() if d.is_dir() and sig_pattern.match(d.name)],
            key=_folder_sort_key
        )

    if not subfolders:
        print(f"No matching signature folders found in: {base_dir}")
        return

    # ── Interactive skip prompt ───────────────────────────────────────────────
    # Show only folders that are actually pending (have input XML, no result yet)
    pending_folders = [
        f for f in subfolders
        if (base_dir / f / f"{f}.xml").exists()
        and not (base_dir / f / f"Result_{f}.xml").exists()
    ]
    if pending_folders and not args.yes:
        print("Folders pending transformation:")
        for i, name in enumerate(pending_folders, 1):
            print(f"  [{i:3}] {name}")
        print()
        raw = input("Enter numbers or folder names to SKIP (comma-separated), or press Enter to transform all: ").strip()
        skip = set()
        if raw:
            for token in raw.split(","):
                token = token.strip()
                if token.isdigit():
                    idx = int(token) - 1
                    if 0 <= idx < len(pending_folders):
                        skip.add(pending_folders[idx])
                    else:
                        print(f"  Warning: index {token} out of range, ignored")
                elif token:
                    if token in pending_folders:
                        skip.add(token)
                    else:
                        print(f"  Warning: '{token}' not in pending list, ignored")
        if skip:
            print(f"\nSkipping: {', '.join(sorted(skip))}\n")
            subfolders = [f for f in subfolders if f not in skip]
        else:
            print()

    # ── Validation pass ───────────────────────────────────────────────────────
    print("Validating XMLs before transformation...\n")
    invalid = []
    for folder_name in subfolders:
        folder_path = base_dir / folder_name
        input_path  = folder_path / f"{folder_name}.xml"
        result_path = folder_path / f"Result_{folder_name}.xml"

        if result_path.exists() or not input_path.exists():
            continue  # will be skipped in the transform pass anyway

        errors = _validate_xml(folder_path, folder_name)
        if errors:
            invalid.append(folder_name)
            print(f"  [FAIL] {folder_name}")
            for err in errors:
                print(f"      {err}")
        else:
            print(f"  [OK] {folder_name}")

    if invalid:
        print(f"\n{len(invalid)} folder(s) failed validation. Fix the issues above before transforming.")
        sys.exit(1)

    print("\nAll XMLs valid. Starting transformation...\n")

    # ── Transform pass ────────────────────────────────────────────────────────
    transformed = []
    with PySaxonProcessor(license=False) as proc:
        xslt_proc  = proc.new_xslt30_processor()
        executable = xslt_proc.compile_stylesheet(stylesheet_file=xslt_file)

        for folder_name in subfolders:
            folder_path = base_dir / folder_name
            input_path  = folder_path / f"{folder_name}.xml"
            output_path = folder_path / f"Result_{folder_name}.xml"

            if output_path.exists():
                print(f"  skip  {folder_name}  (result already exists)")
                continue
            if not input_path.exists():
                print(f"  skip  {folder_name}  (no input XML found)")
                continue

            print(f"  transform  {folder_name} ...")
            try:
                executable.transform_to_file(source_file=str(input_path), output_file=str(output_path))
                transformed.append(folder_name)
            except Exception as e:
                print(f"  ERROR at {folder_name}: {e}")

    # ── Cleanup pass ──────────────────────────────────────────────────────────
    if no_delete:
        print(f"\nTransformed {len(transformed)} file(s). Source XMLs kept (--no-delete).")
    else:
        print(f"\nTransformed {len(transformed)} file(s). Cleaning up...")
        for folder_name in transformed:
            folder_path = base_dir / folder_name

            input_path = folder_path / f"{folder_name}.xml"
            if input_path.exists():
                input_path.unlink()
                print(f"  deleted  {input_path.name}")

            for f in folder_path.iterdir():
                if f.is_file() and f.suffix.lower() in (".tif", ".tiff"):
                    f.unlink()
                    print(f"  deleted  {f.name}  (TIF)")
                elif f.is_file() and f.suffix.lower() == ".jpg" and "_RAW_" in f.name.upper():
                    f.unlink()
                    print(f"  deleted  {f.name}  (RAW)")

    print("\nAll done.")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 · BATCH
#
# Collect all finished Result XMLs that have not yet been assigned to a batch
# into a new numbered, dated batch folder under _batches/.
# Batch membership is tracked exclusively through the manifest files —
# no marker files are written into item folders.
#
# Batch folder structure:
#   <base_dir>/_batches/
#     batch_001_2026-03-30/
#       manifest.txt          ← lists all items, creation date, item count
#     batch_002_2026-04-15/
#       manifest.txt
#
# manifest.txt format:
#   batch:   batch_001_2026-03-30
#   created: 2026-03-30
#   items:   20
#
#   SZ_AAL_B2.1
#   SZ_AAL_B2.2
#   ...
# ─────────────────────────────────────────────────────────────────────────────

def _batches_dir(base_dir: Path) -> Path:
    """Return the path to the _batches directory inside base_dir."""
    return base_dir / "_batches"


def _read_batch_assignments(base_dir: Path) -> dict[str, str]:
    """
    Parse all manifest files under _batches/ and return a mapping of
    folder name → batch name for every item that has been batched.

    Only lines that look like signature folder names (matching SZ_AAL_B\d+\.\d+)
    are treated as item entries; header lines (batch:, created:, items:) and
    blank lines are ignored.
    """
    assignments: dict[str, str] = {}
    batches = _batches_dir(base_dir)
    if not batches.exists():
        return assignments

    # Match any signature folder entry (SZ_AAL_<letter(s)><digit>...) —
    # skips manifest header lines (batch:, created:, items:) and blank lines.
    sig_pattern = re.compile(r"^SZ_AAL_[A-Z]\d")
    for manifest in sorted(batches.glob("*/manifest.txt")):
        batch_name = manifest.parent.name
        for line in manifest.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if sig_pattern.match(line):
                assignments[line] = batch_name

    return assignments


def _next_batch_name(base_dir: Path) -> str:
    """
    Derive the next batch name by finding the highest existing batch number.

    Parses the NNN from each batch_NNN_* directory rather than counting dirs,
    so manually named batches (--name) don't corrupt the auto-counter.

    Format: batch_NNN_YYYY-MM-DD (e.g. batch_003_2026-04-15)
    """
    batches = _batches_dir(base_dir)
    n = 0
    if batches.exists():
        for d in batches.glob("batch_*"):
            m = re.match(r"batch_(\d+)_", d.name)
            if m:
                n = max(n, int(m.group(1)))
    return f"batch_{n + 1:03d}_{date.today().isoformat()}"


def cmd_batch(args) -> None:
    """
    Step 4: Collect newly finished items into a named batch for GAMS ingest.

    Scans base_dir for signature folders that have a Result_*.xml but are not
    yet listed in any existing manifest. Writes a manifest.txt into a new batch
    folder under _batches/.

    Running this command repeatedly is safe: items already listed in a manifest
    are skipped, so each run only captures items that have finished since the
    last batch.

    Use --limit to cap how many items go into one batch (useful when submitting
    to GAMS in fixed-size chunks). Use --dry-run to preview without writing anything.
    """
    base_dir = Path(args.base_dir)
    dry_run  = args.dry_run
    limit    = args.limit  # 0 means no limit

    sig_pattern  = _series_pattern(args.series)
    already_done = _read_batch_assignments(base_dir)

    # Collect all done-but-not-yet-batched items
    all_folders = sorted(
        [d for d in base_dir.iterdir() if d.is_dir() and sig_pattern.match(d.name)],
        key=lambda d: _folder_sort_key(d.name)
    )
    pending = [
        f for f in all_folders
        if (f / f"Result_{f.name}.xml").exists() and f.name not in already_done
    ]

    if not pending:
        print("Nothing to batch — all finished items are already assigned to a batch.")
        return

    if limit and limit > 0:
        pending = pending[:limit]

    batch_name = args.name or _next_batch_name(base_dir)
    batch_dir  = _batches_dir(base_dir) / batch_name

    print(f"{'=== DRY RUN ===' if dry_run else '=== CREATING BATCH ==='}")
    print(f"Batch : {batch_name}")
    print(f"Items : {len(pending)}\n")

    for folder in pending:
        print(f"  {folder.name}")

    if dry_run:
        print(f"\nWould create {batch_dir}")
        return

    batch_dir.mkdir(parents=True, exist_ok=True)

    manifest_lines = [
        f"batch:   {batch_name}",
        f"created: {date.today().isoformat()}",
        f"items:   {len(pending)}",
        "",
    ] + [f.name for f in pending]

    (batch_dir / "manifest.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    print(f"\nBatch created: {batch_dir}")
    print(f"Manifest:      {batch_dir / 'manifest.txt'}")


# ─────────────────────────────────────────────────────────────────────────────
# STATUS
#
# Scan base_dir and report the current pipeline stage of every signature folder.
# Folders are grouped and sorted by stage (batched first, then by pipeline order).
# Batched items are grouped under their specific batch name so you can see at a
# glance which batch each item belongs to.
# ─────────────────────────────────────────────────────────────────────────────

# Static stages in display order (batched items are dynamic — see _folder_stage)
_STATIC_STAGES = {
    "done":         "◉ done (ready to batch)",
    "ready":        "● ready to transform",
    "needs_review": "✎ needs review",
    "no_xml":       "○ no XML yet",
    "no_jpgs":      "! no JPGs",
}

# Sort key for each stage (lower = listed first; batched items get key 0)
_STAGE_ORDER = {
    "done":         1,
    "ready":        2,
    "needs_review": 3,
    "no_xml":       4,
    "no_jpgs":      5,
}


def _folder_stage(
    folder_path: Path,
    folder_name: str,
    batch_assignments: dict[str, str],
) -> tuple[str, str]:
    """
    Return the current pipeline stage for a signature folder as (stage_key, label).

    batch_assignments is the dict returned by _read_batch_assignments(); pass an
    empty dict if batch tracking is not needed.

    Stage keys:
      batched:<name>  — Result XML exists and item is listed in a batch manifest
      done            — Result XML exists, not yet in any batch
      ready           — intermediate XML exists and passes validation
      needs_review    — intermediate XML exists but page ranges are incomplete/invalid
      no_xml          — JPGs present but no intermediate XML generated yet
      no_jpgs         — folder is empty (no JPGs at all)
    """
    result_xml = folder_path / f"Result_{folder_name}.xml"
    input_xml  = folder_path / f"{folder_name}.xml"

    if result_xml.exists():
        batch_name = batch_assignments.get(folder_name)
        if batch_name:
            return (f"batched:{batch_name}", f"[done] {batch_name}")
        return ("done", _STATIC_STAGES["done"])

    jpgs = list(folder_path.glob("*.jpg"))
    if not jpgs:
        return ("no_jpgs", _STATIC_STAGES["no_jpgs"])

    if not input_xml.exists():
        return ("no_xml", _STATIC_STAGES["no_xml"])

    errors = _validate_xml(folder_path, folder_name)
    if errors:
        return ("needs_review", _STATIC_STAGES["needs_review"])

    return ("ready", _STATIC_STAGES["ready"])


# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 · VALIDATE (post-transform audit)
# ─────────────────────────────────────────────────────────────────────────────

_VALID_DIV_TYPES = {"Textseiten", "Farbreferenz", "Kuvert", "Adressseiten",
                    "Fotografie", "Postkarte", "Beilage", "Beilagen"}

_NS_VIEWER = "http://gams.uni-graz.at/viewer"
_NS_XLINK  = "http://www.w3.org/1999/xlink"


def _check_result_xml(folder_path: Path, folder_name: str,
                      issues: dict, stats: dict) -> list | None:
    """Validate a Result XML: parse, metadata, structure, div types. Returns referenced image list."""
    xml_file = folder_path / f"Result_{folder_name}.xml"
    if not xml_file.exists():
        issues["Fehlende Result-XML"].append(f"{folder_name}: Result_{folder_name}.xml fehlt")
        stats["xmls_invalid"] += 1
        return None

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        stats["xmls_valid"] += 1
    except ET.ParseError as e:
        issues["XML Parse-Fehler"].append(f"{folder_name}: {e}")
        stats["xmls_invalid"] += 1
        return None

    tag = f"{{{_NS_VIEWER}}}"

    is_lebensdokument = folder_name.startswith("SZ_AAL_L")
    # L-series items often have no Verfasser*in — check contributor instead of author
    meta_fields = ("title",) if is_lebensdokument else ("title", "author")
    for field in meta_fields:
        el = root.find(f"{tag}{field}")
        if el is None or not (el.text and el.text.strip()):
            issues["Fehlende/leere Metadaten"].append(f"{folder_name}: <{field}> fehlt oder leer")

    title_el  = root.find(f"{tag}title")
    short_sig = re.sub(r"^SZ_AAL_", "", folder_name)  # "B2.1" from "SZ_AAL_B2.1"
    if title_el is not None and title_el.text and short_sig not in title_el.text:
        issues["Metadaten-Inkonsistenz"].append(
            f"{folder_name}: <title> enthält nicht '{short_sig}': '{title_el.text.strip()}'"
        )

    owner_el = root.find(f"{tag}owner/{tag}name")
    if owner_el is None or not (owner_el.text and owner_el.text.strip()):
        issues["Fehlende/leere Metadaten"].append(f"{folder_name}: <owner><name> fehlt oder leer")

    structure_el = root.find(f"{tag}structure")
    if structure_el is None:
        issues["Fehlende Struktur"].append(f"{folder_name}: <structure> fehlt")
        return None

    divs      = structure_el.findall(f"{tag}div")
    div_types = [d.get("type") for d in divs]
    kuvert_only = set(div_types) <= {"Kuvert", "Farbreferenz"}
    if "Textseiten" not in div_types and not kuvert_only:
        issues["Fehlende Struktur"].append(f"{folder_name}: <div type='Textseiten'> fehlt")
    if "Farbreferenz" not in div_types:
        issues["Fehlende Struktur"].append(f"{folder_name}: <div type='Farbreferenz'> fehlt")
    for dt in div_types:
        if dt not in _VALID_DIV_TYPES:
            issues["Unbekannter div-Typ"].append(f"{folder_name}: '{dt}'")

    refs = []
    for page in root.iter(f"{tag}page"):
        href = page.get(f"{{{_NS_XLINK}}}href")
        if href:
            refs.append(href)
    return refs


def _check_result_images(folder_path: Path, folder_name: str,
                          refs: list | None, issues: dict, stats: dict) -> None:
    """Check image references, naming convention, numbering gaps, zero-byte files."""
    if refs is None:
        return

    actual  = {f.name for f in folder_path.iterdir() if f.suffix.lower() in (".jpg", ".jpeg")}
    ref_set = set(refs)

    stats["total_images"]            += len(actual)
    stats["total_referenced_images"] += len(ref_set)

    for r in refs:
        if r not in actual:
            issues["Fehlende Bilder"].append(f"{folder_name}: {r} referenziert, Datei fehlt")

    for jpg in sorted(actual):
        if jpg not in ref_set:
            issues["Verwaiste Bilder"].append(f"{folder_name}: {jpg} nicht in XML referenziert")

    expected = re.compile(rf"^{re.escape(folder_name)}_\d{{3}}\.jpg$", re.IGNORECASE)
    for jpg in sorted(actual):
        if not expected.match(jpg):
            issues["Namenskonvention Bilder"].append(
                f"{folder_name}: {jpg} entspricht nicht dem Schema {folder_name}_NNN.jpg"
            )

    nums = [int(m.group(1)) for jpg in actual
            if (m := re.match(rf"^{re.escape(folder_name)}_(\d{{3}})\.jpg$", jpg, re.IGNORECASE))]
    if nums:
        missing = set(range(1, max(nums) + 1)) - set(nums)
        if missing:
            issues["Luecken in Bildnummerierung"].append(
                f"{folder_name}: fehlende Nummern {sorted(missing)}"
            )

    for jpg in sorted(actual):
        if (folder_path / jpg).stat().st_size == 0:
            issues["Leere Bilddateien"].append(f"{folder_name}: {jpg} ist leer (0 Bytes)")


def cmd_validate(args) -> None:
    """
    Post-transform audit for a Results folder.

    Checks every folder matching the series pattern for:
      - Presence and validity of Result_<signature>.xml
      - Metadata completeness (title, author, date, owner)
      - Structure integrity (Textseiten, Farbreferenz div types)
      - Image reference consistency (missing, orphaned, naming, gaps)
    """
    base_dir    = Path(args.base_dir)
    sig_pattern = _series_pattern(args.series)

    subfolders = sorted(
        [d.name for d in base_dir.iterdir() if d.is_dir() and sig_pattern.match(d.name)],
        key=_folder_sort_key
    )

    if not subfolders:
        print(f"No matching folders found in: {base_dir}")
        return

    issues: dict = defaultdict(list)
    stats: dict  = {
        "folders_checked":         0,
        "xmls_valid":              0,
        "xmls_invalid":            0,
        "total_images":            0,
        "total_referenced_images": 0,
    }

    print("=" * 70)
    print("SZ_AAL Result-Validierung")
    print("=" * 70)
    print(f"Basisverzeichnis: {base_dir}\n")

    for folder_name in subfolders:
        folder_path = base_dir / folder_name
        stats["folders_checked"] += 1
        refs = _check_result_xml(folder_path, folder_name, issues, stats)
        _check_result_images(folder_path, folder_name, refs, issues, stats)

    print("STATISTIK")
    print("-" * 70)
    print(f"  Ordner geprueft:      {stats['folders_checked']}")
    print(f"  XML valide:           {stats['xmls_valid']}")
    print(f"  XML invalide:         {stats['xmls_invalid']}")
    print(f"  Bilder gesamt:        {stats['total_images']}")
    print(f"  Bilder referenziert:  {stats['total_referenced_images']}")
    print()

    if not issues:
        print("ERGEBNIS: Keine Probleme gefunden!")
        return

    total = sum(len(v) for v in issues.values())
    print(f"ERGEBNIS: {total} Probleme in {len(issues)} Kategorien gefunden")
    print("=" * 70)

    sorted_issues = sorted(issues.items(), key=lambda kv: -len(kv[1]))
    for category, items in sorted_issues:
        print(f"\n[{category}] ({len(items)} Probleme)")
        print("-" * 50)
        for item in items:
            print(f"  - {item}")

    print("\n" + "=" * 70)
    print("ZUSAMMENFASSUNG")
    print("=" * 70)
    for category, items in sorted_issues:
        print(f"  {category}: {len(items)}")


def cmd_status(args) -> None:
    """
    Show the current pipeline stage of every signature folder, grouped by stage.

    Batched items are listed under their specific batch name (e.g. '✓ batch_001_2026-03-30')
    so you can see exactly which items went into which batch. The summary at the
    bottom counts items per stage.
    """
    base_dir = Path(args.base_dir)
    pattern  = _series_pattern(args.series)

    folders = sorted(
        [d for d in base_dir.iterdir() if d.is_dir() and pattern.match(d.name)],
        key=lambda d: _folder_sort_key(d.name)
    )

    if not folders:
        print(f"No matching folders found in: {base_dir}")
        return

    batch_assignments = _read_batch_assignments(base_dir)

    # Collect (sort_key, label, folder_name) for each folder
    rows = []
    for folder in folders:
        stage_key, label = _folder_stage(folder, folder.name, batch_assignments)
        if stage_key.startswith("batched:"):
            # Batched items sort before all static stages (key 0), then by batch name
            sort_key = (0, stage_key)
        else:
            sort_key = (_STAGE_ORDER.get(stage_key, 99), stage_key)
        rows.append((sort_key, label, folder.name))

    rows.sort(key=lambda r: r[0])

    # Print table grouped by label; track first-seen sort key per label for summary ordering
    current_label = None
    counts:      dict[str, int]   = {}
    label_order: dict[str, tuple] = {}
    for sort_key, label, name in rows:
        if label not in label_order:
            label_order[label] = sort_key
        if label != current_label:
            print(f"\n{label}")
            current_label = label
        print(f"  {name}")
        counts[label] = counts.get(label, 0) + 1

    # Summary — same order as the table above
    print("\n── Summary " + "─" * 30)
    for label, count in sorted(counts.items(), key=lambda kv: label_order[kv[0]]):
        print(f"  {label:<35}  {count}")
    print(f"  {'total':<35}  {len(folders)}")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="szd_pipeline.py",
        description="Unified pipeline for the Stefan Zweig Digital Archive (SZ-AAL).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Steps (run in order):
  1. sort       Normalize Lightroom export filenames, move TIFF/RAW into subfolders
  2. generate   Generate intermediate XML into each signature folder
                ── MANUAL: open each XML and fill in the page number ranges ──
  3. transform  Validate + apply XSLT → produce final METS viewer XML (Result_*.xml)
  4. batch      Collect finished items into a numbered batch folder for GAMS ingest

Additional:
  status        Show the current stage of every signature folder
        """
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ── Step 1: sort ──────────────────────────────────────────────────────────
    p_sort = sub.add_parser("sort", help="Step 1: Sort and rename Lightroom output files")
    p_sort.add_argument("--root",   default=".", metavar="DIR",
                        help="Root directory containing the signature folders (default: .)")
    p_sort.add_argument("--series", default="SZ_AAL_B2", metavar="PREFIX",
                        help="Signature series prefix to match (default: SZ_AAL_B2)")
    p_sort.add_argument("--folder", metavar="NAME",
                        help="Process only this subfolder, e.g. SZ_AAL_B2.5")
    p_sort.add_argument("--apply",  action="store_true",
                        help="Apply changes (default: dry-run, no files modified)")

    # ── Step 2: generate ──────────────────────────────────────────────────────
    p_gen = sub.add_parser("generate", help="Step 2: Generate intermediate XML into each signature folder")
    p_gen.add_argument("csv_file", metavar="metadata_file",
                       help="Path to the CSV or Excel (.xlsx) metadata file")
    p_gen.add_argument("--base-dir", required=True, metavar="DIR",
                       help="Root directory containing the signature folders")
    p_gen.add_argument("--limit",   type=int, default=0, metavar="N",
                       help="Process only the first N rows (0 = all rows)")
    p_gen.add_argument("--sig-col", default="", metavar="COLUMN",
                       help="Name of the signature column in the CSV (auto-detected if omitted)")
    p_gen.add_argument("--dry-run", action="store_true",
                       help="Preview which XMLs would be created without writing any files")

    # ── Step 2b: autofill ─────────────────────────────────────────────────────
    p_af = sub.add_parser("autofill",
                           help="Step 2b: Auto-fill page ranges from JPG counts (review before transform)")
    p_af.add_argument("--base-dir", required=True, metavar="DIR",
                      help="Directory containing the signature subfolders")
    p_af.add_argument("--series",   default="SZ_AAL_B", metavar="PREFIX",
                      help="Signature series prefix to match (default: SZ_AAL_B)")
    p_af.add_argument("--folder",   metavar="NAME",
                      help="Process only this one folder, e.g. SZ_AAL_B4.1")
    p_af.add_argument("--apply",    action="store_true",
                      help="Write changes (default: dry-run, no files modified)")

    # ── Step 3: transform ─────────────────────────────────────────────────────
    p_tr = sub.add_parser("transform",
                           help="Step 3: Validate + XSLT transform → Result_*.xml (run after manual review)")
    p_tr.add_argument("--base-dir",  required=True, metavar="DIR",
                      help="Directory containing the signature subfolders")
    p_tr.add_argument("--series",    default="SZ_AAL_B", metavar="PREFIX",
                      help="Signature series prefix to match (default: SZ_AAL_B)")
    p_tr.add_argument("--xslt",      required=True, metavar="FILE",
                      help="Path to the XSLT stylesheet (szd-JPGtoMETS.xsl)")
    p_tr.add_argument("--folder",    metavar="NAME",
                      help="Transform only this one folder, e.g. SZ_AAL_B2.5")
    p_tr.add_argument("--no-delete", action="store_true",
                      help="Keep source XML after transformation instead of deleting it")
    p_tr.add_argument("--yes", "-y", action="store_true",
                      help="Skip the interactive skip prompt and transform all pending folders")

    # ── Step 4: batch ─────────────────────────────────────────────────────────
    p_bt = sub.add_parser("batch",
                           help="Step 4: Collect finished items into a numbered batch for GAMS ingest")
    p_bt.add_argument("--base-dir", required=True, metavar="DIR",
                      help="Directory containing the signature subfolders")
    p_bt.add_argument("--series",   default="SZ_AAL_B", metavar="PREFIX",
                      help="Signature series prefix to match (default: SZ_AAL_B)")
    p_bt.add_argument("--limit",    type=int, default=0, metavar="N",
                      help="Maximum number of items to include in this batch (0 = all ready items)")
    p_bt.add_argument("--name",     metavar="NAME",
                      help="Override the auto-generated batch name (default: batch_NNN_YYYY-MM-DD)")
    p_bt.add_argument("--dry-run",  action="store_true",
                      help="Preview which items would be batched without writing anything")

    # ── Validate ──────────────────────────────────────────────────────────────
    p_va = sub.add_parser("validate", help="Post-transform audit: XML validity, metadata, image references")
    p_va.add_argument("--base-dir", required=True, metavar="DIR",
                      help="Results directory containing the signature folders")
    p_va.add_argument("--series", default="SZ_AAL_B", metavar="PREFIX",
                      help="Signature series prefix to match (default: SZ_AAL_B = all series)")

    # ── Status ────────────────────────────────────────────────────────────────
    p_st = sub.add_parser("status", help="Show the current pipeline stage of every signature folder")
    p_st.add_argument("--base-dir", required=True, metavar="DIR",
                      help="Root directory containing the signature folders")
    p_st.add_argument("--series",   default="SZ_AAL_B", metavar="PREFIX",
                      help="Signature series prefix to match (default: SZ_AAL_B)")

    args = parser.parse_args()

    dispatch = {
        "sort":      cmd_sort,
        "generate":  cmd_generate,
        "autofill":  cmd_autofill,
        "transform": cmd_transform,
        "batch":     cmd_batch,
        "validate":  cmd_validate,
        "status":    cmd_status,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
