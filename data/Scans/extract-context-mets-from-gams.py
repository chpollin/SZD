import xml.etree.ElementTree as ET
import csv
import logging
from collections import defaultdict
import requests

def setup_logging():
    logging.basicConfig(filename='conversion.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def extract_pid(pid_uri):
    return pid_uri.split('/')[-1]

def fetch_xml_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching XML data: {str(e)}")
        raise

def xml_to_csv(xml_data, csv_file):
    setup_logging()
    
    ET.register_namespace('', "http://www.w3.org/2001/sw/DataAccess/rf1/result")
    
    root = ET.fromstring(xml_data)
    
    ns = {'sparql': 'http://www.w3.org/2001/sw/DataAccess/rf1/result'}

    grouped_results = defaultdict(list)
    print(grouped_results)
    for result in root.findall('.//sparql:result', ns):
        pid = result.find('sparql:pid', ns).get('uri')
        grouped_results[pid].append(result)

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Fördernehmer', 'ID', 'Type', 'Ressourcenadresse', 'Kontextadresse' 'Titel', 'Language', 'Date', 'Creator', 'Contributor'])

        for pid, results in grouped_results.items():
            print(pid)
            try:
                foerdernehmer = "LAS Salzburg"
                id = extract_pid(pid)
                ressourcenadresse = f"https://gams.uni-graz.at/{id}"
                kontextadresse = f"https://gams.uni-graz.at/{id}/DC"

                result = next((r for r in results if r.find('sparql:type', ns).text != "Text"), results[0])

                type_elem = result.find('sparql:type', ns)
                type = type_elem.text if type_elem is not None and type_elem.text != "Text" else ""

                title = result.find('sparql:title', ns).text

                language_elem = result.find('sparql:language', ns)
                language = language_elem.text if language_elem is not None else ""

                date_elem = result.find('sparql:date', ns)
                date = date_elem.text if date_elem is not None else ""

                creator_elem = result.find('sparql:creator', ns)
                creator = creator_elem.text if creator_elem is not None else ""

                contributor_elem = result.find('sparql:contributor', ns)
                contributor = contributor_elem.text if contributor_elem is not None else ""

                row = [foerdernehmer, id, type, ressourcenadresse, kontextadresse, title, language, date, creator, contributor]
                writer.writerow(row)

            except AttributeError as e:
                logging.error(f"Error processing PID {pid}: {str(e)}")
            except Exception as e:
                logging.error(f"Unexpected error processing PID {pid}: {str(e)}")

    logging.info(f"Conversion complete. CSV file saved as {csv_file}")

if __name__ == "__main__":
    url = "https://gams.uni-graz.at/archive/risearch?type=tuples&lang=sparql&format=Sparql&query=http%3A%2F%2Ffedora%3A8380%2Farchive%2Fget%2Fcontext%3Aszd.mets%2FQUERY%2F2024-08-06T17%3A11%3A10.193Z"
    csv_file = "facsimiles-from-mets.csv"

    try:
       
        xml_data = fetch_xml_data(url)
        if not xml_data:
            raise ValueError("No data fetched from the URL")
        
        xml_to_csv(xml_data, csv_file)
        print(f"Conversion complete. CSV file saved as {csv_file}")
        print("Check conversion.log for any error messages.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Check conversion.log for details.")
        logging.error(f"Script execution failed: {str(e)}")