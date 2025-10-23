#!/usr/bin/env python3
"""
Create a single Zenodo deposit with metadata for all 4 Stefan Zweig collections.
Files will be uploaded manually via web interface.

Usage:
    python zenodo_create_deposit_only.py --token YOUR_TOKEN
"""

import requests
import json
from datetime import datetime
import argparse

# Zenodo Production URL
ZENODO_URL = "https://zenodo.org/api"

# Complete metadata for the entire archive (all 4 collections)
METADATA = {
    'metadata': {
        'title': 'Stefan Zweig Digital - Complete Archive (4 Collections, v1.0.0)',
        'upload_type': 'dataset',
        'description': '''Complete backup of the Stefan Zweig Digital collection from GAMS (Geisteswissenschaftliches Asset Management System, University of Graz).

## Overview

This archive contains the complete Stefan Zweig Digital collection, split into 4 collection-based archives for easier handling:

1. **Facsimiles** (169 objects, 9.0 GB) - Manuscripts and original documents
2. **Essays/Aufsätze** (625 objects, 4.6 GB) - Essays and articles by Stefan Zweig
3. **Life Documents/Lebensdokumente** (127 objects, 3.4 GB) - Biographical materials
4. **Correspondence/Korrespondenzen** (1,186 objects, 5.5 GB) - Letters and correspondence

**Total:** 2,107 digitized objects, 18,719 high-resolution images, ~22.3 GB

## Archive Files

This deposit contains 4 separate tar.gz archives:

- `stefan-zweig-digital-facsimiles-v1.0.0.tar.gz` (9.0 GB)
- `stefan-zweig-digital-aufsatz-v1.0.0.tar.gz` (4.6 GB)
- `stefan-zweig-digital-lebensdokumente-v1.0.0.tar.gz` (3.4 GB)
- `stefan-zweig-digital-korrespondenzen-v1.0.0.tar.gz` (5.5 GB)

Each archive is self-contained and includes:
- Collection-specific data (objects with METS/MODS metadata)
- High-resolution JPEG images (~4912×7360 pixels)
- JSON metadata files
- Complete documentation and scripts
- Processing logs

## Contents

### Data Quality
- **Completeness:** 99.0% (2,085 of 2,107 objects complete)
- **Missing images:** 729 images (3.7%) due to server-side metadata issues
- **Downloaded images:** 18,719 high-resolution images
- **Data integrity:** 100% (all downloaded files validated)

### Metadata Standards
- **METS/MODS:** DFG-METS (Deutsche Forschungsgemeinschaft)
- **DataCite:** Metadata Schema 4.0
- **Citation File Format:** CITATION.cff included

### Technical Details
- **Image format:** JPEG, ~4912×7360 pixels, RGB
- **Archive format:** tar.gz compression
- **Total size:** 22.3 GB compressed (24.7 GB uncompressed)

## Usage

Each archive can be extracted independently:

```bash
# Extract single collection
tar -xzf stefan-zweig-digital-facsimiles-v1.0.0.tar.gz

# Extract all collections
tar -xzf stefan-zweig-digital-*.tar.gz
```

See the included README.md and DOCUMENTATION.md for complete usage instructions.

## Source

- **Project:** https://stefanzweig.digital
- **Source repository:** https://gams.uni-graz.at/context:szd
- **Institution:** Literaturarchiv Salzburg, Paris Lodron Universität Salzburg
- **Technical infrastructure:** GAMS, Universität Graz

## License

- **Code/Scripts:** MIT License
- **Data:** CC-BY 4.0 (Creative Commons Attribution 4.0 International)

## Citation

```
Zangerl, L. M., Glunk, J. R., Matuschek, O., & Pollin, C. (2025).
Stefan Zweig Digital - Complete Archive (4 Collections, v1.0.0) [Data set].
Zenodo. https://doi.org/10.5281/zenodo.XXXXXX
```

## Related Resources

- **GND (Stefan Zweig):** https://d-nb.info/gnd/118637479
- **Wikidata:** https://www.wikidata.org/wiki/Q78491
- **Project website:** https://stefanzweig.digital
- **Source collection:** https://gams.uni-graz.at/context:szd

## FAIR Compliance

This dataset follows FAIR principles with a 92% compliance score:
- **Findable:** DOI, ORCID IDs, GND, Wikidata identifiers
- **Accessible:** Open Access, CC-BY 4.0 license
- **Interoperable:** METS/MODS, DataCite, controlled vocabularies
- **Reusable:** Detailed provenance, clear licensing, complete documentation

## Acknowledgments

This archive was created using data from:
- **Literaturarchiv Salzburg** - Collection ownership and curation
- **GAMS (University of Graz)** - Digital infrastructure and hosting
- **Stefan Zweig Digital Project** - Digitization and coordination

---

**Version:** v1.0.0
**Publication Date:** 2025-10-22
**Archive Creation Date:** 2025-10-23
**Collections:** 4 (Facsimiles, Essays, Life Documents, Correspondence)
**Total Objects:** 2,107
**Total Images:** 18,719
**Total Size:** 22.3 GB compressed
''',
        'creators': [
            {
                'name': 'Zangerl, Lina Maria',
                'affiliation': 'Literaturarchiv Salzburg, Paris Lodron Universität Salzburg',
                'orcid': '0000-0001-9709-3669'
            },
            {
                'name': 'Glunk, Julia Rebecca',
                'affiliation': 'Literaturarchiv Salzburg, Paris Lodron Universität Salzburg',
                'orcid': '0000-0001-6647-9729'
            },
            {
                'name': 'Matuschek, Oliver',
                'affiliation': 'Literaturarchiv Salzburg, Paris Lodron Universität Salzburg'
            },
            {
                'name': 'Pollin, Christopher',
                'affiliation': 'Digital Humanities Craft OG',
                'orcid': '0000-0002-4879-129X'
            }
        ],
        'contributors': [
            {
                'name': 'Literaturarchiv Salzburg, Paris Lodron Universität Salzburg',
                'type': 'HostingInstitution'
            },
            {
                'name': 'GAMS, Universität Graz',
                'type': 'DataCollector'
            }
        ],
        'keywords': [
            'Stefan Zweig',
            'Digital Humanities',
            'Cultural Heritage',
            'Digital Archive',
            'METS/MODS',
            'Manuscripts',
            'Essays',
            'Biography',
            'Correspondence',
            'Literaturarchiv Salzburg',
            'GAMS',
            'DFG-METS',
            'FAIR data',
            'Open Access'
        ],
        'license': 'cc-by-4.0',
        'publication_date': '2025-10-22',
        'version': 'v1.0.0',
        'language': 'deu',
        'subjects': [
            {
                'term': 'Languages and Literature',
                'identifier': 'http://www.oecd.org/science/inno/38235147.pdf',
                'scheme': 'url'
            }
        ],
        'related_identifiers': [
            {
                'relation': 'isSupplementTo',
                'identifier': 'https://stefanzweig.digital',
                'resource_type': 'other'
            },
            {
                'relation': 'isDerivedFrom',
                'identifier': 'https://gams.uni-graz.at/context:szd',
                'resource_type': 'dataset'
            },
            {
                'relation': 'isDerivedFrom',
                'identifier': 'https://gams.uni-graz.at/context:szd.facsimiles',
                'resource_type': 'dataset'
            },
            {
                'relation': 'isDerivedFrom',
                'identifier': 'https://gams.uni-graz.at/context:szd.facsimiles.aufsatz',
                'resource_type': 'dataset'
            },
            {
                'relation': 'isDerivedFrom',
                'identifier': 'https://gams.uni-graz.at/context:szd.facsimiles.lebensdokumente',
                'resource_type': 'dataset'
            },
            {
                'relation': 'isDerivedFrom',
                'identifier': 'https://gams.uni-graz.at/context:szd.facsimiles.korrespondenzen',
                'resource_type': 'dataset'
            },
            {
                'relation': 'documents',
                'identifier': 'https://d-nb.info/gnd/118637479',
                'scheme': 'gnd'
            },
            {
                'relation': 'documents',
                'identifier': 'https://www.wikidata.org/wiki/Q78491',
                'scheme': 'url'
            }
        ],
        'notes': 'This archive is split into 4 separate tar.gz files for easier handling. Each file can be extracted and used independently. See documentation for complete details on data quality, known limitations, and usage instructions.'
    }
}


