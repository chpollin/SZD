---
doc: TEI-CSV Mapping
project: fix-szd
version: 1.0
updated: 2025-04-27
tags: [mapping, zweig, tei, csv]
---

# Purpose  

Define an *exhaustive, one-to-one* mapping from each **CSV column** in
`data/*.csv` to the corresponding **TEI element / attribute / value**
inside every `tei/*.xml` file.  
These rules are the contract the validation script must follow.

---

## 1. Namespaces & shorthands

| Shorthand | URI |
|-----------|-----|
| `tei:`    | `http://www.tei-c.org/ns/1.0` |

All XPath expressions below are written with that default namespace.

---

## 2. General conventions  

* **One CSV row ↔ one `<biblFull>`** inside a partner’s TEI file.  
  Match by *signature* (see §3.10).  
* All bilingual free-text values occur twice:  
  *German* (`@xml:lang="de"`) and *English* (`@xml:lang="en"`).  
* Unless noted otherwise the script compares **string equality after
  normalising whitespace** (`strip()` on both sides).  
* Empty CSV cells are considered “not asserted”; their TEI counterpart
  may be missing or empty.  
* Multiple values in a CSV cell (semicolon-separated) map to the
  *sequence* of parallel TEI nodes.

---

## 3. Column-to-TEI mapping table  

| # | CSV column | XPath in `<biblFull>` scope | Cardinality | Notes |
|---|------------|----------------------------|-------------|-------|
| 3.1 | **PID** | `tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:altIdentifier/tei:idno[@type='PID']` | 0‒1 | If empty in CSV the node *may* be absent. |
| 3.2 | **Context** | `tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:altIdentifier/tei:idno[@type='context']` | 0‒1 | May be empty (`<idno type="context"/>`). |
| 3.3 | **Verfasser\*in** | `tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:persName` | 1 | Compare *concatenated* `forename + ' ' + surname`. |
| 3.4 | **Verfasser\*in GND** | same node as 3.3 – attribute `@ref` | 0‒1 | URL. |
| 3.5 | **Körperschaft Verfasser\*in** | `tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:orgName` | 0‒n | Only if CSV cell not empty. |
| 3.6 | **Körperschaft Verfasser\*in GND** | each `orgName/@ref` | 0‒n | 1:1 with 3.5 order. |
| 3.7 | **Adressat\*in** | `tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName` | 1 | |
| 3.8 | **Adressat\*in GND** | node 3.7 `@ref` | 0‒1 | |
| 3.9 | **Körperschaft Adressat\*in** | `tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:orgName` | 0‒n | |
| 3.10 | **Körperschaft Adressat\*in GND** | each `orgName/@ref` | 0‒n | |
| 3.11 | **Art/Umfang** | `tei:fileDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/tei:extent/tei:span[@xml:lang='de']` | 1 | German text. |
| 3.12 | **Physical Description** | same - `@xml:lang='en'` | 1 | English. |
| 3.13 | **Beilagen** | `tei:fileDesc/tei:physDesc//tei:additional/tei:list[@type='enclosure']/tei:item[@xml:lang='de']` | 0‒n | Not in sample; if absent ignore. |
| 3.14 | **Enclosures** | same list but `@xml:lang='en'` | 0‒n | |
| 3.15 | **Datierung Original** | `tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date[@xml:lang='de']` | 1 | Free text (e.g. “19. 9. 30”). |
| 3.16 | **Date original** | same node `@xml:lang='en'` | 1 | |
| 3.17 | **Datierung erschlossen** | `tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date[@type='supplied'][@xml:lang='de']` | 0‒1 | Optional supplied date. |
| 3.18 | **Date supplied/verified** | same `@xml:lang='en'` | 0‒1 | |
| 3.19 | **Datierung normalisiert** | node 3.15/16 attribute `@when` | 1 | ISO 8601 date (`YYYY-MM-DD`). |
| 3.20 | **Poststempel** | `tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:placeName[@type='postmark']` | 0‒1 | String. |
| 3.21 | **Entstehungsort Original** | `tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:placeName[@xml:lang='de']` | 0‒1 | |
| 3.22 | **Entstehungsort erschlossen** | same but `@xml:lang='en']` | 0‒1 | |
| 3.23 | **Postanschrift (original)** | `tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:address/tei:addrLine[@xml:lang='de']` | 0‒n | |
| 3.24 | **Sprache** | `tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:textLang/tei:lang/@xml:lang` | 1 | Compare ISO 639-3 code (“ger”, “deu”, “eng”…). |
| 3.25 | **Beschreibstoff** | `tei:fileDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/tei:support/tei:material[@ana='szdg:WritingMaterial'][@xml:lang='de']` | 1 | |
| 3.26 | **Writing Material** | same `@xml:lang='en'` | 1 | |
| 3.27 | **Schreibstoff** | `tei:fileDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/tei:support/tei:material[@ana='szdg:WritingInstrument'][@xml:lang='de']` | 1 | |
| 3.28 | **Writing Instrument** | same `@xml:lang='en'` | 1 | |
| 3.29 | **Schreiberhand** | `tei:fileDesc/tei:physDesc/tei:handDesc/tei:handNote` | 0‒1 | |
| 3.30 | **Maße** | `tei:fileDesc/tei:physDesc/tei:objectDesc/tei:measureGrp/tei:measure` | 0‒n | Match all values (order irrelevant). |
| 3.31 | **Standort GND** | `tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:repository/@ref` | 1 | |
| 3.32 | **Signatur** | `tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:idno[@type='signature']` | **key** | Primary link between CSV and TEI. |
| 3.33 | **Provenienz** | `tei:fileDesc/tei:history/tei:provenance/tei:ab[@xml:lang='de']` | 0‒1 | |
| 3.34 | **Erwerbung** | `tei:fileDesc/tei:history/tei:acquisition/tei:ab[@xml:lang='de']` | 0‒1 | |
| 3.35 | **Acquired** | same acquisition `@xml:lang='en'` | 0‒1 | |
| 3.36 | **Beteiligte** | `tei:fileDesc/tei:notesStmt/tei:note[@type='participants'][@xml:lang='de']` | 0‒1 | |
| 3.37 | **Beteiligte (GND)** | each `<name @type='participant'/>/@ref` | 0‒n | |
| 3.38 | **Hinweis** | `tei:fileDesc/tei:notesStmt/tei:note[@type='hint'][@xml:lang='de']` | 0‒1 | |
| 3.39 | **Note(s)** | same `@xml:lang='en'` | 0‒1 | |
| 3.40 | **Postanschrift normalisiert** | `tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:address/tei:addrLine[@type='normalized']` | 0‒n | |
| 3.41 | **Anmerkungen** | `tei:fileDesc/tei:notesStmt/tei:note[@type='comment'][@xml:lang='de']` | 0‒n | Catch-all German comments. |

