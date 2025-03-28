import requests
import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import os
from datetime import datetime
import unicodedata

def fetch_xml_data(url):
    """Fetch XML data from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_xml_to_dict(xml_content):
    """Parse XML content into a Python dictionary."""
    if xml_content is None:
        return []
    
    # Parse XML
    root = ET.fromstring(xml_content)
    
    # Define namespace
    ns = {'sparql': 'http://www.w3.org/2001/sw/DataAccess/rf1/result'}
    
    # Extract results
    results = []
    for result in root.findall('.//sparql:result', ns):
        item = {}
        for child in result:
            tag = child.tag.split('}')[-1]
            if child.get('uri'):
                item[tag] = child.get('uri')
            elif child.get('bound') == 'false':
                item[tag] = None
            else:
                item[tag] = child.text
        results.append(item)
    
    return results

def group_by_correspondent(records):
    """Group records by correspondent (contributor if from Zweig, creator if to Zweig)."""
    grouped = defaultdict(list)
    
    for record in records:
        creator = record.get('creator')
        contributor = record.get('contributor')
        
        # If Stefan Zweig is the creator, group by contributor (recipient)
        if creator and "Zweig, Stefan" in creator and contributor:
            grouped[contributor].append(record)
        # If someone else is the creator, group by creator (they sent to Zweig)
        elif creator and "Zweig, Stefan" not in creator:
            grouped[creator].append(record)
        # Edge case: if no contributor but Zweig is creator, skip or group separately
        elif creator and "Zweig, Stefan" in creator:
            # Skip these or handle differently if needed
            pass
    
    return grouped

def extract_dates(records):
    """Extract earliest and latest dates from records."""
    dates = []
    
    for record in records:
        date = record.get('date')
        if date:
            # Try to extract year from date field
            year_match = re.search(r'(\d{4})', date)
            if year_match:
                dates.append(int(year_match.group(1)))
        
        # If no date field or no year found, try title
        if not date or not year_match:
            title = record.get('title', '')
            year_matches = re.findall(r'(\d{4})', title)
            if year_matches:
                dates.extend([int(year) for year in year_matches])
    
    if dates:
        return min(dates), max(dates)
    return None, None

def determine_correspondence_direction(records):
    """Determine if correspondence is to or from Zweig."""
    # Check the first record to determine direction
    if records:
        creator = records[0].get('creator')
        if creator and "Zweig, Stefan" in creator:
            return "fromZweig"
        else:
            return "toZweig"
    
    # Default if we can't determine
    return "toZweig"

def extract_signatures(records, debug=False, correspondent_name=""):
    """Extract signatures from records and create konvolut signature."""
    signatures = {}
    konvolut_signature = ""
    
    if debug:
        print(f"\nDEBUG: Extracting signatures for {correspondent_name} ({len(records)} records)")
    
    for i, record in enumerate(records):
        title = record.get('title', '')
        # Extract signature after the last comma in the title
        last_comma_pos = title.rfind(',')
        if last_comma_pos != -1 and last_comma_pos < len(title) - 1:
            # Get everything after the last comma and trim whitespace
            full_signature = title[last_comma_pos + 1:].strip()
            
            # Extract konvolut signature (remove number after last dot or dash)
            base_signature_match = re.search(r'(SZ-[A-Za-z0-9]+/[A-Za-z0-9]+)[\.|\-]?\d*', full_signature)
            
            if base_signature_match:
                base_signature = base_signature_match.group(1)
                
                # Add to signatures dict, counting occurrences
                signatures[base_signature] = signatures.get(base_signature, 0) + 1
                
                if debug and i < 5:  # Show first few for debugging
                    print(f"  Record {i+1}: '{title}'")
                    print(f"    Full signature: '{full_signature}'")
                    print(f"    Base signature: '{base_signature}'")
    
    # Use the most common signature as the konvolut signature
    if signatures:
        if debug:
            print(f"  All signatures found: {signatures}")
        
        # Find most common signature
        konvolut_signature = max(signatures, key=signatures.get)
        
        if debug:
            print(f"  Selected konvolut signature: '{konvolut_signature}' (found {signatures[konvolut_signature]} times)")
    else:
        if debug:
            print("  No valid signatures found in records")
    
    return konvolut_signature, list(signatures.keys())

def is_person(name):
    """Determine if a name is a person (has surname, forename structure) or organization."""
    return ',' in name

def parse_name(person):
    """Parse person name into surname and forename."""
    if person is None:
        return "", ""
    
    if ',' in person:
        surname, forename = person.split(',', 1)
        return surname.strip(), forename.strip()
    else:
        # If no comma, assume organization name
        return person.strip(), ""

def format_name_for_id(name):
    """Format a name for use in IDs, handling special characters and umlauts."""
    if name is None:
        return ""
    
    # Normalize unicode characters (convert accented to non-accented)
    # NFD splits characters into base character and diacritical marks, then strip diacritical marks
    normalized = unicodedata.normalize('NFD', name)
    name_without_accents = ''.join([c for c in normalized if not unicodedata.combining(c)])
    
    # Replace German umlauts explicitly (in case they're not decomposed by NFD)
    name_without_accents = name_without_accents.replace('ä', 'a').replace('ö', 'o').replace('ü', 'u')
    name_without_accents = name_without_accents.replace('Ä', 'A').replace('Ö', 'O').replace('Ü', 'U').replace('ß', 'ss')
    
    # Convert to lowercase
    name_without_accents = name_without_accents.lower()
    
    # Replace spaces and commas with hyphens
    name_without_accents = re.sub(r'[,\s]+', '-', name_without_accents)
    
    # Remove any remaining non-alphanumeric chars except hyphen
    name_without_accents = re.sub(r'[^a-z0-9\-]', '', name_without_accents)
    
    # Remove duplicate hyphens
    name_without_accents = re.sub(r'\-+', '-', name_without_accents)
    
    # Remove trailing hyphens
    name_without_accents = name_without_accents.rstrip('-')
    
    return name_without_accents

def generate_konvolut_id(correspondent):
    """Generate Konvolut ID for altIdentifier."""
    formatted_name = format_name_for_id(correspondent)
    return f"o:szd.korrespondenzen.{formatted_name}"

def generate_context_id(correspondent):
    """Generate context ID for altIdentifier."""
    formatted_name = format_name_for_id(correspondent)
    return f"context:szd.facsimiles.korrespondenzen#{formatted_name}"

def generate_konvolut_element(creator_id, correspondent, records, debug=False):
    """Generate TEI XML biblFull element for a Konvolut."""
    surname, forename = parse_name(correspondent)
    from_date, to_date = extract_dates(records)
    direction = determine_correspondence_direction(records)
    count = len(records)
    
    # Extract signatures
    konvolut_signature, individual_signatures = extract_signatures(records, debug, correspondent)
    
    # Generate the IDs
    konvolut_id = generate_konvolut_id(correspondent)
    context_id = generate_context_id(correspondent)
    
    # Create XML structure
    biblFull = ET.Element('biblFull')
    biblFull.set('xml:id', f"SZDKOR.{creator_id}")
    
    # File description
    fileDesc = ET.SubElement(biblFull, 'fileDesc')
    
    # Title statement
    titleStmt = ET.SubElement(fileDesc, 'titleStmt')
    
    if direction == "fromZweig":
        title_de = f"{count} Korrespondenzstücke VON Stefan Zweig"
        title_en = f"{count} Pieces of Correspondence FROM Stefan Zweig"
    else:
        title_de = f"{count} Korrespondenzstücke AN Stefan Zweig"
        title_en = f"{count} Pieces of Correspondence TO Stefan Zweig"
    
    title_de_elem = ET.SubElement(titleStmt, 'title')
    title_de_elem.set('xml:lang', 'de')
    title_de_elem.text = title_de
    
    title_en_elem = ET.SubElement(titleStmt, 'title')
    title_en_elem.set('xml:lang', 'en')
    title_en_elem.text = title_en
    
    # Publication statement
    publicationStmt = ET.SubElement(fileDesc, 'publicationStmt')
    ab = ET.SubElement(publicationStmt, 'ab')
    ab.text = "Briefkonvolut"
    
    # Source description
    sourceDesc = ET.SubElement(fileDesc, 'sourceDesc')
    msDesc = ET.SubElement(sourceDesc, 'msDesc')
    
    # Repository info as specified
    msIdentifier = ET.SubElement(msDesc, 'msIdentifier')
    country = ET.SubElement(msIdentifier, 'country')
    country.text = "Österreich"
    settlement = ET.SubElement(msIdentifier, 'settlement')
    settlement.text = "Salzburg"
    repository = ET.SubElement(msIdentifier, 'repository')
    repository.text = "Literaturarchiv Salzburg"
    repository.set('ref', "http://d-nb.info/gnd/1047605287")
    
    # Add signature if available
    idno = ET.SubElement(msIdentifier, 'idno')
    idno.set('type', 'signature')
    if konvolut_signature:
        idno.text = konvolut_signature
    
    # Add altIdentifier for context
    altIdentifier1 = ET.SubElement(msIdentifier, 'altIdentifier')
    context_idno = ET.SubElement(altIdentifier1, 'idno')
    context_idno.set('type', 'context')
    context_idno.text = context_id
    
    # Add altIdentifier for konvolut
    altIdentifier2 = ET.SubElement(msIdentifier, 'altIdentifier')
    konvolut_idno = ET.SubElement(altIdentifier2, 'idno')
    konvolut_idno.set('type', 'konvolut')
    konvolut_idno.text = konvolut_id
    
    # Physical description
    physDesc = ET.SubElement(msDesc, 'physDesc')
    objectDesc = ET.SubElement(physDesc, 'objectDesc')
    supportDesc = ET.SubElement(objectDesc, 'supportDesc')
    extent = ET.SubElement(supportDesc, 'extent')
    measure = ET.SubElement(extent, 'measure')
    measure.set('type', 'correspondence')
    measure.set('unit', 'piece')
    
    if direction == "fromZweig":
        measure.set('subtype', 'sent')
    else:
        measure.set('subtype', 'received')
    
    measure.text = str(count)
    
    # Profile description
    profileDesc = ET.SubElement(biblFull, 'profileDesc')
    correspDesc = ET.SubElement(profileDesc, 'correspDesc')
    correspDesc.set('type', direction)
    
    # Correspondence action - sent
    correspAction_sent = ET.SubElement(correspDesc, 'correspAction')
    correspAction_sent.set('type', 'sent')
    
    persName_sent = ET.SubElement(correspAction_sent, 'persName')
    
    if direction == "fromZweig":
        # Zweig is the sender if direction is fromZweig
        persName_sent.set('ref', "http://d-nb.info/gnd/118637479")  # Zweig's GND
        surname_elem = ET.SubElement(persName_sent, 'surname')
        surname_elem.text = "Zweig"
        forename_elem = ET.SubElement(persName_sent, 'forename')
        forename_elem.text = "Stefan"
    else:
        # The correspondent is the sender if direction is toZweig
        persName_sent.set('ref', "http://d-nb.info/gnd/placeholder")
        
        if is_person(correspondent):
            # For persons, use surname and forename
            surname_elem = ET.SubElement(persName_sent, 'surname')
            surname_elem.text = surname
            
            if forename:
                forename_elem = ET.SubElement(persName_sent, 'forename')
                forename_elem.text = forename
        else:
            # For organizations, use name
            name_elem = ET.SubElement(persName_sent, 'name')
            name_elem.text = correspondent
    
    # Add date if available
    if from_date and to_date and from_date == to_date:
        # Single year
        date = ET.SubElement(correspAction_sent, 'date')
        date.set('when', str(from_date))
        date.set('xml:lang', 'en')
        date.text = str(from_date)
    elif from_date and to_date:
        # Date range
        date = ET.SubElement(correspAction_sent, 'date')
        date.set('from', str(from_date))
        date.set('to', str(to_date))
        date.set('xml:lang', 'en')
        date.text = f"{from_date}-{to_date}"
    
    # Correspondence action - received
    correspAction_received = ET.SubElement(correspDesc, 'correspAction')
    correspAction_received.set('type', 'received')
    
    persName_received = ET.SubElement(correspAction_received, 'persName')
    
    if direction == "fromZweig":
        # The correspondent is the receiver if direction is fromZweig
        persName_received.set('ref', "http://d-nb.info/gnd/placeholder")
        
        if is_person(correspondent):
            # For persons, use surname and forename
            surname_elem = ET.SubElement(persName_received, 'surname')
            surname_elem.text = surname
            
            if forename:
                forename_elem = ET.SubElement(persName_received, 'forename')
                forename_elem.text = forename
        else:
            # For organizations, use name
            name_elem = ET.SubElement(persName_received, 'name')
            name_elem.text = correspondent
    else:
        # Zweig is the receiver if direction is toZweig
        persName_received.set('ref', "http://d-nb.info/gnd/118637479")  # Zweig's GND
        surname_elem = ET.SubElement(persName_received, 'surname')
        surname_elem.text = "Zweig"
        forename_elem = ET.SubElement(persName_received, 'forename')
        forename_elem.text = "Stefan"
    
    return biblFull

def generate_combined_konvolute(grouped_records, start_id=680, output_file="combined_konvolute.xml", debug=False):
    """Generate a single XML file with all Konvolute in a listBibl."""
    # Create root element
    root = ET.Element('TEI')
    root.set('xmlns', 'http://www.tei-c.org/ns/1.0')
    
    # Create teiHeader
    teiHeader = ET.SubElement(root, 'teiHeader')
    fileDesc = ET.SubElement(teiHeader, 'fileDesc')
    
    # Title statement
    titleStmt = ET.SubElement(fileDesc, 'titleStmt')
    title = ET.SubElement(titleStmt, 'title')
    title.text = "Stefan Zweig Digital - Korrespondenz Konvolute"
    
    # Publication statement
    publicationStmt = ET.SubElement(fileDesc, 'publicationStmt')
    publisher = ET.SubElement(publicationStmt, 'publisher')
    publisher.text = "Stefan Zweig Digital"
    pubPlace = ET.SubElement(publicationStmt, 'pubPlace')
    pubPlace.text = "Salzburg, Austria"
    date = ET.SubElement(publicationStmt, 'date')
    date.text = datetime.now().strftime("%Y-%m-%d")
    
    # Source description
    sourceDesc = ET.SubElement(fileDesc, 'sourceDesc')
    p = ET.SubElement(sourceDesc, 'p')
    p.text = "Generated from GAMS repository data"
    
    # Create text and body elements
    text = ET.SubElement(root, 'text')
    body = ET.SubElement(text, 'body')
    
    # Create listBibl to contain all biblFull elements
    listBibl = ET.SubElement(body, 'listBibl')
    
    # Counter for processed items
    processed = 0
    creator_id = start_id
    
    # Process each correspondent's records
    for correspondent, records in grouped_records.items():
        biblFull = generate_konvolut_element(creator_id, correspondent, records, debug)
        listBibl.append(biblFull)
        processed += len(records)
        creator_id += 1
    
    # Pretty-print the XML
    ET.indent(root, space="  ")
    
    # Write to file
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    
    return output_file, processed, len(grouped_records)

def print_all_titles(records, max_count=10):
    """Print all titles from records for debugging."""
    print(f"Showing up to {max_count} titles:")
    for i, record in enumerate(records[:max_count]):
        print(f"  {i+1}. {record.get('title', 'No title')}")
    if len(records) > max_count:
        print(f"  ... and {len(records) - max_count} more")

def main():
    url = "https://gams.uni-graz.at/archive/risearch?type=tuples&lang=sparql&format=Sparql&query=http://fedora:8380/archive/get/context:szd.facsimiles.korrespondenzen/QUERY"
    
    print("Fetching correspondence data...")
    xml_content = fetch_xml_data(url)
    
    if xml_content:
        records = parse_xml_to_dict(xml_content)
        print(f"Successfully parsed {len(records)} records.")
        
        # Group by correspondent (not by creator)
        print("Grouping records by correspondent...")
        grouped = group_by_correspondent(records)
        print(f"Found {len(grouped)} unique correspondents.")
        
        # Show examples for verification with enhanced debugging
        examples = ["Bazalgette, Léon", "Fleischer, Max", "Köhler, Richard"]
        
        for example in examples:
            if example in grouped:
                print(f"\n=== Detailed check for {example} ===")
                example_records = grouped[example]
                print(f"Found {len(example_records)} letters")
                
                # Print special character handling test
                original_name = example
                formatted_name = format_name_for_id(example)
                print(f"Original name: '{original_name}'")
                print(f"Formatted for ID: '{formatted_name}'")
                
                # Generate IDs
                konvolut_id = generate_konvolut_id(example)
                context_id = generate_context_id(example)
                print(f"Generated konvolut ID: {konvolut_id}")
                print(f"Generated context ID: {context_id}")
                
                # Extract signatures
                konvolut_signature, individual_signatures = extract_signatures(
                    example_records, debug=True, correspondent_name=example
                )
        
        # Generate combined konvolute file
        print("\nGenerating combined Konvolute file...")
        output_file = "konvolute.xml"
        
        # Pass debug=False for the final output
        filename, total_items, total_correspondents = generate_combined_konvolute(
            grouped, start_id=680, output_file=output_file, debug=False
        )
        
        # Print summary
        print("\nKonvolute generation complete!")
        print(f"Created combined file: {filename}")
        print(f"Includes {total_correspondents} Konvolute with IDs starting from SZDKOR.680")
        print(f"Total correspondence pieces processed: {total_items}/{len(records)}")
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    main()