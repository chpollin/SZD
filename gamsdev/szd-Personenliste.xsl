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
            <!-- ///CALL NAVBAR in szd-Templates -->
            <xsl:call-template name="getStickyNavbar">
                <xsl:with-param name="Title">
                    <xsl:choose>
                        <xsl:when test="$locale = 'en'">
                            <xsl:text>Persons</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>Personen</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:with-param>
                <xsl:with-param name="Content" select="//t:listPerson/t:person/t:persName[not(@type)]/t:surname"/>
                <xsl:with-param name="PID" select="'o:szd.personen'"/>
                <xsl:with-param name="locale" select="$locale"/>
            </xsl:call-template>
            <!-- /// PAGE-CONTENT /// -->
            <!-- creates for every person an entry, including reference to GND and alphabetically sorted and linked -->
            <article id="content">
                <div class="list-group entryGroup">       
                    <xsl:for-each-group select="//t:listPerson/t:person" group-by="substring(t:persName[not(@type)]/t:surname|t:persName[not(@type)]/t:name, 1, 1)">
                        <xsl:sort select="current-grouping-key()"></xsl:sort>
                        <!-- ////////////////////////////// -->
                        <xsl:for-each select="current-group()">
                            
                            <span id="{current-grouping-key()}"><xsl:text> </xsl:text></span>
                            <div class="list-group-item shadow-sm" id="{@xml:id}">
                                <div class="row">
                                    <h4 class="text-left col-8">
                                        <xsl:variable name="BaseURL" select="'/archive/objects/query:szd.person_search/methods/sdef:Query/get?params='"/>
                                        <xsl:variable name="Param" select="encode-for-uri(concat('$1|&lt;https://gams.uni-graz.at/o:szd.personen#', @xml:id, '&gt;'))"/>
                                        <xsl:variable name="QueryUrl" select="concat($BaseURL, $Param, '&amp;locale=', $locale)"/>
                                        
                                        <a href="{$QueryUrl}" class="font-weight-bold">
                                        <xsl:choose>
                                            <xsl:when test="t:persName[not(@type)]/t:surname">
                                                <xsl:value-of select="t:persName[not(@type)]/t:surname"/>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:value-of select="t:persName[not(@type)]/t:name"/>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                        <xsl:if test="t:persName[not(@type)]/t:forename">
                                            <xsl:text>, </xsl:text>
                                            <xsl:value-of select="t:persName[not(@type)]/t:forename"/>
                                        </xsl:if>
                                    </a>
                                    </h4>
                                    <span class="col">
                                        <xsl:text> </xsl:text>
                                        <!-- if GND @ref -->
                                        <xsl:if test="contains(t:persName[not(@type)]/@ref, 'd-nb.info/gnd')">
                                            <a target="_blank" title="GND">
                                                <xsl:attribute name="href">
                                                    <xsl:choose>
                                                        <xsl:when test="contains(t:persName[not(@type)]/@ref, ' ')">
                                                            <xsl:value-of select="substring-before(t:persName[not(@type)]/@ref, ' ')"/>
                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <xsl:value-of select="t:persName[not(@type)]/@ref"/>
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                </xsl:attribute>
                                                <img src="{$Icon_person}" class="img-responsive icon" alt="Person" />
                                            </a>
                                         </xsl:if>
                                        <xsl:if test="contains(t:persName[not(@type)]/@ref, 'wikidata.org')">
                                            <a href="{substring-after(t:persName[not(@type)]/@ref, ' ')}" target="_blank" title="Wikidata">
                                                <img src="{$Icon_wikidata}" class="img-responsive icon" alt="Person" width="50"/>
                                            </a>
                                        </xsl:if>
                                         <xsl:text> </xsl:text>
                                         <xsl:if test="@corresp">
                                            <a href="{@corresp}" target="_blank" title="Wikipedia">
                                                <img src="{$Icon_wiki}" alt="Wiki" width="25"/>
                                            </a>
                                          </xsl:if>
                                    </span>
                                 <span class="col-md">
                                     <!-- birth -->
                                     <xsl:variable name="Birth">
                                         <xsl:choose>
                                             <xsl:when test="t:birth/@when castable as xs:date">
                                                 <xsl:value-of select="year-from-date(t:birth/@when )"/>
                                             </xsl:when>
                                             <xsl:otherwise></xsl:otherwise>
                                          </xsl:choose>
                                     </xsl:variable>
                                     <!-- death -->
                                     <xsl:variable name="Death">
                                         <xsl:choose>
                                             <xsl:when test="t:death/@when castable as xs:date">
                                                 <xsl:value-of select="year-from-date(t:death/@when )"/>
                                             </xsl:when>
                                             <xsl:otherwise></xsl:otherwise>
                                         </xsl:choose>
                                     </xsl:variable>
                                     <xsl:if test="not($Birth = '') and not($Death = '')">
                                      <span style="color: #631a34;"><xsl:text>(</xsl:text>
                                          <xsl:value-of select="$Birth"/><xsl:text>–</xsl:text><xsl:value-of select="$Death"/>
                                          <xsl:text>)</xsl:text></span>
                                     </xsl:if>
                                 </span>
                            </div>
                            </div>
                        </xsl:for-each>
                 </xsl:for-each-group>
                </div>   
            </article>
    </xsl:template>
    
</xsl:stylesheet>
