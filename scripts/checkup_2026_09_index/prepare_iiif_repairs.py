#!/usr/bin/env python3
"""Prepare the four further book sources whose IIIF structure labels break the manifest.

Same defect and same remedy as scripts/iiif_structure_labels: sdef:IIIF/getManifest copies
a book div/@type into a range label without escaping the quotation marks it contains, so the
manifest is not valid JSON and the viewer fails. The repair replaces the straight quotation
pair by typographic quotes in the ingest source and changes nothing else.

The four objects come from the verification of the 2026-09 checkup (knowledge/DATA.md,
Archive checkup), two from the Werke and two from the Aufsatzablage:

    o:szd.939   SZ-SAM/W2         Castellio gegen Calvin, five quoted chapter labels
    o:szd.2935  SZ-AP2/W-H172.4   one quoted label
    o:szd.2409  SZ-AAP/W-AA135.1  two quoted labels
    o:szd.2291  SZ-AAP/W-AA183.2  one quoted label

The preparation itself is prepare_source from scripts/iiif_structure_labels, imported here
rather than copied, so both sets of prepared files are produced by the same verified code
and land in the same prepared/ directory. That module never contacts GAMS and never writes
to the source tree; the identity checks it runs are the reason the identifier, page count
and labels are recorded here as constants rather than read from whatever the source happens
to contain.

Usage:

    python scripts/checkup_2026_09_index/prepare_iiif_repairs.py \\
        --source-root C:/Users/Chrisi/Documents/PROJECTS/szd
    python scripts/checkup_2026_09_index/prepare_iiif_repairs.py --source-root ... --apply
    python scripts/checkup_2026_09_index/prepare_iiif_repairs.py --verify

Regime: script pipeline in the shape the other scripts of this repo use, standard library
only, run with plain python.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
PREPARE_MODULE = REPO_ROOT / "scripts" / "iiif_structure_labels" / "prepare_repairs.py"
OUT_DIR = REPO_ROOT / "scripts" / "iiif_structure_labels" / "prepared"
REPORT = OUT_DIR / "repairs-checkup-2026-09.json"

# file name -> (PID, page count, the quoted labels), all three verified against the source
# and against the live manifest, which fails at exactly these labels.
SOURCES = {
    "Result_SZ_SAM_W2.xml": (
        "o:szd.939",
        427,
        (
            'Drittes Kapitel/"Castellio tritt auf"',
            'Fünftes Kapitel/"Servet und Calvin"',
            'Sechstes Kapitel/"Das Manifest der Toleranz"',
            'Siebentes Kapitel/"Der Einzelne gegen die Diktatur"',
            'Achtes Kapitel/"Die Diktatur zerschmettert den Menschen"',
        ),
    ),
    "Result_SZ_AP2_W_H172.4.xml": (
        "o:szd.2935",
        51,
        ('Notiz/"Italienische Fassung"',),
    ),
    "Result_SZ_AAP_W_AA135.1.xml": (
        "o:szd.2409",
        13,
        (
            'Stefan Zweig: Thomas Manns "Rede und Antwort"',
            'Alfred Neumann: "Moll und Dur. Gedichte aus der alten und der neuen Welt"',
        ),
    ),
    "Result_SZ_AAP_W_AA183.2.xml": (
        "o:szd.2291",
        69,
        ('Umschlagblatt "Salzburg"',),
    ),
}


def load_prepare_source():
    """prepare_source from the neighbouring script, which stays the single implementation."""
    spec = importlib.util.spec_from_file_location("prepare_repairs", PREPARE_MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.prepare_source


def build(source_root: Path) -> list[tuple[str, bytes, dict]]:
    prepare_source = load_prepare_source()
    outputs: list[tuple[str, bytes, dict]] = []
    for name, (pid, pages, labels) in SOURCES.items():
        matches = sorted(source_root.rglob(name))
        matches = [path for path in matches if path.resolve().parent != OUT_DIR.resolve()]
        if len(matches) != 1:
            raise ValueError(f"Expected one source {name}, found {len(matches)}")
        payload, record = prepare_source(matches[0], pid, pages, labels)
        record["source"] = matches[0].as_posix()
        outputs.append((name, payload, record))
    return outputs


def verify() -> int:
    """The prepared files on disk match their record, and no straight quote is left."""
    if not REPORT.exists():
        print(f"FAIL  {REPORT.name} missing, nothing prepared yet")
        return 1
    failures: list[str] = []
    records = json.loads(REPORT.read_text(encoding="utf-8"))
    if {record["file"] for record in records} != set(SOURCES):
        failures.append("the report does not cover exactly the four sources")
    for record in records:
        target = OUT_DIR / record["file"]
        if not target.exists():
            failures.append(f"{record['file']} missing from prepared/")
            continue
        payload = target.read_bytes()
        if hashlib.sha256(payload).hexdigest() != record["repairedSha256"]:
            failures.append(f"{record['file']} differs from its recorded checksum")
        text = payload.decode("utf-8")
        for label in record["labels"]:
            if f'type="{label["before"]}"' in text:
                failures.append(f"{record['file']} still carries {label['before']!r}")
            if f'type="{label["after"]}"' not in text:
                failures.append(f"{record['file']} lacks the repaired {label['after']!r}")
    for failure in failures:
        print(f"FAIL  {failure}")
    if failures:
        return 1
    print(f"OK  {len(records)} prepared sources match their record")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, help="the ingest source tree, read only")
    parser.add_argument("--apply", action="store_true", help="write into prepared/")
    parser.add_argument("--verify", action="store_true", help="check prepared/ against itself")
    args = parser.parse_args()

    if args.verify:
        return verify()
    if args.source_root is None or not args.source_root.is_dir():
        print("FAIL  --source-root must name the ingest source tree", file=sys.stderr)
        return 1

    outputs = build(args.source_root)
    report = json.dumps([record for _, _, record in outputs], ensure_ascii=False, indent=2)
    files = [(name, payload) for name, payload, _ in outputs]
    files.append((REPORT.name, (report + "\n").encode("utf-8")))

    for _, _, record in outputs:
        labels = ", ".join(f'{item["before"]!r} -> {item["after"]!r}' for item in record["labels"])
        print(f"OK  {record['pid']} {record['file']} {record['pages']} pages: {labels}")
    # Trust boundary: an existing output is never silently replaced by a different one.
    for name, payload in files:
        target = OUT_DIR / name
        if target.exists() and target.read_bytes() != payload:
            print(f"FAIL  refusing to replace different output: {target}", file=sys.stderr)
            return 1
    if not args.apply:
        print(f"SKIP  dry run, {len(files)} files planned in {OUT_DIR.name}/")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, payload in files:
        target = OUT_DIR / name
        if not target.exists():
            with target.open("xb") as handle:
                handle.write(payload)
        print(f"OK  {target.relative_to(REPO_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
