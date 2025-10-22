#!/usr/bin/env python3
"""
Script to download METS metadata and images from Stefan Zweig Digital archive.
Downloads objects from GAMS archive with rate limiting and resume capability.

TEST MODE: Downloads 10 objects from each container for testing.
Set TEST_MODE = False to download all objects.
"""

import requests
import time
import os
import json
import logging
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple

# ============================================================================
# CONFIGURATION
# ============================================================================

# Test mode: Only download first 10 objects from each container
TEST_MODE = False
TEST_OBJECTS_PER_CONTAINER = 10

# Directories
METADATA_DIR = Path("metadata")
DATA_DIR = Path("data")
LOGS_DIR = Path("logs")

# API URLs
METS_URL_TEMPLATE = "https://gams.uni-graz.at/archive/get/{object_id}/METS_SOURCE"
IMAGE_URL_TEMPLATE = "http://gams.uni-graz.at/{object_id}/{image_id}"

# Rate limiting
DELAY_BETWEEN_REQUESTS = 1.5  # seconds
DELAY_BETWEEN_OBJECTS = 2.0   # seconds

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Logging
LOG_LEVEL = logging.INFO

# Container mapping for folder structure
CONTAINER_FOLDERS = {
    "szd.facsimiles": "facsimiles",
    "szd.facsimiles.aufsatz": "aufsatz",
    "szd.facsimiles.lebensdokumente": "lebensdokumente",
    "szd.facsimiles.korrespondenzen": "korrespondenzen"
}

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging():
    """Configure logging to file and console."""
    LOGS_DIR.mkdir(exist_ok=True)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter('%(message)s')

    # File handler
    log_file = LOGS_DIR / f"download_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(console_formatter)

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger, log_file

# ============================================================================
# PROGRESS TRACKING
# ============================================================================

class ProgressTracker:
    """Track download progress and enable resume capability."""

    def __init__(self, progress_file: Path):
        self.progress_file = progress_file
        self.data = self._load()

    def _load(self) -> Dict:
        """Load progress from file."""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "started": datetime.now().isoformat(),
            "last_updated": None,
            "containers": {},
            "statistics": {
                "total_objects": 0,
                "completed_objects": 0,
                "failed_objects": 0,
                "total_images": 0,
                "downloaded_images": 0,
                "total_bytes": 0
            }
        }

    def save(self):
        """Save progress to file."""
        self.data["last_updated"] = datetime.now().isoformat()
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def is_object_completed(self, container: str, object_id: str) -> bool:
        """Check if object download is completed."""
        if container not in self.data["containers"]:
            return False
        objects = self.data["containers"][container].get("objects", {})
        return objects.get(object_id, {}).get("status") == "completed"

    def mark_object_started(self, container: str, object_id: str):
        """Mark object download as started."""
        if container not in self.data["containers"]:
            self.data["containers"][container] = {"objects": {}}
        if "objects" not in self.data["containers"][container]:
            self.data["containers"][container]["objects"] = {}

        self.data["containers"][container]["objects"][object_id] = {
            "status": "in_progress",
            "started": datetime.now().isoformat(),
            "images_downloaded": 0,
            "errors": []
        }
        self.save()

    def mark_object_completed(self, container: str, object_id: str, image_count: int, bytes_downloaded: int):
        """Mark object download as completed."""
        if container in self.data["containers"] and object_id in self.data["containers"][container]["objects"]:
            self.data["containers"][container]["objects"][object_id].update({
                "status": "completed",
                "completed": datetime.now().isoformat(),
                "images_downloaded": image_count,
                "bytes": bytes_downloaded
            })
            self.data["statistics"]["completed_objects"] += 1
            self.data["statistics"]["downloaded_images"] += image_count
            self.data["statistics"]["total_bytes"] += bytes_downloaded
            self.save()

    def mark_object_failed(self, container: str, object_id: str, error: str):
        """Mark object download as failed."""
        if container in self.data["containers"] and object_id in self.data["containers"][container]["objects"]:
            self.data["containers"][container]["objects"][object_id]["status"] = "failed"
            self.data["containers"][container]["objects"][object_id]["errors"].append({
                "time": datetime.now().isoformat(),
                "error": str(error)
            })
            self.data["statistics"]["failed_objects"] += 1
            self.save()

