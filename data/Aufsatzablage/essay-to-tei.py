import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom
import re

# Possible 3-letter codes and their respective language names.
LANG_MAP = {
    'ger': 'Deutsch',
    'fra': 'Französisch',
    'ita': 'Italienisch',
    'spa': 'Spanisch',
    'eng': 'Englisch',
    'fin': 'Finnisch',
    'cze': 'Tschechisch'
}

def get_row_value(row, field_name):
    """
    A helper function to safely extract a field from the CSV row dictionary
    and pass it to the normalize_string.
    """
    return normalize_string(row.get(field_name, ''))

def normalize_string(text):
    """
    Normalize string by removing extra whitespace.
    """
    if not text:
        return ''
    return ' '.join(text.split())

def load_facsimile_metadata(xml_file_path):
    """
    Load the XML file facsimilies-aufsatz-metadata.xml and build a dictionary:
       { signature_from_title : PID }
    
    The logic:
      1) For each <result> element:
         - Extract the text from <title>, e.g. "Franz Werfel. Ein einführendes Wort, SZ-AAP/W-AA214.1"
         - Take the substring after the last comma (strip it) => "SZ-AAP/W-AA214.1"
           This becomes our 'signature' to match the CSV "Signatur/shelfmark".
         - Extract the <pid> attribute, e.g. "info:fedora/o:szd.2213"
           -> we only need the portion after the last "/", e.g. "o:szd.2213"
      2) Store in a dictionary: signature_to_pid["SZ-AAP/W-AA214.1"] = "o:szd.2213"
    """
    print(f"Loading facsimile metadata from '{xml_file_path}'...")
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    signature_to_pid = {}

    # The SPARQL structure has multiple <result> elements under <results>.
    # Each <result> has:
    #   <title>...</title>
    #   <pid uri="info:fedora/..." />
    # We'll parse them accordingly.
    for result_el in root.findall('.//{*}result'):
        title_el = result_el.find('{*}title')
        pid_el = result_el.find('{*}pid')

        if title_el is None or pid_el is None:
            continue  # Skip if we don't have expected elements

        title_text = title_el.text or ''
        pid_uri = pid_el.get('uri') or ''
        
        # Extract the substring after the last comma in the title
        # e.g. "Franz Werfel. Ein einführendes Wort, SZ-AAP/W-AA214.1"
        # We want "SZ-AAP/W-AA214.1"
        sig = ''
        if ',' in title_text:
            # rsplit with maxsplit=1 so we only split on the last comma
            parts = title_text.rsplit(',', 1)
            sig = parts[-1].strip()  # take the last part after the comma
        else:
            # Fallback: if there's no comma, we might treat the entire title as the 'signature'
            sig = title_text.strip()

        # Extract the actual PID portion from "info:fedora/o:szd.2213" => "o:szd.2213"
        # There's a slash at "info:fedora/" so let's split by '/'
        pid_parts = pid_uri.rsplit('/', 1)
        pid_str = pid_parts[-1].strip() if len(pid_parts) > 1 else pid_uri

        # Save to dictionary
        signature_to_pid[sig] = pid_str
        print(f"  Found signature='{sig}' => PID='{pid_str}'")

    print("Facsimile metadata loaded.\n")
    return signature_to_pid

