# tei_csv_mapping.py  –  final, duplicate-free version
from collections import OrderedDict
from typing import List, Tuple

# MAPPING[column name] -> [(xpath, attribute|None, xml:lang|None), …]
MAPPING: "OrderedDict[str, List[Tuple[str, str | None, str | None]]]" = OrderedDict({

    # Identification ─────────────────────────────────────────────────────────
    "PID": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/"
         "tei:altIdentifier/tei:idno[@type='PID']", None, None)
    ],
    "Context": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/"
         "tei:altIdentifier/tei:idno[@type='context']", None, None)
    ],

    # Agents — sender (sent) ────────────────────────────────────────────────
    "Verfasser*in": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:persName", None, None)
    ],
    "Verfasser*in GND": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:persName", "ref", None)
    ],
    "Körperschaft Verfasser*in": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:orgName", None, None)
    ],
    "Körperschaft Verfasser*in GND": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:orgName", "ref", None)
    ],

    # Agents — receiver (received) ──────────────────────────────────────────
    "Adressat*in": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/"
         "tei:persName", None, None)
    ],
    "Adressat*in GND": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/"
         "tei:persName", "ref", None)
    ],
    "Körperschaft Adressat*in": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/"
         "tei:orgName", None, None)
    ],
    "Körperschaft Adressat*in GND": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/"
         "tei:orgName", "ref", None)
    ],

    # Physical description — extent & enclosures ────────────────────────────
    "Art/Umfang": [                         # de ; en  (two mapping rules)
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/"
         "tei:supportDesc/tei:extent/tei:span", None, "de"),
    ],
    "Physical Description": [                         # de ; en  (two mapping rules)
                ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/"
         "tei:supportDesc/tei:extent/tei:span", None, "en"),
    ],
    "Beilagen": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/"
         "tei:supportDesc/tei:extent/tei:measure[@ana='szdg:Enclosures']",
         None, "de")
    ],
    "Enclosures": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/"
         "tei:supportDesc/tei:extent/tei:measure[@ana='szdg:Enclosures']",
         None, "en")
    ],

    # Dates ─────────────────────────────────────────────────────────────────
    "Datierung Original": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:date", None, "de")
    ],
    "Date original": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:date", None, "en")
    ],
    "Datierung erschlossen": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:date[@type='supplied']", None, "de")
    ],
    "Date supplied/verified": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:date[@type='supplied']", None, "en")
    ],
    "Datierung normalisiert": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date",
         "when", None)
    ],

    # Places & addresses ────────────────────────────────────────────────────
    "Poststempel": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:placeName[@type='postmark']", None, None)
    ],
    "Entstehungsort Original": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:placeName[not(@ana='deduced')]",
         None, "de")
    ],
"Entstehungsort erschlossen": [
    ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
     "tei:placeName[@ana='deduced']",
     None, "de") 
    ],
    "Postanschrift (original)": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:address/tei:addrLine", None, "de")
    ],
    "Postanschrift normalisiert": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:address/tei:addrLine", None, None)
    ],

    # Language of the letter ───────────────────────────────────────────────
    "Sprache": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:textLang/tei:lang",
         "xml:lang", None)
    ],
    # English standalone columns
    "Writing Material": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/"
         "tei:supportDesc/tei:support/tei:material[@ana='szdg:WritingMaterial']",
         None, "en")
    ],
    "Writing Instrument": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/"
         "tei:supportDesc/tei:support/tei:material[@ana='szdg:WritingInstrument']",
         None, "en")
    ],
    # Materials & writing support/instrument ───────────────────────────────
    "Beschreibstoff": [                     # de ; en
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/"
         "tei:supportDesc/tei:support/tei:material[@ana='szdg:WritingMaterial']",
         None, "de"),
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/"
         "tei:supportDesc/tei:support/tei:material[@ana='szdg:WritingMaterial']",
         None, "en"),
    ],
    "Schreibstoff": [                       # de ; en
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/"
         "tei:supportDesc/tei:support/tei:material[@ana='szdg:WritingInstrument']",
         None, "de"),
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/"
         "tei:supportDesc/tei:support/tei:material[@ana='szdg:WritingInstrument']",
         None, "en"),
    ],
    "Maße": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:physDesc/tei:objectDesc/"
         "tei:supportDesc/tei:extent/tei:measure[@type='format']", None, None)
    ],

    # Repository & signature ───────────────────────────────────────────────
    "Standort GND": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:repository",
         "ref", None)
    ],
    "Signatur": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/"
         "tei:idno[@type='signature']", None, None)
    ],

    # History & provenance ────────────────────────────────────────────────
    "Provenienz": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:history/tei:provenance/tei:ab",
         None, "")
    ],
    "Erwerbung": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:history/tei:acquisition/tei:ab",
         None, "de")
    ],
    "Acquired": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:history/tei:acquisition/tei:ab",
         None, "en")
    ],

    # Notes & participants ────────────────────────────────────────────────
    "Beteiligte": [
        ("./tei:fileDesc/tei:notesStmt/tei:note[@type='participants']",
         None, "de")
    ],
    "Beteiligte (GND)": [
        ("./tei:fileDesc/tei:notesStmt/tei:note[@type='participants']/tei:name",
         "ref", None)
    ],
    "Hinweis": [
        ("./tei:fileDesc/tei:notesStmt/tei:note[@type='hint']", None, "de")
    ],
    "Note(s)": [
        ("./tei:fileDesc/tei:notesStmt/tei:note[@type='hint']", None, "en")
    ],
})
