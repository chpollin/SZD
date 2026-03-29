# Stefan Zweig Digital Nachlass-Ontologie (SZDO)

Formale OWL-Ontologie für den digitalen Nachlass Stefan Zweigs.

**Namespace:** `https://gams.uni-graz.at/o:szd.ontology#` (Prefix: `szdo:`)
**Version:** 1.1.0 (Nachfolger der impliziten GAMS v0.x)
**Lizenz:** CC-BY 4.0
**Live-Dokumentation:** https://chpollin.github.io/SZD/ontology/

## Versionierung

| Version | Ort | Status |
|---------|-----|--------|
| v0.x | GAMS (stefanzweig.digital) | Produktiv, 14 Klassen, 67 Properties (englisch) |
| **v1.0.0** | GitHub Pages + dieses Repo | Formalisiert, 58+14 Klassen, 77+53 Properties (deutsch + GAMS-Kompatibilitätsschicht) |
| **v1.1.0** | GitHub Pages + dieses Repo | Datum-Evidenz, Personen-Rollenhierarchie, RiC-Alignments, Klawiter-Korrekturen; 58+14 Klassen, 79+53 Properties |

Die Kompatibilitätsschicht (PART 10 in `szd-ontology.ttl`) definiert alle alten englischen GAMS-Bezeichner als `owl:deprecated` mit `owl:equivalentClass`/`owl:equivalentProperty`-Mapping auf die neuen deutschen v1.0.0-Bezeichner.

## Dateien

| Datei | Beschreibung |
|-------|-------------|
| `szd-ontology.ttl` | Kern-Ontologie in Turtle (1.271 Triples, 72 Klassen, 132 Properties inkl. GAMS-Kompatibilität) |
| `szd-shapes.ttl` | SHACL Shapes für Strukturvalidierung (deprecated Entitäten ausgenommen) |
| `validate.py` | 6-Stufen-Validierungspipeline (Syntax, SHACL, OWL, OntoClean, Kompetenzfragen) |
| `generate_docs.py` | Generiert HTML-Dokumentation aus der Ontologie nach `../docs/ontology/` |

## Grundlagen

Die Ontologie basiert auf drei etablierten Standards:

- **Records in Context (RiC-O)** — Archivische Modellierung (Nachlass → Sammlung → Objekt → Digitales Objekt)
- **IFLA Library Reference Model (LRM)** — Werkmodellierung (Werk → Expression → Manifestation → Exemplar)
- **CIDOC Conceptual Reference Model (CRM)** — Ereignisse, Provenienz, Biographie

## Verwendung

```bash
# Ontologie validieren (0 Fehler = grün)
python ontology/validate.py

# HTML-Dokumentation generieren
python ontology/generate_docs.py

# Lokal anschauen
python -m http.server -d docs 8000
# → http://localhost:8000/ontology/
```

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

- **Ausführliches Design-Dokument:** [../knowledge/ONTOLOGY.md](../knowledge/ONTOLOGY.md) (Designprinzipien, Alignments, Kompetenzfragen, Migrationsstrategie)
- **Live-Dokumentation:** https://chpollin.github.io/SZD/ontology/ (generiert aus `szd-ontology.ttl`)
