"""Assemble the Lebenskalender prototype inside the live page shell of stefanzweig.digital.

Takes navbar (<header>) and <footer> from the live Lebenskalender page, rewires the
DE|EN switch of the navbar to the prototype's own language toggle, and inserts both
into lebenskalender-szd-template.html. Writes the result to the data repository's
docs site (docs/lebenskalender/index.html) unless another output path is given.

    python build-lebenskalender-szd.py [output.html] [--offline]

--offline uses ../build/lebenskalender-live.html instead of fetching the live page.
The resolved output path is printed before writing; check it, Windows paths are
case-insensitive and a wrong parent level silently lands inside another repository.
"""
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIVE_URL = "https://stefanzweig.digital/o:szd.lebenskalender/sdef:TEI/get?locale=de"
# proto -> local-test-build -> data repository
DEFAULT_OUT = HERE.parents[1] / "docs" / "lebenskalender" / "index.html"


def live_html(offline):
    cached = HERE.parent / "build" / "lebenskalender-live.html"
    if offline and cached.exists():
        return cached.read_text(encoding="utf-8", errors="replace")
    html = urllib.request.urlopen(LIVE_URL, timeout=120).read().decode("utf-8", "replace")
    cached.parent.mkdir(parents=True, exist_ok=True)
    cached.write_text(html, encoding="utf-8")
    return html


def between(html, start_tag, end_tag):
    s = html.find(start_tag)
    e = html.find(end_tag, s) + len(end_tag)
    if s < 0 or e < len(end_tag):
        raise SystemExit(f"{start_tag} not found in live page")
    return html[s:e]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    offline = "--offline" in sys.argv
    out = Path(args[0]).resolve() if args else DEFAULT_OUT
    print(f"output: {out}")
    if not out.parent.exists():
        raise SystemExit("output folder does not exist; create it deliberately first")
    html = live_html(offline)
    header = between(html, "<header", "</header>")
    footer = between(html, "<footer", "</footer>")
    # the navbar language switch reloads the GAMS page; the prototype switches in place
    header = re.sub(
        r"""onclick="jump_to_id_switching_language\('[^']*locale=(de|en)'\)\"""",
        lambda m: f'onclick="setLkLang(\'{m.group(1)}\')"',
        header,
    )
    if "setLkLang" not in header:
        raise SystemExit("language switch not found in navbar; live markup changed?")
    template = (HERE / "lebenskalender-szd-template.html").read_text(encoding="utf-8")
    page = template.replace("{{HEADER}}", header).replace("{{FOOTER}}", footer)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out} ({len(page)} bytes, header {len(header)}, footer {len(footer)})")


if __name__ == "__main__":
    main()
