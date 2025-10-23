#!/usr/bin/env python3
"""
Create separate tar.gz archives for each collection in the Stefan Zweig Digital archive.

This script creates four separate archives:
1. stefan-zweig-digital-facsimiles-v1.0.0.tar.gz
2. stefan-zweig-digital-aufsatz-v1.0.0.tar.gz
3. stefan-zweig-digital-lebensdokumente-v1.0.0.tar.gz
4. stefan-zweig-digital-korrespondenzen-v1.0.0.tar.gz

Each archive contains:
- Collection-specific data (objects with images, mets.xml, metadata.json)
- Metadata files
- Documentation
- Scripts
- Logs

This allows for easier upload to Zenodo and better organization.
"""

import tarfile
import os
from pathlib import Path
import json
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR  # Archives will be created in the root directory
VERSION = "v1.0.0"

# Collections to process
COLLECTIONS = {
    'facsimiles': {
        'name': 'Facsimiles',
        'description': 'Manuscripts and original documents',
        'data_path': 'data/facsimiles',
        'objects': 169
    },
    'aufsatz': {
        'name': 'Essays (Aufsätze)',
        'description': 'Essays and articles by Stefan Zweig',
        'data_path': 'data/aufsatz',
        'objects': 625
    },
    'lebensdokumente': {
        'name': 'Life Documents (Lebensdokumente)',
        'description': 'Biographical materials and life documents',
        'data_path': 'data/lebensdokumente',
        'objects': 127
    },
    'korrespondenzen': {
        'name': 'Correspondence (Korrespondenzen)',
        'description': 'Letters and correspondence',
        'data_path': 'data/korrespondenzen',
        'objects': 1186
    }
}

# Common files to include in all archives
COMMON_FILES = [
    'README.md',
    'DOCUMENTATION.md',
    'CHANGELOG.md',
    'CITATION.cff',
    'requirements.txt',
    '.gitignore',
    'metadata',
    'scripts',
    'logs',
    'docs'
]


def get_human_readable_size(size_bytes):
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def create_collection_readme(collection_key, collection_info):
    """Create a collection-specific README."""
    return f"""# Stefan Zweig Digital Archive - {collection_info['name']}

**Version:** {VERSION}
**Collection:** {collection_info['name']}
**Description:** {collection_info['description']}
**Objects:** {collection_info['objects']}

## About This Archive

This archive contains the **{collection_info['name']}** collection from the Stefan Zweig Digital project.

This is part of a multi-volume archive. For the complete collection, see:
- stefan-zweig-digital-facsimiles-{VERSION}.tar.gz (169 objects)
- stefan-zweig-digital-aufsatz-{VERSION}.tar.gz (625 objects)
- stefan-zweig-digital-lebensdokumente-{VERSION}.tar.gz (127 objects)
- stefan-zweig-digital-korrespondenzen-{VERSION}.tar.gz (1,186 objects)

## Contents

```
stefan-zweig-digital-{collection_key}-{VERSION}/
├── data/
│   └── {collection_key}/           # {collection_info['objects']} objects
│       └── o_szd_XXX/
│           ├── mets.xml            # METS/MODS metadata
│           ├── metadata.json       # Parsed JSON
│           └── images/             # High-resolution JPEG images
├── metadata/                       # Container metadata
├── docs/                           # Documentation
├── scripts/                        # Python scripts
├── logs/                           # Progress and validation logs
├── README.md                       # Main documentation
├── DOCUMENTATION.md                # Complete technical docs
├── CHANGELOG.md                    # Version history
├── CITATION.cff                    # Citation metadata
└── requirements.txt                # Python dependencies
```

## Usage

See the main [README.md](README.md) and [DOCUMENTATION.md](DOCUMENTATION.md) for complete usage instructions.

## License

- **Code/Scripts:** MIT License
- **Data:** CC-BY 4.0 (Creative Commons Attribution 4.0 International)

## Citation

See [CITATION.cff](CITATION.cff) for citation information.

## More Information

- **Project:** https://stefanzweig.digital
- **GAMS:** https://gams.uni-graz.at/context:szd
- **Zenodo:** https://doi.org/10.5281/zenodo.XXXXXX

---

**Part of the Stefan Zweig Digital Archive {VERSION}**
**Created:** {datetime.now().strftime('%Y-%m-%d')}
"""


