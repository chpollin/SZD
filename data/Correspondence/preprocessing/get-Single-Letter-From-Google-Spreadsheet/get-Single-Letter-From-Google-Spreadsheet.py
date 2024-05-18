from __future__ import print_function
from glob import escape
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import xml.etree.ElementTree as ET
import urllib.request
import pandas as pd
import validators
from xml.dom import minidom
from datetime import datetime
import re
import unicodedata

language_mapping_de = {
    "GER": "Deutsch",
    "EN": "Englisch",
    "FRA": "Französisch",
    "IT": "Italienisch",
    "ITA": "Italienisch",
    "ES": "Spanisch",
    "ESP": "Spanisch"
}
language_mapping_en = {
    "GER": "German",
    "EN": "English",
    "FRA": "French",
    "IT": "Italian",
    "ITA": "Italian",
    "ES": "Spanish",
    "ESP": "Spanish"
}

def parse_date(date_str):
    """
    Attempt to parse a date string and return it in the format "TT.MM.JJJJ", or the most specific format available.
    Handles cases where the date might not include the day or even the month.
    """
    # Try parsing with day, month, and year
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            # If the date includes only the year, format it as such. Otherwise, use the full date.
            if fmt == "%Y":
                return parsed_date.strftime("%Y")
            elif fmt == "%Y-%m":
                return parsed_date.strftime("%m.%Y")
            else:
                return parsed_date.strftime("%d.%m.%Y")
        except ValueError:
            pass  # Try the next format
    return "Unknown Date"  # Return a placeholder or raise an error if no formats matched


# Function to create and return a TEI header element
def create_tei_header(author_name, safe_author_name):
    teiHeader = ET.Element("teiHeader")
    fileDesc = ET.SubElement(teiHeader, "fileDesc")
    
    # Title Statement
    titleStmt = ET.SubElement(fileDesc, "titleStmt")
    author_parts = author_name.split(", ")
    if len(author_parts) == 2:
        surname, forename = author_parts
    else:
        forename = author_name
        surname = ""

    ET.SubElement(titleStmt, "title", {"xml:lang": "de"}).text = f"Korrespondenz {forename} {surname}"
    ET.SubElement(titleStmt, "title", {"xml:lang": "en"}).text = f"Correspondence {forename} {surname}"
    
    # Publication Statement
    publicationStmt = ET.SubElement(fileDesc, "publicationStmt")
    # Publisher
    publisher = ET.SubElement(publicationStmt, "publisher")
    orgName_publisher = ET.SubElement(publisher, "orgName", {
        "corresp": "https://www.uni-salzburg.at/index.php?id=72",
        "ref": "d-nb.info/gnd/1047605287"
    })
    orgName_publisher.text = "Literaturarchiv Salzburg"
    # More publicationStmt subelements follow similarly...

    # ID Number
    idno = ET.SubElement(publicationStmt, "idno", {"type": "PID"})
    
    idno.text = f"o:szd.korrespondenzen.{safe_author_name}"
       # Encoding Description
    encodingDesc = ET.SubElement(teiHeader, "encodingDesc")
    editorialDecl = ET.SubElement(encodingDesc, "editorialDecl")
    ET.SubElement(editorialDecl, "p").text = "Jeder Einzelbrief wird durch ein biblFull beschrieben."
    projectDesc = ET.SubElement(encodingDesc, "projectDesc")
    ET.SubElement(projectDesc, "p").text = ("Das Projekt verfolgt das Ziel, den weltweit verstreuten Nachlass von Stefan Zweig "
                                             "im digitalen Raum zusammenzuführen und ihn einem literaturwissenschaftlich bzw. "
                                             "wissenschaftlich interessierten Publikum zu erschließen. In Zusammenarbeit mit "
                                             "dem Literaturarchiv der Universität Salzburg wird dabei, basierend auf dem dort "
                                             "vorhandenen Quellenmaterial, eine digitale Nachlassrekonstruktion des Bestandes "
                                             "generiert. So entsteht ein strukturierter Bestand an digitalen Objekten, der im "
                                             "Sinne der digitalen Langzeitarchivierung repräsentiert wird, und NutzerInnen "
                                             "orts- und zeitunabhängig zugänglich ist. Das Projekt ist so konzipiert, dass zu "
                                             "einem späteren Zeitpunkt Erschließung und Anreicherung des Quellenmaterials "
                                             "(z.B. digitalen Editionen) möglich werden.")
    listPrefixDef = ET.SubElement(encodingDesc, "listPrefixDef")
    prefixDef = ET.SubElement(listPrefixDef, "prefixDef", ident="szdg", matchPattern="([(a-z)|(A-Z)]+)", replacementPattern="szdg:$1")
    ET.SubElement(prefixDef, "p").text = "Namespace für den Glossar in Stefan Zweig digital."

    # Series Statement
    seriesStmt = ET.SubElement(fileDesc, "seriesStmt")
    title = ET.SubElement(seriesStmt, "title", ref="https://gams.uni-graz.at/szd")
    title.text = "Stefan Zweig digital"
    
    # Projektleitung
    respStmt_leitung = ET.SubElement(seriesStmt, "respStmt")
    ET.SubElement(respStmt_leitung, "resp").text = "Projektleitung"
    persName_leitung = ET.SubElement(respStmt_leitung, "persName")
    ET.SubElement(persName_leitung, "forename").text = "Lina Maria"
    ET.SubElement(persName_leitung, "surname").text = "Zangerl"
    
    # Datenerfassung
    respStmt_erfassung = ET.SubElement(seriesStmt, "respStmt")
    ET.SubElement(respStmt_erfassung, "resp").text = "Datenerfassung"
    persName_erfassung1 = ET.SubElement(respStmt_erfassung, "persName")
    ET.SubElement(persName_erfassung1, "forename").text = "Oliver"
    ET.SubElement(persName_erfassung1, "surname").text = "Matuschek"
    persName_erfassung2 = ET.SubElement(respStmt_erfassung, "persName")
    ET.SubElement(persName_erfassung2, "forename").text = "Julia"
    ET.SubElement(persName_erfassung2, "surname").text = "Glunk"
    
    # Datenmodellierung
    respStmt_modellierung = ET.SubElement(seriesStmt, "respStmt")
    ET.SubElement(respStmt_modellierung, "resp").text = "Datenmodellierung"
    persName_modellierung = ET.SubElement(respStmt_modellierung, "persName")
    ET.SubElement(persName_modellierung, "forename").text = "Christopher"
    ET.SubElement(persName_modellierung, "surname").text = "Pollin"
    
    # Source Description
    sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
    p = ET.SubElement(sourceDesc, "p")
    p.text = "Korrespondenzen Stefan Zweig"

    return teiHeader



