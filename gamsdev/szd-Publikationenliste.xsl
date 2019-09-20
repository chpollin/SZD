<?xml version="1.0" encoding="UTF-8"?>

<!-- 
    Project: GAMS Projekttemplate
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
    Author: Christopher Pollin
    Last update: 2017
 -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:i18n="http://apache.org/cocoon/i18n/2.1"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    exclude-result-prefixes="#all">
    
    <xsl:include href="szd-static.xsl"/>
    <xsl:include href="szd-Templates.xsl"/>
    
    <xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>
    
    <!-- ///PERSONENLISTE/// -->
    <xsl:template name="content">
        <section class="card">
            <!-- ///CALL NAVBAR in szd-Templates -->
            <xsl:call-template name="getStickyNavbar">
                <xsl:with-param name="Title">
                    <xsl:choose>
                        <xsl:when test="$locale = 'en'">
                            <xsl:text>Initial Release</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>Erstveröffentlichungen</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:with-param>
                <xsl:with-param name="Content" select="//t:listBibl/t:biblFull/t:fileDesc/t:publicationStmt/t:date"/>
                <xsl:with-param name="PID" select="'o:szd.publikation'"/>
                <xsl:with-param name="locale" select="$locale"/>
            </xsl:call-template>
            <!-- /// PAGE-CONTENT /// -->
            <!-- creates for every person an entry, including reference to GND and alphabetically sorted and linked -->
        <article id="content" class="card-body">
            <div class="col-12">
            <!-- ////////////////////////////// -->
            <!-- every biblFull in o:szd.publikation -->
            <xsl:for-each-group select="//t:listBibl/t:biblFull" group-by="t:fileDesc/t:publicationStmt/t:date/@when">
                <xsl:sort select="t:fileDesc/t:publicationStmt/t:date/@when"/>
                <h2 id="{concat('year_', current-grouping-key())}" class="headerEntryList">
                    <xsl:value-of select="current-grouping-key()"/>
                </h2>
                <div class="list-group entryGroup">     
                    <xsl:for-each select="current-group()">
                        <div class="list-group-item entry shadow-sm" id="{@xml:id}">
                            <div class="card-heading bg-light row">
                                <h4 class="card-title text-left col-9">
                                    <a data-toggle="collapse" href="{concat('#c' , generate-id())}">
                                        <span class="arrow">
                                            <xsl:text>&#9660; </xsl:text>
                                        </span>
                                        <span class="font-weight-bold font-italic mr-1">
                                            <xsl:choose>
                                                <xsl:when test="$locale = 'en'">
                                                    <xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@xml:lang = $locale]"/>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:value-of select="t:fileDesc/t:titleStmt/t:title"/>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </span>
                                    </a>
                                    <xsl:text> | </xsl:text><xsl:value-of select="t:fileDesc/t:publicationStmt/t:date"/>
                                </h4>
                                <span class="col-3">
                                    <xsl:text> </xsl:text>
                                    <!-- if GND @ref -->
                                    <xsl:if test="contains(.//t:fileDesc/t:titleStmt/t:title/@ref, 'd-nb')">
                                        <a href="{.//t:fileDesc/t:titleStmt/t:title/@ref}" target="_blank" title="GND">
                                            <xsl:text>GND</xsl:text>
                                        </a>
                                    </xsl:if>
                                </span>
                            </div>
                            <div class="card-body card-collapse collapse" id="{concat('c' , generate-id())}">
                                <!-- its calling the same template which creates the SZD-BIB Entries. 
                                    But a different param type can be used to adapt the template: e.g. to add a query-URL to the title -->
                                <xsl:call-template name="FillbiblFull_SZDBIB">
                                    <xsl:with-param name="locale" select="$locale"/>
                                    <xsl:with-param name="type" select="$PID"/>
                                </xsl:call-template>
                            </div>   
                        </div>
                    </xsl:for-each>
                </div>
         </xsl:for-each-group>
                 
            </div>
            </article>
        </section>
    </xsl:template>
    
</xsl:stylesheet>
