<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet" xmlns:t="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="xs" version="2.0">

    <!--///////////////////////////    
        author: Chistopher Pollin
        date: 2017
            
        Transforming bibliothek.xml (empty cells contain $Empty) 
        to a <listBibl> TEI/XML containing <bibFull>.      
        Names are compared to szd.personen, where a normalized version + gnd-reference exists.
        

        ///////////////////////////  
        
        
    -->
    <!-- ///GLOBAL VARIABLES/// -->
    <xsl:variable name="Languages">
        <xsl:copy-of select="document('https://gams.uni-graz.at/archive/objects/context:szd/datastreams/LANGUAGES/content')"/>
    </xsl:variable>
    <!-- First Row; Categories -->
    <xsl:variable name="RowTemplate">
        <xsl:copy>
            <row id="{generate-id()}">
                <xsl:for-each select="//*:Row[1]/*:Cell">
                    <cell position="{position()}">
                        <xsl:value-of select="normalize-space(.)"/>
                    </cell>
                </xsl:for-each>
            </row>
        </xsl:copy>
    </xsl:variable>

    <xsl:variable name="Empty" select="'NOx'"/>

    <xsl:variable name="Personenliste">
        <xsl:copy-of select="document('http://glossa.uni-graz.at/o:szd.personen/TEI_SOURCE')"/>
    </xsl:variable>
    
    <!--<xsl:variable name="PlacesList">
        <xsl:copy-of select="document('http://gams.uni-graz.at/o:szd.orte/TEI_SOURCE')"/>
    </xsl:variable>-->
    
    <xsl:variable name="Standortliste">
        <xsl:copy-of select="document('http://glossa.uni-graz.at/o:szd.standorte/TEI_SOURCE')"/>
    </xsl:variable>


    <xsl:template match="/">
        <TEI>
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title xml:lang="de">Bibliothek</title>
                        <title xml:lang="en">Library</title>
                        <author><persName><forename>Stefan</forename>
                            <surname>Matthias</surname></persName></author>
                        <author><persName><forename>Oliver</forename>
                            <surname>Matuschek</surname></persName></author>
                    </titleStmt>
                    <publicationStmt>
                        <publisher><orgName ref="d-nb.info/gnd/1047605287"
                            corresp="https://www.uni-salzburg.at/index.php?id=72">Literaturarchiv
                            Salzburg</orgName></publisher>
                        <authority><orgName ref="d-nb.info/gnd/1137284463"
                            corresp="https://informationsmodellierung.uni-graz.at">Zentrum für
                            Informationsmodellierung - Austrian Centre for Digital Humanities,
                            Karl-Franzens-Universität Graz</orgName></authority>
                        <distributor><orgName ref="https://gams.uni-graz.at">GAMS -
                            Geisteswissenschaftliches Asset Management System</orgName></distributor>
                        <availability>
                            <licence target="https://creativecommons.org/licenses/by-nc/4.0">Creative
                                Commons BY-NC 4.0</licence>
                        </availability>
                        <publisher>Literaturarchiv Salzburg</publisher>
                        <idno type="PID">o:szd.bibliothek</idno>
                        <date when="{current-date()}"/>
                    </publicationStmt>
                    <seriesStmt>
                        <title ref="gams.uni-graz.at/szd">Stefan Zweig digital</title>
                        <respStmt>
                            <resp>Projektleitung</resp>
                            <persName><forename>Manfred</forename><surname>Mittermayer</surname></persName>
                        </respStmt>
                        <respStmt>
                            <resp>Datenerfassung</resp>
                            <persName><forename>Stefan</forename>
                                <surname>Matthias</surname></persName>
                            <persName><forename>Oliver</forename>
                                <surname>Matuschek</surname></persName>
                        </respStmt>
                        <respStmt>
                            <resp>Datenmodellierung</resp>
                            <persName><forename>Christopher</forename><surname>Pollin</surname></persName>
                        </respStmt>
                    </seriesStmt>
                    <sourceDesc>
                        <p>Privatbibliothek von Stefan Zweig.</p>
                    </sourceDesc>
                </fileDesc>
                <encodingDesc>
                    <editorialDecl>
                        <p>
                            Jedes Buch in der Bibliothek von Stefan Zweig wid durch ein biblFull ausgedrückt. Neben klassischen biographischen Merkmalen, die beschrieben werden, 
                            liegt der Fokus auf physischen Merkmalen, die als Provenienzmerkmale zu betrachten sind (Originalsignatur, Widmung, Beilage etc.). Diese werden im sourceDesc 
                            beschrieben mit Referenzen auf externe Resourcen.
                        </p>
                    </editorialDecl>
                    <projectDesc>
                        <ab><ref target="gams.uni-graz.at/o:szd.bibliothek" type="object"/>
                        </ab>
                        <p>Das Projekt verfolgt das Ziel, den weltweit verstreuten Nachlass von Stefan Zweig im digitalen Raum zusammenzuführen und ihn einem literaturwissenschaftlich bzw. 
                            wissenschaftlich interessierten Publikum zu erschließen. In Zusammenarbeit mit dem Literaturarchiv der Universität Salzburg wird dabei, basierend auf dem dort vorhandenen 
                            Quellenmaterial, eine digitale Nachlassrekonstruktion des Bestandes generiert. So entsteht ein strukturierter Bestand an digitalen Objekten, der im Sinne der digitalen 
                            Langzeitarchivierung repräsentiert wird, und NutzerInnen orts- und zeitunabhängig zugänglich ist. Das Projekt ist so konzipiert, dass zu einem späteren Zeitpunkt Erschließung 
                            und Anreicherung des Quellenmaterials (z.B. digitalen Editionen) möglich werden.</p>
                    </projectDesc>
                </encodingDesc>
            </teiHeader>
            <text>
                <body>
                    <listBibl>
                        <xsl:for-each select="//*:Row">
                            <!--<xsl:variable name="Row">
                                <xsl:copy>
                                    <row id="{generate-id()}">
                                        <xsl:for-each select="*:Cell">
                                            <cell position="{position()}">
                                                <xsl:value-of select="normalize-space(.)"/>
                                            </cell>
                                        </xsl:for-each>
                                    </row>
                                </xsl:copy>
                            </xsl:variable>-->
                            <xsl:call-template name="getData">
                                <xsl:with-param name="Row" select="."/>
                            </xsl:call-template>
                        </xsl:for-each>
                    </listBibl>
                </body>
            </text>
        </TEI>
    </xsl:template>

    <xsl:template name="getData">
        <!-- defining parameter and variables -->
        <xsl:param name="Row"/>
        <!-- data entry with running id -->
        <xsl:variable name="SZDBIB_ID" select="concat('SZDBIB.', $Row/*:Cell[79])"/>
        <biblFull xml:id="{$SZDBIB_ID}">
            <!-- ///TITLE/// -->
            <fileDesc>
            <titleStmt>
                <!-- Spalte 1; ///Titel/// -->
                <title>
                    <xsl:value-of select="$Row/*:Cell[1]"/>
                </title>
                <!-- Spalte 7; ///Gesamttitel/// -->
                <xsl:if test="not($Row/*:Cell[7] = $Empty)">
                    <title type="series">
                        <xsl:value-of select="$Row/*:Cell[7]"/>
                    </title>
                </xsl:if>
                <!-- Spalte 28; ///Originaltitel/// -->
                <xsl:if test="not($Row/*:Cell[28] = $Empty)">
                    <title type="original">
                        <xsl:value-of select="$Row/*:Cell[28]"/>
                    </title>
                </xsl:if>
                <!-- Spalte 2 - 5; ///Autor/// -->
                <xsl:for-each select="2 to 5">
                    <xsl:variable name="Count" select="."/>
                    <xsl:if test="not($Row/*:Cell[$Count] = $Empty)">
                        <!-- -1 because first column is title, but beginning with 'Verfasser 1'   -->
                        <author>
                            <xsl:call-template name="getGND">
                                <xsl:with-param name="Row" select="$Row"/>
                                <xsl:with-param name="Count" select="$Count"/>
                            </xsl:call-template>
                        </author>
                    </xsl:if>
                </xsl:for-each>
                <!-- Spalte 8-10; ///Bearbeiter | Herausgeber/// -->
                <xsl:for-each select="8 to 10">
                    <xsl:variable name="Count" select="."/>
                    <xsl:if test="not($Row/*:Cell[$Count] = $Empty)">
                        <editor>
                            <xsl:call-template name="getGND">
                                <xsl:with-param name="Row" select="$Row"/>
                                <xsl:with-param name="Count" select="$Count"/>
                            </xsl:call-template>
                        </editor>
                    </xsl:if>
                </xsl:for-each>
                <!-- Spalte 6; Komponist -->
                <xsl:if test="not($Row/*:Cell[6] = $Empty)">
                    <author role="composer">
                        <xsl:call-template name="getGND">
                            <xsl:with-param name="Row" select="$Row"/>
                            <xsl:with-param name="Count" select="6"/>
                        </xsl:call-template>
                    </author>
                </xsl:if>
                <!-- Spalte 11-12; Illustrator -->
                <xsl:for-each select="11 to 12">
                    <xsl:variable name="Count" select="."/>
                    <xsl:if test="not($Row/*:Cell[$Count] = $Empty)">
                        <editor role="illustrator">
                            <xsl:call-template name="getGND">
                                <xsl:with-param name="Row" select="$Row"/>
                                <xsl:with-param name="Count" select="$Count"/>
                            </xsl:call-template>
                        </editor>
                    </xsl:if>
                </xsl:for-each>
                <!-- Spalte 13-14; Übersetzer -->
                <xsl:for-each select="13 to 14">
                    <xsl:variable name="Count" select="."/>
                    <xsl:if test="not($Row/*:Cell[$Count] = $Empty)">
                        <editor role="translator">
                            <xsl:call-template name="getGND">
                                <xsl:with-param name="Row" select="$Row"/>
                                <xsl:with-param name="Count" select="$Count"/>
                            </xsl:call-template>
                        </editor>
                    </xsl:if>
                </xsl:for-each>
                <!-- Spalte 15; Verfasser Vorwort -->
                <xsl:if test="not($Row/*:Cell[15] = $Empty)">
                    <author role="preface">
                        <xsl:call-template name="getGND">
                            <xsl:with-param name="Row" select="$Row"/>
                            <xsl:with-param name="Count" select="15"/>
                        </xsl:call-template>
                    </author>
                </xsl:if>
                <!-- Spalte 16; Verfasser Nachwort -->
                <xsl:if test="not($Row/*:Cell[16] = $Empty)">
                    <author role="afterword">
                        <xsl:call-template name="getGND">
                            <xsl:with-param name="Row" select="$Row"/>
                            <xsl:with-param name="Count" select="16"/>
                        </xsl:call-template>
                    </author>
                </xsl:if>
            </titleStmt>


            <!-- ///EDITION/// -->
            <xsl:if test="not($Row/*:Cell[17] = $Empty)">
                <editionStmt>
                    <!-- Spalte 17; Ausgabevermerk -->
                    <edition>
                        <xsl:value-of select="normalize-space($Row/*:Cell[17])"/>
                    </edition>
                </editionStmt>
            </xsl:if>

            <!-- ///PUBLICATION/// -->
            <xsl:choose>
                <xsl:when
                    test="not($Row/*:Cell[19] = $Empty and $Row/*:Cell[20] = $Empty and $Row/*:Cell[18] = $Empty)">
                    <publicationStmt>
                        <!-- Spalte 19; Verlag -->
                        <!--<xsl:if test="$Row/*:Cell[19]">-->
                        <publisher>
                            <xsl:choose>
                                <xsl:when test="not($Row/*:Cell[19] = $Empty)">
                                    <xsl:value-of select="normalize-space($Row/*:Cell[19])"/>
                                </xsl:when>
                                <xsl:otherwise>Keine Information zum Veröffentlicher</xsl:otherwise>
                            </xsl:choose>
                        </publisher>
                        <!--</xsl:if>-->
                        <!-- Spalte 20; Erscheinungsjahr -->
                        <date>
                            <xsl:if test="not($Row/*:Cell[20] = $Empty)">
                                <xsl:choose>
                                    <xsl:when test="contains(normalize-space($Row/*:Cell[20]), '[')">
                                        <xsl:value-of select="substring-before(substring-after(normalize-space($Row/*:Cell[20]), '['), ']')"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:attribute name="precision" select="'low'"/>                                        
                                        <xsl:value-of select="normalize-space($Row/*:Cell[20])"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                               
                            </xsl:if>
                        </date>
                        <!-- Spalte 18; Verlagsort -->
                        <xsl:if test="not($Row/*:Cell[18] = $Empty)">
                        <pubPlace>
                            <!-- get GeoNames   -->
                           <!-- <xsl:variable name="CurrentPlace" select="normalize-space($Row/*:Cell[18])"/>
                            <xsl:for-each select="$PlacesList//*:place">
                                <xsl:if test="$CurrentPlace = *:placeName">
                                        <xsl:attribute name="ref">
                                            <xsl:value-of select="*:placeName/@ref"/>
                                        </xsl:attribute>
                                </xsl:if>
                            </xsl:for-each>-->
                            
                            <xsl:value-of select="normalize-space($Row/*:Cell[18])"/>
                            
                            
                        </pubPlace>
                        </xsl:if>
                    </publicationStmt>
                </xsl:when>
                <xsl:otherwise>
                    <publicationStmt>
                        <p>Keine Information zur Publikation</p>
                    </publicationStmt>
                </xsl:otherwise>
            </xsl:choose>


            <!-- ///SERIES/// -->
            <xsl:variable name="Reihe" select="$Row/*:Cell[26]"/>
            <xsl:if test="not($Reihe = $Empty)">
                <seriesStmt>
                    <!-- Spalte 26; Reihe -->
                    <xsl:choose>
                        <xsl:when test="contains($Reihe, ';')">
                            <title type="Reihe">
                                <xsl:value-of select="$Reihe"/>
                            </title>
                        </xsl:when>
                        <xsl:otherwise>
                            <title>
                                <xsl:value-of select="$Reihe"/>
                            </title>
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:if test="not($Row/*:Cell[27] = $Empty)">
                        <!-- Spalte 27; Unterreihe -->
                        <title type="Unterreihe">
                            <xsl:value-of select="$Row/*:Cell[27]"/>
                        </title>
                    </xsl:if>
                </seriesStmt>
            </xsl:if>


            <!-- ///SOURCE/// -->
            <sourceDesc>
                <msDesc>
                    <msIdentifier>
                        <!-- Spalte 75; aktueller Standort ; GeoOrt vor Beistrich-->
                        <settlement>
                            <xsl:value-of select="normalize-space(substring-after($Row/*:Cell[74], ','))"/>
                        </settlement>
                        <!-- Spalte 75; aktueller Standort ; Person oder Institution ,nach Beistrich-->
                        <repository>
                            <xsl:call-template name="getGND_Standort">
                                <xsl:with-param name="Repository" select="normalize-space(substring-before($Row/*:Cell[74], ','))"/>
                                <xsl:with-param name="Settelment" select="normalize-space(substring-after($Row/*:Cell[74], ','))"/>
                            </xsl:call-template>
                            <xsl:value-of select="normalize-space(substring-before($Row/*:Cell[74], ','))"/>
                        </repository>
                        <!-- Spalte 75; aktueller Standort -->
                        <xsl:if test="not($Row/*:Cell[75] = $Empty)">
                            <idno>
                                <xsl:value-of select="$Row/*:Cell[75]"/>
                            </idno>
                        </xsl:if>

                        <!-- Alte Signaturen -->
                        <!-- +9 X Signatur ignorieren 41 -->
                        
                        <!-- INalt01 -->
                        <xsl:if test="not($Row/*:Cell[35] = $Empty)">
                            <altIdentifier n="1" corresp="https://gams.uni-graz.at/o:szd.glossar#InventoryNumberOld">
                              <idno>
                                  <xsl:value-of select="normalize-space($Row/*:Cell[35])"/>
                              </idno>
                          </altIdentifier>
                        </xsl:if>
                        <xsl:if test="not($Row/*:Cell[36] = $Empty)">
                            <altIdentifier n="2" corresp="https://gams.uni-graz.at/o:szd.glossar#InventoryNumberOld">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[36])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        <xsl:if test="not($Row/*:Cell[37] = $Empty)">
                            <altIdentifier n="3" corresp="https://gams.uni-graz.at/o:szd.glossar#InventoryNumberOld">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[37])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        <!-- INalt02 -->
                        <xsl:if test="not($Row/*:Cell[38] = $Empty)">
                            <altIdentifier n="1" corresp="https://gams.uni-graz.at/o:szd.glossar#InventoryNumberOld">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[38])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        <xsl:if test="not($Row/*:Cell[39] = $Empty)">
                            <altIdentifier n="2" corresp="https://gams.uni-graz.at/o:szd.glossar#InventoryNumberOld">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[39])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        <xsl:if test="not($Row/*:Cell[40] = $Empty)">
                            <altIdentifier n="3" corresp="https://gams.uni-graz.at/o:szd.glossar#InventoryNumberOld">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[40])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        <!--  -->
                        <xsl:if test="not($Row/*:Cell[41] = $Empty)">
                            <altIdentifier corresp="https://gams.uni-graz.at/o:szd.glossar#InventoryNumberNew">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[41])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        <!-- IN fortlaufend -->
                        <xsl:if test="not($Row/*:Cell[42] = $Empty)">
                            <altIdentifier corresp="https://gams.uni-graz.at/o:szd.glossar#Nummerfortlaufend">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[42])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        
                        <xsl:if test="not($Row/*:Cell[43] = $Empty)">
                            <altIdentifier corresp="https://gams.uni-graz.at/o:szd.glossar#NumberCollection">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[43])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        
                        <xsl:if test="not($Row/*:Cell[44] = $Empty)">
                            <altIdentifier n="1" type="lowercase" corresp="https://gams.uni-graz.at/o:szd.glossar#SingleLetter">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[44])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        <xsl:if test="not($Row/*:Cell[45] = $Empty)">
                            <altIdentifier n="2" type="lowercase" corresp="https://gams.uni-graz.at/o:szd.glossar#SingleLetter">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[45])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        <xsl:if test="not($Row/*:Cell[46] = $Empty)">
                            <altIdentifier n="3" type="lowercase" corresp="https://gams.uni-graz.at/o:szd.glossar#SingleLetter">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[46])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        <xsl:if test="not($Row/*:Cell[47] = $Empty)">
                            <altIdentifier n="4" type="lowercase" corresp="https://gams.uni-graz.at/o:szd.glossar#SingleLetter">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[47])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        <xsl:if test="not($Row/*:Cell[48] = $Empty)">
                            <altIdentifier n="1" type="capital" corresp="https://gams.uni-graz.at/o:szd.glossar#SingleLetter">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[48])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        <xsl:if test="not($Row/*:Cell[49] = $Empty)">
                            <altIdentifier n="2" type="capital"  corresp="https://gams.uni-graz.at/o:szd.glossar#SingleLetter">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[49])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        <xsl:if test="not($Row/*:Cell[50] = $Empty)">
                            <altIdentifier n="3" type="capital"  corresp="https://gams.uni-graz.at/o:szd.glossar#SingleLetter">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[50])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        <xsl:if test="not($Row/*:Cell[51] = $Empty)">
                            <altIdentifier n="4" type="capital"  corresp="https://gams.uni-graz.at/o:szd.glossar#SingleLetter">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[51])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        
                        <xsl:if test="not($Row/*:Cell[52] = $Empty)">
                            <altIdentifier corresp="https://gams.uni-graz.at/o:szd.glossar#FurnitureLocation">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[52])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        
                        <xsl:if test="not($Row/*:Cell[53] = $Empty)">
                            <altIdentifier corresp="https://gams.uni-graz.at/o:szd.glossar#RoomLocation">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[53])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                        
                        <xsl:if test="not($Row/*:Cell[54] = $Empty)">
                            <altIdentifier corresp="https://gams.uni-graz.at/o:szd.glossar#Hausexemplar">
                                <idno>
                                    <xsl:value-of select="normalize-space($Row/*:Cell[54])"/>
                                </idno>
                            </altIdentifier>
                        </xsl:if>
                    </msIdentifier>

                    <!-- Sprachen 29, 30, 31 -->
                    <xsl:if test="not($Row/*:Cell[29] = $Empty)">
                        <msContents>
                            <textLang>
                                <xsl:for-each select="29 to 31">
                                    <xsl:variable name="Count" select="."/>
                                    <xsl:if test="not($Row/*:Cell[$Count] = $Empty)">
                                        <lang xml:lang="{$Row/*:Cell[$Count]}"/>
                                    </xsl:if>
                                </xsl:for-each>
                            </textLang>
                        	
                        	 <!-- Hinweis 1 -->
                        	<xsl:if test="not($Row/*:Cell[66] = $Empty)">
                        		<msItem>
                                    <note>
                                        <xsl:value-of select="$Row/*:Cell[66]"/>
                                    </note>
                        		</msItem>
                            </xsl:if>
                        </msContents>
                    </xsl:if>

                    <!-- physische Beschreibung -->
                    <xsl:variable name="Extent" select="$Row/*:Cell[21]"/>
                    <physDesc>
                        <objectDesc>
                            <supportDesc>
                                <extent>
                                    <!-- ///EXTENT Seitenanzahl/// -->
                                    <!-- Spalte 21; Seiten  -->
                                    <!-- Fälle: ; #;  -->
                                    <xsl:if test="not($Row/*:Cell[21] = $Empty)">
                                        <measure type="page">
                                            <xsl:value-of select="$Row/*:Cell[21]"/>
                                        </measure>
                                    </xsl:if>
                                    <!-- Spalte 22; Blatt  -->
                                    <xsl:if test="not($Row/*:Cell[22] = $Empty)">
                                        <measure type="leaf">
                                            <xsl:value-of select="$Row/*:Cell[22]"/>
                                        </measure>
                                    </xsl:if>
                                    <!-- Spalte 32; Format -->
                                    <xsl:if test="not($Row/*:Cell[32] = $Empty)">
                                        <measure type="format">
                                            <xsl:value-of select="$Row/*:Cell[32]"/>
                                        </measure>
                                    </xsl:if>
                                </extent>
                                <!-- </xsl:if>-->
                            </supportDesc>
                        </objectDesc>
                            
                        <xsl:variable name="Umfangexist" select="not($Row/*:Cell[23] = $Empty) or not($Row/*:Cell[24] = $Empty) or not($Row/*:Cell[25] = $Empty)"/>   
                        <xsl:variable name="Widmungexist" select="
                            not($Row/*:Cell[55] = $Empty) or not($Row/*:Cell[56] = $Empty) or not($Row/*:Cell[57] = $Empty) or not($Row/*:Cell[58] = $Empty) or not($Row/*:Cell[59] = $Empty)
                            or not($Row/*:Cell[60] = $Empty) or not($Row/*:Cell[63] = $Empty) or not($Row/*:Cell[65] = $Empty) or not($Row/*:Cell[64] = $Empty) or not($Row/*:Cell[61] = $Empty) or not($Row/*:Cell[62] = $Empty)"/>  
           
                        <xsl:if test="$Umfangexist = true() or $Widmungexist = true()" >
   
                        <additions>
                            <!-- Spalte 23; illustriert, 24 Karte, 25 Noten  -->
                  
                            <xsl:if test="$Umfangexist = true()">
                                <list type="extent">
                                    <!-- illustriert; 23 -->
                                    <xsl:if test="not($Row/*:Cell[23] = $Empty)">
                                        <item ana="illustrated">
                                            <xsl:value-of select="$Row/*:Cell[23]"/>
                                        </item>
                                    </xsl:if>
                                    <!-- Karten; 24 -->
                                    <xsl:if test="not($Row/*:Cell[24] = $Empty)">
                                        <item ana="map">
                                            <xsl:value-of select="$Row/*:Cell[24]"/>
                                        </item>
                                    </xsl:if>
                                    <!-- Noten; 25 -->
                                    <xsl:if test="not($Row/*:Cell[25] = $Empty)">
                                        <item ana="note">
                                            <xsl:value-of select="$Row/*:Cell[25]"/>
                                        </item>
                                    </xsl:if>
                                </list>
                            </xsl:if>
                            <!-- list of provenence terms -->
                            <xsl:if test="$Widmungexist = true()">
                                <list type="provenance">
                                    <!-- Spalte 65; Widmung -->
                                    <xsl:if test="not($Row/*:Cell[65] = $Empty)">
                                        <item>
                                            <ref target="https://gams.uni-graz.at/o:szd.glossar#PresentationInscription"/>
                                            <term xml:lang="de">Widmung</term>
                                            <term xml:lang="en">Presentation Inscription</term>
                                            <desc><xsl:value-of select="$Row/*:Cell[65]"/></desc>
                                        </item>
                                    </xsl:if>
                                    <!-- Spalte 55; Autogramm -->
                                    <xsl:if test="not($Row/*:Cell[55] = $Empty)">
                                        <item>
                                            <ref target="https://gams.uni-graz.at/o:szd.glossar#Autograph"/>
                                            <term xml:lang="de">Autogramm</term>
                                            <term xml:lang="en">Autograph</term>
                                            <desc><xsl:value-of select="$Row/*:Cell[55]"/></desc>
                                        </item>
                                    </xsl:if>
                                    <!-- Spalte 56; Einlage-->
                                    <xsl:if test="not($Row/*:Cell[56] = $Empty)">
                                        <item>
                                            <ref target="https://gams.uni-graz.at/o:szd.glossar#Autograph"/>
                                            <term xml:lang="de">Einlage</term>
                                            <term xml:lang="en">Insertion</term>
                                            <desc><xsl:value-of select="$Row/*:Cell[56]"/></desc>
                                        </item>
                                    </xsl:if>
                                    <!-- Spalte 57; Exlibris -->
                                    <xsl:if test="not($Row/*:Cell[57] = $Empty)">
                                        <item>
                                            <ref target="https://gams.uni-graz.at/o:szd.glossar#Bookplate"/>
                                            <term xml:lang="de">Exlibris</term>
                                            <term xml:lang="en">Bookplate</term>
                                            <desc><xsl:value-of select="$Row/*:Cell[57]"/></desc>
                                        </item>
                                    </xsl:if>
                                    <!-- Spalte 58; Marginalie -->
                                    <xsl:if test="not($Row/*:Cell[58] = $Empty)">
                                        <item>
                                            <ref target="https://gams.uni-graz.at/o:szd.glossar#Marginalia"/>
                                            <term xml:lang="de">Marginalie</term>
                                            <term xml:lang="en">Marginalia</term>
                                            <desc><xsl:value-of select="$Row/*:Cell[58]"/></desc>
                                        </item>
                                    </xsl:if>
                                    <!-- Spalte 59; Merkzeichen -->
                                    <xsl:if test="not($Row/*:Cell[59] = $Empty)">
                                        <item>
                                            <ref target="https://gams.uni-graz.at/o:szd.glossar#Marker"/>
                                            <term xml:lang="de">Merkzeichen</term>
                                            <term xml:lang="en">Underlining / Marker</term>
                                            <desc><xsl:value-of select="$Row/*:Cell[59]"/></desc>
                                        </item>
                                    </xsl:if>
                                    <!-- Spalte 60; Notiz -->
                                    <xsl:if test="not($Row/*:Cell[60] = $Empty)">
                                        <item>
                                            <ref target="https://gams.uni-graz.at/o:szd.glossar#Note"/>
                                            <term xml:lang="de">Notiz</term>
                                            <term xml:lang="en">Note</term>
                                            <desc><xsl:value-of select="$Row/*:Cell[60]"/></desc>
                                        </item>
                                    </xsl:if>
                                    <!-- Spalte 61 - 62; ///Stempel 01 - Stempel 02/// -->
                                    <xsl:for-each select="61 to 62">
                                        <xsl:variable name="Count" select="."/>
                                        <xsl:if test="not($Row/*:Cell[$Count] = $Empty)">
                                            <item>
                                                <stamp>
                                                    <ref target="https://gams.uni-graz.at/o:szd.glossar#Stamp"/>
                                                    <term xml:lang="de">Stempel</term>
                                                    <term xml:lang="en">Stamp</term>
                                                </stamp>
                                                <desc><xsl:value-of select="$Row/*:Cell[$Count]"/></desc>
                                            </item>
                                        </xsl:if>
                                    </xsl:for-each>
                                    <!-- Spalte 63; Tektur -->
                                    <xsl:if test="not($Row/*:Cell[63] = $Empty)">
                                        <item>
                                            <ref target="https://gams.uni-graz.at/o:szd.glossar#Overpasting"/>
                                            <term xml:lang="de">Tektur</term>
                                            <term xml:lang="en">Overpasting</term>
                                            <desc><xsl:value-of select="$Row/*:Cell[63]"/></desc>
                                        </item>
                                    </xsl:if>
                                    <!-- Spalte 64; Tilgung -->
                                    <xsl:if test="not($Row/*:Cell[64] = $Empty)">
                                        <item>
                                            <ref target="https://gams.uni-graz.at/o:szd.glossar#RemovedPage"/>
                                            <term xml:lang="de">Tektur</term>
                                            <term xml:lang="en">Removed Page</term>
                                            <desc><xsl:value-of select="$Row/*:Cell[64]"/></desc>
                                        </item>
                                    </xsl:if>
                                </list>
                            </xsl:if>
                        </additions>
                        </xsl:if>
                        <!-- Spalte 33; Einband -->
                        <xsl:if test="not($Row/*:Cell[33] = $Empty)">
                            <bindingDesc>
                                <binding>
                                    <ab>
                                        <xsl:choose>
                                            <xsl:when test="$Row/*:Cell[33] = 'Pappe [weiß lackiert mit rotem Rückenschild]'">
                                                <ref target="https://gams.uni-graz.at/o:szd.glossar#Binding"/>
                                             </xsl:when>
                                             <xsl:when test="$Row/*:Cell[33] = 'Pappe [farbig lackiert mit Rückenschild]'">
                                                 <ref target="https://gams.uni-graz.at/o:szd.glossar#Binding"/>
                                             </xsl:when>
                                             <xsl:otherwise/>
                                        </xsl:choose>
                                        <xsl:value-of select="$Row/*:Cell[33]"/>
                                    </ab>
                                </binding>
                            </bindingDesc>
                        </xsl:if>
                    </physDesc>

                    <xsl:if test="not($Row/*:Cell[76] = $Empty)">
                        <history>
                            <!-- Spalte 75///Provenienz/// -->
                            <xsl:if test="not($Row/*:Cell[76] = $Empty)">
                                <provenance>
                                    <!-- Spalte 76; Provenienz-->
                                    <ab>
                                        <xsl:value-of select="$Row/*:Cell[76]"/>
                                        <ref target="https://gams.uni-graz.at/o:szd.glossar#LaterOwner"/>
                                    </ab>
                                </provenance>
                            </xsl:if>
                        </history>
                    </xsl:if>


                </msDesc>
            </sourceDesc>
            </fileDesc>
            <!-- SCHLAGWORT 01,02,03  68-71 -->
            <profileDesc>
                <xsl:if test="not($Row/*:Cell[68] = $Empty) or not($Row/*:Cell[69] = $Empty) or not($Row/*:Cell[70] = $Empty)">
                 <textClass>
                     <keywords>
                     <xsl:for-each select="68 to 70">
                         <xsl:variable name="Count" select="."/>
                         <xsl:if test="not($Row/*:Cell[$Count]= $Empty)">
                         <term type="person">
                             <xsl:call-template name="getGND">
                                 <xsl:with-param name="Row" select="$Row"/>
                                 <xsl:with-param name="Count" select="$Count"/>
                             </xsl:call-template>
                         </term>
                         </xsl:if>
                     </xsl:for-each>
                     </keywords>
                 </textClass>
              </xsl:if>
            </profileDesc>
     </biblFull>

    </xsl:template>
    
    
    <!-- ////////////////////////////////////////////// -->
    <!-- GET PERSON from o:szd.person -->
    <xsl:template name="getGND">
        <xsl:param name="Row"/>
        <xsl:param name="Count"/>
        
        <!-- Zweig, Stefan in Excel -->
        <xsl:variable name="currentName" select="$Row/*:Cell[$Count]"/>
        <xsl:variable name="Person">
           
            <xsl:choose>
                <xsl:when test="$Personenliste//*:person[*:persName[concat(*:surname, ', ', *:forename) = $currentName]]">
                    <xsl:value-of select="$Personenliste//*:person[*:persName[concat(*:surname, ', ', *:forename) = $currentName]]/@xml:id"/>
                </xsl:when>
                <xsl:when test="$Personenliste//*:person[*:persName/*:surname = substring-before($Row/*:Cell[$Count], ',')]">
                    <xsl:value-of select="$Personenliste//*:person[*:persName/*:surname = substring-before($Row/*:Cell[$Count], ',')]/@xml:id"/>
                </xsl:when>
                <xsl:when test="$Personenliste//*:person[contains(*:note[@type='variants'], $Row/*:Cell[$Count])]">
                    <xsl:value-of select="$Personenliste//*:person[contains(*:note[@type='variants'], $Row/*:Cell[$Count])]/@xml:id"/>
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>
            
        </xsl:variable>
        
        <xsl:choose>
            <xsl:when test="$Person">
                <xsl:attribute name="ref">
                    <xsl:choose>
                        <xsl:when test="concat('#', $Person)">
                            <xsl:value-of select="concat('#', $Person)"/>
                        </xsl:when>
                        <xsl:otherwise/>
                    </xsl:choose>
                </xsl:attribute>
                <persName>
                   <xsl:choose>
                       <xsl:when test="$Personenliste//*:person[*:persName/*:surname = substring-before($Row/*:Cell[$Count], ',')]/*:persName/@ref">
                            <xsl:attribute name="ref">
                                <xsl:value-of select="$Personenliste//*:person[*:persName/*:surname = substring-before($Row/*:Cell[$Count], ',')]/*:persName/@ref"/>
                            </xsl:attribute>
                        </xsl:when>
                        <xsl:otherwise/>
                    </xsl:choose>
                    <!-- name -->
                    <xsl:choose>
                        <xsl:when test="contains($currentName, ',')">
                            <forename>
                                <xsl:value-of select="substring-after($currentName, ', ')"/>
                            </forename>
                            <surname>
                                <xsl:value-of select="substring-before($currentName, ',')"/>
                            </surname>
                        </xsl:when>
                        <xsl:otherwise>
                            <name>
                                <xsl:value-of select="$currentName"/>
                            </name>
                        </xsl:otherwise>
                    </xsl:choose>
                </persName>
            </xsl:when>
        </xsl:choose>
        
    </xsl:template>
    
    
    <!-- ////////////////////////////////////////////// -->
    <!-- GET PERSON from o:szd.person -->
    <xsl:template name="getGND_Standort">
        <xsl:param name="Repository"/>
        <xsl:param name="Settelment"/>
        <xsl:choose>
            <xsl:when test="$Repository = 'Privatbesitz'">
                <xsl:variable name="String" select="concat('Privatbesitz, ', $Settelment)"/>
                <xsl:choose>
                    <xsl:when test="$Standortliste//t:org[t:orgName = $String]/t:orgName/@ref">
                        <xsl:attribute name="ref">
                            <xsl:value-of select="$Standortliste//t:org[t:orgName = $String]/t:orgName/@ref"/>
                        </xsl:attribute>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:attribute name="ref">
                            <xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.standorte#', $Standortliste//t:org[t:orgName = $String]/@xml:id)"/>
                        </xsl:attribute>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                <xsl:choose>
                    <xsl:when test="$Standortliste//t:org[t:orgName = $Repository]/t:orgName/@ref">
                        <xsl:attribute name="ref">
                            <xsl:value-of select="$Standortliste//t:org[t:orgName = $Repository]/t:orgName/@ref"/>
                        </xsl:attribute>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:if test="$Standortliste//t:org[t:orgName = $Repository]/@xml:id">
                            <xsl:attribute name="ref">
                                <xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.standorte#', $Standortliste//t:org[t:orgName = $Repository]/@xml:id)"/>
                            </xsl:attribute>
                        </xsl:if>
                     </xsl:otherwise>
                </xsl:choose>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    

    


</xsl:stylesheet>
