#!/usr/bin/env python3
"""
clean_tei_with_csv.py   v3.1   (2025-04-29)

• Aligns TEI <biblFull> nodes with catalogue data in ./data/*.csv
• Writes only changed files to ./tei-cleaned/
• Re-uses existing elements, removes identical siblings, enforces ordering, works
  with lxml, and now handles *duplicate signatures* gracefully.
• Flip DEBUG = True to embed <!-- NEW / REMOVED / … --> comments in output XML.
"""

from __future__ import annotations
import csv, logging, re, unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Dict, Optional, List

from lxml import etree as ET           # external dep:  pip install lxml

# ── switches ───────────────────────────────────────────────────────────
DEBUG = False          # True → inline XML comments for every action

# ── project folders ────────────────────────────────────────────────────
BASE      = Path(__file__).parent
CSV_DIR   = BASE / "data"
TEI_DIR   = BASE / "tei"
OUT_DIR   = BASE / "tei-cleaned"
LOG_FILE  = BASE / "clean.log"

from tei_csv_mapping import MAPPING    # your OrderedDict mapping

# ── namespaces & helpers ───────────────────────────────────────────────
TEI_NS_URI = "http://www.tei-c.org/ns/1.0"
TEI_NS     = {"tei": TEI_NS_URI}
ET.register_namespace("tei", TEI_NS_URI)          # readable <tei:...> output
QName    = lambda t: f"{{{TEI_NS_URI}}}{t}"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

norm   = lambda s: unicodedata.normalize("NFC", re.sub(r"\s+", " ", s.strip())) if s else ""
splitv = lambda c: [norm(x) for x in c.split(";") if norm(x)] if ";" in c else [norm(c)] if c else []

# ── clearer for stray deduced placeNames ───────────────────────────────
def purge_deduced_places(action: ET._Element) -> None:
    """
    If the <correspAction> already contains at least one <placeName>
    **without** @ana='deduced', remove every <placeName ana="deduced">.
    """
    has_explicit = any(
        child.tag == QName("placeName") and child.get("ana") != "deduced"
        for child in action if isinstance(child.tag, str)
    )
    if has_explicit:
        for node in list(action.findall(QName("placeName"))):
            if node.get("ana") == "deduced":
                drop_comment(action, list(action).index(node),
                             "REMOVED deduced place after explicit place added")
                action.remove(node)


def _safe_comment(txt: str) -> str:
    """
    Sanitize for XML comment:
      • replace every “--” with “– –”
      • ensure the comment does not end with “-”
    """
    txt = txt.replace("--", "– –")
    if txt.endswith("-"):
        txt += " "
    return txt

def drop_comment(parent: ET._Element, idx: int, txt: str) -> None:
    if DEBUG:
        try:
            parent.insert(idx, ET.Comment(_safe_comment(txt)))
        except ValueError:
            # as a last resort, suppress the comment rather than crashing
            pass

# ── ensure_node with subset-reuse & ordering rules ─────────────────────
PRED_RE = re.compile(r"([^\[]+)(\[(.+?)\])?")
def _xmlize_key(k: str) -> str:         # 'xml:lang' → Clark key
    return XML_LANG if k == "xml:lang" else k

def ensure_node(root: ET._Element, rel_path: str, lang: Optional[str]) -> ET._Element:
    cur = root
    parts = [p for p in rel_path.strip("./").split("/") if p]
    for i, step in enumerate(parts):
        m = PRED_RE.fullmatch(step)
        tag, preds = m.group(1), m.group(3)
        attrs: Dict[str, str] = {}
        if preds:
            for pr in preds.split("]["):
                if pr.startswith("@"):
                    k, v = pr[1:].split("=", 1)
                    attrs[_xmlize_key(k)] = v.strip("\"'")
        if lang and i == len(parts) - 1:
            attrs[XML_LANG] = lang
        qtag = QName(tag[4:]) if tag.startswith("tei:") else tag

        # try to reuse --------------------------------------------------
        nxt = None
        for c in cur.findall(qtag):
            if all(c.get(k) == v for k, v in attrs.items()):
                nxt = c
                for k, v in attrs.items():
                    if c.get(k) is None:
                        c.set(k, v)
                break

        # create if absent ---------------------------------------------
        if nxt is None:
            nxt = ET.Element(qtag, attrs)
            # ordering tweaks
            if cur.tag == QName("fileDesc") and tag.endswith("notesStmt"):
                ref = next((c for c in cur.findall(QName("sourceDesc"))), None)
                pos = list(cur).index(ref) if ref is not None else len(cur)
                drop_comment(cur, pos, f"NEW {rel_path} (ordered)")
                cur.insert(pos, nxt)
            elif cur.tag == QName("supportDesc") and tag.endswith("support"):
                ref = next((c for c in cur.findall(QName("extent"))), None)
                pos = list(cur).index(ref) if ref is not None else len(cur)
                drop_comment(cur, pos, f"NEW {rel_path} (ordered)")
                cur.insert(pos, nxt)
            elif cur.tag == QName("history") and tag.endswith("provenance"):
                ref = next((c for c in cur.findall(QName("acquisition"))), None)
                pos = list(cur).index(ref) if ref is not None else len(cur)
                drop_comment(cur, pos, f"NEW {rel_path} (ordered)")
                cur.insert(pos, nxt)
            else:
                drop_comment(cur, len(cur), f"NEW {rel_path}")
                cur.append(nxt)
        cur = nxt
    return cur

