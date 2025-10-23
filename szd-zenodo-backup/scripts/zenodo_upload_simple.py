#!/usr/bin/env python3
"""
Simple Zenodo Upload Script for Stefan Zweig Digital Archive v1.0.0

Creates ONE complete archive and uploads it to Zenodo.

Usage:
    # Test on Sandbox
    python zenodo_upload_simple.py --sandbox --token YOUR_SANDBOX_TOKEN

    # Upload to Production
    python zenodo_upload_simple.py --token YOUR_PRODUCTION_TOKEN --publish
"""

import argparse
import json
import os
import sys
import tarfile
from pathlib import Path
import requests
from tqdm import tqdm

# ============================================================================
# CONFIGURATION
# ============================================================================

ZENODO_PRODUCTION_URL = "https://zenodo.org/api"
ZENODO_SANDBOX_URL = "https://sandbox.zenodo.org/api"

ARCHIVE_NAME = "stefan-zweig-digital-v1.0.0.tar.gz"
VERSION = "1.0.0"
PUBLICATION_DATE = "2025-10-22"

# ============================================================================
# ZENODO METADATA
# ============================================================================

METADATA = {
    "title": "Stefan Zweig Digital - Complete Archive Backup (v1.0.0)",
    "upload_type": "dataset",
    "description": """<p><strong>Complete backup of the Stefan Zweig Digital collection from GAMS</strong></p>

<p>This dataset contains a complete backup of the Stefan Zweig Digital collection from GAMS (Geisteswissenschaftliches Asset Management System, University of Graz). The collection includes manuscripts, correspondence, essays, and biographical documents from the Austrian writer Stefan Zweig (1881-1942).</p>

<h3>Contents</h3>
<ul>
<li><strong>2,107 digitized objects</strong> across four collections</li>
<li><strong>18,719 high-resolution images</strong> (JPEG, ~4912x7360 pixels)</li>
<li><strong>24.7 GB</strong> total data volume</li>
<li>Complete METS/MODS metadata (DFG-METS standard)</li>
<li>Parsed JSON metadata for easy access</li>
</ul>

<h3>Collections</h3>
<ul>
<li><strong>Facsimiles</strong>: 169 objects (161 complete, 95.3%)</li>
<li><strong>Essays (Aufsatz)</strong>: 625 objects (619 complete, 99.0%)</li>
<li><strong>Life Documents (Lebensdokumente)</strong>: 127 objects (123 complete, 96.9%)</li>
<li><strong>Correspondence (Korrespondenzen)</strong>: 1,186 objects (1,182 complete, 99.7%)</li>
</ul>

<h3>Known Limitations</h3>
<p><strong>22 objects (1.0%) are incomplete</strong> due to server-side metadata issues. 729 images (3.7%) referenced in METS files do not exist on the source server. See included <code>DATA_QUALITY_ISSUES.md</code> for detailed information.</p>

<p><strong>Most affected objects:</strong></p>
<ul>
<li>o:szd.939: 328 missing images</li>
<li>o:szd.268: 230 missing images</li>
<li>o:szd.267: 125 missing images</li>
</ul>

<p><em>Important: These missing images are due to source data problems, not download errors. All available images have been successfully archived.</em></p>

<h3>Source Information</h3>
<ul>
<li><strong>Institution:</strong> Literaturarchiv Salzburg, University of Salzburg</li>
<li><strong>Platform:</strong> GAMS, University of Graz</li>
<li><strong>Website:</strong> <a href="https://stefanzweig.digital">https://stefanzweig.digital</a></li>
<li><strong>Collection URL:</strong> <a href="https://gams.uni-graz.at/context:szd">https://gams.uni-graz.at/context:szd</a></li>
<li><strong>License:</strong> CC-BY 4.0 (Creative Commons Attribution)</li>
<li><strong>Archive Date:</strong> October 22, 2025</li>
<li><strong>Version:</strong> 1.0.0</li>
</ul>

<h3>Archive Structure</h3>
<pre>
stefan-zweig-digital-v1.0.0/
├── data/
│   ├── facsimiles/           (169 objects)
│   ├── aufsatz/              (625 objects)
│   ├── lebensdokumente/      (127 objects)
│   └── korrespondenzen/      (1,186 objects)
├── metadata/
│   └── container_metadata/
├── logs/
│   ├── download_progress.json
│   └── validation_report.json
├── README.md
├── DATA_QUALITY_ISSUES.md
├── CHANGELOG.md
├── CITATION.cff
└── LICENSE (CC-BY-4.0)
</pre>

<h3>Technical Details</h3>
<ul>
<li><strong>Image Format:</strong> JPEG</li>
<li><strong>Image Resolution:</strong> 4912 x 7360 pixels (typically)</li>
<li><strong>Metadata Standard:</strong> DFG-METS (Deutsche Forschungsgemeinschaft)</li>
<li><strong>Archive Format:</strong> tar.gz</li>
<li><strong>Completeness:</strong> 99.0% (based on validation)</li>
</ul>

<p>This archive ensures long-term preservation of this important cultural heritage resource.</p>
""",

    "creators": [
        {
            "name": "Zangerl, Lina Maria",
            "affiliation": "Literaturarchiv Salzburg, Paris Lodron Universität Salzburg",
            "orcid": "0000-0001-9709-3669"
        },
        {
            "name": "Glunk, Julia Rebecca",
            "affiliation": "Literaturarchiv Salzburg, Paris Lodron Universität Salzburg",
            "orcid": "0000-0001-6647-9729"
        },
        {
            "name": "Matuschek, Oliver",
            "affiliation": "Literaturarchiv Salzburg, Paris Lodron Universität Salzburg"
        },
        {
            "name": "Pollin, Christopher",
            "affiliation": "Digital Humanities Craft OG",
            "orcid": "0000-0002-4879-129X"
        }
    ],

    "keywords": [
        "Stefan Zweig",
        "Digital Humanities",
        "Literary Archive",
        "METS",
        "GAMS",
        "Cultural Heritage",
        "Manuscripts",
        "Correspondence",
        "Facsimiles",
        "Digital Preservation",
        "Austrian Literature",
        "20th Century Literature",
        "Literary Studies",
        "OECD:Literary studies"
    ],

    "access_right": "open",
    "license": "CC-BY-4.0",
    "publication_date": PUBLICATION_DATE,
    "version": VERSION,
    "language": "deu",

    "related_identifiers": [
        {
            "identifier": "https://gams.uni-graz.at/context:szd",
            "relation": "isSupplementTo"
        },
        {
            "identifier": "https://stefanzweig.digital",
            "relation": "isSupplementTo"
        },
        {
            "identifier": "https://d-nb.info/gnd/118637479",
            "relation": "references"
        },
        {
            "identifier": "https://www.wikidata.org/wiki/Q78491",
            "relation": "references"
        }
    ],

    "contributors": [
        {
            "name": "GAMS - Geisteswissenschaftliches Asset Management System",
            "affiliation": "University of Graz",
            "type": "HostingInstitution"
        },
        {
            "name": "Literaturarchiv Salzburg",
            "affiliation": "Paris Lodron Universität Salzburg",
            "type": "DataCurator"
        }
    ],

    "notes": f"Complete backup of the Stefan Zweig Digital collection. Version {VERSION}. Snapshot date: {PUBLICATION_DATE}. Completeness: 99.0% (22/2,107 objects incomplete due to source data issues). See included DATA_QUALITY_ISSUES.md for detailed information about missing images. This is an independent preservation archive.\n\nProvenance: Original materials held by Literaturarchiv Salzburg, digitized 2017-2025 and hosted on GAMS (University of Graz). This backup created 2025-10-22 via automated download and validation.\n\nTemporal coverage: 1881-1942 (Stefan Zweig's lifetime)\nGeographic location: Salzburg, Austria\n\nContact: info@stefanzweig.digital\nGND: https://d-nb.info/gnd/118637479\nWikidata: https://www.wikidata.org/wiki/Q78491"
}

