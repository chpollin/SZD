from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import xml.etree.ElementTree as ET
import urllib.request
import pandas as pd

#  https://docs.google.com/spreadsheets/d/16Po8t7cxqkKO7QUvDnLtSXxe2Gm2amoX6DJgDZeb86Y/edit?usp=sharing

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '16Po8t7cxqkKO7QUvDnLtSXxe2Gm2amoX6DJgDZeb86Y'
SAMPLE_RANGE_NAME = 'A2:J500'

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
    
    tei_listBibl = ET.Element('listBibl')
   
    if not values:
        print('No data found.')
    else:

        for index, row in enumerate(values):

            #####################
            ### <bibl> Attribut sortKey, wie gehen wir das an?
            tei_bibl = ET.SubElement(tei_listBibl, 'bibl')
            tei_bibl.set('xml:id', "SZDWRK." + str(row[0]))
                        
            #####################
            #### <author>
            tei_author = ET.SubElement(tei_bibl, 'author')
            tei_author.set('ref', 'https://gams.uni-graz.at/o:szd.personen#SZDPER.1560')
            tei_persName_aut = ET.SubElement(tei_author, 'persName')
            tei_surname_aut = ET.SubElement(tei_persName_aut, 'surname')
            tei_surname_aut.text = 'Zweig'
            tei__forename_aut = ET.SubElement(tei_persName_aut, 'forename')
            tei__forename_aut.text = 'Stefan'

            #####################
            #### <title>       
            if str(row[0]) != '' :
                tei_title_single = ET.SubElement(tei_bibl, 'title')
                tei_title_single.set('type', 'single')
                tei_title_single.set('ref', str(row[9]))
                tei_title_single.text = str(row[0])
            else:
                tei_title_compil = ET.SubElement(tei_bibl, 'title')
                tei_title_compil.set('type', 'compilation')
                tei_title_compil.set('ref', str(row[9]))  
                tei_title_compil.text = str(row[1])
            
            if str(row[8]) != '' :
                tei_title_alt = ET.SubElement(tei_bibl, 'title')
                tei_title_alt.set('type', 'alt')
                tei_title_alt.text = 'str(row[8])'

            #####################
            #### <lang> language work was written in
            if str(row[5]) == 'ger' :
                tei_lang = ET.SubElement(tei_bibl, 'lang')
                tei_lang.set('xml:lang', 'de')
                tei_lang.text = 'Deutsch'

            #####################
            #### <publisher> includes date of creation and publication
            #### creation date(s)
            origDate = str(row[2])
            tei_publisher = ET.SubElement(tei_bibl, 'publisher')
            tei_origDate = ET.SubElement(tei_publisher, 'origDate')
            tei_origDate.text = origDate
            if '/' in origDate:
                origDate_from = origDate.split('/')[0]
                origDate_to = origDate.split('/')[1]
                tei_origDate.set('from', origDate_from)
                tei_origDate.set('to', origDate_to)
            else:
                origDate.set('when', origDate)
            
            #### publication date # Titel Zusammenstellung hat oft hinten Jahreszahl in Klammer
            pubDate = str(row[3])
            tei_pubDate = ET.SubElement(tei_publisher, 'pubDate')
            tei_pubDate.set('when', pubDate)
            tei_pubDate.text = pubDate

            #####################
            #### <term> form of literature
            tei_term = ET.SubElement(tei_bibl, 'term')
            tei_term.set('type', 'classification')
            tei_term.set('xml:lang', 'de')
            tei_term.text = str(row[4])

            #####################
            #### <sourceDesc> Quelle
            tei_source = ET.SubElement(tei_bibl, 'sourceDesc')
            tei_source_p = ET.SubElement(tei_source, 'p')
            tei_source_p.text = str(row[6])

            #####################
            #### <note> Weitere Angaben im Spreadsheet
            tei_note = ET.SubElement(tei_bibl, ' note')
            tei_note.text = str(row[7])



     
    # debugging only  
    #ET.dump(tei_listBibl) 
    
    # create a new XML file with the results
    ET.ElementTree(tei_listBibl).write('extractedSZDWRK.xml', encoding="UTF-8", xml_declaration=True)
              
if __name__ == '__main__':
    main()
    
    
