#!/usr/bin/env python3
"""
Upload split archives to Zenodo with proper metadata.

This script creates 4 separate Zenodo deposits, one for each collection,
uploads the files, and links them together using Related Identifiers.

Usage:
    # Test on Sandbox
    python zenodo_upload_split.py --sandbox --token YOUR_SANDBOX_TOKEN

    # Upload to Production (creates drafts)
    python zenodo_upload_split.py --token YOUR_PROD_TOKEN

    # Upload to Production and publish
    python zenodo_upload_split.py --token YOUR_PROD_TOKEN --publish
"""

import requests
import json
import os
from pathlib import Path
import argparse
from datetime import datetime
import time

# Configuration
BASE_DIR = Path(__file__).parent.parent
VERSION = "v1.0.0"

# Zenodo URLs
ZENODO_SANDBOX_URL = "https://sandbox.zenodo.org/api"
ZENODO_PROD_URL = "https://zenodo.org/api"

# Collections with metadata
COLLECTIONS = {
    'facsimiles': {
        'title': 'Stefan Zweig Digital - Facsimiles Collection (v1.0.0)',
        'description': """This archive contains the Facsimiles collection from the Stefan Zweig Digital project - manuscripts and original documents from the Stefan Zweig archive at Literaturarchiv Salzburg.

**Collection:** Facsimiles (169 objects)
**Part of:** Stefan Zweig Digital Complete Archive (4 volumes, v1.0.0)

This is one of four collection-based archives:
- Facsimiles (169 objects) - This collection
- Essays/Aufsätze (625 objects)
- Life Documents/Lebensdokumente (127 objects)
- Correspondence/Korrespondenzen (1,186 objects)

**Total archive:** 2,107 objects, 18,719 high-resolution images

**Contents:**
- 169 digitized objects with METS/MODS metadata
- High-resolution JPEG images (~4912×7360 pixels)
- Complete metadata in JSON format
- Documentation and scripts for data processing

**Source:** GAMS (Geisteswissenschaftliches Asset Management System), University of Graz
**Project:** https://stefanzweig.digital
**License:** CC-BY 4.0""",
        'keywords': ['Stefan Zweig', 'Digital Humanities', 'Cultural Heritage', 'Digital Archive',
                     'METS/MODS', 'Manuscripts', 'Facsimiles', 'Literaturarchiv Salzburg', 'GAMS'],
        'archive_file': 'stefan-zweig-digital-facsimiles-v1.0.0.tar.gz',
        'source_url': 'https://gams.uni-graz.at/context:szd.facsimiles'
    },
    'aufsatz': {
        'title': 'Stefan Zweig Digital - Essays Collection (v1.0.0)',
        'description': """This archive contains the Essays (Aufsätze) collection from the Stefan Zweig Digital project - essays and articles by Stefan Zweig from the archive at Literaturarchiv Salzburg.

**Collection:** Essays/Aufsätze (625 objects)
**Part of:** Stefan Zweig Digital Complete Archive (4 volumes, v1.0.0)

This is one of four collection-based archives:
- Facsimiles (169 objects)
- Essays/Aufsätze (625 objects) - This collection
- Life Documents/Lebensdokumente (127 objects)
- Correspondence/Korrespondenzen (1,186 objects)

**Total archive:** 2,107 objects, 18,719 high-resolution images

**Contents:**
- 625 digitized objects with METS/MODS metadata
- High-resolution JPEG images (~4912×7360 pixels)
- Complete metadata in JSON format
- Documentation and scripts for data processing

**Source:** GAMS (Geisteswissenschaftliches Asset Management System), University of Graz
**Project:** https://stefanzweig.digital
**License:** CC-BY 4.0""",
        'keywords': ['Stefan Zweig', 'Digital Humanities', 'Cultural Heritage', 'Digital Archive',
                     'METS/MODS', 'Essays', 'Articles', 'Literaturarchiv Salzburg', 'GAMS'],
        'archive_file': 'stefan-zweig-digital-aufsatz-v1.0.0.tar.gz',
        'source_url': 'https://gams.uni-graz.at/context:szd.facsimiles.aufsatz'
    },
    'lebensdokumente': {
        'title': 'Stefan Zweig Digital - Life Documents Collection (v1.0.0)',
        'description': """This archive contains the Life Documents (Lebensdokumente) collection from the Stefan Zweig Digital project - biographical materials from the Stefan Zweig archive at Literaturarchiv Salzburg.

**Collection:** Life Documents/Lebensdokumente (127 objects)
**Part of:** Stefan Zweig Digital Complete Archive (4 volumes, v1.0.0)

This is one of four collection-based archives:
- Facsimiles (169 objects)
- Essays/Aufsätze (625 objects)
- Life Documents/Lebensdokumente (127 objects) - This collection
- Correspondence/Korrespondenzen (1,186 objects)

**Total archive:** 2,107 objects, 18,719 high-resolution images

**Contents:**
- 127 digitized objects with METS/MODS metadata
- High-resolution JPEG images (~4912×7360 pixels)
- Complete metadata in JSON format
- Documentation and scripts for data processing

**Source:** GAMS (Geisteswissenschaftliches Asset Management System), University of Graz
**Project:** https://stefanzweig.digital
**License:** CC-BY 4.0""",
        'keywords': ['Stefan Zweig', 'Digital Humanities', 'Cultural Heritage', 'Digital Archive',
                     'METS/MODS', 'Biography', 'Life Documents', 'Literaturarchiv Salzburg', 'GAMS'],
        'archive_file': 'stefan-zweig-digital-lebensdokumente-v1.0.0.tar.gz',
        'source_url': 'https://gams.uni-graz.at/context:szd.facsimiles.lebensdokumente'
    },
    'korrespondenzen': {
        'title': 'Stefan Zweig Digital - Correspondence Collection (v1.0.0)',
        'description': """This archive contains the Correspondence (Korrespondenzen) collection from the Stefan Zweig Digital project - letters and correspondence from the Stefan Zweig archive at Literaturarchiv Salzburg.

**Collection:** Correspondence/Korrespondenzen (1,186 objects)
**Part of:** Stefan Zweig Digital Complete Archive (4 volumes, v1.0.0)

This is one of four collection-based archives:
- Facsimiles (169 objects)
- Essays/Aufsätze (625 objects)
- Life Documents/Lebensdokumente (127 objects)
- Correspondence/Korrespondenzen (1,186 objects) - This collection

**Total archive:** 2,107 objects, 18,719 high-resolution images

**Contents:**
- 1,186 digitized objects with METS/MODS metadata
- High-resolution JPEG images (~4912×7360 pixels)
- Complete metadata in JSON format
- Documentation and scripts for data processing

**Source:** GAMS (Geisteswissenschaftliches Asset Management System), University of Graz
**Project:** https://stefanzweig.digital
**License:** CC-BY 4.0""",
        'keywords': ['Stefan Zweig', 'Digital Humanities', 'Cultural Heritage', 'Digital Archive',
                     'METS/MODS', 'Correspondence', 'Letters', 'Literaturarchiv Salzburg', 'GAMS'],
        'archive_file': 'stefan-zweig-digital-korrespondenzen-v1.0.0.tar.gz',
        'source_url': 'https://gams.uni-graz.at/context:szd.facsimiles.korrespondenzen'
    }
}