def create_archive(collection_key, collection_info):
    """Create a tar.gz archive for a specific collection."""

    archive_name = f"stefan-zweig-digital-{collection_key}-{VERSION}.tar.gz"
    archive_path = OUTPUT_DIR / archive_name

    print(f"\n{'='*70}")
    print(f"Creating archive: {archive_name}")
    print(f"Collection: {collection_info['name']}")
    print(f"Expected objects: {collection_info['objects']}")
    print(f"{'='*70}\n")

    # Create a temporary README for this collection
    collection_readme_path = BASE_DIR / f"README_{collection_key}.md"
    with open(collection_readme_path, 'w', encoding='utf-8') as f:
        f.write(create_collection_readme(collection_key, collection_info))

    archive_root = f"stefan-zweig-digital-{collection_key}-{VERSION}"

    try:
        with tarfile.open(archive_path, 'w:gz') as tar:
            # Track statistics
            total_size = 0
            file_count = 0

            # Add collection-specific README
            print(f"[1/6] Adding collection-specific README...")
            tar.add(collection_readme_path,
                   arcname=f"{archive_root}/README_{collection_key}.md")
            file_count += 1

            # Add collection data
            print(f"[2/6] Adding collection data: {collection_info['data_path']}...")
            data_path = BASE_DIR / collection_info['data_path']
            if data_path.exists():
                tar.add(data_path, arcname=f"{archive_root}/data/{collection_key}")

                # Count files and size
                for root, dirs, files in os.walk(data_path):
                    for file in files:
                        file_path = Path(root) / file
                        total_size += file_path.stat().st_size
                        file_count += 1

                print(f"   + Added {file_count} files ({get_human_readable_size(total_size)})")
            else:
                print(f"   ! Warning: {data_path} not found")

            # Add common files
            print(f"[3/6] Adding common documentation files...")
            for common_file in COMMON_FILES:
                file_path = BASE_DIR / common_file
                if file_path.exists():
                    tar.add(file_path, arcname=f"{archive_root}/{common_file}")

                    if file_path.is_file():
                        size = file_path.stat().st_size
                        print(f"   + Added {common_file} ({get_human_readable_size(size)})")
                    else:
                        # Count files in directory
                        dir_file_count = sum(1 for _ in file_path.rglob('*') if _.is_file())
                        print(f"   + Added {common_file}/ ({dir_file_count} files)")

            print(f"[4/6] Finalizing archive...")

        # Get final archive size
        archive_size = archive_path.stat().st_size

        print(f"\n[5/6] Archive created successfully!")
        print(f"   Archive: {archive_name}")
        print(f"   Size: {get_human_readable_size(archive_size)}")
        print(f"   Location: {archive_path}")

        # Create metadata file
        metadata = {
            'collection': collection_key,
            'collection_name': collection_info['name'],
            'description': collection_info['description'],
            'version': VERSION,
            'archive_name': archive_name,
            'objects_count': collection_info['objects'],
            'archive_size_bytes': archive_size,
            'archive_size_human': get_human_readable_size(archive_size),
            'created': datetime.now().isoformat(),
            'part_of': f"Stefan Zweig Digital Archive {VERSION}",
            'other_parts': [
                f"stefan-zweig-digital-facsimiles-{VERSION}.tar.gz",
                f"stefan-zweig-digital-aufsatz-{VERSION}.tar.gz",
                f"stefan-zweig-digital-lebensdokumente-{VERSION}.tar.gz",
                f"stefan-zweig-digital-korrespondenzen-{VERSION}.tar.gz"
            ]
        }

        metadata_path = OUTPUT_DIR / f"{archive_name}.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"[6/6] Metadata saved to: {metadata_path.name}")

        return {
            'archive_name': archive_name,
            'archive_size': archive_size,
            'metadata': metadata
        }

    finally:
        # Clean up temporary README
        if collection_readme_path.exists():
            collection_readme_path.unlink()


def main():
    """Main function to create all collection archives."""

    print("\n" + "="*70)
    print("Stefan Zweig Digital Archive - Split Archive Creator")
    print("="*70)
    print(f"Version: {VERSION}")
    print(f"Base directory: {BASE_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Collections to process: {len(COLLECTIONS)}")
    print("="*70)

    # Verify that data directory exists
    data_dir = BASE_DIR / 'data'
    if not data_dir.exists():
        print(f"\n[ERROR] Data directory not found: {data_dir}")
        print("Please ensure you are running this script from the correct directory.")
        return

    results = []
    total_size = 0

    # Create archives for each collection
    for collection_key, collection_info in COLLECTIONS.items():
        result = create_archive(collection_key, collection_info)
        results.append(result)
        total_size += result['archive_size']

    # Print summary
    print("\n" + "="*70)
    print("SUMMARY - All Archives Created")
    print("="*70)

    for result in results:
        print(f"\n{result['archive_name']}")
        print(f"  Size: {get_human_readable_size(result['archive_size'])}")
        print(f"  Objects: {result['metadata']['objects_count']}")

    print(f"\n{'='*70}")
    print(f"Total size of all archives: {get_human_readable_size(total_size)}")
    print(f"Number of archives: {len(results)}")
    print(f"Average size per archive: {get_human_readable_size(total_size / len(results))}")
    print(f"{'='*70}")

    # Create a master metadata file
    master_metadata = {
        'project': 'Stefan Zweig Digital Archive',
        'version': VERSION,
        'split_archives': True,
        'archive_count': len(results),
        'total_size_bytes': total_size,
        'total_size_human': get_human_readable_size(total_size),
        'created': datetime.now().isoformat(),
        'archives': [r['metadata'] for r in results]
    }

    master_metadata_path = OUTPUT_DIR / f"stefan-zweig-digital-{VERSION}-archives-manifest.json"
    with open(master_metadata_path, 'w', encoding='utf-8') as f:
        json.dump(master_metadata, f, indent=2, ensure_ascii=False)

    print(f"\nMaster manifest created: {master_metadata_path.name}")
    print("\n[SUCCESS] All archives created successfully!")
    print("\nNext steps:")
    print("1. Verify archive contents using tar -tzf <archive_name>")
    print("2. Upload each archive separately to Zenodo")
    print("3. Link all archives together using 'Related Identifiers' in Zenodo metadata")
    print(f"4. Update DOI references in documentation after upload")


if __name__ == "__main__":
    main()
