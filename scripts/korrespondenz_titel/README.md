# Normalise the entry titles of the correspondence konvolute

Brings the titles of the single-letter entries in [`data/Correspondence/konvolute/`](../../data/Correspondence/konvolute/) to the pattern that most entries of the same files already carry. It repairs two import leftovers and leaves editorial titles alone.

## Target form

The title convention, with document type, name form and date, is defined in [`knowledge/COLLECTIONS.md`](../../knowledge/COLLECTIONS.md#entry-title-and-date-convention-konvolut-objects). The script applies it with these additional rules.

- Names come from `persName` (`forename` and `surname`), otherwise from the element text.
- The German title takes the date only from `@when`. The English title takes the ISO value and falls back to the display text when the entry has no `@when`. Without a date the date part is dropped.
- `persName/name` with the bilingual value `Unbekannt/Unidentified` is resolved per title language (`Unbekannt`, `Unidentified`). The mapping is an explicit table in the script, and no slash is split in general.

`--verify` measures the convention against the holdings. It reproduces the existing titles in target form except for the editorial name variants listed below.

## Repaired patterns

1. machine-date. German and English title identical, with ISO date or signature in the title text (`Walter Bauer an Stefan Zweig, 1933-01-07, SZ-SAM/AK.284`). This concerns the picture postcards of the signature group `SZ-SAM/AK`.
2. mangled-partner. The German title carries the unresolved source cell `Nachname, Vorname; Nachname, Vorname` instead of the partner names (`Brief von Lotte Zweig an Hannah; Altmann, Manfred Altmann [...]`). The English title of the same entries is already correct.

## Century error in the date

In the machine-date titles the title often carries a plausible year, while `date/@when` expanded the two-digit year of the source into the 2000s (`@when="2021-02-20"` for `20. 2. 21`, title `1921-02-20`). Before the date leaves the title, the script corrects `@when` from the title, provided both differ only in the century and `@when` lies after 1942. Any other difference between title date and `@when` is reported and not changed. The remaining cases are described in [`knowledge/DATA.md`](../../knowledge/DATA.md#century-error-in-two-digit-years).

## Usage

```bash
# 1) dry run with before and after per entry plus residual list, writes nothing
python scripts/korrespondenz_titel/fix_titles.py

# 2) apply
python scripts/korrespondenz_titel/fix_titles.py --apply

# 3) check
python scripts/korrespondenz_titel/fix_titles.py --verify
```

The check compares the working tree with `HEAD` and fails when the number of `biblFull` elements has changed, a file is not well-formed, an element other than `title` has changed its text or an attribute other than `date/@when` its value, or an old pattern remains outside the documented residual list. The run is idempotent, a second dry run reports zero changes.

## Scope

- A German title already in target form is never overwritten, even where it names other names than `correspDesc`. This concerns above all the letters to Lotte Altmann, addressed by her maiden name before the 1939 marriage while `correspAction` gives `Zweig, Lotte`.
- Entries with an empty sender or recipient would get an incomplete title and stay in the residual list, as do the picture postcards without a title date whose `@when` is implausible and whose century the entry cannot prove.
- The serialisation replaces only `titleStmt/title` and `correspAction/date/@when` in the file text. Indentation, attribute order, a missing XML declaration and line endings stay unchanged.
- The index `SZDKOR.xml` describes bundles (`9 Korrespondenzstücke AN/VON Stefan Zweig`) and follows another convention.
- Some files carry double-encoded umlauts from earlier imports. That is a separate finding.
