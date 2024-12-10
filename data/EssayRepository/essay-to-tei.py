import csv
import xml.etree.ElementTree as ET

def get_row_value(row, field_name):
    return normalize_string(row.get(field_name, ''))

def normalize_string(text):
    """Normalize string by removing unnecessary whitespace."""
    if not text:
        return ''
    # Replace multiple whitespace with single space and strip
    return ' '.join(text.split())

def csv_to_tei(csv_file_path):
    NS_TEI = "http://www.tei-c.org/ns/1.0"
    ET.register_namespace('', NS_TEI)
    NS = {'tei': NS_TEI}

    # Create the root element
    tei = ET.Element('{%s}TEI' % NS_TEI)

    # Create the listBibl element
    listBibl = ET.SubElement(tei, '{%s}listBibl' % NS_TEI)

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row_num, row in enumerate(reader, start=1):
            # Create biblFull element
            biblFull = ET.SubElement(listBibl, '{%s}biblFull' % NS_TEI)
            # Use xml:id="SZDESS.{ID}"
            record_id = get_row_value(row, 'ID')
            biblFull.set('xml:id', f"SZDESS.{record_id}")

            # Create fileDesc element
            fileDesc = ET.SubElement(biblFull, '{%s}fileDesc' % NS_TEI)

            # Create titleStmt
            titleStmt = ET.SubElement(fileDesc, '{%s}titleStmt' % NS_TEI)

            # Map titles
            # Primary title from 'Titel [Vorlage]/title [on document]'
            title_on_document = get_row_value(row, 'Titel [Vorlage]/title [on document]')
            if title_on_document:
                title = ET.SubElement(titleStmt, '{%s}title' % NS_TEI)
                title.text = title_on_document

            # Map 'Titel (erschlossen)' to <title ana="supplied/verified">
            titel_erschlossen = get_row_value(row, 'Titel (erschlossen)')
            if titel_erschlossen:
                title_supplied = ET.SubElement(titleStmt, '{%s}title' % NS_TEI)
                title_supplied.set('ana', 'supplied/verified')
                title_supplied.text = titel_erschlossen

            # <title type="Einheitssachtitel"> from 'Konvoluttitel [entspricht ansonsten "Einheitssachtitel der Werke"]'
            einheitssachtitel_text = get_row_value(row, 'Konvoluttitel [entspricht ansonsten "Einheitssachtitel der Werke"]')
            if einheitssachtitel_text:
                title_einheitssachtitel = ET.SubElement(titleStmt, '{%s}title' % NS_TEI)
                title_einheitssachtitel.set('type', 'Einheitssachtitel')
                title_einheitssachtitel.text = einheitssachtitel_text
            else:
                # If 'Konvoluttitel' is empty, use 'GND Werk (SZ)'
                gnd_werk_sz = get_row_value(row, 'GND Werk (SZ)')
                if gnd_werk_sz:
                    title_einheitssachtitel = ET.SubElement(titleStmt, '{%s}title' % NS_TEI)
                    title_einheitssachtitel.set('type', 'Einheitssachtitel')
                    title_einheitssachtitel.text = gnd_werk_sz

            # <title type="Gesamttitel">Stefan Zweig - Archiv Atrium Press</title>
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
                        author.set('ref', f'#SZDPER.{record_id}')  # Use appropriate ID
                    persName = ET.SubElement(author, '{%s}persName' % NS_TEI)
                    if author_gnd_ref:
                        persName.set('ref', author_gnd_ref)
                    # Split the author_name into surname and forename
                    if ', ' in author_name:
                        surname, forename = author_name.split(', ', 1)
                    else:
                        surname = author_name
                        forename = ''
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
                        # Split the contributor name into surname and forename
                        if ', ' in contributor:
                            surname, forename = contributor.split(', ', 1)
                        else:
                            surname = contributor
                            forename = ''
                        surname_el = ET.SubElement(persName_contrib, '{%s}surname' % NS_TEI)
                        surname_el.text = surname
                        if forename:
                            forename_el = ET.SubElement(persName_contrib, '{%s}forename' % NS_TEI)
                            forename_el.text = forename

            # Map publicationStmt
            publicationStmt = ET.SubElement(fileDesc, '{%s}publicationStmt' % NS_TEI)
            ab = ET.SubElement(publicationStmt, '{%s}ab' % NS_TEI)
            ab.text = 'Archivmaterial'

            # Map sourceDesc
            sourceDesc = ET.SubElement(fileDesc, '{%s}sourceDesc' % NS_TEI)

            # Add publication information if available
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
            idno = ET.SubElement(msIdentifier, '{%s}idno' % NS_TEI)
            idno.set('type', 'signature')
            idno.text = get_row_value(row, 'Signatur/shelfmark')

            # msContents
            text_lang_code = get_row_value(row, 'Sprachencode [dreistellig]') or 'ger'
            if text_lang_code:
                msContents = ET.SubElement(msDesc, '{%s}msContents' % NS_TEI)
                textLang = ET.SubElement(msContents, '{%s}textLang' % NS_TEI)
                lang = ET.SubElement(textLang, '{%s}lang' % NS_TEI)
                lang.set('{http://www.w3.org/XML/1998/namespace}lang', text_lang_code)
                lang.text = 'Deutsch' if text_lang_code == 'ger' else ''

            # Add identifying inscription if available
            identifying_inscription = get_row_value(row, 'Aufschrift erstes Blatt / Identifying Inscription')
            if identifying_inscription:
                # Create msItem to wrap the docEdition elements
                ms_item = ET.SubElement(msContents, '{%s}msItem' % NS_TEI)
                
                # Add German version
                doc_edition_de = ET.SubElement(ms_item, '{%s}docEdition' % NS_TEI)
                doc_edition_de.set('ana', 'szdg:IdentifyingInscription')
                doc_edition_de.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')
                doc_edition_de.text = identifying_inscription

                # Add English version
                doc_edition_en = ET.SubElement(ms_item, '{%s}docEdition' % NS_TEI)
                doc_edition_en.set('ana', 'szdg:IdentifyingInscription')
                doc_edition_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                doc_edition_en.text = identifying_inscription  # Or translated version if available

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

            if writing_instrument:  # Only create English element if there's English content
                # English material element
                material_en = ET.SubElement(support, '{%s}material' % NS_TEI)
                material_en.set('ana', 'szdg:WritingInstrument')
                material_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                material_en.text = writing_instrument

            # extent
            art_umfang_anzahl = get_row_value(row, 'Art, Umfang, Anzahl')
            paginierung = get_row_value(row, 'Paginierung')
            if art_umfang_anzahl or paginierung:
                extent = ET.SubElement(supportDesc, '{%s}extent' % NS_TEI)
                if art_umfang_anzahl:
                    # Split 'Art, Umfang, Anzahl' at the first comma
                    parts = [part.strip() for part in art_umfang_anzahl.split(',', 1)]
                    if parts:
                        # First part is used for <term type="objecttyp">
                        term_text = parts[0]
                        span = ET.SubElement(extent, '{%s}span' % NS_TEI)
                        span.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')
                        term = ET.SubElement(span, '{%s}term' % NS_TEI)
                        term.set('type', 'objecttyp')
                        term.text = term_text
                        if len(parts) > 1:
                            # Remaining text is used for <measure>
                            measure_text = parts[1]
                            measure = ET.SubElement(span, '{%s}measure' % NS_TEI)
                            measure.set('ana', 'corrected')
                            measure.set('type', 'leaf')
                            measure.text = measure_text
                    else:
                        # If splitting fails, use the entire text in <term>
                        span = ET.SubElement(extent, '{%s}span' % NS_TEI)
                        span.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')
                        term = ET.SubElement(span, '{%s}term' % NS_TEI)
                        term.set('type', 'objecttyp')
                        term.text = art_umfang_anzahl

                if paginierung:
                    measure_page = ET.SubElement(extent, '{%s}measure' % NS_TEI)
                    measure_page.set('type', 'page')
                    measure_page.text = paginierung

            # handDesc
            schreiberhand = get_row_value(row, 'Schreiberhand')
            if schreiberhand:
                handDesc = ET.SubElement(physDesc, '{%s}handDesc' % NS_TEI)
                ab_hand_de = ET.SubElement(handDesc, '{%s}ab' % NS_TEI)
                ab_hand_de.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')
                ab_hand_de.text = schreiberhand

            # history
            history = ET.SubElement(msDesc, '{%s}history' % NS_TEI)
            # origin
            origPlace_text = get_row_value(row, 'Entstehungsort/place of creation')
            date_norm = get_row_value(row, 'Datum [normiert]/date [normalized]')
            date_on_document = get_row_value(row, 'Datum [Vorlage]/date [on document]')
            datierung_erschlossen = get_row_value(row, 'Datierung [erschlossen]')
            date_supplied_verified = get_row_value(row, 'Date supplied/verified')

            if origPlace_text or date_norm or date_on_document or datierung_erschlossen:
                origin = ET.SubElement(history, '{%s}origin' % NS_TEI)
                if origPlace_text:
                    origPlace = ET.SubElement(origin, '{%s}origPlace' % NS_TEI)
                    origPlace.text = origPlace_text

                # Map 'Datum [Vorlage]/date [on document]'
                if date_on_document:
                    origDate = ET.SubElement(origin, '{%s}origDate' % NS_TEI)
                    origDate.text = date_on_document
                    if date_norm:
                        origDate.set('when', date_norm)

                # Map 'Datierung [erschlossen]' with ana="supplied/verified"
                if datierung_erschlossen:
                    origDate_supplied = ET.SubElement(origin, '{%s}origDate' % NS_TEI)
                    origDate_supplied.set('ana', 'supplied/verified')
                    origDate_supplied.text = datierung_erschlossen
                    if date_norm:
                        origDate_supplied.set('when', date_norm)

                # Map 'Date supplied/verified' with language tag for English
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
                # Assuming default English translation
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
                # Assuming default English translation
                ab_acq_en = ET.SubElement(acquisition, '{%s}ab' % NS_TEI)
                ab_acq_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                ab_acq_en.text = "Acquisition from Christie's London 2014"

            # profileDesc
            profileDesc = ET.SubElement(biblFull, '{%s}profileDesc' % NS_TEI)
            textClass = ET.SubElement(profileDesc, '{%s}textClass' % NS_TEI)
            # Initialize a list to hold keywords terms
            keywords_terms = []

            # Map Ordnungskategorie [classification]
            ordnungskategorie = get_row_value(row, 'Ordnungskategorie [classification]')
            if ordnungskategorie:
                term_class_de = ET.Element('{%s}term' % NS_TEI)
                term_class_de.set('type', 'classification')
                term_class_de.set('{http://www.w3.org/XML/1998/namespace}lang', 'de')
                term_class_de.text = ordnungskategorie
                keywords_terms.append(term_class_de)
                # Check if English translation is available
                ordnungskategorie_en = get_row_value(row, 'Classification')
                if ordnungskategorie_en:
                    term_class_en = ET.Element('{%s}term' % NS_TEI)
                    term_class_en.set('type', 'classification')
                    term_class_en.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                    term_class_en.text = ordnungskategorie_en
                    keywords_terms.append(term_class_en)

            # Map GND Werk (SZ)
            gnd_werk_sz = get_row_value(row, 'GND Werk (SZ)')
            if gnd_werk_sz:
                term_work = ET.Element('{%s}term' % NS_TEI)
                term_work.set('type', 'work')
                term_work.set('ref', f'#SZDWRK.{record_id}')  # Use appropriate work ID
                term_work.text = gnd_werk_sz
                keywords_terms.append(term_work)

            # Only create <keywords> if there are terms
            if keywords_terms:
                keywords = ET.SubElement(textClass, '{%s}keywords' % NS_TEI)
                for term in keywords_terms:
                    keywords.append(term)

    # Convert the ElementTree to a string
    xml_string = ET.tostring(tei, encoding='utf-8', method='xml')

    # Pretty print the XML
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(xml_string)
    pretty_xml_as_string = dom.toprettyxml(indent="    ")

    return pretty_xml_as_string

# Example usage
tei_xml_output = csv_to_tei('essays.csv')
with open('output.xml', 'w', encoding='utf-8') as f:
    f.write(tei_xml_output)

print("Conversion completed. TEI XML output saved to 'output.xml'.")
