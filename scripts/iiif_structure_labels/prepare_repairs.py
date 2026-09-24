# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Prepare copies of the three book sources with broken IIIF structure labels.

Run with uv run prepare_repairs.py --source-root PATH --out-dir PATH.
The six observed labels in the three sources are replaced byte-for-byte, changing
only straight quotation marks to German typographic quotes. Everything outside
these attributes remains byte-identical. Source files are always read-only.

This standalone repair uses stdlib XML only for strict structural verification;
XML serialisation is deliberately avoided to preserve the ingest source bytes.
The GAMS generator defect is documented in knowledge/COLLECTIONS.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

VIEWER = "{http://gams.uni-graz.at/viewer}"
SOURCES = {
    "Result_SZ_AP2_L_S1.1.xml": (
        "o:szd.174",
        122,
        ('Deckblatt "VERLEGER vor dem Index"',),
    ),
    "Result_SZ_AAP_L2.xml": (
        "o:szd.67",
        237,
        ('Zeitungsausschnitt/Vom "österreichischen" Dichter',),
    ),
    "Result_SZ_AP2_W_G104.1.xml": (
        "o:szd.314",
        55,
        (
            '"In Zürich, wo er nach langen Irrfahrten endlich"',
            'Servet/"Wichtig für die Verbreitung der Irrlehre"',
            '"Unterwerfung unter den Gehorsam"',
            '"Sein Grundsatz ist derjenige"',
        ),
    ),
}


def repaired_label(label: str) -> str:
    if label.count('"') != 2:
        raise ValueError(f"Expected exactly one quotation pair: {label!r}")
    return label.replace('"', "\u201e", 1).replace('"', "\u201c", 1)


def prepare_source(
    source: Path, pid: str, pages: int, labels: tuple[str, ...]
) -> tuple[bytes, dict]:
    original = source.read_bytes()
    tree = ET.fromstring(original)
    if tree.tag != f"{VIEWER}book" or tree.findtext(f"{VIEWER}idno") != pid:
        raise ValueError(f"Unexpected book identity: {source}")
    if len(list(tree.iter(f"{VIEWER}page"))) != pages:
        raise ValueError(f"Unexpected page count: {source}")
    observed = [
        div.get("type", "")
        for div in tree.iter(f"{VIEWER}div")
        if '"' in div.get("type", "")
    ]
    if sorted(observed) != sorted(labels):
        raise ValueError(f"Quoted labels differ from the verified source: {source}")

    result = original
    replacements = []
    for label in labels:
        fixed = repaired_label(label)
        old_attribute = ('type="' + escape(label, {'"': "&quot;"}) + '"').encode(
            "utf-8"
        )
        new_attribute = ('type="' + escape(fixed, {'"': "&quot;"}) + '"').encode(
            "utf-8"
        )
        if result.count(old_attribute) != 1:
            raise ValueError(f"Expected one exact attribute for {label!r}: {source}")
        result = result.replace(old_attribute, new_attribute, 1)
        replacements.append({"before": label, "after": fixed})

    repaired = ET.fromstring(result)
    for div in tree.iter(f"{VIEWER}div"):
        if div.get("type") in labels:
            div.set("type", repaired_label(div.attrib["type"]))
    if ET.tostring(tree) != ET.tostring(repaired):
        raise ValueError(f"Unexpected XML change: {source}")
    if any('"' in div.get("type", "") for div in repaired.iter(f"{VIEWER}div")):
        raise ValueError(f"Unrepaired quotation mark: {source}")
    return result, {
        "file": source.name,
        "pid": pid,
        "pages": pages,
        "sourceSha256": hashlib.sha256(original).hexdigest(),
        "repairedSha256": hashlib.sha256(result).hexdigest(),
        "labels": replacements,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    if not args.source_root.is_dir():
        raise FileNotFoundError(args.source_root)
    outputs = []
    for name, (pid, pages, labels) in SOURCES.items():
        matches = sorted(args.source_root.rglob(name))
        if len(matches) != 1:
            raise ValueError(f"Expected one source {name}, found {len(matches)}")
        if matches[0].resolve() == (args.out_dir / name).resolve():
            raise ValueError("Output must be separate from the source")
        payload, record = prepare_source(matches[0], pid, pages, labels)
        outputs.append((name, payload, record))

    report = (
        json.dumps([record for _, _, record in outputs], ensure_ascii=False, indent=2)
        + "\n"
    )
    files = [(name, payload) for name, payload, _ in outputs] + [
        ("repairs.json", report.encode("utf-8"))
    ]
    for name, payload in files:
        target = args.out_dir / name
        if target.exists() and target.read_bytes() != payload:
            raise FileExistsError(f"Refusing to replace different output: {target}")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in files:
        target = args.out_dir / name
        if not target.exists():
            with target.open("xb") as handle:
                handle.write(payload)
        print(f"OK {target}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
