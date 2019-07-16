<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:template match="/">
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title>Bibliothek</title>
                        <author>
                            <persName>
                                <forename> Rainer-Joachim</forename>
                                <surname>Siegel</surname>
                            </persName>
                        </author>
                    </titleStmt>
                    <publicationStmt>
                        <publisher>
                            <orgName corresp="https://www.uni-salzburg.at/index.php?id=72" ref="d-nb.info/gnd/1047605287">Literaturarchiv
                                Salzburg</orgName>
                        </publisher>
                        <authority>
                            <orgName corresp="https://informationsmodellierung.uni-graz.at" ref="d-nb.info/gnd/1137284463">Zentrum für
                                Informationsmodellierung - Austrian Centre for Digital Humanities,
                                Karl-Franzens-Universität Graz</orgName>
                        </authority>
                        <distributor>
                            <orgName ref="https://gams.uni-graz.at">GAMS -
                                Geisteswissenschaftliches Asset Management System</orgName>
                        </distributor>
                        <availability>
                            <licence target="https://creativecommons.org/licenses/by-nc/4.0">Creative
                                Commons BY-NC 4.0</licence>
                        </availability>
                        <publisher>Literaturarchiv Salzburg</publisher>
                        <idno type="PID">o:szd.publikation</idno>
                    </publicationStmt>
                    <seriesStmt>
                        <title ref="gams.uni-graz.at/szd">Stefan Zweig digital</title>
                        <respStmt>
                            <resp>Projektleitung</resp>
                            <persName>
                                <forename>Manfred</forename>
                                <surname>Mittermayer</surname>
                            </persName>
                        </respStmt>
                        <respStmt>
                            <resp>Datenerfassung</resp>
                            <persName>
                                <forename>Christopher</forename>
                                <surname>Pollin</surname>
                            </persName>
                        </respStmt>
                        <respStmt>
                            <resp>Datenmodellierung</resp>
                            <persName>
                                <forename>Christopher</forename>
                                <surname>Pollin</surname>
                            </persName>
                        </respStmt>
                    </seriesStmt>
                    <sourceDesc>
                        <p>Erstveröffentlichungen von Stefan Zweig.</p>
                    </sourceDesc>
                </fileDesc>
                <encodingDesc>
                    <editorialDecl>
                        <p> ToDo </p>
                    </editorialDecl>
                    <projectDesc>
                        <ab>
                            <ref target="gams.uni-graz.at/o:szd.publikation" type="object"></ref>
                        </ab>
                        <p>Das Projekt verfolgt das Ziel, den weltweit verstreuten Nachlass von Stefan Zweig
                            im digitalen Raum zusammenzuführen und ihn einem literaturwissenschaftlich bzw.
                            wissenschaftlich interessierten Publikum zu erschließen. In Zusammenarbeit mit
                            dem Literaturarchiv der Universität Salzburg wird dabei, basierend auf dem dort
                            vorhandenen Quellenmaterial, eine digitale Nachlassrekonstruktion des Bestandes
                            generiert. So entsteht ein strukturierter Bestand an digitalen Objekten, der im
                            Sinne der digitalen Langzeitarchivierung repräsentiert wird, und NutzerInnen
                            orts- und zeitunabhängig zugänglich ist. Das Projekt ist so konzipiert, dass zu
                            einem späteren Zeitpunkt Erschließung und Anreicherung des Quellenmaterials
                            (z.B. digitalen Editionen) möglich werden.</p>
                    </projectDesc>
                </encodingDesc>
            </teiHeader>
            <text>
                <body>
        <listBibl> 
        <xsl:for-each select="//*:ul[@id='main']/*:li">
            <xsl:variable name="ID" select="concat('SZDPUB.', position())"/>
            <xsl:variable name="Bibl" select="normalize-space(substring-after(., '.'))"/>   
            <xsl:variable name="Title" select="substring-before($Bibl, '.')"/>
                <biblFull xml:id="{$ID}">
                    <fileDesc>
                        <titleStmt>
                            <title ref=""><xsl:value-of select="$Bibl"/></title>
                            <author ref="http://d-nb.info/gnd/118637479"><persName><forename>Stefan</forename><surname> Zweig</surname></persName></author>
                        </titleStmt>
                        <publicationStmt>
                            <publisher> </publisher>
                            <pubPlace> </pubPlace>
                            <date> </date>
                        </publicationStmt>
                        <seriesStmt>
                            <title></title>
                        </seriesStmt>
                        <sourceDesc><author ref="http://d-nb.info/gnd/118637479" role="Verfasser">Zweig,
                                Stefan</author>
                            <ab> </ab>
                        </sourceDesc>
                    </fileDesc>
                    <profileDesc> 
                    </profileDesc>
                </biblFull>
                <xsl:if test="substring-after(./*:a/@href, '#')">
                    <xsl:variable name="Href" select="normalize-space(substring-after(./*:a/@href, '#'))"/>
                  
                    <xsl:for-each select="//*:li[*:span/@id = $Href]/*:ul/*:li">
                           <xsl:variable name="subID" select="concat($ID, '_', position())"/>
                        <biblFull xml:id="{$subID}">
                            <fileDesc>
                                <titleStmt>
                                    <title><xsl:value-of select="normalize-space(substring-after(.,'.'))"/></title>
                                    <author ref="http://d-nb.info/gnd/118637479"><persName><forename>Stefan</forename><surname> Zweig</surname></persName></author>
                                </titleStmt>
                                <publicationStmt>
                                    <publisher> </publisher>
                                    <pubPlace> </pubPlace>
                                    <date> </date>
                                </publicationStmt>
                                <seriesStmt>
                                    <title>
                                        <xsl:value-of select="$Title"/>
                                    </title>
                                    <biblScope><xsl:value-of select="$ID"/></biblScope>
                                </seriesStmt>
                                <sourceDesc>
                                    <ab> </ab>
                                </sourceDesc>
                            </fileDesc>
                            <profileDesc> 
                            </profileDesc>
                           </biblFull>
                           <xsl:if test="*:ul">
                               <xsl:for-each select="./*:ul/*:li">
                                   <biblFull xml:id="{concat($subID, '_', position())}">        
                                   <fileDesc>
                                       <titleStmt>
                                           <title> <xsl:value-of select="normalize-space(.)"/></title>
                                           <author ref="http://d-nb.info/gnd/118637479"><persName><forename>Stefan</forename><surname> Zweig</surname></persName></author>
                                       </titleStmt>
                                       <publicationStmt>
                                           <publisher> </publisher>
                                           <pubPlace> </pubPlace>
                                           <date> </date>
                                       </publicationStmt>
                                       <seriesStmt>
                                           <title></title>
                                           <biblScope><xsl:value-of select="$subID"/></biblScope>
                                       </seriesStmt>
                                       <sourceDesc>
                                           <ab> </ab>
                                       </sourceDesc>
                                   </fileDesc>
                                   <profileDesc> 
                                   </profileDesc>
                                   </biblFull>
                                   </xsl:for-each>
                               
                           </xsl:if>
                       </xsl:for-each>
               </xsl:if> 
        </xsl:for-each>
        </listBibl>
                </body>
            </text>
        </TEI>
        
    </xsl:template>
    
    
</xsl:stylesheet>