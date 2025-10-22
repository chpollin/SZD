#!/usr/bin/env python3
"""
Upload ONLY metadata to an existing Zenodo deposit.
File upload must be done manually via web interface.

Usage:
    python zenodo_metadata_only.py --deposit-id 17418961 --token YOUR_TOKEN
"""

import argparse
import requests
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================

ZENODO_PRODUCTION_URL = "https://zenodo.org/api"
ZENODO_SANDBOX_URL = "https://sandbox.zenodo.org/api"

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
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Upload metadata to existing Zenodo deposit"
    )
    parser.add_argument(
        "--deposit-id",
        required=True,
        type=int,
        help="Zenodo deposit ID (e.g., 17418961)"
    )
    parser.add_argument(
        "--token",
        required=True,
        help="Zenodo API access token"
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use Zenodo Sandbox instead of production"
    )

    args = parser.parse_args()

    # Setup
    base_url = ZENODO_SANDBOX_URL if args.sandbox else ZENODO_PRODUCTION_URL
    env = "SANDBOX" if args.sandbox else "PRODUCTION"

    print("=" * 70)
    print("Zenodo Metadata Upload")
    print("=" * 70)
    print(f"Environment: {env}")
    print(f"Deposit ID:  {args.deposit_id}")
    print()

    # Create session
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {args.token}"})

    # Upload metadata
    url = f"{base_url}/deposit/depositions/{args.deposit_id}"

    print("Uploading metadata...")
    response = session.put(url, json={"metadata": METADATA})

    if response.status_code == 200:
        print("[OK] Metadata uploaded successfully!")
        print()
        web_url = f"https://{'sandbox.' if args.sandbox else ''}zenodo.org/uploads/{args.deposit_id}"
        print(f"View at: {web_url}")
        print()
        print("Next steps:")
        print("  1. Check the metadata on the web interface")
        print("  2. Upload the file manually:")
        print("     C:\\Users\\Chrisi\\Documents\\PROJECTS\\szd-backup\\stefan-zweig-digital-v1.0.0.tar.gz")
        print("  3. Review everything before publishing")
    else:
        print(f"[ERROR] Failed to upload metadata!")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    main()