# ── value writers ──────────────────────────────────────────────────────
def set_val(node: ET._Element, attr: Optional[str], val: str) -> bool:
    if attr:
        key = _xmlize_key(attr)
        if norm(node.get(key) or "") != norm(val):
            drop_comment(node.getparent(), list(node.getparent()).index(node),
                         f"ATTR {attr} → {val!r}")
            node.set(key, val); return True
    else:
        if norm(node.text or "") != norm(val):
            drop_comment(node.getparent(), list(node.getparent()).index(node),
                         f"TEXT → {val!r}")
            node.text = val; return True
    return False

def update_pers(node: ET._Element, csv_name: str) -> bool:
    sur, fore = (lambda s: (norm(s.split(",",1)[0]), norm(s.split(",",1)[1]))
                 if "," in s else (s.split()[-1], " ".join(s.split()[:-1])))(csv_name)
    before = (node.find("./tei:surname", TEI_NS).text if node.find("./tei:surname", TEI_NS) is not None else "",
              node.find("./tei:forename", TEI_NS).text if node.find("./tei:forename", TEI_NS) is not None else "")
    node[:] = []; ET.SubElement(node, QName("surname")).text = sur
    ET.SubElement(node, QName("forename")).text = fore
    if before != (sur, fore):
        drop_comment(node.getparent(), list(node.getparent()).index(node),
                     f"PERS → {sur}, {fore}"); return True
    return False

# ── duplicate-sibling removal  (drop-in replacement)  ───────────────────
IDENT_ATTRS = {
    QName("date"):  (XML_LANG, "type", "when"),
    QName("ab"):    (XML_LANG,),
    QName("span"):  (XML_LANG,),
    QName("note"):  (XML_LANG, "type"),   # ← new line
}

def deduplicate_tree(root: ET._Element) -> None:
    """
    Remove duplicate leaf-nodes **only**:
      • element has *no* child elements
      • the tuple  (tag, ATTRS, normalised-text) is identical
    Nodes that contain children (e.g. <persName><surname>…) are never touched,
    so <correspAction type="sent"> and "...received" can coexist.
    """
    for parent in root.iter():
        seen: Dict[tuple, ET._Element] = {}
        for child in list(parent):
            if not isinstance(child.tag, str):
                continue
            # skip anything that has element children → non-leaf
            if any(isinstance(x.tag, str) for x in child):
                continue

            key_attrs = IDENT_ATTRS.get(child.tag, (XML_LANG,))
            key = (
                child.tag,
                tuple(child.get(a) for a in key_attrs),
                norm(child.text or "")
            )
            prev = seen.get(key)
            if prev is None:
                seen[key] = child
                continue

            # choose richer node (more attributes) and drop the other
            keep, toss = (child, prev) if len(child.attrib) > len(prev.attrib) else (prev, child)
            seen[key] = keep
            idx = list(parent).index(toss)
            drop_comment(parent, idx,
                         f"REMOVED duplicate {child.tag} lang={child.get(XML_LANG)}")
            parent.remove(toss)

# ── CSV ingest helper ──────────────────────────────────────────────────
def load_rows()->Dict[str,Dict[str,str]]:
    rows={}
    for csv_p in CSV_DIR.glob("*.csv"):
        with csv_p.open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                sig=norm(r.get("Signatur",""));   rows[sig]={k:norm(v) for k,v in r.items()} if sig else rows
    return rows

