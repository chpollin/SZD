"""
Klawiter \u2194 SZDWRK Reconciliation
===================================

Matches Klawiter bibliography entries to SZDWRK work index entries
using a multi-stage approach:
  1. Exact title matching
  2. Normalized title matching (lowercase, stripped, no subtitles)
  3. Fuzzy title matching (difflib SequenceMatcher, >=0.85)

Outputs:
  - scripts/reconciliation_results.json \u2014 full match data
  - scripts/reconciliation_report.md \u2014 human-readable report
  - ontology/reconciliation.ttl \u2014 RDF triples (szdo:hatManifestation)

Usage:
    python scripts/reconcile_klawiter.py
"""

import sys
import os
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from difflib import SequenceMatcher
from lxml import etree

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).parent.parent
SZDWRK_FILE = PROJECT_ROOT / "data" / "Index" / "Werke" / "SZDWRK.xml"
KLAWITER_FILE = Path(os.environ.get(
    "KLAWITER_JSON",
    Path(__file__).parent.parent.parent / "klawiter-rescue" / "docs" / "data" / "klawiter.json"
))
RESULTS_FILE = Path(__file__).parent / "reconciliation_results.json"
REPORT_FILE = Path(__file__).parent / "reconciliation_report.md"
TTL_FILE = PROJECT_ROOT / "ontology" / "reconciliation.ttl"

TEI_NS = "http://www.tei-c.org/ns/1.0"

# Entry types that represent Zweig's own works (not secondary literature)
PRIMARY_TYPES = {
    "fiction", "essay", "poetry", "drama", "collected-works",
    "correspondence", "film", "translation", "foreword",
    "dramatic-reading", "newspaper",
}
SECONDARY_TYPES = {"secondary-literature", "historical-study", "symposium"}


# ---------------------------------------------------------------------------
# 1. Parse SZDWRK
# ---------------------------------------------------------------------------

def parse_szdwrk():
    """Parse SZDWRK.xml and return list of work entries."""
    tree = etree.parse(str(SZDWRK_FILE))
    ns = {"t": TEI_NS}
    works = []

    for bibl in tree.xpath("//t:bibl", namespaces=ns):
        xml_id = bibl.get("{http://www.w3.org/XML/1998/namespace}id", "")
        sort_key = bibl.get("sortKey", "")
        title_el = bibl.find("t:title", ns)
        title = title_el.text.strip() if title_el is not None and title_el.text else sort_key
        gnd_ref = title_el.get("ref", "") if title_el is not None else ""
        gnd_id = ""
        if "gnd/" in gnd_ref:
            gnd_id = gnd_ref.split("gnd/")[-1]

        # Type attribute
        btype = bibl.get("type", "")

        # Language
        lang_el = bibl.find("t:lang", ns)
        lang = lang_el.text.strip() if lang_el is not None and lang_el.text else ""

        # Date
        date_el = bibl.find(".//t:date", ns)
        date = date_el.get("when", "") if date_el is not None else ""

        works.append({
            "id": xml_id,
            "title": title,
            "sortKey": sort_key,
            "gnd": gnd_id,
            "gnd_uri": gnd_ref,
            "type": btype,
            "lang": lang,
            "date": date,
        })

    return works


# ---------------------------------------------------------------------------
# 2. Parse Klawiter
# ---------------------------------------------------------------------------

def parse_klawiter():
    """Parse Klawiter JSON and return bibliography entries."""
    with open(str(KLAWITER_FILE), encoding="utf-8") as f:
        data = json.load(f)

    entries = []
    for e in data.get("entries", []):
        etype = e.get("entryType", "")
        if etype in ("mediawiki", "category", "redirect", "template", "help", "file"):
            continue
        entries.append({
            "id": e.get("@id", ""),
            "page_id": e.get("sourcePageId", 0),
            "title": e.get("title", ""),
            "year": e.get("year"),
            "type": etype,
            "language": e.get("language", ""),
            "languageCode": e.get("languageCode", ""),
            "publisher": e.get("publisher", ""),
            "location": e.get("location", ""),
            "mainCategory": e.get("mainCategory", ""),
        })

    return entries


# ---------------------------------------------------------------------------
# 3. Normalization
# ---------------------------------------------------------------------------