# Common metadata for all collections
COMMON_METADATA = {
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
    'license': 'cc-by-4.0',
    'publication_date': '2025-10-22',
    'version': 'v1.0.0',
    'language': 'deu',
    'subjects': [
        {'term': 'Languages and Literature', 'identifier': 'http://www.oecd.org/science/inno/38235147.pdf', 'scheme': 'url'}
    ]
}


def create_deposit_metadata(collection_key, collection_info):
    """Create Zenodo deposit metadata for a collection."""

    metadata = {
        'metadata': {
            'title': collection_info['title'],
            'upload_type': 'dataset',
            'description': collection_info['description'],
            'creators': COMMON_METADATA['creators'],
            'contributors': COMMON_METADATA['contributors'],
            'keywords': collection_info['keywords'],
            'license': COMMON_METADATA['license'],
            'publication_date': COMMON_METADATA['publication_date'],
            'version': COMMON_METADATA['version'],
            'language': COMMON_METADATA['language'],
            'subjects': COMMON_METADATA['subjects'],
            'related_identifiers': [
                {
                    'relation': 'isSupplementTo',
                    'identifier': 'https://stefanzweig.digital',
                    'resource_type': 'other'
                },
                {
                    'relation': 'isDerivedFrom',
                    'identifier': collection_info['source_url'],
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
            ]
        }
    }

    return metadata


def create_deposit(base_url, token):
    """Create a new empty deposit on Zenodo."""

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(
        f"{base_url}/deposit/depositions",
        params={'access_token': token},
        json={},
        headers=headers
    )

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to create deposit: {response.status_code} - {response.text}")


def update_deposit_metadata(base_url, token, deposit_id, metadata):
    """Update deposit metadata."""

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.put(
        f"{base_url}/deposit/depositions/{deposit_id}",
        params={'access_token': token},
        json=metadata,
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to update metadata: {response.status_code} - {response.text}")


def upload_file(base_url, token, deposit_id, bucket_url, file_path):
    """Upload a file to a Zenodo deposit."""

    filename = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    print(f"  Uploading {filename} ({file_size / (1024**3):.2f} GB)...")
    print(f"  This may take a while...")

    with open(file_path, 'rb') as f:
        response = requests.put(
            f"{bucket_url}/{filename}",
            params={'access_token': token},
            data=f
        )

    if response.status_code in [200, 201]:
        print(f"  + Upload successful!")
        return response.json()
    else:
        raise Exception(f"Failed to upload file: {response.status_code} - {response.text}")


def publish_deposit(base_url, token, deposit_id):
    """Publish a deposit."""

    response = requests.post(
        f"{base_url}/deposit/depositions/{deposit_id}/actions/publish",
        params={'access_token': token}
    )

    if response.status_code == 202:
        return response.json()
    else:
        raise Exception(f"Failed to publish: {response.status_code} - {response.text}")


def process_collection(base_url, token, collection_key, collection_info, publish=False):
    """Process one collection: create deposit, upload file, optionally publish."""

    print(f"\n{'='*70}")
    print(f"Processing: {collection_info['title']}")
    print(f"{'='*70}")

    # Step 1: Create deposit
    print(f"\n[1/5] Creating deposit...")
    deposit = create_deposit(base_url, token)
    deposit_id = deposit['id']
    print(f"  + Deposit created: ID {deposit_id}")
    print(f"  + Draft URL: {deposit['links']['html']}")

    # Step 2: Update metadata
    print(f"\n[2/5] Updating metadata...")
    metadata = create_deposit_metadata(collection_key, collection_info)
    updated_deposit = update_deposit_metadata(base_url, token, deposit_id, metadata)
    print(f"  + Metadata updated successfully")

    # Step 3: Upload file
    print(f"\n[3/5] Uploading archive file...")
    archive_path = BASE_DIR / collection_info['archive_file']

    if not archive_path.exists():
        print(f"  ! WARNING: Archive file not found: {archive_path}")
        print(f"  ! Skipping file upload for this collection")
        return {
            'collection': collection_key,
            'deposit_id': deposit_id,
            'doi': deposit.get('doi', 'Not yet assigned'),
            'concept_doi': deposit.get('conceptdoi', 'Not yet assigned'),
            'url': deposit['links']['html'],
            'status': 'draft (no file uploaded)',
            'file_uploaded': False
        }

    bucket_url = deposit['links']['bucket']
    upload_file(base_url, token, deposit_id, bucket_url, str(archive_path))

    # Step 4: Get updated deposit info
    print(f"\n[4/5] Retrieving deposit information...")
    response = requests.get(
        f"{base_url}/deposit/depositions/{deposit_id}",
        params={'access_token': token}
    )
    deposit = response.json()

    result = {
        'collection': collection_key,
        'deposit_id': deposit_id,
        'doi': deposit.get('doi', 'Not yet assigned'),
        'concept_doi': deposit.get('conceptdoi', 'Not yet assigned'),
        'url': deposit['links']['html'],
        'status': 'draft',
        'file_uploaded': True
    }

    # Step 5: Publish if requested
    if publish:
        print(f"\n[5/5] Publishing deposit...")
        published = publish_deposit(base_url, token, deposit_id)
        result['status'] = 'published'
        result['doi'] = published['doi']
        result['url'] = published['links']['record_html']
        print(f"  + Published successfully!")
        print(f"  + DOI: {published['doi']}")
    else:
        print(f"\n[5/5] Skipping publish (draft saved)")
        print(f"  + You can publish later from the Zenodo web interface")

    print(f"\n{'='*70}")
    print(f"Collection processed: {collection_key}")
    print(f"  Deposit ID: {deposit_id}")
    print(f"  Status: {result['status']}")
    print(f"  URL: {result['url']}")
    print(f"{'='*70}")

    return result


def main():
    parser = argparse.ArgumentParser(description='Upload split Stefan Zweig archives to Zenodo')
    parser.add_argument('--token', required=True, help='Zenodo API access token')
    parser.add_argument('--sandbox', action='store_true', help='Use Zenodo Sandbox instead of production')
    parser.add_argument('--publish', action='store_true', help='Publish deposits immediately (default: save as draft)')
    parser.add_argument('--collection', help='Process only one collection (facsimiles, aufsatz, lebensdokumente, korrespondenzen)')
    parser.add_argument('--yes', '-y', action='store_true', help='Skip confirmation prompt')

    args = parser.parse_args()

    # Select Zenodo instance
    base_url = ZENODO_SANDBOX_URL if args.sandbox else ZENODO_PROD_URL
    instance = "Sandbox" if args.sandbox else "Production"

    print("\n" + "="*70)
    print("Stefan Zweig Digital - Zenodo Split Upload")
    print("="*70)
    print(f"Zenodo Instance: {instance}")
    print(f"Base URL: {base_url}")
    print(f"Publish: {'Yes' if args.publish else 'No (draft only)'}")
    print(f"Collections: {args.collection if args.collection else 'All 4'}")
    print("="*70)

    # Verify archives exist
    print("\nVerifying archive files...")
    collections_to_process = [args.collection] if args.collection else list(COLLECTIONS.keys())

    for key in collections_to_process:
        if key not in COLLECTIONS:
            print(f"ERROR: Unknown collection '{key}'")
            return

        archive_path = BASE_DIR / COLLECTIONS[key]['archive_file']
        if archive_path.exists():
            size_gb = archive_path.stat().st_size / (1024**3)
            print(f"  + {COLLECTIONS[key]['archive_file']} ({size_gb:.2f} GB)")
        else:
            print(f"  ! {COLLECTIONS[key]['archive_file']} - NOT FOUND")

    # Skip confirmation prompt if --yes flag is used
    if not args.yes:
        try:
            input("\nPress Enter to continue or Ctrl+C to cancel...")
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled by user")
            return
    else:
        print("\nStarting upload process...")

    # Process collections
    results = []

    for key in collections_to_process:
        collection_info = COLLECTIONS[key]

        try:
            result = process_collection(base_url, args.token, key, collection_info, args.publish)
            results.append(result)

            # Wait a bit between uploads to be nice to the server
            if key != collections_to_process[-1]:
                print("\nWaiting 5 seconds before next collection...")
                time.sleep(5)

        except Exception as e:
            print(f"\n[ERROR] Failed to process {key}: {e}")
            results.append({
                'collection': key,
                'status': 'failed',
                'error': str(e)
            })

    # Summary
    print("\n" + "="*70)
    print("UPLOAD SUMMARY")
    print("="*70)

    for result in results:
        print(f"\n{result['collection'].upper()}")
        print(f"  Status: {result['status']}")
        if result.get('deposit_id'):
            print(f"  Deposit ID: {result['deposit_id']}")
        if result.get('doi') and result['doi'] != 'Not yet assigned':
            print(f"  DOI: {result['doi']}")
        if result.get('concept_doi') and result['concept_doi'] != 'Not yet assigned':
            print(f"  Concept DOI: {result['concept_doi']}")
        if result.get('url'):
            print(f"  URL: {result['url']}")
        if result.get('error'):
            print(f"  Error: {result['error']}")

    # Save results
    results_file = BASE_DIR / f"zenodo_upload_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*70}")
    print(f"Results saved to: {results_file.name}")
    print("="*70)

    # Next steps
    print("\nNext steps:")
    if not args.publish:
        print("1. Review the drafts in Zenodo web interface")
        print("2. Publish each deposit when ready")
        print("3. Note down all DOIs")
    else:
        print("1. Note down all DOIs")
    print("4. Add 'Related Identifiers' to link all 4 deposits together")
    print("5. Update documentation with DOIs")


if __name__ == "__main__":
    main()
