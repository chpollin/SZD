---
title: Konvolut title curation
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD  # the served files it describes are in https://zimlab.uni-graz.at/gams/projects/szd/gams-www
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: snapshot
language: en
created: 2026-09-10
updated: 2026-10-28
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Opus 5.5)
related: [correspondence-gallery-architecture, plan]
---

# Konvolut title curation

Curation sheet for readable titles of the B shelfmark groups in the Konvolut mode of the correspondence gallery, generated on 2026-09-10 from the gallery data of `context:szd.facsimiles.korrespondenzen`. Piece counts and partner lists are the state of that day. The grouping it serves is described in [correspondence-gallery-architecture](correspondence-gallery-architecture.md#three-konvolut-levels). The sheet matters only as long as the B shelfmark view is kept, because a view coupled to the curated Personen-Konvolute would take its titles from the Konvolut objects, see [plan](plan.md#operator-questions). The row `SZ-SAM/AK` stands for the Personen-Konvolute of all postcard senders.

## Use

The column "Current title (fallback)" is what the page shows today, because `KONVOLUT_TITLES` in `js/facsimiles-konvolut.js` of gams-www is empty. The two right-hand columns take the curated plain titles (de, en) by the archive staff of the Literaturarchiv Salzburg. Once filled in, they move into `KONVOLUT_TITLES` and replace the fallback.

- Konvolute with exactly one partner usually take the title "Korrespondenz <partner> und Stefan Zweig", and the table names the recognised partner.
- Collective Konvolute with several partners, marked "collective" in the column "Note", need a curated bundle title (family, couple, publisher). For large Konvolute the partner assignment from Dublin Core can differ from the archival definition, for instance `SZ-AAP/B1` lists many partners but is "Reichner" according to the archive.
- Picture postcards (`AK`) and single pieces (`L`) are no Konvolute, a title is optional.

| # | Key | Class | Pieces | Current title (fallback) | Recognised partners | Note | Title de (curated) | Title en (curated) |
|---|---|---|---|---|---|---|---|---|
| 1 | `HD-AHL/B1` | Konvolut | 1 | Konvolut HD-AHL/B1 | Deißinger, Hans |  |  |  |
| 2 | `SZ-AAL/B1` | Konvolut | 201 | Konvolut SZ-AAL/B1 | Altmann, Eva; Altmann, Hannah; Broch, Hermann; Unidentified; Zweig, Lotte | collective |  |  |
| 3 | `SZ-AAL/B2` | Konvolut | 97 | Konvolut SZ-AAL/B2 | Altmann, Lotte; Zweig, Lotte | collective |  |  |
| 4 | `SZ-AAL/B3` | Konvolut | 144 | Konvolut SZ-AAL/B3 | Galatti, R.; Geiringer, Josef; Haupolter, Walter; Hofmannsthal, Emil von; Meiler, Friedrich; Thalhuber, Joh… | collective |  |  |
| 5 | `SZ-AAL/B4` | Konvolut | 9 | Konvolut SZ-AAL/B4 | Maass, Joachim |  |  |  |
| 6 | `SZ-AAL/B5` | Konvolut | 2 | Konvolut SZ-AAL/B5 | Walter, Rose |  |  |  |
| 7 | `SZ-AAL/B6` | Konvolut | 1 | Konvolut SZ-AAL/B6 | Zweig, Friderike |  |  |  |
| 8 | `SZ-AAL/B7` | Konvolut | 2 | Konvolut SZ-AAL/B7 | Kaufmann, Charlotte |  |  |  |
| 9 | `SZ-AAL/B8` | Konvolut | 2 | Konvolut SZ-AAL/B8 | Bauer, Walter |  |  |  |
| 10 | `SZ-AAL/B9` | Konvolut | 4 | Konvolut SZ-AAL/B9 | Roth, Joseph |  |  |  |
| 11 | `SZ-AAL/B10` | Konvolut | 9 | Konvolut SZ-AAL/B10 | Birman, C.; Süssland, Ernst; Trading; Zweig, Alfred | collective |  |  |
| 12 | `SZ-AAL/B11` | Konvolut | 1 | Konvolut SZ-AAL/B11 | Wolfenstein, Alfred |  |  |  |
| 13 | `SZ-AAL/B12` | Konvolut | 1 | Konvolut SZ-AAL/B12 | Beierle, Alfred |  |  |  |
| 14 | `SZ-AAL/B13` | Konvolut | 1 | Konvolut SZ-AAL/B13 | Zarek, Otto |  |  |  |
| 15 | `SZ-AAL/B14` | Konvolut | 1 | Konvolut SZ-AAL/B14 | Frenkel, Lotte |  |  |  |
| 16 | `SZ-AAL/B15` | Konvolut | 1 | Konvolut SZ-AAL/B15 | Kiefer, Oskar Alexander |  |  |  |
| 17 | `SZ-AAL/B16` | Konvolut | 1 | Konvolut SZ-AAL/B16 | Chaine, René |  |  |  |
| 18 | `SZ-AAL/B17` | Konvolut | 1 | Konvolut SZ-AAL/B17 | Rieger, Erwin |  |  |  |
| 19 | `SZ-AAL/B18` | Konvolut | 1 | Konvolut SZ-AAL/B18 | Monath, Paul |  |  |  |
| 20 | `SZ-AAL/B19` | Konvolut | 1 | Konvolut SZ-AAL/B19 | Sambat, M. |  |  |  |
| 21 | `SZ-AAL/B20` | Konvolut | 1 | Konvolut SZ-AAL/B20 | Garcés, Mario |  |  |  |
| 22 | `SZ-AAL/B21` | Konvolut | 1 | Konvolut SZ-AAL/B21 | Singer, Emmerich |  |  |  |
| 23 | `SZ-AAP/B1` | Konvolut | 273 | Konvolut SZ-AAP/B1 | Allert de Lange; Bing, Edward; Brüder Wltžek, Buchhandlung; Buchhandlung Julius Kittls Nachfolger; Cassell … | collective |  |  |
| 24 | `SZ-AAP/B2` | Konvolut | 74 | Konvolut SZ-AAP/B2 | Friedenthal, Richard; Unbekannt | collective |  |  |
| 25 | `SZ-AAP/B3` | Konvolut | 34 | Konvolut SZ-AAP/B3 | International Copyright Bureau Ltd., The; Romains, Jules; Theatre Guild, New York; Unbekannt | collective |  |  |
| 26 | `SZ-AAP/B4` | Konvolut | 1 | Konvolut SZ-AAP/B4 | Martin Du Gard, Roger |  |  |  |
| 27 | `SZ-AAP/B5` | Konvolut | 3 | Konvolut SZ-AAP/B5 | Nygaard, Mads |  |  |  |
| 28 | `SZ-AAP/B6` | Konvolut | 1 | Konvolut SZ-AAP/B6 | Strauss, Richard |  |  |  |
| 29 | `SZ-AAP/B7` | Konvolut | 1 | Konvolut SZ-AAP/B7 | Szilley, Béla von |  |  |  |
| 30 | `SZ-AAP/B8` | Konvolut | 1 | Konvolut SZ-AAP/B8 | Willert, Paul |  |  |  |
| 31 | `SZ-AAP/B9` | Konvolut | 1 | Konvolut SZ-AAP/B9 | Viertel, Berthold |  |  |  |
| 32 | `SZ-AAP/B10` | Konvolut | 5 | Konvolut SZ-AAP/B10 | Zweig, Alfred; Zweig, Lotte; Zweig, Stefanie | collective |  |  |
| 33 | `SZ-AAP/B11` | Konvolut | 2 | Konvolut SZ-AAP/B11 | Zweig, Friderike |  |  |  |
| 34 | `SZ-AAP/B12` | Konvolut | 1 | Konvolut SZ-AAP/B12 | Unbekannt |  |  |  |
| 35 | `SZ-AAP/B13` | Konvolut | 2 | Konvolut SZ-AAP/B13 | Fuchs, Emil; Zweig, Lotte | collective |  |  |
| 36 | `SZ-AAP/B14` | Konvolut | 1 | Konvolut SZ-AAP/B14 | Cohen, Betty |  |  |  |
| 37 | `SZ-AAP/L` | Einzelstücke | 18 | Einzelstücke SZ-AAP | — |  |  |  |
| 38 | `SZ-AP2/L` | Einzelstücke | 8 | Einzelstücke SZ-AP2 | — |  |  |  |
| 39 | `SZ-LAS/B1` | Konvolut | 65 | Konvolut SZ-LAS/B1 | Masereel, Frans; Zweig, Friderike | collective |  |  |
| 40 | `SZ-LAS/B2` | Konvolut | 8 | Konvolut SZ-LAS/B2 | Romains, Jules |  |  |  |
| 41 | `SZ-LAS/B3` | Konvolut | 75 | Konvolut SZ-LAS/B3 | Fleischer, Max; Fleischer, Victor; Zweig, Friderike | collective |  |  |
| 42 | `SZ-LAS/B4` | Konvolut | 6 | Konvolut SZ-LAS/B4 | Hirschfeld, Eugenie; Kubin, Alfred; Unbekannt | collective |  |  |
| 43 | `SZ-LAS/B5` | Konvolut | 1 | Konvolut SZ-LAS/B5 | Winternitz, Alix |  |  |  |
| 44 | `SZ-LAS/B6` | Konvolut | 1 | Konvolut SZ-LAS/B6 | Unbekannt |  |  |  |
| 45 | `SZ-LAS/B7` | Konvolut | 48 | Konvolut SZ-LAS/B7 | Freud, Anna; Freud, Sigmund | collective |  |  |
| 46 | `SZ-SAH/B1` | Konvolut | 2 | Konvolut SZ-SAH/B1 | Fleischer, Victor; Heidelbach, Paul | collective |  |  |
| 47 | `SZ-SAH/B2` | Konvolut | 5 | Konvolut SZ-SAH/B2 | Mees, Friedrich Siegbert |  |  |  |
| 48 | `SZ-SAH/B3` | Konvolut | 1 | Konvolut SZ-SAH/B3 | Weissel, Otto |  |  |  |
| 49 | `SZ-SAH/B4` | Konvolut | 1 | Konvolut SZ-SAH/B4 | York-Steiner, Heinrich |  |  |  |
| 50 | `SZ-SAH/B5` | Konvolut | 1 | Konvolut SZ-SAH/B5 | Zander, Moritz |  |  |  |
| 51 | `SZ-SAH/B6` | Konvolut | 1 | Konvolut SZ-SAH/B6 | Unbekannt |  |  |  |
| 52 | `SZ-SAH/B7` | Konvolut | 1 | Konvolut SZ-SAH/B7 | Hauptmann, Gerhart |  |  |  |
| 53 | `SZ-SAM/AK` | Ansichtskarten | 301 | Ansichtskarten SZ-SAM | Alberts, Margot; Alexich-Brettauer, Erna; Ammers-Küller, Jo van; Arens, Hanns; Baer, [unbekannt]; Bandler, … |  |  |  |
| 54 | `SZ-SAM/B1` | Konvolut | 1 | Konvolut SZ-SAM/B1 | Gans, Helmut |  |  |  |
| 55 | `SZ-SAM/B2` | Konvolut | 1 | Konvolut SZ-SAM/B2 | Hasenstab, Irene |  |  |  |
| 56 | `SZ-SAM/B3` | Konvolut | 1 | Konvolut SZ-SAM/B3 | Clemens, Cyril |  |  |  |
| 57 | `SZ-SAM/B4` | Konvolut | 4 | Konvolut SZ-SAM/B4 | Meingast, Anna |  |  |  |
| 58 | `SZ-SAM/B5` | Konvolut | 3 | Konvolut SZ-SAM/B5 | Rolland, Romain |  |  |  |
| 59 | `SZ-SAM/B6` | Konvolut | 1 | Konvolut SZ-SAM/B6 | Unbekannt |  |  |  |
| 60 | `SZ-SAM/B7` | Konvolut | 105 | Konvolut SZ-SAM/B7 | Meingast, Anna; Zweig, Friderike | collective |  |  |
| 61 | `SZ-SAM/B8` | Konvolut | 1 | Konvolut SZ-SAM/B8 | Strauss, Richard |  |  |  |
| 62 | `SZ-SAM/B9` | Konvolut | 1 | Konvolut SZ-SAM/B9 | Wolf, Hugo |  |  |  |
| 63 | `SZ-SAM/B10` | Konvolut | 19 | Konvolut SZ-SAM/B10 | Meingast, Anna; Zweig, Lotte | collective |  |  |
| 64 | `SZ-SAM/B11` | Konvolut | 19 | Konvolut SZ-SAM/B11 | Meingast, Anna; Zweig, Friderike | collective |  |  |
| 65 | `SZ-SAM/B12` | Konvolut | 1 | Konvolut SZ-SAM/B12 | Meingast, Anna; Winternitz, Suse von | collective |  |  |
| 66 | `SZ-SAM/B13` | Konvolut | 1 | Konvolut SZ-SAM/B13 | Bellonk, Erich; Meingast, Anna | collective |  |  |
| 67 | `SZ-SAM/B14` | Konvolut | 1 | Konvolut SZ-SAM/B14 | Einstein, Alfred; Meingast, Anna | collective |  |  |
| 68 | `SZ-SAM/B15` | Konvolut | 1 | Konvolut SZ-SAM/B15 | Mazzucchetti, Lavinia; Meingast, Anna | collective |  |  |
| 69 | `SZ-SAM/B16` | Konvolut | 1 | Konvolut SZ-SAM/B16 | Meingast, Anna; Podbieliki, Gert René | collective |  |  |
| 70 | `SZ-SAM/B17` | Konvolut | 1 | Konvolut SZ-SAM/B17 | Meingast, Anna; Thalhuber, Johann | collective |  |  |
| 71 | `SZ-SAM/B18` | Konvolut | 3 | Konvolut SZ-SAM/B18 | Meingast, Anna; Rieger, Erwin | collective |  |  |
| 72 | `SZ-SAM/B19` | Konvolut | 1 | Konvolut SZ-SAM/B19 | Meingast, Willi; Zweig, Friderike | collective |  |  |
| 73 | `SZ-SAM/B20` | Konvolut | 1 | Konvolut SZ-SAM/B20 | Meingast, Anna; Meingast, Willi | collective |  |  |
| 74 | `SZ-SAM/L` | Einzelstücke | 1 | Einzelstücke SZ-SAM | — |  |  |  |
| 75 | `SZ-SDP/L` | Einzelstücke | 1 | Einzelstücke SZ-SDP | — |  |  |  |
| 76 | `SZ-SEF/B1` | Konvolut | 1 | Konvolut SZ-SEF/B1 | Berger, Gisela von |  |  |  |
| 77 | `SZ-SEF/B2` | Konvolut | 1 | Konvolut SZ-SEF/B2 | Feld, Leo |  |  |  |
| 78 | `SZ-SEF/B3` | Konvolut | 1 | Konvolut SZ-SEF/B3 | Fleischer, Victor |  |  |  |
| 79 | `SZ-SEF/B4` | Konvolut | 2 | Konvolut SZ-SEF/B4 | Glücksmann, Heinrich |  |  |  |
| 80 | `SZ-SEF/B5` | Konvolut | 18 | Konvolut SZ-SEF/B5 | Hirschfeld, Eugenie |  |  |  |
| 81 | `SZ-SEF/B6` | Konvolut | 9 | Konvolut SZ-SEF/B6 | Klammer, Karl |  |  |  |
| 82 | `SZ-SEF/B7` | Konvolut | 1 | Konvolut SZ-SEF/B7 | Monath, Elisabeth |  |  |  |
| 83 | `SZ-SEF/B8` | Konvolut | 1 | Konvolut SZ-SEF/B8 | Sinaiberger, Hugo |  |  |  |
| 84 | `SZ-SEF/B9` | Konvolut | 3 | Konvolut SZ-SEF/B9 | Specht, Richard |  |  |  |
| 85 | `SZ-SEF/B10` | Konvolut | 1 | Konvolut SZ-SEF/B10 | Zweig, Alfred |  |  |  |
| 86 | `SZ-SEF/B11` | Konvolut | 1 | Konvolut SZ-SEF/B11 | Zweig, Friderike |  |  |  |
| 87 | `SZ-SEF/B12` | Konvolut | 2 | Konvolut SZ-SEF/B12 | Zweig, Ida |  |  |  |
| 88 | `SZ-SEF/B13` | Konvolut | 1 | Konvolut SZ-SEF/B13 | Csokor, Franz Theodor |  |  |  |
| 89 | `SZ-SEF/B14` | Konvolut | 1 | Konvolut SZ-SEF/B14 | Weisse, Adolf |  |  |  |
| 90 | `SZ-SEF/B15` | Konvolut | 1 | Konvolut SZ-SEF/B15 | Glücksmann, Heinrich |  |  |  |
| 91 | `SZ-SEF/L` | Einzelstücke | 6 | Einzelstücke SZ-SEF | Zweig, Alfred |  |  |  |
| 92 | `SZ-SHB/B1` | Konvolut | 1 | Konvolut SZ-SHB/B1 | Bahr, Hermann |  |  |  |
| 93 | `SZ-SHB/B2` | Konvolut | 7 | Konvolut SZ-SHB/B2 | Kaemmerer, Ami |  |  |  |
| 94 | `SZ-SHB/B3` | Konvolut | 5 | Konvolut SZ-SHB/B3 | Kaemmerer, Ami; Kaemmerer, Erich Ami | collective |  |  |
| 95 | `SZ-SHB/B4` | Konvolut | 3 | Konvolut SZ-SHB/B4 | Kaemmerer, Maria |  |  |  |
| 96 | `SZ-SHB/B5` | Konvolut | 3 | Konvolut SZ-SHB/B5 | Jeanrenaud, [unbekannt] |  |  |  |
| 97 | `SZ-SHB/B6` | Konvolut | 2 | Konvolut SZ-SHB/B6 | Möller, Rudolf |  |  |  |
| 98 | `SZ-SHB/B7` | Konvolut | 1 | Konvolut SZ-SHB/B7 | Oppeln-Bronikowski, Friedrich von |  |  |  |
| 99 | `SZ-SHB/B8` | Konvolut | 1 | Konvolut SZ-SHB/B8 | Unbekannt |  |  |  |