def normalize(title):
    """Normalize a title for matching."""
    t = title.strip().lower()
    # Remove parenthetical year/info
    t = re.sub(r"\s*\(.*?\)\s*", " ", t)
    # Remove subtitle after colon or dash
    t = re.sub(r"\s*[:\-\u2013\u2014]\s.*$", "", t)
    # Remove punctuation
    t = re.sub(r'[.,;!?\"\'\u00bb\u00ab\u201e\u201c()\[\]]', '', t)
    # Normalize whitespace
    t = re.sub(r"\s+", " ", t).strip()
    # Normalize umlauts
    t = t.replace("\u00e4", "ae").replace("\u00f6", "oe").replace("\u00fc", "ue")
    t = t.replace("\u00df", "ss")
    return t


def similarity(a, b):
    """Compute string similarity ratio."""
    return SequenceMatcher(None, a, b).ratio()


# ---------------------------------------------------------------------------
# 4. Matching
# ---------------------------------------------------------------------------

def _match_stage(works, index, key_fn, matched_ids,
                 confidence_primary, confidence_secondary,
                 method_primary, method_secondary):
    """Run a single matching stage against an index.

    Parameters
    ----------
    works : list
        SZDWRK work entries.
    index : dict
        Mapping from key (produced by *key_fn*) to list of Klawiter entries.
    key_fn : callable
        Receives a work dict, returns the lookup key (or None to skip).
    matched_ids : set
        Work IDs already matched in earlier stages (mutated in place).
    confidence_primary / confidence_secondary : float
        Confidence scores assigned to primary / secondary matches.
    method_primary / method_secondary : str
        Method labels assigned to primary / secondary matches.

    Returns
    -------
    list of (work, klawiter_entry, confidence, method) tuples.
    """
    stage_matches = []
    for w in works:
        if w["id"] in matched_ids:
            continue
        key = key_fn(w)
        if not key:
            continue
        candidates = index.get(key, [])
        primary = [c for c in candidates if c["type"] in PRIMARY_TYPES]
        if primary:
            for c in primary:
                stage_matches.append((w, c, confidence_primary, method_primary))
            matched_ids.add(w["id"])
        elif candidates:
            for c in candidates:
                stage_matches.append((w, c, confidence_secondary, method_secondary))
            matched_ids.add(w["id"])
    return stage_matches


def _fuzzy_match_stage(works, klawiter_entries, matched_ids):
    """Fuzzy title matching stage (primary types only, >=0.85 similarity).

    Parameters
    ----------
    works : list
        SZDWRK work entries.
    klawiter_entries : list
        All Klawiter entries.
    matched_ids : set
        Work IDs already matched (mutated in place).

    Returns
    -------
    list of (work, klawiter_entry, confidence, method) tuples.
    """
    stage_matches = []
    remaining_works = [w for w in works if w["id"] not in matched_ids]
    primary_kl = [e for e in klawiter_entries if e["type"] in PRIMARY_TYPES]

    for w in remaining_works:
        wt_norm = normalize(w["title"])
        if not wt_norm or len(wt_norm) < 3:
            continue
        best_sim = 0
        best_candidates = []
        for e in primary_kl:
            et_norm = normalize(e["title"])
            if not et_norm:
                continue
            sim = similarity(wt_norm, et_norm)
            if sim > best_sim and sim >= 0.85:
                best_sim = sim
                best_candidates = [(e, sim)]
            elif sim == best_sim and sim >= 0.85:
                best_candidates.append((e, sim))

        for c, sim in best_candidates[:3]:  # Max 3 fuzzy matches per work
            stage_matches.append((w, c, round(sim * 0.9, 3), "fuzzy_title"))
        if best_candidates:
            matched_ids.add(w["id"])

    return stage_matches


