<?xml version="1.0" encoding="UTF-8"?>

<!-- 
    Project: GAMS Projekttemplate
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
    Author: Christopher Pollin
    Last update: 2019
 -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:i18n="http://apache.org/cocoon/i18n/2.1"
    xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    exclude-result-prefixes="#all">
    
    <xsl:include href="szd-static.xsl"/>
    <xsl:include href="szd-Templates.xsl"/>
    
    <xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>
    
    <!-- ///STANDORTESLISTE/// -->
    <xsl:template name="content">
            	<!-- HEADER -->
                <!-- call getStickyNavbar in szd-Templates.xsl -->
                <xsl:call-template name="getNavbar">
                    <xsl:with-param name="Title">
                        <xsl:choose>
                            <xsl:when test="$locale = 'en'">
                                <xsl:value-of select="//t:titleStmt/t:title[@xml:lang='en']"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="//t:titleStmt/t:title[@xml:lang='de']"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:with-param>
                    <xsl:with-param name="PID" select="$PID"/>
                    <xsl:with-param name="mode" select="$mode"/>
                    
                </xsl:call-template>
                <!-- /// PAGE-CONTENT /// -->
                <article id="content">
                    <div class="list-group entryGroup">
                    <xsl:for-each-group select="//t:listOrg/t:org" group-by="@xml:id">
                        <xsl:sort data-type="text" lang="ger" select="t:orgName"/>
                        <xsl:variable name="SZDORG" select="current-grouping-key()"/>
                        <!-- build query URL -->
                        <xsl:variable name="BaseURL" select="'/archive/objects/query:szd.standort_search/methods/sdef:Query/get?params='"/>
                        <xsl:variable name="Param" select="encode-for-uri(concat('$1|&lt;https://gams.uni-graz.at/o:szd.standorte#', @xml:id, '&gt;', ';$2|', $locale))"/>
                        <xsl:variable name="QueryUrl" select="concat($BaseURL, $Param, '&amp;locale=', $locale)"/>

                        <div class="list-group-item mb-1" id="{@xml:id}">
                            <div class="row">
                                <h4 class="text-left col-9">
                                <a href="{$QueryUrl}" class="font-weight-bold">
                                    <xsl:value-of select="t:orgName"/>
                                    <xsl:if test="t:settlement">
                                        <xsl:text>, </xsl:text><xsl:value-of select="t:settlement"/>
                                    </xsl:if>
                                </a>
                                <xsl:text> </xsl:text>
                            </h4>
                            <div class="col-2">
                                <xsl:if test="contains(t:orgName/@ref, 'd-nb.info/gnd')">
                                    <a target="_blank" title="GND">
                                        <xsl:attribute name="href">
                                            <xsl:choose>
                                                <xsl:when test="contains(t:orgName/@ref, ' ')">
                                                    <xsl:value-of select="substring-before(t:orgName/@ref, ' ')"/>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:value-of select="t:orgName/@ref"/>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:attribute>
                                        <img src="{$Icon_gnd}" class="img-responsive icon" alt="Person" />
                                    </a>
                                </xsl:if>
                                <xsl:if test="@corresp">
                                    <a href="{@corresp}" target="_blank">
                                        <xsl:attribute name="title">
                                            <i18n:text>toexternresource</i18n:text>
                                        </xsl:attribute>
                                        <!--<xsl:choose>
                                            <xsl:when test="$locale = 'en'">
                                                <xsl:attribute name="title">
                                                    <i18n:text>toexternresource</i18n:text>
                                                </xsl:attribute>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:attribute name="title" select="'Zur externen Ressource'"/>
                                            </xsl:otherwise>
                                        </xsl:choose>-->
                                        <i class="fas fa-link"><xsl:text> </xsl:text></i>
                                    </a>
                                </xsl:if>
                            <!-- <a href="{s:gnd/@uri}" target="_blank">
                                    <xsl:text>GND</xsl:text>
                              </a>-->
                                <xsl:text> </xsl:text>
                             </div></div>
                        </div>
                    </xsl:for-each-group>
                    </div>
                </article>
    </xsl:template>
    
</xsl:stylesheet>
