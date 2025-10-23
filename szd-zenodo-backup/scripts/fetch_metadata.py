#!/usr/bin/env python3
"""
Script to download metadata XML files from GAMS archive containers.
Downloads all object metadata for szd.facsimiles and its sub-containers.
"""

import requests
import time
import os
from pathlib import Path
import xml.etree.ElementTree as ET

# Configuration
BASE_URL = "https://gams.uni-graz.at/archive/objects/{container}/methods/sdef:Object/getMetadata"
OUTPUT_DIR = Path("metadata")
DELAY_SECONDS = 1  # Delay between requests to be server-friendly

# Containers to download
CONTAINERS = [
    "context:szd.facsimiles",
    "context:szd.facsimiles.aufsatz",
    "context:szd.facsimiles.lebensdokumente",
    "context:szd.facsimiles.korrespondenzen"
]

def download_metadata(container: str, output_dir: Path) -> bool:
    """
    Download metadata XML for a given container.

    Args:
        container: Container ID (e.g., "context:szd.facsimiles")
        output_dir: Directory to save the XML file

    Returns:
        True if successful, False otherwise
    """
    url = BASE_URL.format(container=container)

    # Create safe filename from container name
    filename = container.replace(":", "_").replace(".", "_") + ".xml"
    filepath = output_dir / filename

    print(f"Downloading: {container}")
    print(f"  URL: {url}")

    try:
        # Follow redirects automatically
        response = requests.get(url, allow_redirects=True, timeout=30)
        response.raise_for_status()

        # Save the XML content
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"  [OK] Saved to: {filepath}")
        print(f"  Size: {len(response.content)} bytes")

        return True

    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Error: {e}")
        return False

def parse_object_ids(xml_file: Path) -> list:
    """
    Parse object IDs (PIDs) from a metadata XML file.

    Args:
        xml_file: Path to the XML file

    Returns:
        List of object IDs (e.g., ['o:szd.199', 'o:szd.200', ...])
    """
    print(f"\nParsing: {xml_file.name}")

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Define namespace
        ns = {'sparql': 'http://www.w3.org/2001/sw/DataAccess/rf1/result'}

        # Find all <pid> elements
        pids = []
        for pid_elem in root.findall('.//sparql:pid', ns):
            uri = pid_elem.get('uri')
            if uri and 'o:szd.' in uri:
                # Extract o:szd.XXX from info:fedora/o:szd.XXX
                object_id = uri.split('/')[-1]
                pids.append(object_id)

        print(f"  Found {len(pids)} objects")
        return pids

    except Exception as e:
        print(f"  [ERROR] Error parsing: {e}")
        return []

def main():
    """Main function to download all metadata and extract object IDs."""

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR.absolute()}\n")

    # Download metadata for all containers
    print("=" * 60)
    print("STEP 1: Downloading metadata XML files")
    print("=" * 60)

    success_count = 0
    for container in CONTAINERS:
        if download_metadata(container, OUTPUT_DIR):
            success_count += 1

        # Be nice to the server
        if container != CONTAINERS[-1]:  # Don't delay after last request
            time.sleep(DELAY_SECONDS)
        print()

    print(f"Downloaded {success_count}/{len(CONTAINERS)} metadata files\n")

    # Parse all downloaded XML files to extract object IDs
    print("=" * 60)
    print("STEP 2: Extracting object IDs from XML files")
    print("=" * 60)

    all_objects = {}
    for container in CONTAINERS:
        filename = container.replace(":", "_").replace(".", "_") + ".xml"
        filepath = OUTPUT_DIR / filename

        if filepath.exists():
            pids = parse_object_ids(filepath)
            container_name = container.split(":")[-1]
            all_objects[container_name] = pids

    # Save object IDs to a summary file
    summary_file = OUTPUT_DIR / "object_ids_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("Stefan Zweig Digital - Object IDs Summary\n")
        f.write("=" * 60 + "\n\n")

        total_objects = 0
        for container, pids in all_objects.items():
            f.write(f"{container}:\n")
            f.write(f"  Total: {len(pids)} objects\n")
            f.write(f"  IDs: {', '.join(sorted(pids))}\n\n")
            total_objects += len(pids)

        f.write(f"\nTotal objects across all containers: {total_objects}\n")

    print(f"\n[OK] Summary saved to: {summary_file}")

    # Print summary to console
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for container, pids in all_objects.items():
        print(f"{container}: {len(pids)} objects")
    print(f"\nTotal: {sum(len(pids) for pids in all_objects.values())} objects")

if __name__ == "__main__":
    main()