# SZ_LAS_Freud: https://docs.google.com/spreadsheets/d/15fcpWsuX9-VWjx2WswwgYheDYsY4iKHWMK70idPq5qk/edit#gid=0
# SZ-SAM/AK-Meingast_Ansichtskarten: https://docs.google.com/spreadsheets/d/15s3Hipu6dznhaFo5xWAEb4gYMKOCVVYJwUpJNy_dYTE/edit#gid=0

Freud = '15fcpWsuX9-VWjx2WswwgYheDYsY4iKHWMK70idPq5qk'
Ansichtskarten = '15s3Hipu6dznhaFo5xWAEb4gYMKOCVVYJwUpJNy_dYTE'

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = Ansichtskarten
SAMPLE_RANGE_NAME = 'A1:AO294'

def main():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    
    sheet = service.spreadsheets()
    
    
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    # select data in tab "Beruf_Tätigkeit"
    SAMPLE_RANGE_NAME_corr_by_zweig = "'Einzelbriefe'!A2:AM49"
    
   
    if not values:
        print('No data found.')
    else:

        headers = values[0]
        data_rows = values[1:]
        df = pd.DataFrame(data_rows, columns=headers)
        verfasser_values = df['Verfasser*in'].unique()
        groups = df.groupby('Verfasser*in')
        if len(verfasser_values) == 1 and verfasser_values[0] == "Zweig, Stefan":
            groups = df.groupby('Adressat*in')

        total_members_count = 0

        for author_name, group in groups:
            total_members_count = len(group)
            #print(author_name)
            if "Unbekannt" in author_name:
                safe_author_name = "Unknown"
            safe_author_name = author_name.replace(' ', '-').replace(',', '').replace('/', '_').replace('?', '').replace('.', '')
            safe_author_name= re.sub(r'[()<>:"/\\|\?*].', '', safe_author_name)
            if safe_author_name.endswith('-') or safe_author_name.endswith('-()') or safe_author_name.endswith('-(') or safe_author_name.endswith(')'):
                safe_author_name = safe_author_name[:-1]

            # Corrected line: use 'safe_author_name' instead of 's'
            safe_author_name = unicodedata.normalize('NFD', safe_author_name)
            # Encode to ASCII bytes, ignoring errors, then decode back to string
            safe_author_name = safe_author_name.encode('ascii', 'ignore').decode('ascii')
            # Convert to lowercase
            safe_author_name = safe_author_name.lower()
                        
            #print(safe_author_name)



            dir_name = os.path.join("../../byName", f"{safe_author_name}")
            
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)


            file_path = os.path.join(dir_name, f"{safe_author_name}.xml")

            main_dir_name = os.path.join("../../byName", f"{safe_author_name}")
            os.makedirs(main_dir_name, exist_ok=True)

  


 
            # Initialize the root of your XML document and add TEI namespace
            TEI = ET.Element("TEI")
            TEI.set("xmlns", "http://www.tei-c.org/ns/1.0")
            # Create and add the TEI header for this record
            teiHeader = create_tei_header(author_name, safe_author_name)
            TEI.append(teiHeader)
            text = ET.Element("text")
            TEI.append(text)
            body = ET.Element("body")
            text.append(body)
            tei_listBibl = ET.Element('listBibl')
            body.append(tei_listBibl)
            

            for index, row in group.iterrows():
                biblFull = ET.SubElement(tei_listBibl, "biblFull", {"xml:id": f"SZDKOR.{safe_author_name}." + str(index+1)})  # PID at index 0

                # Create nested elements based on the spreadsheet data
                fileDesc = ET.SubElement(biblFull, "fileDesc")
                titleStmt = ET.SubElement(fileDesc, "titleStmt")
                # [Verfasser] an [Empfänger], [Datierung normalisiert – aber angezeigt als TT.MM.JJJJ] 
                normalized_date = parse_date(row.iloc[18])
                ET.SubElement(titleStmt, "title", {"xml:lang": "de"}).text = row.iloc[2] + " an " + row.iloc[6] + ", " + normalized_date
                ET.SubElement(titleStmt, "title", {"xml:lang": "en"}).text = row.iloc[2] + " to " + row.iloc[6] + ", " + normalized_date

                publicationStmt = ET.SubElement(fileDesc, "publicationStmt")
                ET.SubElement(publicationStmt, "ab").text = "Einzelbrief"

                sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
                msDesc = ET.SubElement(sourceDesc, "msDesc")
                msIdentifier = ET.SubElement(msDesc, "msIdentifier")
                ET.SubElement(msIdentifier, "country").text = "Österreich"  # Static text
                ET.SubElement(msIdentifier, "settlement").text = "Salzburg"  # Static text
                repository = ET.SubElement(msIdentifier, "repository", {"ref": row.iloc[30]})
                repository.text = "Literaturarchiv Salzburg"  # Static text
                ET.SubElement(msIdentifier, "idno", {"type": "signature"}).text = row.iloc[31]
                altIdentifier1 = ET.SubElement(msIdentifier, "altIdentifier")
                ET.SubElement(altIdentifier1, "idno", {"type": "PID"}).text = "o:szd." + str(3100 + index)  # PID value
                altIdentifier2 = ET.SubElement(msIdentifier, "altIdentifier")
                ET.SubElement(altIdentifier2, "idno", {"type": "context"}).text = row.iloc[1]

                # msContents
                msContents = ET.SubElement(msDesc, "msContents")
                textLang = ET.SubElement(msContents, "textLang")
                if row.iloc[23]:
                    #ET.SubElement(textLang, "lang", {"xml:lang": row.iloc[23].lower()}).text = language_mapping_de.get(row.iloc[23])
                    ET.SubElement(textLang, "lang", {"xml:lang": row.iloc[23].lower()}).text = language_mapping_en.get(row.iloc[23])
                else:
                    #ET.SubElement(textLang, "lang", {"xml:lang": "ger"}).text = "Deutsch"
                    ET.SubElement(textLang, "lang", {"xml:lang": "ger"}).text = "German"
                
                # physDesc
                physDesc = ET.SubElement(msDesc, "physDesc")
                objectDesc = ET.SubElement(physDesc, "objectDesc")
                supportDesc = ET.SubElement(objectDesc, "supportDesc")
                support = ET.SubElement(supportDesc, "support")
                if row.iloc[24]: 
                    ET.SubElement(support, "material", {"ana": "szdg:WritingMaterial", "xml:lang": "de"}).text = row.iloc[24]  # 'Beschreibstoff' in German
                if row.iloc[25]:
                    ET.SubElement(support, "material", {"ana": "szdg:WritingMaterial", "xml:lang": "en"}).text = row.iloc[25]  # 'Writing Material' in English
                if row.iloc[26]:
                    ET.SubElement(support, "material", {"ana": "szdg:WritingInstrument", "xml:lang": "de"}).text = row.iloc[26]  # 'Schreibstoff' in German
                if row.iloc[27]:
                    ET.SubElement(support, "material", {"ana": "szdg:WritingInstrument", "xml:lang": "en"}).text = row.iloc[27]  # 'Writing Instrument' in English

                extent = ET.SubElement(supportDesc, "extent")
                if row.iloc[10]:
                    ET.SubElement(extent, "span", {"xml:lang": "de"}).text = row.iloc[10]  # 'Art/Umfang' in German
                if row.iloc[11]:
                    ET.SubElement(extent, "span", {"xml:lang": "en"}).text = row.iloc[11]  # 'Physical Description' in English
                if row.iloc[29]:
                    ET.SubElement(extent, "measure", {"type": "format"}).text = row.iloc[29]  # 'Maße'

                if row.iloc[28]:
                    handDesc = ET.SubElement(physDesc, "handDesc")
                    ET.SubElement(handDesc, "ab", {"xml:lang": "de"}).text = row.iloc[28]  # Static text
                    ET.SubElement(handDesc, "ab", {"xml:lang": "en"}).text = row.iloc[28]  # Static text

                profileDesc = ET.SubElement(biblFull, "profileDesc")

                # Create 'correspDesc' element
                correspDesc = ET.SubElement(profileDesc, "correspDesc", {"type": "toZweig"})

                # Create 'correspAction' for the sender (Verfasser*in)
                correspActionSent = ET.SubElement(correspDesc, "correspAction", {"type": "sent"})
                if row.iloc[2]:
                    if row.iloc[3]:  # 'Verfasser*in GND'
                        persNameSent = ET.SubElement(correspActionSent, "persName", {"ref": row.iloc[3]})  # 'Verfasser*in GND'
                    else:
                        persNameSent = ET.SubElement(correspActionSent, "persName")
                    if ',' in row.iloc[2]:  # Check if the name contains a comma
                        surname, forename = row.iloc[2].split(", ")
                        ET.SubElement(persNameSent, "surname").text = surname
                        ET.SubElement(persNameSent, "forename").text = forename
                    else:
                        ET.SubElement(persNameSent, "name").text = row.iloc[2]  # If no comma, entire content as surname

                if row.iloc[4]:
                    orgNameSent = ET.SubElement(correspActionSent, "orgName", {"ref": row.iloc[5]})  # 'Körperschaft Verfasser*in'
                    orgNameSent.text = row.iloc[4]

                if row.iloc[14]:  # 'Datierung Original'
                    ET.SubElement(correspActionSent, "date", {"xml:lang": "de", "when": row.iloc[18]}).text = row.iloc[14]
                
                if row.iloc[15]:  # 'Date original'
                    ET.SubElement(correspActionSent, "date", {"xml:lang": "en", "when": row.iloc[18]}).text = row.iloc[14]
                
                if row.iloc[16]:  # 'Datierung erschlossen'
                    ET.SubElement(correspActionSent, "date", {"ana": "supplied/verified", "when": row.iloc[18]}).text = row.iloc[16]

                # Handling 'Entstehungsort Original' and 'Entstehungsort erschlossen'
                if row.iloc[20]:  # 'Entstehungsort Original'
                    ET.SubElement(correspActionSent, "placeName", {"type": "original"}).text = row.iloc[20]

                if row.iloc[21]:  # 'Entstehungsort erschlossen'
                    ET.SubElement(correspActionSent, "placeName", {"ana": "supplied/verified"}).text = row.iloc[21]

                # Create 'correspAction' for the receiver (Adressat*in)
                correspActionReceived = ET.SubElement(correspDesc, "correspAction", {"type": "received"})
                persNameReceived = ET.SubElement(correspActionReceived, "persName", {"ref": row.iloc[7]})  # 'Adressat*in GND'
                if ',' in row.iloc[6]:  # Similarly for receiver
                    surname, forename = row.iloc[6].split(", ")
                    ET.SubElement(persNameReceived, "surname").text = surname
                    ET.SubElement(persNameReceived, "forename").text = forename
                else:
                    ET.SubElement(persNameReceived, "name").text = row.iloc[6]

                # Handling 'Poststempel' (Postal Stamp)
                if row.iloc[19]:
                    ET.SubElement(correspActionSent, "note", {"type": "postalStamp"}).text = row.iloc[19]

                # Handling 'Postanschrift' (Postal Address)
                if row.iloc[22]:
                    address = ET.SubElement(correspActionSent, "address")
                    ET.SubElement(address, "addrLine").text = row.iloc[22]



                history = ET.SubElement(msDesc, "history")
                # Add provenance information
                
                #provenance = ET.SubElement(history, "provenance")
                #ET.SubElement(provenance, "ab", {"xml:lang": "de"}).text = "Archiv Atrium Press"
                #ET.SubElement(provenance, "ab", {"xml:lang": "en"}).text = "Atrium Press"

                # Add acquisition information
                acquisition = ET.SubElement(history, "acquisition")
                ET.SubElement(acquisition, "ab", {"xml:lang": "de"}).text = row.iloc[33]  # Text in German
                ET.SubElement(acquisition, "ab", {"xml:lang": "en"}).text = row.iloc[34]
        

            
