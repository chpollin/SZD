# Zenodo Upload Guide for Split Archives

**Version:** 1.0.0
**Date:** 2025-10-23
**Purpose:** Step-by-step guide for uploading split archives to Zenodo

---

## Overview

This guide explains how to upload the 4 separate collection archives to Zenodo and link them together.

---

## Prerequisites

- [ ] Zenodo account created
- [ ] All 4 split archives created (using `create_split_archives.py`)
- [ ] Access token from Zenodo
- [ ] Verified archive file sizes

---

## Upload Strategy

### Option 1: Manual Upload via Web Interface (Recommended for First Time)

Upload each archive separately through Zenodo's web interface.

### Option 2: Automated Upload via API

Use the Python script (requires modification for split archives).

---

## Step-by-Step: Manual Upload

### Step 1: Create First Deposit (Facsimiles)

1. **Go to Zenodo**
   - Navigate to: https://zenodo.org
   - Click "Upload" → "New upload"

2. **Upload Files**
   - Upload: `stefan-zweig-digital-facsimiles-v1.0.0.tar.gz`
   - Wait for upload to complete (~9.3 GB)

3. **Fill Metadata**

   **Basic Information:**
   - **Upload type:** Dataset
   - **Publication date:** 2025-10-22
   - **Title:** Stefan Zweig Digital - Facsimiles Collection (v1.0.0)
   - **Creators:**
     ```
     Zangerl, Lina Maria (ORCID: 0000-0001-9709-3669)
     Affiliation: Literaturarchiv Salzburg, Paris Lodron Universität Salzburg

     Glunk, Julia Rebecca (ORCID: 0000-0001-6647-9729)
     Affiliation: Literaturarchiv Salzburg, Paris Lodron Universität Salzburg

     Matuschek, Oliver
     Affiliation: Literaturarchiv Salzburg, Paris Lodron Universität Salzburg

     Pollin, Christopher (ORCID: 0000-0002-4879-129X)
     Affiliation: Digital Humanities Craft OG
     ```

   **Description:**
   ```
   This archive contains the Facsimiles collection from the Stefan Zweig Digital project -
   manuscripts and original documents from the Stefan Zweig archive at Literaturarchiv Salzburg.

   **Collection:** Facsimiles (169 objects, ~9.3 GB)
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
   **License:** CC-BY 4.0
   ```

   **License:**
   - Select: **Creative Commons Attribution 4.0 International**

   **Keywords:**
   ```
   Stefan Zweig
   Digital Humanities
   Cultural Heritage
   Digital Archive
   METS/MODS
   Manuscripts
   Facsimiles
   Literaturarchiv Salzburg
   GAMS
   ```

   **Additional fields:**
   - **Version:** v1.0.0
   - **Language:** German (primary content)
   - **Subjects:**
     - OECD FOS: 6.02 Languages and Literature
     - OECD FOS: 6.03 Philosophy, Ethics and Religion (History)

   **Related Identifiers:**
   ```
   Relation: Is derived from
   Identifier: https://gams.uni-graz.at/context:szd.facsimiles
   Resource type: Dataset

   Relation: Documents
   Identifier: https://d-nb.info/gnd/118637479
   Scheme: GND

   Relation: Documents
   Identifier: https://www.wikidata.org/wiki/Q78491
   Scheme: Wikidata

   Relation: Is documented by
   Identifier: https://stefanzweig.digital
   Resource type: Other
   ```

   **Contributors:**
   ```
   Type: Hosting institution
   Name: Literaturarchiv Salzburg, Paris Lodron Universität Salzburg

   Type: Data collector
   Name: GAMS, Universität Graz
   ```

4. **Save Draft**
   - Click "Save draft" (do not publish yet)
   - Note the Deposit ID

---

### Step 2: Create Second Deposit (Essays/Aufsätze)

Repeat Step 1 with these changes:

**Upload File:**
- `stefan-zweig-digital-aufsatz-v1.0.0.tar.gz`

**Title:**
- Stefan Zweig Digital - Essays Collection (v1.0.0)

