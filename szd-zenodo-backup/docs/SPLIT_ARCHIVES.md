# Split Archives Strategy - Stefan Zweig Digital

**Version:** 1.0.0
**Date:** 2025-10-23
**Purpose:** Multi-volume Zenodo upload strategy

---

## Overview

Due to the large size of the complete archive (23 GB), the Stefan Zweig Digital Archive has been split into **4 separate collection-based archives** for easier upload to Zenodo and better organization.

---

## Archive Structure

### Complete Archive Set (v1.0.0)

| Archive Name | Collection | Objects | Size | Description |
|--------------|------------|---------|------|-------------|
| **stefan-zweig-digital-facsimiles-v1.0.0.tar.gz** | Facsimiles | 169 | ~9.3 GB | Manuscripts and original documents |
| **stefan-zweig-digital-aufsatz-v1.0.0.tar.gz** | Essays (Aufsätze) | 625 | ~4.7 GB | Essays and articles by Stefan Zweig |
| **stefan-zweig-digital-lebensdokumente-v1.0.0.tar.gz** | Life Documents | 127 | ~3.5 GB | Biographical materials and life documents |
| **stefan-zweig-digital-korrespondenzen-v1.0.0.tar.gz** | Correspondence | 1,186 | ~5.7 GB | Letters and correspondence |
| **TOTAL** | **All Collections** | **2,107** | **~23 GB** | **Complete archive** |

---

## Benefits of Split Archives

### 1. Upload Efficiency
- Smaller file sizes for easier upload
- Better handling of network interruptions
- Faster individual uploads

### 2. Download Flexibility
- Users can download only collections of interest
- Reduced bandwidth for targeted research
- Faster access to specific materials

### 3. Organization
- Clear separation by collection type
- Logical grouping matches GAMS structure
- Easier to manage and update individual collections

### 4. Zenodo Optimization
- Each archive under 50 GB limit
- Better metadata granularity
- Can be linked using "Related Identifiers"

---

## What's Included in Each Archive

Each archive is **self-contained** and includes:

### Collection-Specific Content
```
data/
└── [collection-name]/           # Only this collection's objects
    └── o_szd_XXX/
        ├── mets.xml             # METS/MODS metadata
        ├── metadata.json        # Parsed JSON
        └── images/              # High-resolution JPEG images
            ├── IMG_1.jpg
            ├── IMG_2.jpg
            └── ...
```

### Common Files (in all archives)
```
├── README.md                    # Main documentation
├── README_[collection].md       # Collection-specific README
├── DOCUMENTATION.md             # Complete technical docs
├── CHANGELOG.md                 # Version history
├── CITATION.cff                 # Citation metadata
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git excludes
├── metadata/                    # Container metadata (all collections)
├── scripts/                     # All Python scripts
├── logs/                        # Progress and validation logs
└── docs/                        # All documentation
```

---

## Zenodo Upload Strategy

### 1. Create Separate Deposits

Create **4 separate Zenodo deposits**, one for each collection:

**Deposit 1: Facsimiles**
- Upload: `stefan-zweig-digital-facsimiles-v1.0.0.tar.gz`
- Title: "Stefan Zweig Digital - Facsimiles Collection (v1.0.0)"
- Description: Focus on manuscripts collection

**Deposit 2: Essays (Aufsätze)**
- Upload: `stefan-zweig-digital-aufsatz-v1.0.0.tar.gz`
- Title: "Stefan Zweig Digital - Essays Collection (v1.0.0)"
- Description: Focus on essays collection

**Deposit 3: Life Documents**
- Upload: `stefan-zweig-digital-lebensdokumente-v1.0.0.tar.gz`
- Title: "Stefan Zweig Digital - Life Documents Collection (v1.0.0)"
- Description: Focus on biographical materials

**Deposit 4: Correspondence**
- Upload: `stefan-zweig-digital-korrespondenzen-v1.0.0.tar.gz`
- Title: "Stefan Zweig Digital - Correspondence Collection (v1.0.0)"
- Description: Focus on letters and correspondence

### 2. Link Deposits Together

Use Zenodo's **"Related Identifiers"** feature to link all archives:

For each deposit, add:
- **Relation type:** "Is part of"
- **Related identifier:** DOI of the parent project (if exists)

And add the other 3 collections as:
- **Relation type:** "Is supplement to"
- **Related identifier:** DOIs of the other 3 collections

### 3. Metadata Consistency

Ensure **consistent metadata** across all deposits:
- Same creators (with ORCID IDs)
- Same license (CC-BY 4.0)
- Same keywords
- Same related identifiers (GND, Wikidata)
- Same subjects (OECD classification)

### 4. Version Numbers

All archives use the **same version number** (v1.0.0) to indicate they are part of the same release.

---

## Creating the Split Archives

### Using the Script

```bash
cd szd-backup
python scripts/create_split_archives.py
```

### What the Script Does

1. Creates 4 separate tar.gz archives
2. Each archive includes collection-specific data
3. All archives include common documentation and scripts
4. Creates collection-specific README files
5. Generates JSON metadata files for each archive
6. Creates a master manifest file

### Output Files

After running the script, you'll have:

