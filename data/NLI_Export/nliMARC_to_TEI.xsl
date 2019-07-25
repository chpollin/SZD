<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs"
    xmlns="http://www.loc.gov/MARC21/slim" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.loc.gov/MARC21/slim
    http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd"
    xmlns:t="http://www.tei-c.org/ns/1.0" version="2.0">

    <!-- author: Chhristopher Pollin  
         date: July 2019 
         this xsl transform an MARC-export from the national library of jerusalem to a biblFull-structure für the SZD project.
    -->

    <xsl:template match="/">
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title>Title</title>
                    </titleStmt>
                    <publicationStmt>
                        <publisher>
                            <orgName corresp="https://www.uni-salzburg.at/index.php?id=72"
                                ref="d-nb.info/gnd/1047605287">Literaturarchiv Salzburg</orgName>
                        </publisher>
                        <authority>
                            <orgName corresp="https://informationsmodellierung.uni-graz.at"
                                ref="d-nb.info/gnd/1137284463">Zentrum für Informationsmodellierung
                                - Austrian Centre for Digital Humanities, Karl-Franzens-Universität
                                Graz</orgName>
                        </authority>
                        <distributor>
                            <orgName ref="https://gams.uni-graz.at">GAMS - Geisteswissenschaftliches
                                Asset Management System</orgName>
                        </distributor>
                        <availability>
                            <licence target="https://creativecommons.org/licenses/by-nc/4.0"
                                >Creative Commons BY-NC 4.0</licence>
                        </availability>
                        <publisher>Literaturarchiv Salzburg</publisher>
                        <idno type="PID">o:szd.nli</idno>
                    </publicationStmt>
                    <sourceDesc>
                        <p>Information about the source</p>
                    </sourceDesc>
                </fileDesc>
            </teiHeader>
            <text>
                <body>
                    <listBibl>
                        <xsl:for-each select="//*:record">
                            <!-- variable names = MARC21 field -->
                            <xsl:variable name="Title"
                                select="*:datafield[@tag = '245']/*:subfield[@code = 'a']"/>
                            <!-- Deutsche Dichtung -->
                            <xsl:variable name="ShortTitle"
                                select="*:datafield[@tag = '246']/*:subfield[@code = 'a']"/>
                            <xsl:variable name="LanguageCodeOfText"
                                select="*:datafield[@tag = '041']/*:subfield[@code = 'a']"/>
                            <xsl:variable name="DateofManufacture"
                                select="*:datafield[@tag = '260']/*:subfield[@code = 'g']"/>
                            <!-- Volume? -->
                            <xsl:variable name="GeneralNote"
                                select="*:datafield[@tag = '500']/*:subfield[@code = 'a']"/>
                            <xsl:variable name="Summary"
                                select="*:datafield[@tag = '520']/*:subfield[@code = 'a']"/>
                            <!-- not relevant; describes that an object e.g. was repaired or in an exhibition -->
                            <!--<xsl:variable name="ActionNote" select="*:datafield[@tag='583']/*:subfield[@code = 'a']"/>-->
                            <!-- 590 is a local note -->
                            <!-- Added Entry-Personal Name like  Rosenkranz, Hans, -->
                            <xsl:variable name="PersonalName"
                                select="*:datafield[@tag = '700']/*:subfield[@code = 'a']"/>
                            <xsl:variable name="Signature"
                                select="*:datafield[@tag = '911']/*:subfield[@code = 'c']"/>

                            <biblFull xml:id="{concat('SZDMSK.', position(), '_nli')}">
                                <fileDesc>
                                    <titleStmt>
                                        <title>
                                            <xsl:value-of select="$Title"/>
                                        </title>

                                        <xsl:if test="$ShortTitle">
                                            <title>
                                                <xsl:value-of select="$ShortTitle"/>
                                            </title>
                                        </xsl:if>
                                        <title type="Einheitssachtitel">TEST </title>
                                        <author ref="http://d-nb.info/gnd/118637479">
                                            <surname>Zweig</surname>
                                            <forename>Stefan</forename>
                                        </author>
                                    </titleStmt>
                                    <publicationStmt>
                                        <ab>Archive material in the National Library of Israel</ab>
                                    </publicationStmt>
                                    <xsl:if test="$GeneralNote">
                                        <notesStmt>
                                            <note>
                                                <xsl:value-of select="$GeneralNote"/>
                                            </note>
                                        </notesStmt>
                                    </xsl:if>
                                    <sourceDesc>
                                        <msDesc>
                                            <msIdentifier>
                                                <country>Israel</country>
                                                <settlement>Jerusalem</settlement>
                                                <repository ref="http://d-nb.info/gnd/1004728-1">The
                                                  National Library of Israel</repository>
                                                <xsl:if test="$Signature">
                                                  <idno type="signature">
                                                  <xsl:value-of select="$Signature"/>
                                                  </idno>
                                                </xsl:if>
                                            </msIdentifier>
                                            <msContents>
                                                <xsl:if test="$Summary">
                                                  <summary>
                                                  <ab>
                                                    <xsl:value-of select="$Summary"/>
                                                  </ab>
                                                  </summary>
                                                </xsl:if>
                                                <xsl:if test="$LanguageCodeOfText">
                                                  <textLang>
                                                  <lang>
                                                  <xsl:value-of select="$LanguageCodeOfText"/>
                                                  </lang>
                                                  </textLang>
                                                </xsl:if>
                                            </msContents>
                                            <xsl:if test="$DateofManufacture">
                                                 <history>
                                                     <origin>
                                                         <origDate>
                                                             <xsl:value-of select="$DateofManufacture"/>
                                                         </origDate>
                                                     </origin>
                                                 </history>
                                            </xsl:if>
                                        </msDesc>
                                    </sourceDesc>
                                </fileDesc>
                                <profileDesc>
                                    <textClass>
                                        <keywords>
                                            <term type="classification" xml:lang="en">NLI</term>
                                            <term type="classification" xml:lang="de">NLI</term>
                                            <xsl:for-each select="$PersonalName">
                                                <term type="person">
                                                  <xsl:value-of select="."/>
                                                </term>
                                            </xsl:for-each>
                                        </keywords>
                                    </textClass>
                                </profileDesc>
                            </biblFull>
                        </xsl:for-each>
                    </listBibl>
                </body>
            </text>
        </TEI>
    </xsl:template>



</xsl:stylesheet>
