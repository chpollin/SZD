<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0"
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:functx="http://www.functx.com"
	xmlns:gn="http://www.geonames.org/ontology#"
	xmlns:szd="https://gams.uni-graz.at/o:szd.ontology#"
	xmlns:skos="https://gams.uni-graz.at/skos/scheme/o:oth/#" xmlns:t="http://www.tei-c.org/ns/1.0"
	xmlns:dcterms="http://purl.org/dc/terms/" xmlns:wiki="https://www.wikidata.org/wiki/Property:"
	xmlns:gnd="http://d-nb.info/standards/elementset/gnd#"
	xmlns:owl="http://www.w3.org/2002/07/owl#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
	xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:gams="https://gams.uni-graz.at/o:gams-ontology#"
	xmlns:szdg="https://gams.uni-graz.at/o:szd.glossar#"
	xmlns:wgs84_pos="http://www.w3.org/2003/01/geo/wgs84_pos#">

	<!-- author: Christopher Pollin
		date: 2019

		this XSL-T transforms TEI/XML data to RDF/Data. Different TEI-Datasets in SZD are processed.
		every concept, property etc. bases on gams.uni-graz.at/o:szd.ontology
	-->


	<!-- DEFINE global variables -->
	<xsl:variable name="Personlist">
		<xsl:copy-of select="document('https://gams.uni-graz.at/o:szd.personen/TEI_SOURCE')"/>
	</xsl:variable>

	<xsl:variable name="OrganisationList">
		<xsl:copy-of select="document('https://gams.uni-graz.at/o:szd.organisation/TEI_SOURCE')"/>
	</xsl:variable>

	<xsl:variable name="StandorteList">
		<xsl:copy-of select="document('https://gams.uni-graz.at/o:szd.standorte/TEI_SOURCE')"/>
	</xsl:variable>

	<xsl:variable name="Languages">
		<xsl:copy-of
			select="document('http://glossa.uni-graz.at/archive/objects/context:szd/datastreams/LANGUAGES/content')"/>
	</xsl:variable>
	
	<xsl:variable name="Werkindex">
		<xsl:copy-of select="document('https://glossa.uni-graz.at/o:szd.werkindex/TEI_SOURCE')"/>
	</xsl:variable>
	
	<xsl:variable name="BASE_URL" select="'https://gams.uni-graz.at/'"/>
	<xsl:variable name="PID" select="//t:fileDesc/t:publicationStmt/t:idno[@type = 'PID']"/>

	<!-- ///////////////////////////////// -->
	<xsl:template match="/">
		
		<rdf:RDF>
			<xsl:choose>
				<xsl:when
					test="$PID = 'o:szd.bibliothek'">
					<xsl:call-template name="Bibliothek"/>
				</xsl:when>
				<xsl:when
					test="$PID = 'o:szd.autographen'">
					<xsl:call-template name="Autographen"/>
				</xsl:when>
				<xsl:when
					test="$PID = 'o:szd.werke'">
					<xsl:call-template name="Manuskripte"/>
				</xsl:when>
				<xsl:when
					test="$PID = 'o:szd.lebensdokumente'">
					<xsl:call-template name="Lebensdokumente"/>
				</xsl:when>
				<xsl:when
					test="$PID = 'o:szd.personen'">
					<xsl:call-template name="Personen"/>
				</xsl:when>
				<xsl:when
					test="contains($PID, 'lebenskalender')">
					<xsl:call-template name="Lebenskalender"/>
				</xsl:when>
				<xsl:when
					test="$PID = 'o:szd.standorte'">
					<xsl:call-template name="Standorte"/>
				</xsl:when>
				<xsl:when
					test="$PID = 'o:szd.publikation'">
					<xsl:call-template name="Publikation"/>
				</xsl:when>
				<xsl:when
					test="contains($PID, 'o:szd.thema')">
					<xsl:call-template name="Collection"/>
				</xsl:when>
				<xsl:when
					test="contains($PID, 'o:szd.korrespondenzen')">
					<xsl:call-template name="Korrespondenzen"/>
				</xsl:when>
				<xsl:when
					test="contains($PID, 'o:szd.SZDBRI')">
					<szd:Letter>
						<rdf:comment>Prototype</rdf:comment>
					</szd:Letter>
				</xsl:when>
				<xsl:when
					test="contains($PID, 'o:szd.werkindex')">
					<xsl:call-template name="WerkIndex"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:text>No data source define! (like o:szd.bibliothek, o:szd.autographen, o:szd.werke...)</xsl:text>
				</xsl:otherwise>
			</xsl:choose>
		</rdf:RDF>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- szd:BundleOfCorrespondence SZDKOR -->
	<xsl:template name="Korrespondenzen">
		<xsl:for-each select="//t:listBibl/t:biblFull">
			<xsl:variable name="Correspondence_URI" select="concat($BASE_URL, $PID, '#', @xml:id)"/>
			<xsl:variable name="Correspondence_Extent_URI" select="concat($Correspondence_URI, 'EX')"/>
			
			<szd:BundleOfCorrespondence rdf:about="{$Correspondence_URI}">
				
				<xsl:if test="t:fileDesc/t:titleStmt/t:title[@xml:lang='de']">
					<szd:title xml:lang="de">
						<xsl:value-of
							select="normalize-space(t:fileDesc/t:titleStmt/t:title[@xml:lang='de'])"/>
					</szd:title>
				</xsl:if>
				<xsl:if test="t:fileDesc/t:titleStmt/t:title[@xml:lang='en']">
					<szd:title xml:lang="en">
						<xsl:value-of
							select="normalize-space(t:fileDesc/t:titleStmt/t:title[@xml:lang='en'])"/>
					</szd:title>
				</xsl:if>
				<!-- szd:signature -->
				<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno">
					<szd:signature>
						<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno"/>
					</szd:signature>
				</xsl:if>
				<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent">
					<szd:extent rdf:resource="{$Correspondence_Extent_URI}"/>
				</xsl:if>
				
				<xsl:for-each select="t:profileDesc/t:correspDesc/t:correspAction">
					<xsl:choose>
						<xsl:when test="@type = 'sent'">
							<xsl:call-template name="GetPersonlist">
								<xsl:with-param name="Person" select="t:persName/@ref"/>
								<xsl:with-param name="Typ" select="'szd:sender'"/>
							</xsl:call-template>
						</xsl:when>
						<xsl:when test="@type = 'received'">
							<xsl:call-template name="GetPersonlist">
								<xsl:with-param name="Person" select="t:persName/@ref"/>
								<xsl:with-param name="Typ" select="'szd:receiver'"/>
							</xsl:call-template>
						</xsl:when>
						<xsl:otherwise>
							<xsl:comment>Error: missing @type in t:correspAction</xsl:comment>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:for-each>
				
				<!--
				-->
				
				<xsl:call-template name="getLocation"/>
				
				<!-- COLLECTION  -->
				<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.korrespondenzen"/>
				<!-- FULLTEXT -->
				<xsl:call-template name="FulltextSearchData"/>
			</szd:BundleOfCorrespondence>
			
			<!-- extent -->
			<xsl:variable name="EXTENT" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent"/>
			<xsl:variable name="piecesOfCorrespondenc" select="sum($EXTENT/t:measure[@type='correspondence'])"/>
			<xsl:if test="$EXTENT">
				<szd:Extent rdf:about="{$Correspondence_Extent_URI}">
					<xsl:if test="$EXTENT/t:measure[@type='correspondence']">
						<szd:piecesOfCorrespondence>
							<xsl:value-of select="$piecesOfCorrespondenc"/>
						</szd:piecesOfCorrespondence>
					</xsl:if>
					<xsl:if test="$EXTENT/t:measure[@type='enclosures'][@xml:lang='en']">
						<szd:piecesOfEnclosures xml:lang="en">
							<xsl:value-of select="normalize-space($EXTENT/t:measure[@type='enclosures'][@xml:lang='en'])"/>
						</szd:piecesOfEnclosures>
					</xsl:if>
					<xsl:if test="$EXTENT/t:measure[@type='enclosures'][@xml:lang='de']">
						<szd:piecesOfEnclosures xml:lang="de">
							<xsl:value-of select="normalize-space($EXTENT/t:measure[@type='enclosures'][@xml:lang='de'])"/>
						</szd:piecesOfEnclosures>
					</xsl:if>
					<szd:text xml:lang="en">
						<xsl:value-of select="$piecesOfCorrespondenc"/>
						<xsl:choose>
							<xsl:when test="$piecesOfCorrespondenc &gt; 1">
								<xsl:text> Piece of Correspondence</xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text> Pieces of Correspondence</xsl:text>
							</xsl:otherwise>
						</xsl:choose>
						<xsl:if test="$EXTENT/t:measure[@type='enclosures'][@xml:lang='en']">
							<xsl:text> : </xsl:text>
							<xsl:value-of select="normalize-space($EXTENT/t:measure[@type='enclosures'][@xml:lang='en'])"/>
						</xsl:if>
					</szd:text>
					<szd:text xml:lang="de">
						<xsl:value-of select="$piecesOfCorrespondenc"/>
						<xsl:choose>
							<xsl:when test="$piecesOfCorrespondenc &gt; 1">
								<xsl:text> Korrespondenzstücke</xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text> Korrespondenzstück</xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</szd:text>
				</szd:Extent>
			</xsl:if>
		</xsl:for-each>
	</xsl:template>

	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- szd:Book -->
	<xsl:template name="Bibliothek">
		<xsl:for-each select="//t:listBibl/t:biblFull">
			<xsl:variable name="Book_URI" select="concat($BASE_URL, $PID, '#', @xml:id)"/>
			<xsl:variable name="Book_Extent_URI" select="concat($Book_URI, 'EX')"/>
			<xsl:variable name="Book_Publication_URI" select="concat($Book_URI, 'PU')"/>
			<xsl:variable name="Book_ProvenanceCharacteristic_URI" select="concat($Book_URI, 'PC')"/>
			
			<szd:Book rdf:about="{$Book_URI}">
				<xsl:call-template name="Bibliothek_RDF">
					<xsl:with-param name="Book-ID" select="@xml:id"/>
					<xsl:with-param name="Book_Extent_URI" select="$Book_Extent_URI"/>
					<xsl:with-param name="Book_Publication_URI" select="$Book_Publication_URI"/>
					<xsl:with-param name="Book_ProvenanceCharacteristic_URI" select="$Book_ProvenanceCharacteristic_URI"/>
				</xsl:call-template>
				<!-- COLLECTION  -->
				<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.bibliothek"/>
				<!-- FULLTEXT -->
				<xsl:call-template name="FulltextSearchData"/>
			</szd:Book>

			<!-- /////////////////////////////////// -->
			<!-- rdf:about for szd:Book -->
			<!-- Extent -->
			<xsl:if
				test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent">
			
				<szd:Extent
					rdf:about="{$Book_Extent_URI}">
					<!-- page -->
					<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type = 'page']">
						<xsl:call-template name="createTriple">
							<xsl:with-param name="PropertyTyp" select="'data'"/>
							<xsl:with-param name="XPpath"
								select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type = 'page']"/>
							<xsl:with-param name="Property" select="'szd:page'"/>
						</xsl:call-template>
					</xsl:if>
					<!-- format -->
					<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type = 'format']">
						<xsl:call-template name="createTriple">
							<xsl:with-param name="PropertyTyp" select="'data'"/>
							<xsl:with-param name="XPpath"
								select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type = 'format']"/>
							<xsl:with-param name="Property" select="'szd:format'"/>
						</xsl:call-template>
					</xsl:if>
					<!-- binding -->
					<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding">
						<xsl:call-template name="createTriple">
							<xsl:with-param name="PropertyTyp" select="'object'"/>
							<!-- https://gams.uni-graz.at/o:szd.bibliothek#wrapper -->
							<xsl:with-param name="XPpath"
								select="concat($BASE_URL, $PID, '#', replace(normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab[@xml:lang = 'en'][1]), ' ', ''))"/>
							<xsl:with-param name="Property" select="'szd:binding'"/>
						</xsl:call-template>
					</xsl:if>
					
					<!-- //////// -->
					<!-- szd:text -->

					<xsl:call-template name="getExtent_SZDBIB_SZDAUT">
						<xsl:with-param name="locale" select="'en'"/>
						<xsl:with-param name="SZD_ID"/>
					</xsl:call-template>
					<xsl:call-template name="getExtent_SZDBIB_SZDAUT">
						<xsl:with-param name="locale" select="'de'"/>
						<xsl:with-param name="SZD_ID"/>
					</xsl:call-template>

				</szd:Extent>
			</xsl:if>
			<!-- /// -->
			<!-- Publication Statment for szd:Book -->
			<xsl:if test="t:fileDesc/t:publicationStmt">
				<szd:PublicationStmt
					rdf:about="{$Book_Publication_URI}">
					<!-- szd:publisher -->
					<xsl:if test="t:fileDesc/t:publicationStmt/t:publisher">
						<xsl:choose>
							<xsl:when test="t:fileDesc/t:publicationStmt/t:publisher/t:span[@xml:lang]">
								<szd:publisher xml:lang="de">
									<xsl:value-of select="normalize-space(t:fileDesc/t:publicationStmt/t:publisher/t:span[@xml:lang ='de'])"/>
								</szd:publisher>
								<szd:publisher xml:lang="en">
									<xsl:value-of select="normalize-space(t:fileDesc/t:publicationStmt/t:publisher/t:span[@xml:lang ='en'])"/>
								</szd:publisher>
							</xsl:when>
							<xsl:otherwise>
								<szd:publisher>
									<xsl:value-of select="normalize-space(t:fileDesc/t:publicationStmt/t:publisher)"/>
								</szd:publisher>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:if>
					<!-- szd:pubPlace -->
					<xsl:if test="t:fileDesc/t:publicationStmt/t:pubPlace">
						<szd:pubPlace>
							<xsl:value-of select="normalize-space(t:fileDesc/t:publicationStmt/t:pubPlace)"/>
						</szd:pubPlace>
					</xsl:if>
					<!-- szd:pubDate -->
					<xsl:if test="t:fileDesc/t:publicationStmt/t:date">
						<szd:pubDate>
							<szd:pubDateStmt rdf:about="{concat($Book_URI, 'pubDate')}">
								<xsl:if test="t:fileDesc/t:publicationStmt/t:date/@precision">
									<szd:precision><xsl:value-of select="t:fileDesc/t:publicationStmt/t:date/@precision"/></szd:precision>
								</xsl:if>
								<xsl:choose>
										<xsl:when test="t:fileDesc/t:publicationStmt/t:date/t:span[@xml:lang]">
											<szd:text xml:lang="en">
												<xsl:value-of select="normalize-space(t:fileDesc/t:publicationStmt/t:date/t:span[@xml:lang ='en'])"/>
											</szd:text>
											<szd:text xml:lang="de">
												<xsl:value-of select="normalize-space(t:fileDesc/t:publicationStmt/t:date/t:span[@xml:lang ='de'])"/>
											</szd:text>
										</xsl:when>
										<xsl:otherwise>
											<szd:text><xsl:value-of select="normalize-space(t:fileDesc/t:publicationStmt/t:date)"/></szd:text>
										</xsl:otherwise>
									</xsl:choose>					
							</szd:pubDateStmt>
						</szd:pubDate>
					</xsl:if>
					<!-- szd:pubDate -->
					<xsl:if test="t:fileDesc/t:editionStmt/t:edition">
						<szd:edition xml:lang="en">
							<xsl:call-template name="printEnDe">
								<xsl:with-param name="path"
									select="t:fileDesc/t:editionStmt/t:edition/t:span"/>
								<xsl:with-param name="locale" select="'en'"/>
							</xsl:call-template>
						</szd:edition>
						<szd:edition xml:lang="de">
							<xsl:call-template name="printEnDe">
								<xsl:with-param name="path"
									select="t:fileDesc/t:editionStmt/t:edition/t:span"/>
								<xsl:with-param name="locale" select="'de'"/>
							</xsl:call-template>
						</szd:edition>
					</xsl:if>
					<!-- //////// -->
					<!-- szd:text -->
					<szd:text>
						<xsl:if test="t:fileDesc/t:editionStmt/t:edition">
							<xsl:choose>
								<xsl:when
									test="t:fileDesc/t:editionStmt/t:edition/t:span[@xml:lang = 'en']">
									<xsl:value-of
										select="normalize-space(t:fileDesc/t:editionStmt/t:edition/t:span[@xml:lang = 'en'])"
									/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="normalize-space(t:fileDesc/t:editionStmt/t:edition)"/>
								</xsl:otherwise>
							</xsl:choose>
							<!-- auf wunsch im juli 2020 geändert -->
							<xsl:text>. – </xsl:text>
						</xsl:if>
						<!-- pubPlace -->
						<xsl:value-of select="normalize-space(t:fileDesc/t:publicationStmt/t:pubPlace)"/>
						<xsl:text> : </xsl:text>
						<!-- publisher -->
						<xsl:if test="t:fileDesc/t:publicationStmt/t:publisher">
							<xsl:choose>
								<xsl:when test="t:fileDesc/t:publicationStmt/t:publisher/t:span">
									<xsl:value-of
										select="normalize-space(t:fileDesc/t:publicationStmt/t:publisher/t:span[@xml:lang = 'en'])"
									/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="normalize-space(t:fileDesc/t:publicationStmt/t:publisher)"
									/>
								</xsl:otherwise>
							</xsl:choose>
						</xsl:if>
						<xsl:text>, </xsl:text>
						<!-- date -->
						<xsl:choose>
							<xsl:when
								test="t:fileDesc/t:publicationStmt/t:date/t:span[@xml:lang = 'en']">
								<xsl:value-of
									select="normalize-space(t:fileDesc/t:publicationStmt/t:date/t:span[@xml:lang = 'en'])"
								/>
							</xsl:when>
							<xsl:otherwise>
								<xsl:value-of select="normalize-space(t:fileDesc/t:publicationStmt/t:date)"/>
							</xsl:otherwise>
						</xsl:choose>
					</szd:text>
				</szd:PublicationStmt>
			</xsl:if>
			<!-- ProvenanceCharacteristic -->
			<xsl:if
				test="
					t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type = 'provenance'] or
					t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier//t:altIdentifier or
					t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc//t:ab/t:ref or
					t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp">
				<szd:ProvenanceCharacteristic
					rdf:about="{$Book_ProvenanceCharacteristic_URI}">
					<xsl:for-each
						select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type = 'provenance']/t:item">
						<xsl:choose>
							<xsl:when test="t:desc/@xml:lang">
									<xsl:element
										name="{concat('szd:',lower-case(substring-after(t:ref/@target|t:stamp/t:ref/@target, ':')))}">
										<xsl:attribute name="xml:lang" select="'en'"/>
											<xsl:value-of select="normalize-space(t:desc[@xml:lang = 'en'])"/>
									</xsl:element>
									<xsl:element
										name="{concat('szd:',lower-case(substring-after(t:ref/@target|t:stamp/t:ref/@target, ':')))}" xml:lang="de">
										<xsl:attribute name="xml:lang" select="'de'"/>
										<xsl:value-of select="normalize-space(t:desc[@xml:lang = 'de'])"/>
									</xsl:element>
							</xsl:when>
							<xsl:otherwise>
								<xsl:element
									name="{concat('szd:',lower-case(substring-after(t:ref/@target|t:stamp/t:ref/@target, ':')))}">
									<xsl:value-of select="t:desc"/>
								</xsl:element>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:for-each>
					<!-- Nachbesitzer -->
					<xsl:for-each
						select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:ab/t:ref">
						<xsl:element
							name="{concat('szd:',lower-case(substring-after(@target, '#')))}">
							<xsl:value-of select="normalize-space(..)"/>
						</xsl:element>
					</xsl:for-each>
					<!-- Einband -->
					<xsl:for-each
						select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc//t:ab/t:ref">
						<xsl:element
							name="{concat('szd:',lower-case(substring-after(@target, ':')))}">
							<xsl:value-of select="normalize-space(..)"/>
						</xsl:element>
					</xsl:for-each>
					<!--  -->
					<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier//t:altIdentifier">
						<szd:originalShelfmark
							rdf:resource="{concat($Book_ProvenanceCharacteristic_URI, 'OS')}"
						/>
					</xsl:if>
					<!-- stamp -->
					<xsl:for-each
						select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp/t:desc">
						<szd:stamp>
							<xsl:call-template name="printEnDe">
								<xsl:with-param name="locale"/>
								<xsl:with-param name="path" select="."/>
							</xsl:call-template>
						</szd:stamp>
					</xsl:for-each>

					<xsl:for-each select="t:fileDesc//t:ref/@target">
						<szd:glossar
							rdf:resource="{concat($BASE_URL, 'o:szd.glossar#', substring-after(., ':'))}"
						/>
					</xsl:for-each>


					<xsl:for-each
						select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier//t:altIdentifier/@corresp | 
						t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp/t:ref/@target">
						<szd:glossar
							rdf:resource="{concat($BASE_URL, 'o:szd.glossar#', substring-after(., ':'))}"
						/>
					</xsl:for-each>

					<szd:text xml:lang="en">
						<xsl:for-each
							select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type = 'provenance']/t:item/t:term[@xml:lang = 'en'] | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp/t:term[@xml:lang = 'en']">
							<xsl:value-of select="normalize-space(.)"/>
							<xsl:if test="not(position() = last())">
								<xsl:text>,</xsl:text>
							</xsl:if>
						</xsl:for-each>
						<xsl:if test=".//t:msDesc/t:msIdentifier/t:altIdentifier">
							<xsl:if
								test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type = 'provenance'] | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp/t:term">
								<xsl:text>, </xsl:text>
							</xsl:if>
							<xsl:text>Original Shelfmark</xsl:text>
						</xsl:if>
						<xsl:if
							test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:ab/t:ref">
							<xsl:if
								test=".//t:msDesc/t:msIdentifier/t:altIdentifier | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type = 'provenance']/t:item/t:term">
								<xsl:text>, </xsl:text>
							</xsl:if>
							<xsl:text>Later Owner</xsl:text>
						</xsl:if>
					</szd:text>
					<szd:text xml:lang="de">
						<xsl:for-each
							select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type = 'provenance']/t:item/t:term[@xml:lang = 'de'] | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp/t:term[@xml:lang = 'de']">
							<xsl:value-of select="normalize-space(.)"/>
							<xsl:if test="not(position() = last())">
								<xsl:text>, </xsl:text>
							</xsl:if>
						</xsl:for-each>
						<xsl:if test=".//t:msDesc/t:msIdentifier/t:altIdentifier">
							<xsl:if
								test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type = 'provenance'] | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp/t:term">
								<xsl:text>, </xsl:text>
							</xsl:if>
							<xsl:text>Originalsignatur</xsl:text>
						</xsl:if>
						<xsl:if
							test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:ab/t:ref">
							<xsl:if
								test=".//t:msDesc/t:msIdentifier/t:altIdentifier | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type = 'provenance']/t:item/t:term">
								<xsl:text>, </xsl:text>
							</xsl:if>
							<xsl:text>Nachbesitzer</xsl:text>
						</xsl:if>
					</szd:text>
				</szd:ProvenanceCharacteristic>
			</xsl:if>
			<!-- ProvenanceCharacteristic -->
			<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier//t:altIdentifier">
				<szd:OriginalShelfmark
					rdf:about="{concat($Book_ProvenanceCharacteristic_URI, 'OS')}">
					<!-- Originalsiganturen und Hausexemplar -->
					<xsl:for-each
						select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier//t:altIdentifier">
							<xsl:choose>
								<xsl:when test="t:note/t:span">
									<xsl:for-each select="t:note/t:span">
										<xsl:element
											name="{concat('szd:',lower-case(substring-after(../../@corresp, ':')))}">
										<xsl:if test="@xml:lang">
											<xsl:attribute name="xml:lang" select="@xml:lang"/>
										</xsl:if>
										<xsl:value-of select="."/>
										</xsl:element>
									</xsl:for-each>
								</xsl:when>
								<xsl:otherwise>
									<xsl:element
										name="{concat('szd:',lower-case(substring-after(@corresp, ':')))}">
									<xsl:value-of select="t:idno"/>
									</xsl:element>
								</xsl:otherwise>
							</xsl:choose>
						
					</xsl:for-each>
				</szd:OriginalShelfmark>
			</xsl:if>
		</xsl:for-each>
		
		<!-- /// -->
		<!-- szd:Binding for szd:Book -->
		<xsl:for-each-group select="//t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab[@xml:lang = 'en'][1]" group-by=".">
			<szd:Binding rdf:about="{concat($BASE_URL, $PID, '#', replace(normalize-space(.), ' ', ''))}">
				<szd:text xml:lang="en">
					<xsl:call-template name="printEnDe">
						<xsl:with-param name="locale" select="'en'"></xsl:with-param>
						<xsl:with-param name="path" select="."></xsl:with-param>
					</xsl:call-template>
				</szd:text>
				<szd:text xml:lang="de">
					<xsl:call-template name="printEnDe">
						<xsl:with-param name="locale" select="'de'"></xsl:with-param>
						<xsl:with-param name="path" select="../t:ab[@xml:lang = 'de']"></xsl:with-param>
					</xsl:call-template>
				</szd:text>
			</szd:Binding>
		</xsl:for-each-group>
	</xsl:template>

	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///AUTOGRAPHEN/// -->
	<xsl:template name="Autographen">
		<xsl:for-each select="//t:listBibl/t:biblFull">
			<xsl:variable name="Autograph_URI" select="concat($BASE_URL, $PID, '#', @xml:id)"/>
			<xsl:variable name="Autograph_Extent_URI" select="concat($Autograph_URI, 'EX')"/>
			<szd:Autograph
				rdf:about="{$Autograph_URI}">
				<!-- AUTOGRAPHEN DATA -->
				<xsl:call-template name="RDF_autograph">
					<xsl:with-param name="Autograph_Extent_URI" select="$Autograph_Extent_URI"/>
				</xsl:call-template>
				<!-- FULLTEXT -->
				<xsl:call-template name="FulltextSearchData"/>
				<!-- DATASOURCE SPECIFIC RULES  -->
				<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.autographen"
				/>
			</szd:Autograph>
			<!--  -->
			<szd:Extent
				rdf:about="{$Autograph_Extent_URI}">
				<xsl:call-template name="getExtent_SZDBIB_SZDAUT">
					<xsl:with-param name="locale" select="'en'"/>
				</xsl:call-template>
				<xsl:call-template name="getExtent_SZDBIB_SZDAUT">
					<xsl:with-param name="locale" select="'de'"/>
				</xsl:call-template>
			</szd:Extent>
		</xsl:for-each>
	</xsl:template>

	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///LEBENSKALENDAR/// -->
	<xsl:template name="Lebenskalender">
		<xsl:for-each select="//t:listEvent/t:event">

			<szd:BiographicalEvent
				rdf:about="{concat($BASE_URL, $PID, '#',  @xml:id)}">
				<!-- FULLTEXT -->
				<xsl:call-template name="FulltextSearchData"/>
				<!-- DATE -->
				<xsl:choose>
					<xsl:when test="t:head/t:span/t:date/@from">
						<szd:when>
							<xsl:value-of select="t:head/t:span[1]/t:date/@from"/>
						</szd:when>
					</xsl:when>
					<xsl:otherwise>
						<szd:when>
							<xsl:value-of select="t:head/t:span[1]/t:date[1]/@when"/>
						</szd:when>
					</xsl:otherwise>
				</xsl:choose>
				<!-- HEAD -->
				<xsl:if test="t:head/t:span[@xml:lang = 'en']">
					<szd:head xml:lang="en">
						<xsl:value-of select="normalize-space(t:head/t:span[@xml:lang = 'en'])"/>
					</szd:head>
				</xsl:if>
				<xsl:if test="t:head/t:span[@xml:lang = 'de']">
					<szd:head xml:lang="de">
						<xsl:value-of select="normalize-space(t:head/t:span[@xml:lang = 'de'])"/>
					</szd:head>
				</xsl:if>
				<!-- CONTENT -->
				<xsl:if test="t:ab[@xml:lang = 'en']">
					<szd:content xml:lang="en">
						<xsl:value-of select="normalize-space(t:ab[@xml:lang = 'en'])"/>
					</szd:content>
				</xsl:if>
				<xsl:if test="t:ab[@xml:lang = 'de']">
					<szd:content xml:lang="de">
						<xsl:value-of select="normalize-space(t:ab[@xml:lang = 'de'])"/>
					</szd:content>
				</xsl:if>
				<!-- relationsTo -->
				<xsl:for-each select="t:ab/t:name">
					<xsl:choose>
						<xsl:when test="contains(@ref, 'SZDPER')">
							<szd:relationTo
								rdf:resource="{concat($BASE_URL, 'o:szd.personen', @ref)}"
							/>
						</xsl:when>
						<xsl:when test="contains(@ref, 'SZDMSK')">
							<szd:relationTo
								rdf:resource="{concat($BASE_URL, 'o:szd.werke', @ref)}"
							/>
						</xsl:when>
						<xsl:when test="contains(@ref, 'SZDLEB')">
							<szd:relationTo
								rdf:resource="{concat($BASE_URL, 'o:szd.lebensdokumente', @ref)}"
							/>
						</xsl:when>
						<xsl:when test="contains(@ref, 'SZDBIB')">
							<szd:relationTo
								rdf:resource="{concat($BASE_URL, 'o:szd.bibliothek', @ref)}"
							/>
						</xsl:when>
						<xsl:when test="contains(@ref, 'SZDAUT')">
							<szd:relationTo
								rdf:resource="{concat($BASE_URL, 'o:szd.autographen', @ref)}"
							/>
						</xsl:when>
						<xsl:when test="contains(@ref, 'SZDKOR')">
							<xsl:comment>ToDo: szd:relationTo SZDKOR </xsl:comment>
						</xsl:when>
						<xsl:otherwise/>
					</xsl:choose>
				</xsl:for-each>

				<gams:isMemberOfCollection
					rdf:resource="https://gams.uni-graz.at/o:szd.lebenskalender"/>
			</szd:BiographicalEvent>

		</xsl:for-each>
	</xsl:template>

	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///PERSONEN szd:Agent/// -->
	<xsl:template name="Personen">
		<xsl:for-each select="//t:listPerson/t:person">

			<!-- get the RDF resource behind the GND -->
			<xsl:variable name="url" select="string(concat(t:persName/@ref, '/about/lds.rdf'))"/>

			<szd:Agent rdf:about="{concat($BASE_URL, $PID, '#', @xml:id)}">
				<xsl:if test="t:idno[@type = 'wikidata']">
					<szd:wikidata rdf:resource="{t:idno[@type='wikidata']}"/>
				</xsl:if>
				<xsl:if test="t:persName/@ref">
					<szd:gnd rdf:resource="{t:persName/@ref}"/>
				</xsl:if>

				<!-- gnd identifier -->

				<!-- viaf identifier -->
				<!-- https://www.wikidata.org/wiki/Property:P214 -->

				<!-- wiki:P734 forename | t:surname
					 gnd:forename surname | t:forename
					 wiki:P2561 foaf:name (alternative name) | t:name
				-->
				<xsl:choose>
					<!-- process first "Ausgabename" (how it should appear in SZD) than "Normalisiert" (Name in GND) than "Ansetzungsname" (in the Source)  -->
					<xsl:when test="t:persName[not(@type = 'variant')]/t:name">
						<szd:name>
							<xsl:value-of select="t:persName[not(@type = 'variant')]/t:name"/>
						</szd:name>
					</xsl:when>
					<xsl:otherwise>
						<xsl:if test="t:persName[not(@type = 'variant')]/t:forename">
							<szd:forename>
								<xsl:value-of select="t:persName[not(@type)]/t:forename"/>
							</szd:forename>
						</xsl:if>
						<xsl:if test="t:persName[not(@type = 'variant')]/t:surname">
							<szd:surname>
								<xsl:value-of select="t:persName[not(@type)]/t:surname"/>
							</szd:surname>
						</xsl:if>
					</xsl:otherwise>
				</xsl:choose>
				<!-- wikipedia -->
				<xsl:if test="@corresp">
					<foaf:page rdf:resource="{@corresp}"/>
				</xsl:if>
				<!-- wikipedia -->
				<xsl:if test="idno[@type = 'wikidata']">
					<owl:seeAlso rdf:resource="{idno[@type='wikidata']}"/>
				</xsl:if>
				<!-- date of birth -->
				<xsl:if test="t:birth/@when">
					<szd:birth>
						<xsl:call-template name="getDate">
							<!-- fix in PersonToTEI, that only valid dates are inside @when -->
							<xsl:with-param name="Date" select="t:birth/@when"/>
						</xsl:call-template>
					</szd:birth>
				</xsl:if>
				<!-- date of death -->
				<xsl:if test="t:death/@when">
					<szd:death>
						<xsl:call-template name="getDate">
							<xsl:with-param name="Date" select="t:death/@when"/>
						</xsl:call-template>
					</szd:death>
				</xsl:if>
				<!-- FULLTEXT -->
				<gams:textualContent>
					<xsl:for-each select=".//*/text()">
						<!-- remove ';' and ',' -->
						<xsl:value-of
							select="normalize-space(replace(replace(normalize-unicode(.), ';', ''), ',', ''))"/>
						<xsl:text> </xsl:text>
					</xsl:for-each>
					<!-- adding ID like SZDBIB.n -->
					<xsl:if test="@xml:id">
						<xsl:value-of select="@xml:id"/>
					</xsl:if>
				</gams:textualContent>
				<!-- COLLECTION -->
				<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.personen"/>
			</szd:Agent>

		</xsl:for-each>
	</xsl:template>


	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///Orte szd:Place/// -->
	<!--<xsl:template name="Orte">
		<xsl:for-each select="//t:listPlace/t:place">

			<szd:Place rdf:about="{concat($BASE_URL, o:szd.orte#', @xml:id)}">
				<!-\- GeoNames Ontology -\->
				<gn:geonamesID rdf:resource="{t:placeName/@ref}"/>
				<gn:name>
					<xsl:value-of select="t:placeName"/>
				</gn:name>
				<!-\- FULLTEXT -\->
				<xsl:call-template name="FulltextSearchData"/>
				<!-\- COLLECTION -\->
				<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.orte"/>
			</szd:Place>

		</xsl:for-each>
	</xsl:template>-->


	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///Organisation/// -->
	<!--<xsl:template name="Organisation">
		<xsl:for-each select="//t:listOrg/t:org">

			<szd:Org rdf:about="{concat($BASE_URL, $PID, '#', @xml:id)}">
				<!-\- PERSON DATA -\->
				<szd:name>
					<xsl:value-of select="t:orgName"/>
				</szd:name>
				<gnd:gndIdentifier rdf:resource="{t:orgName/@ref}"/>

				<!-\- FULLTEXT -\->
				<xsl:call-template name="FulltextSearchData"/>
				<!-\- COLLECTION -\->
				<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.organisation"/>
			</szd:Org>

		</xsl:for-each>
	</xsl:template>-->

	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///STANDORTE szd:Location/// -->
	<xsl:template name="Standorte">
		<xsl:for-each select="//t:listOrg/t:org">
			<szd:Location rdf:about="{concat($BASE_URL, $PID, '#', @xml:id)}">
				<xsl:choose>
					<xsl:when test="t:orgName/@xml:lang = 'en'">
						<szd:name xml:lang="en">
							<xsl:call-template name="printEnDe">
								<xsl:with-param name="locale" select="'en'"/>
								<xsl:with-param name="path" select="t:orgName"/>
							</xsl:call-template>
							<!---->
						</szd:name>
					</xsl:when>
					<xsl:when test="t:orgName/@xml:lang = 'de'">
						<szd:name xml:lang="en">
							<xsl:call-template name="printEnDe">
								<xsl:with-param name="locale" select="'de'"/>
								<xsl:with-param name="path" select="t:orgName"/>
							</xsl:call-template>
						</szd:name>
					</xsl:when>
					<xsl:otherwise>
						<szd:name>
							<xsl:value-of select="normalize-space(t:orgName)"/>
						</szd:name>
					</xsl:otherwise>
				</xsl:choose>

				<xsl:if test="t:settlement">
					<szd:settlement>
						<xsl:value-of select="normalize-space(t:settlement)"/>
					</szd:settlement>
				</xsl:if>
				<xsl:if test="t:orgName/@ref">
					<gnd:gndIdentifier rdf:resource="{t:orgName/@ref}"/>
				</xsl:if>
				<xsl:if test="@corresp">
					<rdfs:seeAlso rdf:resource="{@corresp}"/>
				</xsl:if>
				<xsl:if test="t:location/t:geo">
					<wgs84_pos:lat>
						<xsl:value-of
							select="normalize-space(substring-before(t:location/t:geo, ','))"/>
					</wgs84_pos:lat>
					<wgs84_pos:long>
						<xsl:value-of
							select="normalize-space(substring-after(t:location/t:geo, ','))"/>
					</wgs84_pos:long>
				</xsl:if>

				<!-- FULLTEXT -->
				<xsl:call-template name="FulltextSearchData"/>
				<!-- COLLECTION -->
				<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.standorte"/>
			</szd:Location>

		</xsl:for-each>
	</xsl:template>


	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///PUBLIKATION WORK biblFull (like Silberne Saiten. Gedichte : Schuster & Loeffler, Berlin / Leipzig | 1901) /// -->
	<xsl:template name="Publikation">
		<xsl:for-each select="//t:listBibl/t:biblFull">
			<szd:Publication
				rdf:about="{concat($BASE_URL, $PID, '#', @xml:id)}">
				<!-- /////////////////////// -->
				<!-- TITLE -->
				<xsl:if test="t:fileDesc/t:titleStmt/t:title[@xml:lang = 'en']">
					<szd:title xml:lang="en">
						<xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@xml:lang = 'en']"/>
					</szd:title>
				</xsl:if>
				<xsl:if test="t:fileDesc/t:titleStmt/t:title[@xml:lang = 'de']">
					<szd:title xml:lang="de">
						<xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@xml:lang = 'de']"/>
					</szd:title>
				</xsl:if>
				<!-- /////////////////////// -->
				<!-- szd:author, @roles -->
				<xsl:choose>
					<xsl:when test="t:fileDesc/t:titleStmt/t:author[not(@role)]/t:persName/@ref">
						<xsl:call-template name="GetPersonlist">
							<xsl:with-param name="Person"
								select="t:fileDesc/t:titleStmt/t:author[not(@role)]/t:persname/@ref"/>
							<xsl:with-param name="Typ" select="'szd:author'"/>
						</xsl:call-template>
					</xsl:when>
					<xsl:when test="t:fileDesc/t:titleStmt/t:author[not(@role)]/t:persName">
						<szd:author>
							<xsl:value-of
								select="t:fileDesc/t:titleStmt/t:author[not(@role)]/t:persName/t:forename"/>
							<xsl:text> </xsl:text>
							<xsl:value-of
								select="t:fileDesc/t:titleStmt/t:author[not(@role)]/t:persName/t:surname"
							/>
						</szd:author>
					</xsl:when>
					<xsl:otherwise>
						<xsl:comment>error</xsl:comment>
					</xsl:otherwise>
				</xsl:choose>
				<!-- /////////////////////// -->
				<!-- publicationStmt -->
				<xsl:for-each select="t:fileDesc/t:publicationStmt/t:publisher">
					<szd:publisher>
						<xsl:value-of select="."/>
					</szd:publisher>
				</xsl:for-each>
				<xsl:for-each select="t:fileDesc/t:publicationStmt/t:pubPlace">
					<szd:pubPlace>
						<xsl:value-of select="."/>
					</szd:pubPlace>
				</xsl:for-each>
				<xsl:for-each select="t:fileDesc/t:publicationStmt/t:date">
					<szd:date>
						<xsl:value-of select="."/>
					</szd:date>
				</xsl:for-each>

				<!-- FULLTEXT -->
				<xsl:call-template name="FulltextSearchData"/>
				<!-- COLLECTION -->
				<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.publikation"/>
				<xsl:if test="t:fileDesc/t:titleStmt/t:title/@ref">
					<owl:sameAs rdf:resource="{t:fileDesc/t:titleStmt/t:title/@ref}"/>
				</xsl:if>
			</szd:Publication>
		</xsl:for-each>
		<!-- //////////////////////////////////////////////////////////////////////////////////// -->
		<!-- ///PUBLIKATION Chapter, bibl (like Zur Einleitung: Was ins Weite einst geflogen…, S.9)/// -->
		<xsl:for-each select="//t:listBibl/t:bibl">
			<szd:Publication
				rdf:about="{concat($BASE_URL, $PID, '#', @xml:id)}">
				<!-- TITLE -->
				<xsl:if test="t:fileDesc/t:titleStmt/t:title[@xml:lang = 'en']">
					<szd:title xml:lang="en">
						<xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@xml:lang = 'en']"/>
					</szd:title>
				</xsl:if>
				<xsl:if test="t:fileDesc/t:titleStmt/t:title[@xml:lang = 'de']">
					<szd:title xml:lang="de">
						<xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@xml:lang = 'de']"/>
					</szd:title>
				</xsl:if>
				<!-- szd:author = Stefan Zweig -->

				<!-- FULLTEXT -->
				<xsl:call-template name="FulltextSearchData"/>
				<!-- COLLECTION -->
				<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.publikation"/>
				<owl:sameAs rdf:resource="{t:title/@ref}"/>
			</szd:Publication>
			<xsl:for-each select="t:bibl">
				<szd:Publication
					rdf:about="{concat($BASE_URL, $PID, '#', @xml:id)}">
					<!-- TITLE -->
					<szd:title>
						<xsl:value-of select="t:title"/>
					</szd:title>
					<!-- szd:author = Stefan Zweig -->
					<szd:author rdf:resource="https://gams.uni-graz.at/o:szd.personen#SZDPER.1560"/>
					<!-- FULLTEXT -->
					<xsl:call-template name="FulltextSearchData"/>
					<!-- COLLECTION -->
					<gams:isMemberOfCollection
						rdf:resource="https://gams.uni-graz.at/o:szd.publikation"/>
					<dcterms:partOf rdf:resource="{../@xml:id}"/>
					<owl:sameAs rdf:resource="{t:title/@ref}"/>
				</szd:Publication>
			</xsl:for-each>

		</xsl:for-each>


	</xsl:template>

	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///Werk - szd:WORK/// -->
	<xsl:template name="Manuskripte">
		<xsl:for-each select="//t:listBibl/t:biblFull">
			<xsl:variable name="Work_URI" select="concat($BASE_URL, $PID, '#', @xml:id)"/>
			<xsl:variable name="Work_Extent_URI" select="concat($Work_URI, 'EX')"/>
			<xsl:variable name="Work_Enclosure_URI" select="concat($Work_URI, 'EN')"/>
			<!-- sameAs bibo:Manuscript -->
			<szd:Work rdf:about="{$Work_URI}">
				<!-- GET BASIC DATA: author, title, date, place -->
				<xsl:call-template name="Work_RDF">
					<xsl:with-param name="Work_URI" select="$Work_URI"/>
					<xsl:with-param name="Work_Extent_URI" select="$Work_Extent_URI"/>
					<xsl:with-param name="Work_Enclosure_URI" select="$Work_Enclosure_URI"/>
				</xsl:call-template>
				<!-- FULLTEXT -->
				<xsl:call-template name="FulltextSearchData"/>
				<!-- COLLECTION -->
				<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.werke"/>
			</szd:Work>
			<!-- ////////////////////////////////// -->
			<!-- szd:Extent szd:Work -->
			<szd:Extent rdf:about="{$Work_Extent_URI}">
				<xsl:call-template name="getExtentMSK">
					<xsl:with-param name="locale" select="'en'"/>
				</xsl:call-template>
				<xsl:call-template name="getExtentMSK">
					<xsl:with-param name="locale" select="'de'"/>
				</xsl:call-template>
			</szd:Extent>
			<!-- ////////////////////////////////// -->
			<!-- szd:Enclosure  szd:Work -->
			<xsl:call-template name="getEnclosure">
				<xsl:with-param name="Work_Enclosure_URI" select="$Work_Enclosure_URI"/>
			</xsl:call-template>
		</xsl:for-each>
	</xsl:template>

	<!-- ///Werkindex --><!-- Wo ist der dann einzusetzen? -->
	<xsl:template name="WerkIndex">
		<xsl:for-each select="//t:listBibl/t:bibl">
				<xsl:variable name="WerkIndex_URI" select="concat($BASE_URL, $PID, '#', @xml:id)"/>
				<szd:WorkIndexEntry 
					rdf:about="{$WerkIndex_URI}">
					<!-- TITLE -->
					<szd:title>
						<xsl:value-of select="normalize-space(t:title)"/>
					</szd:title>
					<xsl:if test="t:title/@ref"><gnd:gndIdentifier rdf:resource="{t:title/@ref}"/></xsl:if>
					<!-- szd:author = Stefan Zweig -->
					<szd:author rdf:resource="https://gams.uni-graz.at/o:szd.personen#SZDPER.1560"/>
					<xsl:if
						test="t:term">
						<xsl:variable name="CurrentCategory"
							select="t:term"/>
						<szd:category>
							<xsl:attribute name="rdf:resource">
								<xsl:choose>
									<xsl:when test="$CurrentCategory = 'Romane'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Novel</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Autobiographie'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Autobiography</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Biographien'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Biography</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Erzählungen'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Stories</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Drama'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Drama</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Essay'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Essay</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Vorworte'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Foreword</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Historische Miniaturen'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#HistoricalMiniature</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Interview'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Interview</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Journalistische Arbeiten'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#JournalisticWork</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Film'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Movie</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Erzählung'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Movie</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Vorträge'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Narration</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Notizbücher'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Notebook</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Prosa'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Prose</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Romane'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Novel</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Reden'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Speech</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Übersetzung'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Translation</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Werknotizen'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Worknote</xsl:text>
									</xsl:when>
									<xsl:when test="$CurrentCategory = 'Tagebücher'">
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Diary</xsl:text>
									</xsl:when>
									<xsl:otherwise>
										<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Work</xsl:text>
									</xsl:otherwise>
								</xsl:choose>
							</xsl:attribute>
						</szd:category>
					</xsl:if>
					<xsl:if test="t:publisher/t:origDate">
						<szd:creation><!-- Orientierung an pubDate -->
						<szd:creationStmt rdf:about="{concat($WerkIndex_URI, 'creation')}">
							<szd:text><xsl:value-of select="normalize-space(t:publisher/t:origDate)"/></szd:text>
						</szd:creationStmt>
					</szd:creation>
					</xsl:if>
				</szd:WorkIndexEntry>
				<!-- vorher ein xsl:if? -->
				<szd:Publication>
					<xsl:if test="t:publisher/t:date">
						<szd:pubDate>
						<!-- von Book --><szd:pubDateStmt rdf:about="{concat($WerkIndex_URI, 'pubDate')}">
							<!--<xsl:choose>
								<xsl:when test="t:fileDesc/t:publicationStmt/t:date/t:span[@xml:lang]">
									<szd:text xml:lang="en">
										<xsl:value-of select="normalize-space(t:fileDesc/t:publicationStmt/t:date/t:span[@xml:lang ='en'])"/>
									</szd:text>
									<szd:text xml:lang="de">
										<xsl:value-of select="normalize-space(t:fileDesc/t:publicationStmt/t:date/t:span[@xml:lang ='de'])"/>
									</szd:text>
								</xsl:when>-->
								<szd:text><xsl:value-of select="normalize-space(t:publisher/t:date)"/></szd:text>
							<!--</xsl:choose>-->					
						</szd:pubDateStmt>
					</szd:pubDate>
					</xsl:if>
					<xsl:call-template name="getLanguage">
						<xsl:with-param name="path" select="t:lang"/>
					</xsl:call-template>
				</szd:Publication>
			</xsl:for-each>
			
		
	</xsl:template>

	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///Lebensdokumente - szd:PersonalDocument/// -->
	<xsl:template name="Lebensdokumente">
		
		<xsl:for-each select="//t:listBibl/t:biblFull">
			<xsl:variable name="PersonalDocument_URI" select="concat($BASE_URL, $PID, '#',  @xml:id)"/>
			<xsl:variable name="PersonalDocument_Extent_URI" select="concat($PersonalDocument_URI, 'EX')"/>
			<xsl:variable name="PersonalDocument_Enclosure_URI" select="concat($PersonalDocument_URI, 'EN')"/>
			<!-- sameAs bibo:Manuscript -->
			<szd:PersonalDocument
				rdf:about="{$PersonalDocument_URI}">
				<!-- GET BASIC DATA: author, title, date, place -->
				<xsl:call-template name="Work_RDF">
					<xsl:with-param name="Work_URI" select="$PersonalDocument_URI"/>
					<xsl:with-param name="Work_Extent_URI" select="$PersonalDocument_Extent_URI"/>
					<xsl:with-param name="Work_Enclosure_URI" select="$PersonalDocument_Enclosure_URI"/>
				</xsl:call-template>
				<!-- FULLTEXT -->
				<xsl:call-template name="FulltextSearchData"/>
				<!-- COLLECTION -->
				<gams:isMemberOfCollection
					rdf:resource="https://gams.uni-graz.at/o:szd.lebensdokumente"/>
			</szd:PersonalDocument>
			<!-- ////////////////////////////////// -->
			<!-- szd:Extent szd:PersonalDocument -->
			<szd:Extent
				rdf:about="{$PersonalDocument_Extent_URI}">
				<xsl:call-template name="getExtentMSK">
					<xsl:with-param name="locale" select="'en'"/>
				</xsl:call-template>
				<xsl:call-template name="getExtentMSK">
					<xsl:with-param name="locale" select="'de'"/>
				</xsl:call-template>
			</szd:Extent>
			<!-- ////////////////////////////////// -->
			<!-- szd:Enclosure szd:PersonalDocument -->
			<xsl:call-template name="getEnclosure">
				<xsl:with-param name="Work_Enclosure_URI" select="$PersonalDocument_Enclosure_URI"/>
			</xsl:call-template>
		</xsl:for-each>
	</xsl:template>
	
	<xsl:template name="getEnclosure">
		<xsl:param name="Work_Enclosure_URI"/>
		<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:accMat/t:list/t:item[@ana='szdg:Enclosures']">
			<xsl:choose>
				<!-- Enclosure has is own SZDMSK id -->
				<xsl:when test="t:ref[@ana = 'szd:hasContentRelation']">
					
				</xsl:when>
				<xsl:when test="t:ref[@ana = 'szd:hasPhysicalRelation']">
					
				</xsl:when>
				<xsl:otherwise>
					<szd:Enclosur rdf:about="{$Work_Enclosure_URI}">
						<xsl:choose>
							<xsl:when test="t:desc/@xml:lang">
								<szd:desc xml:lang="en">
									<xsl:value-of select="normalize-space(t:desc[@xml:lang='en'])"/>
								</szd:desc>
								<szd:desc xml:lang="de">
									<xsl:value-of select="normalize-space(t:desc[@xml:lang='de'])"/>
								</szd:desc>
							</xsl:when>
							<xsl:otherwise>
								<szd:desc>
									<xsl:value-of select="normalize-space(t:desc[1])"/>
								</szd:desc>
							</xsl:otherwise>
						</xsl:choose>
						<xsl:call-template name="createTriple">
							<xsl:with-param name="PropertyTyp" select="'data'"/>
							<xsl:with-param name="XPpath" select="t:measure[@type = 'format']"/>
							<xsl:with-param name="Property" select="'szd:format'"/>
						</xsl:call-template>
					</szd:Enclosur>
				</xsl:otherwise>
			</xsl:choose>
			
		</xsl:for-each>
	</xsl:template>

	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///COLLECTION/// -->
	<xsl:template name="Collection">
		<szd:Collection
			rdf:about="{concat($BASE_URL, $PID)}">
			<!-- szd:title -->
			<szd:title>
				<xsl:value-of select="//t:teiHeader//t:titleStmt/t:title"/>
			</szd:title>

			<xsl:for-each-group select="//t:div/t:head/t:title" group-by="@ref">
				<xsl:choose>
					<xsl:when test="contains(@ref, ' ')">
						<xsl:for-each select="tokenize(current-grouping-key(), ' ')">
							<szd:connectedWithDocument rdf:resource="{.}"/>
						</xsl:for-each>
					</xsl:when>
					<xsl:otherwise>
						<szd:connectedWithDocument rdf:resource="{current-grouping-key()}"/>
					</xsl:otherwise>
				</xsl:choose>

			</xsl:for-each-group>
			<!--<xsl:for-each-group select="//t:body//t:div//t:name[@type='work']" group-by="@ref">
				<szd:connectedWithDocument rdf:resource="{concat($BASE_URL, ', current-grouping-key())}"/>
			</xsl:for-each-group>-->
			<xsl:for-each-group select="//t:body//t:div//t:name[@type = 'person']" group-by="@ref">
				<szd:connectedWithPerson
					rdf:resource="{concat($BASE_URL, $PID, '#', current-grouping-key())}"
				/>
			</xsl:for-each-group>
			<!-- FULLTEXT -->
			<gams:textualContent>
				<xsl:value-of select="//t:titleStmt/t:title"/>
				<xsl:text> </xsl:text>
				<xsl:for-each select="//t:text//text()">
					<xsl:value-of select="normalize-space(.)"/>
					<xsl:text> </xsl:text>
				</xsl:for-each>

			</gams:textualContent>
			<!-- COLLECTION -->
			<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/context:szd"/>
		</szd:Collection>
	</xsl:template>




	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- TEMPLATES -->


	<!-- ///CREATE DATA FOR FULLTEXTSEARCH/// -->
	<!-- get the fulltext of every data entry and normalizes the text (unicode and whitespaces) -->
	<xsl:template name="FulltextSearchData">
		<gams:textualContent>
			<xsl:for-each select=".//*/text()">
				<xsl:value-of select="normalize-space(normalize-unicode(.))"/>
				<xsl:text> </xsl:text>
			</xsl:for-each>
			<xsl:variable name="GND">
				<!-- Further add variant names of author to the resource -->
				<xsl:choose>
					<xsl:when test="t:fileDesc/t:titleStmt/t:author/t:persName">
						<xsl:value-of select="t:fileDesc/t:titleStmt/t:author/t:persName/@ref"/>
					</xsl:when>
					<xsl:when test="t:titleStmt/t:author/t:persName">
						<xsl:value-of select="t:titleStmt/t:author/t:persName/@ref"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="t:fileDesc/t:titleStmt/t:author/@ref"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>
			<!-- adding variantname for fulltextsearch -->
			<xsl:for-each
				select="$Personlist//t:person/t:persName[@ref = $GND]/following-sibling::t:persName[@type = 'Variantname']">
				<xsl:value-of select="normalize-unicode(.)"/>
				<xsl:text> </xsl:text>
			</xsl:for-each>
			<!-- adding ID like SZDBIB.n -->
			<xsl:if test="@xml:id">
				<xsl:value-of select="@xml:id"/>
			</xsl:if>
			<!-- adding language -->
			<xsl:for-each select=".//t:textLang/t:lang">
				<xsl:variable name="Actual" select="."/>
				<xsl:for-each select="$Languages//*:entry">
					<!-- comparing string, iso-code -->
					<xsl:if test="*:code[@type = 'ISO639-2'] = $Actual">
						<xsl:text> </xsl:text>
						<xsl:value-of select="*:language[@type = 'german']"/>
						<xsl:text> </xsl:text>
						<xsl:value-of select="*:language[@type = 'english']"/>
						<xsl:text> </xsl:text>
					</xsl:if>
				</xsl:for-each>
			</xsl:for-each>
		</gams:textualContent>
	</xsl:template>

	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///RDF_bibliothek/// -->
	<xsl:template name="Bibliothek_RDF">
		<xsl:param name="Book-ID"/>
		<xsl:param name="Book_Extent_URI"/>
		<xsl:param name="Book_Publication_URI"/>
		<xsl:param name="Book_ProvenanceCharacteristic_URI"/>

		<!-- szd:title -->
		<xsl:call-template name="getTitle"/>

		<xsl:if test="t:fileDesc/t:titleStmt/t:title[@type = 'original']">
			<szd:originaltitle>
				<xsl:value-of
					select="normalize-space(t:fileDesc/t:titleStmt/t:title[@type = 'original'])"/>
			</szd:originaltitle>
		</xsl:if>

		<!-- szd:author  -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:author[not(@role)]/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person"
					select="t:fileDesc/t:titleStmt/t:author[not(@role)]/@ref"/>
				<xsl:with-param name="Typ" select="'szd:author'"/>
			</xsl:call-template>
		</xsl:if>
		<!-- szd:composer -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:author[@role = 'composer']/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person"
					select="t:fileDesc/t:titleStmt/t:author[@role = 'composer']/@ref"/>
				<xsl:with-param name="Typ" select="'szd:composer'"/>
			</xsl:call-template>
		</xsl:if>
		<!-- szd:editor -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:editor[not(@role)]/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person"
					select="t:fileDesc/t:titleStmt/t:editor[not(@role)]/@ref"/>
				<xsl:with-param name="Typ" select="'szd:editor'"/>
			</xsl:call-template>
		</xsl:if>
		<!-- szd:illustrator -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:editor[@role = 'illustrator']/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person"
					select="t:fileDesc/t:titleStmt/t:editor[@role = 'illustrator']/@ref"/>
				<xsl:with-param name="Typ" select="'szd:illustrator'"/>
			</xsl:call-template>
		</xsl:if>
		<!-- szd:translator -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:editor[@role = 'translator']/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person"
					select="t:fileDesc/t:titleStmt/t:editor[@role = 'translator']/@ref"/>
				<xsl:with-param name="Typ" select="'szd:translator'"/>
			</xsl:call-template>
		</xsl:if>
		<!-- szd:writerForeword -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:author[@role = 'preface']/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person"
					select="t:fileDesc/t:titleStmt/t:author[@role = 'preface']/@ref"/>
				<xsl:with-param name="Typ" select="'szd:writerForeword'"/>
			</xsl:call-template>
		</xsl:if>
		<!-- szd:writerAfterword -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:author[@role = 'afterword']/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person"
					select="t:fileDesc/t:titleStmt/t:author[@role = 'afterword']/@ref"/>
				<xsl:with-param name="Typ" select="'szd:writerAfterword'"/>
			</xsl:call-template>
		</xsl:if>

		<!-- person -->
		<xsl:call-template name="GetPersonlist">
			<xsl:with-param name="Person"
				select="t:profileDesc/t:textClass/t:keywords/t:term[@type = 'person']/@ref"/>
			<xsl:with-param name="Typ" select="'szd:relationToPerson'"/>
		</xsl:call-template>

		<xsl:for-each select="t:profileDesc/t:textClass/t:keywords/t:term[@type = 'work']/@ref">
			<szd:realtionToWork rdf:resource="{.}"/>
		</xsl:for-each>

		<!--Publication Details-->
		<xsl:if test="t:fileDesc/t:publicationStmt">
			<szd:publicationStmt
				rdf:resource="{$Book_Publication_URI}"
			/>
		</xsl:if>

		<!--Series-->
		<!-- szd:series -->
		<xsl:if test="t:fileDesc/t:seriesStmt/t:title">
			<szd:series>
				<xsl:value-of select="t:fileDesc/t:seriesStmt/t:title"/>
			</szd:series>
		</xsl:if>

		<!-- Language -->
		<xsl:call-template name="getLanguage">
			<xsl:with-param name="path" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang/t:lang"/>
		</xsl:call-template>

		<!-- szd:location -->
		<xsl:call-template name="getLocation"/>
		

		<!-- szd:signature -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno">
			<szd:signature>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno"/>
			</szd:signature>
		</xsl:if>

		<!-- ////////////// -->
		<!-- Extent -->
		<xsl:if
			test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent">
			<szd:extent
				rdf:resource="{$Book_Extent_URI}"
			/>
		</xsl:if>

		<xsl:call-template name="getProvenance"/>


		<!-- illustriert -->

		<!-- szd:provenanceCharacteristic -->
		<xsl:if
			test="
				t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type = 'provenance'] or
				t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier//t:altIdentifier or
				t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc//t:ab/t:ref or
				t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp">
			<szd:provenanceCharacteristic
				rdf:resource="{$Book_ProvenanceCharacteristic_URI}"
			/>
		</xsl:if>

		<!-- ////////////// -->
		<!-- Umfang, extent -->
		<xsl:for-each
			select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:span">
			<xsl:call-template name="createTriple">
				<xsl:with-param name="XPpath" select="."/>
				<!-- name of the property -->
				<xsl:with-param name="Property" select="'szd:extent'"/>
				<!-- data or object property; param "data" or "object" -->
				<xsl:with-param name="PropertyTyp" select="'data'"/>
			</xsl:call-template>
		</xsl:for-each>

	</xsl:template>

	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///szd:Work/// -->
	<xsl:template name="Work_RDF">
		<xsl:param name="Work_URI"/>
		<xsl:param name="Work_Extent_URI"/>
		<xsl:param name="Work_Enclosure_URI"/>
		<!-- szd:title -->
		<xsl:call-template name="getTitle"/>

		<!-- person -->
		<xsl:call-template name="GetPersonlist">
			<xsl:with-param name="Person"
				select="t:profileDesc/t:textClass/t:keywords/t:term[@type = 'person']/@ref"/>
			<xsl:with-param name="Typ" select="'szd:relationToPerson'"/>
		</xsl:call-template>

		<!-- Ordnungskateroire = GND-Sachgruppe -->
		<xsl:if
			test="t:profileDesc/t:textClass/t:keywords/t:term[@type = 'classification'][@xml:lang = 'de']">
			<xsl:variable name="CurrentCategory"
				select="t:profileDesc/t:textClass/t:keywords/t:term[@type = 'classification'][@xml:lang = 'de']"/>
			<szd:category>
				<xsl:attribute name="rdf:resource">
					<xsl:choose>
						<xsl:when test="$CurrentCategory = 'Romane'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Novel</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Autobiographie'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Autobiography</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Biographien'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Biography</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Erzählungen'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Stories</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Drama'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Drama</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Essay'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Essay</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Vorworte'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Foreword</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Historische Miniaturen'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#HistoricalMiniature</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Interview'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Interview</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Journalistische Arbeiten'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#JournalisticWork</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Film'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Movie</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Erzählung'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Movie</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Vorträge'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Narration</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Notizbücher'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Notebook</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Prosa'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Prose</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Romane'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Novel</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Reden'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Speech</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Übersetzung'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Translation</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Werknotizen'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Worknote</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Tagebücher'">
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Diary</xsl:text>
						</xsl:when>
						<xsl:otherwise>
							<xsl:text>https://gams.uni-graz.at/o:szd.glossar#Work</xsl:text>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute>
			</szd:category>
		</xsl:if>

		<!-- /// -->
		<!-- szd:author: define Stefan zweig as szd:author if not an explicitly other author is mentioned, as Zweig is always author of his works and personal documents  -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:author">
			<xsl:choose>
				<xsl:when test="not(t:fileDesc/t:titleStmt/t:author[@ref = 'SZDPER.1560'])">
					<xsl:for-each select="t:fileDesc/t:titleStmt/t:author/@ref">
						<szd:author
							rdf:resource="{concat('https://gams.uni-graz.at/o:szd.personen', .)}"/>
					</xsl:for-each>
				</xsl:when>
				<!-- szd:author = Stefan Zweig -->
				<xsl:otherwise>
					<szd:author rdf:resource="https://gams.uni-graz.at/o:szd.personen#SZDPER.1560"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
		
		<!-- Datum -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:origin/t:origDate/@when">
			<szd:dateOfPublication>
				<xsl:value-of
					select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:origin/t:origDate/@when"/>
			</szd:dateOfPublication>
		</xsl:if>

		<!-- Signatur -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno">
			<szd:signature>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno"/>
			</szd:signature>
		</xsl:if>

		<!-- Objekttyp -->
		<xsl:if test=".//t:extent/t:span[@xml:lang = 'de']/t:term[@type = 'objecttyp']">
			<szd:objecttyp xml:lang="de">
				<xsl:value-of
					select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:span[@xml:lang = 'de']/t:term[@type = 'objecttyp']"
				/>
			</szd:objecttyp>
		</xsl:if>
		<xsl:if test=".//t:extent/t:span[@xml:lang = 'en']/t:term[@type = 'objecttyp']">
			<szd:objecttyp xml:lang="en">
				<xsl:value-of
					select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:span[@xml:lang = 'en']/t:term[@type = 'objecttyp']"
				/>
			</szd:objecttyp>
		</xsl:if>

		<!-- szd:location  -->
		<xsl:choose>
			<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ana">
				<szd:location
					rdf:resource="{t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ana}"
				/>
			</xsl:when>
			<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository">
				<xsl:call-template name="GetStandortelist">
					<xsl:with-param name="Standort"
						select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository"/>
					<xsl:with-param name="Typ" select="'szd:location'"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise/>
		</xsl:choose>

		<xsl:for-each select=".//*[contains(@ana, 'szdg:')][1]">
			<szd:glossar
				rdf:resource="{concat($BASE_URL, 'o:szd.glossar#', substring-after(@ana, 'szdg:'))}"
			/>
		</xsl:for-each>

		<xsl:if test=".//t:incipit[1]">
			<szd:glossar rdf:resource="https://gams.uni-graz.at/o:szd.glossar#Incipit"/>
		</xsl:if>

		<xsl:if test=".//t:origDate[1]">
			<szd:glossar rdf:resource="https://gams.uni-graz.at/o:szd.glossar#Date"/>
		</xsl:if>

		<!-- szd:lang -->
		<xsl:call-template name="getLanguage">
			<xsl:with-param name="path" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang/t:lang"/>
		</xsl:call-template>

		<!-- Extent -->
		<xsl:if
			test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent">
			<szd:extent
				rdf:resource="{$Work_Extent_URI}"/>
		</xsl:if>

		<!-- provenance -->
		<xsl:call-template name="getProvenance"/>

		<!-- acquisition -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition">
			<xsl:choose>
				<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition/t:ab[@xml:lang]">
					<szd:acquired xml:lang="en">
						<xsl:value-of
							select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition/t:ab[@xml:lang ='en'])"
						/>
					</szd:acquired>
					<szd:acquired xml:lang="de">
						<xsl:value-of
							select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition/t:ab[@xml:lang ='de'])"
						/>
					</szd:acquired>
				</xsl:when>
				<xsl:otherwise>
					<szd:acquired>
						<xsl:value-of
							select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition[1])"
						/>
					</szd:acquired>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>

		<!-- Identifying Inscription -->
		<xsl:if
			test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:docEdition[@xml:lang = 'de']">
			<szd:identifyingInscription xml:lang="de">
				<xsl:value-of
					select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:docEdition[@xml:lang = 'de']"
				/>
			</szd:identifyingInscription>
		</xsl:if>
		<xsl:if
			test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:docEdition[@xml:lang = 'en']">
			<szd:identifyingInscription xml:lang="en">
				<xsl:value-of
					select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:docEdition[@xml:lang = 'en']"
				/>
			</szd:identifyingInscription>
		</xsl:if>

		<!-- Schreibmaterial -->
		<!-- ana="https://gams.uni-graz.at/o:szd.glossar#WritingMaterial"  -->
		<xsl:if
			test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'szdg:WritingMaterial')][@xml:lang = 'de']">
			<szd:writingMaterial xml:lang="de">
				<xsl:value-of
					select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'szdg:WritingMaterial')][@xml:lang = 'de']"
				/>
			</szd:writingMaterial>
		</xsl:if>
		<xsl:if
			test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'szdg:WritingMaterial')][@xml:lang = 'en']">
			<szd:writingMaterial xml:lang="en">
				<xsl:value-of
					select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'szdg:WritingMaterial')][@xml:lang = 'en']"
				/>
			</szd:writingMaterial>
		</xsl:if>

		<!-- Beschreibmaterial -->
		<xsl:if
			test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'szdg:WritingInstrument')][@xml:lang = 'de']">
			<szd:writingInstrument xml:lang="de">
				<xsl:value-of
					select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'szdg:WritingInstrument')][@xml:lang = 'de']"
				/>
			</szd:writingInstrument>
		</xsl:if>
		<xsl:if
			test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'szdg:WritingInstrument')][@xml:lang = 'en']">
			<szd:writingInstrument xml:lang="en">
				<xsl:value-of
					select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'szdg:WritingInstrument')][@xml:lang = 'en']"
				/>
			</szd:writingInstrument>
		</xsl:if>

		<!-- Schreiberhand -->
		<!-- this should be a reference to a SZDPER-ID -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:handDesc/t:ab">
			<szd:secretarialHand xml:lang="en">
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:handDesc/t:ab[@xml:lang = 'de']"/>
			</szd:secretarialHand>
			<szd:secretarialHand xml:lang="de">
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:handDesc/t:ab[@xml:lang = 'en']"/>
			</szd:secretarialHand>
		</xsl:if>

		<!-- Einband -->
		<!-- this should be a reference to a binding-taxonomy -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab[@xml:lang='en']">
			<xsl:call-template name="createTriple">
				<xsl:with-param name="Property" select="'szd:binding'"/>
				<xsl:with-param name="PropertyTyp" select="'object'"/>
				<xsl:with-param name="XPpath"
					select="concat($BASE_URL, $PID, '#', replace(normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab[@xml:lang = 'en'][1]), ' ', ''))"/>
			</xsl:call-template>
		</xsl:if>

		<!-- Beilagen -->
		<!-- szdg:Enclosures -->
		<!-- reference to enclosures-uri -->
		<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:accMat/t:list/t:item[@ana = 'szdg:Enclosures']">
			<xsl:choose>
				<xsl:when test="t:ref[@ana = 'szd:hasContentRelation']">
					<szd:hasContentRelation rdf:resource="{concat($Work_URI, @ref)}"/>
				</xsl:when>
				<xsl:when test="t:ref[@ana = 'szd:hasPhysicalRelation']">
					<szd:hasPhysicalRelation rdf:resource="{concat($Work_URI, @ref)}"/>
				</xsl:when>
				<xsl:otherwise>
					<szd:enclosures rdf:resource="{$Work_Enclosure_URI}"/>
				</xsl:otherwise>
			</xsl:choose>
			<!-- Enclosure has is own SZDMSK id -->
			
			
		</xsl:for-each>

		<!-- Zusatzmaterial -->
		<!-- szdg:Enclosures -->
		<!-- this should be a reference to a SZDPER-ID -->
		<xsl:for-each
			select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:accMat/t:list/t:item[contains(@ana, 'szdg:AdditionalMaterial')]">
			<xsl:choose>
				<xsl:when test="t:desc[@xml:lang]">
					<xsl:for-each select="t:desc[@xml:lang='en']">
						<szd:additionalMaterial xml:lang="en">
							<xsl:value-of select="normalize-space(.)"/>
						</szd:additionalMaterial>
					</xsl:for-each>
					<xsl:for-each select="t:desc[@xml:lang='de']">
						<szd:additionalMaterial xml:lang="de">
							<xsl:value-of select="normalize-space(.)"/>
						</szd:additionalMaterial>
					</xsl:for-each>
				</xsl:when>
				<xsl:otherwise>
					<szd:additionalMaterial>
						<xsl:value-of select="normalize-space(t:desc[1])"/>
					</szd:additionalMaterial>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>

		<!-- Note, Hinweis -->
		<xsl:if test="t:fileDesc/t:notesStmt/t:note[@xml:lang = 'de']">
			<szd:note xml:lang="de">
				<xsl:value-of select="t:fileDesc/t:notesStmt/t:note[@xml:lang = 'de']"/>
			</szd:note>
		</xsl:if>
		<xsl:if test="t:fileDesc/t:notesStmt/t:note[@xml:lang = 'en']">
			<szd:note xml:lang="en">
				<xsl:value-of select="t:fileDesc/t:notesStmt/t:note[@xml:lang = 'en']"/>
			</szd:note>
		</xsl:if>

		<!-- Incipit -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:incipit">
			<szd:incipit>
				<xsl:value-of
					select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:incipit"/>
			</szd:incipit>
		</xsl:if>

		<!--  -->
		<xsl:for-each-group select="t:fileDesc/t:titleStmt/t:editor[@role = 'contributor']"
			group-by="@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="current-grouping-key()"/>
				<xsl:with-param name="Typ" select="'szd:partyInvolved'"/>
			</xsl:call-template>
		</xsl:for-each-group>

	</xsl:template>


	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///RDF_autograph/// -->
	<xsl:template name="RDF_autograph">
		<xsl:param name="Autograph_Extent_URI"/>

		<xsl:call-template name="getTitle"/>
		<!-- szd:author -->
		<xsl:for-each select="t:fileDesc/t:titleStmt/t:author[not(@role)]/t:persName">
			<xsl:choose>
				<xsl:when test="@ref">
					<xsl:call-template name="GetPersonlist">
						<xsl:with-param name="Person" select="@ref"/>
						<xsl:with-param name="Typ" select="'szd:author'"/>
					</xsl:call-template>
				</xsl:when>
				<!-- author has a @ref -->
				<xsl:when test="../@ref">
					<xsl:call-template name="GetPersonlist">
						<xsl:with-param name="Person" select="../@ref"/>
						<xsl:with-param name="Typ" select="'szd:author'"/>
					</xsl:call-template>
				</xsl:when>
				<xsl:otherwise>
					<xsl:comment>Error: no GND or SZDPER found</xsl:comment>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>

		<!-- szd:composer -->
		<xsl:call-template name="GetPersonlist">
			<xsl:with-param name="Person"
				select="t:fileDesc/t:titleStmt/t:author[@role = 'composer']/t:persName/@ref"/>
			<xsl:with-param name="Typ" select="'szd:composer'"/>
		</xsl:call-template>

		<xsl:for-each-group select="t:profileDesc/t:textClass/t:keywords/t:term[@type = 'person']"
			group-by="@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="current-grouping-key()"/>
				<xsl:with-param name="Typ" select="'szd:partyInvolved'"/>
			</xsl:call-template>
		</xsl:for-each-group>

		<xsl:for-each-group
			select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary/t:persName"
			group-by="@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="current-grouping-key()"/>
				<xsl:with-param name="Typ" select="'szd:relationToPerson'"/>
			</xsl:call-template>
		</xsl:for-each-group>

		<!-- affected person -->
		<xsl:for-each
			select="t:profileDesc/t:textClass/t:keywords/t:term[@type = 'person_affected']/t:persName/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="."/>
				<xsl:with-param name="Typ" select="'szd:affectedPerson'"/>
			</xsl:call-template>
		</xsl:for-each>

		<!-- summary -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary">
			<xsl:call-template name="getEnDe">
				<xsl:with-param name="XPpath" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary/t:span"/>
				<xsl:with-param name="Type" select="'szd:content'"></xsl:with-param>
			</xsl:call-template>
			
			<!--<szd:content>
				<xsl:value-of
					select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary)"
				/>
			</szd:content>-->
		</xsl:if>

		<!-- szd:location  -->
		<xsl:choose>
			<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:span[text() = 'unbekannt']">
				<szd:location rdf:resource="https://gams.uni-graz.at/context:szd#unknown"/>
			</xsl:when>
			<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/*/t:orgName/@ref">
				<xsl:for-each
					select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/*/t:orgName/@ref">
					<xsl:call-template name="GetStandortelist">
						<xsl:with-param name="Standort" select="."/>
						<xsl:with-param name="Typ" select="'szd:location'"/>
					</xsl:call-template>
				</xsl:for-each>
			</xsl:when>
			<xsl:otherwise>
				<szd:location rdf:resource="https://gams.uni-graz.at/context:szd#unknown"/>
			</xsl:otherwise>
		</xsl:choose>
		
		<!-- languagecode -->
		<xsl:call-template name="getLanguage">
			<xsl:with-param name="path" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang/t:lang"/>
		</xsl:call-template>		

		<!-- extent for SZDAUT -->
		<szd:extent
			rdf:resource="{$Autograph_Extent_URI}"/>

		<!-- provenance for SZDAUT -->
		<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance">
			<xsl:call-template name="getEnDe">
				<xsl:with-param name="XPpath" select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:span"/>
				<xsl:with-param name="Type" select="'szd:provenance'"/>
			</xsl:call-template>
		</xsl:for-each>

		<!-- acquired -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition">
			<xsl:call-template name="getEnDe">
				<xsl:with-param name="XPpath" select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition/t:span"/>
				<xsl:with-param name="Type" select="'szd:acquired'"/>
			</xsl:call-template>
			<!--<szd:acquired>
				<xsl:value-of
					select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition)"
				/>
			</szd:acquired>-->
		</xsl:if>
	</xsl:template>

	<!-- Template taking @ref = GND and goes through o:szd.personen for getting the intern #SZDPER
	all #SZDPER.n are in the triplestore when o:szd.personen is ingested. -->
	<xsl:template name="GetPersonlist">
		<xsl:param name="Person"/>
		<xsl:param name="Typ"/>
		<xsl:choose>
			<xsl:when test="$Person">
				<xsl:for-each select="$Person">
					<xsl:variable name="String">
						<xsl:choose>
							<xsl:when test="contains(., ' ')">
								<xsl:value-of select="substring-before(., ' ')"/>
							</xsl:when>
							<xsl:otherwise>
								<xsl:value-of select="string(.)"/>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:variable>
					<xsl:variable name="SZDPER"
						select="$Personlist//t:person[t:persName[contains(@ref, $String)]]/@xml:id"/>
					<!-- check if there is a GND-Ref, otherwise all empty gnd would be listed -->
					<xsl:choose>
						<!-- if @ref is a GND-ID -->
						<xsl:when test="substring-after($String, 'd-nb.info/gnd/')">
							<xsl:for-each select="$SZDPER">
								<xsl:element name="{$Typ}">
									<xsl:attribute name="rdf:resource">
										<xsl:value-of
											select="concat($BASE_URL, 'o:szd.personen', '#', .)"
										/>
									</xsl:attribute>
								</xsl:element>
							</xsl:for-each>
						</xsl:when>
						<!-- if @ref = SZDPER -->
						<xsl:when test="contains($String, '#SZDPER.')">
							<xsl:element name="{$Typ}">
								<xsl:attribute name="rdf:resource">
									<xsl:value-of
										select="concat($BASE_URL, 'o:szd.personen', $String)"
									/>
								</xsl:attribute>
							</xsl:element>
						</xsl:when>
						<xsl:otherwise/>
					</xsl:choose>
				</xsl:for-each>
			</xsl:when>
			<xsl:otherwise/>
		</xsl:choose>
	</xsl:template>

	<!-- ///////////////////////////////// -->
	<!-- creates valid dates, only valid dates get a @rdf:datatype = date -->
	<xsl:template name="getDate">
		<xsl:param name="Date"/>
		<xsl:choose>
			<xsl:when test="$Date/@when castable as xs:date">
				<xsl:attribute name="rdf:datatype" select="'http://www.w3.org/2001/XMLSchema#date'"/>
				<xsl:value-of select="normalize-space($Date/@when)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="normalize-space($Date)"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<!-- Template taking @ref = GND and goues through o:szd.organisation for getting the intern #SZDORG
	all #SZDPER.n are in the triplestore when o:szd.personen is ingested. -->
	<xsl:template name="GetOrglist">
		<xsl:param name="Org"/>
		<xsl:param name="Typ"/>
		<xsl:for-each select="$Org">
			<xsl:variable name="String" select="string(.)"/>
			<xsl:variable name="SZDORG"
				select="$OrganisationList//t:org[t:orgName[@ref = $String]]/@xml:id"/>
			<!-- check if there is a GND-Ref, otherwise all empty gnd would be listed -->
			<xsl:if test="substring-after($String, 'http://d-nb.info/gnd/')">
				<xsl:for-each select="$SZDORG">
					<xsl:element name="{$Typ}">
						<xsl:attribute name="rdf:resource">
							<xsl:value-of
								select="concat($BASE_URL, 'o:szd.standorte', '#', .)"/>
						</xsl:attribute>
					</xsl:element>
				</xsl:for-each>
			</xsl:if>
		</xsl:for-each>
	</xsl:template>

	<xsl:template name="GetStandortelist">
		<xsl:param name="Standort"/>
		<xsl:param name="Typ"/>
		<xsl:choose>
			<xsl:when test="$Standort = 'Privatbesitz'">
				<xsl:if test="normalize-space($Standort/../t:settlement)">
					<xsl:element name="{$Typ}">
						<xsl:variable name="String"
							select="concat(normalize-space($Standort), ', ', normalize-space($Standort/../t:settlement))"/>
						<xsl:attribute name="rdf:resource">
							<xsl:value-of
								select="concat($BASE_URL, 'o:szd.standorte', $StandorteList//t:org[t:orgName = $String]/@xml:id)"
							/>
						</xsl:attribute>
					</xsl:element>
				</xsl:if>
			</xsl:when>
			<xsl:when test="$StandorteList//t:org[t:orgName = normalize-space($Standort)]/@xml:id">
				<xsl:element name="{$Typ}">
					<xsl:attribute name="rdf:resource">
						<xsl:value-of
							select="concat($BASE_URL, 'o:szd.standorte', '#', $StandorteList//t:org[t:orgName = normalize-space($Standort)]/@xml:id)"
						/>
					</xsl:attribute>
				</xsl:element>
			</xsl:when>
			<xsl:when test="$StandorteList//t:org[t:orgName/@ref = $Standort]/@xml:id">
				<xsl:element name="{$Typ}">
					<xsl:attribute name="rdf:resource">
						<xsl:value-of
							select="concat($BASE_URL, 'o:szd.standorte', '#', $StandorteList//t:org[t:orgName/@ref = normalize-space($Standort)][1]/@xml:id)"
						/>
					</xsl:attribute>
				</xsl:element>
			</xsl:when>
			<xsl:when test="contains($Standort, '#SZDSTA')">
				<xsl:element name="{$Typ}">
					<xsl:attribute name="rdf:resource">
						<xsl:value-of select="$Standort"/>
					</xsl:attribute>
				</xsl:element>
			</xsl:when>
			<xsl:when test="$StandorteList//t:org[t:orgName/@ref = $Standort/@ref]/@xml:id">
				<xsl:element name="{$Typ}">
					<xsl:attribute name="rdf:resource">
						<xsl:value-of
							select="concat($BASE_URL, 'o:szd.standorte', '#', $StandorteList//t:org[t:orgName/@ref = $Standort/@ref]/@xml:id)"
						/>
					</xsl:attribute>
				</xsl:element>
			</xsl:when>
			<xsl:otherwise/>
		</xsl:choose>
	</xsl:template>

	<xsl:template name="GetPlace">
		<xsl:param name="Place"/>
		<xsl:param name="Type"/>
		<xsl:variable name="String" select="string(.)"/>
		<xsl:value-of select="$String"/>
		<xsl:value-of select="$StandorteList//t:place[t:placeName[@ref = $String]]/@xml:id"/>
		<!--<xsl:element name="{$Type}">
			<xsl:attribute name="rdf:resource">
				<xsl:value-of select="$BASE_URLo:szd.orte#'"/>
			</xsl:attribute>
		</xsl:element>-->


		<!--<xsl:for-each select="$Place">
			<xsl:variable name="String" select="string(.)"/>
			<xsl:variable name="SZDORT" select="$PlacesList//t:place[t:placeName[@ref = $String]]/@xml:id"/>
			<!-\- check if there is a GND-Ref, otherwise all empty gnd would be listed -\->
			<xsl:value-of select="$String"/>
			<xsl:if test="substring-after($String, 'http://www.geonames.org/')">
				<xsl:for-each select="$SZDORT">
					<xsl:element name="{$Type}">
						<xsl:attribute name="rdf:resource">
							<xsl:value-of select="concat($BASE_URL, o:szd.orte#', .)"/>
						</xsl:attribute>
					</xsl:element>
				</xsl:for-each>
			</xsl:if>
		</xsl:for-each>-->
	</xsl:template>

	<!-- /////////////////////////////////////////////////////////// -->
	<!-- ///LANGUAGES/// -->
	<!-- called when iso-lanuage is found in TEI, checks with $Languages, which is a simple .xml. datastream in context:szd -->
	<xsl:template name="languageCode">
		<xsl:param name="Current"/>
		<xsl:for-each select="$Languages//*:entry">
			<!-- comparing string, iso-code -->
			<xsl:if test="*:code[@type = 'ISO639-2'] = $Current">
				<xsl:value-of select="*:language[@type = 'german']"/>
			</xsl:if>
		</xsl:for-each>
	</xsl:template>

	<xsl:template name="getLanguage">
		<xsl:param name="path"/>
		<xsl:for-each select="$path">
			<xsl:choose>
				<xsl:when test="@xml:lang">
					<xsl:for-each select="@xml:lang">
						<szd:language
							rdf:resource="{concat('http://id.loc.gov/vocabulary/iso639-2/', normalize-space(.))}"/>
					</xsl:for-each>
				</xsl:when>
				<xsl:otherwise>
					<szd:language>
						<xsl:value-of select="normalize-space(.)"/>
					</szd:language>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
	</xsl:template>

	<!-- /////////////////////////////////////////// -->
	<xsl:template name="createTriple">
		<xsl:param name="Property"/>
		<xsl:param name="PropertyTyp"/>
		<xsl:param name="XPpath"/>

		<xsl:choose>
			<!-- data property with literal -->
			<xsl:when test="$PropertyTyp = 'data'">
				<xsl:choose>
					<!-- check xml:lang -->
					<!-- ToDo: EN DE Binding -->

					<xsl:when test="$XPpath/@xml:lang = 'en'">
						<xsl:element name="{$Property}">
							<xsl:attribute name="xml:lang" select="'en'"/>
							<xsl:call-template name="printEnDe">
								<xsl:with-param name="locale" select="$XPpath/@xml:lang"/>
								<xsl:with-param name="path" select="$XPpath[@xml:lang = 'en']"/>
							</xsl:call-template>
							<!--<xsl:value-of select="normalize-space($XPpath)"/>-->
						</xsl:element>
					</xsl:when>
					<xsl:when test="$XPpath/@xml:lang = 'de'">
						<xsl:element name="{$Property}">
							<xsl:attribute name="xml:lang" select="'de'"/>
							<xsl:call-template name="printEnDe">
								<xsl:with-param name="locale" select="$XPpath/@xml:lang"/>
								<xsl:with-param name="path" select="$XPpath[@xml:lang = 'de']"/>
							</xsl:call-template>
							<!--<xsl:value-of select="normalize-space($XPpath)"/>-->
						</xsl:element>
					</xsl:when>
					<xsl:otherwise>
						<xsl:element name="{$Property}">
							<xsl:value-of select="normalize-space($XPpath)"/>
						</xsl:element>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<!-- object property with rdf:resource -->
			<xsl:when test="$PropertyTyp = 'object'">
				<xsl:element name="{$Property}">
					<xsl:attribute name="rdf:resource">
						<xsl:value-of select="normalize-space($XPpath)"/>
					</xsl:attribute>
				</xsl:element>
			</xsl:when>
			<xsl:otherwise>
				<xsl:comment>Error: $PropertyTyp in createTriple is wrong</xsl:comment>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>

	<xsl:template name="getExtent_SZDBIB_SZDAUT">
		<xsl:param name="locale"/>
		<xsl:param name="SZD_ID"/>
		<xsl:variable name="EXTENT"
			select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent"/>
		<xsl:if test="$EXTENT">
			<szd:text>
				<xsl:attribute name="xml:lang">
					<xsl:choose>
						<xsl:when test="$locale = 'en'">
							<xsl:text>en</xsl:text>
						</xsl:when>
						<xsl:otherwise>
							<xsl:text>de</xsl:text>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute>
				<xsl:if test="$EXTENT/t:measure[@type = 'page']">
					<xsl:choose>
						<xsl:when test="$EXTENT/t:measure[@type = 'page']/t:span">
							<xsl:value-of
								select="normalize-space($EXTENT/t:measure[@type = 'page']/t:span[@xml:lang = $locale])"
							/>
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="normalize-space($EXTENT/t:measure[@type = 'page'])"/>
						</xsl:otherwise>
					</xsl:choose>
					<xsl:text> </xsl:text>
					<xsl:choose>
						<xsl:when test="$EXTENT/t:measure[@type = 'page'] = '1'">
							<xsl:choose>
								<xsl:when test="$locale = 'en'">
									<xsl:text>page</xsl:text>
								</xsl:when>
								<xsl:otherwise>
									<xsl:text>Seite</xsl:text>
								</xsl:otherwise>
							</xsl:choose>
						</xsl:when>
						<xsl:otherwise>
							<xsl:choose>
								<xsl:when test="$locale = 'en'">
									<xsl:text>pages</xsl:text>
								</xsl:when>
								<xsl:otherwise>
									<xsl:text>Seiten</xsl:text>
								</xsl:otherwise>
							</xsl:choose>
						</xsl:otherwise>
					</xsl:choose>
					<xsl:choose>
						<xsl:when test="$EXTENT/t:measure[@type = 'leaf']">
							<xsl:text>, </xsl:text>
						</xsl:when>
						<xsl:when
							test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type = 'extent']/t:item">
							<xsl:text> : </xsl:text>
						</xsl:when>
						<xsl:otherwise>
							<xsl:if test="contains($SZD_ID, 'SZDBIB')">
								<xsl:text>. </xsl:text>
							</xsl:if>
							<xsl:text> </xsl:text>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:if>
				<xsl:if test="$EXTENT/t:measure[@type = 'leaf']">
					<xsl:value-of select="normalize-space($EXTENT/t:measure[@type = 'leaf'])"/>
					<xsl:text> </xsl:text>
					<xsl:choose>
						<xsl:when test="$EXTENT/t:measure[@type = 'leaf'] = '1'">
							<xsl:text> Blatt </xsl:text>
						</xsl:when>
						<xsl:otherwise>
							<xsl:choose>
								<xsl:when test="$locale = 'en'">
									<xsl:text> leaves </xsl:text>
								</xsl:when>
								<xsl:otherwise>
									<xsl:text> Blatt </xsl:text>
								</xsl:otherwise>
							</xsl:choose>
						</xsl:otherwise>
					</xsl:choose>
					<xsl:text> </xsl:text>
				</xsl:if>
				<!-- illustriert, Karte, Noten -->
				<!-- <item><span xml:lang="de">illustriert</span><span xml:lang="en">illustrated</span></item>
                      <item><span xml:lang="de">Karten</span><span xml:lang="en">maps</span></item> -->
				<xsl:for-each
					select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type = 'extent']/t:item">
					<xsl:choose>
						<xsl:when test="position() = last()">
							<xsl:choose>
								<xsl:when test="$locale = 'en'">
									<xsl:call-template name="printEnDe">
										<xsl:with-param name="locale" select="'en'"/>
										<xsl:with-param name="path" select="t:span"/>
									</xsl:call-template>
								</xsl:when>
								<xsl:otherwise>
									<xsl:call-template name="printEnDe">
										<xsl:with-param name="locale" select="'de'"/>
										<xsl:with-param name="path" select="t:span"/>
									</xsl:call-template>
								</xsl:otherwise>
							</xsl:choose>
							<xsl:text>. </xsl:text>
						</xsl:when>
						<xsl:otherwise>
							<xsl:choose>
								<xsl:when test="$locale = 'en'">
									<xsl:call-template name="printEnDe">
										<xsl:with-param name="locale" select="'en'"/>
										<xsl:with-param name="path" select="t:span"/>
									</xsl:call-template>
								</xsl:when>
								<xsl:otherwise>
									<xsl:call-template name="printEnDe">
										<xsl:with-param name="locale" select="'de'"/>
										<xsl:with-param name="path" select="t:span"/>
									</xsl:call-template>
								</xsl:otherwise>
							</xsl:choose>
							<xsl:text>, </xsl:text>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:for-each>
				<xsl:text> </xsl:text>
				<!-- FORMAT -->
				<xsl:choose>
					<xsl:when test="$EXTENT/t:measure[@type = 'format']/t:span[@xml:lang]">
						<xsl:value-of select="$EXTENT/t:measure[@type = 'format']/t:span[@xml:lang = $locale]"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="$EXTENT/t:measure[@type = 'format']"/>
					</xsl:otherwise>
				</xsl:choose>
				<!-- BINDING -->
				<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab">
					<xsl:text>, </xsl:text>
					<xsl:choose>
						<xsl:when test="$locale = 'en'">
							<xsl:call-template name="printEnDe">
								<xsl:with-param name="locale" select="'en'"/>
								<xsl:with-param name="path" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab"/>
							</xsl:call-template>
						</xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="printEnDe">
								<xsl:with-param name="locale" select="'de'"/>
								<xsl:with-param name="path" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab"/>
							</xsl:call-template>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:if>
			</szd:text>
		</xsl:if>
	</xsl:template>

	<xsl:template name="getExtentMSK">
		<xsl:param name="locale"/>
		<xsl:variable name="EXTENT"
			select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent"/>
		<szd:text>
			<xsl:attribute name="xml:lang">
				<xsl:choose>
					<xsl:when test="$locale = 'en'">
						<xsl:text>en</xsl:text>
					</xsl:when>
					<xsl:otherwise>
						<xsl:text>de</xsl:text>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:attribute>
			<xsl:value-of select="normalize-space($EXTENT/t:span[@xml:lang = $locale])"/>
			<xsl:choose>
				<xsl:when test="$EXTENT/t:measure[@type = 'format'][@xml:lang = $locale]">
					<xsl:text>, </xsl:text>
					<xsl:value-of select="normalize-space($EXTENT/t:measure[@type = 'format'][@xml:lang = $locale])"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:text>, </xsl:text>
					<xsl:value-of select="normalize-space($EXTENT/t:measure[@type = 'format'])"/>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:if
				test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:foliation/t:ab">
				<xsl:text>, </xsl:text>
				<xsl:value-of
					select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:foliation/t:ab[@xml:lang = $locale])"
				/>
			</xsl:if>
			<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab">
				<xsl:text>, </xsl:text>
				<xsl:value-of
					select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab[@xml:lang = $locale])"
				/>
			</xsl:if>
		</szd:text>
	</xsl:template>

	<!-- //////// -->
	<!-- getTitle -->
	<xsl:template name="getTitle">
		<szd:title xml:lang="de">
			<xsl:choose>
				<xsl:when test="t:fileDesc/t:titleStmt/t:title[@xml:lang = 'de']">
					<xsl:value-of
						select="normalize-space(t:fileDesc/t:titleStmt/t:title[@xml:lang = 'de'][1])"
					/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[1])"/>
				</xsl:otherwise>
			</xsl:choose>
		</szd:title>
		<szd:title xml:lang="en">
			<xsl:choose>
				<xsl:when test="t:fileDesc/t:titleStmt/t:title[@xml:lang = 'en']">
					<xsl:value-of
						select="normalize-space(t:fileDesc/t:titleStmt/t:title[@xml:lang = 'en'][1])"
					/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[1])"/>
				</xsl:otherwise>
			</xsl:choose>
		</szd:title>
		<xsl:for-each select="t:fileDesc/t:titleStmt/t:title[@type = 'Einheitssachtitel']">
			<szd:originaltitle>
				<xsl:value-of
					select="normalize-space(.)"/>
			</szd:originaltitle>
		</xsl:for-each>
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary/t:ab">
			<szd:summary xml:lang="en">
				<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary/t:ab[@xml:lang ='en'])"/>
			</szd:summary>
			<szd:summary xml:lang="de">
				<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary/t:ab[@xml:lang ='de'])"/>
			</szd:summary>
		</xsl:if>
		
	</xsl:template>

	<!-- //////// -->
	<!-- Nachbesitzer/in -->
	<xsl:template name="getProvenance">
		<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance">
			<xsl:choose>
				<xsl:when
					test="t:*/@xml:lang">
						<szd:provenance xml:lang="en">
							<xsl:value-of select="normalize-space(t:*[@xml:lang = 'en']/text())"/>
						</szd:provenance>
						<szd:provenance xml:lang="de">
							<xsl:value-of select="normalize-space(t:*[@xml:lang = 'de']/text())"/>
						</szd:provenance>
				</xsl:when>
				<xsl:otherwise>
					<szd:provenance>
						<xsl:value-of select="normalize-space(.)"/>
					</szd:provenance>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
	</xsl:template>

	<!-- /////////////////////////////////////////////////////////// -->
	<!-- ///EN|DE/// -->
	<!-- this template gets an xpath-selection as input and check if there is a xml:lang, than $locale, otherwise print without @xml:lang -->
	<xsl:template name="printEnDe">
		<xsl:param name="path"/>
		<xsl:param name="locale"/>
		<xsl:choose>
			<xsl:when test="$path/@xml:lang">
				<xsl:value-of select="normalize-space($path[@xml:lang = $locale][1])"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="normalize-space($path[1])"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<!--  -->
	<xsl:template name="getLocation">
		<xsl:choose>
			<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ana">
				<szd:location
					rdf:resource="{t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ana}"
				/>
			</xsl:when>
			<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ref">
				<xsl:choose>
					<xsl:when
						test="contains(t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ref, 'SZDSTA')">
						<szd:location
							rdf:resource="{t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ref}"
						/>
					</xsl:when>
					<!-- it is a gnd @ref -->
					<xsl:otherwise>
						<xsl:call-template name="GetStandortelist">
							<xsl:with-param name="Standort"
								select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository"/>
							<xsl:with-param name="Typ" select="'szd:location'"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
				
			</xsl:when>
			<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository">
				<xsl:call-template name="GetStandortelist">
					<xsl:with-param name="Standort"
						select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository"/>
					<xsl:with-param name="Typ" select="'szd:location'"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>Error: in XPath: "t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository"</xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<!-- get en/de differentiation -->
	<xsl:template name="getEnDe">
		<xsl:param name="XPpath"/>
		<xsl:param name="Type"/>
		<xsl:if test="$XPpath">
			<xsl:element name="{$Type}">
				<xsl:attribute name="xml:lang" select="'en'"/>
				<xsl:value-of select="normalize-space($XPpath[@xml:lang = 'en'])"/>
			</xsl:element>
		</xsl:if>
		<xsl:if test="$XPpath">
			<xsl:element name="{$Type}">
				<xsl:attribute name="xml:lang" select="'de'"/>
				<xsl:value-of select="normalize-space($XPpath[@xml:lang = 'de'])"/>
			</xsl:element>
		</xsl:if>
	</xsl:template>
</xsl:stylesheet>