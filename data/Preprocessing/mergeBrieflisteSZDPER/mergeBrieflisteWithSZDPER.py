import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle
import xml.etree.ElementTree as ET
import urllib.request
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

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


# DataFrame = Google Spreadsheet
df=pd.DataFrame(values_input[1:], columns=values_input[0])

# define two sets with "SURNAME, FORENAME" from spreadsheet and from SZDPER
set_excelNames = set()
set_SZDPER  = set()

# save all "SURNAME, FORENAME" from the spreadsheet 
for name in df["Correspondent"]:
    set_excelNames.add(name)

# extract SURNAME, FORENAME from https://gams.uni-graz.at/o:szd.personen/TEI_SOURCE
for person in tree.findall('.//'+tei+'listPerson//'+tei+'persName'):
    if(person.find(tei+'name') is not None):
        name = person.find(tei+'name').text
        set_SZDPER.add(name)
    else:
        if (person.find(tei+'forename') is not None):
            forename = person.find(tei+'forename').text
        else:
            pass
        if (person.find(tei+'surname') is not None):
            surname = person.find(tei+'surname').text
        else:
            pass
        set_SZDPER.add(surname + ", " + forename)

# difference of the two sets
newPerson = set_excelNames - set_SZDPER

#print(newPerson)

# creates XML/TEI person/persName
SZDPER_ID = 1645
#print(df["Correspondent"])

for person in newPerson:
    
    
    # select the row in which google spreadsheet "Correspondent" has same name
    df.loc[df["Correspondent"] == person]
    #print(type(df.loc[df["Correspondent"] == person]["GND"].item()))
    if(df.loc[df["Correspondent"] == person]["GND"].item() is not None):
        row = df.loc[df["Correspondent"] == person]["GND"].item()
    else:
        row = "TESTerrich"

    # t:person
    tei_person = ET.Element('person')
    tei_person.set('xml:id', str(SZDPER_ID) )
    # t:persName
    tei_persName = ET.SubElement(tei_person, 'persName')
    if(row):
        tei_persName.set('ref', row)
    # t:forename|t:surname|t:name
    if(', ' in person):
        tei_surname = ET.SubElement(tei_persName, 'surname')
        tei_surname.text = person.split(', ')[0]
        tei_forename = ET.SubElement(tei_persName, 'forename')
        tei_forename.text = person.split(', ')[1]
    else:
        tei_name = ET.SubElement(tei_persName, 'name')
        tei_name.text = person
        
    SZDPER_ID += 1
    ET.dump(tei_person)   
