# Stefan Zweig Digital Nachlass-Ontologie (SZDO)

Formale OWL-Ontologie für den digitalen Nachlass Stefan Zweigs.

**Namespace:** `https://gams.uni-graz.at/o:szd.ontology#` (Prefix: `szdo:`)
**Version:** 0.1.0
**Lizenz:** CC-BY 4.0

## Dateien

| Datei | Beschreibung |
|-------|-------------|
| `szd-ontology.ttl` | Kern-Ontologie in Turtle-Serialisierung |

## Grundlagen

Die Ontologie basiert auf drei etablierten Standards:

- **Records in Context (RiC-O)** — Archivische Modellierung (Nachlass → Sammlung → Objekt → Digitales Objekt)
- **IFLA Library Reference Model (LRM)** — Werkmodellierung (Werk → Expression → Manifestation → Exemplar)
- **CIDOC Conceptual Reference Model (CRM)** — Ereignisse, Provenienz, Biographie

## Klassenübersicht

```
szdo:Nachlass (Fonds)
├── szdo:Sammlung (Werksammlung, Korrespondenz, Autographen, Bibliothek, ...)
│   └── szdo:NachlassObjekt (Manuskript, Typoskript, Buch, Autograph, ...)
│       └── szdo:DigitalesObjekt (METS, IIIF, Faksimile)
│
szdo:Werk (Werkindex SZDWRK)
├── szdo:WerkExpression (Übersetzung, Adaption)
├── szdo:Manifestation (publizierte Ausgabe → Klawiter)
└── szdo:Sekundaerliteratur (→ Klawiter)
│
szdo:Person / szdo:Organisation (Akteure, SZDPER/SZDSTA)
szdo:BiographischesEreignis (Lebenskalender SZDBIO)
szdo:Ort (Geographisch, Aufbewahrung, Entstehung)
szdo:Provenienzereignis / szdo:ProvenienzmerkmalInstanz
```

## Dokumentation

Ausführliche Dokumentation im Knowledge-Ordner: [../knowledge/ONTOLOGY.md](../knowledge/ONTOLOGY.md)