# ============================================================================
# ARCHIVE CREATION
# ============================================================================

def create_complete_archive() -> Path:
    """
    Create a complete tar.gz archive with all data and documentation.

    Returns:
        Path to created archive
    """
    archive_path = Path(ARCHIVE_NAME)

    if archive_path.exists():
        print(f"\n[OK] Archive already exists: {archive_path}")
        size_gb = archive_path.stat().st_size / (1024**3)
        print(f"  Size: {size_gb:.2f} GB")
        return archive_path

    print(f"\n[CREATING ARCHIVE] {ARCHIVE_NAME}")
    print("This may take a while for 24.7 GB of data...\n")

    # Files and folders to include
    include_items = [
        ("data", "Main data directory"),
        ("metadata", "Container metadata"),
        ("logs", "Download and validation logs"),
        ("README.md", "Main documentation"),
        ("DATA_QUALITY_ISSUES.md", "Known issues documentation"),
        ("CHANGELOG.md", "Version history"),
        ("CITATION.cff", "Citation information"),
        ("ZENODO_VERSIONING_STRATEGY.md", "Versioning strategy"),
    ]

    with tarfile.open(archive_path, "w:gz") as tar:
        for item, description in include_items:
            item_path = Path(item)
            if item_path.exists():
                print(f"  Adding: {item:<40} ({description})")
                tar.add(item_path, arcname=f"stefan-zweig-digital-v{VERSION}/{item}")
            else:
                print(f"  ⚠ Skipping: {item:<38} (not found)")

    size_gb = archive_path.stat().st_size / (1024**3)
    print(f"\n[OK] Archive created successfully!")
    print(f"  Path: {archive_path}")
    print(f"  Size: {size_gb:.2f} GB")

    return archive_path