def reconcile(works, klawiter_entries):
    """Multi-stage matching."""
    matched_work_ids = set()

    # Build Klawiter indexes
    kl_by_title_exact = defaultdict(list)
    kl_by_title_norm = defaultdict(list)
    for e in klawiter_entries:
        kl_by_title_exact[e["title"].strip().lower()].append(e)
        kl_by_title_norm[normalize(e["title"])].append(e)

    # Stage 1: Exact title match
    exact_matches = _match_stage(
        works, kl_by_title_exact,
        key_fn=lambda w: w["title"].strip().lower(),
        matched_ids=matched_work_ids,
        confidence_primary=0.95, confidence_secondary=0.90,
        method_primary="exact_title", method_secondary="exact_title_secondary",
    )

    # Stage 2: Normalized title match
    norm_matches = _match_stage(
        works, kl_by_title_norm,
        key_fn=lambda w: normalize(w["title"]) or None,
        matched_ids=matched_work_ids,
        confidence_primary=0.85, confidence_secondary=0.80,
        method_primary="normalized_title", method_secondary="normalized_title_secondary",
    )

    # Stage 3: Fuzzy title match
    fuzzy_matches = _fuzzy_match_stage(works, klawiter_entries, matched_work_ids)

    matches = exact_matches + norm_matches + fuzzy_matches
    return matches, matched_work_ids


# ---------------------------------------------------------------------------
# 5. Output: JSON
# ---------------------------------------------------------------------------

def write_json(matches, works, matched_ids):
    results = {
        "meta": {
            "total_works": len(works),
            "matched_works": len(matched_ids),
            "total_matches": len(matches),
            "match_rate": round(len(matched_ids) / len(works) * 100, 1),
        },
        "matches": [],
    }
    for w, k, conf, method in sorted(matches, key=lambda x: (-x[2], x[0]["id"])):
        results["matches"].append({
            "work_id": w["id"],
            "work_title": w["title"],
            "work_gnd": w["gnd"],
            "klawiter_id": k["id"],
            "klawiter_title": k["title"],
            "klawiter_type": k["type"],
            "klawiter_year": k["year"],
            "klawiter_language": k["language"],
            "confidence": conf,
            "method": method,
        })
    RESULTS_FILE.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return results


# ---------------------------------------------------------------------------
# 6. Output: Markdown Report
# ---------------------------------------------------------------------------

def compute_match_stats(results):
    """Compute aggregated match statistics from results.

    Returns
    -------
    dict with keys:
        method_counts : Counter  -- matches per method
        type_counts   : Counter  -- matches per Klawiter type
    """
    method_counts = Counter(m["method"] for m in results["matches"])
    type_counts = Counter(m["klawiter_type"] for m in results["matches"])
    return {
        "method_counts": method_counts,
        "type_counts": type_counts,
    }


def write_report(results):
    meta = results["meta"]
    stats = compute_match_stats(results)
    method_counts = stats["method_counts"]
    type_counts = stats["type_counts"]

    lines = [
        "# Klawiter \u2194 SZDWRK Reconciliation Report",
        "",
        f"**Datum:** {__import__('datetime').date.today().isoformat()}",
        f"**SZDWRK Werke:** {meta['total_works']}",
        f"**Gematchte Werke:** {meta['matched_works']} ({meta['match_rate']}%)",
        f"**Gesamte Matches:** {meta['total_matches']} (ein Werk kann mehrere Klawiter-Eintr\u00e4ge haben)",
        "",
        "## Methoden-Verteilung",
        "",
        "| Methode | Matches | Konfidenz |",
        "|---------|---------|-----------|",
    ]

    method_labels = {
        "exact_title": "Exakter Titel",
        "exact_title_secondary": "Exakter Titel (Sekund\u00e4rlit.)",
        "normalized_title": "Normalisierter Titel",
        "normalized_title_secondary": "Normalisiert (Sekund\u00e4rlit.)",
        "fuzzy_title": "Fuzzy-Match (>=85%)",
    }
    for method, count in method_counts.most_common():
        label = method_labels.get(method, method)
        confs = [m["confidence"] for m in results["matches"] if m["method"] == method]
        avg_conf = sum(confs) / len(confs) if confs else 0
        lines.append(f"| {label} | {count} | {avg_conf:.0%} |")

    lines += [
        "",
        "## Matches nach Klawiter-Typ",
        "",
        "| Typ | Matches |",
        "|-----|---------|",
    ]
    for t, n in type_counts.most_common():
        lines.append(f"| {t} | {n} |")

    lines += [
        "",
        "## Top-Matches (Konfidenz >= 0.90)",
        "",
        "| SZDWRK | Titel | Klawiter | Typ | Jahr | Konfidenz |",
        "|--------|-------|----------|-----|------|-----------|",
    ]
    for m in results["matches"]:
        if m["confidence"] >= 0.90:
            kl_short = m['klawiter_id'].split('/')[-1]
            year = m['klawiter_year'] or '\u2014'
            lines.append(
                f"| {m['work_id']} | {m['work_title'][:40]} | {kl_short} | {m['klawiter_type']} | {year} | {m['confidence']:.0%} |"
            )

    lines += [
        "",
        "## Nicht gematchte Werke",
        "",
    ]
    matched_wids = set(m["work_id"] for m in results["matches"])
    # We need access to full works list \u2014 pass it through
    lines.append("*(Siehe reconciliation_results.json f\u00fcr Details)*")

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# 7. Output: RDF Triples (Turtle)
# ---------------------------------------------------------------------------

