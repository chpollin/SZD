# Live audit of 2026-10-13, second batch

`fix_audit_findings_2.py` corrects a second batch of findings of the audit of the published site, each only where the repository itself evidences the value. Nothing is read from GAMS. A change is a literal replacement, written only where the old text occurs exactly as often as expected inside its scope, the enclosing entry (`biblFull/@xml:id`) or the language column (`div/@xml:lang`).

| Finding | File | Change | Evidence |
|---|---|---|---|
| `thema6-reply` | `data/Issue/Freud/szd-thema6.xml`, English | `o:szd.122` → `o:szd.996` | `o:szd.122` is a publishing contract (`SZDLEB.38`). The German column links the same reply as `o:szd.996`, `SZ-LAS/B7.9`, letter to Freud of 6 December 1929. |
| `thema6-last-letter` | same | `o:szd.162` → `o:szd.990` | `o:szd.162` answers 404. The German column links the letter of 14 September 1939 as `o:szd.990`, `SZ-LAS/B7.47`. |
| `thema6-scheme` | same | `stefanzweig.digital/…#SZDBIO.87` → `https://stefanzweig.digital/…` | Every other link to the site in the file uses `https://`. |
| `thema6-gallery` | same, German and English | `#SigmundFreud` → `#freud-sigmund` | The anchor does not exist. The context anchor of `SZ-LAS/B7` in `SZDKOR.xml` is `context:szd.facsimiles.korrespondenzen#freud-sigmund`, the heading slug of "Freud, Sigmund". |
| `thema6-space`, `thema6-typo` | same, English | six missing spaces at element boundaries, "Maylan sa" → "Maylan a" | "called Maylan a … and an …" is the only grammatical reading. |
| `thema4-markup` | `data/Issue/Autographen/szd-thema4.xml`, English | `>">An autograph` → `>An autograph` | Markup leftover rendered as text. |
| `thema1-nli` | `data/Issue/MarieAntoinette/szd-thema1.xml`, English | old `merhav.nli.org.il` URL with a literal quote → current URL | The German column gives the same record `NNL_ARCHIVE_AL003432560` under the current URL. |
| `thema1-heading` | same | heading "Hauptbuch" → "Principal Ledger" | English Einheitssachtitel of `SZDLEB.3`. |
| `thema7-locale` | `data/Issue/Masereel-Aufsatz/szd-thema7-masareel.xml`, English | 14 catalogue links `locale=de` → `locale=en` | English column. |
| `szdleb-classification` | `data/PersonalDocument/SZDLEB.xml`, `SZDLEB.40` | "Contracts" → "Publishing Contracts" | Every other entry with "Verlagsverträge" carries "Publishing Contracts". |
| `szdmsk-title` | `data/Work/SZDMSK.xml`, `SZDMSK.289` | "Drei Dicher" → "Drei Dichter", three titles | All three titles carry the typo; the entry's work reference reads "Drei Dichter ihres Lebens" (`#SZDWRK.164`). |
| `about-typo` | `webpage/ABOUT.xml` | "MEADATEN", "TRÄGER*INNENT", "the the" | Plain typos. |
| `konvolut-century` | four Konvolut files | `@when` 20xx → 19xx in eleven entries | See below. |

Konvolut dates are changed only where `@when` lies in the future (year 2027 or later), the display text of the date gives the two-digit year and 19xx falls within Zweig's lifetime. A search of all Konvolut files for any attribute with a year from 2027 found exactly these eleven entries, each with a German and an English `date`.

| Entry | Old | New | Display text |
|---|---|---|---|
| `SZDKOR.freud-sigmund.8` | 2027-03-18 | 1927-03-18 | 18. 3. 27 |
| `SZDKOR.freud-sigmund.9` | 2029-12-06 | 1929-12-06 | 6. 12. 29 |
| `SZDKOR.freud-sigmund.10` | 2029-12-08 | 1929-12-08 | 8. 12. 29 |
| `SZDKOR.freud-sigmund.11` | 2029-12-31 | 1929-12-31 | 31. 12. 29 |
| `SZDKOR.freud-sigmund.12` | 2030-08-12 | 1930-08-12 | 12. 8. 30 |
| `SZDKOR.kaemmerer-maria.B.2` | 2027-02-24 | 1927-02-24 | 24. 2. 27 |
| `SZDKOR.kaemmerer-maria.B.3` | 2027-08-02 | 1927-08-02 | 2. 8. 27 |
| `SZDKOR.mees-friedrich-siegbert.B.2` | 2027-04-19 | 1927-04-19 | 19. 4. 27 |
| `SZDKOR.mees-friedrich-siegbert.B.3` | 2027-05-16 | 1927-05-16 | 16. 5. 27 |
| `SZDKOR.mees-friedrich-siegbert.B.4` | 2030-08-26 | 1930-08-26 | 26. 8. 30 |
| `SZDKOR.unidentified.039` | 2030-09-23 | 1930-09-23 | 23. 9. 30 |

The entry titles of the first ten give the same date with a four-digit 19xx year. `unidentified.039` (`SZ-SAM/AK.287`) has no date in its title; the `SZ-SAM/AK` pieces of unknown senders run from 1903 to 1939 (`SZDKOR.696`).

## Left unchanged

- `szd-thema6.xml`, English, "Maylan egiving it a perfunctory glance": the stray "e" is clear, but whether a comma or "and" belongs there is not.
- `szd-thema6.xml`, English, "Neue Freien Presse" and "Münchener Neuesten Nachrichten": German inflected forms in an English sentence; whether to give the nominative title is editorial.
- `szd-thema6.xml`, German, "in den<ref" before "Münchener Neuesten Nachrichten": a missing space in the German column, outside the scope of this batch.
- Konvolut dates from 1951 to 2026 whose display text also gives a two-digit year, see the [plan](../../knowledge/plan.md#konvolute).

## Run

```
python scripts/audit_2026_10_13_teil2/fix_audit_findings_2.py            # dry run
python scripts/audit_2026_10_13_teil2/fix_audit_findings_2.py --apply
python scripts/audit_2026_10_13_teil2/fix_audit_findings_2.py --verify
```

Files are read and written through [`scripts/_szd_io.py`](../_szd_io.py), so line endings stay as they were, and every changed file is checked well formed before it is written. `--verify` checks that no old text remains in scope, every new one is in place and every file is well formed.

## Log

`audit_findings_2_log.csv` holds one row per replaced occurrence with the columns `befund`, `datei`, `zeile`, `eintrag`, `alt`, `neu` and `beleg`.
