# Dead references, live audit of 2026-10-13

`fix_dead_references.py` repoints references to GAMS objects that production does not serve, found by an audit of the live site on 2026-10-13. Every target was read from production (object root, `TEI_SOURCE` or `DC`), one request at a time with a pause, and each replacement names its evidence in the log.

| File | Old | New | Evidence |
|---|---|---|---|
| `data/Correspondence/SZDKOR.xml`, `SZDKOR.857` | `o:szd.korrespondenzen.podbielski-gert-rene` | `o:szd.korrespondenzen.podbieliki-gert-rene` | Production answers 404 for the first and serves the second, whose single letter carries the same signature `SZ-SAM/B16`. The data follow the misspelt live PID, because renaming a GAMS object is the operator's. |
| `data/Correspondence/SZDKOR.xml`, `SZDKOR.696` | `o:szd.korrespondenzen.unbekannt` | `o:szd.korrespondenzen.unidentified` | Production answers 404 for `unbekannt`. The entry counts `SZ-SAM/AK` pieces from sender "Unbekannt", 1903 to 1939, and `unidentified` is the only Konvolut holding `SZ-SAM/AK` pieces of sender "Unbekannt/Unidentified", the earliest dated 1903. |
| `data/Issue/MarieAntoinette/szd-thema1.xml`, English column | `facs="o:szd.8360"` | `facs="o:szd.143"` | Pre-2022 PID. `SZDLEB.3` and the German column give `o:szd.143` (Hauptbuch, `SZ-SAM/L1`), commit `e71a0edb` fixed only the German line. |
| `data/Issue/Textgenese/szd-thema2.xml` | `o:szd.8249` | `o:szd.233` | Pre-2022 PID. Every linked image is a `SZ_AAP_W45` notebook page, the ring notebook H1 (Werknotizen 7, `SZDMSK.64`). |
| `data/Issue/Textgenese/szd-thema2.xml` | `o:szd.8232` | `o:szd.278` | Pre-2022 PID. Every linked image is a `SZ_AAP_W7` typescript page (`SZDMSK.13`). |
| `data/Issue/Textgenese/szd-thema2.xml` | `o:szd.8231` | `o:szd.234` | Pre-2022 PID for the loose sheets H2. The theme image of H2 ("Dieses Jahr 1837, Menschheit …") is a crop of `IMG.1` of `o:szd.234`, Das erste Wort über den Ozean [Beilage], `SZ-AAP/W45` (`SZDMSK.287`). |
| `webpage/MISCELLANEOUS.xml`, news item 4, German and English | `o:szd.8250` | `o:szd.306` | Pre-2022 PID. The item links `SZDMSK.351`, Über Dostojewsky, whose facsimile is `o:szd.306` (`SZ-LAS/W3`). |

The context anchors (`idno[@type="context"]`) of the two index entries stay unchanged, they are gallery anchors and not object PIDs.

## Procedure

```
python scripts/referenzen_2026_10_13/fix_dead_references.py            # dry run
python scripts/referenzen_2026_10_13/fix_dead_references.py --apply
python scripts/referenzen_2026_10_13/fix_dead_references.py --verify
```

A replacement is written only when its old value occurs exactly as often as expected and, in the index, inside the expected entry. The rewritten text is checked for well-formedness before it is written through `scripts/_szd_io.py`. `--verify` checks that no old value remains and every new one is in place.

## Log

`dead_references_log.csv` holds one row per replaced occurrence with the columns `datei`, `zeile`, `eintrag`, `alt`, `neu` and `beleg`.
