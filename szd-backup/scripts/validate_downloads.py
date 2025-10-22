#!/usr/bin/env python3
"""
Validation script for Stefan Zweig Digital archive downloads.
Checks completeness and integrity of downloaded data.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET

# Configuration
DATA_DIR = Path("data")
CONTAINER_FOLDERS = {
    "szd.facsimiles": "facsimiles",
    "szd.facsimiles.aufsatz": "aufsatz",
    "szd.facsimiles.lebensdokumente": "lebensdokumente",
    "szd.facsimiles.korrespondenzen": "korrespondenzen"
}

class ValidationResult:
    """Store validation results for an object."""

    def __init__(self, object_id: str):
        self.object_id = object_id
        self.has_mets = False
        self.has_metadata_json = False
        self.expected_images = 0
        self.found_images = 0
        self.missing_images = []
        self.extra_images = []
        self.errors = []

    @property
    def is_complete(self) -> bool:
        """Check if object is complete."""
        return (self.has_mets and
                self.has_metadata_json and
                self.expected_images == self.found_images and
                len(self.missing_images) == 0 and
                len(self.errors) == 0)

    def add_error(self, error: str):
        """Add an error message."""
        self.errors.append(error)

def validate_object(object_folder: Path) -> ValidationResult:
    """Validate a single object's downloaded data."""

    object_id = object_folder.name.replace("_", ":")
    result = ValidationResult(object_id)

    # Check METS file
    mets_file = object_folder / "mets.xml"
    if not mets_file.exists():
        result.add_error("METS file missing")
        return result
    result.has_mets = True

    # Check metadata.json
    metadata_file = object_folder / "metadata.json"
    if not metadata_file.exists():
        result.add_error("metadata.json missing")
        return result
    result.has_metadata_json = True

    # Parse METS to get expected images
    try:
        tree = ET.parse(mets_file)
        root = tree.getroot()
        ns = {'mets': 'http://www.loc.gov/METS/'}

        expected_image_ids = set()
        for file_elem in root.findall('.//mets:file[@MIMETYPE="image/jpeg"]', ns):
            file_id = file_elem.get('ID')
            if file_id and file_id.startswith('IMG.'):
                expected_image_ids.add(file_id)

        result.expected_images = len(expected_image_ids)

    except Exception as e:
        result.add_error(f"Failed to parse METS: {e}")
        return result

    # Parse metadata.json to cross-check
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        metadata_image_count = len(metadata.get('images', []))
        if metadata_image_count != result.expected_images:
            result.add_error(
                f"Image count mismatch: METS has {result.expected_images}, "
                f"metadata.json has {metadata_image_count}"
            )
    except Exception as e:
        result.add_error(f"Failed to parse metadata.json: {e}")

    # Check downloaded images
    images_folder = object_folder / "images"
    if not images_folder.exists():
        result.add_error("Images folder missing")
        return result

    # Find all downloaded images
    downloaded_images = set()
    for img_file in images_folder.glob("*.jpg"):
        # Convert filename back to METS ID format (IMG_1.jpg -> IMG.1)
        file_id = img_file.stem.replace("_", ".")
        downloaded_images.add(file_id)

    result.found_images = len(downloaded_images)

    # Find missing and extra images
    result.missing_images = sorted(expected_image_ids - downloaded_images)
    result.extra_images = sorted(downloaded_images - expected_image_ids)

    # Check file sizes (warn if any image is too small)
    for img_file in images_folder.glob("*.jpg"):
        size = img_file.stat().st_size
        if size < 10000:  # Less than 10KB is suspicious
            result.add_error(f"{img_file.name} is too small ({size} bytes)")

    return result

def validate_container(container_name: str, folder_name: str) -> List[ValidationResult]:
    """Validate all objects in a container."""

    container_path = DATA_DIR / folder_name

    if not container_path.exists():
        print(f"  [SKIP] Container folder not found: {container_path}")
        return []

    results = []
    object_folders = sorted([f for f in container_path.iterdir() if f.is_dir()])

    if not object_folders:
        print(f"  [INFO] No objects found in {container_path}")
        return []

    for obj_folder in object_folders:
        result = validate_object(obj_folder)
        results.append(result)

    return results

def print_validation_summary(results: List[ValidationResult], container_name: str):
    """Print summary for a container."""

    if not results:
        return

    complete = sum(1 for r in results if r.is_complete)
    incomplete = len(results) - complete

    print(f"\n  Total objects: {len(results)}")
    print(f"  Complete: {complete}")
    print(f"  Incomplete: {incomplete}")

    # Detailed issues
    if incomplete > 0:
        print(f"\n  Issues found:")
        for result in results:
            if not result.is_complete:
                print(f"\n    {result.object_id}:")

                if not result.has_mets:
                    print(f"      - Missing METS file")
                if not result.has_metadata_json:
                    print(f"      - Missing metadata.json")

                if result.missing_images:
                    print(f"      - Missing {len(result.missing_images)} images: {', '.join(result.missing_images[:5])}")
                    if len(result.missing_images) > 5:
                        print(f"        ... and {len(result.missing_images) - 5} more")

                if result.extra_images:
                    print(f"      - Extra {len(result.extra_images)} images: {', '.join(result.extra_images[:5])}")

                if result.expected_images != result.found_images:
                    print(f"      - Image count: expected {result.expected_images}, found {result.found_images}")

                for error in result.errors:
                    print(f"      - {error}")

def main():
    """Main validation function."""

    print("=" * 70)
    print("Stefan Zweig Digital - Download Validation")
    print("=" * 70)
    print()

    all_results = {}
    total_objects = 0
    total_complete = 0
    total_images_expected = 0
    total_images_found = 0

    # Validate each container
    for container_name, folder_name in CONTAINER_FOLDERS.items():
        print(f"\n{container_name}:")
        print("-" * 70)

        results = validate_container(container_name, folder_name)
        all_results[container_name] = results

        if results:
            print_validation_summary(results, container_name)

            total_objects += len(results)
            total_complete += sum(1 for r in results if r.is_complete)
            total_images_expected += sum(r.expected_images for r in results)
            total_images_found += sum(r.found_images for r in results)

    # Overall summary
    print("\n" + "=" * 70)
    print("OVERALL SUMMARY")
    print("=" * 70)
    print(f"Total objects validated: {total_objects}")
    print(f"Complete objects: {total_complete}")
    print(f"Incomplete objects: {total_objects - total_complete}")
    print(f"Success rate: {(total_complete / total_objects * 100) if total_objects > 0 else 0:.1f}%")
    print()
    print(f"Total images expected: {total_images_expected}")
    print(f"Total images found: {total_images_found}")
    print(f"Missing images: {total_images_expected - total_images_found}")

    if total_objects == total_complete:
        print("\n[OK] All downloads are complete and valid!")
    else:
        print(f"\n[WARNING] {total_objects - total_complete} objects need attention")

    print("=" * 70)

    # Save detailed report
    report_file = Path("logs") / "validation_report.json"
    report_file.parent.mkdir(exist_ok=True)

    report_data = {}
    for container_name, results in all_results.items():
        report_data[container_name] = [
            {
                "object_id": r.object_id,
                "complete": r.is_complete,
                "has_mets": r.has_mets,
                "has_metadata_json": r.has_metadata_json,
                "expected_images": r.expected_images,
                "found_images": r.found_images,
                "missing_images": r.missing_images,
                "extra_images": r.extra_images,
                "errors": r.errors
            }
            for r in results
        ]

    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    print(f"\nDetailed report saved to: {report_file}")

if __name__ == "__main__":
    main()
