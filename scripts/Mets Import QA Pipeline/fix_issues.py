"""
Fix-Script für SZ_AAL_B2 Result-Ordner.
Behebt alle automatisch fixbaren Probleme.
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
DRY_RUN = False  # Set True to only print what would happen

def log(action, detail):
    prefix = "[DRY RUN] " if DRY_RUN else ""
    print(f"  {prefix}{action}: {detail}")


def fix_rename_and_delete_duplicates():
    """
    B2.1: Delete duplicates (keep Result_SZ_AAL_B2.1.xml)
    B2.2-5: Rename double-named XML -> standard name, delete extensionless
    """
    print("\n[1] Duplikate bereinigen & XMLs umbenennen (B2.1-B2.5)")
    print("-" * 55)

    for i in range(1, 6):
        folder = BASE_DIR / f"SZ_AAL_B2.{i}"
        standard_xml = folder / f"Result_SZ_AAL_B2.{i}.xml"
        double_xml = folder / f"Result_SZ_AAL_B2SZ_AAL_B2.{i}.xml"
        extensionless = folder / f"Result_SZ_AAL_B2.{i}"

        if i == 1:
            # B2.1: standard XML exists, delete the other two
            if double_xml.exists():
                log("LÖSCHEN", double_xml.name)
                if not DRY_RUN:
                    double_xml.unlink()
            if extensionless.exists():
                log("LÖSCHEN", extensionless.name)
                if not DRY_RUN:
                    extensionless.unlink()
        else:
            # B2.2-5: standard XML missing, rename double -> standard, delete extensionless
            if double_xml.exists() and not standard_xml.exists():
                log("UMBENENNEN", f"{double_xml.name} -> {standard_xml.name}")
                if not DRY_RUN:
                    double_xml.rename(standard_xml)
            if extensionless.exists():
                log("LÖSCHEN", extensionless.name)
                if not DRY_RUN:
                    extensionless.unlink()


def fix_remove_file_namespace():
    """B2.1-5: Remove xmlns:file namespace from XMLs."""
    print("\n[2] xmlns:file Namespace entfernen (B2.1-B2.5)")
    print("-" * 55)

    for i in range(1, 6):
        folder = BASE_DIR / f"SZ_AAL_B2.{i}"
        xml_path = folder / f"Result_SZ_AAL_B2.{i}.xml"

        if not xml_path.exists():
            print(f"  WARNUNG: {xml_path.name} nicht gefunden!")
            continue

        content = xml_path.read_text(encoding="utf-8")
        # Remove the xmlns:file declaration (with optional surrounding whitespace)
        new_content = re.sub(
            r'\s+xmlns:file="http://expath\.org/ns/file"', "", content
        )

        if content != new_content:
            log("NAMESPACE ENTFERNT", xml_path.name)
            if not DRY_RUN:
                xml_path.write_text(new_content, encoding="utf-8")
        else:
            log("KEIN CHANGE", xml_path.name)


def fix_div_type_b2_14():
    """B2.14: Farbreferenzen -> Farbreferenz"""
    print("\n[3] div-Typ korrigieren: B2.14 Farbreferenzen -> Farbreferenz")
    print("-" * 55)

    xml_path = BASE_DIR / "SZ_AAL_B2.14" / "Result_SZ_AAL_B2.14.xml"
    content = xml_path.read_text(encoding="utf-8")
    new_content = content.replace('type="Farbreferenzen"', 'type="Farbreferenz"')

    if content != new_content:
        log("GEÄNDERT", 'Farbreferenzen -> Farbreferenz')
        if not DRY_RUN:
            xml_path.write_text(new_content, encoding="utf-8")


def fix_div_types_b2_50():
    """B2.50: Textseite -> Textseiten, Adressseite -> Adressseiten"""
    print("\n[4] div-Typen korrigieren: B2.50 Singular -> Plural")
    print("-" * 55)

    xml_path = BASE_DIR / "SZ_AAL_B2.50" / "Result_SZ_AAL_B2.50.xml"
    content = xml_path.read_text(encoding="utf-8")
    new_content = content.replace('type="Textseite"', 'type="Textseiten"')
    new_content = new_content.replace('type="Adressseite"', 'type="Adressseiten"')

    if content != new_content:
        log("GEÄNDERT", 'Textseite -> Textseiten, Adressseite -> Adressseiten')
        if not DRY_RUN:
            xml_path.write_text(new_content, encoding="utf-8")


def main():
    print("=" * 55)
    print("SZ_AAL_B2 Fix-Script")
    print("=" * 55)
    if DRY_RUN:
        print(">>> DRY RUN - keine Änderungen werden geschrieben <<<")

    fix_rename_and_delete_duplicates()
    fix_remove_file_namespace()
    fix_div_type_b2_14()
    fix_div_types_b2_50()

    print("\n" + "=" * 55)
    print("FERTIG. Bitte validate_results.py erneut ausführen.")
    print("=" * 55)


if __name__ == "__main__":
    main()