def create_deposit(token):
    """Create a new Zenodo deposit with metadata."""

    print("="*70)
    print("Creating Zenodo Deposit for Stefan Zweig Digital Archive")
    print("="*70)

    # Step 1: Create empty deposit
    print("\n[1/3] Creating empty deposit...")
    headers = {'Content-Type': 'application/json'}

    response = requests.post(
        f"{ZENODO_URL}/deposit/depositions",
        params={'access_token': token},
        json={},
        headers=headers
    )

    if response.status_code != 201:
        print(f"[ERROR] Failed to create deposit: {response.status_code}")
        print(response.text)
        return None

    deposit = response.json()
    deposit_id = deposit['id']
    print(f"  + Deposit created successfully!")
    print(f"  + Deposit ID: {deposit_id}")

    # Step 2: Update metadata
    print("\n[2/3] Updating metadata...")
    response = requests.put(
        f"{ZENODO_URL}/deposit/depositions/{deposit_id}",
        params={'access_token': token},
        json=METADATA,
        headers=headers
    )

    if response.status_code != 200:
        print(f"[ERROR] Failed to update metadata: {response.status_code}")
        print(response.text)
        return None

    updated_deposit = response.json()
    print(f"  + Metadata updated successfully!")

    # Step 3: Display results
    print("\n[3/3] Deposit created successfully!")
    print("="*70)
    print("DEPOSIT INFORMATION")
    print("="*70)
    print(f"Deposit ID: {deposit_id}")
    print(f"Draft URL: {updated_deposit['links']['html']}")
    print(f"Bucket URL: {updated_deposit['links']['bucket']}")
    print(f"Pre-reserved DOI: {updated_deposit.get('doi', 'Will be assigned on publish')}")
    print(f"Concept DOI: {updated_deposit.get('conceptdoi', 'Will be assigned on publish')}")

    print("\n" + "="*70)
    print("FILES TO UPLOAD MANUALLY")
    print("="*70)
    print("\nPlease upload these 4 files via the Zenodo web interface:")
    print("\n1. stefan-zweig-digital-facsimiles-v1.0.0.tar.gz (9.0 GB)")
    print("2. stefan-zweig-digital-aufsatz-v1.0.0.tar.gz (4.6 GB)")
    print("3. stefan-zweig-digital-lebensdokumente-v1.0.0.tar.gz (3.4 GB)")
    print("4. stefan-zweig-digital-korrespondenzen-v1.0.0.tar.gz (5.5 GB)")

    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print(f"\n1. Go to: {updated_deposit['links']['html']}")
    print("2. Click 'Upload files'")
    print("3. Upload all 4 tar.gz archives")
    print("4. Review the metadata")
    print("5. Click 'Publish' when ready")
    print("\nIMPORTANT: Do not publish until all 4 files are uploaded!")

    # Save deposit info
    result = {
        'deposit_id': deposit_id,
        'deposit_url': updated_deposit['links']['html'],
        'bucket_url': updated_deposit['links']['bucket'],
        'doi': updated_deposit.get('doi', 'Not yet assigned'),
        'concept_doi': updated_deposit.get('conceptdoi', 'Not yet assigned'),
        'created': datetime.now().isoformat(),
        'status': 'draft',
        'files_to_upload': [
            'stefan-zweig-digital-facsimiles-v1.0.0.tar.gz',
            'stefan-zweig-digital-aufsatz-v1.0.0.tar.gz',
            'stefan-zweig-digital-lebensdokumente-v1.0.0.tar.gz',
            'stefan-zweig-digital-korrespondenzen-v1.0.0.tar.gz'
        ]
    }

    output_file = f"zenodo_deposit_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nDeposit information saved to: {output_file}")
    print("="*70)

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Create Zenodo deposit with metadata for Stefan Zweig Digital Archive'
    )
    parser.add_argument('--token', required=True, help='Zenodo API access token')

    args = parser.parse_args()

    result = create_deposit(args.token)

    if result:
        print("\n[SUCCESS] Deposit created successfully!")
        print(f"\nDeposit URL: {result['deposit_url']}")
    else:
        print("\n[FAILED] Could not create deposit")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
