#!/usr/bin/env python3
"""
compare_tei_bodies.py  (concise log edition)

Creates a log of text- and attribute-level differences inside the <body> of
each TEI XML pair found in two folders, but prints only a minimal tag-path
(e.g. 'div/p') instead of the full XPath.

Usage:
    python compare_tei_bodies.py --tei-dir tei --cleaned-dir tei-cleaned
"""

from __future__ import annotations
from pathlib import Path
import argparse, sys

try:
    from lxml import etree as ET          # pip install lxml
except ImportError:
    sys.exit("Missing dependency: pip install lxml")

# --------------------------------------------------------------------------- #
def get_body(path: Path):
    """Return the <body> element (or None)."""
    tree = ET.parse(str(path))
    root = tree.getroot()
    ns = root.nsmap.get(None)
    return root.find(f".//{{{ns}}}body") if ns else root.find(".//body")


def index_body(body) -> dict[str, tuple[str, dict]]:
    """
    Walk `body`, building {internal_xpath: (text, attrs)} where internal_xpath
    includes sibling positions so each element is unique.
    """
    out: dict[str, tuple[str, dict]] = {}
    stack = [("/body", body)]

    while stack:
        base, node = stack.pop()
        counts: dict[str, int] = {}
        for child in node:
            if not isinstance(child.tag, str):
                continue
            tag = ET.QName(child).localname
            counts[tag] = counts.get(tag, 0) + 1
            pos = counts[tag]
            xp = f"{base}/{tag}[{pos}]"
            out[xp] = ((child.text or "").strip(), dict(child.attrib))
            stack.append((xp, child))
    return out


def shorten(path: str) -> str:
    """Remove '/body' prefix and '[n]' sibling indexes."""
    if path.startswith("/body/"):
        path = path[6:]
    return path.replace("[", "").replace("]", "")


def diff_maps(a: dict, b: dict) -> list[str]:
    """Return concise diff lines for changed text or attribute values."""
    lines: list[str] = []
    for xp in sorted(set(a) & set(b)):        # only shared elements
        txt1, at1 = a[xp]
        txt2, at2 = b[xp]
        short = shorten(xp)
        if txt1 != txt2:
            lines.append(f"TEXT  {short}: {txt1!r} → {txt2!r}")
        for k in set(at1) | set(at2):
            v1, v2 = at1.get(k), at2.get(k)
            if v1 != v2:
                lines.append(f"ATTR  {short} @{k}: {v1!r} → {v2!r}")
    return lines
# --------------------------------------------------------------------------- #
def main(tei_dir: Path, cleaned_dir: Path, log_file: Path):
    originals = sorted(tei_dir.glob("*.xml"))
    if not originals:
        sys.exit(f"No XML found in {tei_dir}")

    with log_file.open("w", encoding="utf-8") as log:
        for src in originals:
            tgt = cleaned_dir / src.name
            if not tgt.exists():
                continue

            b1, b2 = get_body(src), get_body(tgt)
            if b1 is None or b2 is None:
                continue

            diffs = diff_maps(index_body(b1), index_body(b2))
            if diffs:
                log.write(f"\n## {src.name}\n")
                log.write("\n".join(diffs) + "\n")

    print(f"Wrote diff log to {log_file}")


if __name__ == "__main__":
    argp = argparse.ArgumentParser(description="Compare TEI bodies (concise log).")
    argp.add_argument("--tei-dir", default="tei", type=Path)
    argp.add_argument("--cleaned-dir", default="tei-cleaned", type=Path)
    argp.add_argument("--log-file", default="tei_value_diff.txt", type=Path)
    main(**vars(argp.parse_args()))