##########################################
                ### Create the "scans" subdirectory
                # Be careful not to overwrite anything!
                scans_dir_name = os.path.join(main_dir_name, "scans")
                os.makedirs(scans_dir_name, exist_ok=True)
                # Create and populate the "{name}-scans.xml" document in the "scans" subfolder
                scans_file_path = os.path.join(scans_dir_name, f"{safe_author_name}-scans.xml")

                # Define namespaces
                NS = {
                    '': 'http://gams.uni-graz.at/viewer',  # Default namespace
                    'xlink': 'http://www.w3.org/1999/xlink'
                }
                ET.register_namespace('', NS[''])
                ET.register_namespace('xlink', NS['xlink'])

                # Extract and prepare author name and signature
                author_name = row['Verfasser*in']
                surname, forename = author_name.split(", ") if ", " in author_name else (author_name, "")

                date = row['Datierung normalisiert']  # Assuming date is correctly formatted
                signature = row['Signatur']
                normalized_signature = re.sub(r'[<>:"/\\|?*]', '', signature)
                normalized_signature = normalized_signature.replace(" ", "_").replace(".", "_")[:50]
                # SZ-SAM/AK.1 - SZ_SAM_AK.1
                folder_name = signature.replace("-", "_").replace("/", "_")
                print(f"Processing {folder_name}...")

                # Define base directory and ensure it exists
                base_dir_name = r"C:\Users\pollin\Documents\GitHub\SZD\data\Scans\KulturerbeDigital\SZ_SAM_Ansichtskarten"
                author_dir_name = os.path.join(base_dir_name, folder_name)
                os.makedirs(author_dir_name, exist_ok=True)  # Ensures the directory exists without raising an error if it already does

                # Full path for the XML file
                scans_file_path = os.path.join(author_dir_name, f"{normalized_signature}-scans.xml")

                # Create the XML structure
                root_book = ET.Element("book", {"xmlns": NS[''], "xmlns:xlink": NS['xlink'], "xmlns:file": "http://expath.org/ns/file"})
                ET.SubElement(root_book, "title").text = f"{forename} {surname} an Stefan Zweig, {date}, {signature}"
                ET.SubElement(root_book, "author").text = f"{surname}, {forename}"
                ET.SubElement(root_book, "date").text = parse_date(date)  # Normalized
                ET.SubElement(root_book, "category").text = "Ansichtskarte"
                ET.SubElement(root_book, "idno").text = "o:szd." + str(3100 + index)

                owner_element = ET.SubElement(root_book, "owner")
                name_element = ET.Element("name")
                name_element.text = "Literaturarchiv Salzburg, https://stefanzweig.digital, CC-BY"
                owner_element.append(name_element)

                structure = ET.SubElement(root_book, "structure")
                for title, frm in [("Bildseite", "1"), ("Adressseite", "2"), ("Farbreferenz", "3")]:
                    div = ET.SubElement(structure, "div", {"type": title})
                    ET.SubElement(div, "page", {"xlink:href": f"{folder_name}-{frm}.jpg"})

                # Writing the XML file with UTF-8 encoding and XML declaration
                tree_scans = ET.ElementTree(root_book)
                tree_scans.write(scans_file_path, encoding="UTF-8", xml_declaration=True)
                #print(f"Successfully wrote {scans_file_path}")


