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
    
    <!-- ///WERKELISTE/// -->
    <xsl:template name="content">
            <!-- ///CALL NAVBAR in szd-Templates -->
            <xsl:call-template name="getStickyNavbar">
                <xsl:with-param name="Title">
                    <xsl:choose>
                        <xsl:when test="$locale = 'en'">
                            <xsl:text>Index of Works</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>Werkindex</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:with-param>
                <xsl:with-param name="Content" select="//t:listBibl/t:bibl/@sortKey"/>
                <xsl:with-param name="PID" select="'o:szd.werkindex'"/>
                <xsl:with-param name="locale" select="$locale"/>
                <!-- (i) -->
                <!--<xsl:with-param name="GlossarRef" select="'Werk'"/>-->
            </xsl:call-template>
            <!-- /// PAGE-CONTENT /// -->
            <!-- creates for every person an entry, including reference to GND and alphabetically sorted and linked -->
        <article id="content" class="card">
                <div class="list-group entryGroup">
                    <xsl:for-each-group select="//t:listBibl/t:bibl" group-by="substring(@sortKey, 1, 1)">
                        <xsl:sort select="current-grouping-key()"/>
                        <h2 id="{substring(@sortKey, 1, 1)}" class="mt-5">
                            <xsl:value-of select="current-grouping-key()"/>
                        </h2>
                        <xsl:for-each select="current-group()">
                            <xsl:sort select="@sortKey" data-type="text"/>
                            <div class="list-group-item mb-1 py-0" id="{@xml:id}">
                                <div class="row">
                                    <span class="col-10">
                                        <h4 class="text-left">
                                            <!--<xsl:variable name="BaseURL" select="'/archive/objects/query:szd.work_search/methods/sdef:Query/get?params='"/>
                                            <xsl:variable name="Param" select="encode-for-uri(concat('$1|&lt;https://gams.uni-graz.at/o:szd.personen#', @xml:id, '&gt;', ';$2|', $locale))"/>
                                            <xsl:variable name="QueryUrl" select="concat($BaseURL, $Param, '&amp;locale=', $locale)"/>-->
                                            <a href="#" class="font-weight-bold">
                                                <xsl:value-of select="t:title"/>
                                            </a>
                                        </h4>
                                    </span>
                                    <span class="col-2 text-center">
                                        <xsl:text> </xsl:text>
                                        <xsl:value-of select="t:lang"/>
                                        <xsl:text> </xsl:text>
                                        <xsl:value-of select="t:publisher"/>
                                        <xsl:text> </xsl:text>
                                    </span>
                                </div>
                            </div>
                        </xsl:for-each>
                    </xsl:for-each-group>
                    
                    
                    
                </div>   
            </article>
    </xsl:template>
    
</xsl:stylesheet>
