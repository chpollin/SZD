# Lebenskalender prototype

Static prototype of an alternative presentation of the biography (`o:szd.lebenskalender`),
published with the docs site at https://chpollin.github.io/SZD/lebenskalender/.
It adds a sticky year scale with event density, place filters, a compact/full toggle
and DE/EN switching without reload. Person names link to the person search of the
live site, library references to the library entry.

`SZDBIO.xml` is a copy of `data/Biography/SZDBIO.xml`, because GitHub Pages serves
only `docs/`. Refresh it after changes to the biography TEI:

    cp data/Biography/SZDBIO.xml docs/lebenskalender/SZDBIO.xml

`lanes/` holds the derived timeline lanes, written by
`scripts/lebenskalender_lanes/build_lanes.py` alongside the copy in
`data/derived/lebenskalender/`. The multi-collection timeline built from them is part of
the presentation repository `ZIMLAB/szd` (`mode=timeline`, with `mode=fancy` as alias) and
loads its own copy of the lane files. This static biography prototype remains a separate
view. Schema, coverage and delivery state of the lanes are in
[knowledge/Lebenskalender-Lanes.md](../../knowledge/Lebenskalender-Lanes.md).

`index.html` is generated. It embeds the navbar and footer of the live page and loads
the live stylesheets via `<base href="https://stefanzweig.digital/">`, so the page
shows the prototype inside the real SZD design. Generator and template live in the
presentation repository (`gams-www`, `local-test-build/proto/build-lebenskalender-szd.py`
and `lebenskalender-szd-template.html`). Rerun the generator when the live navbar
changes. Do not edit `index.html` by hand. The docs-site variant of the same prototype
is kept there as `lebenskalender-proto.html` with a jsdom smoke test.