# ── core patcher ───────────────────────────────────────────────────────
def patch_bibl(bibl: ET._Element, row: Dict[str, str]) -> List[str]:
    changed: List[str] = []

    for col, rules in MAPPING.items():
        cell = row.get(col, "")
        if col == "Sprache":
            cell = cell.lower()

        vals = splitv(cell)
        # pad mapping if CSV has more chunks than rules
        rules += rules[-1:] * (len(vals) - len(rules))

        for val, (xp, attr, lang) in zip(vals, rules):
            node = ensure_node(bibl, xp, lang)

            if val:   # non-empty cell → set / update
                modified = (
                    update_pers(node, val)
                    if col in ("Verfasser*in", "Adressat*in")
                    else set_val(node, attr, val)
                )
            else:     # empty cell → clear existing value
                modified = clear_val(node, attr)

            if modified:
                changed.append(col)

    deduplicate_tree(bibl)
    for act in bibl.findall(".//tei:correspAction", TEI_NS):
        purge_deduced_places(act)
    return changed

# ── deleter (new) ───────────────────────────────────────────────────────
def clear_val(node: ET._Element, attr: Optional[str]) -> bool:
    """
    Remove the attribute or the element’s text.
    Return True if something actually changed.
    """
    if attr:
        key = _xmlize_key(attr)
        if node.get(key) is not None:
            drop_comment(node.getparent(), list(node.getparent()).index(node),
                         f"DEL @{attr}")
            del node.attrib[key]
            return True
    else:
        if (node.text or "").strip():
            drop_comment(node.getparent(), list(node.getparent()).index(node),
                         "DEL text")
            node.text = None
            return True
    # If the mapping told us to clear text (attr is None) and the CSV was empty,
    # remove the whole element—even if attributes such as @ana are still set.
    if attr is None:
        parent = node.getparent()
        if parent is not None:
            drop_comment(parent, list(parent).index(node),
                         f"REMOVED <{ET.QName(node).localname}> after empty cell")
            parent.remove(node)
            return True
    return False

# ── main workflow ──────────────────────────────────────────────────────
def main()->None:
    logging.basicConfig(level=logging.INFO,format="%(message)s",
                        handlers=[logging.FileHandler(LOG_FILE,"w","utf-8"),logging.StreamHandler()])
    OUT_DIR.mkdir(exist_ok=True)
    csv_rows=load_rows(); logging.info("[CSV] rows loaded: %d",len(csv_rows))

    trees: Dict[Path,ET._ElementTree]={}
    sig2paths: Dict[str,List[Path]]=defaultdict(list)

    # index TEI files
    for p in TEI_DIR.glob("*.xml"):
        try: t=ET.parse(p)
        except ET.XMLSyntaxError: logging.warning("parse error in %s – skipped",p.name); continue
        trees[p]=t
        for idn in t.findall(".//tei:idno[@type='signature']",TEI_NS):
            if not idn.text: continue
            key=norm(idn.text)
            if key in sig2paths:
                logging.warning("⚠ duplicate signature %s in %s (already in %s)",
                                key,p.name,", ".join(q.name for q in sig2paths[key]))
            sig2paths[key].append(p)

    dirty={p:False for p in trees}
    stats={"ok":0,"updated":0,"missing":0}

    for sig,row in csv_rows.items():
        for src in sig2paths.get(sig,[]):
            bibl=next((b for b in trees[src].findall(".//tei:biblFull",TEI_NS)
                       if norm(b.findtext('.//tei:idno[@type="signature"]',namespaces=TEI_NS))==sig),None)
            if bibl is None:
                logging.info("!! %s – <biblFull> not found in %s",sig,src.name); stats["missing"]+=1; continue
            mods=patch_bibl(bibl,row)
            if mods:
                dirty[src]=True; stats["updated"]+=1
                logging.info("✓ %s – %s (%s)",sig,", ".join(sorted(set(mods))),src.name)
            else:
                stats["ok"]+=1
                logging.info("· %s – already up-to-date (%s)",sig,src.name)

        if sig not in sig2paths:
            logging.info("!! %s – TEI file missing",sig); stats["missing"]+=1

    written=0
    for p,flag in dirty.items():
        if flag:
            trees[p].write(OUT_DIR/p.name,encoding="utf-8",xml_declaration=True,pretty_print=True); written+=1

    logging.info("--- summary ---")
    logging.info("files: %d  unchanged: %d  updated: %d  missing rows: %d  written: %d",
                 len(trees),stats["ok"],stats["updated"],stats["missing"],written)
    print(f"\nCleaned files → {OUT_DIR.resolve()}  ({written} written)")

# ────────────────────────────────────────────────────────────────────────
if __name__=="__main__":
    main()