def write_ttl(results):
    lines = [
        '@prefix szdo:    <https://gams.uni-graz.at/o:szd.ontology#> .',
        '@prefix gams:    <https://gams.uni-graz.at/> .',
        '@prefix klawiter: <https://klawiter-rescue.github.io/vocab/> .',
        '@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .',
        '@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .',
        '@prefix dcterms: <http://purl.org/dc/terms/> .',
        '',
        '# =============================================================================',
        '# Klawiter <-> SZDWRK Reconciliation Triples',
        '# Generated by scripts/reconcile_klawiter.py',
        '# =============================================================================',
        '',
    ]

    # Group by work
    work_matches = defaultdict(list)
    for m in results["matches"]:
        work_matches[m["work_id"]].append(m)

    for work_id, matches_list in sorted(work_matches.items()):
        w = matches_list[0]
        work_uri = f"gams:o:szd.werkindex#{work_id}"
        safe_title = w['work_title'].replace('\n', ' ').replace('\r', ' ').strip()
        lines.append(f"# {work_id}: {safe_title[:80]}")
        lines.append(f"{work_uri}")

        for i, m in enumerate(matches_list):
            kl_uri = m["klawiter_id"].replace("klawiter:", "klawiter:")
            prop = "szdo:hatManifestation" if m["klawiter_type"] in PRIMARY_TYPES else "szdo:wirdBehandeltIn"
            sep = " ;" if i < len(matches_list) - 1 else " ."
            lines.append(f'    {prop} <https://klawiter-rescue.github.io/vocab/{m["klawiter_id"].split(":")[-1]}>{sep}')
            lines.append(f'    # \u2192 {m["klawiter_title"][:60]} [{m["klawiter_type"]}] conf:{m["confidence"]:.0%}')

        lines.append("")

    TTL_FILE.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Klawiter <-> SZDWRK Reconciliation")
    print("=" * 50)

    # Parse
    print("[1/5] Parsing SZDWRK ...")
    works = parse_szdwrk()
    print(f"       {len(works)} works")
    gnd_count = sum(1 for w in works if w["gnd"])
    print(f"       {gnd_count} with GND identifiers")

    print("[2/5] Parsing Klawiter ...")
    kl = parse_klawiter()
    print(f"       {len(kl)} entries")
    primary = sum(1 for e in kl if e["type"] in PRIMARY_TYPES)
    secondary = sum(1 for e in kl if e["type"] in SECONDARY_TYPES)
    print(f"       {primary} primary (Zweig's works), {secondary} secondary (about Zweig)")

    # Match
    print("[3/5] Reconciling ...")
    matches, matched_ids = reconcile(works, kl)
    print(f"       {len(matched_ids)}/{len(works)} works matched ({len(matched_ids)/len(works)*100:.1f}%)")
    print(f"       {len(matches)} total matches (incl. multiple per work)")

    # Output
    print("[4/5] Writing results ...")
    results = write_json(matches, works, matched_ids)
    write_report(results)
    print(f"       {RESULTS_FILE}")
    print(f"       {REPORT_FILE}")

    print("[5/5] Writing RDF triples ...")
    write_ttl(results)
    print(f"       {TTL_FILE}")

    # Summary
    print()
    print("SUMMARY")
    print("-" * 50)
    print(f"  SZDWRK works:        {len(works)}")
    print(f"  Klawiter entries:    {len(kl)}")
    print(f"  Matched works:       {len(matched_ids)} ({len(matched_ids)/len(works)*100:.1f}%)")
    print(f"  Total match links:   {len(matches)}")
    mc = Counter(m[3] for m in matches)
    for method, count in mc.most_common():
        print(f"    {method}: {count}")


if __name__ == "__main__":
    main()
