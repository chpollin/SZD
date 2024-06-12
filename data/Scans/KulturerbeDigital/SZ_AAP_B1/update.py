import os
import xml.etree.ElementTree as ET

# Base directory containing all the folders
base_dir = r'C:\Users\pollin\Documents\GitHub\SZD\data\Scans\KulturerbeDigital\SZ_AAP_B1'
id_counter = 3400

# Namespaces
ns = {'': 'http://gams.uni-graz.at/viewer', 'xlink': 'http://www.w3.org/1999/xlink'}

# Register namespaces
ET.register_namespace('', ns[''])
ET.register_namespace('xlink', ns['xlink'])

# Function to add <idno> element to XML
def add_idno_to_xml(file_path, id_value):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Find all <idno> elements
        idno_elements = root.findall('.//{http://gams.uni-graz.at/viewer}idno')

        # Remove all existing <idno> elements
        for idno_element in idno_elements:
            root.remove(idno_element)

        # Create new <idno> element
        idno_element = ET.Element(f'{{{ns[""]}}}idno')
        idno_element.text = f'o:szd.{id_value}'

        # Append the new <idno> element to the root element
        root.append(idno_element)

        # Save the modified XML back to the file
        tree.write(file_path, encoding='UTF-8', xml_declaration=True)

    except ET.ParseError:
        print(f"Error parsing XML file: {file_path}")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

# Function to validate page elements against image files
def validate_pages_vs_images(subfolder_path, xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Find all <page> elements
        page_elements = root.findall('.//{http://gams.uni-graz.at/viewer}page', ns)
        page_hrefs = [page.get('{http://www.w3.org/1999/xlink}href') for page in page_elements]

        # List all .jpg files in the subfolder
        jpg_files = [f for f in os.listdir(subfolder_path) if f.endswith('.jpg')]

        issues_found = False

        # Check if the number of <page> elements matches the number of .jpg files
        if len(page_elements) != len(jpg_files):
            print(f"Mismatch in number of pages and images in {subfolder_path}: {len(page_elements)} pages vs {len(jpg_files)} images")
            issues_found = True

        # Check if each <page> element href matches a .jpg file
        for href in page_hrefs:
            if href not in jpg_files:
                print(f"Image file {href} referenced in XML but not found in {subfolder_path}")
                issues_found = True

        # Check if each .jpg file has a corresponding <page> element href
        for jpg_file in jpg_files:
            if jpg_file not in page_hrefs:
                print(f"Image file {jpg_file} found in {subfolder_path} but not referenced in XML")
                issues_found = True

    except ET.ParseError:
        print(f"Error parsing XML file: {xml_file}")
    except Exception as e:
        print(f"An error occurred while validating {xml_file}: {e}")

# Iterate over each folder in the base directory
for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)

    if os.path.isdir(folder_path):
        # Check and delete any XML files in the current folder
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.xml'):
                file_path = os.path.join(folder_path, file_name)
                try:
                    os.remove(file_path)
                    print(f"Deleted {file_path}")
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")

        # Check for subfolder
        for subfolder_name in os.listdir(folder_path):
            subfolder_path = os.path.join(folder_path, subfolder_name)
            
            if os.path.isdir(subfolder_path):
                # Look for a single XML file in the subfolder
                xml_files = [f for f in os.listdir(subfolder_path) if f.endswith('.xml')]
                if len(xml_files) == 1:
                    subfile_path = os.path.join(subfolder_path, xml_files[0])
                    add_idno_to_xml(subfile_path, id_counter)
                    validate_pages_vs_images(subfolder_path, subfile_path)
                    id_counter += 1
                else:
                    print(f"Warning: Found {len(xml_files)} XML files in {subfolder_path}. Expected exactly 1.")
