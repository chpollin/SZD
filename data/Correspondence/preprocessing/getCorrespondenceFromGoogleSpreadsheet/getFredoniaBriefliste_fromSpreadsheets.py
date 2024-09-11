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
from datetime import datetime
import requests


language_mapping_de = {
    "GER": "Deutsch",
    "EN": "Englisch",
    "ENG": "Englisch",
    "FRA": "Französisch",
    "FRE": "Französisch",
    "IT": "Italienisch",
    "ITA": "Italienisch",
    "ES": "Spanisch",
    "ESP": "Spanisch"
}
language_mapping_en = {
    "GER": "German",
    "EN": "English",
    "ENG": "English",
    "FRA": "French",
    "FRE": "French",
    "IT": "Italian",
    "ITA": "Italian",
    "ES": "Spanish",
    "ESP": "Spanish"
}

# https://docs.google.com/spreadsheets/d/1VX9XBH2yQV5TygdRpWLNjkaEObuQ4Hd1eMSyIo6lgxo/edit?usp=sharing
# C2:AK274
Reichner = '19RQoTKals6woN2QGYzt2tKp6mKJpfbLUmwnnqgrLqyI'


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '19RQoTKals6woN2QGYzt2tKp6mKJpfbLUmwnnqgrLqyI'
SAMPLE_RANGE_NAME = 'A2:AK274'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the senderization flow completes for the first
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

    ## select data in tab "Beruf_Tätigkeit"
    SAMPLE_RANGE_NAME_corr_by_zweig = "C2:AK274"
    result_corr_by_zweig = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_corr_by_zweig).execute()
    values_corr_by_zweig = result_corr_by_zweig.get('values', [])
        
    
    
    tei_listBibl = ET.Element('listBibl')
   
    if not values:
        print('No data found.')
    else:
        #print(values)
        sender = ""
        receiver = ""
        for index, row in enumerate(values):
            # if the length of row is 12 (columns) than its a valid row
            if str(row[0]):
                if ", " in str(row[0]):
                    surname, firstname = str(row[0]).split(", ") 
                    sender = f"{firstname} {surname}"
            # Körperschaft Verfasser*in     
            elif str(row[2]):
                sender = str(row[2])
            
            # Adressat*in
            if str(row[4]):
                if ", " in str(row[4]):
                    receiver_surname,  receiver_firstname = str(row[4]).split(", ") 
                    receiver = f"{receiver_firstname} {receiver_surname}"
            # Körperschaft Adressat*in    
            elif str(row[6]):
                receiver = str(row[6])

            date =  str(row[16])
            signature = str(row[29])


            split_languages = [lang.strip() for lang in str(row[21]).split(';')]
                

            
            #####################
            ### <biblFull>
            tei_biblFull = ET.SubElement(tei_listBibl, 'biblFull')
            tei_biblFull.set('xml:id', "SZDKOR.reichner-herbert.B." + str(index + 1) )
            
            #####################
            #### <fileDesc> <titleStmt>
            tei_fileDesc = ET.SubElement(tei_biblFull, 'fileDesc')
            tei_titleStmt = ET.SubElement(tei_fileDesc, 'titleStmt')
            tei_title_de = ET.SubElement(tei_titleStmt, 'title') 
            tei_title_de.set('xml:lang', "de")
            tei_title_en = ET.SubElement(tei_titleStmt, 'title')
            tei_title_en.set('xml:lang', "en")

            if date:
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d.%m.%Y")

            tei_title_de.text =  sender + " an " + receiver + ", " + formatted_date
            tei_title_en.text =  sender + " to " + receiver + ", " + formatted_date

            #####################
            ### <publicationStmt>
            tei_publicationStmt = ET.SubElement(tei_fileDesc, 'publicationStmt')
            tei_ab_publicationStmt = ET.SubElement(tei_publicationStmt, 'ab')
            tei_ab_publicationStmt.text = "Einzelbrief"
            
            ###
            try:
                if row[35]:
                    tei_notesStmt = ET.SubElement(tei_fileDesc, 'notesStmt')
                    tei_note_de = ET.SubElement(tei_notesStmt, 'note')
                    tei_note_de.set('xml:lang', "de")
                    tei_note_en = ET.SubElement(tei_notesStmt, 'note')
                    tei_note_en.set('xml:lang', "en")
                    tei_note_de.text = row[35]
                    tei_note_en.text = row[36]
            except:
                pass

                
            #####################
            ### <sourceDesc>
            tei_sourceDesc = ET.SubElement(tei_fileDesc, 'sourceDesc')
            tei_msDesc = ET.SubElement(tei_sourceDesc, 'msDesc')
            tei_msIdentifier = ET.SubElement(tei_msDesc, 'msIdentifier')
            # chrildren of 
            tei_country_msIdentifier = ET.SubElement(tei_msIdentifier, 'country')
            tei_country_msIdentifier.text = "Österreich"
            tei_settlement_msIdentifier = ET.SubElement(tei_msIdentifier, 'settlement')
            tei_settlement_msIdentifier.text = "Salzburg"
            tei_repository_msIdentifier = ET.SubElement(tei_msIdentifier, 'repository')
            tei_repository_msIdentifier.text = "Literaturarchiv Salzburg"
            tei_repository_msIdentifier.set('ref', 'http://d-nb.info/gnd/1047605287')
            
            tei_idno_msIdentifier = ET.SubElement(tei_msIdentifier, 'idno')
            tei_idno_msIdentifier.set('type', 'signature')
            tei_idno_msIdentifier.text = str(signature)

           # Step 4: Extract and print <identifier> elements for each <result>
            for result in results:
                title_from_xml = result.find('ns:title', namespaces=namespace)
                signatur_from_xml = title_from_xml.text.split(',')[1].strip()
                identifier = result.find('ns:identifier', namespaces=namespace)
                if signature == signatur_from_xml:
                    tei_altIdentifier_pid = ET.SubElement(tei_msIdentifier, 'altIdentifier')
                    tei_altIdentifier_pid_idno = ET.SubElement(tei_altIdentifier_pid, 'idno')
                    tei_altIdentifier_pid_idno.set('type', 'PID')
                    tei_altIdentifier_pid_idno.text = str(identifier.text)


            # msContents
            tei_msContents = ET.SubElement(tei_msDesc, "msContents")
            tei_textLang = ET.SubElement(tei_msContents, "textLang")

            if split_languages:
                for language in split_languages:
                    if language != "GER":
                        ET.SubElement(tei_textLang, "lang", {"xml:lang": language.lower()}).text = language_mapping_en.get(language)
                        ET.SubElement(tei_textLang, "lang", {"xml:lang": language.lower()}).text = language_mapping_de.get(language)
                    else:
                        ET.SubElement(tei_textLang, "lang", {"xml:lang": "ger"}).text = "Deutsch"
                        ET.SubElement(tei_textLang, "lang", {"xml:lang": "ger"}).text = "German"

            #####################
            ### <physDesc>
            tei_physDesc = ET.SubElement(tei_msDesc, 'physDesc')
            tei_objectDesc = ET.SubElement(tei_physDesc, 'objectDesc')
            tei_supportDesc = ET.SubElement(tei_objectDesc, 'supportDesc')
            tei_support = ET.SubElement(tei_supportDesc, 'support')
            tei_extent = ET.SubElement(tei_supportDesc, 'extent')
            
            if row[22]:
                ET.SubElement(tei_support, "material", {"ana": "szdg:WritingMaterial", "xml:lang": "de"}).text = row[22]  # 'Beschreibstoff' in German
            if row[23]:
                ET.SubElement(tei_support, "material", {"ana": "szdg:WritingMaterial", "xml:lang": "en"}).text = row[23]  # 'Writing Material' in English
            if row[24]:
                ET.SubElement(tei_support, "material", {"ana": "szdg:WritingInstrument", "xml:lang": "de"}).text = row[24]  # 'Schreibstoff' in German
            if row[25]:
                ET.SubElement(tei_support, "material", {"ana": "szdg:WritingInstrument", "xml:lang": "en"}).text = row[25]  # 'Writing Instrument' in English
            
            if row[8]:
                ET.SubElement(tei_extent, "span", {"xml:lang": "de"}).text = row[8]  # 'Art/Umfang' in German
            if row[9]:
                ET.SubElement(tei_extent, "span", {"xml:lang": "en"}).text = row[9]  # 'Physical Description' in English
            if row[27]:
                ET.SubElement(tei_extent, "measure", {"type": "format"}).text = row[27]  # 'Maße'

            if(row[10]):
                tei_measure_3 = ET.SubElement(tei_extent, 'measure')
                tei_measure_3.text = row[10]
                tei_measure_3.set('type', "enclosures") 
                tei_measure_3.set('ana', "szdg:Enclosures") 
                tei_measure_3.set('xml:lang', 'de')
            if(row[11]):
                tei_measure_3 = ET.SubElement(tei_extent, 'measure')
                tei_measure_3.text = row[11]
                tei_measure_3.set('type', "enclosures")
                tei_measure_3.set('ana', "szdg:Enclosures") 
                tei_measure_3.set('xml:lang', 'en')

            if(str(row[26])):
                tei_handDesc = ET.SubElement(tei_physDesc, 'handDesc')
                tei_handDesc_ab = ET.SubElement(tei_handDesc, 'ab')
                tei_handDesc_ab.text = str(row[26])

            tei_history = ET.SubElement(tei_msDesc, 'history')
            if str(row[30]):
                tei_provenance = ET.SubElement(tei_history, 'provenance')
                tei_provenance_ab = ET.SubElement(tei_provenance, 'ab')
                tei_provenance_ab.text = row[30]
            tei_acquisition = ET.SubElement(tei_history, 'acquisition')
            if str(row[31]):
                tei_ab_de = ET.SubElement(tei_acquisition, 'ab', {"xml:lang": "de"})
                tei_ab_de.text = row[31]
            if str(row[32]):
                tei_ab_en = ET.SubElement(tei_acquisition, 'ab', {"xml:lang": "en"})
                tei_ab_en.text = row[32]

            ####  <profileDesc>    
            tei_profileDesc = ET.SubElement(tei_biblFull, 'profileDesc')

            # Parties involved | GND (Parties involved)
            try:
                if(str(row[33])):
                    tei_textClass = ET.SubElement(tei_profileDesc, 'textClass')
                    tei_keywords = ET.SubElement(tei_textClass, 'keywords')
                    tei_term = ET.SubElement(tei_keywords, 'term')
                    tei_term.set('type', 'person')
                    tei_term_persName = ET.SubElement(tei_term, 'persName')
                    if(',' in row[33]):
                        tei_term_surName = ET.SubElement(tei_term_persName, 'surname')
                        tei_term_foreName = ET.SubElement(tei_term_persName, 'forename')
                        tei_term_surName.text = row[33].split(', ')[0]
                        tei_term_foreName.text = row[33].split(', ')[1]
                    else:
                        tei_term_name = ET.SubElement(tei_term_persName, 'name')
                        tei_term_name.text = row[33]
                    if(',' in row[34]):
                        tei_term_persName.set('ref', row[34])
                    elif(row[34]):
                        tei_term_name.set('ref', row[34])     
            except:
                pass

            tei_correspDesc = ET.SubElement(tei_profileDesc, 'correspDesc')
            tei_correspDesc.set('type', 'toZweig')
           
            
            #####################
            ### correspAction_sent
            tei_correspAction_sent = ET.SubElement(tei_correspDesc, 'correspAction')
            tei_correspAction_sent.set('type', "sent")
            if row[0]:
                tei_persName_sent = ET.SubElement(tei_correspAction_sent, 'persName')
                tei_surname_sent = ET.SubElement(tei_persName_sent, 'surname')
                tei_surname_sent.text = surname
                tei_forename_sent = ET.SubElement(tei_persName_sent, 'forename')
                tei_forename_sent.text = firstname
                if(str(row[1])):  
                    tei_persName_sent.set('ref', row[1])
            if(str(row[2])):   
                tei_orgName_sent = ET.SubElement(tei_correspAction_sent, 'orgName')
                tei_orgName_sent.text = str(row[2])
                if(str(row[3])):
                    tei_orgName_sent.set('ref', row[3])
            # date
            if(str(row[12])):
                tei_date = ET.SubElement(tei_correspAction_sent, 'date')
                tei_date.text = str(row[12])
                if str(row[16]):
                    tei_date.set('when', str(row[16]))
            # palce
            if(str(row[18])):
                tei_placeName = ET.SubElement(tei_correspAction_sent, 'placeName')
                tei_placeName.text = str(row[18])

            ### correspAction_received
            if row[4] or row[6]:
                tei_correspAction_received = ET.SubElement(tei_correspDesc, 'correspAction')
                tei_correspAction_received.set('type', "received")
                if row[4]:
                    tei_persName_received = ET.SubElement(tei_correspAction_received, 'persName')
                    tei_surname_received = ET.SubElement(tei_persName_received, 'surname')
                    tei_surname_received.text = receiver_surname
                    tei_forename_received = ET.SubElement(tei_persName_received, 'forename')
                    tei_forename_received.text = receiver_firstname
                    if(str(row[5])):  
                        tei_persName_received.set('ref', row[5])
                if(str(row[6])):   
                    tei_orgName_received = ET.SubElement(tei_correspAction_received, 'orgName')
                    tei_orgName_received.text = str(row[6])
                    if(str(row[7])):
                        tei_orgName_received.set('ref', row[7])
     
    # create a new XML file with the results
    ET.ElementTree(tei_listBibl).write('extractedSZDKOR.xml', encoding="UTF-8", xml_declaration=True)
              
if __name__ == '__main__':

    url = "https://gams.uni-graz.at/archive/risearch?type=tuples&lang=sparql&format=Sparql&query=http%3A%2F%2Ffedora%3A8380%2Farchive%2Fget%2Fcontext%3Aszd.facsimiles.korrespondenzen%2FQUERY%2F2024-05-17T13%3A52%3A12.890Z"
    response = requests.get(url)
    xml_data = response.content
    namespace = {'ns': 'http://www.w3.org/2001/sw/DataAccess/rf1/result'}
    root = ET.fromstring(xml_data)
    # Step 3: Extract all titles using XPath, accounting for namespace
    results = root.findall('.//ns:result', namespaces=namespace)


    main()
    
    
