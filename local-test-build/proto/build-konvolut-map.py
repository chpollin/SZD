"""Build konvolut-map.json for the prototype view.

Sources (in ../build, downloaded when missing):
  korrespondenzen-index.xml  TEI_SOURCE of o:szd.korrespondenzen
  dc/<pid with _ for :>.xml  DC datastreams of the konvolut objects (title)
Output: proto/konvolut-map.json keyed by konvolut PID, with title, signatures,
partners (non-Zweig persons and organisations from correspAction) and extent.
"""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent / "build"
NS = {"t": "http://www.tei-c.org/ns/1.0"}
TEI = "{http://www.tei-c.org/ns/1.0}"
INDEX_URL = "https://gams.uni-graz.at/archive/objects/o:szd.korrespondenzen/datastreams/TEI_SOURCE/content"


def text(el):
    return (el.text or "").strip() if el is not None else None


def fetch_dc(pids):
    """Download the DC datastream of every konvolut object not yet cached in build/dc."""
    from concurrent.futures import ThreadPoolExecutor
    (BUILD / "dc").mkdir(parents=True, exist_ok=True)

    def one(pid):
        f = BUILD / "dc" / (pid.replace(":", "_") + ".xml")
        if f.exists() and f.stat().st_size > 0:
            return
        url = f"https://gams.uni-graz.at/archive/objects/{pid}/datastreams/DC/content"
        try:
            f.write_bytes(urllib.request.urlopen(url, timeout=60).read())
        except OSError as e:
            print(f"  {pid}: {e}")

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(one, pids))


def dc_title(pid):
    f = BUILD / "dc" / (pid.replace(":", "_") + ".xml")
    if not f.exists():
        return None
    m = re.search(r"<dc:title>(.*?)</dc:title>", f.read_text(encoding="utf-8"), re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else None


def main():
    index = BUILD / "korrespondenzen-index.xml"
    if not index.exists():
        BUILD.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(INDEX_URL, index)
    root = ET.parse(index).getroot()
    pids = sorted({p for p in (text(i) for i in root.iter(TEI + "idno") if i.get("type") == "konvolut") if p})
    fetch_dc(pids)
    agg = {}
    for bf in root.iter(TEI + "biblFull"):
        pid = text(bf.find('.//t:idno[@type="konvolut"]', NS))
        if not pid:
            continue
        a = agg.setdefault(pid, {"pid": pid, "title": dc_title(pid), "signatures": [], "partners": [], "extent": 0, "entries": 0})
        sig = text(bf.find('.//t:idno[@type="signature"]', NS))
        if sig and sig not in a["signatures"]:
            a["signatures"].append(sig)
        for ca in bf.findall(".//t:correspAction", NS):
            for pn in ca.findall("t:persName", NS):
                sn = pn.findtext("t:surname", default="", namespaces=NS).strip()
                fn = pn.findtext("t:forename", default="", namespaces=NS).strip()
                name = (sn + ", " + fn).strip(", ") if sn else "".join(pn.itertext()).strip()
                if name != "Zweig, Stefan" and name not in a["partners"]:
                    a["partners"].append(name)
            for on in ca.findall("t:orgName", NS):
                name = "".join(on.itertext()).strip()
                if name and name not in a["partners"]:
                    a["partners"].append(name)
        ext = text(bf.find(".//t:measure", NS))
        a["extent"] += int(ext) if ext and ext.isdigit() else 0
        a["entries"] += 1
    # LF only, the fetch script reads it line by line in bash
    (BUILD / "pids.txt").write_text("\n".join(sorted(agg)) + "\n", encoding="utf-8", newline="\n")
    out = HERE / "konvolut-map.json"
    out.write_text(json.dumps(agg, ensure_ascii=False, indent=1), encoding="utf-8")
    missing = sum(1 for a in agg.values() if a["title"] is None)
    print(f"{len(agg)} konvolute -> {out} ({missing} without DC title: object missing on GAMS or fetch failed, see above)")


if __name__ == "__main__":
    main()
