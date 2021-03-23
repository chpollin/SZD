from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import xml.etree.ElementTree as ET
import urllib.request
import pandas as pd

# https://docs.google.com/spreadsheets/d/1VX9XBH2yQV5TygdRpWLNjkaEObuQ4Hd1eMSyIo6lgxo/edit?usp=sharing

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1VX9XBH2yQV5TygdRpWLNjkaEObuQ4Hd1eMSyIo6lgxo'
SAMPLE_RANGE_NAME = 'A2:L500'

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
    
    lettersByZweigbegin = 435
    
    tei_listBibl = ET.Element('listBibl')
   
    if not values:
        print('No data found.')
    else:
        for index, row in enumerate(values):
            
            if(index < lettersByZweigbegin):
                # if the length of row is 12 (columns) than its a valid row
                try:
                    if(len(row) == 12):
                        SZDKOR_ID = int(row[0])
                        author = str(row[1])
                        
                        signature = str(row[11])
                        count_sig = 0
                        piecesOfCorr_by_zweig = False
                        enclosuers_by_zweig = False
                        for list_ in values:
                            if signature in list_:
                                count_sig += 1
                                a = list_[3]
                                b = list_[4] 
                        
                        #####################
                        ### <biblFull>
                        tei_biblFull = ET.SubElement(tei_listBibl, 'biblFull')
                        tei_biblFull.set('xml:id', "SZDKOR." + str(row[0]) )
                        
                        #####################
                        #### <fileDesc> <titleStmt>
                        tei_fileDesc = ET.SubElement(tei_biblFull, 'fileDesc')
                        tei_titleStmt = ET.SubElement(tei_fileDesc, 'titleStmt')
                        tei_title_de = ET.SubElement(tei_titleStmt, 'title') 
                        tei_title_de.set('xml:lang', "de")
                        tei_title_en = ET.SubElement(tei_titleStmt, 'title')
                        tei_title_en.set('xml:lang', "en") 
                        try:
                            if(int(row[3]) > 1):
                                if(count_sig == 2):
                                    tei_title_de.text =  str(int(row[3]) + int(a)) + " Korrespondenzstücke [AN/VON Stefan Zweig]"
                                    tei_title_en.text =  str(int(row[3]) + int(a)) + " Pieces of Correspondence  [TO/FROM Stefan Zweig]"
                                else:
                                    tei_title_de.text =  str(row[3]) + " Korrespondenzstücke [AN Stefan Zweig]"
                                    tei_title_en.text =  str(row[3]) + " Pieces of Correspondence  [TO Stefan Zweig]"
                            else:
                                tei_title_de.text = str(row[3]) + " Korrespondenzstück [AN Stefan Zweig]"
                                tei_title_en.text =  str(row[3]) + " Piece of Correspondence  [TO Stefan Zweig]"
                        except:
                            print(f"Exception: invalid data in 'Pieces of correspondenc' {row}")  
                       
                        #####################
                        ### <publicationStmt>
                        tei_publicationStmt = ET.SubElement(tei_fileDesc, 'publicationStmt')
                        tei_ab_publicationStmt = ET.SubElement(tei_publicationStmt, 'ab')
                        tei_ab_publicationStmt.text = "Briefkonvolut"
                        
                        #####################
                        ### <notesStmt>
                        if(row[7]):
                            tei_notesStmt = ET.SubElement(tei_fileDesc, 'notesStmt')
                            tei_note = ET.SubElement(tei_notesStmt, 'note')
                            tei_note.text = str(row[7])
                            #tei_note.set('xml:lang', 'en')
                        
                        #####################
                        ### <sourceDesc>
                        tei_sourceDesc = ET.SubElement(tei_fileDesc, 'sourceDesc')
                        tei_msDesc = ET.SubElement(tei_sourceDesc, 'msDesc')
                        tei_msIdentifier = ET.SubElement(tei_msDesc, 'msIdentifier')
                        # chrildren of 
                        tei_country_msIdentifier = ET.SubElement(tei_msIdentifier, 'country')
                        tei_country_msIdentifier.text = "USA"
                        tei_settlement_msIdentifier = ET.SubElement(tei_msIdentifier, 'settlement')
                        tei_settlement_msIdentifier.text = "Fredonia"
                        tei_repository_msIdentifier = ET.SubElement(tei_msIdentifier, 'repository')
                        tei_repository_msIdentifier.text = "Reed Library – Stefan Zweig Collection"
                        tei_repository_msIdentifier.set('ref', 'http://d-nb.info/gnd/2156743-8')
                        
                        tei_idno_msIdentifier = ET.SubElement(tei_msIdentifier, 'idno')
                        tei_idno_msIdentifier.set('type', 'signature')

                        #####################
                        ### <physDesc>
                        tei_physDesc = ET.SubElement(tei_msDesc, 'physDesc')
                        tei_objectDesc = ET.SubElement(tei_physDesc, 'objectDesc')
                        tei_supportDesc = ET.SubElement(tei_objectDesc, 'supportDesc')
                        tei_extent = ET.SubElement(tei_supportDesc, 'extent')
                        
                        
                        #####################
                        ####  <profileDesc>    
                        tei_profileDesc = ET.SubElement(tei_biblFull, 'profileDesc')
                        tei_correspDesc = ET.SubElement(tei_profileDesc, 'correspDesc')
                        
                        #####################
                        ### <correspAction>
                        tei_correspAction_sent = ET.SubElement(tei_correspDesc, 'correspAction')
                        tei_correspAction_sent.set('type', "sent")
                        tei_correspAction_received = ET.SubElement(tei_correspDesc, 'correspAction')
                        tei_correspAction_received.set('type', "received")
                         # check if signature exists a second time
                       
                        if(count_sig == 2):
                            if(a):
                                piecesOfCorr_by_zweig = a
                            if(b):
                                enclosuers_by_zweig = b 
                            tei_correspAction_sent_by_zweig = ET.SubElement(tei_correspDesc, 'correspAction')
                            tei_correspAction_sent_by_zweig.set('type', "sent")
                            tei_correspAction_received_by_zweig = ET.SubElement(tei_correspDesc, 'correspAction')
                            tei_correspAction_received_by_zweig.set('type', "received")
                            
                            tei_persName_sent_by_zweig = ET.SubElement(tei_correspAction_sent_by_zweig, 'persName')
                            tei_surname_sent_by_zweig = ET.SubElement(tei_persName_sent_by_zweig, 'surname')
                            tei_surname_sent_by_zweig.text = "Zweig"
                            tei_forename_sent_by_zweig = ET.SubElement(tei_persName_sent_by_zweig, 'forename')
                            tei_forename_sent_by_zweig.text = "Stefan"
                            tei_persName_sent_by_zweig.set('ref', 'http://d-nb.info/gnd/118637479')
                            
                            tei_persName_received_by_zweig = ET.SubElement(tei_correspAction_received_by_zweig, 'persName')
                            tei_surname_received_by_zweig = ET.SubElement(tei_persName_received_by_zweig, 'surname')
                            tei_surname_received_by_zweig.text = author.split(', ')[0]
                            tei_forename_received_by_zweig = ET.SubElement(tei_persName_received_by_zweig, 'forename')
                            tei_forename_received_by_zweig.text = author.split(', ')[1]
                            #tei_title.text = "Briefkonvolut " + author.split(', ')[1] + " " + author.split(', ')[0] + " an Stefan Zweig"
                            
                            if(row[2]):
                                tei_persName_sent.set('ref', str(row[2]))
                        ###    
                        if(row[3]):
                            tei_measure_1 = ET.SubElement(tei_extent, 'measure')
                            tei_measure_1.text = str(row[3])
                            tei_measure_1.set('type', "correspondence")
                            tei_measure_1.set('unit', "piece")
                            tei_measure_1.set('ana', "received")
                            
                        if(row[4]):
                            tei_measure_2 = ET.SubElement(tei_extent, 'measure')
                            tei_measure_2.text = str(row[4])
                            tei_measure_2.set('type', "enclosures")
                            tei_measure_2.set('unit', "piece")
                            tei_measure_2.set('ana', "received")
                            
                        if(piecesOfCorr_by_zweig):
                            tei_measure_3 = ET.SubElement(tei_extent, 'measure')
                            tei_measure_3.text = piecesOfCorr_by_zweig
                            tei_measure_3.set('type', "correspondence")
                            tei_measure_3.set('unit', "piece")
                            tei_measure_3.set('ana', "sent")
                            
                        if(enclosuers_by_zweig):
                            tei_measure_3 = ET.SubElement(tei_extent, 'measure')
                            tei_measure_3.text = enclosuers_by_zweig
                            tei_measure_3.set('type', "enclosures")
                            tei_measure_3.set('unit', "piece")
                            tei_measure_3.set('ana', "sent") 
                         
                            
                        tei_idno_msIdentifier.text = str(row[11])
                        
                        #####################
                        # <persName> in <correspAction>
                        
                        tei_persName_received = ET.SubElement(tei_correspAction_received, 'persName')
                        tei_surname_received = ET.SubElement(tei_persName_received, 'surname')
                        tei_surname_received.text = "Zweig"
                        tei_forename_received = ET.SubElement(tei_persName_received, 'forename')
                        tei_forename_received.text = "Stefan"
                        tei_persName_received.set('ref', 'http://d-nb.info/gnd/118637479')
                        
                        
                        if(', ' in author):
                            tei_persName_sent = ET.SubElement(tei_correspAction_sent, 'persName')
                            tei_surname = ET.SubElement(tei_persName_sent, 'surname')
                            tei_surname.text = author.split(', ')[0]
                            tei_forename = ET.SubElement(tei_persName_sent, 'forename')
                            tei_forename.text = author.split(', ')[1]
                            #tei_title.text = "Briefkonvolut " + author.split(', ')[1] + " " + author.split(', ')[0] + " an Stefan Zweig"
                            
                            if(row[2]):
                                tei_persName_sent.set('ref', str(row[2]))
                        else:
                            tei_name_sent = ET.SubElement(tei_correspAction_sent, 'name')
                            tei_name_sent.text = author
                            tei_title.text = author + " an Stefan Zweig"
                            if(row[2]):
                                tei_name_sent.set('ref', str(row[2]))
                        
                    
                            
                        #####################
                        # <date> in <correspAction>
                        tei_date_sent = ET.SubElement(tei_correspAction_sent, 'date')
                        if(row[9]):
                            tei_date_sent.text = str(row[9])             
                except:
                    print(f"Exception: invalid row")
            # LETTERS By Zweig
            else:
                print("Log: a LETTERS By Zweig")                   
                                   
                   
     
    # debugging only  
    #ET.dump(tei_listBibl) 
    
    # create a new XML file with the results
    ET.ElementTree(tei_listBibl).write('extractedSZDKOR.xml', encoding="UTF-8", xml_declaration=True)
    #SZDKOR = ET.tostring(tei_listBibl, encoding="us-ascii", method='xml')
    #myfile = open("SZDKOR.xml", "w")
    #myfile.write(SZDKOR) 
              
if __name__ == '__main__':
    main()
    
    
