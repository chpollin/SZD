<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0"
	 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
	 xmlns:dc="http://purl.org/dc/elements/1.1/" 
	 xmlns:functx="http://www.functx.com" 
	 xmlns:gn="http://www.geonames.org/ontology#" 
	 xmlns:szd="https://gams.uni-graz.at/o:szd.ontology#" 
     xmlns:skos="https://gams.uni-graz.at/skos/scheme/o:oth/#" 
     xmlns:t="http://www.tei-c.org/ns/1.0"
     xmlns:dcterms="http://purl.org/dc/terms/"
     xmlns:wiki="https://www.wikidata.org/wiki/Property:"
     xmlns:gnd="http://d-nb.info/standards/elementset/gnd#"
	 xmlns:owl="http://www.w3.org/2002/07/owl#"
	 xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
	 xmlns:foaf="http://xmlns.com/foaf/0.1/"
	 xmlns:gams="https://gams.uni-graz.at/o:gams-ontology#">
	
	<!-- author: Christopher Pollin
		date: 2019
		
		this XSL-T transforms TEI/XML data to RDF/Data. Different TEI-Datasets in SZD are processed.
		every concept, property etc. bases on gams.uni-graz.at/o:szd.ontology
	-->
	
    
	<!-- DEFINE global variables -->
	<xsl:variable name="Personlist">
		<xsl:copy-of select="document('https://glossa.uni-graz.at/o:szd.personen/TEI_SOURCE')"/>
	</xsl:variable>

	<xsl:variable name="OrganisationList">
		<xsl:copy-of select="document('https://glossa.uni-graz.at/o:szd.organisation/TEI_SOURCE')"/>
	</xsl:variable>
	
	<xsl:variable name="StandorteList">
		<xsl:copy-of select="document('https://glossa.uni-graz.at/o:szd.standorte/TEI_SOURCE')"/>
	</xsl:variable>
	
	
	<xsl:variable name="Languages">
		<xsl:copy-of select="document('http://glossa.uni-graz.at/archive/objects/context:szd/datastreams/LANGUAGES/content')"/>
	</xsl:variable>
    
    <!-- ///////////////////////////////// -->
    <xsl:template match="/">
        <rdf:RDF>
            <xsl:choose>
            	<xsl:when test="//t:fileDesc/t:publicationStmt/t:idno[@type='PID'] = 'o:szd.bibliothek'">
            		<xsl:call-template name="Bibliothek"/>
            	</xsl:when>
            	<xsl:when test="//t:fileDesc/t:publicationStmt/t:idno[@type='PID'] = 'o:szd.autographen'">
            		<xsl:call-template name="Autographen"/>
            	</xsl:when>
            	<xsl:when test="//t:fileDesc/t:publicationStmt/t:idno[@type='PID'] = 'o:szd.werke'">
            		<xsl:call-template name="Manuskripte"/>
            	</xsl:when>
            	<xsl:when test="//t:fileDesc/t:publicationStmt/t:idno[@type='PID'] = 'o:szd.lebensdokumente'">
            		<xsl:call-template name="Lebensdokumente"/>
            	</xsl:when>
            	<xsl:when test="//t:fileDesc/t:publicationStmt/t:idno[@type='PID'] = 'o:szd.personen'">
            		<xsl:call-template name="Personen"/>
            	</xsl:when>
            	<xsl:when test="contains(//t:fileDesc/t:publicationStmt/t:idno[@type='PID'], 'lebenskalender')">
            		<xsl:call-template name="Lebenskalender"/>
            	</xsl:when>
            	<xsl:when test="//t:fileDesc/t:publicationStmt/t:idno[@type='PID'] = 'o:szd.standorte'">
            		<xsl:call-template name="Standorte"/>
            	</xsl:when>
            	<xsl:when test="//t:fileDesc/t:publicationStmt/t:idno[@type='PID'] = 'o:szd.publikation'">
            		<xsl:call-template name="Publikation"/>
            	</xsl:when>
            	<xsl:when test="contains(//t:fileDesc/t:publicationStmt/t:idno[@type='PID'], 'o:szd.thema')">
            		<xsl:call-template name="Collection"/>
            	</xsl:when>
            	<xsl:otherwise>
            		<xsl:text>No data source define! (like o:szd.bibliothek, o:szd.autographen, o:sud.werke...)</xsl:text>
            	</xsl:otherwise>
            </xsl:choose>   
        </rdf:RDF>
    </xsl:template>
	
	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- szd:Book -->	
	<xsl:template name="Bibliothek">
		<xsl:for-each select="//t:listBibl/t:biblFull">
			<xsl:variable name="Book-ID" select="@xml:id"/>
			<szd:Book rdf:about="{concat('https://gams.uni-graz.at/o:szd.bibliothek#',  $Book-ID)}">
	        	<xsl:call-template name="Bibliothek_RDF">
	            	<xsl:with-param name="Book-ID" select="@xml:id"/>
	            </xsl:call-template>
	          	<!-- COLLECTION  -->
	        	<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.bibliothek"/>
	        	<!-- FULLTEXT -->
	        	<xsl:call-template name="FulltextSearchData"/>
	        </szd:Book>
			
			<!-- /////////////////////////////////// -->
			<!-- rdf:about for szd:Book -->
			<!-- Extent -->
			<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent">
				<szd:Extent rdf:about="{concat('https://gams.uni-graz.at/o:szd.bibliothek#', $Book-ID, 'EX')}">
					<!-- page -->
					<xsl:call-template name="createTriple">
						<xsl:with-param name="PropertyTyp" select="'data'"/>
						<xsl:with-param name="XPpath" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type='page']"/>
						<xsl:with-param name="Property" select="'szd:page'"/>
					</xsl:call-template>
					<!-- format -->
					<xsl:call-template name="createTriple">
						<xsl:with-param name="PropertyTyp" select="'data'"/>
						<xsl:with-param name="XPpath" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type='format']"/>
						<xsl:with-param name="Property" select="'szd:format'"/>
					</xsl:call-template>
					<!-- binding -->
					<xsl:call-template name="createTriple">
						<xsl:with-param name="PropertyTyp" select="'data'"/>
						<xsl:with-param name="XPpath" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab"/>
						<xsl:with-param name="Property" select="'szd:binding'"/>
					</xsl:call-template>
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
			<!-- Publication Statment -->
			<xsl:if test="t:fileDesc/t:publicationStmt">
				<szd:PublicationStmt rdf:about="{concat('https://gams.uni-graz.at/o:szd.bibliothek#', $Book-ID, 'PUS')}">
					<!-- szd:publisher -->
					<xsl:if test="t:fileDesc/t:publicationStmt/t:publisher">
						<szd:publisher>
							<xsl:value-of select="t:fileDesc/t:publicationStmt/t:publisher"/>
						</szd:publisher>
					</xsl:if>
					<!-- szd:pubPlace -->
					<xsl:if test="t:fileDesc/t:publicationStmt/t:pubPlace">
						<szd:pubPlace>
							<xsl:value-of select="t:fileDesc/t:publicationStmt/t:pubPlace"/>
						</szd:pubPlace>
					</xsl:if>
					<!-- szd:pubDate -->
					<xsl:if test="t:fileDesc/t:publicationStmt/t:date">
						<szd:pubDate>
							<xsl:value-of select="t:fileDesc/t:publicationStmt/t:date"/>
						</szd:pubDate>
					</xsl:if>
					<!-- szd:pubDate -->
					<xsl:if test="t:fileDesc/t:editionStmt/t:edition">
						<szd:pubDate>
							<xsl:value-of select="t:fileDesc/t:editionStmt/t:edition"/>
						</szd:pubDate>
					</xsl:if>
					<!-- //////// -->
					<!-- szd:text -->
					<szd:text>
						<xsl:if test="t:fileDesc/t:editionStmt/t:edition">
							<xsl:value-of select="t:fileDesc/t:editionStmt/t:edition"/>
							<xsl:text> . – </xsl:text>
						</xsl:if>
						<xsl:value-of select="t:fileDesc/t:publicationStmt/t:pubPlace"/><xsl:text> : </xsl:text>
						<xsl:value-of select="t:fileDesc/t:publicationStmt/t:publisher"/>
						<xsl:text>, </xsl:text>
						<xsl:value-of select="t:fileDesc/t:publicationStmt/t:date"/>
					</szd:text>
				</szd:PublicationStmt>
			</xsl:if>
			<!-- ProvenanceCharacteristic -->
			<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='provenance'] or 
				t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier//t:altIdentifier or
				t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc//t:ab/t:ref or
				t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp">
				<szd:ProvenanceCharacteristic rdf:about="{concat('https://gams.uni-graz.at/o:szd.bibliothek#', $Book-ID, 'PS')}">
					<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='provenance']/t:item/t:ref">
						<xsl:element name="{concat('szd:',lower-case(substring-after(@target, '#')))}">
							<xsl:value-of select="normalize-space(../t:desc)"/>
						</xsl:element>
					</xsl:for-each>
					<!--<!-\- Nachbesitzer -\->
					<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:ab/t:ref">
						<xsl:element name="{concat('szd:',lower-case(substring-after(@target, '#')))}">
							<xsl:value-of select="normalize-space(..)"/>
						</xsl:element>
					</xsl:for-each>-->
					<!-- Einband -->
					<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc//t:ab/t:ref">
						<xsl:element name="{concat('szd:',lower-case(substring-after(@target, '#')))}">
							<xsl:value-of select="normalize-space(..)"/>
						</xsl:element>
					</xsl:for-each>
					<!--  -->
					<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier//t:altIdentifier">
						<szd:originalShelfmark rdf:resource="{concat('https://gams.uni-graz.at/o:szd.bibliothek#', $Book-ID, 'OS')}"/>
					</xsl:if>
					<!-- stamp -->
					<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp">
						<szd:stamp>
							<xsl:value-of select="normalize-space(../t:desc)"/>
						</szd:stamp>
					</xsl:for-each>
					
					<xsl:for-each select="t:fileDesc//t:ref/@target">
						<szd:glossar rdf:resource="{.}"/>	
					</xsl:for-each>
				
					
					<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier//t:altIdentifier/@corresp">
						<szd:glossar rdf:resource="{.}"/>	
					</xsl:for-each>
					
					<szd:text xml:lang='en'>
						<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='provenance']/t:item/t:term[@xml:lang='en'] | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp/t:term[@xml:lang='en']">
							<xsl:value-of select="."/>
							<xsl:if test="not(position()=last())">
								<xsl:text>,</xsl:text>
							</xsl:if>
						</xsl:for-each>
						<xsl:if test=".//t:msDesc/t:msIdentifier/t:altIdentifier">
							<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='provenance'] | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp/t:term">
								<xsl:text>, </xsl:text>
							</xsl:if>
							<xsl:text>Original Shelfmark</xsl:text>
						</xsl:if>
						<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:ab/t:ref">
							<xsl:if test=".//t:msDesc/t:msIdentifier/t:altIdentifier | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='provenance']/t:item/t:term">
								<xsl:text>, </xsl:text>
							</xsl:if>
							<xsl:text>Later Owner</xsl:text>
						</xsl:if>
					</szd:text>
					<szd:text xml:lang='de'>
						<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='provenance']/t:item/t:term[@xml:lang='de'] | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp/t:term[@xml:lang='de']">
							<xsl:value-of select="."/>
							<xsl:if test="not(position()=last())">
								<xsl:text>, </xsl:text>
							</xsl:if>
						</xsl:for-each>
						<xsl:if test=".//t:msDesc/t:msIdentifier/t:altIdentifier">
							<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='provenance'] | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp/t:term">
								<xsl:text>, </xsl:text>
							</xsl:if>
							<xsl:text>Originalsignatur</xsl:text>
						</xsl:if>
						<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:ab/t:ref">
							<xsl:if test=".//t:msDesc/t:msIdentifier/t:altIdentifier | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='provenance']/t:item/t:term">
								<xsl:text>, </xsl:text>
							</xsl:if>
							<xsl:text>Nachbesitzer</xsl:text>
						</xsl:if>
					</szd:text>
				</szd:ProvenanceCharacteristic>
			</xsl:if>
			<!-- ProvenanceCharacteristic -->
			<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier//t:altIdentifier">
				<szd:OriginalShelfmark rdf:about="{concat('https://gams.uni-graz.at/o:szd.bibliothek#', $Book-ID, 'OS')}">
					<!-- Originalsiganturen und Hausexemplar -->
					<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier//t:altIdentifier">
						<xsl:element name="{concat('szd:',lower-case(substring-after(@corresp, '#')))}">
							<xsl:value-of select="normalize-space(.)"/>
						</xsl:element>
					</xsl:for-each>
				</szd:OriginalShelfmark>
			</xsl:if>
	    </xsl:for-each>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////////////////////////////// -->	
	<!-- ///AUTOGRAPHEN/// -->
	<xsl:template name="Autographen">
		<xsl:for-each select="//t:listBibl/t:biblFull">
			
                <szd:Autograph rdf:about="{concat('https://gams.uni-graz.at/o:szd.autographen#',  @xml:id)}">
                	<!-- AUTOGRAPHEN DATA -->
                	<xsl:call-template name="RDF_autograph"/>
                	<!-- FULLTEXT -->
                	<xsl:call-template name="FulltextSearchData"/>
                	<!-- DATASOURCE SPECIFIC RULES  -->
                	<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.autographen"/>
                </szd:Autograph>
				<!--  -->
			<szd:Extent rdf:about="{concat('https://gams.uni-graz.at/o:szd.autographen#', @xml:id, 'EX')}">
			    	<xsl:call-template name="getExtent_SZDBIB_SZDAUT">
			    		<xsl:with-param name="locale" select="'en'"/>
			    	</xsl:call-template>
			    	<xsl:call-template name="getExtent_SZDBIB_SZDAUT">
			    		<xsl:with-param name="locale" select="'de'"/>
			    	</xsl:call-template>
			    	<!--<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent">
			    		<szd:extent>
			    			<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent)"/>
			    		</szd:extent>
			    	</xsl:if>-->
			    </szd:Extent>
            </xsl:for-each>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////////////////////////////// -->	
	<!-- ///LEBENSKALENDAR/// -->
	<xsl:template name="Lebenskalender">
		<xsl:for-each select="//t:listEvent/t:event">
			
			<szd:BiographicalEvent rdf:about="{concat('https://gams.uni-graz.at/o:szd.lebenskalender#',  @xml:id)}">
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
							<szd:relationTo rdf:resource="{concat('https://gams.uni-graz.at/o:szd.personen', @ref)}"/>
						</xsl:when>
						<xsl:when test="contains(@ref, 'SZDMSK')">
							<szd:relationTo rdf:resource="{concat('https://gams.uni-graz.at/o:szd.werke', @ref)}"/>
						</xsl:when>
						<xsl:when test="contains(@ref, 'SZDLEB')">
							<szd:relationTo rdf:resource="{concat('https://gams.uni-graz.at/o:szd.lebensdokumente', @ref)}"/>
						</xsl:when>
						<xsl:when test="contains(@ref, 'SZDBIB')">
							<szd:relationTo rdf:resource="{concat('https://gams.uni-graz.at/o:szd.bibliothek', @ref)}"/>
						</xsl:when>
						<xsl:otherwise/>
					</xsl:choose>
				</xsl:for-each>
			
				<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.lebenskalender"/>
			</szd:BiographicalEvent>
			
		</xsl:for-each>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////////////////////////////// -->	
	<!-- ///PERSONEN szd:Agent/// -->
		<xsl:template name="Personen">
		<xsl:for-each select="//t:listPerson/t:person">

			<!-- get the RDF resource behind the GND -->
			<xsl:variable name="url" select="string(concat(t:persName/@ref, '/about/lds.rdf'))"/>
			
			<szd:Agent rdf:about="{concat('https://gams.uni-graz.at/o:szd.personen#', @xml:id)}">
				<xsl:if test="t:idno[@type='wikidata']">
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
					<xsl:when test="t:persName[not(@type='variant')]/t:name">
						<szd:name>
							<xsl:value-of select="t:persName[not(@type='variant')]/t:name"/>
						</szd:name>
					</xsl:when>
					<xsl:otherwise>
						<xsl:if test="t:persName[not(@type='variant')]/t:forename">
							<szd:forename>
								<xsl:value-of select="t:persName[not(@type)]/t:forename"/>
							</szd:forename>
						</xsl:if>
						<xsl:if test="t:persName[not(@type='variant')]/t:surname">
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
				<xsl:if test="idno[@type='wikidata']">
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
						<xsl:value-of select="normalize-space(replace(replace(normalize-unicode(.), ';', ''), ',', ''))"/>
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

			<szd:Place rdf:about="{concat('https://gams.uni-graz.at/o:szd.orte#', @xml:id)}">
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
			
			<szd:Org rdf:about="{concat('https://gams.uni-graz.at/o:szd.organisation#', @xml:id)}">
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
				<szd:Location rdf:about="{concat('https://gams.uni-graz.at/o:szd.standorte#', @xml:id)}">
					<szd:name>
						<xsl:value-of select="t:orgName"/>
					</szd:name>
					<xsl:if test="t:settlement">
						<szd:settlement>
							<xsl:value-of select="t:settlement"/>
						</szd:settlement>
					</xsl:if>
					<xsl:if test="t:orgName/@ref">
						<gnd:gndIdentifier rdf:resource="{t:orgName/@ref}"/>
					</xsl:if>
					<xsl:if test="@corresp">
						<rdfs:seeAlso rdf:resource="{@corresp}"/>
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
			<szd:Publication rdf:about="{concat('https://gams.uni-graz.at/o:szd.publikation#', @xml:id)}">
				<!-- /////////////////////// -->
				<!-- TITLE -->
				<xsl:if test="t:fileDesc/t:titleStmt/t:title[@xml:lang ='en']">
					<szd:title xml:lang="en">
						<xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@xml:lang ='en']"/>
					</szd:title>
				</xsl:if>
				<xsl:if test="t:fileDesc/t:titleStmt/t:title[@xml:lang ='de']">
					<szd:title xml:lang="de">
						<xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@xml:lang ='de']"/>
					</szd:title>
				</xsl:if>
				<!-- /////////////////////// -->
				<!-- szd:author, @roles -->
				<xsl:choose>
					<xsl:when test="t:fileDesc/t:titleStmt/t:author[not(@role)]/t:persName/@ref">
						<xsl:call-template name="GetPersonlist">
							<xsl:with-param name="Person" select="t:fileDesc/t:titleStmt/t:author[not(@role)]/t:persname/@ref"/>
							<xsl:with-param name="Typ" select="'szd:author'"></xsl:with-param>
						</xsl:call-template>	
					</xsl:when>
					<xsl:when test="t:fileDesc/t:titleStmt/t:author[not(@role)]/t:persName">
						<szd:author>
							<xsl:value-of select="t:fileDesc/t:titleStmt/t:author[not(@role)]/t:persName/t:forename"/>
							<xsl:text> </xsl:text>
							<xsl:value-of select="t:fileDesc/t:titleStmt/t:author[not(@role)]/t:persName/t:surname"/>
						</szd:author>
					</xsl:when>
					<xsl:otherwise><xsl:comment>error</xsl:comment></xsl:otherwise>
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
				<szd:Publication rdf:about="{concat('https://gams.uni-graz.at/o:szd.publikation#', @xml:id)}">
					<!-- TITLE -->
					<xsl:if test="t:fileDesc/t:titleStmt/t:title[@xml:lang ='en']">
						<szd:title xml:lang="en">
							<xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@xml:lang ='en']"/>
						</szd:title>
					</xsl:if>
					<xsl:if test="t:fileDesc/t:titleStmt/t:title[@xml:lang ='de']">
						<szd:title xml:lang="de">
							<xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@xml:lang ='de']"/>
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
					<szd:Publication rdf:about="{concat('https://gams.uni-graz.at/o:szd.publikation#', @xml:id)}">
						<!-- TITLE -->
						<szd:title><xsl:value-of select="t:title"/></szd:title>
						<!-- szd:author = Stefan Zweig -->
						<szd:author rdf:resource="https://gams.uni-graz.at/o:szd.personen#SZDPER.1560"/>
						<!-- FULLTEXT -->
						<xsl:call-template name="FulltextSearchData"/>
						<!-- COLLECTION -->
						<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.publikation"/>	
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
			<!-- sameAs bibo:Manuscript -->
			<szd:Work rdf:about="{concat('https://gams.uni-graz.at/o:szd.werke#',  @xml:id)}">
				<!-- GET BASIC DATA: author, title, date, place -->
				<xsl:call-template name="Work_RDF"/>
				<!-- FULLTEXT -->
				<xsl:call-template name="FulltextSearchData"/>
				<!-- COLLECTION -->
				<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.werke"/>
			</szd:Work>
			<szd:Extent rdf:about="{concat('https://gams.uni-graz.at/o:szd.werke#', @xml:id, 'EX')}">
				<!-- page -->
				<!--<xsl:call-template name="createTriple">
					<xsl:with-param name="PropertyTyp" select="'data'"/>
					<xsl:with-param name="XPpath" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type='page']"/>
					<xsl:with-param name="Property" select="'szd:page'"/>
				</xsl:call-template>
				<!-\- format -\->
				<xsl:call-template name="createTriple">
					<xsl:with-param name="PropertyTyp" select="'data'"/>
					<xsl:with-param name="XPpath" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type='format']"/>
					<xsl:with-param name="Property" select="'szd:format'"/>
				</xsl:call-template>
				<!-\- binding -\->
				<xsl:call-template name="createTriple">
					<xsl:with-param name="PropertyTyp" select="'data'"/>
					<xsl:with-param name="XPpath" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab"/>
					<xsl:with-param name="Property" select="'szd:binding'"/>
				</xsl:call-template>-->
				<!-- //////// -->
				<!-- szd:text -->
				
				<xsl:call-template name="getExtentMSK">
					<xsl:with-param name="locale" select="'en'"/>
				</xsl:call-template>
				<xsl:call-template name="getExtentMSK">
					<xsl:with-param name="locale" select="'de'"/>
				</xsl:call-template>
				
			</szd:Extent>
		</xsl:for-each>
	</xsl:template>
	
	
	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///Lebensdokumente - szd:PersonalDocument/// -->
	<xsl:template name="Lebensdokumente">
		<xsl:for-each select="//t:listBibl/t:biblFull">
			<!-- sameAs bibo:Manuscript -->
			<szd:PersonalDocument rdf:about="{concat('https://gams.uni-graz.at/o:szd.lebensdokumente#',  @xml:id)}">
				
				<!-- GET BASIC DATA: author, title, date, place -->
				<xsl:call-template name="Work_RDF"/>
				<!-- FULLTEXT -->
				<xsl:call-template name="FulltextSearchData"/>
				<!-- COLLECTION -->
				<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.lebensdokumente"/>
			</szd:PersonalDocument>
			<szd:Extent rdf:about="{concat('https://gams.uni-graz.at/o:szd.lebensdokumente#', @xml:id, 'EX')}">
				<!-- page -->
				<!--<xsl:call-template name="createTriple">
					<xsl:with-param name="PropertyTyp" select="'data'"/>
					<xsl:with-param name="XPpath" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type='page']"/>
					<xsl:with-param name="Property" select="'szd:page'"/>
				</xsl:call-template>
				<!-\- format -\->
				<xsl:call-template name="createTriple">
					<xsl:with-param name="PropertyTyp" select="'data'"/>
					<xsl:with-param name="XPpath" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type='format']"/>
					<xsl:with-param name="Property" select="'szd:format'"/>
				</xsl:call-template>
				<!-\- binding -\->
				<xsl:call-template name="createTriple">
					<xsl:with-param name="PropertyTyp" select="'data'"/>
					<xsl:with-param name="XPpath" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab"/>
					<xsl:with-param name="Property" select="'szd:binding'"/>
				</xsl:call-template>-->
				<!-- //////// -->
				<!-- szd:text -->
				<xsl:call-template name="getExtentMSK">
					<xsl:with-param name="locale" select="'en'"/>
				</xsl:call-template>
				<xsl:call-template name="getExtentMSK">
					<xsl:with-param name="locale" select="'de'"/>
				</xsl:call-template>
			</szd:Extent>
		</xsl:for-each>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////////////////////////////// -->	
	<!-- ///COLLECTION/// -->
	<xsl:template name="Collection">
		<szd:Collection rdf:about="{concat('https://gams.uni-graz.at/', //t:publicationStmt/t:idno[@type='PID'])}">
			<!-- szd:title -->
			<szd:title><xsl:value-of select="//t:teiHeader//t:titleStmt/t:title"/></szd:title>
			
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
				<szd:connectedWithDocument rdf:resource="{concat('https://gams.uni-graz.at/', current-grouping-key())}"/>
			</xsl:for-each-group>-->
			<xsl:for-each-group select="//t:body//t:div//t:name[@type='person']" group-by="@ref">
				<szd:connectedWithPerson rdf:resource="{concat('https://gams.uni-graz.at/o:szd.personen', current-grouping-key())}"/>
			</xsl:for-each-group>
			<!-- FULLTEXT -->
			<gams:textualContent>
				<xsl:value-of select="//t:titleStmt/t:title"/><xsl:text> </xsl:text>
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
			<xsl:for-each select="$Personlist//t:person/t:persName[@ref=$GND]/following-sibling::t:persName[@type='Variantname']">
				<xsl:value-of select="normalize-unicode(.)"/><xsl:text> </xsl:text>
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
		
		<!-- szd:title -->
		<xsl:call-template name="getTitle"/>
		
		<xsl:if test="t:fileDesc/t:titleStmt/t:title[@type ='original']">
			<szd:originaltitle>
				<xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[@type ='original'])"/>
			</szd:originaltitle>
		</xsl:if>
		
		<!-- szd:author  -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:author[not(@role)]/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="t:fileDesc/t:titleStmt/t:author[not(@role)]/@ref"/>
				<xsl:with-param name="Typ" select="'szd:author'"/>
			</xsl:call-template>
		</xsl:if>
		<!-- szd:composer -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:author[@role='composer']/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="t:fileDesc/t:titleStmt/t:author[@role='composer']/@ref"/>
				<xsl:with-param name="Typ" select="'szd:composer'"/>
			</xsl:call-template>
		</xsl:if>
		<!-- szd:editor -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:editor[not(@role)]/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="t:fileDesc/t:titleStmt/t:editor[not(@role)]/@ref"/>
				<xsl:with-param name="Typ" select="'szd:editor'"/>
			</xsl:call-template>
		</xsl:if>
		<!-- szd:illustrator -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:editor[@role='illustrator']/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="t:fileDesc/t:titleStmt/t:editor[@role='illustrator']/@ref"/>
				<xsl:with-param name="Typ" select="'szd:illustrator'"/>
			</xsl:call-template>
		</xsl:if>
		<!-- szd:translator -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:editor[@role='translator']/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="t:fileDesc/t:titleStmt/t:editor[@role='translator']/@ref"/>
				<xsl:with-param name="Typ" select="'szd:translator'"/>
			</xsl:call-template>
		</xsl:if>
		<!-- szd:writerForeword -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:author[@role='preface']/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="t:fileDesc/t:titleStmt/t:author[@role='preface']/@ref"/>
				<xsl:with-param name="Typ" select="'szd:writerForeword'"/>
			</xsl:call-template>
		</xsl:if>
		<!-- szd:writerAfterword -->
		<xsl:if test="t:fileDesc/t:titleStmt/t:author[@role='afterword']/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="t:fileDesc/t:titleStmt/t:author[@role='afterword']/@ref"/>
				<xsl:with-param name="Typ" select="'szd:writerAfterword'"/>
			</xsl:call-template>
		</xsl:if>

		<!-- person -->
		<xsl:call-template name="GetPersonlist">
			<xsl:with-param name="Person" select="t:profileDesc/t:textClass/t:keywords/t:term[@type='person']/@ref"/>
			<xsl:with-param name="Typ" select="'szd:relationToPerson'"/>
		</xsl:call-template>
		
		<xsl:for-each select="t:profileDesc/t:textClass/t:keywords/t:term[@type='work']/@ref">
			<szd:realtionToWork rdf:resource="{.}"/>
		</xsl:for-each>
		
		<!--Publication Details-->
		<xsl:if test="t:fileDesc/t:publicationStmt">
			<szd:publicationStmt rdf:resource="{concat('https://gams.uni-graz.at/o:szd.bibliothek#', $Book-ID, 'PUS')}"/>
		</xsl:if>

		<!--Series-->
		<!-- szd:series -->
		<xsl:if test="t:fileDesc/t:seriesStmt/t:title">
			<szd:series>
				<xsl:value-of select="t:fileDesc/t:seriesStmt/t:title"/>
			</szd:series>
		</xsl:if>
		
		<!-- Language -->
		<xsl:call-template name="getLanguage"/>

		<!-- szd:location -->
		<xsl:choose>
			<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ana">
				<szd:location rdf:resource="{t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ana}"/>
			</xsl:when>
			<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository">
				<xsl:call-template name="GetStandortelist">
					<xsl:with-param name="Standort" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository"/>
					<xsl:with-param name="Typ" select="'szd:location'"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise/>
		</xsl:choose>
		
		<!-- szd:signature -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno">
			<szd:signature>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno"/>
			</szd:signature>
		</xsl:if>
		
		<!-- ////////////// -->
		<!-- Extent -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent">
			<szd:extent rdf:resource="{concat('https://gams.uni-graz.at/o:szd.bibliothek#', $Book-ID, 'EX')}"/>
		</xsl:if>
		
		<xsl:call-template name="getProvenance"/>
		
		
		<!-- illustriert -->

		<!-- szd:provenanceCharacteristic -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='provenance'] or 
			t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier//t:altIdentifier or
			t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc//t:ab/t:ref or
			t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list/t:item/t:stamp">
			<szd:provenanceCharacteristic rdf:resource="{concat('https://gams.uni-graz.at/o:szd.bibliothek#', $Book-ID, 'PS')}"/>
		</xsl:if>

		<!-- ////////////// -->
		<!-- Umfang, extent -->
		<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:span">
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
		
		<!-- szd:title -->
		<xsl:call-template name="getTitle"/>
		
		<!-- person -->
		<xsl:call-template name="GetPersonlist">
			<xsl:with-param name="Person" select="t:profileDesc/t:textClass/t:keywords/t:term[@type='person']/@ref"/>
			<xsl:with-param name="Typ" select="'szd:relationToPerson'"/>
		</xsl:call-template>
		
		<!--	
		<xsl:if test="t:profileDesc/t:textClass/t:keywords/t:term[@type='person']">
			<szd:relationToPerson rdf:resource="{t:profileDesc/t:textClass/t:keywords/t:term[@type='person']/@ref}"/>
		</xsl:if>-->
		
		<!-- Ordnungskateroire = GND-Sachgruppe -->
		<xsl:if test="t:profileDesc/t:textClass/t:keywords/t:term[@type='classification'][@xml:lang='de']">
			<xsl:variable name="CurrentCategory" select="t:profileDesc/t:textClass/t:keywords/t:term[@type='classification'][@xml:lang='de']"/>
			<szd:category>
				<xsl:attribute name="rdf:resource">
					<xsl:choose>
						<xsl:when test="$CurrentCategory = 'Romane'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Novel</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Autobiographie'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Autobiography</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Biographien'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Biography</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Erzählungen'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Stories</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Drama'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Drama</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Essay'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Essay</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Vorworte'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Foreword</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Historische Miniaturen'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#HistoricalMiniature</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Interview'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Interview</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Journalistische Arbeiten'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#JournalisticWork</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Film'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Movie</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Erzählung'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Movie</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Vorträge'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Narration</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Notizbücher'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Notebook</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Prosa'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Prose</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Romane'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Novel</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Reden'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Speech</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Übersetzung'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Translation</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Werknotizen'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Worknote</xsl:text>
						</xsl:when>
						<xsl:when test="$CurrentCategory = 'Tagebücher'">
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Diary</xsl:text>
						</xsl:when>
						<xsl:otherwise>
							<xsl:text>https://gams.uni-graz.at/o:szd.nachlass#Work</xsl:text>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute>
			</szd:category>
		</xsl:if>
		
		<!-- szd:author = Stefan Zweig -->
		<szd:author rdf:resource="https://gams.uni-graz.at/o:szd.personen#SZDPER.1560"/>
		
		<!-- Collection -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:altIdentifier/t:idno[@type='Context']">
			<szd:collection rdf:resource="{concat('https://gams.uni-graz.at/', t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:altIdentifier/t:idno[@type='Context'])}"/>
		</xsl:if>
		
		<!-- Datum -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:origin/t:origDate/@when">
			<szd:dateOfPublication>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:origin/t:origDate/@when"/>
			</szd:dateOfPublication>
		</xsl:if>
		
		<!-- Signatur -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno">
			<szd:signature><xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno"/></szd:signature>
		</xsl:if>

		<!-- Objekttyp -->
		<xsl:if test=".//t:extent/t:span[@xml:lang='de']/t:term[@type='objecttyp']">
			<szd:objecttyp xml:lang="de">
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:span[@xml:lang='de']/t:term[@type='objecttyp']"/>
			</szd:objecttyp>
		</xsl:if>
		<xsl:if test=".//t:extent/t:span[@xml:lang='en']/t:term[@type='objecttyp']">
			<szd:objecttyp xml:lang="en">
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:span[@xml:lang='en']/t:term[@type='objecttyp']"/>
			</szd:objecttyp>
		</xsl:if>
		
		<!-- szd:location  -->
		<xsl:choose>
			<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ana">
				<szd:location rdf:resource="{t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ana}"/>
			</xsl:when>
			<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository">
				<xsl:call-template name="GetStandortelist">
					<xsl:with-param name="Standort" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository"/>
					<xsl:with-param name="Typ" select="'szd:location'"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise></xsl:otherwise>
		</xsl:choose>
		
		<xsl:for-each select=".//*[contains(@ana, 'o:szd.glossar')]">
			<szd:term rdf:resource="{@ana}"/>
		</xsl:for-each>
		
		<xsl:if test=".//t:incipit[1]">
			<szd:term rdf:resource="https://gams.uni-graz.at/o:szd.glossar#Incipit"/>
		</xsl:if>
		
		<xsl:if test=".//t:origDate[1]">
			<szd:term rdf:resource="https://gams.uni-graz.at/o:szd.glossar#Date"/>
		</xsl:if>
		
		<!-- szd:lang -->
		<xsl:call-template name="getLanguage"/>
		
		<!-- Extent -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent">
			<szd:extent rdf:resource="{concat('https://gams.uni-graz.at/o:szd.werke#', @xml:id, 'EX')}"/>
		</xsl:if>
		
		
		<!-- provenance -->
		<xsl:call-template name="getProvenance">
			<xsl:with-param name="locale" select="'en'"/>
		</xsl:call-template>
		<xsl:call-template name="getProvenance">
			<xsl:with-param name="locale" select="'de'"/>
		</xsl:call-template>
		
		<!-- acquisition -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition">
			<szd:acquired>
				<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition)"/>
			</szd:acquired>
		</xsl:if>
		
		<!-- Identifying Inscription -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:docEdition[@xml:lang='de']">
			<szd:identifyingInscription xml:lang='de'>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:docEdition[@xml:lang='de']"/>
			</szd:identifyingInscription>
		</xsl:if>
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:docEdition[@xml:lang='en']">
			<szd:identifyingInscription xml:lang='en'>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:docEdition[@xml:lang='en']"/>
			</szd:identifyingInscription>
		</xsl:if>
		
		<!-- Schreibmaterial -->
		<!-- ana="https://gams.uni-graz.at/o:szd.glossar#WritingMaterial"  -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'o:szd.glossar#WritingMaterial')][@xml:lang='de']">
			<szd:writingMaterial xml:lang='de'>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'o:szd.glossar#WritingMaterial')][@xml:lang='de']"/>
		    </szd:writingMaterial>
		</xsl:if>
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'o:szd.glossar#WritingMaterial')][@xml:lang='en']">
			<szd:writingMaterial xml:lang='en'>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'o:szd.glossar#WritingMaterial')][@xml:lang='en']"/>
			</szd:writingMaterial>
		</xsl:if>
		
		<!-- Beschreibmaterial -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'o:szd.glossar#WritingInstrument')][@xml:lang='de']">
			<szd:writingInstrument xml:lang='de'>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'o:szd.glossar#WritingInstrument')][@xml:lang='de']"/>
			</szd:writingInstrument>
		</xsl:if>
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'o:szd.glossar#WritingInstrument')][@xml:lang='en']">
			<szd:writingInstrument xml:lang='en'>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material[contains(@ana, 'o:szd.glossar#WritingInstrument')][@xml:lang='en']"/>
			</szd:writingInstrument>
		</xsl:if>
		
		<!-- Schreiberhand -->
		<!-- this should be a reference to a SZDPER-ID -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:handDesc/t:ab">
			<szd:secretarialHand>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:handDesc/t:ab"/>
			</szd:secretarialHand>
		</xsl:if>
		
		<!-- Einband -->
		<!-- this should be a reference to a SZDPER-ID -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab[@xml:lang='de']">
			<szd:binding xml:lang='de'>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab[@xml:lang='de']"/>
			</szd:binding>
		</xsl:if>
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab[@xml:lang='en']">
			<szd:binding xml:lang='en'>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab[@xml:lang='en']"/>
			</szd:binding>
		</xsl:if>
		
		<!-- Beilagen -->
		<!-- o:szd.glossar#Enclosures -->
		<!-- this should be a reference to a SZDPER-ID -->
		<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:accMat/t:list/t:item[contains(@ana, 'o:szd.glossar#Enclosures')]">
			<szd:enclosures>
				<xsl:value-of select="."/>
			</szd:enclosures>
		</xsl:for-each>
		
		<!-- Zusatzmaterial -->
		<!-- o:szd.glossar#Enclosures -->
		<!-- this should be a reference to a SZDPER-ID -->
		<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:accMat/t:list/t:item[contains(@ana, 'o:szd.glossar#AdditionalMaterial')]">
			<szd:additionalMaterial>
				<xsl:value-of select="."/>
			</szd:additionalMaterial>
		</xsl:for-each>
				
		<!-- Note, Hinweis -->
		<xsl:if test="t:fileDesc/t:notesStmt/t:note[@xml:lang='de']">
			<szd:note xml:lang='de'>
				<xsl:value-of select="t:fileDesc/t:notesStmt/t:note[@xml:lang='de']"/>
			</szd:note>
		</xsl:if>
		<xsl:if test="t:fileDesc/t:notesStmt/t:note[@xml:lang='en']">
			<szd:note xml:lang='en'>
				<xsl:value-of select="t:fileDesc/t:notesStmt/t:note[@xml:lang='en']"/>
			</szd:note>
		</xsl:if>
		
		<!-- Incipit -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:incipit">
			<szd:incipit>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:incipit"/>
			</szd:incipit>
		</xsl:if>
		
		<xsl:for-each-group select="t:fileDesc/t:titleStmt/t:editor[@role='contributor']" group-by="@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="current-grouping-key()"/>
				<xsl:with-param name="Typ" select="'szd:partyInvolved'"/>
			</xsl:call-template>
		</xsl:for-each-group>
		
	</xsl:template>

	
	<!-- //////////////////////////////////////////////////////////////////////////////////// -->
	<!-- ///RDF_autograph/// -->
	<xsl:template name="RDF_autograph">
		
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
			<xsl:with-param name="Person" select="t:fileDesc/t:titleStmt/t:author[@role = 'composer']/t:persName/@ref"/>
			<xsl:with-param name="Typ" select="'szd:composer'"/>
		</xsl:call-template>
		
		<xsl:for-each-group select="t:profileDesc/t:textClass/t:keywords/t:term[@type='person']" group-by="@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="current-grouping-key()"/>
				<xsl:with-param name="Typ" select="'szd:partyInvolved'"/>
			</xsl:call-template>
		</xsl:for-each-group>
		
		<xsl:for-each-group select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary/t:persName[@type='person']" group-by="@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="current-grouping-key()"/>
				<xsl:with-param name="Typ" select="'szd:relationToPerson'"/>
			</xsl:call-template>
		</xsl:for-each-group>
		
		<!-- affected person -->
		<xsl:for-each select="t:profileDesc/t:textClass/t:keywords/t:term[@type='person_affected']/t:persName/@ref">
			<xsl:call-template name="GetPersonlist">
				<xsl:with-param name="Person" select="."/>
				<xsl:with-param name="Typ" select="'szd:affectedPerson'"/>
			</xsl:call-template>
		</xsl:for-each>
		
		<!-- summary -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary">
			<szd:content>
				<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary)"/>
			</szd:content>
		</xsl:if>

		<!-- szd:location -->
		<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:orgName/@ref">
			<xsl:call-template name="GetStandortelist">
				<xsl:with-param name="Standort" select="."/>
				<xsl:with-param name="Typ" select="'szd:location'"/>
			</xsl:call-template>
		</xsl:for-each>
			
		<!-- languagecode -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang">
			<szd:lang>
				<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang)"/>
			</szd:lang>
		</xsl:if>
		
		<!-- extent -->
		<szd:extent rdf:resource="{concat('https://gams.uni-graz.at/o:szd.autographen#', @xml:id, 'EX')}"/>

		<!-- provenance -->
		<xsl:call-template name="getProvenance">
			<xsl:with-param name="locale" select="'en'"/>
		</xsl:call-template>
		<xsl:call-template name="getProvenance">
			<xsl:with-param name="locale" select="'de'"/>
		</xsl:call-template>
		
		
		<!-- acquired -->
		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition">
			<szd:acquired>
				<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition)"/>
			</szd:acquired>
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
					<xsl:variable name="SZDPER" select="$Personlist//t:person[t:persName[contains(@ref, $String)]]/@xml:id"/>
					<!-- check if there is a GND-Ref, otherwise all empty gnd would be listed -->
					<xsl:choose>
						<!-- if @ref is a GND-ID -->
						<xsl:when test="substring-after($String, 'd-nb.info/gnd/')">
							<xsl:for-each select="$SZDPER">
								<xsl:element name="{$Typ}">
									<xsl:attribute name="rdf:resource">
										<xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.personen#', .)"/>
									</xsl:attribute>
								</xsl:element>
							</xsl:for-each>
						</xsl:when>
						<!-- if @ef = SZDPER -->
						<xsl:when test="contains($String, '#SZDPER.')">
							<xsl:element name="{$Typ}">
								<xsl:attribute name="rdf:resource">
									<xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.personen', $String)"/>
								</xsl:attribute>
							</xsl:element>
						</xsl:when>
						<xsl:otherwise>
							<xsl:comment>huhu</xsl:comment>
						</xsl:otherwise>
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
			<xsl:variable name="SZDORG" select="$OrganisationList//t:org[t:orgName[@ref = $String]]/@xml:id"/>
			<!-- check if there is a GND-Ref, otherwise all empty gnd would be listed -->
			<xsl:if test="substring-after($String, 'http://d-nb.info/gnd/')">
				<xsl:for-each select="$SZDORG">
					<xsl:element name="{$Typ}">
						<xsl:attribute name="rdf:resource">
							<xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.organisation#', .)"/>
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
								<xsl:variable name="String" select="concat(normalize-space($Standort),', ', normalize-space($Standort/../t:settlement))"/>
								<xsl:attribute name="rdf:resource">
									<xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.standorte#', $StandorteList//t:org[t:orgName = $String]/@xml:id)"/>
								</xsl:attribute>
							</xsl:element>
						</xsl:if>
					</xsl:when>
					<xsl:when test="$StandorteList//t:org[t:orgName = normalize-space($Standort)]/@xml:id">
						<xsl:element name="{$Typ}">
							<xsl:attribute name="rdf:resource">
								<xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.standorte#', $StandorteList//t:org[t:orgName = normalize-space($Standort)]/@xml:id)"/>
							</xsl:attribute>
						</xsl:element>
					</xsl:when>
					<xsl:when test="$StandorteList//t:org[t:orgName/@ref = $Standort]/@xml:id">
						<xsl:element name="{$Typ}">
							<xsl:attribute name="rdf:resource">
								<xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.standorte#', $StandorteList//t:org[t:orgName/@ref  = normalize-space($Standort)][1]/@xml:id)"/>
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
								<xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.standorte#', $StandorteList//t:org[t:orgName/@ref = $Standort/@ref]/@xml:id)"/>
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
				<xsl:value-of select="'https://gams.uni-graz.at/o:szd.orte#'"/>
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
							<xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.orte#', .)"/>
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
	
	<xsl:template  name="getLanguage">
		<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang/t:lang">
			<xsl:choose>
				<xsl:when test="@xml:lang">
					<xsl:for-each select="@xml:lang">
						<szd:language rdf:resource="{concat('http://id.loc.gov/vocabulary/iso639-2/', .)}"/>
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
					<xsl:when test="$XPpath/@xml:lang">
						<xsl:element name="{$Property}">
							<xsl:attribute name="xml:lang" select="$XPpath/@xml:lang"/>
							<xsl:value-of select="normalize-space($XPpath)"/>
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
		<xsl:variable name="EXTENT" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent | t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent"/>
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
			<xsl:if test="$EXTENT/t:measure[@type='page']">
				<xsl:value-of select="$EXTENT/t:measure[@type='page']"/>
				<xsl:text> </xsl:text>
				<xsl:choose>
					<xsl:when test="$EXTENT/t:measure[@type='page'] = '1'">
						<xsl:choose>
							<xsl:when test="$locale = 'en'">
								<xsl:text>Page</xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>Seite</xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:when>
					<xsl:otherwise>
						<xsl:choose>
							<xsl:when test="$locale = 'en'">
								<xsl:text>Pages</xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>Seiten</xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:otherwise>
				</xsl:choose>
				<xsl:choose>
					<xsl:when test="$EXTENT/t:measure[@type='leaf']">
						<xsl:text>, </xsl:text>
					</xsl:when>
					<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='extent']/t:item">
						<xsl:text> : </xsl:text>
					</xsl:when>
					<xsl:otherwise>
						<xsl:if test="contains($SZD_ID,  'SZDBIB')">
							<xsl:text>. </xsl:text>
						</xsl:if>
						<xsl:text> </xsl:text>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			<xsl:if test="$EXTENT/t:measure[@type='leaf']">
				<xsl:value-of select="$EXTENT/t:measure[@type='leaf']"/>
				<xsl:text> </xsl:text>
				<xsl:choose>
					<xsl:when test="$EXTENT/t:measure[@type='leaf'] = '1'">
						<xsl:text> Blatt </xsl:text>
					</xsl:when>
					<xsl:otherwise>
						<xsl:choose>
							<xsl:when test="$locale = 'en'">
								<xsl:text> Leaves </xsl:text>
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
			<xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='extent']/t:item">
				<xsl:choose>
					<xsl:when test="position() = last()">
						<xsl:value-of select="."/>
						<xsl:text>. </xsl:text>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="."/><xsl:text>, </xsl:text>
					</xsl:otherwise>
				</xsl:choose> 	
			</xsl:for-each>
			<xsl:text> </xsl:text>
			<xsl:value-of select="$EXTENT/t:measure[@type='format']"/>
			<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding">
				<xsl:text>, </xsl:text>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding"/>
			</xsl:if>
		</szd:text>
		</xsl:if>
	</xsl:template>
	
	<xsl:template name="getExtentMSK">
		<xsl:param name="locale"/>
		<xsl:variable name="EXTENT" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent"/>
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
			<xsl:value-of select="$EXTENT/t:span[@xml:lang = $locale]"/>
			
	
			<xsl:if test="$EXTENT/t:measure[@type='format']">
				<xsl:text>, </xsl:text>
				<xsl:value-of select="$EXTENT/t:measure[@type='format']"/>
			</xsl:if>
			<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:foliation/t:ab">
				<xsl:text>, </xsl:text>
				<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:foliation/t:ab[@xml:lang = $locale]"/>
			</xsl:if>
			<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab">
				<xsl:text>, </xsl:text>
				<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab[@xml:lang = $locale])"/>
			</xsl:if>
		</szd:text>
	</xsl:template>
	
	<!-- //////// -->
	<!-- getTitle -->
	<xsl:template name="getTitle">
			<szd:title xml:lang="de">
				<xsl:choose>
					<xsl:when test="t:fileDesc/t:titleStmt/t:title[@xml:lang='de']">
						<xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[@xml:lang='de'][1])"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[1])"/>
					</xsl:otherwise>
				</xsl:choose>
			</szd:title>
		<szd:title xml:lang="en">
			<xsl:choose>
				<xsl:when test="t:fileDesc/t:titleStmt/t:title[@xml:lang='en']">
					<xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[@xml:lang='en'][1])"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[1])"/>
				</xsl:otherwise>
			</xsl:choose>
		</szd:title>
	</xsl:template>
	
	<!-- //////// -->
	<!-- getTitle -->
	<xsl:template name="getProvenance">
		<xsl:param name="locale"/>
		
		<xsl:choose>
			<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:ab[@xml:lang='en']">
				<xsl:choose>
					<xsl:when test="$locale='en'">
						<szd:provenance xml:lang="en">
							<xsl:choose>
								<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:ab[@xml:lang='en']">
									<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:ab[@xml:lang='en'])"/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:ab)"/>
								</xsl:otherwise>
							</xsl:choose>
						</szd:provenance>
					</xsl:when>
					<xsl:otherwise>
						<szd:provenance xml:lang="de">
							<xsl:choose>
								<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:ab[@xml:lang='de']">
									<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:ab[@xml:lang='de'])"/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:ab)"/>
								</xsl:otherwise>
							</xsl:choose>
						</szd:provenance>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<xsl:otherwise>
				<xsl:choose>
					<xsl:when test="$locale='en'">
						<szd:provenance xml:lang="en">
							<xsl:choose>
								<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance[@xml:lang='en']">
									<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance[@xml:lang='en'])"/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance[1])"/>
								</xsl:otherwise>
							</xsl:choose>
						</szd:provenance>
					</xsl:when>
					<xsl:otherwise>
						<szd:provenance xml:lang="de">
							<xsl:choose>
								<xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance[@xml:lang='de']">
									<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance[@xml:lang='de'])"/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance[1])"/>
								</xsl:otherwise>
							</xsl:choose>
						</szd:provenance>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>