# ============================================================================
# ZENODO CLIENT
# ============================================================================

class ZenodoClient:
    """Simple Zenodo API client."""

    def __init__(self, token: str, sandbox: bool = False):
        self.token = token
        self.base_url = ZENODO_SANDBOX_URL if sandbox else ZENODO_PRODUCTION_URL
        self.sandbox = sandbox
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def create_deposit(self) -> dict:
        """Create a new empty deposit."""
        url = f"{self.base_url}/deposit/depositions"
        response = self.session.post(url, json={})
        response.raise_for_status()
        return response.json()

    def upload_file(self, bucket_url: str, filename: str, filepath: Path) -> dict:
        """Upload a file to deposit bucket with progress bar."""
        file_size = filepath.stat().st_size
        upload_url = f"{bucket_url}/{filename}"

        print(f"\n[UPLOADING] {filename} ({file_size / (1024**3):.2f} GB)...")
        print("This will take a while, please be patient...\n")

        with open(filepath, 'rb') as f:
            with tqdm(total=file_size, unit='B', unit_scale=True,
                      unit_divisor=1024, desc="Progress") as pbar:
                # Simple PUT upload (Zenodo handles large files)
                response = self.session.put(
                    upload_url,
                    data=f,
                    headers={"Content-Type": "application/octet-stream"}
                )
                pbar.update(file_size)

        response.raise_for_status()
        print("\n[OK] Upload complete!")
        return response.json()

    def set_metadata(self, deposit_id: int, metadata: dict) -> dict:
        """Set metadata for deposit."""
        url = f"{self.base_url}/deposit/depositions/{deposit_id}"
        response = self.session.put(url, json={"metadata": metadata})
        if response.status_code != 200:
            print(f"\n[DEBUG] Metadata error response: {response.text}")
        response.raise_for_status()
        return response.json()

    def publish_deposit(self, deposit_id: int) -> dict:
        """Publish deposit (assigns DOI)."""
        url = f"{self.base_url}/deposit/depositions/{deposit_id}/actions/publish"
        response = self.session.post(url)
        response.raise_for_status()
        return response.json()

# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Upload Stefan Zweig Digital Archive v1.0.0 to Zenodo"
    )
    parser.add_argument(
        "--token",
        help="Zenodo API access token"
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use Zenodo Sandbox for testing (recommended first!)"
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish deposit after upload (assigns DOI)"
    )
    parser.add_argument(
        "--create-archive-only",
        action="store_true",
        help="Only create archive, don't upload"
    )

    args = parser.parse_args()

    # Header
    print("=" * 70)
    print("Stefan Zweig Digital Archive - Zenodo Upload")
    print(f"Version: {VERSION}")
    print(f"Date: {PUBLICATION_DATE}")
    print("=" * 70)

    # Step 1: Create archive
    print("\nSTEP 1: CREATE ARCHIVE")
    print("-" * 70)
    archive_path = create_complete_archive()

    if args.create_archive_only:
        print("\n[OK] Archive creation complete. Exiting (--create-archive-only)")
        return

    # Get token
    token = args.token or os.getenv("ZENODO_TOKEN")
    if not token:
        print("\n[ERROR] Zenodo token required!")
        print("Options:")
        print("  1. Use --token YOUR_TOKEN")
        print("  2. Set ZENODO_TOKEN environment variable")
        print("\nFor Sandbox: Use your Sandbox token")
        print("For Production: Use your Production token")
        sys.exit(1)

    # Confirm environment
    env = "SANDBOX (sandbox.zenodo.org)" if args.sandbox else "PRODUCTION (zenodo.org)"
    print(f"\nSTEP 2: UPLOAD TO ZENODO")
    print("-" * 70)
    print(f"Environment: {env}")
    print(f"Archive: {archive_path}")
    print(f"Size: {archive_path.stat().st_size / (1024**3):.2f} GB")
    print(f"Will publish: {'YES [WARNING]' if args.publish else 'NO (draft only)'}")

    if not args.sandbox and args.publish:
        print("\n[WARNING] You are about to publish to PRODUCTION!")
        confirm = input("Type 'yes' to continue: ")
        if confirm.lower() != 'yes':
            print("Aborted.")
            sys.exit(0)

    # Initialize client
    client = ZenodoClient(token, sandbox=args.sandbox)

    try:
        # Create deposit
        print("\n2.1 Creating deposit...")
        deposit = client.create_deposit()
        deposit_id = deposit['id']
        bucket_url = deposit['links']['bucket']
        print(f"[OK] Deposit created (ID: {deposit_id})")

        # Upload file
        print(f"\n2.2 Uploading file...")
        client.upload_file(bucket_url, ARCHIVE_NAME, archive_path)

        # Set metadata
        print(f"\n2.3 Setting metadata...")
        client.set_metadata(deposit_id, METADATA)
        print("[OK] Metadata set")

        # Publish or save as draft
        if args.publish:
            print(f"\n2.4 Publishing deposit...")
            result = client.publish_deposit(deposit_id)
            doi = result.get('doi', 'N/A')
            concept_doi = result.get('conceptdoi', 'N/A')
            record_url = result['links'].get('record_html', 'N/A')

            print("\n" + "=" * 70)
            print("[SUCCESS] SUCCESSFULLY PUBLISHED!")
            print("=" * 70)
            print(f"Version DOI:  {doi}")
            print(f"Concept DOI:  {concept_doi}")
            print(f"URL:          {record_url}")
            print("\n[INFO] Version DOI: Use in citations for this specific version")
            print("[INFO] Concept DOI: Always points to latest version")

        else:
            web_url = f"https://{'sandbox.' if args.sandbox else ''}zenodo.org/deposit/{deposit_id}"
            print("\n" + "=" * 70)
            print("[SUCCESS] DRAFT SAVED!")
            print("=" * 70)
            print(f"Deposit ID: {deposit_id}")
            print(f"Review at:  {web_url}")
            print("\nNext steps:")
            print("  1. Review the deposit in your browser")
            print("  2. Check metadata and files")
            print("  3. Publish manually or re-run with --publish")

    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        print(f"\nDeposit ID {deposit_id} may have been created.")
        print("Check your Zenodo dashboard to clean up or continue manually.")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("Done!")
    print("=" * 70)

if __name__ == "__main__":
    main()