# ============================================================================
# HTTP UTILITIES
# ============================================================================

def download_with_retry(url: str, max_retries: int = MAX_RETRIES) -> Optional[bytes]:
    """Download content with retry logic."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                logging.warning(f"  Attempt {attempt + 1} failed: {e}. Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
            else:
                logging.error(f"  Failed after {max_retries} attempts: {e}")
                return None
    return None

# ============================================================================
# METS PARSING
# ============================================================================

def parse_mets(mets_xml: bytes, object_id: str) -> Optional[Dict]:
    """Parse METS XML and extract metadata and image information."""
    try:
        root = ET.fromstring(mets_xml)

        # Define namespaces
        ns = {
            'mets': 'http://www.loc.gov/METS/',
            'mods': 'http://www.loc.gov/mods/v3',
            'xlink': 'http://www.w3.org/1999/xlink',
            'dv': 'http://dfg-viewer.de/',
            'exif': 'http://ns.adobe.com/exif/1.0/'
        }

        metadata = {
            "object_id": object_id,
            "title": None,
            "signature": None,
            "author": None,
            "language": None,
            "language_code": None,
            "owner": None,
            "rights": None,
            "images": []
        }

        # Extract MODS metadata
        mods = root.find('.//mods:mods', ns)
        if mods is not None:
            # Title
            title_elem = mods.find('.//mods:title', ns)
            if title_elem is not None:
                metadata["title"] = title_elem.text

            # Signature
            signature_elem = mods.find('.//mods:note[@type="signature"]', ns)
            if signature_elem is not None:
                metadata["signature"] = signature_elem.text

            # Author
            author_elem = mods.find('.//mods:name[@type="personal"]/mods:displayForm', ns)
            if author_elem is not None:
                metadata["author"] = author_elem.text

            # Language
            lang_text_elem = mods.find('.//mods:languageTerm[@type="text"]', ns)
            if lang_text_elem is not None:
                metadata["language"] = lang_text_elem.text

            lang_code_elem = mods.find('.//mods:languageTerm[@type="code"]', ns)
            if lang_code_elem is not None:
                metadata["language_code"] = lang_code_elem.text

        # Extract rights information
        owner_elem = root.find('.//dv:owner', ns)
        if owner_elem is not None:
            metadata["owner"] = owner_elem.text
            # Extract rights from owner text if present
            if "CC-BY" in (owner_elem.text or ""):
                metadata["rights"] = "CC-BY"

        # Extract images
        for file_elem in root.findall('.//mets:file[@MIMETYPE="image/jpeg"]', ns):
            file_id = file_elem.get('ID')
            if not file_id or not file_id.startswith('IMG.'):
                continue

            # Get image URL
            flocat = file_elem.find('.//mets:FLocat', ns)
            if flocat is None:
                continue

            image_url = flocat.get('{http://www.w3.org/1999/xlink}href')

            # Get dimensions
            width = None
            height = None
            width_elem = file_elem.find('.//exif:PixelXDimension', ns)
            height_elem = file_elem.find('.//exif:PixelYDimension', ns)
            if width_elem is not None:
                width = int(width_elem.text)
            if height_elem is not None:
                height = int(height_elem.text)

            # Get order from structMap
            order = None
            for div in root.findall(f'.//mets:div[@TYPE="page"]', ns):
                fptr = div.find(f'.//mets:fptr[@FILEID="{file_id}"]', ns)
                if fptr is not None:
                    order = div.get('ORDER')
                    break

            metadata["images"].append({
                "id": file_id,
                "url": image_url,
                "width": width,
                "height": height,
                "order": int(order) if order else None
            })

        # Sort images by order
        metadata["images"].sort(key=lambda x: x["order"] if x["order"] else 999)

        return metadata

    except ET.ParseError as e:
        logging.error(f"  Failed to parse METS XML: {e}")
        return None

# ============================================================================
# DOWNLOAD FUNCTIONS
# ============================================================================

def download_object(object_id: str, container: str, progress: ProgressTracker) -> bool:
    """Download METS and all images for a single object."""

    # Skip if already completed
    if progress.is_object_completed(container, object_id):
        logging.info(f"  [SKIP] {object_id} - already completed")
        return True

    logging.info(f"\n  Downloading: {object_id}")
    progress.mark_object_started(container, object_id)

    # Create object directory
    folder_name = CONTAINER_FOLDERS[container]
    object_folder = DATA_DIR / folder_name / object_id.replace(":", "_")
    object_folder.mkdir(parents=True, exist_ok=True)
    images_folder = object_folder / "images"
    images_folder.mkdir(exist_ok=True)

    # Download METS
    mets_url = METS_URL_TEMPLATE.format(object_id=object_id)
    logging.info(f"    Downloading METS...")
    mets_content = download_with_retry(mets_url)

    if mets_content is None:
        progress.mark_object_failed(container, object_id, "Failed to download METS")
        return False

    # Save METS
    mets_file = object_folder / "mets.xml"
    with open(mets_file, 'wb') as f:
        f.write(mets_content)
    logging.info(f"    [OK] METS saved ({len(mets_content)} bytes)")

    time.sleep(DELAY_BETWEEN_REQUESTS)

    # Parse METS
    metadata = parse_mets(mets_content, object_id)
    if metadata is None:
        progress.mark_object_failed(container, object_id, "Failed to parse METS")
        return False

    # Save metadata JSON
    metadata["container"] = container
    metadata["download_date"] = datetime.now().isoformat()
    metadata_file = object_folder / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    logging.info(f"    Title: {metadata.get('title', 'N/A')}")
    logging.info(f"    Images: {len(metadata['images'])} files")

    # Download images
    total_bytes = 0
    downloaded_count = 0

    for i, image_info in enumerate(metadata['images'], 1):
        image_id = image_info['id']
        image_url = image_info['url']

        # Generate filename with padded number
        image_filename = f"{image_id.replace('.', '_')}.jpg"
        image_path = images_folder / image_filename

        # Skip if already exists
        if image_path.exists():
            existing_size = image_path.stat().st_size
            logging.info(f"    [{i}/{len(metadata['images'])}] {image_id} - already exists ({existing_size} bytes)")
            total_bytes += existing_size
            downloaded_count += 1
            continue

        # Download image
        logging.info(f"    [{i}/{len(metadata['images'])}] Downloading {image_id}...")
        image_content = download_with_retry(image_url)

        if image_content is None:
            logging.warning(f"    [WARN] Failed to download {image_id}")
            continue

        # Save image
        with open(image_path, 'wb') as f:
            f.write(image_content)

        total_bytes += len(image_content)
        downloaded_count += 1
        logging.info(f"    [OK] {image_id} ({len(image_content)} bytes)")

        # Rate limiting
        if i < len(metadata['images']):
            time.sleep(DELAY_BETWEEN_REQUESTS)

    # Mark as completed
    progress.mark_object_completed(container, object_id, downloaded_count, total_bytes)
    logging.info(f"  [COMPLETED] {object_id} - {downloaded_count} images, {total_bytes:,} bytes")

    return True

# ============================================================================
# MAIN DOWNLOAD LOGIC
# ============================================================================

def load_object_ids() -> Dict[str, List[str]]:
    """Load object IDs from metadata XML files."""
    object_ids = {}

    for container, folder in CONTAINER_FOLDERS.items():
        xml_file = METADATA_DIR / f"context_{container.replace('.', '_')}.xml"

        if not xml_file.exists():
            logging.warning(f"Metadata file not found: {xml_file}")
            continue

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            ns = {'sparql': 'http://www.w3.org/2001/sw/DataAccess/rf1/result'}

            pids = []
            for pid_elem in root.findall('.//sparql:pid', ns):
                uri = pid_elem.get('uri')
                if uri and 'o:szd.' in uri:
                    object_id = uri.split('/')[-1]
                    if object_id not in pids:  # Avoid duplicates
                        pids.append(object_id)

            object_ids[container] = pids
            logging.info(f"Loaded {len(pids)} objects from {container}")

        except Exception as e:
            logging.error(f"Error loading {xml_file}: {e}")

    return object_ids

def main():
    """Main download function."""

    # Setup
    logger, log_file = setup_logging()

    print("=" * 70)
    print("Stefan Zweig Digital - Archive Download")
    print("=" * 70)
    print()

    if TEST_MODE:
        print(f"[TEST MODE] Downloading {TEST_OBJECTS_PER_CONTAINER} objects per container")
        print()

    # Create directories
    DATA_DIR.mkdir(exist_ok=True)
    for folder in CONTAINER_FOLDERS.values():
        (DATA_DIR / folder).mkdir(exist_ok=True)

    # Initialize progress tracker
    progress_file = LOGS_DIR / "download_progress.json"
    progress = ProgressTracker(progress_file)

    # Load object IDs
    logging.info("Loading object IDs from metadata files...")
    object_ids = load_object_ids()

    if not object_ids:
        logging.error("No object IDs loaded. Please run fetch_metadata.py first.")
        return

    # Calculate totals
    total_objects = sum(len(ids) for ids in object_ids.values())
    if TEST_MODE:
        total_objects = min(total_objects, len(object_ids) * TEST_OBJECTS_PER_CONTAINER)

    progress.data["statistics"]["total_objects"] = total_objects
    progress.save()

    print()
    print(f"Total objects to download: {total_objects}")
    print(f"Log file: {log_file}")
    print(f"Progress file: {progress_file}")
    print()
    print("=" * 70)

    # Download objects
    start_time = time.time()

    for container, ids in object_ids.items():
        folder_name = CONTAINER_FOLDERS[container]

        # Limit objects in test mode
        if TEST_MODE:
            ids = ids[:TEST_OBJECTS_PER_CONTAINER]

        logging.info(f"\n{'=' * 70}")
        logging.info(f"Container: {container} ({len(ids)} objects)")
        logging.info(f"Folder: data/{folder_name}/")
        logging.info(f"{'=' * 70}")

        for idx, object_id in enumerate(ids, 1):
            logging.info(f"\n[{idx}/{len(ids)}] Processing {object_id}")

            try:
                download_object(object_id, container, progress)
            except Exception as e:
                logging.error(f"  [ERROR] Unexpected error: {e}")
                progress.mark_object_failed(container, object_id, str(e))

            # Delay between objects
            if idx < len(ids):
                time.sleep(DELAY_BETWEEN_OBJECTS)

    # Summary
    elapsed_time = time.time() - start_time
    stats = progress.data["statistics"]

    print()
    print("=" * 70)
    print("DOWNLOAD COMPLETED")
    print("=" * 70)
    print(f"Total time: {elapsed_time:.1f} seconds ({elapsed_time/60:.1f} minutes)")
    print(f"Objects completed: {stats['completed_objects']}/{stats['total_objects']}")
    print(f"Objects failed: {stats['failed_objects']}")
    print(f"Images downloaded: {stats['downloaded_images']}")
    print(f"Total data: {stats['total_bytes']:,} bytes ({stats['total_bytes']/1024/1024:.1f} MB)")
    print()
    print(f"Log file: {log_file}")
    print(f"Progress file: {progress_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()
