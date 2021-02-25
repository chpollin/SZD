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
    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:i18n="http://apache.org/cocoon/i18n/2.1"
    exclude-result-prefixes="#all">
    
    <xsl:include href="szd-static.xsl"/>
    <xsl:include href="szd-Templates.xsl"/>
    <xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>
    
    
    <!-- ///AUTOGRAPHEN/// -->
    <xsl:template name="content">
        <section class="card">
            <xsl:variable name="biblFull" select="//t:body/t:listBibl/t:biblFull"/>
            <xsl:variable name="Sender" select="$biblFull/t:profileDesc/t:correspDesc/t:correspAction[@type='sent']/t:persName | 
                $biblFull/t:profileDesc/t:correspDesc/t:correspAction[@type='sent']/t:name"/>
            <!-- call getStickyNavbar in szd-Templates.xsl -->
                <xsl:call-template name="getStickyNavbar">
                    <xsl:with-param name="Title">
                        <xsl:choose>
                            <xsl:when test="$locale = 'en'">
                                <xsl:text>Korrespondenzen</xsl:text>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:text>Korrespondenzen</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:with-param>
                    <!--<xsl:with-param name="Category" select="$biblFull/t:profileDesc/t:textClass/t:keywords/t:term[@type='classification'][@xml:lang=$locale]"/>-->
                    <!-- $biblFull/t:profileDesc/t:textClass/t:keywords/t:term[@type='person_affected'][1]/t:persName/t:surname -->
                    <xsl:with-param name="Content" select="$Sender"/>
                    <xsl:with-param name="PID" select="$PID"/>
                    <xsl:with-param name="locale" select="$locale"/>
                </xsl:call-template>
                
                <!-- /// PAGE-CONTENT /// -->
                <article class="card-body" id="content">
                    <!-- select every biblFull and group through t:author -->
                    
                    <xsl:for-each-group select="$biblFull" group-by="t:profileDesc/t:correspDesc/t:correspAction[@type='sent']/t:persName| 
                        t:profileDesc/t:correspDesc/t:correspAction[@type='sent']/t:name">  
                        <xsl:sort data-type="text" lang="ger" select="current-grouping-key()"/>
                        
                        <xsl:variable name="person_affected" select="t:profileDesc/t:textClass/t:keywords/t:term[@type='person_affected'][1]"/>
                        
                        <xsl:variable name="author" select="t:profileDesc/t:correspDesc/t:correspAction[@type='sent']"/>
                        
                        <xsl:call-template name="getfirstforABC">
                            <xsl:with-param name="Persons" select="$Sender"/>
                            <xsl:with-param name="CurrentNodes" select="t:profileDesc/t:correspDesc/t:correspAction[@type='sent']/t:persName/t:surname| 
                                t:profileDesc/t:correspDesc/t:correspAction[@type='sent']/t:name"/>
                        </xsl:call-template>
                        
                        <!-- if this is the first element beginning with 'A' give it e.g. id="A"; checked by the -->  
                        <!-- current SZDPER -->
                        <xsl:variable name="SZDPER">
                            <!-- called in szd-Templates -->
                            <xsl:call-template name="GetPersonList">
                                <xsl:with-param name="Person" select="$author[not(@role)]/@ref | t:fileDesc/t:titleStmt/t:editor[not(@role)][not(preceding-sibling::t:author[not(@role)])]"/>
                            </xsl:call-template>
                        </xsl:variable>
                        <!--<h3 id="{$SZDPER}">-->
                        <div class="list-group">
                            <xsl:if test="not(position()=1)">
                                <xsl:attribute name="class">
                                    <xsl:text>list-group mt-4</xsl:text>
                                </xsl:attribute>
                            </xsl:if>
                            <h3>
                                <xsl:choose>
                                    <xsl:when test="$person_affected">
                                        <xsl:call-template name="printAuthor">
                                            <xsl:with-param name="currentAuthor" select="$person_affected"/>
                                        </xsl:call-template>
                                        <xsl:text> (</xsl:text>
                                        <xsl:choose>
                                            <xsl:when test="$locale = 'en'">
                                                <xsl:text>affected party</xsl:text>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:text>betroffene Person</xsl:text>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                        <xsl:text>)</xsl:text>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:call-template name="printAuthor">
                                            <xsl:with-param name="currentAuthor" select="$author"/>
                                        </xsl:call-template>
                                    </xsl:otherwise>
                                </xsl:choose>
                               
                            </h3>
                        <!-- Go through all entries connected to xpath selection in group-by -->
                        <!-- list ccontent -->
                        <xsl:for-each select="current-group()">
                            <xsl:sort data-type="text" lang="ger" select="t:fileDesc/t:titleStmt/t:title[1]"/>
                            <div class="list-group-item entry db_entry shadow-sm" id="{@xml:id}">
                                <!-- //// -->
                                <!-- getEntry_SZDBIB_SZDKOR -->
                                <xsl:call-template name="AddData-Databasket"/>
                                <div class="bg-light row">
                                    <h4 class="card-title text-left col-9 small">
                                        <a data-toggle="collapse" href="{concat('#c' , generate-id())}">
                                            <span class="arrow">
                                                <xsl:text>▼ </xsl:text>
                                            </span>
                                            <span>
                                            <!--<xsl:call-template name="printEnDe">
                                                <xsl:with-param name="path" select="t:fileDesc/t:titleStmt/t:title"/>
                                                <xsl:with-param name="locale" select="$locale"/>
                                            </xsl:call-template>-->
                                                <xsl:text>Briefkonvolut</xsl:text>
                                            </span>
                                        </a>
                                        <!-- Signatur -->
                                        <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno[@type='signature']">
                                            <xsl:text> | </xsl:text>
                                            <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno[@type='signature']"/>                                                                     
                                        </xsl:if>
                                    </h4>
                                   
                                    <!-- checkbox databasket -->
                                    <xsl:call-template name="getLabelDatabasket">
                                        <xsl:with-param name="locale" select="$locale"/>
                                        <xsl:with-param name="SZDID" select="@xml:id"/>
                                    </xsl:call-template>
                                </div>
                                <!-- //// -->
                                <!-- FillbiblFull_SZDKOR -->
                                <div class="card-body card-collapse collapse" id="{concat('c' , generate-id())}">
                                    <xsl:call-template name="FillbiblFull_SZDKOR">
                                        <xsl:with-param name="locale" select="$locale"/>
                                        <xsl:with-param name="PID" select="$PID"/>
                                    </xsl:call-template>
                                </div>
                            </div>
                        </xsl:for-each>
                        </div>
                    </xsl:for-each-group>
                    
                    <!-- /////////////////////////////////////////////////// -->
                    <!-- all biblFull without an author[@role = "Verfasser"] -->
                    <!-- ? -->
                </article>
        </section>        
    </xsl:template>

</xsl:stylesheet>