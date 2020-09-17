<?xml version="1.0" encoding="UTF-8"?>

<!-- 
    Project: GAMS Projekttemplate
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
    Author: Christopher Pollin
    Last update: 2017
 -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="#all">
    
    <xsl:include href="szd-static.xsl"/>
    <xsl:include href="szd-Templates.xsl"/>
    
    <xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>
    
    <!-- Timeline http://bootsnipp.com/snippets/featured/timeline-responsive -->
    <xsl:template name="content">
        <section class="card">	
            <!--///CALL getStickyNavbar/// called in szd-Templates -->
            <xsl:call-template name="getStickyNavbar">
                <xsl:with-param name="Title">
                    <xsl:choose>
                        <xsl:when test="$locale = 'en'">
                            <xsl:text>Biography</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>Biographie</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:with-param>
                <xsl:with-param name="Content" select="//t:listEvent/t:event"/>
                <xsl:with-param name="PID" select="$PID"/>
                <xsl:with-param name="locale" select="$locale"/>
                <xsl:with-param name="GlossarRef" select="'Biography'"/>
            </xsl:call-template>   
             <!-- CONTENT -->
                <div class="row" id="content">		
                    <div class="col-12">
                        <ul class="timeline">
                            <xsl:for-each-group select="//t:listEvent/t:event" group-by="t:head/t:span[1]/t:date/substring(@when | @from, 1, 4)">
                                <xsl:variable name="actualYear" select="current-grouping-key()"/>
                                <xsl:variable name="Position" select="position()"/>
                                <!-- heading YEAR -->
                                <h2 class="text-left">
                                    <xsl:choose>
                                        <xsl:when test="contains($actualYear, '-')">
                                            <xsl:value-of select="substring-before($actualYear, '-')"/>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:value-of select="$actualYear"/>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                    <xsl:text> </xsl:text>
                                </h2>
                                <!-- ///////////////////// -->
                                <!-- every Entry in a year -->
                                <xsl:for-each-group select="current-group()" group-by="substring(t:head/t:span[1]/t:date/@when | t:head/t:span[1]/t:date/@from, 1,7)">
                                    <xsl:variable name="currentMonth" select="substring-after(current-grouping-key(), '-')"/>
                                    
                                    <xsl:for-each select="current-group()">
                                        <li id="{@xml:id}">
                                            <xsl:attribute name="class">
                                                <xsl:for-each select="$Position">
                                                    <xsl:if test=". mod 2 = 0">
                                                        <xsl:value-of select="'timeline-inverted'"/>
                                                    </xsl:if>
                                                </xsl:for-each>
                                            </xsl:attribute>
                                            <div class="timeline-panel">
                                                <xsl:apply-templates select="t:head"/>
                                                <xsl:choose>
                                                    <xsl:when test="$locale = 'en'">
                                                        <xsl:apply-templates select="t:ab[@xml:lang = 'en']"/>
                                                    </xsl:when>
                                                    <xsl:otherwise>
                                                        <xsl:apply-templates select="t:ab[@xml:lang = 'de']"/>
                                                    </xsl:otherwise>
                                                </xsl:choose>
                                                <div class="row card-footer small p-1 d-none d-sm-block" id="{concat('a_fo', substring-after(@xml:id, '.'))}">
                                                   <!-- <i class="fas fas fa-link small" data-toggle="collapse" data-target="{concat('#u', substring-after(@xml:id, '.'))}" style="color: #631a34">
                                                        <xsl:attribute name="title" select="'Link'"/>
                                                        <xsl:text> </xsl:text>
                                                    </i>
                                                    <span id="{$currentID}" class="collapse font-weight-light pl-2 small">
                                                        <xsl:value-of select="concat('stefanzweig.digital/o:szd.lebenskalender#', @xml:id)"/>
                                                    </span>-->
                                                    <xsl:variable name="permalink_id" select="concat('u', substring-after(@xml:id, '.'))"/>
                                                      <!--<xsl:call-template name="printPERMALINK">
                                                          <xsl:with-param name="locale" select="$locale"/>
                                                          <xsl:with-param name="id" select="$permalink_id"/>
                                                      </xsl:call-template>-->
                                                    <span class="text-center" data-toggle="collapse" data-target="#{$permalink_id}">
                                                        <i class="fas fa-link small" style="color: #631a34" title="Permalink">
                                                            <xsl:text> </xsl:text>
                                                        </i>
                                                        <span class="footer_icon_text display_block ml-2">
                                                            <xsl:choose>
                                                                <xsl:when test="$locale = 'en'">
                                                                    <xsl:text>Permalink</xsl:text>
                                                                </xsl:when>
                                                                <xsl:otherwise>
                                                                    <xsl:text>Permalink</xsl:text>
                                                                </xsl:otherwise>
                                                            </xsl:choose>
                                                            <xsl:text> </xsl:text>
                                                        </span>
                                                    </span>
                                                    <u id="{$permalink_id}" class="collapse font-weight-lightcard-body" style="color: #631a34" data-parent="{concat('#a_fo', substring-after(@xml:id, '.'))}">
                                                        <xsl:value-of select="concat('stefanzweig.digital/o:szd.lebenskalender#', @xml:id)"/>
                                                        <xsl:text> </xsl:text>
                                                        <i class="far fa-copy ml-2"  style="color: #631a34" onclick="copy({$permalink_id})">
                                                            <xsl:attribute name="title">
                                                                <xsl:choose>
                                                                    <xsl:when test="$locale = 'en'">
                                                                        <xsl:text>Copy Permalink</xsl:text>
                                                                    </xsl:when>
                                                                    <xsl:otherwise>
                                                                        <xsl:text>Permalink kopieren</xsl:text>
                                                                    </xsl:otherwise>
                                                                </xsl:choose>
                                                            </xsl:attribute>
                                                            <xsl:text> </xsl:text>
                                                        </i>
                                                    </u>
                                                </div>
                                            </div>
                                        </li>
                                    </xsl:for-each>
                                </xsl:for-each-group>
                            </xsl:for-each-group>
                        </ul>
                    </div>
                </div>
        </section>
    </xsl:template>
    

    <!-- //////////////////////////////////////////////////////////// -->
    <xsl:template match="t:event/t:head">
        <h3 class="text-uppercase">
            <xsl:choose>
                <xsl:when test="$locale = 'en'">
                    <xsl:apply-templates select="t:span[@xml:lang = 'en']"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="t:span[@xml:lang = 'de']"/>
                </xsl:otherwise>
            </xsl:choose>
        </h3>
    </xsl:template>
    
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- ///PERSON/// -->
    <xsl:template match="t:name[@type='person']">
        <xsl:variable name="SZDPER" select="substring-after(@ref, '#')"/>
        <xsl:variable name="BaseURL" select="'/archive/objects/query:szd.person_search/methods/sdef:Query/get?params='"/>
        <xsl:variable name="Param" select="encode-for-uri(concat('$1|&lt;https://gams.uni-graz.at/o:szd.personen#', $SZDPER, '&gt;', ';$2|', $locale))"/>
        <xsl:variable name="QueryUrl" select="concat($BaseURL, $Param, '&amp;locale=', $locale)"/>
        
        <a href="{$QueryUrl}" target="_blank">
          <xsl:choose>
              <xsl:when test="$locale = 'en'">
                  <xsl:attribute name="title" select="'Search query'"/>
              </xsl:when>
              <xsl:otherwise>
                  <xsl:attribute name="title" select="'Suchanfrage'"/>
              </xsl:otherwise>
          </xsl:choose>
          <u>
            <xsl:apply-templates/>
          </u>
        </a>
    </xsl:template>
    
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- ///BIBLIOTHEK/// -->
    <xsl:template match="t:name[@type='book']">
        <xsl:variable name="SZDBIB" select="@ref"/>
        <a href="{concat('/o:szd.bibliothek/sdef:TEI/get?locale=',$locale, $SZDBIB)}" target="_blank">
            <xsl:choose>
                <xsl:when test="$locale = 'en'">
                    <xsl:attribute name="title" select="'Access this entry in the library'"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="title" select="'Zum Eintrag in der Bibliothek'"/>
                </xsl:otherwise>
            </xsl:choose>
            <u>
                <xsl:apply-templates/>
            </u>
        </a>
    </xsl:template>
    
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- ///WERK/// -->
    <xsl:template match="t:name[@type='work']">
        <xsl:variable name="SZDMSK" select="@ref"/>
        <a href="{concat('/o:szd.werke/sdef:TEI/get?locale=',$locale, $SZDMSK)}" target="_blank">
            <xsl:choose>
                <xsl:when test="$locale = 'en'">
                    <xsl:attribute name="title" select="'Access this entry in the Works'"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="title" select="'Zum Eintrag in den Werken'"/>
                </xsl:otherwise>
            </xsl:choose>
            <u>
                <xsl:apply-templates/>
            </u>
        </a>
    </xsl:template>
    
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- ///Lebensdokumente/// -->
    <xsl:template match="t:name[@type='personaldocument']">
        <xsl:variable name="SZDLEB" select="@ref"/>
        <a href="{concat('/o:szd.lebensdokumente/sdef:TEI/get?locale=',$locale, $SZDLEB)}" target="_blank">
            <xsl:choose>
                <xsl:when test="$locale = 'en'">
                    <xsl:attribute name="title" select="'Access this entry in the Personal Documents'"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="title" select="'Zum Eintrag in den Lebensdokumenten'"/>
                </xsl:otherwise>
            </xsl:choose>
            <u>
                <xsl:apply-templates/>
            </u>
        </a>
    </xsl:template>
    
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- ///EXTERN/// -->
    <xsl:template match="t:name[@type='extern']">
        <xsl:variable name="URL" select="@ref"/>
        <a href="{$URL}" target="_blank">
            <xsl:choose>
                <xsl:when test="$locale = 'en'">
                    <xsl:attribute name="title" select="'Access external resource'"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="title" select="'Zu einer externen Ressource'"/>
                </xsl:otherwise>
            </xsl:choose>
            <u>
                <xsl:apply-templates/>
            </u>
        </a>
    </xsl:template>
    
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- ///HREF/// -->
    <xsl:template match="t:name[@type='href']">
        <xsl:variable name="URL" select="@ref"/>
        <a href="{$URL}" target="_blank" title="Wikipedia">
            <xsl:apply-templates/>
        </a>
    </xsl:template>
    
    <!-- ///HEAD/// -->
    <!--<xsl:template match="t:head">
        <div class="timeline-heading">
            <h3 class="timeline-title">
                <xsl:choose>
                    <xsl:when test="$locale = 'en'">
                        <xsl:apply-templates select="t:span[@xml:lang = 'en']"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:apply-templates select="t:span[@xml:lang = 'de']"/>
                    </xsl:otherwise>
                </xsl:choose>
            </h3>
        </div>
    </xsl:template>
    -->
    <!--    <xsl:template match="t:span[@xml:lang = 'en']">
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="t:span[@xml:lang = 'de']">
        <xsl:apply-templates/>
    </xsl:template>
    -->
    <!--<xsl:template match="t:ab[@xml:lang = 'en']">
        <div>1  
            <xsl:apply-templates></xsl:apply-templates>
        </div>  
    </xsl:template>
    
    <xsl:template match="t:ab[@xml:lang = 'de']">
        <div>
            <xsl:apply-templates></xsl:apply-templates>
        </div>  
    </xsl:template>-->
</xsl:stylesheet>