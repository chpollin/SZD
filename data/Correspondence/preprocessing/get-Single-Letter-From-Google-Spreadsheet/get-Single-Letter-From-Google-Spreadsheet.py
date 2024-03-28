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
def create_tei_header(safe_author_name):
    teiHeader = ET.Element("teiHeader")
    fileDesc = ET.SubElement(teiHeader, "fileDesc")
    
    # Title Statement
    titleStmt = ET.SubElement(fileDesc, "titleStmt")
    title = ET.SubElement(titleStmt, "title")
    title.text = f"{safe_author_name}"
    
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
    title.text = "Stefan Zweig digitale"
    
    # Projektleitung
    respStmt_leitung = ET.SubElement(seriesStmt, "respStmt")
    ET.SubElement(respStmt_leitung, "resp").text = "Projektleitung"
    persName_leitung = ET.SubElement(respStmt_leitung, "persName")
    ET.SubElement(persName_leitung, "forename").text = "Manfred"
    ET.SubElement(persName_leitung, "surname").text = "Mittermayer"
    
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

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '15s3Hipu6dznhaFo5xWAEb4gYMKOCVVYJwUpJNy_dYTE'
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
        groups = df.groupby('Verfasser*in')
        print(groups)

        for author_name, group in groups:
            #print(author_name)
            if "Unbekannt" in author_name:
                safe_author_name = "Unknown"
            else:
                safe_author_name = author_name.replace(' ', '-').replace(',', '').replace('/', '_')



            dir_name = os.path.join("../../byName", f"{safe_author_name}")
            
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)


            file_path = os.path.join(dir_name, f"{safe_author_name}.xml")

 
            # Initialize the root of your XML document and add TEI namespace
            TEI = ET.Element("TEI")
            TEI.set("xmlns", "http://www.tei-c.org/ns/1.0")
            # Create and add the TEI header for this record
            teiHeader = create_tei_header(safe_author_name)
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
                normalized_date = parse_date(row[18])
                ET.SubElement(titleStmt, "title", {"xml:lang": "de"}).text = row[2] + " an " + row[6] + ", " + normalized_date
                ET.SubElement(titleStmt, "title", {"xml:lang": "en"}).text = row[2] + " to " + row[6] + ", " + normalized_date

                publicationStmt = ET.SubElement(fileDesc, "publicationStmt")
                ET.SubElement(publicationStmt, "ab").text = "Einzelbrief"

                sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
                msDesc = ET.SubElement(sourceDesc, "msDesc")
                msIdentifier = ET.SubElement(msDesc, "msIdentifier")
                ET.SubElement(msIdentifier, "country").text = "Österreich"  # Static text
                ET.SubElement(msIdentifier, "settlement").text = "Salzburg"  # Static text
                repository = ET.SubElement(msIdentifier, "repository", {"ref": row[30]})
                repository.text = "Literaturarchiv Salzburg"  # Static text
                ET.SubElement(msIdentifier, "idno", {"type": "signature"}).text = row[31]
                altIdentifier1 = ET.SubElement(msIdentifier, "altIdentifier")
                ET.SubElement(altIdentifier1, "idno", {"type": "PID"}).text = row[0]  # PID value
                altIdentifier2 = ET.SubElement(msIdentifier, "altIdentifier")
                ET.SubElement(altIdentifier2, "idno", {"type": "context"}).text = row[1]

                # msContents
                msContents = ET.SubElement(msDesc, "msContents")
                textLang = ET.SubElement(msContents, "textLang")
                if row[23]:
                    ET.SubElement(textLang, "lang", {"xml:lang": row[23].lower()}).text = language_mapping_de.get(row[23])
                    ET.SubElement(textLang, "lang", {"xml:lang": row[23].lower()}).text = language_mapping_en .get(row[23])
                else:
                    ET.SubElement(textLang, "lang", {"xml:lang": "ger"}).text = "Deutsch"
                    ET.SubElement(textLang, "lang", {"xml:lang": "ger"}).text = "German"
                
                # physDesc
                physDesc = ET.SubElement(msDesc, "physDesc")
                objectDesc = ET.SubElement(physDesc, "objectDesc")
                supportDesc = ET.SubElement(objectDesc, "supportDesc")
                support = ET.SubElement(supportDesc, "support")
                if row[24]: 
                    ET.SubElement(support, "material", {"ana": "szdg:WritingMaterial", "xml:lang": "de"}).text = row[24]  # 'Beschreibstoff' in German
                if row[25]:
                    ET.SubElement(support, "material", {"ana": "szdg:WritingMaterial", "xml:lang": "en"}).text = row[25]  # 'Writing Material' in English
                if row[26]:
                    ET.SubElement(support, "material", {"ana": "szdg:WritingInstrument", "xml:lang": "de"}).text = row[26]  # 'Schreibstoff' in German
                if row[27]:
                    ET.SubElement(support, "material", {"ana": "szdg:WritingInstrument", "xml:lang": "en"}).text = row[27]  # 'Writing Instrument' in English

                extent = ET.SubElement(supportDesc, "extent")
                if row[10]:
                    ET.SubElement(extent, "span", {"xml:lang": "de"}).text = row[10]  # 'Art/Umfang' in German
                if row[11]:
                    ET.SubElement(extent, "span", {"xml:lang": "en"}).text = row[11]  # 'Physical Description' in English
                if row[29]:
                    ET.SubElement(extent, "measure", {"type": "format"}).text = row[29]  # 'Maße'

                if row[28]:
                    handDesc = ET.SubElement(physDesc, "handDesc")
                    ET.SubElement(handDesc, "ab", {"xml:lang": "de"}).text = row[28]  # Static text
                    ET.SubElement(handDesc, "ab", {"xml:lang": "en"}).text = row[28]  # Static text

                profileDesc = ET.SubElement(biblFull, "profileDesc")

                # Create 'correspDesc' element
                correspDesc = ET.SubElement(profileDesc, "correspDesc", {"type": "byZweig"})

                # Create 'correspAction' for the sender (Verfasser*in)
                correspActionSent = ET.SubElement(correspDesc, "correspAction", {"type": "sent"})
                if row[2]:
                    if row[3]:  # 'Verfasser*in GND'
                        persNameSent = ET.SubElement(correspActionSent, "persName", {"ref": row[3]})  # 'Verfasser*in GND'
                    else:
                        persNameSent = ET.SubElement(correspActionSent, "persName")
                    if ',' in row[2]:  # Check if the name contains a comma
                        surname, forename = row[2].split(", ")
                        ET.SubElement(persNameSent, "surname").text = surname
                        ET.SubElement(persNameSent, "forename").text = forename
                    else:
                        ET.SubElement(persNameSent, "name").text = row[2]  # If no comma, entire content as surname

                if row[4]:
                    orgNameSent = ET.SubElement(correspActionSent, "orgName", {"ref": row[5]})  # 'Körperschaft Verfasser*in'
                    orgNameSent.text = row[4]

                if row[14]:  # 'Datierung Original'
                    ET.SubElement(correspActionSent, "date", {"xml:lang": "de", "when": row[18]}).text = row[14]
                
                if row[15]:  # 'Date original'
                    ET.SubElement(correspActionSent, "date", {"xml:lang": "en", "when": row[18]}).text = row[14]
                
                if row[16]:  # 'Datierung erschlossen'
                    ET.SubElement(correspActionSent, "date", {"ana": "supplied/verified", "when": row[18]}).text = row[16]

                # Handling 'Entstehungsort Original' and 'Entstehungsort erschlossen'
                if row[20]:  # 'Entstehungsort Original'
                    ET.SubElement(correspActionSent, "placeName", {"type": "original"}).text = row[20]

                if row[21]:  # 'Entstehungsort erschlossen'
                    ET.SubElement(correspActionSent, "placeName", {"ana": "supplied/verified"}).text = row[21]

                # Create 'correspAction' for the receiver (Adressat*in)
                correspActionReceived = ET.SubElement(correspDesc, "correspAction", {"type": "received"})
                persNameReceived = ET.SubElement(correspActionReceived, "persName", {"ref": row[7]})  # 'Adressat*in GND'
                if ',' in row[6]:  # Similarly for receiver
                    surname, forename = row[6].split(", ")
                    ET.SubElement(persNameReceived, "surname").text = surname
                    ET.SubElement(persNameReceived, "forename").text = forename
                else:
                    ET.SubElement(persNameReceived, "name").text = row[6]

                # Handling 'Poststempel' (Postal Stamp)
                if row[19]:  # Assuming 'Poststempel' is in column 19
                    ET.SubElement(correspActionSent, "note", {"type": "postalStamp"}).text = row[19]

                # Handling 'Postanschrift' (Postal Address)
                if row[22]:  # Assuming 'Postanschrift' is in column 22
                    address = ET.SubElement(correspActionSent, "address")
                    ET.SubElement(address, "addrLine").text = row[22]



                history = ET.SubElement(msDesc, "history")
                # Add provenance information
                
                #provenance = ET.SubElement(history, "provenance")
                #ET.SubElement(provenance, "ab", {"xml:lang": "de"}).text = "Archiv Atrium Press"
                #ET.SubElement(provenance, "ab", {"xml:lang": "en"}).text = "Atrium Press"

                # Add acquisition information
                acquisition = ET.SubElement(history, "acquisition")
                ET.SubElement(acquisition, "ab", {"xml:lang": "de"}).text = row[33]  # Text in German
                ET.SubElement(acquisition, "ab", {"xml:lang": "en"}).text = row[34]
        

            # Using ElementTree to write the XML document
            tree = ET.ElementTree(TEI)
            tree.write(file_path, encoding="UTF-8", xml_declaration=True)
            
            print(f"XML file saved at: {file_path}")

              
if __name__ == '__main__':
    main()
    
    