**Description:**
```
This archive contains the Essays (Aufsätze) collection from the Stefan Zweig Digital project -
essays and articles by Stefan Zweig from the archive at Literaturarchiv Salzburg.

**Collection:** Essays/Aufsätze (625 objects, ~4.7 GB)
**Part of:** Stefan Zweig Digital Complete Archive (4 volumes, v1.0.0)

[... rest similar to Facsimiles ...]
```

**Related Identifiers:**
- Update "Is derived from" to: `https://gams.uni-graz.at/context:szd.facsimiles.aufsatz`

**Keywords:** Add "Essays" instead of "Manuscripts", "Facsimiles"

---

### Step 3: Create Third Deposit (Life Documents)

**Upload File:**
- `stefan-zweig-digital-lebensdokumente-v1.0.0.tar.gz`

**Title:**
- Stefan Zweig Digital - Life Documents Collection (v1.0.0)

**Description:**
```
This archive contains the Life Documents (Lebensdokumente) collection from the Stefan Zweig Digital
project - biographical materials from the Stefan Zweig archive at Literaturarchiv Salzburg.

**Collection:** Life Documents/Lebensdokumente (127 objects, ~3.5 GB)
**Part of:** Stefan Zweig Digital Complete Archive (4 volumes, v1.0.0)

[... rest similar ...]
```

**Related Identifiers:**
- Update "Is derived from" to: `https://gams.uni-graz.at/context:szd.facsimiles.lebensdokumente`

---

### Step 4: Create Fourth Deposit (Correspondence)

**Upload File:**
- `stefan-zweig-digital-korrespondenzen-v1.0.0.tar.gz`

**Title:**
- Stefan Zweig Digital - Correspondence Collection (v1.0.0)

**Description:**
```
This archive contains the Correspondence (Korrespondenzen) collection from the Stefan Zweig Digital
project - letters and correspondence from the Stefan Zweig archive at Literaturarchiv Salzburg.

**Collection:** Correspondence/Korrespondenzen (1,186 objects, ~5.7 GB)
**Part of:** Stefan Zweig Digital Complete Archive (4 volumes, v1.0.0)

[... rest similar ...]
```

**Related Identifiers:**
- Update "Is derived from" to: `https://gams.uni-graz.at/context:szd.facsimiles.korrespondenzen`

---

### Step 5: Link All Deposits Together

After creating all 4 deposits (in draft), link them:

**For EACH deposit, add Related Identifiers:**

1. **Facsimiles deposit:**
   ```
   Relation: Is supplement to
   Identifier: [DOI of Essays deposit]

   Relation: Is supplement to
   Identifier: [DOI of Life Documents deposit]

   Relation: Is supplement to
   Identifier: [DOI of Correspondence deposit]
   ```

2. **Essays deposit:**
   ```
   Relation: Is supplement to
   Identifier: [DOI of Facsimiles deposit]

   Relation: Is supplement to
   Identifier: [DOI of Life Documents deposit]

   Relation: Is supplement to
   Identifier: [DOI of Correspondence deposit]
   ```

3. **Life Documents deposit:**
   ```
   Relation: Is supplement to
   Identifier: [DOI of Facsimiles deposit]

   Relation: Is supplement to
   Identifier: [DOI of Essays deposit]

   Relation: Is supplement to
   Identifier: [DOI of Correspondence deposit]
   ```

4. **Correspondence deposit:**
   ```
   Relation: Is supplement to
   Identifier: [DOI of Facsimiles deposit]

   Relation: Is supplement to
   Identifier: [DOI of Essays deposit]

   Relation: Is supplement to
   Identifier: [DOI of Life Documents deposit]
   ```

**Note:** You can use the Concept DOI (without version) for permanent linking.

---

### Step 6: Publish All Deposits

1. Review each deposit carefully
2. Check all metadata is consistent
3. Verify files uploaded correctly
4. Publish all 4 deposits

**Important:** Once published, you cannot delete, only create new versions.

---

## After Publishing

### 1. Collect All DOIs

Create a file with all DOIs:

