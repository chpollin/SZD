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
    xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:i18n="http://apache.org/cocoon/i18n/2.1"
    xmlns:search="http://gams.uni-graz.at/search#"
    
    exclude-result-prefixes="#all">
    
    <xsl:include href="szd-static.xsl"/>
    <xsl:include href="szd-Templates.xsl"/>
    <xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>
    
 
    <xsl:template name="content">
        <section class="card">	

        <xsl:variable name="RESULT_SET" select="//s:results/s:result"/>
        <!-- use PID to identify the object as a query result -->
        <xsl:variable name="PID" select="'query:szd'"/>
        
       <!-- # re = resource in szd, ?t = fulltextindex, ?sn = surname, ?fn = forename, ?h = head,  ?co = content,
        # ?fn_ed = forename editor, ?sn_ed = surname editor, ?ti = title, ?fn_co = forename composer, ?sn_co = surname composer,
        # ?d = date, ?sig = Signatur, ?ot = objecttype, ?col = collection -->
        <!-- ///CALL NAVBAR in szd-Templates -->
        <xsl:call-template name="getNavbar">
            <xsl:with-param name="Title">
                <xsl:choose>
                    <xsl:when test="$locale = 'en' and $RESULT_SET[1]">
                        <xsl:text>Search Results</xsl:text>
                    </xsl:when>
                    <xsl:when test="$locale = 'en'">
                        <xsl:text>No Entries Found</xsl:text>
                    </xsl:when>
                    <xsl:when test="$locale = 'de' and $RESULT_SET[1]">
                        <xsl:text>Suchergebnisse</xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>Es konnten keine Einträge gefunden werden</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:with-param>
            <xsl:with-param name="PID" select="'search'"/>
        </xsl:call-template>              
        <!-- //////////////////////////////////////////////////////////// -->
        <!-- CONTENT -->
        <article id="content">
            <div class="row">
                <div class="col-3 d-none d-sm-block">
                    <!-- called in Templates.xsl -->
                    <xsl:choose>
                        <xsl:when test="$RESULT_SET[1]">
                            <xsl:variable name="Filter_search">
                            <xsl:for-each-group select="//s:re/@uri" group-by="substring-before(., '#')">
                                <xsl:value-of select="current-grouping-key()"/>
                            </xsl:for-each-group>
                            </xsl:variable>
                            <xsl:call-template name="filter">
                              <xsl:with-param name="Filter_search" select="$Filter_search"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text> </xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </div>
            <!-- CONTENT -->
            <!-- //////////////////////////////////////////////////////////////// -->
            <div class="col">
                <div class="shadow-sm rounded border d-none d-sm-block">
                    <!-- //////////////////////////////////////////////////////////////// -->
                    <!-- Search Query -->
                    <div class="row">
                            <xsl:choose>
                                <xsl:when test="contains($RESULT_SET[1]/s:query/@uri, 'SZDPER')">
                                    <span class="font-weight-bold text-uppercase col-4">
                                        <i18n:text>searchquery_person</i18n:text>
                                        <xsl:text>: </xsl:text>
                                    </span>
                                    <span class="col-8">
                                        <xsl:value-of select="$RESULT_SET[1]/s:q_sn"/><xsl:if test="$RESULT_SET[1]/s:q_fn"><xsl:text>, </xsl:text><xsl:value-of select="$RESULT_SET[1]/s:q_fn"/></xsl:if>
                                    </span>
                                </xsl:when>
                                <xsl:when test="contains($RESULT_SET[1]/s:query/@uri, 'SZDSTA')">
                                    <span class="font-weight-bold text-uppercase col-4">
                                        <i18n:text>searchquery_location</i18n:text>
                                        <xsl:text>: </xsl:text>
                                    </span>
                                    <span class="col-8">
                                        <xsl:value-of select="$RESULT_SET[1]/s:q_n"/>
                                    </span>
                                </xsl:when>
                                <xsl:when test="contains($RESULT_SET[1]/s:query/@uri, 'SZDPUB')">
                                    <span class="font-weight-bold text-uppercase col-4">
                                         <i18n:text>searchquery_publication</i18n:text>
                                         <xsl:text>: </xsl:text>
                                    </span>
                                    <span class="col-8">
                                        <xsl:text>ToDo</xsl:text>
                                    </span>
                                </xsl:when>
                                <xsl:when test="contains($RESULT_SET[1]/s:query/@uri, 'o:szd.glossar')">
                                    <span class="font-weight-bold text-uppercase col-4">
                                      <i18n:text>searchquery_glossary</i18n:text>
                                      <xsl:text>: </xsl:text>
                                    </span>
                                    <span class="col-8">
                                        <xsl:value-of select="$RESULT_SET[1]/s:prefLabel"/>
                                    </span>
                                </xsl:when>
                                <xsl:otherwise>
                                    <span class="font-weight-bold text-uppercase col-4">
                                     <i18n:text>ftsearch</i18n:text>
                                     <xsl:text>: </xsl:text>
                                    </span>
                                </xsl:otherwise>
                            </xsl:choose>
                        <span class="col-8">
                            <xsl:value-of select="$RESULT_SET[1]/s:query"/>
                        </span>
                    </div>
                    <!-- //////////////////////////////////////////////////////////////// -->
                    <!-- Results -->
                    <div class="row">
                        <span class="font-weight-bold text-uppercase col-4">
                            <i18n:text>Results</i18n:text>
                            <xsl:text>: </xsl:text>
                        </span>
                        <span id="query_result" class="col-8">
                            <xsl:value-of select="count(distinct-values(//s:result/s:re/@uri))"/>
                      </span>
                    </div>
                </div>
                
                <!-- //////////////////////////////////////////////////////////////// -->
                <!-- results -->
                <div class="row" id="all_search" >
                <xsl:choose>
                    <!-- ///SEARCHRESULT/// -->
                    <!-- check if search result exists -->
                    <xsl:when test="$RESULT_SET[1]">
                        
                        <!-- if Collection found -->
                        <xsl:if test="$RESULT_SET/s:re/@uri[contains(.,'/o:szd.collection')]">
                            <div class="row" id="thema_search">
                                <xsl:for-each-group select="$RESULT_SET" group-by="s:re/@uri[contains(.,'/o:szd.collection')]">
                                    <xsl:for-each select="current-group()">
                                        
                                        <xsl:variable name="SZDPER" select="substring-after(s:re/@uri, '#')"/>
                                        <!-- OUTPUT OF FOUND PERSON -->
                                        <h3>
                                            <i18n:text>subjects</i18n:text>
                                            <a href="{concat(current-grouping-key(), '&amp;locale=', $locale)}" target="_blank" title="Collection">
                                                <xsl:value-of select="s:t"/>
                                            </a>
                                        </h3> 
                                    </xsl:for-each>
                                </xsl:for-each-group>
                            </div>
                        </xsl:if>
                        
                        <!-- if Person found -->
                        <!-- checks if a person was found and offers a list of names with href to person_search -->
                        <xsl:if test="$RESULT_SET/s:re/@uri[contains(.,'/o:szd.personen')]">
                            <!-- /////////////////////////////////////////// -->
                            <div class="col-12 mt-5" id="person_search">
                                <h3 class="text-uppercase">
                                    <i18n:text>persons</i18n:text>
                                </h3>
                                <xsl:for-each-group select="$RESULT_SET" group-by="s:re/@uri[contains(.,'SZDPER.')]">
                                    <xsl:sort select="s:sn"/>
                                    <xsl:for-each select="current-group()">
                                        <!-- OUTPUT OF FOUND PERSON -->
                                        <xsl:if test="s:sn">
                                        <h4 class="col-12 text-left">
                                            <xsl:variable name="SZDPER" select="substring-after(s:re/@uri, '#')"/>
                                            <img src="{$Icon_person}" class="img-responsive icon" alt="Person"/>
                                            <xsl:text> </xsl:text>
                                            <a href="{concat('/archive/objects/query:szd.person_search/methods/sdef:Query/get?params=$1|&lt;https%3A%2F%2Fgams.uni-graz.at%2Fo%3Aszd.personen%23', $SZDPER , '&gt;', '&amp;locale=', $locale)}" target="_blank">
                                                <xsl:value-of select="s:sn"/>
                                                <xsl:if test="s:fn">
                                                    <xsl:text>, </xsl:text><xsl:value-of select="s:fn"/>
                                                </xsl:if>
                                                <xsl:text> </xsl:text>  
                                            </a>
                                        </h4> 
                                        </xsl:if>
                                    </xsl:for-each>
                                </xsl:for-each-group>
                            </div>
                        </xsl:if>
                        
                        
                        <!-- if BiographicalEvent aka Lebenskalender found -->
                        <xsl:if test="$RESULT_SET/s:re/@uri[contains(.,'o:szd.lebenskalender#SZDBIO')]">
                            <div class="col-12 mt-5" id="biography_search">
                                <h3 class="text-uppercase">
                                    <i18n:text>biography</i18n:text>
                                </h3>
                                <ul>
                                    <xsl:for-each-group select="$RESULT_SET[s:locale_h = $locale]" group-by="s:re/@uri[contains(.,'o:szd.lebenskalender#SZDBIO')]">
                                        <xsl:sort select="s:d"/>
                                        <xsl:variable name="SZDBIO" select="substring-after(s:re/@uri, '#')"/>
                                            <!-- OUTPUT OF FOUND PERSON -->
                                            <li>
                                                <a class="small" href="{concat('/o:szd.lebenskalender/sdef:TEI/get?locale=', $locale, '#', $SZDBIO)}" target="_blank" onclick="scrolldown(this)">
                                                    <xsl:attribute name="title">
                                                        <xsl:choose>
                                                            <xsl:when test="$locale='en'">
                                                                <xsl:text>Go to Biography</xsl:text>
                                                            </xsl:when>
                                                            <xsl:otherwise>
                                                                <xsl:text>Zur Biographie</xsl:text>
                                                            </xsl:otherwise>
                                                        </xsl:choose>
                                                    </xsl:attribute>
                                                    <span class="font-weight-bold">
                                                        <xsl:value-of select="s:h"/>
                                                    </span>
                                                    <xsl:text>: </xsl:text>
                                                    <xsl:choose>
                                                        <xsl:when test="string-length(s:co)>50">
                                                            <xsl:value-of select="substring(s:co,1,50)"/>
                                                            <xsl:text>... </xsl:text>
                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <xsl:value-of select="s:co"/>
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                </a>
                                            </li>
                                    </xsl:for-each-group>
                                </ul>
                            </div>
                        </xsl:if>
                        <!-- search results ordered by collection which are used (@id) for hidding/filtering  -->
                        <xsl:for-each-group select="$RESULT_SET" group-by="substring-before(s:re/@uri, '#')">
                            <!--<xsl:sort select="current-grouping-key()" lang="ge"/>-->
                            <xsl:choose>
                                <xsl:when test="contains(current-grouping-key(), '/o:szd.personen')">
                                   <!-- do nothing -->
                                </xsl:when>
                                <xsl:when test="contains(current-grouping-key(), '/o:szd.werke')">
                                    <div class="col-12 list-group entryGroup mt-5" id="werke_search"> 
                                        <h3 class="text-uppercase"><i18n:text>work</i18n:text></h3>
                                        <xsl:call-template name="SearchListGroup">
                                             <xsl:with-param name="Current-Grouping-Key" select="current-grouping-key()"/>
                                             <xsl:with-param name="Current-Group" select="current-group()"/>
                                         </xsl:call-template>
                                    </div>
                                </xsl:when>
                                <xsl:when test="contains(current-grouping-key(), '/o:szd.lebensdokumente')">
                                    <div class="col-12 list-group entryGroup mt-5" id="lebensdokumente_search"> 
                                        <h3 class="text-uppercase"><i18n:text>personaldocument</i18n:text></h3>
                                        <xsl:call-template name="SearchListGroup">
                                            <xsl:with-param name="Current-Grouping-Key" select="current-grouping-key()"/>
                                            <xsl:with-param name="Current-Group" select="current-group()"/>
                                        </xsl:call-template>
                                    </div>
                                </xsl:when>
                                <xsl:when test="contains(current-grouping-key(), '/o:szd.bibliothek')">
                                    <div class="col-12 list-group entryGroup mt-5" id="bibliothek_search">
                                        <h3 class="text-uppercase"><i18n:text>library_szd</i18n:text></h3>
                                       <xsl:call-template name="SearchListGroup">
                                           <xsl:with-param name="Current-Grouping-Key" select="current-grouping-key()"/>
                                           <xsl:with-param name="Current-Group" select="current-group()[s:locale]"/>
                                       </xsl:call-template>
                                    </div>
                                </xsl:when>
                                <xsl:when test="contains(current-grouping-key(), '/o:szd.autographen')">
                                    <div class="col-12 list-group entryGroup mt-5" id="autographen_search">
                                        <h3 class="text-uppercase"><i18n:text>autograph</i18n:text></h3>
                                        <xsl:call-template name="SearchListGroup">
                                            <xsl:with-param name="Current-Grouping-Key" select="current-grouping-key()"/>
                                            <xsl:with-param name="Current-Group" select="current-group()"/>
                                        </xsl:call-template>
                                    </div>
                                </xsl:when>
                                <xsl:when test="contains(current-grouping-key(), '/o:szd.publikation')">
                                    <div class="col-12 list-group entryGroup mt-5" id="autographen_search">
                                        <h3 class="text-uppercase"><i18n:text>publication</i18n:text></h3>
                                        <xsl:call-template name="SearchListGroup">
                                            <xsl:with-param name="Current-Grouping-Key" select="current-grouping-key()"/>
                                            <xsl:with-param name="Current-Group" select="current-group()"/>
                                        </xsl:call-template>
                                    </div>
                                </xsl:when>
                                <xsl:otherwise>
                                    <!-- nope -->
                                </xsl:otherwise>
                            </xsl:choose>
                       </xsl:for-each-group>
                    </xsl:when>
                    <!-- ///NO SEARCHRESULT/// -->
                    <xsl:otherwise>
                        <div class="card-body col-12">
                            <div class="card-text">
                                <xsl:apply-templates select="document(concat('/context:szd/', 'SEARCH_HELP'))/t:TEI/t:text/t:body/t:div"/>
                            </div>
                        </div>
                    </xsl:otherwise>
                </xsl:choose>
                </div>
              </div>
           </div>
        </article>
        </section>
    </xsl:template>
    
    <!-- ///SEARCHRESULTS: LIST-GROUP with SPARQL s:results /// -->
    <xsl:template name="SearchListGroup">
        <xsl:param name="Current-Grouping-Key"/>
        <xsl:param name="Current-Group"/>
        <!-- to filter all entries with the same @uri, as SPARQL returns same URI's but with other variables: Titel, Originaltitel -->
        <xsl:for-each-group select="$Current-Group[s:sn | s:sn_ed | s:sn_co | s:sn_pi| s:sn_ap]" group-by="substring-after(s:re/@uri, '#')">  
           <!-- <xsl:sort select="s:rank" data-type="number"/>-->
            <xsl:sort select="s:sn" data-type="text" lang="ger"/>
            <xsl:sort select="s:sn_ed" data-type="text" lang="ger"/>
            <xsl:sort select="s:sn_co" data-type="text" lang="ger"/>
            <xsl:sort select="s:sn_pi" data-type="text" lang="ger"/>
            <xsl:sort select="s:sn_ap" data-type="text" lang="ger"/>
            <xsl:call-template name="createEntery"/>
            <!-- ////////////////////////////////// -->
            <!-- ENTRY -->
        </xsl:for-each-group>
        <xsl:if test="$Current-Group[not(s:sn | s:sn_ed | s:sn_co | s:sn_pi| s:sn_ap)]">
            <h3>
                <i18n:text>without_author</i18n:text>
            </h3>
            <xsl:for-each-group select="$Current-Group[not(s:sn | s:sn_ed | s:sn_co | s:sn_pi| s:sn_ap)]" group-by="substring-after(s:re/@uri, '#')">  
                <!-- <xsl:sort select="s:rank" data-type="number"/>-->
                <xsl:sort select="s:ti" data-type="text" lang="ger"/>
                <xsl:call-template name="createEntery"/>
                <!-- ////////////////////////////////// -->
                <!-- ENTRY -->
            </xsl:for-each-group>
        </xsl:if>
        
        
    </xsl:template>
    
    <xsl:template name="AddData-Databasket_Search">
        <xsl:attribute name="data-check">
            <xsl:text>unchecked</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="data-uri">
            <xsl:value-of select="current-grouping-key()"/>
        </xsl:attribute>
        <xsl:attribute name="data-author">
            <xsl:choose>
                <xsl:when test="s:sn">
                    <xsl:value-of select="concat(s:sn, ' ', s:fn)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="'o.V.'"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:attribute>
        <xsl:if test="s:ti">
            <xsl:attribute name="data-title">
                <xsl:value-of select="s:ti"/>
            </xsl:attribute>
        </xsl:if>
        <xsl:attribute name="data-date">
            <xsl:choose>
                <xsl:when test="s:d">
                    <xsl:value-of select="s:d"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="'o.D.'"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:attribute>
    </xsl:template>
    
    <xsl:template name="createEntery">
        <div class="list-group-item entry db_entry shadow-sm">
            <div class="bg-light row">
                <!-- DATABASKET -->
                <xsl:call-template name="AddData-Databasket_Search"/>
                
                <!-- ///PANEL-TITIEL/// -->
                <!-- creating collapse id -->
                <h4 class="card-title text-left col-10 small">
                    <xsl:variable name="PID" select="substring-before(substring-after(s:re/@uri, 'gams.uni-graz.at/'), '#')"/>
                    <a data-toggle="collapse" href="{concat('#c' , generate-id())}">
                        <span class="arrow">
                            <xsl:text>&#9660; </xsl:text>
                        </span>
                        <!-- AUTOR -->
                        <xsl:choose> 
                            <xsl:when test="s:sn">
                                <strong>
                                    <xsl:value-of select="s:sn[1]"/>
                                    <xsl:if test="s:fn">
                                        <xsl:text>, </xsl:text>
                                        <xsl:value-of select="s:fn"/>
                                    </xsl:if>
                                </strong>
                                <xsl:text>: </xsl:text>
                            </xsl:when>
                            <xsl:when test="s:sn_ed">
                                <strong>
                                    <xsl:value-of select="s:sn_ed"/>
                                    <xsl:if test="s:fn_ed"><xsl:text>, </xsl:text>
                                        <xsl:value-of select="s:fn_ed[1]"/>
                                    </xsl:if>
                                    <xsl:choose>
                                        <xsl:when test="$locale = 'en'">
                                            <xsl:text> (Editor) </xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text> (Herausgeber/in) </xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </strong>
                                <xsl:text>: </xsl:text>
                            </xsl:when>
                            <xsl:when test="s:sn_co">
                                <strong>
                                    <xsl:value-of select="s:sn_co"/>
                                    <xsl:if test="s:fn_co">
                                        <xsl:text>, </xsl:text>
                                        <xsl:value-of select="s:fn_co"/>
                                    </xsl:if>
                                    <xsl:text> (</xsl:text><i18n:text>composer</i18n:text><xsl:text>)</xsl:text>
                                </strong>
                                <xsl:text>: </xsl:text>
                            </xsl:when>
                            <!-- partie involved -->
                            <xsl:when test="s:sn_pi">
                                <strong>
                                    <xsl:value-of select="s:sn_pi"/>
                                    <xsl:if test="s:fn_pi"><xsl:text>, </xsl:text>
                                        <xsl:value-of select="s:fn_pi"/>
                                    </xsl:if>
                                    <xsl:text> (</xsl:text><i18n:text>partiesinvolved</i18n:text><xsl:text>)</xsl:text>
                                </strong>
                                <xsl:text>: </xsl:text>
                            </xsl:when>
                            <!-- affected person -->
                            <xsl:when test="s:sn_ap">
                                <strong>
                                    <xsl:value-of select="s:sn_ap"/>
                                    <xsl:if test="s:fn_ap"><xsl:text>, </xsl:text>
                                        <xsl:value-of select="s:fn_ap"/>
                                    </xsl:if>
                                    <xsl:text> (</xsl:text><i18n:text>person_affected</i18n:text><xsl:text>)</xsl:text>
                                </strong>
                                <xsl:text>: </xsl:text>
                            </xsl:when>
                            <xsl:otherwise>
                                <strong>o. V.:</strong><xsl:text> </xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                        <!-- TITEL, OBJECTTYP, SIGNATURE,  -->
                        <!-- current-group() because of multiple titles with langauge tag -->
                        <xsl:for-each select="current-group()">
                            <span class="font-italic">
                                <xsl:choose>
                                    <xsl:when test="$locale = 'en'">
                                        <xsl:choose>
                                            <xsl:when test="s:ti[following-sibling::s:locale[text()='en']]">
                                                <xsl:value-of select="s:ti[following-sibling::s:locale[text()='en']]"/>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:value-of select="s:ti"/>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </xsl:when>
                                    <xsl:when test="s:ti[following-sibling::s:locale[text()='de']]">
                                        <xsl:value-of select="s:ti[following-sibling::s:locale[text()='de']]"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select="s:ti"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </span>
                        </xsl:for-each>
                        <xsl:if test="s:ot">
                            <xsl:text> | </xsl:text>
                            <xsl:value-of select="s:ot"/>
                        </xsl:if>
                        <xsl:if test="s:sig">
                            <xsl:text> | </xsl:text>
                            <xsl:value-of select="s:sig"/> 
                        </xsl:if>
                        <xsl:if test="s:d">
                            <xsl:text> | </xsl:text>
                            <xsl:choose>
                                <xsl:when test="s:d castable as xs:date">
                                    <xsl:value-of select="year-from-date(s:d)"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="s:d"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:if>  
                    </a>
                </h4>
                    <xsl:variable name="currentPID" select="substring-after(s:pid/@uri, 'uni-graz.at/')"/>
                    <span class="col-1">
                        <xsl:if test="$currentPID">
                            <a  href="{concat('/archive/objects/', $currentPID, '/methods/sdef:IIIF/getMirador')}">
                                <img src="{$Icon_viewer}"  class="img-responsive icon_navbar" alt="Viewer"/>
                            </a>
                        </xsl:if>
                        <xsl:text> </xsl:text>
                    </span>
                    <xsl:call-template name="getLabelDatabasket">
                        <xsl:with-param name="locale" select="$locale"/>
                    </xsl:call-template>
            </div>
            <div class="card-body card-collapse collapse" id="{concat('c' , generate-id())}">
                <div class="table-responsive">
                    <table class="table table-sm">
                        <tbody>
                            <!-- ///Verfasser/// -->
                            <xsl:if test="s:sn">
                                <tr class="row">
                                    <td class="col-3">
                                        <!-- if object like "Haarlocke Goethes" than ... otherwise author-->
                                        <i18n:text>author_szd</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:call-template name="PersonSearch">
                                            <xsl:with-param name="locale"/>
                                        </xsl:call-template>
                                        <xsl:text> </xsl:text>
                                        <img src="{$Icon_suche_template}" class="img-responsive icon" alt="Person"/>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- ///Composer/// -->
                            <xsl:if test="s:sn_co">
                                <tr class="row">
                                    <td class="col-3">
                                        <!-- if object like "Haarlocke Goethes" than ... otherwise author-->
                                        <i18n:text>composer</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:sn_co"/>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- ///Betroffene Person/// -->
                            <xsl:if test="s:sn_ap">
                                <tr class="row">
                                    <td class="col-3">
                                        <i18n:text>person_affected</i18n:text>                            
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:sn_ap"/>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- ///Beteilgite Person/// -->
                            <xsl:if test="s:sn_pi">
                                <tr class="row">
                                    <td class="col-3">
                                        <i18n:text>partiesinvolved</i18n:text>                            
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:sn_pi"/>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- ///TITEL/// -->
                            <tr class="row">
                                <td class="col-3">
                                    <i18n:text>Titel</i18n:text>
                                </td>
                                <td class="col-9">
                                    <a href="{substring-after(s:re/@uri, 'gams.uni-graz.at')}" target="_blank"  id="{substring-after(s:re/@uri, '#')}">
                                        <xsl:attribute name="title">
                                            <xsl:choose>
                                                <xsl:when test="$locale = 'en'">
                                                    <xsl:text>To the Resource</xsl:text>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:text>Zur Ressource</xsl:text>
                                                </xsl:otherwise>
                                            </xsl:choose> 
                                        </xsl:attribute>
                                        <xsl:value-of select="s:ti"/>
                                    </a>
                                </td>
                            </tr>
                            
                            <xsl:if test="s:co">
                                <tr class="row">
                                    <td class="col-3">
                                        <i18n:text>description</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:co"/>
                                    </td>
                                </tr>
                            </xsl:if>
                            <xsl:if test="s:la">
                                <tr class="row">
                                    <td class="col-3">
                                        <i18n:text>language</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:la"/>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- ///UMFANG/// -->
                            <xsl:if test="s:ex">
                                <tr class="group row">
                                    <td class="col-3">
                                        <i18n:text>physicaldescription</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:ex"/>
                                    </td>
                                </tr>	                                        	 		
                            </xsl:if>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- //////Acquired = Ewerb -->
                            <xsl:if test="s:ac">
                                <tr class="group row">
                                    <td class="col-3">
                                        <i18n:text>acquired</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:ac"/>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- ///Provenienz/// -->
                            <xsl:if test="s:pr">
                                <tr class="row">
                                    <td class="col-3">
                                        <i18n:text>provenance</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:pr"/>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- ///Standort/// -->
                            <xsl:if test="s:lo">
                                <tr class="row">
                                    <td class="col-3">
                                        <i18n:text>currentlocation</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:lo/@uri"/>
                                    </td>
                                </tr>
                            </xsl:if>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
    </xsl:template>

  
    
   
    
    
</xsl:stylesheet>
