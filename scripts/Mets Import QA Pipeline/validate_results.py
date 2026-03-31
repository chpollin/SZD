"""
Validierungsscript für SZ_AAL_B2 Result-Ordner.
Prüft XML-Wohlgeformtheit, Bild-Referenzen, Namenskonventionen,
Vollständigkeit und Konsistenz.
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent
EXPECTED_RANGE = range(1, 51)  # B2.1 bis B2.50
NS = {"v": "http://gams.uni-graz.at/viewer", "xlink": "http://www.w3.org/1999/xlink"}

# Regex patterns
RE_FOLDER_NAME = re.compile(r"SZ_AAL_B2\.(\d+)$")
RE_DOUBLE_XML = re.compile(r"Result_SZ_AAL_B2SZ_AAL_B2\.\d+\.xml$")

# Issue category constants
ISSUE_CAT = {
    "missing_folders": "Fehlende Ordner",
    "unexpected_folders": "Unerwartete Ordner",
    "no_extension": "Dateien ohne Endung",
    "double_xml": "Doppelt benannte XMLs",
    "unexpected_types": "Unerwartete Dateitypen",
    "missing_standard_xml": "Fehlende Standard-XML",
    "missing_xml": "Fehlende XML",
    "xml_parse": "XML Parse-Fehler",
    "ns_inconsistency": "Namespace-Inkonsistenz",
    "missing_metadata": "Fehlende/leere Metadaten",
    "metadata_inconsistency": "Metadaten-Inkonsistenz",
    "missing_structure": "Fehlende Struktur",
    "unexpected_structure": "Unerwartete Struktur",
    "missing_images": "Fehlende Bilder (XML referenziert, Datei fehlt)",
    "orphan_images": "Verwaiste Bilder (Datei vorhanden, nicht in XML)",
    "image_naming": "Namenskonvention Bilder",
    "image_gaps": "Lücken in Bildnummerierung",
    "empty_images": "Leere Bilddateien",
}

# Collect all issues
issues = defaultdict(list)  # category -> list of issue strings
stats = {
    "folders_checked": 0,
    "xmls_valid": 0,
    "xmls_invalid": 0,
    "total_images": 0,
    "total_referenced_images": 0,
}


def check_folder_completeness():
    """1. Prüfe ob alle Ordner B2.1 bis B2.50 vorhanden sind."""
    existing = set()
    for d in BASE_DIR.iterdir():
        if d.is_dir():
            m = RE_FOLDER_NAME.match(d.name)
            if m:
                existing.add(int(m.group(1)))

    for i in EXPECTED_RANGE:
        if i not in existing:
            issues[ISSUE_CAT["missing_folders"]].append(f"SZ_AAL_B2.{i} fehlt")

    # Check for unexpected folders
    for d in BASE_DIR.iterdir():
        if d.is_dir() and not RE_FOLDER_NAME.match(d.name):
            issues[ISSUE_CAT["unexpected_folders"]].append(f"Unerwarteter Ordner: {d.name}")

    return existing


def check_unexpected_files(folder_path, folder_name, num):
    """6. Prüfe auf unerwartete Dateien (ohne Endung, doppelte XMLs etc.)."""
    expected_xml = f"Result_{folder_name}.xml"

    for f in folder_path.iterdir():
        if f.is_file():
            # Files without extension
            if not f.suffix:
                issues[ISSUE_CAT["no_extension"]].append(
                    f"{folder_name}/{f.name} - Datei ohne Dateiendung"
                )
            # Double-named XMLs
            elif RE_DOUBLE_XML.match(f.name):
                issues[ISSUE_CAT["double_xml"]].append(
                    f"{folder_name}/{f.name} - fehlerhafter Dateiname (doppeltes Präfix)"
                )
            # Unexpected file types
            elif f.suffix.lower() not in (".xml", ".jpg", ".jpeg"):
                issues[ISSUE_CAT["unexpected_types"]].append(
                    f"{folder_name}/{f.name} - unerwarteter Dateityp '{f.suffix}'"
                )


def check_xml(folder_path, folder_name, num):
    """1-2, 9-10, 12. XML-Validierung: Wohlgeformtheit, Schema, Struktur, Namespaces, Metadaten."""
    xml_file = folder_path / f"Result_{folder_name}.xml"

    if not xml_file.exists():
        # Try alternate naming
        alt_xml = folder_path / f"Result_SZ_AAL_B2SZ_AAL_B2.{num}.xml"
        if alt_xml.exists():
            issues[ISSUE_CAT["missing_standard_xml"]].append(
                f"{folder_name}: Result_{folder_name}.xml fehlt, "
                f"nur {alt_xml.name} vorhanden"
            )
            xml_file = alt_xml
        else:
            issues[ISSUE_CAT["missing_xml"]].append(f"{folder_name}: Keine XML-Datei gefunden")
            stats["xmls_invalid"] += 1
            return None

    # 1. XML well-formedness
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        stats["xmls_valid"] += 1
    except ET.ParseError as e:
        issues[ISSUE_CAT["xml_parse"]].append(f"{folder_name}: {e}")
        stats["xmls_invalid"] += 1
        return None

    # 10. Namespace consistency - check raw file for extra namespaces
    with open(xml_file, "r", encoding="utf-8") as f:
        raw = f.read()
    if "xmlns:file=" in raw:
        issues[ISSUE_CAT["ns_inconsistency"]].append(
            f"{folder_name}: Enthält extra Namespace xmlns:file (nicht in allen XMLs vorhanden)"
        )

    # 2 & 12. Required elements
    tag_prefix = "{http://gams.uni-graz.at/viewer}"

    title_el = root.find(f"{tag_prefix}title")
    if title_el is None or not (title_el.text and title_el.text.strip()):
        issues[ISSUE_CAT["missing_metadata"]].append(f"{folder_name}: <title> fehlt oder leer")
    else:
        # Check title contains correct reference
        if f"B2.{num}" not in title_el.text:
            issues[ISSUE_CAT["metadata_inconsistency"]].append(
                f"{folder_name}: <title> enthält nicht 'B2.{num}': '{title_el.text}'"
            )

    author_el = root.find(f"{tag_prefix}author")
    if author_el is None or not (author_el.text and author_el.text.strip()):
        issues[ISSUE_CAT["missing_metadata"]].append(f"{folder_name}: <author> fehlt oder leer")

    date_el = root.find(f"{tag_prefix}date")
    if date_el is None or not (date_el.text and date_el.text.strip()):
        issues[ISSUE_CAT["missing_metadata"]].append(f"{folder_name}: <date> fehlt oder leer")

    owner_el = root.find(f"{tag_prefix}owner/{tag_prefix}name")
    if owner_el is None or not (owner_el.text and owner_el.text.strip()):
        issues[ISSUE_CAT["missing_metadata"]].append(f"{folder_name}: <owner><name> fehlt oder leer")

    # 9. Structure check - Textseiten and Farbreferenz
    structure_el = root.find(f"{tag_prefix}structure")
    if structure_el is None:
        issues["Fehlende Struktur"].append(f"{folder_name}: <structure> fehlt")
        return None

    divs = structure_el.findall(f"{tag_prefix}div")
    div_types = [d.get("type") for d in divs]

    if "Textseiten" not in div_types:
        issues[ISSUE_CAT["missing_structure"]].append(f"{folder_name}: <div type='Textseiten'> fehlt")
    if "Farbreferenz" not in div_types:
        issues[ISSUE_CAT["missing_structure"]].append(f"{folder_name}: <div type='Farbreferenz'> fehlt")

    # Unexpected div types
    for dt in div_types:
        if dt not in ("Textseiten", "Farbreferenz"):
            issues[ISSUE_CAT["unexpected_structure"]].append(
                f"{folder_name}: Unerwarteter div-Typ '{dt}'"
            )

    # Collect all referenced images
    referenced_images = []
    for page in root.iter(f"{tag_prefix}page"):
        href = page.get(f"{{{NS['xlink']}}}href")
        if href:
            referenced_images.append(href)

    return referenced_images


def check_image_references(folder_path, folder_name, num, referenced_images):
    """3-4, 7, 11. Bild-Referenzen, verwaiste Bilder, Nummerierung, Integrität."""
    if referenced_images is None:
        return

    # Get actual JPG files
    actual_jpgs = {f.name for f in folder_path.iterdir() if f.suffix.lower() in (".jpg", ".jpeg")}
    referenced_set = set(referenced_images)

    stats["total_images"] += len(actual_jpgs)
    stats["total_referenced_images"] += len(referenced_set)

    # 3. Referenced images that don't exist
    for ref in referenced_images:
        if ref not in actual_jpgs:
            issues[ISSUE_CAT["missing_images"]].append(
                f"{folder_name}: {ref} in XML referenziert, aber Datei fehlt"
            )

    # 4. Orphan images (exist but not referenced)
    for jpg in sorted(actual_jpgs):
        if jpg not in referenced_set:
            issues[ISSUE_CAT["orphan_images"]].append(
                f"{folder_name}: {jpg} existiert, ist aber nicht in XML referenziert"
            )

    # 5. Naming convention for images
    for jpg in sorted(actual_jpgs):
        expected_pattern = rf"^SZ_AAL_B2\.{num}_\d{{3}}\.jpg$"
        if not re.match(expected_pattern, jpg):
            issues[ISSUE_CAT["image_naming"]].append(
                f"{folder_name}: {jpg} entspricht nicht dem Schema SZ_AAL_B2.{num}_NNN.jpg"
            )

    # 7. Sequential numbering
    numbers = []
    for jpg in actual_jpgs:
        m = re.match(rf"SZ_AAL_B2\.{num}_(\d{{3}})\.jpg$", jpg)
        if m:
            numbers.append(int(m.group(1)))

    if numbers:
        numbers.sort()
        expected = list(range(1, max(numbers) + 1))
        if numbers != expected:
            missing = set(expected) - set(numbers)
            if missing:
                issues[ISSUE_CAT["image_gaps"]].append(
                    f"{folder_name}: Fehlende Nummern: {sorted(missing)}"
                )

    # 11. Image integrity (file size > 0)
    for jpg in sorted(actual_jpgs):
        jpg_path = folder_path / jpg
        if jpg_path.stat().st_size == 0:
            issues[ISSUE_CAT["empty_images"]].append(
                f"{folder_name}: {jpg} ist leer (0 Bytes)"
            )


def main():
    print("=" * 70)
    print("SZ_AAL_B2 Result-Validierung")
    print("=" * 70)
    print(f"Basisverzeichnis: {BASE_DIR}\n")

    # 8. Check folder completeness
    existing_nums = check_folder_completeness()
    stats["folders_checked"] = len(existing_nums)

    # Process each folder
    for num in sorted(existing_nums):
        folder_name = f"SZ_AAL_B2.{num}"
        folder_path = BASE_DIR / folder_name

        # 6. Unexpected files
        check_unexpected_files(folder_path, folder_name, num)

        # 1, 2, 9, 10, 12. XML checks
        referenced_images = check_xml(folder_path, folder_name, num)

        # 3, 4, 5, 7, 11. Image checks
        check_image_references(folder_path, folder_name, num, referenced_images)

    # Print results
    print("STATISTIK")
    print("-" * 70)
    print(f"  Ordner geprüft:       {stats['folders_checked']}")
    print(f"  XML valide:           {stats['xmls_valid']}")
    print(f"  XML invalide:         {stats['xmls_invalid']}")
    print(f"  Bilder gesamt:        {stats['total_images']}")
    print(f"  Bilder referenziert:  {stats['total_referenced_images']}")
    print()

    if not issues:
        print("ERGEBNIS: Keine Probleme gefunden!")
        return

    total_issues = sum(len(v) for v in issues.values())
    print(f"ERGEBNIS: {total_issues} Probleme in {len(issues)} Kategorien gefunden")
    print("=" * 70)

    for category, items in sorted(issues.items()):
        print(f"\n[{category}] ({len(items)} Probleme)")
        print("-" * 50)
        for item in items:
            print(f"  - {item}")

    print("\n" + "=" * 70)
    print("ZUSAMMENFASSUNG")
    print("=" * 70)
    for category, items in sorted(issues.items()):
        print(f"  {category}: {len(items)}")


if __name__ == "__main__":
    main()
