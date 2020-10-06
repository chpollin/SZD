import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle
import xml.etree.ElementTree as ET
import urllib.request

# https://docs.google.com/spreadsheets/d/1VX9XBH2yQV5TygdRpWLNjkaEObuQ4Hd1eMSyIo6lgxo/edit?usp=sharing

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1VX9XBH2yQV5TygdRpWLNjkaEObuQ4Hd1eMSyIo6lgxo'
SAMPLE_RANGE_NAME = 'A1:AA1000'

def main():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'googleapi.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    if not values_input and not values_expansion:
        print('No data found.')

main()

# load SZDPER
URL = "https://gams.uni-graz.at/o:szd.personen/TEI_SOURCE"
response = urllib.request.urlopen(URL).read()
tree = ET.fromstring(response)
tei = "{http://www.tei-c.org/ns/1.0}"


df=pd.DataFrame(values_input[1:], columns=values_input[0])

set_excelNames = set()
set_SZDPER  = set()

for name in df["Correspondent(s)"]:
    set_excelNames.add(name)

#print(tree)

for person in tree.findall('.//'+tei+'listPerson//'+tei+'persName'):
    if(person.find(tei+'name') is not None):
        name = person.find(tei+'name').text
        set_SZDPER.add(name)
    else:
        if (person.find(tei+'forename') is not None):
            forename = person.find(tei+'forename').text
        else:
            forename = "x"
        if (person.find(tei+'surname') is not None):
            surname = person.find(tei+'surname').text
        else:
            surname = "x"
        set_SZDPER.add(surname + ", " + forename)

#print("#### Exist in Google SpreadSheet and in SZDPER")    
#print(set_SZDPER & set_excelNames)     
print("#### Exist only in Google SpreadSheet")
print(set_excelNames - set_SZDPER)                
    ## ToDo: alle namen heraus bekommen NACHNAME, Vorname und mit df["Correspondent(s)"] abgleichen; 
    # wenn es matchts --> ignorieren; wenn nicht eine neue Person hinzufügen
    # gleich immer SZDPER von szd direkt herholen; weiter anreichern über Wikidata und wieder ingestieren? 