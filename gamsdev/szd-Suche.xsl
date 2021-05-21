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
                <!--<xsl:choose>
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
                </xsl:choose>-->
                <xsl:choose>
                    <xsl:when test="$locale = 'en'">
                        <xsl:text>Search results</xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>Suchergebnisse</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:with-param>
            <xsl:with-param name="PID" select="'search'"/>
        </xsl:call-template>              
        <!-- //////////////////////////////////////////////////////////// -->
        <!-- CONTENT -->
        <article id="content">
            <!-- CONTENT -->
            <!-- //////////////////////////////////////////////////////////////// -->
            <div class="col">
                <div class="shadow-sm rounded border">
                    <!-- //////////////////////////////////////////////////////////////// -->
                    <!-- Search Query -->
                    <div class="row">
                            <div class="col-sm-8">
                                <div class="row">
                                    <xsl:choose>
                                    <xsl:when test="contains($RESULT_SET[1]/s:query/@uri, 'SZDPER')">
                                        <span class="font-weight-bold text-uppercase col-6">
                                            <i18n:text>searchquery_person</i18n:text>
                                            <xsl:text>: </xsl:text>
                                        </span>
                                        <span class="col-6">
                                            <xsl:value-of select="$RESULT_SET[1]/s:qs"/>
                                            <xsl:if test="$RESULT_SET[1]/s:qf"><xsl:text>, </xsl:text><xsl:value-of select="$RESULT_SET[1]/s:qf"/></xsl:if>
                                        </span>
                                    </xsl:when>
                                    <xsl:when test="contains($RESULT_SET[1]/s:query/@uri, 'SZDSTA')">
                                        <span class="font-weight-bold text-uppercase col-6">
                                            <i18n:text>searchquery_location</i18n:text>
                                            <xsl:text>: </xsl:text>
                                        </span>
                                        <span class="col-6">
                                            <!-- extracts SZDSTA from URI; gets orgName from $StandorteList and prints EN|DE -->
                                            <xsl:call-template name="printEnDe">
                                                <xsl:with-param name="locale" select="$locale"/>
                                                <xsl:with-param name="path" select="$StandorteList//t:org[@xml:id = substring-after($RESULT_SET[1]/s:lo/@uri, '#')]/t:orgName"/>
                                            </xsl:call-template>
                                        </span>
                                    </xsl:when>
                                    <!--<xsl:when test="contains($RESULT_SET[1]/s:query/@uri, 'SZDPUB')">
                                        <span class="font-weight-bold text-uppercase col-6">
                                             <i18n:text>searchquery_publication</i18n:text>
                                             <xsl:text>: </xsl:text>
                                        </span>
                                        <span class="col-8">
                                            <xsl:text>ToDo</xsl:text>
                                        </span>
                                    </xsl:when>-->
                                    <xsl:when test="contains($RESULT_SET[1]/s:query/@uri, 'o:szd.glossar')">
                                        <!-- -->
                                        <xsl:variable name="GLOSSAR">
                                            <xsl:copy-of select="document('/o:szd.glossar/ONTOLOGY')"/>
                                        </xsl:variable>
                                        <xsl:variable name="Query_URI" select="$RESULT_SET[1]/s:query/@uri"/>
                                        <span class="font-weight-bold text-uppercase col-6">
                                          <i18n:text>searchquery_glossary</i18n:text>
                                          <xsl:text>: </xsl:text>
                                        </span>
                                        <span class="col-6">
                                            <xsl:call-template name="printEnDe">
                                                <xsl:with-param name="locale" select="$locale"/>
                                                <xsl:with-param name="path" select="$GLOSSAR//*:Concept[@*:about = string($Query_URI)]/*:prefLabel"/>
                                            </xsl:call-template>
                                        </span>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <span class="font-weight-bold text-uppercase col-6">
                                         <i18n:text>ftsearch</i18n:text>
                                         <xsl:text>: </xsl:text>
                                        </span>
                                    </xsl:otherwise>
                            </xsl:choose>
                                 <span class="col-6">
                                     <xsl:value-of select="$RESULT_SET[1]/s:query"/>
                                 </span>
                                </div>
                                <div class="row">
                                    <span class="font-weight-bold text-uppercase col-6">
                                    <i18n:text>Results</i18n:text>
                                    <xsl:text>: </xsl:text>
                                </span>
                                <span id="query_result" class="col-6">
                                    <xsl:value-of select="count(distinct-values(//s:result/s:re/@uri))"/>
                                </span>
                           </div>
                         </div>
                        <div class="col-sm-4 d-print-none">
                            <div class="btn-group-vertical float-right">
                                <button type="button" class="btn small text-uppercase border" id="open_all">
                                        <xsl:choose>
                                            <xsl:when test="$locale='en'">
                                                <xsl:text>Expand all entries</xsl:text>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:text>Alle öffnen</xsl:text>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                  </button>
                                <button type="button" class="btn small text-uppercase border" onclick="window.print();">
                                    <xsl:choose>
                                        <xsl:when test="$locale='en'">
                                            <xsl:text>Print</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>Drucken</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </button>
                                <button type="button" class="btn small text-uppercase border disabled">
                                    <xsl:choose>
                                        <xsl:when test="$locale='en'">
                                            <xsl:text>Add all to databasket</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>Alle zum Datenkorb hinzufügen</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </button>
                                </div> 
                        </div>
                    </div>
                    <div class="col-sm-12 mt-4 d-print-none">
                        <xsl:choose>
                            <xsl:when test="$RESULT_SET[1]">
                                <xsl:variable name="Filter_search">
                                    <xsl:for-each-group select="//s:re/@uri" group-by="substring-before(., '#')">
                                        <xsl:value-of select="current-grouping-key()"/>
                                    </xsl:for-each-group>
                                </xsl:variable>
                                <!--<xsl:call-template name="filter">
                                    <xsl:with-param name="Filter_search" select="$Filter_search"/>
                                </xsl:call-template>-->
                                <div class="all_search col-sm-12 mb-2">
                                    <h3>FILTER</h3>
                                    <form id="SucheErweitert" class="form-inline">
                                        <div class="form-group mr-3 small">
                                            <label class="text-uppercase small">
                                                <input class="form-check-input" type="radio" name="optradio"  id="all_radio" value="all_search" onchange="filter(this)"/>
                                                <i18n:text>all</i18n:text>
                                            </label>
                                        </div>               
                                        <xsl:if test="contains($Filter_search, 'o:szd.autographen')">
                                            <div class="form-group mr-3 small">
                                                <label class="text-uppercase small">
                                                    <input class="form-check-input" type="radio" name="optradio" id="autograph_radio" value="autographen_search" onchange="filter(this)"/>
                                                    <i18n:text>autograph</i18n:text>
                                                </label>
                                            </div>
                                        </xsl:if>
                                        <xsl:if test="contains($Filter_search, 'o:szd.bibliothek')">
                                            <div class="form-group mr-3 small">
                                                <label class="text-uppercase small">
                                                    <input class="form-check-input" type="radio" name="optradio" id="bibliothek_radio" value="bibliothek_search" onchange="filter(this)"/>
                                                    <i18n:text>library_szd</i18n:text>
                                                </label>
                                            </div>
                                        </xsl:if>
                                        <xsl:if test="contains($Filter_search, 'o:szd.lebenskalender')">
                                            <div class="form-group mr-3 small">
                                                <label class="text-uppercase small">
                                                    <input class="form-check-input" type="radio" name="optradio" id="biography_radio" value="biography_search" onchange="filter(this)"/>
                                                    <i18n:text>biography</i18n:text>
                                                </label>
                                            </div>
                                        </xsl:if>
                                        <xsl:if test="contains($Filter_search, 'o:szd.lebensdokumente')">
                                            <div class="form-group mr-3 small">
                                                <label class="text-uppercase small">
                                                 <input class="form-check-input" type="radio" name="optradio" id="lebensdokumente_radio" value="lebensdokumente_search" onchange="filter(this)"/>
                                                 <i18n:text>personaldocument</i18n:text>
                                                </label>
                                            </div>
                                        </xsl:if>
                                        <xsl:if test="contains($Filter_search, 'o:szd.personen')">
                                            <div class="form-group mr-3 small">
                                                <label class="text-uppercase small">
                                                    <input class="form-check-input" type="radio" name="optradio" id="person_radio" value="person_search" onchange="filter(this)"/>
                                                    <i18n:text>persons</i18n:text>
                                                </label>
                                            </div>
                                        </xsl:if>
                                        <xsl:if test="contains($Filter_search, 'o:szd.werke')">
                                            <div class="form-group mr-3 small">
                                                <label class="text-uppercase small">
                                                    <input class="form-check-input" type="radio" name="optradio" id="werke_radio" value="werke_search" onchange="filter(this)"/>
                                                    <i18n:text>works</i18n:text>
                                                </label>
                                            </div>
                                        </xsl:if>
                                        <xsl:if test="contains($Filter_search, 'o:szd.korrespondenzen')">
                                            <div class="form-group mr-3 small">
                                                <label class="text-uppercase small">
                                                    <input class="form-check-input" type="radio" name="optradio" id="corresp_radio" value="corresp_search" onchange="filter(this)"/>
                                                    <i18n:text>correspondence</i18n:text>
                                                </label>
                                            </div>
                                        </xsl:if>
                                    </form>
                                    <!-- filter: hide elements -->
                                    <script>
                                        //goes through all collections, hides all others, shows pressed one.
                                        function filter(id) 
                                        {
                                        
                                        current = document.getElementById(id.value);
                                        if( 'all_search' != current.id)
                                        
                                        {
                                        children =  current.parentNode.childNodes;
                                        children.forEach(function(entry) {
                                        if( entry != current)
                                        {
                                        current.style.display = "block";
                                        entry.style.display = "none";
                                        }
                                        });
                                        }
                                        else
                                        {
                                        children.forEach(function(entry) {
                                        if( entry != current)
                                        {
                                        entry.style.display = "block";
                                        }
                                        });
                                        }
                                        }
                                    </script>
                                    <!-- Collapse all enries -->
                                    <script>
                                        $("#open_all").click(function(){
                                        
                                        if ($(this).data("closedAll")) {
                                        $(".card-body.collapse").collapse("show");
                                        }
                                        else {
                                        $(".card-body.collapse").collapse("hide");
                                        }
                                        
                                        // save last state
                                        $(this).data("closedAll",!$(this).data("closedAll")); 
                                        });
                                        
                                        // init with all closed
                                        $("#open_all").data("closedAll",true);
                                    </script>
                                </div>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:text> </xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                    </div>
                    <!-- //////////////////////////////////////////////////////////////// -->
                    <!-- Results -->
                    <!--<div class="row">
                        <span class="font-weight-bold text-uppercase col-4">
                            <i18n:text>Results</i18n:text>
                            <xsl:text>: </xsl:text>
                        </span>
                        <span id="query_result" class="col-8">
                            <xsl:value-of select="count(distinct-values(//s:result/s:re/@uri))"/>
                      </span>
                    </div>-->
                </div>
                
                <!-- //////////////////////////////////////////////////////////////// -->
                <!-- results -->
                <div  id="all_search" >
                <xsl:choose>
                    <!-- ///SEARCHRESULT/// -->
                    <!-- check if search result exists -->
                    <xsl:when test="$RESULT_SET[1]">
                        
                        <!-- if Collection found -->
                        <xsl:if test="$RESULT_SET/s:re/@uri[contains(.,'/o:szd.collection')]">
                            <div class="row" id="thema_search">
                                <xsl:for-each-group select="$RESULT_SET" group-by="s:re/@uri[contains(.,'/o:szd.collection')]">
                                    <xsl:sort select="current-grouping-key()"></xsl:sort>
                                    <!--<xsl:for-each select="current-group()">-->
                                        
                                        <xsl:variable name="SZDPER" select="substring-after(s:re/@uri, '#')"/>
                                        <!-- OUTPUT OF FOUND PERSON -->
                                        <h3>
                                            <i18n:text>subjects</i18n:text>
                                            <a href="{concat(current-grouping-key(), '&amp;locale=', $locale)}" target="_blank" title="Collection">
                                                <xsl:value-of select="s:t"/>
                                            </a>
                                        </h3> 
                                    <!--</xsl:for-each>-->
                                </xsl:for-each-group>
                            </div>
                        </xsl:if>
                        
                        <!-- if Person found -->
                        <!-- checks if a person was found and offers a list of names with href to person_search -->
                        <xsl:if test="$RESULT_SET/s:re/@uri[contains(.,'/o:szd.personen')]">
                            <!-- /////////////////////////////////////////// -->
                            <div class="col-12 mt-3" id="person_search">
                                <h3 class="text-uppercase">
                                    <i18n:text>persons</i18n:text>
                                </h3>
                                <xsl:for-each-group select="$RESULT_SET" group-by="s:re/@uri[contains(.,'SZDPER.')]">
                                    <xsl:sort select="s:s"/>
                                    <xsl:for-each select="current-group()">
                                        <!-- OUTPUT OF FOUND PERSON -->
                                        <xsl:if test="s:s">
                                        <h4 class="col-12 text-left">
                                            <xsl:variable name="SZDPER" select="substring-after(s:re/@uri, '#')"/>
                                            <xsl:variable name="BaseURL" select="'/archive/objects/query:szd.person_search/methods/sdef:Query/get?params='"/>
                                            <xsl:variable name="Param" select="encode-for-uri(concat('$1|&lt;https://gams.uni-graz.at/o:szd.personen#', $SZDPER, '&gt;', ';$2|', $locale))"/>
                                            <xsl:variable name="QueryUrl" select="concat($BaseURL, $Param, '&amp;locale=', $locale)"/>
                                            
                                            <img src="{$Icon_person}" class="img-responsive icon" alt="Person"/>
                                            <xsl:text> </xsl:text>
                                            <a href="{$QueryUrl}" target="_blank">
                                                <xsl:value-of select="s:s"/>
                                                <xsl:if test="s:f">
                                                    <xsl:text>, </xsl:text><xsl:value-of select="s:f"/>
                                                </xsl:if>
                                                <xsl:text> </xsl:text>  
                                            </a>
                                        </h4> 
                                        </xsl:if>
                                    </xsl:for-each>
                                </xsl:for-each-group>
                            </div>
                        </xsl:if>
                        <!-- ///////// -->
                        <!-- BIOGRAPHY -->
                        <xsl:if test="$RESULT_SET/s:re/@uri[contains(.,'o:szd.lebenskalender#SZDBIO')]">
                            <div class="col-12 mt-3" id="biography_search">
                                <h3 class="text-uppercase">
                                    <i18n:text>biography</i18n:text>
                                </h3>
                                <ul>
                                    <!-- locale:h contains 'enÄ or 'de' for the language -->
                                    <xsl:for-each-group select="$RESULT_SET" group-by="s:re/@uri[contains(.,'o:szd.lebenskalender#SZDBIO')]">
                                        <xsl:sort select="s:d"/>
                                        <xsl:variable name="SZDBIO" select="substring-after(s:re/@uri, '#')"/>
                                            <!-- OUTPUT OF FOUND PERSON -->
                                            <li>
                                                <a class="small" href="{concat('/o:szd.lebenskalender/sdef:TEI/get?locale=', $locale, '#', $SZDBIO)}" target="_blank">
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
                            <xsl:sort select="current-grouping-key()" lang="ger" order="descending"/>
                            <xsl:choose>
                                <xsl:when test="contains(current-grouping-key(), '/o:szd.personen')">
                                   <!-- do nothing -->
                                </xsl:when>
                                <xsl:when test="contains(current-grouping-key(), '/o:szd.werke')">
                                    <div class="col-12 list-group mt-5" id="werke_search"> 
                                        <h3 class="text-uppercase"><i18n:text>works</i18n:text></h3>
                                        <xsl:call-template name="SearchListGroup">
                                             <xsl:with-param name="Current-Grouping-Key" select="current-grouping-key()"/>
                                             <xsl:with-param name="Current-Group" select="current-group()"/>
                                         </xsl:call-template>
                                    </div>
                                </xsl:when>
                                <xsl:when test="contains(current-grouping-key(), '/o:szd.lebensdokumente')">
                                    <div class="col-12 list-group mt-5" id="lebensdokumente_search"> 
                                        <h3 class="text-uppercase"><i18n:text>personaldocument</i18n:text></h3>
                                        <xsl:call-template name="SearchListGroup">
                                            <xsl:with-param name="Current-Grouping-Key" select="current-grouping-key()"/>
                                            <xsl:with-param name="Current-Group" select="current-group()"/>
                                        </xsl:call-template>
                                    </div>
                                </xsl:when>
                                <xsl:when test="contains(current-grouping-key(), '/o:szd.bibliothek')">
                                    <div class="col-12 list-group mt-5" id="bibliothek_search">
                                        <h3 class="text-uppercase"><i18n:text>library_szd</i18n:text></h3>
                                       <xsl:call-template name="SearchListGroup">
                                           <xsl:with-param name="Current-Grouping-Key" select="current-grouping-key()"/>
                                           <xsl:with-param name="Current-Group" select="current-group()"/>
                                       </xsl:call-template>
                                    </div>
                                </xsl:when>
                                <xsl:when test="contains(current-grouping-key(), '/o:szd.autographen')">
                                    <div class="col-12 list-group mt-5" id="autographen_search">
                                        <h3 class="text-uppercase"><i18n:text>autograph</i18n:text></h3>
                                        <xsl:call-template name="SearchListGroup">
                                            <xsl:with-param name="Current-Grouping-Key" select="current-grouping-key()"/>
                                            <xsl:with-param name="Current-Group" select="current-group()"/>
                                        </xsl:call-template>
                                    </div>
                                </xsl:when>
                                <xsl:when test="contains(current-grouping-key(), '/o:szd.korrespondenzen')">
                                    <div class="col-12 list-group mt-5" id="corresp_search">
                                        <h3 class="text-uppercase"><i18n:text>correspondence</i18n:text></h3>
                                        <xsl:call-template name="SearchListGroup">
                                            <xsl:with-param name="Current-Grouping-Key" select="current-grouping-key()"/>
                                            <xsl:with-param name="Current-Group" select="current-group()"/>
                                        </xsl:call-template>
                                    </div>
                                </xsl:when>
                               <!-- <xsl:when test="contains(current-grouping-key(), '/o:szd.publikation')">
                                    <div class="col-12 list-group mt-5" id="autographen_search">
                                        <h3 class="text-uppercase"><i18n:text>publication</i18n:text></h3>
                                        <xsl:call-template name="SearchListGroup">
                                            <xsl:with-param name="Current-Grouping-Key" select="current-grouping-key()"/>
                                            <xsl:with-param name="Current-Group" select="current-group()"/>
                                        </xsl:call-template>
                                    </div>
                                </xsl:when>-->
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
                                <h2>
                                    <xsl:choose>
                                        <xsl:when test="$locale = 'en'">
                                           <xsl:text>No matches found</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>Es konnten keine Einträge gefunden werden</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </h2>
                                <p>
                                    <xsl:choose>
                                        <xsl:when test="$locale = 'en'">
                                            <xsl:text>No results matched your search query. Note: index and search results may include entries of persons not yet linked to a record</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>Zur Suchanfrage konnten keine Ergebnisse gefunden werden. Hinweis: Im Index und in Suchergebnissen werden bereits Einträge zu Personen angezeigt, die noch mit keinem Datensatz verknüpft sind.</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </p>
                                <h3 style="font-size: 20px;"  class="mt-5">
                                    <xsl:choose>
                                        <xsl:when test="$locale = 'en'">
                                            <xsl:text>Help on searching</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise><xsl:text>Hilfe zur Suche</xsl:text></xsl:otherwise>
                                    </xsl:choose>
                                </h3>
                                <div class="mt-3">
                                    <xsl:apply-templates select="document(concat('/context:szd/', 'SEARCH_HELP'))/t:TEI/t:text/t:body/t:div"/>
                                </div>
                            </div>
                        </div>
                    </xsl:otherwise>
                </xsl:choose>
                </div>
              </div>
        </article>
        </section>
    </xsl:template>
    
    <!-- SearchListGroup -->
    <xsl:template name="SearchListGroup">
        <xsl:param name="Current-Grouping-Key"/>
        <xsl:param name="Current-Group"/>
        <!-- to filter all entries with the same @uri, as SPARQL returns same URI's but with other variables: Titel, Originaltitel -->
        <xsl:for-each-group select="$Current-Group[s:a='T'][s:s | s:sed | s:sco | s:spi | s:sap | s:ss]" group-by="substring-after(s:re/@uri, '#')">  
           <!-- <xsl:sort select="s:rank" data-type="number"/>-->
            <xsl:sort select="s:s" data-type="text" lang="ger"/>
            <xsl:sort select="s:sed" data-type="text" lang="ger"/>
            <xsl:sort select="s:sco" data-type="text" lang="ger"/>
            <xsl:sort select="s:spi" data-type="text" lang="ger"/>
            <xsl:sort select="s:sap" data-type="text" lang="ger"/>
            <xsl:sort select="s:t" data-type="text" lang="ger"/>
            <!-- ////////////////////////////////// -->
            <!-- ENTRY -->
            <xsl:call-template name="createEntry"/>
        </xsl:for-each-group>
        <xsl:if test="$Current-Group[not(s:s | s:sed | s:sco | s:spi| s:sap | s:ss)][s:a='T']">
            <div class="mt-2 mb-2">
                <h3>
                    <i18n:text>without_author</i18n:text>
                </h3>
                <xsl:for-each-group select="$Current-Group[not(s:s | s:sed | s:sco | s:spi | s:sap | s:ss)]" group-by="substring-after(s:re/@uri, '#')">  
                    <!-- <xsl:sort select="s:rank" data-type="number"/>-->
                    <xsl:sort select="s:t" data-type="text" lang="ger"/>
                    <!-- ////////////////////////////////// -->
                    <!-- ENTRY without author -->
                    
                    <xsl:call-template name="createEntry"/>
                    
                </xsl:for-each-group>
            </div>
        </xsl:if>
        
        
    </xsl:template>
    
    <!--<xsl:template name="AddData-Databasket_Search">
        <xsl:attribute name="data-check">
            <xsl:text>unchecked</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="data-uri">
            <xsl:value-of select="current-grouping-key()"/>
        </xsl:attribute>
        <xsl:attribute name="data-author">
            <xsl:choose>
                <xsl:when test="s:s">
                    <xsl:value-of select="concat(s:s, ' ', s:f)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="'o.V.'"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:attribute>
        <xsl:if test="s:t">
            <xsl:attribute name="data-title">
                <xsl:value-of select="s:t"/>
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
    </xsl:template>-->
    
    <xsl:template name="createEntry">
        <xsl:variable name="PID" select="substring-before(substring-after(s:re/@uri, 'gams.uni-graz.at/'), '#')"/>
        <xsl:variable name="SZDID" select="substring-after(s:re/@uri, '#')"/>
        <xsl:variable name="currentPID" select="substring-after(s:pid/@uri, 'uni-graz.at/')"/>
        <div id="{$SZDID}" class="list-group-item entry db_entry shadow-sm" >
            <!-- DATABASKET -->
            <xsl:call-template name="AddData-Databasket">
                <xsl:with-param name="locale" select="$locale"/>
            </xsl:call-template>
            <div class="bg-light row">
                <!-- ///PANEL-TITIEL/// -->
                <!-- creating collapse id -->
                <h4 class="card-title text-left col-9 small">
                   <!-- -->
                    <a data-toggle="collapse" href="{concat('#c' , generate-id())}">
                        <span class="arrow">
                            <xsl:text>&#9660; </xsl:text>
                        </span>
                        <!-- AUTOR -->
                        <xsl:choose> 
                            <!-- s:s = surname; s:ss = sender surname -->
                            <xsl:when test="s:s | s:ss[1]">
                                <strong>
                                    <xsl:value-of select="s:s[1] | s:ss[1]"/>
                                    <xsl:if test="s:f  | s:sf[1]">
                                        <xsl:text>, </xsl:text>
                                        <xsl:value-of select="s:f | s:sf[1]"/>
                                    </xsl:if>
                                </strong>
                                <xsl:text>: </xsl:text>
                            </xsl:when>
                            <xsl:when test="s:sed">
                                <strong>
                                    <xsl:value-of select="s:sed"/>
                                    <xsl:if test="s:fed"><xsl:text>, </xsl:text>
                                        <xsl:value-of select="s:fed[1]"/>
                                    </xsl:if>
                                    <xsl:value-of select="if ($locale = 'en') then ' (Editor)' else ' (Herausgeber/in)'"/>
                                </strong>
                                <xsl:text>: </xsl:text>
                            </xsl:when>
                            <xsl:when test="s:sco">
                                <strong>
                                    <xsl:value-of select="s:sco"/>
                                    <xsl:if test="s:fco">
                                        <xsl:text>, </xsl:text>
                                        <xsl:value-of select="s:fco"/>
                                    </xsl:if>
                                    <xsl:text> (</xsl:text><i18n:text>composer</i18n:text><xsl:text>)</xsl:text>
                                </strong>
                                <xsl:text>: </xsl:text>
                            </xsl:when>
                            <!-- partie involved -->
                            <xsl:when test="s:spi">
                                <strong>
                                    <xsl:value-of select="s:spi"/>
                                    <xsl:if test="s:fpi"><xsl:text>, </xsl:text>
                                        <xsl:value-of select="s:fpi"/>
                                    </xsl:if>
                                    <xsl:text> (</xsl:text><i18n:text>partiesinvolved</i18n:text><xsl:text>)</xsl:text>
                                </strong>
                                <xsl:text>: </xsl:text>
                            </xsl:when>
                            <!-- affected person -->
                            <xsl:when test="s:sap">
                                <strong>
                                    <xsl:value-of select="s:sap"/>
                                    <xsl:if test="s:fap"><xsl:text>, </xsl:text>
                                        <xsl:value-of select="s:fap"/>
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
                            <span class="font-italic">
                                <xsl:value-of select="s:t"/>
                            </span>
                        <xsl:value-of select="$currentPID"/>
                        <!-- for SZDMSK and SZDLEB add: TITEL | SIGNATURE | SZDID -->
                        <xsl:if test="s:si and (contains($SZDID, 'SZDMSK') or (contains($SZDID, 'SZDLEB')))">
                            <xsl:text> | </xsl:text>
                            <xsl:value-of select="s:si"/>
                        </xsl:if>
                        <xsl:text> | </xsl:text>
                        <xsl:value-of select="$SZDID"/>
                    </a>
                </h4>
                    
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
                        <xsl:with-param name="SZDID" select="$SZDID"/>
                    </xsl:call-template>
            </div>
            <div class="card-body card-collapse collapse" id="{concat('c' , generate-id())}">
                <div class="table-responsive">
                    <table class="table table-sm">
                        <tbody>
                            <!-- https://glossa.uni-graz.at/o:szd.lebensdokumente/sdef:TEI/get?locale=de#SZDLEB.2 -->
                            <xsl:variable name="jumpURL" select="concat('/', $PID, '/sdef:TEI/get?locale=', $locale, '#', $SZDID)"/>
                            <a href="{$jumpURL}" class="font-weight-bold">
                                <xsl:choose>
                                    <xsl:when test="$locale = 'en'">
                                        <xsl:text>More information: catalogue view</xsl:text>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:text>Mehr Informationen: Katalogansicht</xsl:text>
                                    </xsl:otherwise>
                                </xsl:choose>
                                <xsl:text> </xsl:text>
                                <i class="fas fa-link"><xsl:text> </xsl:text></i>
                            </a>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- ///TITEL/// -->
                            <tr class="row">
                                <td class="col-3 text-truncate">
                                    <i18n:text>Titel</i18n:text>
                                </td>
                                <td class="col-9 font-italic">
                                    <xsl:value-of select="s:t"/>
                                    <!-- id="{substring-after(s:re/@uri, '#')} -->
                                    <!--<a href="{substring-after(s:re/@uri, 'gams.uni-graz.at')}" target="_blank">
                                        <xsl:attribute name="title">
                                            <xsl:choose>
                                                <xsl:when test="$locale = 'en'">
                                                    <xsl:text>To the general view in the catalogue</xsl:text>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:text>Zur Gesamtansicht in den Katalog</xsl:text>
                                                </xsl:otherwise>
                                            </xsl:choose> 
                                        </xsl:attribute>
                                        <xsl:value-of select="s:t"/>
                                    </a>-->
                                </td>
                            </tr>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- /// /// -->
                            <xsl:if test="s:co">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>description</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:co"/>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- ///SPRACHE/// -->
                            <!--<xsl:if test="s:i">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <xsl:text>Incipit</xsl:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:i"/>
                                    </td>
                                </tr>
                            </xsl:if>-->
                            <!-- ///Veröffentlichung/// -->
                            <xsl:if test="s:ps">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>publicationdetails</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:ps"/>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-- //REIHE/// -->	                                                                             
                            <!--<xsl:if test="s:se">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>series</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:se"/>
                                        <!-\- //UNTERREIHE// -\->
                                        <!-\-<xsl:if test="t:fileDesc/t:seriesStmt/t:title[@type='Unterreihe']">
                                            <xsl:text> / </xsl:text>
                                            <xsl:value-of select="t:fileDesc/t:seriesStmt/t:title[@type='Unterreihe']"/>
                                        </xsl:if>-\->
                                    </td>
                                </tr>
                            </xsl:if>-->
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- ///SPRACHE/// -->
                            <xsl:if test="s:la">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>language</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:call-template name="languageCode">
                                            <xsl:with-param name="Current" select="substring-after(s:la/@uri, 'iso639-2/')"/>
                                            <xsl:with-param name="locale" select="$locale"/>
                                        </xsl:call-template>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- ///UMFANG/// -->
                            <xsl:if test="s:ex">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>physicaldescription</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:ex"/>
                                    </td>
                                </tr>	                                        	 		
                            </xsl:if>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- //Originaltitel/// -->
                            <!--<xsl:if test="s:oti">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>originaltitle</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <span class="font-italic">
                                            <xsl:value-of select="s:oti"/>
                                        </span>
                                    </td>
                                </tr>
                            </xsl:if>-->
                            <!-- //////////////////////////////////////////////////////////// --> 
                            <!-- ///Provenienzkriterien/// -->
                            <xsl:if test="s:pc">
                                <tr class="row group">
                                    <td class="col-3 text-truncate">
                                        <xsl:choose>
                                            <xsl:when test="$locale = 'en'">
                                                <xsl:text>Provenance characteristics</xsl:text>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:text>Provenienzmerkmale</xsl:text>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </td>
                                    <!-- ///TABLE-LEFT/// -->
                                    <td class="col-9">
                                        <!--<xsl:value-of select="s:pc"/>-->
                                        <a href="{$jumpURL}" class="font-weight-bold">
                                            <xsl:choose>
                                                <xsl:when test="$locale = 'en'">
                                                    <xsl:text>More information: catalogue view</xsl:text>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:text>Mehr Informationen: Katalogansicht</xsl:text>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                            <xsl:text> </xsl:text>
                                            <i class="fas fa-link"><xsl:text> </xsl:text></i>
                                        </a>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- Hinweise -->
                           <!-- <xsl:if test="s:n">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>notes</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:n"/>                                        
                                    </td>
                                </tr>
                            </xsl:if>-->
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- Beilagen, bold -->
                            <!--<xsl:if test="s:en">
                                <tr class="group row">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>enclosures</i18n:text> 
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:en"/>                                            
                                    </td>
                                </tr>
                            </xsl:if>-->
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- Zusatzmaterial -->
                            <!--<xsl:if test="s:am">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <a>
                                            <i18n:text>additionalmaterial</i18n:text>
                                        </a>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:am"/>
                                    </td>
                                </tr>
                            </xsl:if>-->
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- ///Provenienz/// -->
                            <!--<xsl:if test="s:pr">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>provenance</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:pr"/>
                                    </td>
                                </tr>
                            </xsl:if>-->
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- //////Acquired = Ewerb -->
                            <!--<xsl:if test="s:ac">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>acquired</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:value-of select="s:ac"/>
                                    </td>
                                </tr>
                            </xsl:if>-->
                            <!-- //////////////////////////////////////////////////////////// -->
                            <!-- ///Standort/// -->
                                <tr class="row group">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>currentlocation</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:if test="s:lo">
                                            <xsl:call-template name="LocationSearch">
                                                <xsl:with-param name="locale" select="$locale"/>
                                                <xsl:with-param name="SZDSTA" select="substring-after(s:lo/@uri, '#')"/>
                                            </xsl:call-template>
                                            <xsl:if test="s:si">
                                                <br/>
                                                <xsl:value-of select="s:si"/>
                                            </xsl:if>
                                            <br/>
                                        </xsl:if>
                                        <a href="{s:re/@uri}">
                                            <xsl:value-of select="s:re/@uri"/>
                                        </a>
                                       
                                    </td>
                                </tr>
                            
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
    </xsl:template>
    
    <xsl:template name="printAuthor_Search">
        <xsl:param name="surname"/>
        <xsl:param name="forename"/>
            <xsl:value-of select="current-grouping-key()"/>
            <xsl:if test="$forename">
                <xsl:text>, </xsl:text>
                <xsl:value-of select="$forename"/>
            </xsl:if>
            <xsl:if test="not(position()=last())">
                <xsl:text> / </xsl:text>
            </xsl:if>
    </xsl:template>
    
    
    <!-- ///Verfasser/// -->
    <!--<xsl:if test="s:s">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>author_szd</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:for-each-group select="current-group()" group-by="s:s">
                                            <xsl:call-template name="printAuthor_Search">
                                                <xsl:with-param name="surname" select="current-grouping-key()"/>
                                                <xsl:with-param name="forename" select="s:f"/>
                                            </xsl:call-template>
                                        </xsl:for-each-group>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-\- //////////////////////////////////////////////////////////// -\->
                            <!-\- ///Composer/// -\->
                            <xsl:if test="s:sco">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <!-\- if object like "Haarlocke Goethes" than ... otherwise author-\->
                                        <i18n:text>composer</i18n:text>
                                    </td>
                                    <td class="col-9">
                                        <xsl:for-each-group select="current-group()" group-by="s:sco">
                                            <xsl:call-template name="printAuthor_Search">
                                                <xsl:with-param name="surname" select="current-grouping-key()"/>
                                                <xsl:with-param name="forename" select="s:fco"/>
                                            </xsl:call-template>
                                        </xsl:for-each-group>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-\- //////////////////////////////////////////////////////////// -\->
                            <!-\- ///Herausgeber/// -\->
                            <xsl:if test="s:sed">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <!-\- keeping language check because of the <br> -\->
                                        <xsl:choose>
                                            <xsl:when test="$locale = 'en'">
                                                <xsl:text>Editor or Compiler</xsl:text>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:text>Herausgeber/in</xsl:text><br></br><xsl:text>oder Bearbeiter/in</xsl:text>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </td>
                                    <td class="col-9">
                                        <xsl:for-each-group select="current-group()" group-by="s:sed">
                                             <xsl:call-template name="printAuthor_Search">
                                                 <xsl:with-param name="surname" select="current-grouping-key()"/>
                                                 <xsl:with-param name="forename" select="s:fed"/>
                                             </xsl:call-template>
                                        </xsl:for-each-group>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-\- //////////////////////////////////////////////////////////// -\->
                            <!-\- ///Betroffene Person/// -\->
                            <xsl:if test="s:sap">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>person_affected</i18n:text>                            
                                    </td>
                                    <td class="col-9">
                                        <xsl:for-each-group select="current-group()" group-by="s:sap">
                                            <xsl:call-template name="printAuthor_Search">
                                                <xsl:with-param name="surname" select="current-grouping-key()"/>
                                                <xsl:with-param name="forename" select="s:fap"/>
                                            </xsl:call-template>
                                        </xsl:for-each-group>
                                    </td>
                                </tr>
                            </xsl:if>
                            <!-\- //////////////////////////////////////////////////////////// -\->
                            <!-\- ///Beteilgite Person/// -\->
                            <xsl:if test="s:pi">
                                <tr class="row">
                                    <td class="col-3 text-truncate">
                                        <i18n:text>partiesinvolved</i18n:text>                            
                                    </td>
                                    <td class="col-9">
                                        <!-\- here its just the uri and names are extracted from SZDPER -\->
                                        <xsl:for-each-group select="current-group()" group-by="s:pi/@uri">
                                            <xsl:call-template name="GetPersonList">
                                                <xsl:with-param name="Person" select="substring-after(current-grouping-key(), '#')"/>
                                            </xsl:call-template>
                                            <xsl:if test="not(position()=last())">
                                                <xsl:text> / </xsl:text>
                                            </xsl:if>
                                        </xsl:for-each-group>
                                    </td>
                                </tr>
                            </xsl:if>-->


</xsl:stylesheet>
