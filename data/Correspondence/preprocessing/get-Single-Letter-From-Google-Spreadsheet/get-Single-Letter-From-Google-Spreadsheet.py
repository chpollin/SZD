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
    "ITA": "Italian",  # Assuming ITA is the same as IT
    "ES": "Spanish",
    "ESP": "Spanish"  # Assuming ESP is the same as ES
}



# SZ_LAS_Freud: https://docs.google.com/spreadsheets/d/15fcpWsuX9-VWjx2WswwgYheDYsY4iKHWMK70idPq5qk/edit#gid=0
# SZ-SAM/AK-Meingast_Ansichtskarten: https://docs.google.com/spreadsheets/d/15s3Hipu6dznhaFo5xWAEb4gYMKOCVVYJwUpJNy_dYTE/edit#gid=0

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '15s3Hipu6dznhaFo5xWAEb4gYMKOCVVYJwUpJNy_dYTE'
SAMPLE_RANGE_NAME = 'A2:AO294'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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
    tei_listBibl = ET.Element('listBibl')
   
    if not values:
        print('No data found.')
    else:
        #print(values)
        for index, row in enumerate(values):
            # 491 = Freud
            # ansichtskarten = SZ-SAM/AK-Meingast_Ansichtskarten
            biblFull = ET.SubElement(tei_listBibl, "biblFull", {"xml:id": "SZDKOR.ansichtskarten." + str(index+1)})  # PID at index 0

            # Create nested elements based on the spreadsheet data
            fileDesc = ET.SubElement(biblFull, "fileDesc")
            titleStmt = ET.SubElement(fileDesc, "titleStmt")
            ET.SubElement(titleStmt, "title", {"xml:lang": "de"}).text = row[10]  # 'Art/Umfang' in German
            ET.SubElement(titleStmt, "title", {"xml:lang": "en"}).text = row[11]  # 'Physical Description' in English

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
                ET.SubElement(textLang, "lang", {"xml:lang": "de"}).text = language_mapping_de.get(row[23])
                ET.SubElement(textLang, "lang", {"xml:lang": "en"}).text = language_mapping_en .get(row[23])
            else:
                ET.SubElement(textLang, "lang", {"xml:lang": "de"}).text = "Deutsch"
                ET.SubElement(textLang, "lang", {"xml:lang": "en"}).text = "German"
            
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
            '''
            provenance = ET.SubElement(history, "provenance")
            ET.SubElement(provenance, "ab", {"xml:lang": "de"}).text = "Archiv Atrium Press"
            ET.SubElement(provenance, "ab", {"xml:lang": "en"}).text = "Atrium Press"
            '''

            # Add acquisition information
            acquisition = ET.SubElement(history, "acquisition")
            ET.SubElement(acquisition, "ab", {"xml:lang": "de"}).text = row[33]  # Text in German
            ET.SubElement(acquisition, "ab", {"xml:lang": "en"}).text = row[34]




    # Write the XML to a file
    #ET.ElementTree(tei_listBibl).write('extractedSZDKOR-single.xml', encoding="UTF-8", xml_declaration=True)

    # Instead of writing directly to a file, first convert to a string
    tree_str = ET.tostring(tei_listBibl, encoding='utf-8')

    # Use minidom to parse the string
    dom = minidom.parseString(tree_str)

    # Pretty-print with indentation (e.g., "\t" for tab)
    pretty_xml_as_string = dom.toprettyxml(indent="\t")

    # Write the pretty-printed XML to a file
    with open('extractedSZDKOR-single.txt', 'w', encoding="UTF-8") as output_file:
        output_file.write(pretty_xml_as_string)
              
if __name__ == '__main__':
    main()
    
    
