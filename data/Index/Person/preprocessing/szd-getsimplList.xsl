<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">


    <xsl:output encoding="UTF-8"/>

    <xsl:template match="/">
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title>Personenliste</title>
                        <author>
                            <forename>Christopher</forename>
                            <surname>Pollin</surname>
                        </author>
                    </titleStmt>
                    <publicationStmt>
                        <publisher>
                            <orgName corresp="https://www.uni-salzburg.at/index.php?id=72" ref="d-nb.info/gnd/1047605287">Literaturarchiv Salzburg</orgName>
                        </publisher>
                        <authority>
                            <orgName corresp="https://informationsmodellierung.uni-graz.at" ref="d-nb.info/gnd/1137284463"> Zentrum für Informationsmodellierung - Austrian Centre for Digital
                                Humanities, Karl-Franzens-Universität Graz </orgName>
                        </authority>
                        <distributor>
                            <orgName ref="https://gams.uni-graz.at"> GAMS - Geisteswissenschaftliches Asset Management System </orgName>
                        </distributor>
                        <availability>
                            <licence target="https://creativecommons.org/licenses/by-nc-sa/4.0"> Creative Commons BY-NC-SA 4.0 </licence>
                        </availability>
                        <publisher>Literaturarchiv Salzburg</publisher>
                        <idno type="PID">o:szd.personen</idno>
                        <date when="2017-12-15">15.12.2017</date>
                    </publicationStmt>
                    <seriesStmt>
                        <title ref="gams.uni-graz.at/szd"> Stefan Zweig Digitale Nachlassrekonstruktion </title>
                        <respStmt>
                            <resp>Projektleitung</resp>
                            <persName>
                                <forename>Manfred</forename>
                                <surname>Mittermayer</surname>
                            </persName>
                        </respStmt>
                    </seriesStmt>
                    <sourceDesc>
                        <p>ToDo: Ortsliste von Stefan Zweig in progress</p>
                    </sourceDesc>
                </fileDesc>
                <encodingDesc>
                    <editorialDecl>
                        <p> ToDo: was über die editionsregeln und kodierungsrichtlinien </p>
                    </editorialDecl>
                    <projectDesc>
                        <ab>
                            <ref target="glossa.uni-graz.at/o:szd.orte" type="object"></ref>
                        </ab>
                        <p> Das Projekt verfolgt das Ziel, den weltweit verstreuten Nachlass von Stefan Zweig im digitalen Raum zusammenzuführen und ihn einem literaturwissenschaftlich bzw. wissenschaftlich
                            interessierten Publikum zu erschließen. In Zusammenarbeit mit dem Literaturarchiv der Universität Salzburg wird dabei, basierend auf dem dort vorhandenen Quellenmaterial, eine
                            digitale Nachlassrekonstruktion des Bestandes generiert. So entsteht ein strukturierter Bestand an digitalen Objekten, der im Sinne der digitalen Langzeitarchivierung repräsentiert
                            wird, und NutzerInnen orts- und zeitunabhängig zugänglich ist. Das Projekt ist so konzipiert, dass zu einem späteren Zeitpunkt Erschließung und Anreicherung des Quellenmaterials
                            (z.B. digitalen Editionen) möglich werden. </p>
                    </projectDesc>
                </encodingDesc>
            </teiHeader>
            <text>
                <body>
                    <head>Personenliste</head>
                    <listPerson>
                        <xsl:for-each select="//*:person">
                            <person xml:id="{@xml:id}">
                                <xsl:choose>
                                    <xsl:when test="*:persName[@type='Ausgabename']">
                                        <xsl:apply-templates select="*:persName[@type='Ausgabename']"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:apply-templates select="*:persName"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                                
                                
                                <!--<persName ref="{*:persName/@ref}">-->
                                       
                                <!--</persName>-->
                            </person>
                        </xsl:for-each>
                    </listPerson>
                </body>
            </text>
        </TEI>
    </xsl:template>

    <xsl:template match="*:persName[@type='variant']"></xsl:template>

    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>