```
Facsimiles:        https://doi.org/10.5281/zenodo.XXXXXXX
Essays:            https://doi.org/10.5281/zenodo.YYYYYYY
Life Documents:    https://doi.org/10.5281/zenodo.ZZZZZZZ
Correspondence:    https://doi.org/10.5281/zenodo.AAAAAAA

Concept DOIs (version-independent):
Facsimiles:        https://doi.org/10.5281/zenodo.XXXXXXX
Essays:            https://doi.org/10.5281/zenodo.YYYYYYY
Life Documents:    https://doi.org/10.5281/zenodo.ZZZZZZZ
Correspondence:    https://doi.org/10.5281/zenodo.AAAAAAA
```

### 2. Update Documentation

Update these files with the actual DOIs:

- [ ] `README.md` - Update DOI badges
- [ ] `DOCUMENTATION.md` - Update all DOI references
- [ ] `CITATION.cff` - Update DOI fields
- [ ] `docs/SPLIT_ARCHIVES.md` - Add DOI table
- [ ] `CHANGELOG.md` - Update release notes

**Example update for README.md:**

```markdown
## 📦 Complete Archive on Zenodo

The Stefan Zweig Digital archive is available as 4 separate collections on Zenodo:

| Collection | Objects | Size | Zenodo DOI |
|------------|---------|------|------------|
| **Facsimiles** | 169 | 9.3 GB | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX) |
| **Essays** | 625 | 4.7 GB | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.YYYYYYY.svg)](https://doi.org/10.5281/zenodo.YYYYYYY) |
| **Life Documents** | 127 | 3.5 GB | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.ZZZZZZZ.svg)](https://doi.org/10.5281/zenodo.ZZZZZZZ) |
| **Correspondence** | 1,186 | 5.7 GB | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.AAAAAAA.svg)](https://doi.org/10.5281/zenodo.AAAAAAA) |
```

### 3. Update CITATION.cff

```yaml
# Add all 4 DOIs as identifiers
identifiers:
  - type: doi
    value: 10.5281/zenodo.XXXXXXX
    description: "Facsimiles Collection"
  - type: doi
    value: 10.5281/zenodo.YYYYYYY
    description: "Essays Collection"
  - type: doi
    value: 10.5281/zenodo.ZZZZZZZ
    description: "Life Documents Collection"
  - type: doi
    value: 10.5281/zenodo.AAAAAAA
    description: "Correspondence Collection"
```

### 4. Create GitHub Release

1. Commit and push all documentation updates
2. Create GitHub release tagged `v1.0.0`
3. Link to all 4 Zenodo deposits in release notes

---

## Verification Checklist

After uploading, verify:

- [ ] All 4 archives uploaded successfully
- [ ] File sizes match expectations
- [ ] All metadata fields filled correctly
- [ ] ORCIDs for all creators present
- [ ] License is CC-BY 4.0 for all
- [ ] Keywords consistent across deposits
- [ ] Related identifiers link all 4 deposits
- [ ] GND and Wikidata IDs present
- [ ] Version numbers all v1.0.0
- [ ] All deposits published
- [ ] DOIs collected and documented
- [ ] Documentation updated with DOIs
- [ ] CITATION.cff updated
- [ ] GitHub release created

---

## Troubleshooting

### Upload Timeout

If uploads timeout:
- Try during off-peak hours
- Use Zenodo's chunked upload (API)
- Check network stability

### Missing Metadata Fields

Zenodo requires:
- Upload type
- Publication date
- Title
- At least one creator
- License

### Related Identifiers Not Linking

- Verify DOI format correct
- Use Concept DOI for version-independent links
- Allow time for Zenodo to process links

### Cannot Edit Published Deposit

- Create a new version
- Update metadata in new version
- Publish new version

---

## Alternative: Create Zenodo Community

Consider creating a Zenodo Community:

1. **Create Community:** "Stefan Zweig Digital Archive"
2. **Add all 4 deposits** to the community
3. **Benefits:**
   - Unified landing page
   - Easier discovery
   - Grouped citations

---

## Future Versions

When creating v1.0.1, v1.1.0, etc.:

1. Upload new archives to existing deposits (creates new version)
2. Zenodo automatically creates new version DOI
3. Concept DOI remains the same
4. Update documentation with new version DOIs

---

**Document Version:** 1.0
**Last Updated:** 2025-10-23
**Related:** [SPLIT_ARCHIVES.md](SPLIT_ARCHIVES.md)