def csv_to_tei(csv_file_path, facsimiles_metadata_path):
    """
    1) Load the facsimile metadata from facsimiles_metadata_path XML file.
    2) Parse the CSV and create TEI XML.
    3) Compare each row's signature with the loaded dictionary from step 1.
       If there's a match, add <altIdentifier><idno type="PID">...</idno></altIdentifier> with that PID.
    4) Return the TEI XML as a pretty-printed string.
    """
    # Load facsimile metadata into a dict: { signature : pid }
    signature_pid_map = load_facsimile_metadata(facsimiles_metadata_path)

    NS_TEI = "http://www.tei-c.org/ns/1.0"
    ET.register_namespace('', NS_TEI)
    NS = {'tei': NS_TEI}

    # Create the root element
    tei = ET.Element('{%s}TEI' % NS_TEI)

    # Create the listBibl element
    listBibl = ET.SubElement(tei, '{%s}listBibl' % NS_TEI)

    print(f"Reading CSV file '{csv_file_path}' to convert to TEI...")
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row_num, row in enumerate(reader, start=1):
            print(f" Processing row #{row_num}, ID={row.get('ID', '')}")
            
            # Create biblFull element
            biblFull = ET.SubElement(listBibl, '{%s}biblFull' % NS_TEI)
            # Use xml:id="SZDESS.{ID}"
            record_id = get_row_value(row, 'ID')
            biblFull.set('xml:id', f"SZDESS.{record_id}")
          

            # Create fileDesc element
            fileDesc = ET.SubElement(biblFull, '{%s}fileDesc' % NS_TEI)

            # Create titleStmt
            titleStmt = ET.SubElement(fileDesc, '{%s}titleStmt' % NS_TEI)

            # -- Map titles --
            # Primary title from 'Titel [Vorlage]/title [on document]'
            title_on_document = get_row_value(row, 'Titel [Vorlage]/title [on document]')
            if title_on_document:
                
                # Exception dictionary for special sorting cases
                exceptions = {
                    "d'Annunzio": "ann",
                    "Max Brod": "bro",
                    "An die Frauen": "fra",
                    "The Future of Writing in a World at War": "fut",
                    "du Gard, Roger Martin": "gar",
                    "Jeremias Gotthelf und Jean Paul": "got",
                    "Das Kreuz": "kre",
                    "Ein Verbummelter": "ver"
                }
    
                # Handle special prefixes
                if title_on_document.startswith("Aufsätze "):
                    remainder = title_on_document[9:]  # length of "Aufsätze " is 9
                    sort_key = remainder[:3].lower()
                elif title_on_document.startswith("Register "):
                    remainder = title_on_document[9:]  # length of "Register " is 9
                    sort_key = remainder[:3].lower()
                else:
                    # Check regular exceptions first
                    if title_on_document in exceptions:
                        sort_key = exceptions[title_on_document]
                    else:
                        # For titles with space, take only up to first space
                        first_word = title_on_document.split()[0]
                        sort_key = first_word[:3].lower()
                
                biblFull.set('sortKey', sort_key)
                
                # Create title element
                title = ET.SubElement(titleStmt, '{%s}title' % NS_TEI)
                title.text = title_on_document

            # Titel (fingiert/assigned)
            titel_fingiert = get_row_value(row, 'Titel (fingiert/assigned)')
            if titel_fingiert:
                title_fingiert_element = ET.SubElement(titleStmt, '{%s}title' % NS_TEI)
                title_fingiert_element.set('ana', 'assigned')
                title_fingiert_element.text = titel_fingiert

            # <title ana="supplied/verified">
            titel_erschlossen = get_row_value(row, 'Titel (erschlossen)')
            if titel_erschlossen:
                title_supplied = ET.SubElement(titleStmt, '{%s}title' % NS_TEI)
                title_supplied.set('ana', 'supplied/verified')
                title_supplied.text = titel_erschlossen

            # <title type="Einheitssachtitel"> from 'Konvoluttitel [...]' or fallback 'GND Werk (SZ)'
            einheitssachtitel_text = get_row_value(row, 'Konvoluttitel [entspricht ansonsten "Einheitssachtitel der Werke"]')
            if einheitssachtitel_text:
                title_einheitssachtitel = ET.SubElement(titleStmt, '{%s}title' % NS_TEI)
                title_einheitssachtitel.set('type', 'Einheitssachtitel')
                title_einheitssachtitel.text = einheitssachtitel_text
            else:
                gnd_werk_sz = get_row_value(row, 'GND Werk (SZ)')
                if gnd_werk_sz:
                    title_einheitssachtitel = ET.SubElement(titleStmt, '{%s}title' % NS_TEI)
                    title_einheitssachtitel.set('type', 'Einheitssachtitel')
                    title_einheitssachtitel.text = gnd_werk_sz

            # <title type="Gesamttitel">
            title_gesamttitel = ET.SubElement(titleStmt, '{%s}title' % NS_TEI)
            title_gesamttitel.set('type', 'Gesamttitel')
            title_gesamttitel.text = 'Stefan Zweig - Archiv Atrium Press'

            # Map author
            author_name = get_row_value(row, 'Verfasser*in')
            if author_name:
                author = ET.SubElement(titleStmt, '{%s}author' % NS_TEI)
                if author_name == 'Unbekannt':
                    name_el = ET.SubElement(author, '{%s}name' % NS_TEI)
                    name_el.text = 'Unbekannt'
                else:
                    author_gnd_ref = get_row_value(row, 'Verfasser*in GND')
                    if author_gnd_ref:
                        author.set('ref', f'#SZDPER.{record_id}')  # Example usage of an ID
                    persName = ET.SubElement(author, '{%s}persName' % NS_TEI)
                    if author_gnd_ref:
                        persName.set('ref', author_gnd_ref)
                    # Attempt to split the author name into surname/forename
                    if ', ' in author_name:
                        surname, forename = author_name.split(', ', 1)
                    else:
                        surname, forename = author_name, ''
                    surname_el = ET.SubElement(persName, '{%s}surname' % NS_TEI)
                    surname_el.text = surname
                    if forename:
                        forename_el = ET.SubElement(persName, '{%s}forename' % NS_TEI)
                        forename_el.text = forename

            # Map contributors to <editor role="contributor">
            contributors_text = get_row_value(row, 'Beteiligte/contributor')
            if contributors_text:
                contributors = [c.strip() for c in contributors_text.split(';') if c.strip()]
                gnd_refs_text = get_row_value(row, 'Beteiligte GND')
                gnd_refs = [g.strip() for g in gnd_refs_text.split(';')] if gnd_refs_text else []
                for idx, contributor in enumerate(contributors):
                    editor = ET.SubElement(titleStmt, '{%s}editor' % NS_TEI)
                    editor.set('role', 'contributor')
                    if contributor == 'Unbekannt':
                        name_el = ET.SubElement(editor, '{%s}name' % NS_TEI)
                        name_el.text = 'Unbekannt'
                    else:
                        persName_contrib = ET.SubElement(editor, '{%s}persName' % NS_TEI)
                        if idx < len(gnd_refs):
                            gnd_ref = gnd_refs[idx]
                            if gnd_ref:
                                persName_contrib.set('ref', gnd_ref)
                        if ', ' in contributor:
                            surname, forename = contributor.split(', ', 1)
                        else:
                            surname, forename = contributor, ''
                        surname_el = ET.SubElement(persName_contrib, '{%s}surname' % NS_TEI)
                        surname_el.text = surname
                        if forename:
                            forename_el = ET.SubElement(persName_contrib, '{%s}forename' % NS_TEI)
                            forename_el.text = forename

            # Map publicationStmt
            publicationStmt = ET.SubElement(fileDesc, '{%s}publicationStmt' % NS_TEI)
            ab = ET.SubElement(publicationStmt, '{%s}ab' % NS_TEI)
            ab.text = 'Archivmaterial'

            # notesStmt with German hint and English note
            hinweis_de = get_row_value(row, 'Hinweis')
            notes_statement_en = get_row_value(row, 'Notes/Statement')
            if hinweis_de or notes_statement_en:
                notesStmt = ET.SubElement(fileDesc, '{%s}notesStmt' % NS_TEI)
                if hinweis_de:
                    note_de = ET.SubElement(notesStmt, '{%s}note' % NS_TEI)
                    note_de.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')
                    note_de.text = hinweis_de
                if notes_statement_en:
                    note_en = ET.SubElement(notesStmt, '{%s}note' % NS_TEI)
                    note_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                    note_en.text = notes_statement_en

            # sourceDesc
            sourceDesc = ET.SubElement(fileDesc, '{%s}sourceDesc' % NS_TEI)

            # Add publication info if available
            publikationsangabe = get_row_value(row, 'Publikationsangabe')
            if publikationsangabe:
                bibl = ET.SubElement(sourceDesc, '{%s}bibl' % NS_TEI)
                bibl.set('type', 'published')
                bibl.text = publikationsangabe

            msDesc = ET.SubElement(sourceDesc, '{%s}msDesc' % NS_TEI)

            # msIdentifier
            msIdentifier = ET.SubElement(msDesc, '{%s}msIdentifier' % NS_TEI)
            country = ET.SubElement(msIdentifier, '{%s}country' % NS_TEI)
            country.text = 'Österreich'
            settlement_text = get_row_value(row, 'Entstehungsort/place of creation') or 'Salzburg'
            settlement = ET.SubElement(msIdentifier, '{%s}settlement' % NS_TEI)
            settlement.text = settlement_text
            repository = ET.SubElement(msIdentifier, '{%s}repository' % NS_TEI)
            repository.text = 'Literaturarchiv Salzburg'
            gnd_standort = get_row_value(row, 'GND Standort')
            if gnd_standort:
                repository.set('ref', gnd_standort)

            idno_signature = ET.SubElement(msIdentifier, '{%s}idno' % NS_TEI)
            idno_signature.set('type', 'signature')
            csv_signature = get_row_value(row, 'Signatur/shelfmark')
            idno_signature.text = csv_signature

            # -- Compare with the facsimile metadata dictionary to add PID if found --
            pid_for_signature = signature_pid_map.get(csv_signature)
            if pid_for_signature:
                print(f"  Signature '{csv_signature}' matched PID '{pid_for_signature}'. Adding altIdentifier...")
                altIdentifier = ET.SubElement(msIdentifier, '{%s}altIdentifier' % NS_TEI)
                idno_pid = ET.SubElement(altIdentifier, '{%s}idno' % NS_TEI)
                idno_pid.set('type', 'PID')
                idno_pid.text = pid_for_signature
            else:
                print(f"  No PID match found for signature '{csv_signature}'.")

            # msContents
            text_lang_code = get_row_value(row, 'Sprachencode [dreistellig]')
            if text_lang_code:
                msContents = ET.SubElement(msDesc, '{%s}msContents' % NS_TEI)
                textLang = ET.SubElement(msContents, '{%s}textLang' % NS_TEI)
                lang_el = ET.SubElement(textLang, '{%s}lang' % NS_TEI)
                lang_el.set('{http://www.w3.org/XML/1998/namespace}lang', text_lang_code)
                lang_el.text = LANG_MAP.get(text_lang_code, '')

            # Add identifying inscription if available
            identifying_inscription = get_row_value(row, 'Aufschrift erstes Blatt / Identifying Inscription')
            if identifying_inscription:
                # Ensure msContents exists
                if not text_lang_code:
                    msContents = msDesc.find('{%s}msContents' % NS_TEI)
                    if msContents is None:
                        msContents = ET.SubElement(msDesc, '{%s}msContents' % NS_TEI)

                ms_item = ET.SubElement(msContents, '{%s}msItem' % NS_TEI)
                # German version
                doc_edition_de = ET.SubElement(ms_item, '{%s}docEdition' % NS_TEI)
                doc_edition_de.set('ana', 'szdg:IdentifyingInscription')
                doc_edition_de.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')
                doc_edition_de.text = identifying_inscription
                # English version
                doc_edition_en = ET.SubElement(ms_item, '{%s}docEdition' % NS_TEI)
                doc_edition_en.set('ana', 'szdg:IdentifyingInscription')
                doc_edition_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                doc_edition_en.text = identifying_inscription  # Or a real translation if available

            # physDesc
            physDesc = ET.SubElement(msDesc, '{%s}physDesc' % NS_TEI)
            objectDesc = ET.SubElement(physDesc, '{%s}objectDesc' % NS_TEI)
            supportDesc = ET.SubElement(objectDesc, '{%s}supportDesc' % NS_TEI)
            support = ET.SubElement(supportDesc, '{%s}support' % NS_TEI)

            schreibstoff = get_row_value(row, 'Schreibstoff')
            writing_instrument = get_row_value(row, 'Writing Instrument')

            if schreibstoff:
                # German material element
                material_de = ET.SubElement(support, '{%s}material' % NS_TEI)
                material_de.set('ana', 'szdg:WritingInstrument')
                material_de.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')
                material_de.text = schreibstoff

            if writing_instrument:
                # English material element
                material_en = ET.SubElement(support, '{%s}material' % NS_TEI)
                material_en.set('ana', 'szdg:WritingInstrument')
                material_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                material_en.text = writing_instrument

            # extent
            art_umfang_anzahl = get_row_value(row, 'Art, Umfang, Anzahl')  # German physical description
            physical_description = get_row_value(row, 'Physical Description')  # English physical description
            paginierung = get_row_value(row, 'Paginierung')

            # Only create <extent> if we have at least one of them
            if art_umfang_anzahl or physical_description or paginierung:
                extent = ET.SubElement(supportDesc, '{%s}extent' % NS_TEI)

                #
                # 1) German version (Art, Umfang, Anzahl)
                #
                if art_umfang_anzahl:
                    # Split only once on the first comma
                    parts_de = [part.strip() for part in art_umfang_anzahl.split(',', 1)]
                    span_de = ET.SubElement(extent, '{%s}span' % NS_TEI)
                    span_de.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')

                    if parts_de:
                        # First chunk -> <term type="objecttyp">
                        term_text_de = parts_de[0]
                        term_de = ET.SubElement(span_de, '{%s}term' % NS_TEI)
                        term_de.set('type', 'objecttyp')
                        term_de.text = term_text_de

                        # If there was a second chunk, use it for <measure ana="corrected" type="leaf">
                        if len(parts_de) > 1:
                            measure_text_de = parts_de[1]
                            measure_de = ET.SubElement(span_de, '{%s}measure' % NS_TEI)
                            measure_de.set('ana', 'corrected')
                            measure_de.set('type', 'leaf')
                            measure_de.text = measure_text_de
                    else:
                        # Fallback if splitting failed
                        term_de = ET.SubElement(span_de, '{%s}term' % NS_TEI)
                        term_de.set('type', 'objecttyp')
                        term_de.text = art_umfang_anzahl

                #
                # 2) English version (Physical Description)
                #
                if physical_description:
                    # Same splitting logic for the English version
                    parts_en = [part.strip() for part in physical_description.split(',', 1)]
                    span_en = ET.SubElement(extent, '{%s}span' % NS_TEI)
                    span_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')

                    if parts_en:
                        # First chunk -> <term type="objecttyp">
                        term_text_en = parts_en[0]
                        term_en = ET.SubElement(span_en, '{%s}term' % NS_TEI)
                        term_en.set('type', 'objecttyp')
                        term_en.text = term_text_en

                        # If there was a second chunk, use it for <measure ana="corrected" type="leaf">
                        if len(parts_en) > 1:
                            measure_text_en = parts_en[1]
                            measure_en = ET.SubElement(span_en, '{%s}measure' % NS_TEI)
                            measure_en.set('ana', 'corrected')
                            measure_en.set('type', 'leaf')
                            measure_en.text = measure_text_en
                    else:
                        # Fallback if splitting failed
                        term_en = ET.SubElement(span_en, '{%s}term' % NS_TEI)
                        term_en.set('type', 'objecttyp')
                        term_en.text = physical_description

                if paginierung:
                    measure_page = ET.SubElement(extent, '{%s}measure' % NS_TEI)
                    measure_page.set('type', 'page')
                    measure_page.text = paginierung

            # handDesc
            schreiberhand = get_row_value(row, 'Schreiberhand')
            if schreiberhand:
                handDesc = ET.SubElement(physDesc, '{%s}handDesc' % NS_TEI)

                # German text node (no changes)
                ab_hand_de = ET.SubElement(handDesc, '{%s}ab' % NS_TEI)
                ab_hand_de.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')
                ab_hand_de.text = schreiberhand

                # English text node (replace any form of "Unbekannt" with "Unknown")
                ab_hand_en = ET.SubElement(handDesc, '{%s}ab' % NS_TEI)
                ab_hand_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                # Use regex with re.IGNORECASE to replace “unbekannt” anywhere it appears
                schreiberhand_en = re.sub(r'(?i)unbekannt', 'Unknown', schreiberhand)
                ab_hand_en.text = schreiberhand_en

            # history
            history = ET.SubElement(msDesc, '{%s}history' % NS_TEI)
            # origin
            origPlace_text = get_row_value(row, 'Entstehungsort/place of creation')
            date_norm = get_row_value(row, 'Datum [normiert]/date [normalized]')
            date_on_document = get_row_value(row, 'Datum [Vorlage]/date [on document]')
            datierung_erschlossen = get_row_value(row, 'Datierung erschlossen')
            date_supplied_verified = get_row_value(row, 'Date supplied/verified')

            if origPlace_text or date_norm or date_on_document or datierung_erschlossen:
                origin = ET.SubElement(history, '{%s}origin' % NS_TEI)
                if origPlace_text:
                    origPlace = ET.SubElement(origin, '{%s}origPlace' % NS_TEI)
                    origPlace.text = origPlace_text

                if date_on_document:
                    origDate = ET.SubElement(origin, '{%s}origDate' % NS_TEI)
                    origDate.text = date_on_document

                if datierung_erschlossen:
                    origDate_supplied_de = ET.SubElement(origin, '{%s}origDate' % NS_TEI)
                    origDate_supplied_de.set('ana', 'supplied/verified')
                    origDate_supplied_de.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')
                    origDate_supplied_de.text = datierung_erschlossen
                    if date_norm:
                        origDate_supplied_de.set('when', date_norm)

                if date_supplied_verified:
                    origDate_supplied_en = ET.SubElement(origin, '{%s}origDate' % NS_TEI)
                    origDate_supplied_en.set('ana', 'supplied/verified')
                    origDate_supplied_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                    origDate_supplied_en.text = date_supplied_verified
                    if date_norm:
                        origDate_supplied_en.set('when', date_norm)

            # provenance
            provenance_text = get_row_value(row, 'Provenienz/provenance')
            if provenance_text:
                provenance = ET.SubElement(history, '{%s}provenance' % NS_TEI)
                ab_prov_de = ET.SubElement(provenance, '{%s}ab' % NS_TEI)
                ab_prov_de.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')
                ab_prov_de.text = provenance_text
                # default English translation
                ab_prov_en = ET.SubElement(provenance, '{%s}ab' % NS_TEI)
                ab_prov_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                ab_prov_en.text = 'Atrium Press'

            # acquisition
            acquisition_text = get_row_value(row, 'Erwerbung/acquisition')
            if acquisition_text:
                acquisition = ET.SubElement(history, '{%s}acquisition' % NS_TEI)
                ab_acq_de = ET.SubElement(acquisition, '{%s}ab' % NS_TEI)
                ab_acq_de.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')
                ab_acq_de.text = acquisition_text
                # default English translation
                ab_acq_en = ET.SubElement(acquisition, '{%s}ab' % NS_TEI)
                ab_acq_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                ab_acq_en.text = "Acquisition from Christie's London 2014"

            # profileDesc
            profileDesc = ET.SubElement(biblFull, '{%s}profileDesc' % NS_TEI)
            textClass = ET.SubElement(profileDesc, '{%s}textClass' % NS_TEI)
            keywords_terms = []

            # classification
            ordnungskategorie = get_row_value(row, 'Ordnungskategorie [classification]')
            if ordnungskategorie:
                term_class_de = ET.Element('{%s}term' % NS_TEI)
                term_class_de.set('type', 'classification')
                term_class_de.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')
                term_class_de.text = ordnungskategorie
                keywords_terms.append(term_class_de)

                ordnungskategorie_en = get_row_value(row, 'Classification')
                if ordnungskategorie_en:
                    term_class_en = ET.Element('{%s}term' % NS_TEI)
                    term_class_en.set('type', 'classification')
                    term_class_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                    term_class_en.text = ordnungskategorie_en
                    keywords_terms.append(term_class_en)

            # person_schlagwort -> <term type="person">
            person_schlagwort = get_row_value(row, 'Personenschlagwort')
            person_gnd = get_row_value(row, 'GND Personenschlagwort')
            if person_schlagwort:
                term_person = ET.Element('{%s}term' % NS_TEI)
                term_person.set('type', 'person')
                if person_gnd:
                    term_person.set('ref', person_gnd)
                term_person.text = person_schlagwort
                keywords_terms.append(term_person)

            # werk_schlagwort -> <term type="work">
            werkschlagwort = get_row_value(row, 'Werkschlagwort Dritte')
            werkschlagwort_gnd = get_row_value(row, 'GND Werkschlagwort Dritte')
            if werkschlagwort:
                term_work = ET.Element('{%s}term' % NS_TEI)
                term_work.set('type', 'work')
                if werkschlagwort_gnd:
                    term_work.set('ref', werkschlagwort_gnd)
                term_work.text = werkschlagwort
                keywords_terms.append(term_work)

            # If we have collected any <term> elements, create <keywords> and append them
            if keywords_terms:
                keywords_el = ET.SubElement(textClass, '{%s}keywords' % NS_TEI)
                for term_el in keywords_terms:
                    keywords_el.append(term_el)

                # Map GND Werk (SZ)
                gnd_werk_sz = get_row_value(row, 'GND Werk (SZ)')
                if gnd_werk_sz:
                    term_work = ET.Element('{%s}term' % NS_TEI)
                    term_work.set('type', 'work')
                    term_work.set('ref', f'#SZDWRK.{record_id}')  # Example usage of an ID
                    term_work.text = gnd_werk_sz
                    keywords_terms.append(term_work)

    # Convert the ElementTree to a string
    xml_string = ET.tostring(tei, encoding='utf-8', method='xml')

    # Pretty print the XML
    dom = xml.dom.minidom.parseString(xml_string)
    pretty_xml_as_string = dom.toprettyxml(indent="    ")

    print("Conversion completed. Returning TEI XML as a string.")
    return pretty_xml_as_string

# Example usage of the function:
if __name__ == "__main__":
    # In real usage, adjust the file paths as needed.
    csv_file_path = 'essays.csv'
    facsimilies_xml_path = 'facsimilies-aufsatz-metadata.xml'

    tei_xml_output = csv_to_tei(csv_file_path, facsimilies_xml_path)
    with open('output.xml', 'w', encoding='utf-8') as f:
        f.write(tei_xml_output)

    print("TEI XML output saved to 'output.xml'.")
