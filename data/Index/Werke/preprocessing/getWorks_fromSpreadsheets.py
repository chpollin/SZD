from __future__ import print_function
import logging
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import xml.etree.ElementTree as ET
from typing import List
import os


#  https://docs.google.com/spreadsheets/d/1yf2L0gxUf5nJzYexHkHfd3Xqr_IAezOrKVdJCGclDJ4/edit#gid=0

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1yf2L0gxUf5nJzYexHkHfd3Xqr_IAezOrKVdJCGclDJ4'
SAMPLE_RANGE_NAME = 'A2:J214'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    try:
        os.mkdir("./log")
    except FileExistsError:
        pass
    logging.basicConfig(filename='log/getWorks.log', level=logging.DEBUG, filemode="w")
    logging.debug('Program started')

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
            SZDWRK_ID = index + 1
            

            #####################
            ### <bibl>
            title = col_to_string(row, 0)
            compilation_title = col_to_string(row, 1)
            tei_bibl = ET.SubElement(tei_listBibl, 'bibl')
            tei_bibl.set('xml:id', "SZDWRK." + str(SZDWRK_ID))
            if ('Der' in title[0:4]): 
                tei_bibl.set('sortKey', title.split("Der ",1)[1].replace(" ", "").capitalize())
            elif ('Die' in title[0:4]): 
                tei_bibl.set('sortKey', title.split("Die ",1)[1].replace(" ", "").capitalize())
            elif ('Das' in title[0:4]): 
                tei_bibl.set('sortKey', title.split("Das ",1)[1].replace(" ", "").capitalize())    
            elif (compilation_title != ''):    
                tei_bibl.set('sortKey', compilation_title.replace(" ", "").capitalize())
            else:
                if ('Der' in compilation_title[0:4]): 
                    tei_bibl.set('sortKey', compilation_title.split("Der ",1)[1].replace(" ", "").capitalize())
                elif ('Die' in compilation_title[0:4]): 
                    tei_bibl.set('sortKey', title.split("Die ",1)[1].replace(" ", "").capitalize())
                elif ('Das' in compilation_title[0:4]): 
                    tei_bibl.set('sortKey', compilation_title.split("Das ",1)[1].replace(" ", "").capitalize())    
                elif (compilation_title != ''):    
                    tei_bibl.set('sortKey', compilation_title.replace(" ", "").capitalize())
                else:
                    tei_bibl.set('sortKey', title.replace(" ", "").capitalize())   

                        
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
            if col_to_string(row, 0) != '' :
                tei_title_single = ET.SubElement(tei_bibl, 'title')
                tei_title_single.text = col_to_string(row, 0)
                if col_to_string(row, 9) != '' :
                    set_col_att(tei_title_single, 'ref', row, 9)   
            elif compilation_title != '' :
                tei_title_compil = ET.SubElement(tei_bibl, 'title')
                tei_title_compil.set('type', 'compilation')
                tei_title_compil.text = compilation_title
                if col_to_string(row, 9) != '' :
                    set_col_att(tei_title_single, 'ref', row, 9) 

            #####################
            #### <lang> language work was written in
            if col_to_string(row, 5) != '':
                tei_lang = ET.SubElement(tei_bibl, 'lang')
                tei_lang.text = col_to_string(row, 5)

            #####################
            #### <publisher> includes date of creation and publication
            #### creation date(s)
            origDate = col_to_string(row, 2)
            pubDate = col_to_string(row, 3)
            if origDate or pubDate:
                tei_publisher = ET.SubElement(tei_bibl, 'publisher')
                if origDate != '' :
                    tei_origDate = ET.SubElement(tei_publisher, 'origDate')
                    tei_origDate.text = origDate
                    if '/' in origDate:
                        origDate_from = origDate.split('/')[0]
                        origDate_to = origDate.split('/')[1]
                        tei_origDate.set('from', origDate_from)
                        tei_origDate.set('to', origDate_to)
                    else:
                        tei_origDate.set('when', origDate)
                #### publication date # Titel Zusammenstellung hat oft hinten Jahreszahl in Klammer
                if pubDate != '' :
                    tei_pubDate = ET.SubElement(tei_publisher, 'date')
                    tei_pubDate.set('when', col_to_string(row, 3))
                    tei_pubDate.text = col_to_string(row, 3)
            #####################
            #### <term> form of literature - erzeugt durch copy aus SDZMSK
            # if col_to_string(row, 5) != '' :
            #     tei_term = ET.SubElement(tei_bibl, 'term')
            #     tei_term.set('type', 'classification')
            #     tei_term.set('xml:lang', 'de')
            #     tei_term.text = col_to_string(row, 5)

            #####################
            #### <sourceDesc> Quelle
            '''
            if col_to_string(row, 7) != '' :
                tei_source = ET.SubElement(tei_bibl, 'sourceDesc')
                tei_source_p = ET.SubElement(tei_source, 'p')
                tei_source_p.text = col_to_string(row, 7)
            '''
     
    # debugging only  
    #ET.dump(tei_listBibl) 
    
    # create a new XML file with the results
    ET.ElementTree(tei_listBibl).write('extractedSZDWRK.xml', encoding="UTF-8", xml_declaration=True)
              
def col_to_string(row: List[str], index: int):#type annotation: row = array
    """
    try and catch empty cells
    """
    try:
        return str(row[index])
    
    except:
        logging.info(f'Empty string in {str(index)}, {str(row)}. Return empty string to proceed.')
        return ''

def set_col_att(element, attribute: str, row, index: int):
    if col_to_string(row, index) != '':
        element.set(attribute, col_to_string(row, index))

if __name__ == '__main__':
    main()
    
    
