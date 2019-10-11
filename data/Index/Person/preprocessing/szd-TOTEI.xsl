<?xml version="1.0" encoding="UTF-8"?>


    <!-- 
    Project: Stefan zweig Digital
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
    Author: Christopher Pollin
    Last update: 2019
    -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:i18n="http://apache.org/cocoon/i18n/2.1"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:gndo="http://d-nb.info/standards/elementset/gnd#"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    exclude-result-prefixes="#all"
    version="2.0">
    
    <!-- GLOBAL VARIABLES -->
    <xsl:variable name="PID" select="//*:idno[@type='PID']"/>
    
    <!-- ////////////////////////////////////// -->
    <!-- checking if TOTEI is needed -->
    <xsl:template match="/">
        <xsl:choose>
            <!-- enrichment of SZDPER_simplList -->
            <xsl:when test="contains($PID,'o:szd.personen')">
                <xsl:copy>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:copy>
            </xsl:when>
            <xsl:otherwise>
                <TEI>
                   <xsl:comment>Error: TOTEI not defined for this PID.</xsl:comment>
                </TEI>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!-- copy -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!--More specific template for Node766 that provides custom behavior -->
    <xsl:template match="*:person"> 
        <!-- add here further data from GND -->
        <!-- http://d-nb.info/gnd/118582143/about/lds.rdf -->
        <xsl:variable name="GND-ID" select="*:persName/@ref"/>
        <xsl:variable name="URL" select="concat($GND-ID, '/about/lds.rdf')"/>
        <xsl:variable name="GND-Data" select="document($URL)/rdf:RDF/rdf:Description"/>
        
        <xsl:copy>
            <xsl:if test="$GND-Data//*:page/@rdf:resource">
                <xsl:attribute name="corresp">
                    <xsl:value-of select="$GND-Data//*:page/@rdf:resource"/>
                </xsl:attribute>
            </xsl:if>
            
            <xsl:apply-templates select="@*|node()"/>
           

            <!-- some variant names -->
            <xsl:if test="$GND-Data/gndo:variantNameForThePerson">
                <note type="variants">
                    <xsl:for-each select="$GND-Data/gndo:variantNameForThePerson">
                        <xsl:if test="position() &lt;= 20">
                            <xsl:value-of select="normalize-space(.)"/>
                            <xsl:if test="not(position()=last())">
                                <xsl:text> ; </xsl:text>
                            </xsl:if>
                        </xsl:if>
                    </xsl:for-each>
                </note>
            </xsl:if>
            <!-- date of birth -->
            <xsl:if test="$GND-Data/gndo:dateOfBirth">
                <birth when="{$GND-Data/gndo:dateOfBirth}"/>
            </xsl:if>
            <!-- date of death-->
            <xsl:if  test="$GND-Data/gndo:dateOfDeath">
                <death when="{$GND-Data/gndo:dateOfDeath}"/>
            </xsl:if>
            <xsl:if test="$GND-Data//*:sameAs[contains(@rdf:resource, 'www.wikidata.org')]">
                <idno type="wikidata">
                    <xsl:value-of select="$GND-Data//*:sameAs[contains(@rdf:resource, 'www.wikidata.org')]/@rdf:resource"/>
                </idno>
            </xsl:if>
        </xsl:copy>
    </xsl:template>
    


</xsl:stylesheet> 
    
