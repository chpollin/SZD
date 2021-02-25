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
                <xsl:with-param name="Content" select="//t:listPerson/t:person/t:persName/t:surname"/>
                <xsl:with-param name="PID" select="'o:szd.personen'"/>
                <xsl:with-param name="locale" select="$locale"/>
                <xsl:with-param name="GlossarRef" select="'Person'"/>
            </xsl:call-template>
            <!-- /// PAGE-CONTENT /// -->
            <!-- creates for every person an entry, including reference to GND and alphabetically sorted and linked -->
        <article id="content" class="card">
                <div class="list-group entryGroup">       
                    <xsl:for-each-group select="//t:listPerson/t:person" group-by="substring(t:persName/t:surname|t:persName/t:name, 1, 1)">
                        <xsl:sort select="current-grouping-key()"/>
                        <!-- ////////////////////////////// -->
                        <h2 id="{current-grouping-key()}" class="mt-5">
                            <xsl:value-of select="current-grouping-key()"/>
                        </h2>
                        <xsl:for-each select="current-group()">
                            <xsl:sort select="t:persName/t:surname|t:persName/t:name" data-type="text"/>
                            <div class="list-group-item mb-1 py-0" id="{@xml:id}">
                                <div class="row">
                                    <span class="col-10">
                                        <h4 class="text-left">
                                            <xsl:variable name="BaseURL" select="'/archive/objects/query:szd.person_search/methods/sdef:Query/get?params='"/>
                                            <xsl:variable name="Param" select="encode-for-uri(concat('$1|&lt;https://gams.uni-graz.at/o:szd.personen#', @xml:id, '&gt;', ';$2|', $locale))"/>
                                            <xsl:variable name="QueryUrl" select="concat($BaseURL, $Param, '&amp;locale=', $locale)"/>
                                            
                                            <a href="{$QueryUrl}" class="font-weight-bold">
                                            <xsl:choose>
                                                <xsl:when test="t:persName/t:surname">
                                                    <xsl:value-of select="t:persName/t:surname"/>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:value-of select="t:persName/t:name"/>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                            <xsl:if test="t:persName/t:forename">
                                                <xsl:text>, </xsl:text>
                                                <xsl:value-of select="t:persName/t:forename"/>
                                            </xsl:if>
                                        </a>
                                            <!-- /////// -->
                                            <!-- birth -->
                                            <xsl:variable name="Birth">
                                                <xsl:choose>
                                                    <!-- YYYY-MM-DD -->
                                                    <xsl:when test="t:birth/@when castable as xs:date">
                                                        <xsl:value-of select="year-from-date(t:birth/@when)"/>
                                                    </xsl:when>
                                                    <xsl:when test="string-length(t:birth/@when) = 4">
                                                        <xsl:value-of select="t:birth/@when"/>
                                                    </xsl:when>
                                                    <xsl:otherwise/>
                                                </xsl:choose>
                                            </xsl:variable>
                                            <!-- death -->
                                            <xsl:variable name="Death">
                                                <xsl:choose>
                                                    <xsl:when test="t:death/@when castable as xs:date">
                                                        <xsl:value-of select="year-from-date(t:death/@when)"/>
                                                    </xsl:when>
                                                    <xsl:when test="string-length(t:death/@when) = 4">
                                                        <xsl:value-of select="t:death/@when"/>
                                                    </xsl:when>
                                                    <xsl:otherwise></xsl:otherwise>
                                                </xsl:choose>
                                            </xsl:variable>
                                            <xsl:if test="not($Birth = '') and not($Death = '')">
                                                <xsl:text> </xsl:text>
                                                <span style="color: #631a34;">
                                                    <xsl:text>(</xsl:text>
                                                    <xsl:value-of select="$Birth"/><xsl:text>–</xsl:text><xsl:value-of select="$Death"/>
                                                    <xsl:text>)</xsl:text>
                                                </span>
                                            </xsl:if>
                                        </h4>
                                        <xsl:text> </xsl:text>
                                    </span>
                                    <span class="col-2 text-center">
                                        <xsl:text> </xsl:text>
                                        <!-- if GND @ref -->
                                        <xsl:if test="contains(t:persName/@ref, 'd-nb.info/gnd')">
                                            <a target="_blank" title="GND">
                                                <xsl:attribute name="href">
                                                    <xsl:choose>
                                                        <xsl:when test="contains(t:persName/@ref, ' ')">
                                                            <xsl:value-of select="substring-before(t:persName/@ref, ' ')"/>
                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <xsl:value-of select="t:persName/@ref"/>
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                </xsl:attribute>
                                                <img src="{$Icon_gnd}" class="img-responsive icon" alt="GND Icon"/>
                                            </a>
                                         </xsl:if>
                                        <!--<xsl:if test="contains(t:persName/@ref, 'wikidata.org')">
                                            <a href="{substring-after(t:persName/@ref, ' ')}" target="_blank" title="Wikidata">
                                                <img src="{$Icon_wikidata}" class="img-responsive icon" alt="Person" width="50"/>
                                            </a>
                                        </xsl:if>-->
                                        <xsl:if test="t:idno[@type='wikidata']">
                                            <a href="{t:idno[@type='wikidata']}" target="_blank" title="Wikidata">
                                                <img src="{$Icon_wikidata}" class="img-responsive icon" alt="Wikidata Icon" width="50"/>
                                            </a>
                                        </xsl:if>
                                         <xsl:text> </xsl:text>
                                         <xsl:if test="@corresp">
                                            <a href="{@corresp}" target="_blank" title="Wikipedia">
                                                <img src="{$Icon_wiki}" alt="Wikipedia Icon" width="25"/>
                                            </a>
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