##########################################
            biblFull_path = os.path.join(dir_name, f"{safe_author_name}-biblFull.xml")

            biblFull = ET.Element("biblFull", {"xml:id": ""})

            # fileDesc
            fileDesc = ET.SubElement(biblFull, "fileDesc")
            titleStmt = ET.SubElement(fileDesc, "titleStmt")
            ET.SubElement(titleStmt, "title", {"xml:lang": "de"}).text = str(total_members_count) + " Korrespondenzstücke AN Stefan Zweig" 
            ET.SubElement(titleStmt, "title", {"xml:lang": "en"}).text = str(total_members_count) + " Pieces of Correspondence TO Stefan Zweig"

            publicationStmt = ET.SubElement(fileDesc, "publicationStmt")
            ET.SubElement(publicationStmt, "ab").text = "Briefkonvolut"

            # sourceDesc
            sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
            msDesc = ET.SubElement(sourceDesc, "msDesc")
            msIdentifier = ET.SubElement(msDesc, "msIdentifier")
            ET.SubElement(msIdentifier, "country").text = "Österreich"
            ET.SubElement(msIdentifier, "settlement").text = "Salzburg"
            repository = ET.SubElement(msIdentifier, "repository", {"ref": "http://d-nb.info/gnd/1047605287"})
            repository.text = "Literaturarchiv Salzburg"
            ET.SubElement(msIdentifier, "idno", {"type": "signature"}).text = ""

            altIdentifier1 = ET.SubElement(msIdentifier, "altIdentifier")
            ET.SubElement(altIdentifier1, "idno", {"type": "context"}).text = "context:szd.facsimiles.korrespondenzen#" + safe_author_name

            altIdentifier2 = ET.SubElement(msIdentifier, "altIdentifier")
            ET.SubElement(altIdentifier2, "idno", {"type": "konvolut"}).text = "o:szd.korrespondenzen." + safe_author_name

            # physDesc
            physDesc = ET.SubElement(msDesc, "physDesc")
            objectDesc = ET.SubElement(physDesc, "objectDesc")
            supportDesc = ET.SubElement(objectDesc, "supportDesc")
            extent = ET.SubElement(supportDesc, "extent")
            measure = ET.SubElement(extent, "measure", {"type": "correspondence", "unit": "piece", "subtype": "sent"})
            measure.text = str(total_members_count)

            # profileDesc
            profileDesc = ET.SubElement(biblFull, "profileDesc")
            correspDesc = ET.SubElement(profileDesc, "correspDesc", {"type": "toZweig"})
            correspAction_sent = ET.SubElement(correspDesc, "correspAction", {"type": "sent"})
            persName_sent = ET.SubElement(correspAction_sent, "persName", {"ref": ""})
            ET.SubElement(persName_sent, "surname").text = surname
            ET.SubElement(persName_sent, "forename").text = forename

            correspAction_received = ET.SubElement(correspDesc, "correspAction", {"type": "received"})
            persName_received = ET.SubElement(correspAction_received, "persName", {"ref": "http://d-nb.info/gnd/118637479"})
            ET.SubElement(persName_received, "surname").text = "Zweig"
            ET.SubElement(persName_received, "forename").text = "Stefan"

            ET.SubElement(correspAction_received, "date", {"xml:lang": "en", "from": "", "to": ""}).text = ""

            # After all sub-elements have been added, then create the ElementTree and write to the file
            tree_biblFull = ET.ElementTree(biblFull)
            tree_biblFull.write(biblFull_path, encoding="UTF-8", xml_declaration=True)


            # Using ElementTree to write the XML document
            tree = ET.ElementTree(TEI)
            tree.write(file_path, encoding="UTF-8", xml_declaration=True)
            #print(f"Successfully wrote {file_path}")


            # New directory for collected-byName-XML
            collected_dir_name = os.path.join("../../byName/collected-byName-XML")
            # Path to save the XML file in the new directory
            collected_file_path = os.path.join(collected_dir_name, f"{safe_author_name}.xml")
            tree.write(file_path, encoding="UTF-8", xml_declaration=True)
            tree.write(collected_file_path, encoding="UTF-8", xml_declaration=True)

        
              
if __name__ == '__main__':
    main()
    
    