```
szd-backup/
├── stefan-zweig-digital-facsimiles-v1.0.0.tar.gz
├── stefan-zweig-digital-facsimiles-v1.0.0.tar.gz.json
├── stefan-zweig-digital-aufsatz-v1.0.0.tar.gz
├── stefan-zweig-digital-aufsatz-v1.0.0.tar.gz.json
├── stefan-zweig-digital-lebensdokumente-v1.0.0.tar.gz
├── stefan-zweig-digital-lebensdokumente-v1.0.0.tar.gz.json
├── stefan-zweig-digital-korrespondenzen-v1.0.0.tar.gz
├── stefan-zweig-digital-korrespondenzen-v1.0.0.tar.gz.json
└── stefan-zweig-digital-v1.0.0-archives-manifest.json
```

---

## Verification

### Check Archive Contents

```bash
# List contents without extracting
tar -tzf stefan-zweig-digital-facsimiles-v1.0.0.tar.gz | head -20

# Verify file count
tar -tzf stefan-zweig-digital-facsimiles-v1.0.0.tar.gz | wc -l
```

### Check Metadata

```bash
# View archive metadata
cat stefan-zweig-digital-facsimiles-v1.0.0.tar.gz.json

# View master manifest
cat stefan-zweig-digital-v1.0.0-archives-manifest.json
```

---

## Extraction

### Extract Single Collection

```bash
# Extract facsimiles collection
tar -xzf stefan-zweig-digital-facsimiles-v1.0.0.tar.gz

# Extract all collections
tar -xzf stefan-zweig-digital-facsimiles-v1.0.0.tar.gz
tar -xzf stefan-zweig-digital-aufsatz-v1.0.0.tar.gz
tar -xzf stefan-zweig-digital-lebensdokumente-v1.0.0.tar.gz
tar -xzf stefan-zweig-digital-korrespondenzen-v1.0.0.tar.gz
```

---

## Future Updates

### Version Updates

When creating future versions (e.g., v1.0.1, v1.1.0, v2.0.0):

1. Run `create_split_archives.py` with updated VERSION
2. Upload new versions to Zenodo
3. Zenodo will automatically create new version DOIs
4. Keep the same linking structure

### Adding New Collections

If new collections are added:

1. Add to COLLECTIONS dict in `create_split_archives.py`
2. Create new archive for the collection
3. Upload to Zenodo as new deposit
4. Link to existing collections

---

## Citation

When citing the split archives, you can either:

### Cite Individual Collection

```bibtex
@dataset{szd_facsimiles_2025,
  author    = {Zangerl, Lina Maria and Glunk, Julia Rebecca and
               Matuschek, Oliver and Pollin, Christopher},
  title     = {Stefan Zweig Digital - Facsimiles Collection},
  year      = {2025},
  publisher = {Zenodo},
  version   = {v1.0.0},
  doi       = {10.5281/zenodo.XXXXXX}
}
```

### Cite Complete Archive

```bibtex
@dataset{szd_complete_2025,
  author    = {Zangerl, Lina Maria and Glunk, Julia Rebecca and
               Matuschek, Oliver and Pollin, Christopher},
  title     = {Stefan Zweig Digital - Complete Archive (4 volumes)},
  year      = {2025},
  publisher = {Zenodo},
  version   = {v1.0.0},
  note      = {Collections: Facsimiles, Essays, Life Documents, Correspondence}
}
```

---

## Advantages vs. Single Archive

| Aspect | Single Archive (23 GB) | Split Archives (4 × 3-9 GB) |
|--------|------------------------|----------------------------|
| Upload time | Long, single upload | Faster, parallel uploads |
| Download flexibility | All or nothing | Download only what you need |
| Network resilience | Must restart if failed | Only restart failed archive |
| Organization | Monolithic | Logical by collection |
| Zenodo limits | Close to limit | Well under limit |
| User experience | Heavy download | Lighter, targeted downloads |

---

## Technical Notes

### Archive Naming Convention

```
stefan-zweig-digital-[collection]-[version].tar.gz
```

- `[collection]`: facsimiles, aufsatz, lebensdokumente, korrespondenzen
- `[version]`: Semantic versioning (e.g., v1.0.0)

### Metadata Files

Each `.tar.gz.json` file contains:
- Collection information
- Archive size
- Object count
- Creation timestamp
- Links to other parts

### Master Manifest

The `archives-manifest.json` file contains:
- Summary of all archives
- Total size and object count
- Complete metadata for all collections

---

## Troubleshooting

### "File too large" error

If individual archives are still too large, consider:
- Further splitting by object ID ranges
- Using Zenodo's chunked upload API
- Compressing with higher compression ratios

### Missing files in archive

Verify with:
```bash
tar -tzf archive.tar.gz | grep "missing-file"
```

### Extraction fails

Ensure sufficient disk space:
- Facsimiles: ~10 GB
- Aufsatz: ~5 GB
- Lebensdokumente: ~4 GB
- Korrespondenzen: ~6 GB

---

**Document Version:** 1.0
**Last Updated:** 2025-10-23
**Script:** [create_split_archives.py](../scripts/create_split_archives.py)