---

## 4. Validation guidelines for the script

1. **Locate TEI**  
   *Find the TEI file whose `<idno type="signature">` matches the
   row’s `Signatur`.*
2. **Traverse mapping**  
   For each column **C** with non-empty value:  
   * Evaluate XPath **P(C)**.  
   * Fail if **no node** found.  
   * Fail if **count** outside allowed cardinality.  
   * For bilingual columns check *both* languages.  
   * Trim whitespace on both ends before comparing.  
3. **Report**  
   *One line per row, listing mismatches; OK rows may be silent or counted.*

---

## 5. Example – sample row vs. TEI

| Column | CSV value | TEI node (XPath result) |
|--------|-----------|--------------------------|
| Signatur | **SZ-SAM/AK.1** | `<idno type="signature">SZ-SAM/AK.1</idno>` |
| Verfasser\*in | Alberts Margot | `<persName><surname>Alberts</surname><forename>Margot</forename></persName>` |
| Adressat\*in GND | `http://d-nb.info/gnd/118637479` | `<persName ref="http://d-nb.info/gnd/118637479">…Zweig…</persName>` |
| Datierung normalisiert | 1930-09-19 | `<date when="1930-09-19">19. 9. 30</date>` |
| Writing Material | Picture postcard: "Nella Villa Carlotta" | `<material ana="szdg:WritingMaterial" xml:lang="en">Picture postcard: "Nella Villa Carlotta"</material>` |

✔︎ All sample values match the provided TEI snippet.

---

*End of mapping file.*
