<?xml version="1.0" encoding="UTF-8"?>


    <!-- 
    Project: Stefan zweig Digital
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
    Author: Christopher Pollin
    Last update: 2019
    Comment: This .xslt contains a couple of variables, xml and tempaltes which are used to in a 
             different other xslt. must be inluced like the szd-static.xsl
    -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:i18n="http://apache.org/cocoon/i18n/2.1"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    exclude-result-prefixes="#all"
    version="2.0">
    
    <!-- VARIABLES -->
    <!-- /////////////////////////////////////////////////////////// -->    
    <xsl:variable name="PersonList">
        <xsl:copy-of select="document('/o:szd.personen/TEI_SOURCE')"/>
    </xsl:variable>
    
	 <xsl:variable name="StandorteList">
        <xsl:copy-of select="document('/o:szd.standorte/TEI_SOURCE')"/>
    </xsl:variable>
    
    <!-- the following are needed for the THEMEN pages (Marie-Antoinette etc.) -->
	<xsl:variable name="BIBLIOTHEK">
		<xsl:copy-of select="document('/o:szd.bibliothek')"/>
	</xsl:variable>
	<xsl:variable name="MANUSKRIPTE">
        <xsl:copy-of select="document('/o:szd.werke/TEI_SOURCE')"/>
    </xsl:variable>
	<xsl:variable name="LEBENSDOKUMENTE">
        <xsl:copy-of select="document('/o:szd.lebensdokumente/TEI_SOURCE')"/>
    </xsl:variable>

    <!-- project-specific variables -->
    <xsl:variable name="server_template"></xsl:variable>
    <xsl:variable name="gamsdev_template">/gamsdev/pollin/szd/trunk/www</xsl:variable>
	
	
	<!-- ICONS: path to .png's  ================================================== -->
    <xsl:variable name="Icon_Path_template" select="concat($server_template, $gamsdev_template, '/icons/')"/>
	<xsl:variable name="Icon_bibliothek_template" select="concat($Icon_Path_template, 'biblothek.png')"/>
	<xsl:variable name="Icon_bilder_template" select="concat($Icon_Path_template, 'bilder.png')"/>
	<xsl:variable name="Icon_datenkorb_template" select="concat($Icon_Path_template, 'datenkorb.png')"/>
	<xsl:variable name="Icon_korrespodenzen_template" select="concat($Icon_Path_template, 'korrespodenzen.png')"/>
	<xsl:variable name="Icon_mail_template" select="concat($Icon_Path_template, 'mail.png')"/>
	<xsl:variable name="Icon_manuskript_template" select="concat($Icon_Path_template, 'manuskript.png')"/>
	<xsl:variable name="Icon_markieren_template" select="concat($Icon_Path_template, 'markieren.png')"/>
	<xsl:variable name="Icon_person_template" select="concat($Icon_Path_template, 'person.png')"/>
	<xsl:variable name="Icon_pfeil_template" select="concat($Icon_Path_template, 'pfeil.png')"/>
	<xsl:variable name="Icon_suche_template" select="concat($Icon_Path_template, 'suche.png')"/>
	<xsl:variable name="Icon_viewer_template" select="concat($Icon_Path_template, 'viewer.png')"/>
	<xsl:variable name="Icon_telefon_template" select="concat($Icon_Path_template, 'telefon.png')"/>
	<xsl:variable name="Icon_x_template" select="concat($Icon_Path_template, 'x.png')"/>
	<xsl:variable name="Icon_wiki_template" select="concat($Icon_Path_template, 'wiki.jpg')"/>
    
    
    <!-- ///TEI/// -->
<!--    <xsl:variable name="TEI_Body">
        <xsl:copy-of select="//t:body"/>
    </xsl:variable>-->
    
    <!-- ///TEI/// -->
  <!--  <xsl:variable name="Query_Result">
        <xsl:copy-of select="//s:results"/>
    </xsl:variable>-->
      
    <!-- ///LANGUAGE-XML/// -->
    <xsl:variable name="Languages">
        <xsl:copy-of select="document('/archive/objects/context:szd/datastreams/LANGUAGES/content')"/>
    </xsl:variable>

    <!-- ///ABC-Array/// -->
    <xsl:variable name="ABCarray" as="element()*">
        <Item>A</Item>
        <Item>B</Item>
        <Item>C</Item>
        <Item>D</Item>
        <Item>E</Item>
        <Item>F</Item>
        <Item>G</Item>
        <Item>H</Item>
        <Item>I</Item>
        <Item>J</Item>
        <Item>K</Item>
        <Item>L</Item>
        <Item>M</Item>
        <Item>N</Item>
        <Item>O</Item>
        <Item>P</Item>
        <Item>Q</Item>
        <Item>R</Item>
        <Item>S</Item>
        <Item>T</Item>
        <Item>U</Item>
        <Item>V</Item>
        <Item>W</Item>
        <Item>X</Item>
        <Item>Y</Item>
        <Item>Z</Item>
    	<Item>Ö</Item>
    </xsl:variable>
    
    <!-- END VARIABLES -->
    <!-- /////////////////////////////////////////////////////////// -->
    
    
	<!-- /////////////////////////////////////////////////////////// -->
    <!-- getStickyNavbar, TOP -->  
    <xsl:template name="getStickyNavbar">
        <xsl:param name="Category"/>
        <xsl:param name="Content"/>
        <xsl:param name="PID"/>
        <xsl:param name="locale"/>
        <xsl:param name="Title"/>
        <xsl:param name="GlossarRef"/>
        <!-- card-header  -->
        <article class="sticky-top header-card-nav d-none d-sm-block">     
           <div class="row">
               <div class="col-2">
                    <xsl:text> </xsl:text>
                </div>
                <!-- NAME -->
               <div class="col-8">    	
                   <h2 class="text-uppercase">
                        <xsl:value-of select="$Title"/>
                        <xsl:text> </xsl:text>
                       <!--  substring-after($PID, '.')) -->
                       <a href="{concat('/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=', $locale, '#', $GlossarRef)}" class="button" title="Glossary">
                           <xsl:choose>
                                <xsl:when test="$locale = 'en'">
                                    <xsl:attribute name="title" select="'About this collection'"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:attribute name="title" select="'Informationen zum Sammlungsbereich'"/>
                                </xsl:otherwise>
                            </xsl:choose>
                            <i class="fa fa-info-circle info_icon_header" aria-hidden="true"><xsl:text> </xsl:text></i>
                        </a>
                    </h2>  
                </div>
               <div class="col-2 text-right">
                   <xsl:choose>
                       <xsl:when test="contains($PID, 'szd.glossar')">
                           <a href="{concat('/',$PID,'/ONTOLOGY')}" role="button" target="_blank">
                               <img alt="RDF" height="25" id="rdf" src="/templates/img/RDF_icon.png" title="RDF"/>
                           </a>
                       </xsl:when>
                       <xsl:otherwise>
                           <a href="{concat('/',$PID,'/TEI_SOURCE')}" role="button" target="_blank">
                               <img alt="TEI" height="25" id="tei" src="/templates/img/tei_icon.jpg" title="TEI"/>
                           </a>
                           <xsl:text> </xsl:text>
                           <a href="{concat('/',$PID,'/RDF')}" role="button" target="_blank">
                               <img alt="RDF" height="25" id="rdf" src="/templates/img/RDF_icon.png" title="RDF"/>
                           </a>
                       </xsl:otherwise>
                   </xsl:choose>
                </div>
           </div>
            <!-- ///ABC-sorted Navigation of author (bibliothek) or categorylist (werke, lebensdokumente) //-->
            <ul class="list-inline text-center">
            <!-- GLOSSARY -->
            <xsl:choose>
                <xsl:when test="$PID = 'o:szd.glossar' ">
                    <xsl:for-each-group select="$Category" group-by=".">
                        <xsl:sort select="current-grouping-key()"/>
                        <xsl:variable name="currentRDFABOUT" select="../@rdf:about"/>
                        <div class="btn-group btn-group-sm">
                            <xsl:choose>
                                <xsl:when test="//skos:Concept[skos:broader/@rdf:resource = $currentRDFABOUT]">
                                    <button type="button" class="btn pl-1 bg-white dropdown-toggle dropdown-toggle-split" data-toggle="dropdown">
                                        <xsl:value-of select="current-grouping-key()"/> 
                                    </button>
                                    <div class="dropdown-menu scrollable-menu" role="menu">
                                        <xsl:for-each select="//skos:Concept[skos:broader/@rdf:resource = $currentRDFABOUT]">
                                            <button class="btn dropdown-item small" href="{concat('#',substring-after(@rdf:about, '#'))}" onclick="scrolldown(this)">
                                                <xsl:value-of select="skos:prefLabel[@xml:lang = $locale]"/>
                                            </button>
                                        </xsl:for-each>
                                    </div> 
                                </xsl:when>
                                <xsl:otherwise>
                                    <button  href="{concat('#',substring-after(../@rdf:about, '#'))}" class="btn pl-1" onclick="scrolldown(this)">
                                        <xsl:value-of select="current-grouping-key()"/> 
                                    </button>
                                </xsl:otherwise>
                            </xsl:choose>  
                        </div>
                    </xsl:for-each-group>
                 </xsl:when>
            <!-- ORDNUNGSKATEGORIEN for SZDMSK and SZDLEB -->
            <xsl:when test="$PID = 'o:szd.werke' or $PID = 'o:szd.lebensdokumente'">    
                <xsl:for-each-group select="$Category" group-by=".">
                    <xsl:sort select="."/>
                    <div class="btn-group btn-group-sm">
                        <!-- dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" href="{concat('#mt',generate-id())}"-->
                        <button type="button" class="btn btn-sm bg-white" href="{concat('#',current-grouping-key())}" onclick="scrolldown(this)">
                            <xsl:value-of select="current-grouping-key()"/>
                           <!-- <span class="caret"><xsl:text> </xsl:text></span>-->
                        </button>
                        <!--<div class="dropdown-menu scrollable-menu" role="menu">
                            <xsl:for-each-group select="current-group()/ancestor::t:biblFull[1]" group-by="t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel']">
                                <xsl:sort select="."/>
                                <a class="dropdown-item small" href="{concat('#mt',generate-id())}" onclick="scrolldown(this)">
                                    <xsl:choose>
                                        <xsl:when test="$locale = 'en'">
                                            <xsl:choose>
                                                <xsl:when test="t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel'][@xml:lang = 'en']">
                                                    <xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel'][@xml:lang = 'en']"/>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel']"/>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:choose>
                                                <xsl:when test="t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel'][@xml:lang = 'de']">
                                                    <xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel'][@xml:lang = 'de']"/>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel']"/>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </a>
                            </xsl:for-each-group>
                        </div>-->
                    </div>
                </xsl:for-each-group>
                   <!-- <xsl:for-each-group select="$Category" group-by=".">
                            <xsl:sort select="."/>
                             <li class="list-inline-item small">
                                <a onclick="scrolldown(this)">
                                    <!-\- glossar href can come from different pages, just use the @rdf:about in the SKOS for it -\->
                                    <xsl:choose>
                                        <xsl:when test="$PID = 'o:szd.glossar'">
                                            <xsl:attribute name="href" select="concat('#',substring-after(../@rdf:about, '#'))"/>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:attribute name="href" select="concat('#',translate(current-grouping-key(), ' ', ''))"/>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                    <xsl:choose>
                                        <xsl:when test="$locale = 'en'">
                                            <xsl:attribute name="title" select="concat('Go to ', .)"/>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:attribute name="title" select="concat('Springe zu ', .)"/>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                    <xsl:value-of select="."/>
                                </a>
                             </li>
                        </xsl:for-each-group>-->
                </xsl:when>
                <!-- /////////////////////////////// -->
                <!-- navbar years for lebenskalender -->
                <xsl:when test="$PID = 'o:szd.lebenskalender'">
                    <xsl:for-each-group select="//t:listEvent/t:event" group-by="t:head/t:span[1]/t:date/substring(@when | @from, 1, 4)">
                        <xsl:if test="position() = 1">
                            <button type="button" class="btn btn-sm pr-0" href="{concat('#',@xml:id)}" onclick="scrolldown(this)">
                                <xsl:value-of select="current-grouping-key()"/>
                            </button>
                        </xsl:if>
                        <xsl:if test="position() mod 2 = 0">
                            <button type="button" class="btn btn-sm pr-0" href="{concat('#',@xml:id)}" onclick="scrolldown(this)">
                              <xsl:value-of select="current-grouping-key()"/>
                          </button>
                        </xsl:if>
                        <!--<div class="btn-group">
                            <button type="button" class="btn bg-white dropdown-toggle dropdown-toggle-split" data-toggle="dropdown">
                                <xsl:value-of select="concat(current-grouping-key(), 0)"/>
                                <span class="caret"><xsl:text> </xsl:text></span>
                            </button>
                            <div class="dropdown-menu scrollable-menu" role="menu">
                                <xsl:for-each select="current-group()">
                                    <!-\- @style for making it scrollable. i really dont want to make a new class for it  ;) -\->
                                    <a class="dropdown-item small text-uppercase" href="{concat('#',@xml:id)}" onclick="scrolldown(this)">
                                        <xsl:choose>
                                            <xsl:when test="$locale = 'en'">
                                                <xsl:value-of select="t:head/t:span[@xml:lang = 'en']"/>
                                                <xsl:text> </xsl:text>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:value-of select="t:head/t:span[@xml:lang = 'de']"/>
                                                <xsl:text> </xsl:text>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </a>
                                </xsl:for-each>
                            </div>
                        </div> -->
                    </xsl:for-each-group>
                </xsl:when>
                <!-- /////////////////////////////// -->
                <xsl:when test="$PID = 'o:szd.publikation'">
                    <div class="btn-group">
                    <xsl:for-each-group select="//t:date" group-by="substring(@when, 1, 3)">
                    <div class="dropdown">
                         <button type="button" class="btn bg-white">
                             <xsl:value-of select="concat(current-grouping-key(), '0')"/>
                             <span class="caret"><xsl:text> </xsl:text></span>
                         </button>
                        <div class="dropdown-menu">
                            <xsl:for-each-group select="current-group()" group-by="@when">
                                <a class="dropdown-item" href="{concat('#year_', current-grouping-key())}" onclick="scrolldown(this)">
                                    <xsl:value-of select="@when"/>
                                </a>
                            </xsl:for-each-group>
                        </div>
                    </div>
                    </xsl:for-each-group>
                    </div>
                </xsl:when>
             <xsl:otherwise>
             <!-- creates ABC-Navbar in Bibliothek and Personen -->
                 <xsl:for-each select="$ABCarray">
                     <xsl:variable name="current" select="string(.)"/>
                     <xsl:if test="$Content[substring(., 1, 1) = $current]">
                        <!-- <li class=" small">-->
                         <button type="button" class="btn btn-sm list-inline-item" href="{concat('#',.)}" onclick="scrolldown(this)">
                              <xsl:attribute name="title"></xsl:attribute>
                              <xsl:choose>
                                  <xsl:when test="$locale = 'en'">
                                      <xsl:attribute name="title" select="concat('Jump to first entry beginning with ', .)"/>
                                  </xsl:when>
                                  <xsl:otherwise>
                                      <xsl:attribute name="title" select="concat('Springe zum ersten Eintrag beginnend mit ', .)"/>
                                  </xsl:otherwise>
                              </xsl:choose>
                              <xsl:value-of select="."/>
                          </button>
                         <!--</li>-->
                     </xsl:if>
                    <!-- <xsl:if test="">-->
                     <!--</xsl:if>-->
                 </xsl:for-each>
                 <xsl:if test="not($PID = 'o:szd.personen') and not($PID = 'o:szd.autographen')">
                    <button type="button" class="btn btn-sm list-inline-item" href="#withoutAuthor" onclick="scrolldown(this)">
                        <xsl:text>o.V.</xsl:text>
                    </button>
                 </xsl:if>
             </xsl:otherwise>
            </xsl:choose>
         </ul>
      </article>
    </xsl:template>  
      
    <!-- /////////////////////////////////////////////////////////// --> 
    <!-- ///LANGUAGES/// -->
    <!-- called when iso-lanuage is found in TEI, checks with $Languages, which is a simple .xml. datastream in context:szd -->
    <!--<xsl:template name="languageCode">
        <xsl:variable name="Current" select="."/>	
        <xsl:for-each select="$Languages//*:entry">
            <!-\- comparing string, iso-code -\->
            <xsl:if test="*:code[@type = 'ISO639-2'] = $Current">
                <xsl:value-of select="*:language[@type = 'german']"/>
                <!-\- <xsl:value-of select="*:language[@type = 'english']"/>-\->
            </xsl:if>
        </xsl:for-each>
    </xsl:template>-->
    
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- ///AUTOCOMPLETE/// -->
    <!--<xsl:template name="AutoComplete">
        <!-\- used for Ordnungskategorien in szd-Manuskripte -\->
        <xsl:param name="Content"/>
        <xsl:param name="PID"/>
        <!-\- https://jqueryui.com/autocomplete -\->
        <!-\- Autocomplete of all author @role='Verfasser', filling the available Tags  -\->
        <!-\- defining a list of values items as availableTags, #author_tags is to address <form>, <input> select: 
            here is the jquery part where you can select the input-data -\->
        <xsl:variable name="apos"><xsl:text>'</xsl:text></xsl:variable>
        <xsl:variable name="apos2"><xsl:text>"</xsl:text></xsl:variable>
        <script type="text/javascript">
            $( function() 
            {
            var availableTags = [
            <xsl:for-each-group select="$Content" group-by=".">
                <xsl:if test="not(. = '')">
                {
                value: "<xsl:value-of select="normalize-space(replace(., $apos2, $apos))"/>",
                    <xsl:choose>
                        <xsl:when test="$PID = 'o:szd.werke'">
                            <xsl:variable name="SZDMSK">
                                <xsl:value-of select="ancestor::t:biblFull/@xml:id"/>
                            </xsl:variable>
                            id: "<xsl:value-of select="$SZDMSK"/>"
                        </xsl:when>
                       <!-\- <xsl:when test="$PID = 'o:szd.publikation'">
                            <xsl:variable name="SZDMSK">
                                <xsl:value-of select="parent::t:bibl/@xml:id"/>
                            </xsl:variable>
                            id: "<xsl:value-of select="$SZDMSK"/>"
                        </xsl:when>-\->
                        <xsl:when test="$PID = 'o:szd.autographen'">
                            <xsl:variable name="SZDPER">
                                <xsl:call-template name="GetPersonList">
                                    <xsl:with-param name="Person" select="./@ref"/>
                                </xsl:call-template>
                            </xsl:variable>
                            <xsl:variable name="SZDMSK">
                                <xsl:value-of select="parent::t:bibl/@xml:id"/>
                            </xsl:variable>
                            id: "<xsl:value-of select="$SZDPER"/>"
                        </xsl:when>
                        <xsl:when test="$PID = 'o:szd.personen'">
                            id: "<xsl:value-of select="substring-after(../s:szdperson/@uri, '#')"/>"
                        </xsl:when>
                        <xsl:when test="$PID = 'o:szd.orte'">
                            id: "<xsl:value-of select="substring-after(../s:szdplace/@uri, '#')"/>"
                        </xsl:when>
                        <xsl:when test="$PID = 'o:szd.organisation'">
                            id: "<xsl:value-of select="substring-after(../s:szdorg/@uri, '#')"/>"
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:variable name="SZDPER">
                                <xsl:call-template name="GetPersonList">
                                    <xsl:with-param name="Person" select="./@ref"/>
                                </xsl:call-template>
                            </xsl:variable>
                            id: "<xsl:value-of select="$SZDPER"/>"
                        </xsl:otherwise>
                    </xsl:choose>
                },
                </xsl:if>
            </xsl:for-each-group>
            ];
            $( "#author_tags" ).autocomplete({
            minLength: 0,
            source: availableTags,
            select: function( event, ui ) 
            {
            window.location.href = "#" + ui.item.id;
            window.scrollBy(0, -250)
            return false;
            }
            })
            });
        </script>
        <xsl:variable name="teiname" select="upper-case(substring-after($PID, '.'))"/>
        <form class="navbar-form navbar-left" id="autocomplete_szd">
            <div class="form-control">
                <xsl:variable name="Description">
                    <xsl:choose>
                        <xsl:when test="$teiname = 'BIBLIOTHEK' or $teiname = 'AUTOGRAPHEN'">
                            <xsl:value-of select="'PERSONENSUCHE'"/>
                        </xsl:when>
                        <xsl:when test="$teiname = 'WERKE' or $teiname = 'LEBENSDOKUMENTE' or $teiname = 'KORRESPODENZEN'">
                            <xsl:value-of select="'TITELSUCHE'"/>
                        </xsl:when>
                        <xsl:otherwise><xsl:value-of select="$teiname"/></xsl:otherwise>
                    </xsl:choose>
                </xsl:variable>
                <input id="author_tags" placeholder="{$Description}"/>
            </div>
            <button id="searchbutton" class="btn btn-default icon_suche">
                <img src="{$Icon_suche_template}"  class="img-responsive" alt="Volltextsuche" />
            </button>  
        </form>
    </xsl:template>-->
    
    
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- ///FILTER INTERFACE/// -->
    <!-- called from szd-Suche, when search results are shown and when get?mode=advancedSearch is called -->
    <xsl:template name="filter">
        <xsl:param name="Filter_search"/>
        <div class="all_search">
            <h2>FILTER</h2>
            <form id="SucheErweitert" class="form-check">
                <!-- all Person-data is included
                 CP: 12.10: check if this is needed-->
                <!-- <xsl:variable name="Personen">
                    <xsl:copy-of select="document('/o:szd.personen/TEI_SOURCE')"></xsl:copy-of>
                </xsl:variable>-->

                <div class="form-group" id="filterSelect">
                    <div class="radio">
                        <label class="text-uppercase small">
                            <input class="mr-1" type="radio" name="optradio"  id="all_radio" value="all_search" onchange="filter(this)"/>
                            <i18n:text>all</i18n:text>
                        </label>
                    </div>
                    <xsl:if test="contains($Filter_search, 'o:szd.autographen')">
                        <div class="radio">
                            <label class="text-uppercase small">
                                <input class="mr-1" type="radio" name="optradio" id="autograph_radio" value="autographen_search" onchange="filter(this)"/>
                                <i18n:text>autograph</i18n:text>
                            </label>
                        </div>
                    </xsl:if>
                    <xsl:if test="contains($Filter_search, 'o:szd.bibliothek')">
                        <div class="radio">
                            <label class="text-uppercase small">
                                <input class="mr-1" type="radio" name="optradio" id="bibliothek_radio" value="bibliothek_search" onchange="filter(this)"/>
                                <i18n:text>library_szd</i18n:text>
                            </label>
                        </div>
                    </xsl:if>
                    <xsl:if test="contains($Filter_search, 'o:szd.lebenskalender')">
                        <div class="radio">
                            <label class="text-uppercase small">
                                <input class="mr-1" type="radio" name="optradio" id="biography_radio" value="biography_search" onchange="filter(this)"/>
                                <i18n:text>biography</i18n:text>
                            </label>
                        </div>
                    </xsl:if>
                    <xsl:if test="contains($Filter_search, 'o:szd.lebensdokumente')">
                        <div class="radio">
                            <label class="text-uppercase small">
                                <input class="mr-1" type="radio" name="optradio" id="lebensdokumente_radio" value="lebensdokumente_search" onchange="filter(this)"/>
                                <i18n:text>personaldocument</i18n:text>
                            </label>
                        </div>
                    </xsl:if>
                    
                    <xsl:if test="contains($Filter_search, 'o:szd.personen')">
                        <div class="radio">
                            <label class="text-uppercase small">
                                <input class="mr-1" type="radio" name="optradio" id="person_radio" value="person_search" onchange="filter(this)"/>
                                <i18n:text>Persons</i18n:text>
                            </label>
                        </div>
                    </xsl:if>
                    <xsl:if test="contains($Filter_search, 'o:szd.werke')">
                        <div class="radio">
                            <label class="text-uppercase small">
                                <input class="mr-1" type="radio" name="optradio" id="werke_radio" value="werke_search" onchange="filter(this)"/>
                                <i18n:text>work</i18n:text>
                            </label>
                        </div>
                    </xsl:if>

                    <!--<div class="radio">
                        <label><input type="radio" name="optradio"  id="autographen_radio" value="autographen_search" onchange="filter(this)"/>Autographen</label>
                    </div>-->
                    <!--<div class="radio">
                        <label><input type="radio" name="optradio" id="orte_radio" value="orte_search" onchange="filter(this)"/>Standorte</label>
                    </div>-->
                    <!--<div class="radio">
                        <label><input type="radio" name="optradio" id="organisation_radio"  value="organisation_search" onchange="filter(this)"/>Organisationen</label>
                    </div>-->
                    <!--<div class="radio">
                        <label><input type="radio" name="optradio" id="personen_radio" value="personen_search" onchange="filter(this)"/>Personen</label>
                    </div>-->
                </div>
                
                <!-- select id trhough option select and hide the div with this id, use toogle for show/hide -->
                <script>
                    //goes through all collections, hides all others, shows pressed one.
                   function filter(id) 
                    {
                        
                        current = document.getElementById(id.value);
                                                        console.log(current);
                     
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
                <!-- <div class="form-group">
                    <label for="pricefrom" class="control-label">Zeitbereich</label>
                    <div class="input-group">
                        <div class="input-group-addon">vor</div>
                        <input name="$1" type="text" class="form-control" id="search_before" aria-describedby="basic-addon1"/>
                        <div class="input-group-addon">nach</div>
                        <input name="$2" type="text" class="form-control" id="search_after" aria-describedby="basic-addon1"/>
                    </div>
                </div>
               <button type="submit" class="btn btn-default icon_suche">
                    <img src="{$Icon_suche}"  class="img-responsive" alt="ErweiterteSuche"/>
                </button>-->
            </form>
</div>
    </xsl:template>
    
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- ///ADDDATA-DATABASKET -->
    <!-- Add the data- attributs, used for the databasket: Author or Editor, title and date -->
    <xsl:template name="AddData-Databasket">
        <xsl:attribute name="data-check">
            <xsl:text>unchecked</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="data-uri">
            <xsl:value-of select="normalize-space(concat('/', //t:publicationStmt/t:idno[@type='PID'], '#', @xml:id))"/>
        </xsl:attribute>
        <!-- AUTHOR -->
        <xsl:choose>
            <xsl:when test="t:fileDesc/t:titleStmt/t:author[1]">
                <xsl:attribute name="data-author">
                    <xsl:call-template name="printAuthor">
                        <xsl:with-param name="currentAuthor" select=".//t:titleStmt/t:author[1]"/>
                    </xsl:call-template>
                </xsl:attribute>
            </xsl:when>
           <xsl:otherwise/>
        </xsl:choose>
        <!-- all other involved persons -->
        <xsl:if test="t:fileDesc/t:titleStmt/t:editor[not(@role)][1] or t:fileDesc/t:titleStmt/t:author[@role] or t:profileDesc/t:textClass/t:keywords/t:term[@type='person'] or t:profileDesc/t:textClass/t:keywords/t:term[@type='person_affected']">
            <xsl:attribute name="data-involved">
                <xsl:for-each select="t:fileDesc/t:titleStmt/t:editor | t:fileDesc/t:titleStmt/t:author[@role] | t:profileDesc/t:textClass/t:keywords/t:term[@type='person'] | t:profileDesc/t:textClass/t:keywords/t:term[@type='person_affected']">
                    <xsl:call-template name="printAuthor">
                        <xsl:with-param name="currentAuthor" select="."/>
                    </xsl:call-template>
                    <xsl:if test="not(position()=last())">
                        <xsl:text> / </xsl:text>
                    </xsl:if>
                </xsl:for-each>
            </xsl:attribute>
        </xsl:if>
        <!-- TITEL -->
        <xsl:if test="t:fileDesc/t:titleStmt/t:title">
            <xsl:attribute name="data-title">
                <xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[1])"/>
            </xsl:attribute>
        </xsl:if>
        <!-- DATUM -->
        <xsl:choose>
            <xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:origin/t:origDate">
                <xsl:attribute name="data-date">
                    <xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:origin/t:origDate)"/>
                </xsl:attribute>
            </xsl:when>
            <xsl:when test="t:fileDesc/t:publicationStmt/t:date">
                <xsl:attribute name="data-date">
                    <xsl:value-of select="normalize-space(t:fileDesc/t:publicationStmt/t:date)"/>
                </xsl:attribute>
            </xsl:when>
            <xsl:otherwise/>
        </xsl:choose>
    </xsl:template>
    
    <!-- /////////////////////////////////////////////////////////// -->
	<!-- ///GETPERSONLIST/// -->    
    <xsl:template name="GetPersonList">
        <xsl:param name="Person"/>
        <xsl:for-each select="$Person">
         <xsl:choose>
             <xsl:when test="contains(., 'SZDPER.')">
                     <xsl:variable name="String" select="string(.)"/>
                     <xsl:variable name="SZDPER" select="$PersonList//t:person[@xml:id = $String]/t:persName"/>
                     <xsl:value-of select="$SZDPER/t:surname|$SZDPER/t:name"/>
                     <xsl:if test="$SZDPER/t:forename">
                         <xsl:text>, </xsl:text>
                         <xsl:value-of select="$SZDPER/t:forename"/>
                     </xsl:if>
             </xsl:when>
             <xsl:otherwise>
                     <xsl:variable name="SZDPER" select="string(.)"/>
                     <xsl:value-of select="$PersonList//t:person[t:persName[contains(@ref, $SZDPER)]]/@xml:id"/>
             </xsl:otherwise>
         </xsl:choose>
        </xsl:for-each>
    </xsl:template>
	
	<!-- /////////////////////////////////////////////////////////// -->
    <!-- ///GetStandorteList/// --> 
    <!-- if input is a GND-ID it returns a SZDPER, and if input a SZDPER is a GND-ID -->
	<xsl:template name="GetStandortList">
		<xsl:param name="Standort"/>
	    <xsl:choose>
	        <xsl:when test="contains($Standort, 'SZDSTA.')">
	            <xsl:for-each select="$Standort">
	                <xsl:variable name="String" select="string(.)"/>
	                <xsl:variable name="SZDSTA" select="$StandorteList//t:org[@xml:id = $String]"/>
	                <xsl:value-of select="$SZDSTA/t:orgName"/>
	                <xsl:if test="$SZDSTA/t:settlement">
	                    <xsl:text>, </xsl:text>
	                    <xsl:value-of select="$SZDSTA/t:settlement"/>
	                </xsl:if>
	            </xsl:for-each>
	        </xsl:when>
	        <xsl:otherwise>
	            <xsl:for-each select="$Standort">
	                <xsl:variable name="String" select="string(.)"/>
	                <xsl:variable name="SZDSTA" select="$StandorteList//t:org[t:orgName[@ref = $String]]/@xml:id"/>
	                <!-- check if there is a GND-Ref, otherwise all empty gnd would be listed -->
	                <xsl:if test="substring-after($String, 'http://d-nb.info/gnd/')">
	                    <xsl:value-of select="$SZDSTA"/>
	                </xsl:if>
	            </xsl:for-each>
	        </xsl:otherwise>
	    </xsl:choose>
	    
	</xsl:template>
	
	
	<!-- /////////////////////////////////////////////////////////// -->
    <!-- ///getNavbar/// -->
	<!-- Creates header of Collection, Biographie, Glossar, etc. -->
	<xsl:template name="getNavbar">
		<xsl:param name="Title"/>
		<xsl:param name="PID"/>
	    <xsl:param name="mode"/>
	        <!-- tei, rdf button -->
	    <div class="row mt-5">
	            <!-- creates language button DE | EN in the header -->
            <div class="col-2">
                <xsl:text> </xsl:text>
            </div>
	            <div class="col-8">
	            	<xsl:choose>
	            	    <xsl:when test="contains($PID, 'o:szd.thema')">
	            	        <img src="{concat('/', $PID, '/TITELBILD')}" class="img-responsive center-block" alt="Titelbild" width="400" height="400"/> 
	            	    </xsl:when>
	            		<xsl:otherwise>
	            		<h2>
	                		<xsl:value-of select="upper-case($Title)"/>
	            		    <xsl:if test="not(contains($PID, 'o:szd.glossar'))">
      	            		    <xsl:text> </xsl:text>
	            		        <a href="{concat('/o:szd.glossar#', lower-case($Title))}" class="button" title="Hier erhalten Sie mehr Information zum Sammlungsbereich">
	            		            <!-- style="color:#C2A360; font-size: 50%;" -->
	            		            <span class="glyphicon glyphicon-info-sign" ><xsl:text> </xsl:text></span>
      	            		    </a>
	            		    </xsl:if>
	                	</h2>
	            		</xsl:otherwise>
	            	</xsl:choose>
	            </div>
	            <!-- creates TEI and/or RDF BUtton on the right side in the header -->
	            <div class="btn-group col-2">
	                <xsl:if test="$PID">
	                    <div class="float-right">
	                        <xsl:choose>
	                            <!-- this skips TEI and RDF button -->
           	                    <xsl:when test="$PID = 'context:szd'"/>
           	                    <xsl:when test="contains($PID, 'o:szd.glossar') or contains($PID, 'o:szd.ontology')">
           	                        <a class="button" href="{concat('/', $PID,'/ONTOLOGY')}" role="button" target="_blank">
           	                            <img alt="RDF" height="25" id="rdf" src="/templates/img/RDF_icon.png" title="RDF"/>
           	                        </a>
           	                    </xsl:when>
	                            <!-- TEI RDF Button in Search Result -->
	                            <xsl:when test="$PID ='search'">
	                               <xsl:text> </xsl:text>
	                            </xsl:when>
           	                    <xsl:otherwise>
           	                        <a class="button" href="{concat('/',$PID,'/TEI_SOURCE')}" role="button" target="_blank">
           	                            <img alt="TEI" height="25" id="tei" src="/templates/img/tei_icon.jpg" title="TEI"/>
           	                        </a>
           	                        <xsl:text> </xsl:text>
           	                        <a class="button" href="{concat('/',$PID,'/RDF')}" role="button" target="_blank">
           	                            <img alt="RDF" height="25" id="rdf" src="/templates/img/RDF_icon.png" title="RDF"/>
           	                        </a>
           	                    </xsl:otherwise>
    	                   </xsl:choose>
	                    </div>
	                </xsl:if>
	                <xsl:text> </xsl:text>
	            </div>
	        </div>    	
	</xsl:template>
	
	<!-- /////////////////////////////////////////////////////////// -->
    <!-- SZDBIB -->
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- creates metadata representation of eyer biblFull in SZDBIB  -->
	<xsl:template name="FillbiblFull_SZDBIB">
	    <xsl:param name="locale"/>
	    <xsl:param name="type"/>
         <!-- ///START CREATING TABLE FOR EACH BIBLFULL -->
         <!--   for each child: <titleStmt>,<seriesStmt>, <editionStmt>, <publicationStmt>, <publicationStmt>, <sourceDesc>
               structure the data in a table based on the TEI-structure.-->
         <div class="table-responsive">	    
             <table class="table table-sm">
                <tbody>
                 <!-- //////////////////////////////////////////////////////////// -->
                 <!-- PERSON -->
    			 <!-- ///Verfasser/// -->
                 <xsl:if test="t:fileDesc/t:titleStmt/t:author[1]">
                 <tr class="row">
                       <td class="col-3">
                           <i18n:text>author_szd</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:fileDesc/t:titleStmt/t:author[not(@type)]">
                                <xsl:call-template name="PersonSearch">
                                    <xsl:with-param name="locale" select="$locale"/>
                                </xsl:call-template>
                              <!-- <xsl:if test="not(position() = last())">
                                   <xsl:text> / </xsl:text>
                               </xsl:if>-->
                           </xsl:for-each>
                        </td>
                    </tr>
                 </xsl:if>
                 <!-- //////////////////////////////////////////////////////////// -->
                 <!-- ///Komponist/// -->
                <xsl:if test="t:fileDesc/t:titleStmt/t:author[@role='composer']">
                     <tr class="row">
                       <td class="col-3">
                           <i18n:text>composer</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:fileDesc/t:titleStmt/t:author[@role='composer']">
                            	<xsl:call-template name="PersonSearch"/>
                            </xsl:for-each>
                        </td>
                    </tr>
                 </xsl:if>
                 <!-- //////////////////////////////////////////////////////////// -->
                 <!-- ///Herausgeber/// -->
                 <xsl:if test="t:fileDesc/t:titleStmt/t:editor[not(@role)]">
                    <tr class="row">
                        <td class="col-3">
                           <!-- keeping language check because of the <br> -->
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
                            <xsl:for-each select="t:fileDesc/t:titleStmt/t:editor[not(@role)]">
                            	<xsl:call-template name="PersonSearch">
                            	    <xsl:with-param name="locale"/>
                            	</xsl:call-template>
                            </xsl:for-each>
                        </td>
                    </tr>
                  </xsl:if>
                  <!-- //////////////////////////////////////////////////////////// -->
                  <!-- ///Illustrator/// -->
                  <xsl:if test="t:fileDesc/t:titleStmt/t:editor[@role='illustrator']">
                     <tr class="row">
                        <td class="col-3">
                            <i18n:text>illustrator</i18n:text>
                         </td>
                         <td class="col-9">
                             <xsl:for-each select="t:fileDesc/t:titleStmt/t:editor[@role='illustrator']">
                                 <xsl:call-template name="PersonSearch">
                                     <xsl:with-param name="locale"/>
                                 </xsl:call-template>
                             </xsl:for-each>
                         </td>
                     </tr>
                  </xsl:if>
                  <!-- //////////////////////////////////////////////////////////// -->
                  <!-- ///Übersetzer/// -->
                  <xsl:if test="t:fileDesc/t:titleStmt/t:editor[@role='translator']">
                     <tr class="row">
                       <td class="col-3">
                           <i18n:text>translator</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:fileDesc/t:titleStmt/t:editor[@role='translator']">
                                <xsl:call-template name="PersonSearch">
                                    <xsl:with-param name="locale"/>
                                </xsl:call-template>
                            </xsl:for-each>
                        </td>
                    </tr>
                 </xsl:if>
                 <!-- //////////////////////////////////////////////////////////// -->
                 <!-- ///Verfasser Vorwort/// -->
                 <xsl:if test="t:fileDesc/t:titleStmt/t:author[@role='preface']">
                     <tr class="row">
                       <td class="col-3">
                           <i18n:text>writerpreface</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:fileDesc/t:titleStmt/t:author[@role='preface']">
                                <xsl:call-template name="PersonSearch">
                                    <xsl:with-param name="locale"/>
                                </xsl:call-template>
                            </xsl:for-each>
                        </td>
                    </tr>
                 </xsl:if>
                 <!-- //////////////////////////////////////////////////////////// -->
                 <!-- ///Verfasser Nachwort/// -->
                 <xsl:if test="t:fileDesc/t:titleStmt/t:author[@role='afterword']">
                     <tr class="row">
                       <td class="col-3">
                           <i18n:text>writerafterword</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:fileDesc/t:titleStmt/t:author[@role='afterword']">
                                <xsl:call-template name="PersonSearch">
                                    <xsl:with-param name="locale"/>
                                </xsl:call-template>
                            </xsl:for-each>
                        </td>
                    </tr>
                 </xsl:if>
                 <!-- //////////////////////////////////////////////////////////// -->
                 <!-- END PERSON -->
                 
    			 <!-- //////////////////////////////////////////////////////////// -->
                 <!-- ///TITEL/// -->
                <xsl:if test="t:fileDesc/t:titleStmt/t:title[1]">
                     <tr class="row">
                       <td class="col-3">
                           <i18n:text>Titel</i18n:text>
                        </td>
                        <td class="col-9">
                            <span class="font-italic">
                                <xsl:choose>
                                    <!-- if its o:szd.publikation than add a search-query-url -->
                                    <xsl:when test="$type = 'o:szd.publikation'">
                                        <xsl:choose>
                                            <xsl:when test="$locale = 'en'">
                                                <xsl:for-each select="t:fileDesc/t:titleStmt/t:title[@xml:lang = $locale]">
                                                    <xsl:call-template name="WorkSearch"/>
                                                </xsl:for-each>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:for-each select="t:fileDesc/t:titleStmt/t:title">
                                                    <xsl:call-template name="WorkSearch"/>
                                                </xsl:for-each>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </xsl:when>
                                    <!-- in o:szd.bibliothek -->
                                    <xsl:otherwise>
                                        <xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[1])"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </span>
                        </td>
                    </tr>
                </xsl:if>
                <!-- //////////////////////////////////////////////////////////// -->
                <!-- //GESAMTTITEL/// -->
                <xsl:if test="t:fileDesc/t:titleStmt/t:title[@type='series']">
                         <tr class="row">
                           <td class="col-3">
                               <i18n:text>seriestitle</i18n:text>
                            </td>
                            <td class="col-9">
                                <xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@type='series']"/>
                            </td>
                        </tr>
                     </xsl:if>
                     <!-- //////////////////////////////////////////////////////////// -->
                     <!-- ///PUBLICATIONSTMT/// -->
                     <!-- ///Veröffentlichung/// -->
                     <tr class="row">
                        <td class="col-3">
                            <i18n:text>publicationdetails</i18n:text>
                         </td>
                         <td class="col-9">
                             <xsl:if test="t:fileDesc/t:editionStmt/t:edition">
                                 <xsl:value-of select="t:fileDesc/t:editionStmt/t:edition"/>
                                 <xsl:text> . – </xsl:text>
                             </xsl:if>
                             <xsl:value-of select="t:fileDesc/t:publicationStmt/t:pubPlace"/><xsl:text> : </xsl:text>
                             <xsl:value-of select="t:fileDesc/t:publicationStmt/t:publisher"/>
                             <xsl:text>, </xsl:text>
                             <xsl:value-of select="t:fileDesc/t:publicationStmt/t:date"/>
                         </td>
                     </tr>
                    <!-- //////////////////////////////////////////////////////////// -->
                    <!-- ///REIHENANGABE/// -->
                    <!-- //REIHE/// -->	                                                                             
                    <xsl:if test="t:fileDesc/t:seriesStmt/t:title[1]">
                             <tr class="row">
    	                       <td class="col-3">
    	                           <i18n:text>series</i18n:text>
    	                        </td>
    	                        <td class="col-9">
    	                            <xsl:value-of select="t:fileDesc/t:seriesStmt/t:title[1]"/>
    	                        	<!-- //UNTERREIHE// -->
    	                            <xsl:if test="t:fileDesc/t:seriesStmt/t:title[@type='Unterreihe']">
    	                        		<xsl:text> / </xsl:text>
    	                                <xsl:value-of select="t:fileDesc/t:seriesStmt/t:title[@type='Unterreihe']"/>
    	                        	</xsl:if>
    	                        </td>
    	                    </tr>
                         </xsl:if>
                     <!-- //////////////////////////////////////////////////////////// -->
                     <!-- ///SOURCEDESC/// -->
                     <!-- ///Sprache/// -->
    			     <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang/t:lang">
                         <tr class="row">
                           <td class="col-3">
                               <i18n:text>language</i18n:text>
                            </td>
                            <td class="col-9">
                                <xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang/t:lang">
                               	<xsl:choose>
                               		<xsl:when test="position() = last()">
                               		 	<xsl:call-template name="languageCode">
                               		 	    <xsl:with-param name="Current" select="@xml:lang"/>
                               		 	    <xsl:with-param name="locale" select="$locale"/>
                               		 	</xsl:call-template>
                               		</xsl:when>
                               		<xsl:otherwise>
                               			<xsl:call-template name="languageCode">
                               			    <xsl:with-param name="Current" select="@xml:lang"/>
                               			    <xsl:with-param name="locale" select="$locale"/>
                               			</xsl:call-template>
                               		</xsl:otherwise>
                               	</xsl:choose>
                           </xsl:for-each>
                        </td>
                        </tr>
                     </xsl:if>
    			 	  <!-- //////////////////////////////////////////////////////////// -->
                      <!-- ///UMFANG/// -->
    			     <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc">
                         <tr class="row">
                           <td class="col-3">
                               <!-- SZBIB -->
                               <i18n:text>physicaldescription</i18n:text>
                            </td>
                            <td class="col-9">
                                <xsl:variable name="EXTENT" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent"/>
                                <xsl:if test="$EXTENT/t:measure[@type='page']">
                                    <xsl:value-of select="$EXTENT/t:measure[@type='page']"/>
                                    <xsl:text> </xsl:text>
                                    <xsl:choose>
                                        <xsl:when test="$EXTENT/t:measure[@type='page'] = '1'">
                                            <xsl:choose>
                                                <xsl:when test="$locale = 'en'">
                                                    <xsl:text>page</xsl:text>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:text>Seite</xsl:text>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <i18n:text>pages</i18n:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                            	    <xsl:choose>
                            	        <xsl:when test="$EXTENT/t:measure[@type='leaf']">
                            				<xsl:text>, </xsl:text>
                            			</xsl:when>
                            	        <xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='extent']/t:item">
                            				<xsl:text> : </xsl:text>
                            			</xsl:when>
                            			<xsl:otherwise>
                            				<xsl:text>. </xsl:text>
                            			</xsl:otherwise>
                            		</xsl:choose>
                            	</xsl:if>
                                <xsl:if test="$EXTENT/t:measure[@type='leaf']">
                                    <xsl:value-of select="$EXTENT/t:measure[@type='leaf']"/>
                                    <xsl:text> </xsl:text>
                                    <xsl:choose>
                                        <xsl:when test="$EXTENT/t:measure[@type='leaf'] = '1'">
                                            <i18n:text>leaf</i18n:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:choose>
                                                <xsl:when test="$locale = 'en'">
                                                    <xsl:text>Leaves</xsl:text>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:text>Blatt</xsl:text>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:otherwise>
                                    </xsl:choose>
                            		<xsl:choose>
                            			<!--<xsl:when test="t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type='leaf']">
                            				<xsl:text>, </xsl:text>
                            			</xsl:when>-->
                            		    <xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='extent']/t:item">
                            				<xsl:text> : </xsl:text>
                            			</xsl:when>
                            			<xsl:otherwise>
                            				<xsl:text>. </xsl:text>
                            			</xsl:otherwise>
                            		</xsl:choose>
                            	</xsl:if>
    	                        <!-- illustriert, Karte, Noten -->
                                <xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='extent']/t:item">
    	                        	<xsl:choose>
    	                        		<xsl:when test="position() = last()">
    	                        			<xsl:value-of select="."/>
    	                        			<xsl:text>. </xsl:text>
    	                        		</xsl:when>
    	                        		<xsl:otherwise><xsl:value-of select="."/><xsl:text>, </xsl:text></xsl:otherwise>
    	                        	</xsl:choose> 	
                                </xsl:for-each>
                                <xsl:value-of select="$EXTENT/t:measure[@type='format']"/>
                                <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding">
    	                        	<xsl:text>, </xsl:text>
                                    <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding"/>
                            	</xsl:if>
                            </td>
                        </tr>	                                        	 		
                     </xsl:if>
    			 	 <!-- //////////////////////////////////////////////////////////// -->
                     <!-- //Originaltitel/// -->
    			     <xsl:if test="t:fileDesc/t:titleStmt/t:title[@type='original']">
                         <tr class="row">
                           <td class="col-3">
                               <i18n:text>originaltitle</i18n:text>
                            </td>
                            <td class="col-9">
                              <span class="font-italic">
                                  <xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@type='original']"/>
                            	</span>
                            </td>
                        </tr>
                     </xsl:if>
    			 	<!-- //////////////////////////////////////////////////////////// -->
    			 	<!--  HINWEIS  -->
    			     <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:note">
                         <tr class="row">
                           <td class="col-3">
                               <i18n:text>comment</i18n:text>
                            </td>
                            <td class="col-9">
                                <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:note"/>
                            </td>
                        </tr>
                     </xsl:if>
                         <!-- //////////////////////////////////////////////////////////// --> 
    				 	<!-- ///Provenienzkriterien/// -->
    				     <xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='provenancefeature']/t:item[not(t:stamp)]">
                              <tr class="row">
                                  <xsl:if test="position() = 1">
                                      <xsl:attribute name="class" select="'group row'"/>
                                  </xsl:if>
                               <td class="col-3">
                                   <a href="{t:ref/@target}" target="_blank">
                                        <xsl:choose>
                                            <xsl:when test="$locale = 'en'">
                                                <xsl:value-of select="t:term[@xml:lang = 'en']"/>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:value-of select="t:term[@xml:lang = 'de']"/>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                  	  <i class="fa fa-info-circle info_icon" aria-hidden="true"><xsl:text> </xsl:text></i>
                                	</a>
                                </td>
        						<!-- ///TABLE-LEFT/// -->
                                  <td class="col-9">		                                                                         	 			
                                      <!-- get @corresp -->
                                      <xsl:value-of select="t:desc"/>
                                  </td>
                              </tr>
                          </xsl:for-each>
    				     <xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='provenancefeature']/t:item[t:stamp]">
    				         <tr class="row">
    				             <td class="col-3">
    				                 <a href="{t:stamp/t:ref/@target}" target="_blank">
    				                     <xsl:choose>
    				                         <xsl:when test="$locale = 'en'">
    				                             <xsl:value-of select="t:stamp/t:term[@xml:lang = 'en']"/>
    				                         </xsl:when>
    				                         <xsl:otherwise>
    				                             <xsl:value-of select="t:stamp/t:term[@xml:lang = 'de']"/>
    				                         </xsl:otherwise>
    				                     </xsl:choose>
    				                     <i class="fa fa-info-circle info_icon" aria-hidden="true"><xsl:text> </xsl:text></i>
    				                 </a>
    				             </td>
    				             <!-- ///TABLE-LEFT/// -->
    				             <td class="col-9">		                                                                         	 			
    				                 <!-- get @corresp -->
    				                 <xsl:value-of select="t:desc"/>
    				             </td>
    				         </tr>
    				     </xsl:for-each>
    				 	 <!-- //////////////////////////////////////////////////////////// -->
                         <!-- ///ORIGINALSIGNATUREN/// -->
    				     <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:altIdentifier">
                              <tr class="group row">
    	                       <td class="col-3">
    	                           <a href="{concat('/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=', $locale, '#OriginalShelfmark')}" target="_blank">
    	                                <i18n:text>originalshelfmark</i18n:text>
    	                        		<i class="fa fa-info-circle info_icon" aria-hidden="true"><xsl:text> </xsl:text></i>
    	                        	</a>
    	                        </td>
                                   <td class="col-9">
                                       <!--<xsl:call-template name="Originalsignaturen"/>-->
                                       <div class="originalsignatur row">
                                           <xsl:for-each-group select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:altIdentifier" group-by="@corresp">
                                               <xsl:for-each select="current-group()">
                                                   <div class="col-3">
                                               	        <span><xsl:value-of select="normalize-space(.)"/></span></div>
                                               </xsl:for-each>
                                           </xsl:for-each-group>
                                       </div>
                                  </td>
                              </tr>
                          </xsl:if>
    				 	  <!-- //////////////////////////////////////////////////////////// -->
                          <!-- ///Provenienz/// -->
    				     <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance">
                              <tr class="group row">
    	                       <td class="col-3">
    	                           <i18n:text>laterowner</i18n:text>
    	                        </td>
                                  <td class="col-9">
                                      <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance"/>
                                  </td>
                              </tr>
                          </xsl:if>
    				 	 <!-- //////////////////////////////////////////////////////////// -->
                         <!-- ///Aktueller Ort/// -->
    				     <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:settlement">
    				         <tr class="group row">
                                 <!-- <xsl:if test="not(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance)">
                                      <xsl:attribute name="class" select="'group'"/>
                                  </xsl:if> -->
                                 <td class="col-3">
                                     <i18n:text>currentlocation</i18n:text>
                                  </td>
                                  <td class="col-9">
                                      <!-- /// -->
                                      <!-- SEARCH in BIBLIOHEK-->
                                      <xsl:call-template name="LocationSearch">
                                          <xsl:with-param name="locale" select="$locale"/>
                                          <xsl:with-param name="SZDSTA" select="substring-after(t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ref, '#')"/>
                                          <xsl:with-param name="location_string" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository"/>
                                      </xsl:call-template>
                                      <xsl:choose>
                                          <xsl:when test="contains(t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository, 'Literaturarchiv')">
                                              <xsl:text> </xsl:text>
                                              <a href="mailto:literaturarchiv@sbg.ac.at" title="Mail" >
                                                  <span class="glyphicon glyphicon-envelope icon small">
                                                      <xsl:text> </xsl:text>
                                                  </span>
                                              </a>
                                          </xsl:when>
                                          <xsl:otherwise></xsl:otherwise>
                                      </xsl:choose>
                                      <br></br>
                                      <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno"/>
                                  </td>
                              </tr>
                          </xsl:if>
               </tbody>
            </table>
             
             <!-- ////////////////////////////////// -->
             <!-- if its o:szd.publikation, no footer-->
             <xsl:choose>
                 <xsl:when test="$type = 'o:szd.publikation'">
                     <!-- all bibl inside a biblfull, all chapters -->
                     <!-- <xsl:value-of select="following-sibling::t:bibl/t:biblScope/text()"/>= <xsl:value-of select="@xml:id"/>-->
                     <xsl:variable name="ID" select="@xml:id"/>
                     <xsl:if test="..//t:bibl[t:biblScope/t:ref = $ID]">
                         <h3>
                             <a data-toggle="collapse" data-target="{concat('#', generate-id())}">
                                <span class="arrow">▼</span>
                                <xsl:choose>
                                    <xsl:when test="$locale = 'en'">
                                        <xsl:text>Content</xsl:text>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:text>Inhalt</xsl:text>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </a>
                         </h3>
                         <ul class="collapse" id="{generate-id()}">
                             <xsl:for-each select="..//t:bibl[t:biblScope/t:ref = $ID]">
                                 <li>
                                     <xsl:value-of select="t:title"/>
                                     <xsl:if test="t:biblScope/t:measure[@type='pages']">
                                         <xsl:text>, S.</xsl:text>
                                         <xsl:value-of select="t:biblScope/t:measure[@type='pages']"/>
                                     </xsl:if>
                                     <xsl:variable name="subID" select="@xml:id"/>  
                                     <xsl:variable name="subBibl" select="..//t:bibl[t:biblScope/t:ref = $subID]"/>
                                     <xsl:if test="$subBibl">
                                         <ul>
                                             <xsl:for-each select="$subBibl">
                                                 <li>
                                                    <xsl:value-of select="t:title"/>
                                                 </li>
                                             </xsl:for-each>
                                         </ul>
                                     </xsl:if>
                                 </li>
                             </xsl:for-each>
                         </ul>
                     </xsl:if>
                 </xsl:when>
                 <xsl:otherwise>
                     <xsl:call-template name="getFooter">
                         <xsl:with-param name="locale" select="$locale"/>
                     </xsl:call-template>
                 </xsl:otherwise>
             </xsl:choose>
         </div>
	</xsl:template>
    
    <!-- //////////////////////////////////////////////////////////// -->
    <!-- ZITIERVORSCHLAG -->
    <xsl:template name="getFooter">
        <xsl:param name="locale"/>
        <div class="card-footer small">
            <button data-toggle="collapse" data-target="{concat('#quote_', substring-after(@xml:id, '.'))}">
                <i18n:text>suggestedcitation</i18n:text>
            </button>
            <div id="{concat('quote_', substring-after(@xml:id, '.'))}" class="collapse font-weight-light">
              <xsl:if test=".//t:titleStmt/t:author[not(@role)]">
                  <xsl:for-each select=".//t:titleStmt/t:author[not(@role)]">
                      <xsl:call-template name="printAuthor">
                          <xsl:with-param name="currentAuthor" select="."/>
                      </xsl:call-template>
                      <xsl:if test="not(position()=last())">
                        <xsl:text> / </xsl:text>
                      </xsl:if>
                  </xsl:for-each>
              	 <xsl:text>: </xsl:text>
              </xsl:if>	
              <xsl:if test=".//t:titleStmt/t:author[@role='composer']">
                  <xsl:for-each select=".//t:titleStmt/t:author[@role='composer']">
                      <xsl:call-template name="printAuthor">
                          <xsl:with-param name="currentAuthor" select="."/>
                      </xsl:call-template>
                      <xsl:if test="not(position()=last())">
                          <xsl:text> / </xsl:text>
                      </xsl:if>
                  </xsl:for-each>  
              	 <xsl:text>: </xsl:text>
              </xsl:if>
              <xsl:if test=".//t:titleStmt/t:editor[@role='editor']">
               	<xsl:text> (</xsl:text>
                   <i18n:text>Hrsg.</i18n:text>
                   <xsl:text> </xsl:text>
                    <xsl:value-of select=".//t:titleStmt/t:editor[@role='editor']"/>
               	<xsl:text>)</xsl:text>
              </xsl:if>	
                <!-- e.g. Geheimnis des Alcovens -->
               <span class="font-italic">
                    <xsl:call-template name="printEnDe">
                        <xsl:with-param name="locale" select="$locale"/>
                        <!-- bibliothek, werke, autograph immer erster titel? -->
                        <xsl:with-param name="path" select=".//t:titleStmt/t:title[1]"/>
                    </xsl:call-template>
               </span>
                <!-- Ordnugnskategorie -->
                <xsl:if test=".//t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:span[@xml:lang = $locale]/t:term[@type='objecttyp']">
                    <xsl:text>, </xsl:text>
                    <xsl:value-of select=".//t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:span[@xml:lang = $locale]/t:term[@type='objecttyp']"/>
                </xsl:if>
               <!-- e.g. [Marie Antoinette] -->
                <xsl:if test=".//t:titleStmt/t:title[@type='Einheitssachtitel'][1]">
	              <xsl:text> [</xsl:text>
                    <xsl:call-template name="printEnDe">
                        <xsl:with-param name="locale" select="$locale"/>
                        <xsl:with-param name="path" select=".//t:titleStmt/t:title[@type='Einheitssachtitel']"/>
                    </xsl:call-template>
	              <xsl:text>]</xsl:text>
               </xsl:if>
               <xsl:text>. </xsl:text>
                <xsl:if test=".//t:sourceDesc/t:msDesc/t:msIdentifier/t:repository">
                    <xsl:value-of select=".//t:sourceDesc/t:msDesc/t:msIdentifier/t:repository"/>
                    <xsl:text>, </xsl:text>
                </xsl:if>
                <xsl:if test=".//t:sourceDesc/t:msDesc/t:msIdentifier/t:idno">
                    <xsl:value-of select=".//t:sourceDesc/t:msDesc/t:msIdentifier/t:idno"/>
               </xsl:if>		
              <xsl:text>. In: stefanzweig.digital, </xsl:text>
              <i18n:text>Hrsg.</i18n:text>
              <xsl:text> Literaturarchiv Salzburg, </xsl:text>
              <i18n:text>lastupdate</i18n:text>
              <xsl:text> </xsl:text>
              <xsl:choose>
                    <xsl:when test="//t:teiHeader/t:fileDesc/t:publicationStmt/t:date[1]/@when castable as xs:date">
                        <xsl:variable name="Date" select="//t:teiHeader/t:fileDesc/t:publicationStmt/t:date[1]/@when"/>
                        <xsl:value-of select="day-from-date($Date)"/><xsl:text>.</xsl:text><xsl:value-of select="month-from-date($Date)"/><xsl:text>.</xsl:text><xsl:value-of select="year-from-date($Date)"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="//t:teiHeader/t:fileDesc/t:publicationStmt/t:date[1]"/>
                    </xsl:otherwise>
              </xsl:choose>
              <xsl:text>, URL: </xsl:text>
              <xsl:value-of select="concat('stefanzweig.digital/', //t:publicationStmt//t:idno[@type='PID'], '#', @xml:id)"/>
            </div>
        </div>
    </xsl:template>
	
	<!-- PERSONSEARCH -->
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template name="PersonSearch">
	    <xsl:param name="locale"/>
	    <xsl:variable name="BaseURL" select="'/archive/objects/query:szd.person_search/methods/sdef:Query/get?params='"/>
		<xsl:choose>
			<xsl:when test="@ref or t:persName/@ref">
			    <xsl:variable name="REF" select="@ref | t:persName/@ref"/>
				<xsl:variable name="SZDPER">
					<xsl:call-template name="GetPersonList">
					    <xsl:with-param name="Person" select="$REF"/>
					</xsl:call-template>
				</xsl:variable>
			    
			    <xsl:variable name="Param" select="encode-for-uri(concat('$1|&lt;https://gams.uni-graz.at/o:szd.personen#', $SZDPER, '&gt;', ';$2|', $locale))"/>
			    <xsl:variable name="QueryUrl" select="concat($BaseURL, $Param, '&amp;locale=', $locale)"/>
			    
			    <!-- {concat('/archive/objects/query:szd.person_search/methods/sdef:Query/get?params=', encode-for-uri('$1|&lt;https://gams.uni-graz.at/o:szd.personen#'), encode-for-uri($SZDPER), '&gt;', encode-for-uri(';$2|'), encode-for-uri($locale), '&amp;locale=', $locale)} -->
			    <a href="{$QueryUrl}" target="_blank">
				    <xsl:choose>
				        <xsl:when test="$locale = 'en'">
				            <xsl:attribute name="title" select="'Suchanfrage'"/>
				        </xsl:when>
				        <xsl:otherwise>
				            <xsl:attribute name="title" select="'Search query'"/>
				        </xsl:otherwise>
				    </xsl:choose>
			        <xsl:call-template name="printAuthor">
			            <xsl:with-param name="currentAuthor" select="."/>
			        </xsl:call-template>
					<xsl:text> </xsl:text>
					<img src="{$Icon_suche_template}" class="img-responsive icon" alt="Person"/>
				</a>
				<xsl:text> </xsl:text>
			</xsl:when>
		    <xsl:when test="s:sn">
		        <xsl:variable name="SZDPER" select="s:author/@uri"/>
		        <xsl:variable name="Param" select="encode-for-uri(concat('$1|&lt;https://gams.uni-graz.at/o:szd.personen#', @xml:id, '&gt;', ';$2|', $locale))"/>
		        <xsl:variable name="QueryUrl" select="concat($BaseURL, $Param, '&amp;locale=', $locale)"/>
		        
		        <a href="{concat('/archive/objects/query:szd.person_search/methods/sdef:Query/get?params=', encode-for-uri('$1|&lt;'), encode-for-uri($SZDPER), '&gt;', encode-for-uri(';$2|'), encode-for-uri($locale), '&amp;locale=', $locale)}" target="_blank">
		            <xsl:choose>
		                <xsl:when test="$locale = 'en'">
		                    <xsl:attribute name="title" select="'Suchanfrage'"/>
		                </xsl:when>
		                <xsl:otherwise>
		                    <xsl:attribute name="title" select="'Search query'"/>
		                </xsl:otherwise>
		            </xsl:choose>
       		        <xsl:value-of select="s:sn"/>
       		        <xsl:if test="s:fn">
       		            <xsl:text>, </xsl:text>
       		            <xsl:value-of select="s:fn"/>
       		        </xsl:if>
		        </a>
		    </xsl:when>
			<xsl:otherwise>
			    <xsl:call-template name="printAuthor"/>
			    <!--<xsl:choose>
			        <xsl:when test="t:persName/t:surname">
			            <xsl:value-of select="normalize-space(t:persName/t:surname)"/>
			            <xsl:if test="t:persName/t:forename">
			                <xsl:value-of select="normalize-space(t:persName/t:forename)"/>
			            </xsl:if>
			        </xsl:when>
			        <xsl:otherwise>
			            <xsl:value-of select="normalize-space(.)"/>
			        </xsl:otherwise>
			    </xsl:choose>-->
			   
			    <xsl:text> </xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
    
    <!-- LOCATIONSEARCH -->
    <!-- //////////////////////////////////////////////////////////// -->
    <xsl:template name="LocationSearch">
        <xsl:param name="locale"/>
        <xsl:param name="SZDSTA"/>
        <xsl:param name="location_string"/>
        
        <xsl:variable name="BaseURL" select="'/archive/objects/query:szd.standort_search/methods/sdef:Query/get?params='"/>
        <xsl:variable name="Param" select="encode-for-uri(concat('$1|&lt;https://gams.uni-graz.at/o:szd.standorte#', $SZDSTA, '&gt;', ';$2|', $locale))"/>
        <xsl:variable name="QueryUrl" select="concat($BaseURL, $Param, '&amp;locale=', $locale)"/>
        
        <!-- Standortsuche -->
        <a href="{$QueryUrl}" target="_blank">
            <xsl:attribute name="title">
                <xsl:choose>
                    <xsl:when test="$locale = 'en'">
                        <xsl:text>Search query</xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>Suchanfrage</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <xsl:if test="$location_string">
                <xsl:value-of select="normalize-space($location_string)"/>
            </xsl:if>
            <xsl:if test=".//t:sourceDesc/t:msDesc/t:msIdentifier/t:settlement">
                <xsl:text>, </xsl:text>
                <xsl:value-of select="normalize-space(.//t:sourceDesc/t:msDesc/t:msIdentifier/t:settlement)"/>
            </xsl:if>
            <img src="{$Icon_suche_template}" class="img-responsive icon" alt="Standort"/>
        </a>
    </xsl:template>
    
    <!-- WORKSEARCH -->
    <!-- //////////////////////////////////////////////////////////// -->
    <xsl:template name="WorkSearch">
        <xsl:param name="locale"/>
        <xsl:choose>
            <xsl:when test="ancestor::t:biblFull/@xml:id">
                <xsl:variable name="SZDPUB" select="ancestor::t:biblFull/@xml:id"/>
                <a href="{concat('/archive/objects/query:szd.person_search/methods/sdef:Query/get?params=$1|&lt;https%3A%2F%2Fgams.uni-graz.at%2Fo%3Aszd.publikation%23', $SZDPUB, '&gt;', '&amp;locale=', $locale)}" target="_blank">
                    <xsl:choose>
                        <xsl:when test="$locale = 'en'">
                            <xsl:attribute name="title" select="'Suchanfrage'"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:attribute name="title" select="'Search query'"/>
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:value-of select="normalize-space(.)"/>
                    <xsl:text> </xsl:text>
                    <img src="{$Icon_suche_template}" class="img-responsive icon" alt="Person"/>
                </a>
                <xsl:text> </xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="normalize-space(.)"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- /////////////////////////////////////////////////////////// -->
    <!-- SZDMSK -->
    <!-- /////////////////////////////////////////////////////////// -->
	<!-- CREATE MANUSKRIPTE biblFull Entry -->
	<xsl:template name="FillbiblFull_SZDMSK">
	    <xsl:param name="locale"/>
	    <div class="table-responsive">
	       <table class="table table-sm">
	           <tbody>
               <!-- //////////////////////////////////////////////////////////// -->
               <!-- ///VERFASSER/// -->
                   <tr class="row">
                    <td class="col-3">
                        <i18n:text>author_szd</i18n:text>
                     </td>
                     <td class="col-9">
                         <xsl:call-template name="printAuthor">
                             <xsl:with-param name="currentAuthor" select="t:fileDesc/t:titleStmt/t:author[1]"/>
                         </xsl:call-template>
                     </td>
                   </tr>
                   <!-- //////////////////////////////////////////////////////////// -->
                   <!-- ///Beteiligte/// -->
	               <xsl:if test="t:fileDesc/t:titleStmt/t:editor">
                       <tr class="row">
                          <td class="col-3">
                              <a href="{concat('/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=', $locale, '#PartiesInvolved')}" target="_blank">
                                  <i18n:text>partiesinvolved</i18n:text>
                                  <i class="fa fa-info-circle info_icon" aria-hidden="true"><xsl:text> </xsl:text></i>
                               </a>
                           </td>
                           <td class="col-9">
                               <xsl:for-each select="t:fileDesc/t:titleStmt/t:editor[@role='contributor']">
                                   <xsl:call-template name="PersonSearch">
                                       <xsl:with-param name="locale" select="$locale"/>
                                   </xsl:call-template>
                               </xsl:for-each>
                           </td>
                       </tr>
                   </xsl:if>
                   <!-- //////////////////////////////////////////////////////////// -->
                   <!-- ///TITLEL/// -->
                   <tr class="row">
                    <td class="col-3">
                        <a href="/o:szd.glossar#Title" target="_blank">
                            <i18n:text>Titel</i18n:text>
                        </a>
                         <span>
                             <xsl:text> </xsl:text>
                             <xsl:if test="t:fileDesc/t:titleStmt/t:title[1]/@ana">
                                  <xsl:text>(</xsl:text>
                                      <xsl:choose>
                                          <xsl:when test="$locale = 'en'">
                                              <xsl:value-of select="t:fileDesc/t:titleStmt/t:title[1]/@ana"/>
                                          </xsl:when>
                                          <xsl:otherwise>
                                              <xsl:choose>
                                                  <xsl:when test="t:fileDesc/t:titleStmt/t:title[1]/@ana = 'assigned'">
                                                      <xsl:text>fingiert</xsl:text>
                                                  </xsl:when>
                                                  <xsl:when test="t:fileDesc/t:titleStmt/t:title[1]/@ana = 'supplied/verified'">
                                                      <xsl:text>ermittelt</xsl:text>
                                                  </xsl:when>
                                                  <xsl:otherwise>
                                                      <xsl:text>original</xsl:text>
                                                  </xsl:otherwise>
                                              </xsl:choose>
                                          </xsl:otherwise>
                                      </xsl:choose>    	                             	     
                                  <xsl:text>)</xsl:text>
                              </xsl:if>
                         </span>
                         <i class="fa fa-info-circle info_icon" aria-hidden="true"><xsl:text> </xsl:text></i>
                     </td>
                     <td class="col-9">
                     <i>
                         <xsl:call-template name="printEnDe">
                             <xsl:with-param name="path" select="t:fileDesc/t:titleStmt/t:title[not(@type)]"/>
                             <xsl:with-param name="locale" select="$locale"/>
                         </xsl:call-template>
                         <!--<xsl:choose>
                             <xsl:when test="$locale = 'en'">
                                 <xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[@xml:lang = 'en'][not(@type)][1])"/>
                             </xsl:when>
                             <xsl:otherwise>
                                 <xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[not(@type)][1])"/>
                             </xsl:otherwise>
                         </xsl:choose>-->
                         </i>
                     <xsl:text> </xsl:text>
                     <!-- INHALT -->
                     <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary/*">
                        <br/>
                        <xsl:text>[</xsl:text>
                         <xsl:call-template name="printEnDe">
                             <xsl:with-param name="locale" select="$locale"/>
                             <xsl:with-param name="path" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary/*"/>
                         </xsl:call-template>
                        <xsl:text>]</xsl:text>
                     </xsl:if>
                     </td>
                   </tr>
                   <!-- //////////////////////////////////////////////////////////// -->
	               <!-- /// INCIPIT /// -->
	               <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:incipit">
                       <tr class="row">
                          <td class="col-3">
                              <a href="{concat('/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=', $locale, '#Incipit')}" target="_blank">
                                   <xsl:text>Incipit</xsl:text>
                                   <i class="fa fa-info-circle info_icon" aria-hidden="true"><xsl:text> </xsl:text></i>
                               </a>
                           </td>
                           <td class="col-9">
                               <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:incipit"/>
                           </td>
                       </tr>
                   </xsl:if>
                   <!-- //////////////////////////////////////////////////////////// -->
                   <!-- /// AUFSCHRIFT /// -->
	               <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:docEdition">
                       <tr class="row">
                            <td class="col-3">
                                <a href="{concat('/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=', $locale, '#IdentifyingInscription')}" target="_blank">
                                <i18n:text>identifyinginscription</i18n:text>
                                <i class="fa fa-info-circle info_icon" aria-hidden="true"><xsl:text> </xsl:text></i>
                             </a>
                           </td>
                           <td class="col-9">
                               <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:docEdition[@xml:lang = $locale]"/>
                           </td>
                       </tr>
                   </xsl:if>
                   <!-- //////////////////////////////////////////////////////////// -->
                   <!-- ///ORIGIPLACE/// -->
	               <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:origin/t:origPlace">
                       <tr class="row">
                          <td class="col-3">
                              <i18n:text>placeofcreation</i18n:text>
                           </td>
                           <td class="col-9">
                               <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:origin/t:origPlace"/>
                           </td>
                       </tr>
                   </xsl:if>
                   <!-- //////////////////////////////////////////////////////////// -->
                   <!-- ///ORIGIDATE, Datierung/// -->
	               <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:origin/t:origDate">
                   <tr class="row">
                      <td class="col-3">
                          <a href="{concat('/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=', $locale, '#Date')}" target="_blank">
                              <i18n:text>dates</i18n:text>
                              <i class="fa fa-info-circle info_icon" aria-hidden="true"><xsl:text> </xsl:text></i>
                          </a>
                       </td>
                       <td class="col-9">
                           <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:origin/t:origDate"/>
                       </td>
                   </tr>
                   </xsl:if>	
                   <!-- //////////////////////////////////////////////////////////// -->
                   <!-- ///Sprache/// -->
	               <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang">
                       <tr class="row">
                          <td class="col-3">
                              <i18n:text>language</i18n:text>
                           </td>
                           <td class="col-9">
                               <xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang/t:lang/@xml:lang">
                                   <xsl:choose>
                                       <xsl:when test="position() = last()">
                                           <!-- tempalte in szd-genericTempaltes.xsl -->
                                           <xsl:call-template name="languageCode">
                                               <xsl:with-param name="locale" select="$locale"/>
                                               <xsl:with-param name="Current" select="."/>
                                           </xsl:call-template><xsl:text> </xsl:text>
                                       </xsl:when>
                                       <xsl:otherwise>
                                           <xsl:call-template name="languageCode">
                                               <xsl:with-param name="locale" select="$locale"/>
                                               <xsl:with-param name="Current" select="."/>
                                           </xsl:call-template><xsl:text>, </xsl:text>
                                       </xsl:otherwise>
                                   </xsl:choose>
                               </xsl:for-each>
                               <xsl:text> </xsl:text>
                           </td>
                       </tr>
                   </xsl:if>
                   <!-- //////////////////////////////////////////////////////////// -->
                   <!-- ///Typ, Blatt, Format/// -->
	               <xsl:variable name="EXTENT" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent"/>
	               <xsl:if test="$EXTENT">
                       <tr class="group row">
                          <td class="col-3">
                              <!-- SZDMSK -->
                              <i18n:text>physicaldescription</i18n:text>
                           </td>
                           <td class="col-9">
                               <xsl:value-of select="$EXTENT/t:span[@xml:lang = $locale]"/>
                           <!--	<xsl:value-of select="t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent"/>-->
                               <!--<xsl:choose>
                                   <!-\- if "Konvolut" -\->
                                   <xsl:when test="$EXTENT/t:span/t:term[text() = 'Konvolut'] | $EXTENT/t:span/t:term[text() = 'Collection']">
                                       <xsl:value-of select="$EXTENT/t:span[@xml:lang = $locale]/t:term"/>
                                       <xsl:text>: </xsl:text>
                                       <xsl:choose>
                                           <xsl:when test="$EXTENT/t:span[@xml:lang = $locale]/t:measure[@type='leaf']">
                                               <xsl:value-of select="$EXTENT/t:span[@xml:lang = $locale]/t:measure[@type='leaf']"/>
                                           </xsl:when>
                                           <xsl:when test="$EXTENT/t:span[@xml:lang = $locale]/t:measure[@type='piece']">
                                               <xsl:text>, </xsl:text>
                                               <xsl:value-of select="$EXTENT/t:span[@xml:lang = $locale]/t:measure[@type='piece']"/>
                                               <!-\- <xsl:text> Stück</xsl:text>-\->
                                               <xsl:text> </xsl:text>
                                               <i18n:text>piece</i18n:text>
                                           </xsl:when>
                                           <xsl:otherwise/>
                                       </xsl:choose>
                                   </xsl:when>
                                   <!-\- e.g. Ledger, or Notebook, -\->
                                   <xsl:otherwise>
                                       <xsl:value-of select="$EXTENT/t:span[@xml:lang = $locale]/t:term"/>
                                       <xsl:choose>
                                           <xsl:when test="$EXTENT/t:span/t:measure[@type='leaf']">
                                               <xsl:text>, </xsl:text>
                                               <xsl:value-of select="$EXTENT/t:span[@xml:lang = $locale]/t:measure[@type='leaf']"/>
                                               <!-\- if Leaf or Blatt is not included in the <measure> -\->
                                               <xsl:if test="not(contains($EXTENT/t:span[@xml:lang = $locale]/t:measure[@type='leaf'], 'Blatt')
                                                   or contains($EXTENT/t:span[@xml:lang = $locale]/t:measure[@type='leaf'], 'leaf') 
                                                   or contains($EXTENT/t:span[@xml:lang = $locale]/t:measure[@type='leaf'], 'leav'))">
                                                   <xsl:text> </xsl:text>
                                                   <i18n:text>leaf</i18n:text>
                                               </xsl:if>
                                           </xsl:when>
                                           <xsl:when test="$EXTENT/t:span[@xml:lang = $locale]/t:measure[@type='piece']">
                                               <xsl:text>, </xsl:text>
                                               <xsl:value-of select="$EXTENT/t:span[@xml:lang = $locale]/t:measure[@type='piece']"/>
                                               <xsl:text> </xsl:text>
                                               <i18n:text>piece</i18n:text>
                                           </xsl:when>
                                           <xsl:otherwise/>
                                       </xsl:choose>
                                   </xsl:otherwise>
                               </xsl:choose>-->
                               <xsl:if test="$EXTENT/t:span/t:measure[@type='leaf']/@ana">
                                   <!--<xsl:if test="not(contains($EXTENT/t:span/t:measure[@type='leaf'], 'corrected'))">
                                   <xsl:text>, </xsl:text>
                                   <!-\-<xsl:text>, korrigiert</xsl:text>-\->
                                       <i18n:text>corrected</i18n:text>
                                   </xsl:if>-->
                               </xsl:if>
                               <xsl:if test="$EXTENT/t:measure[@type='format']">
                                   <xsl:text>, </xsl:text>
                                        <xsl:value-of select="$EXTENT/t:measure[@type='format']"/>
                                   </xsl:if>
                               <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:foliation/t:ab">
                                   <xsl:text>, </xsl:text>
                                   <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:foliation/t:ab[@xml:lang = $locale]"/>
                                  </xsl:if>
                               <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab">
                                   <xsl:text>, </xsl:text>
                                   <xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding/t:ab[@xml:lang = $locale])"/>
                               </xsl:if>
                           </td>
                       </tr>
                   </xsl:if>
                   <!-- //////////////////////////////////////////////////////////// -->
                   <!-- ///Beschreibstoff/// -->
	               <xsl:variable name="SUPPORT" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:support"/>
	               <xsl:if test="$SUPPORT/t:material[@ana='https://gams.uni-graz.at/o:szd.glossar#WritingMaterial']">
                       <tr class="row">
                          <td class="col-3">
                              <i18n:text>writingmaterial</i18n:text>
                           </td>
                           <td class="col-9">
                               <xsl:value-of select="$SUPPORT/t:material[@ana='https://gams.uni-graz.at/o:szd.glossar#WritingMaterial'][@xml:lang = $locale]"/>
                           </td>
                       </tr>
                   </xsl:if>
                   <!-- //////////////////////////////////////////////////////////// -->
                   <!-- ///Schreibstoff/// -->
	               <xsl:if test="$SUPPORT/t:material[@ana='https://gams.uni-graz.at/o:szd.glossar#WritingInstrument']">
                       <tr class="row">
                          <td class="col-3">
                              <i18n:text>writinginstrument</i18n:text>
                           </td>
                           <td class="col-9">
                               <xsl:value-of select="$SUPPORT/t:material[@ana='https://gams.uni-graz.at/o:szd.glossar#WritingInstrument'][@xml:lang = $locale]"/>
                               <xsl:if test="$SUPPORT/t:label[@ana='https://gams.uni-graz.at/o:szd.glossar#WritingInstrument']">
                                    <br/>
                                    <xsl:text>Label: </xsl:text><xsl:value-of select="$SUPPORT/t:label[@ana='https://gams.uni-graz.at/o:szd.glossar#WritingInstrument']"/>
                               </xsl:if>
                           </td>
                       </tr>
                       </xsl:if>
                   <!-- //////////////////////////////////////////////////////////// -->
                   <!-- Schreiberhände -->
	               <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:handDesc/t:ab">
                       <tr class="row">
                          <td class="col-3">
                              <i18n:text>secretarialhand</i18n:text>
                           </td>
                           <td class="col-9">
                               <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:handDesc/t:ab"/>
                           </td>
                       </tr>
                   </xsl:if>
                  <!-- //////////////////////////////////////////////////////////// -->
                  <!-- Hinweise -->
	              <xsl:if test="t:fileDesc/t:notesStmt/t:note">
                    <tr class="row">
                      <td class="col-3">
                          <i18n:text>notes</i18n:text>
                       </td>
                       <td class="col-9">
                           <xsl:call-template name="printEnDe">
                               <xsl:with-param name="path" select="t:fileDesc/t:notesStmt/t:note"/>
                               <xsl:with-param name="locale" select="$locale"/>
                           </xsl:call-template>
                       </td>
                    </tr>
                  </xsl:if>
                  <!-- //////////////////////////////////////////////////////////// -->
                  <!-- Beilagen, bold -->
	               <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:accMat/t:list/t:item[@ana='https://gams.uni-graz.at/o:szd.glossar#Enclosures']/t:desc">
                       <tr class="group row">
                          <td class="col-3">
                              <a  href="{concat('/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=', $locale, '#Enclosures')}" target="_blank" title="vom Autor oder im Entstehungszusammenhang">
                                  <i18n:text>enclosures</i18n:text>
                                   <i class="fa fa-info-circle info_icon" aria-hidden="true"><xsl:text> </xsl:text></i>
                               </a>
                           </td>
                           <td class="col-9">
                               <xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:accMat/t:list/t:item[@ana='https://gams.uni-graz.at/o:szd.glossar#Enclosures']">
                                   <xsl:value-of select="t:desc[@xml:lang = $locale]"/>
                                   <xsl:if test="not(t:measure = '')">
                                       <xsl:text>, </xsl:text>
                                       <xsl:value-of select="normalize-space(t:measure)"/>
                                   </xsl:if>
                                   <xsl:if test="not(position() = last())"><br/><br/></xsl:if>
                               </xsl:for-each>	                                       
                           </td>
                       </tr>
                  </xsl:if>
                  <!-- //////////////////////////////////////////////////////////// -->
                  <!-- Zusatzmaterial -->
	               <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:accMat/t:list/t:item[@ana='https://gams.uni-graz.at/o:szd.glossar#AdditionalMaterial']">
                   <tr class="row">
                       <xsl:if test="not(t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:accMat/t:list/t:item[@ana='https://gams.uni-graz.at/o:szd.glossar#AdditionalMaterial']/t:desc)">
                           <xsl:attribute name="class" select="'group'"/>
                       </xsl:if>
                      <td class="col-3">
                          <a href="{concat('/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=', $locale, '#AdditionalMaterial')}" target="_blank" title="Später oder von Dritten hinzugefügtes">
                            <i18n:text>additionalmaterial</i18n:text>
                               <i class="fa fa-info-circle info_icon" aria-hidden="true"><xsl:text> </xsl:text></i>
                           </a>
                       </td>
                       <td class="col-9">
                           <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:accMat/t:list/t:item[@ana='https://gams.uni-graz.at/o:szd.glossar#AdditionalMaterial']/t:desc[@xml:lang = $locale]"/>
                       </td>
                   </tr>
                   </xsl:if>
                   <!-- //////////////////////////////////////////////////////////// -->
                   <!-- ///Provenienz/// -->
	               <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance">
                       <tr class="group row">
                          <td class="col-3">
                              <i18n:text>provenance</i18n:text>
                           </td>
                           <td class="col-9">
                               <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance"/>
                           </td>
                       </tr>
                   </xsl:if>
                   <!-- //////////////////////////////////////////////////////////// -->
                   <!-- ///Erwerbung/// -->
	               <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition">
                       <tr class="row">
                          <td class="col-3">
                              <i18n:text>acquired</i18n:text>
                           </td>
                           <td class="col-9">
                               <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition"/>
                           </td>
                       </tr>
                   </xsl:if>
                   <!-- //////////////////////////////////////////////////////////// -->
                   <!-- ///Standort/// -->
	               <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier">
                       <tr class="row">
                          <td class="col-3">
                              <i18n:text>currentlocation</i18n:text>
                           </td>
                           <td class="col-9">
                               <!-- SEARCH WERKE -->
                               <xsl:call-template name="LocationSearch">
                                   <xsl:with-param name="locale" select="$locale"/>
                                   <xsl:with-param name="SZDSTA">
                                       <xsl:choose>
                                           <xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ana">
                                               <xsl:value-of select="substring-after(t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ana, '#')"/>
                                           </xsl:when>
                                           <xsl:otherwise>
                                               <xsl:call-template name="GetStandortList">
                                                   <xsl:with-param name="Standort" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository/@ref"></xsl:with-param>
                                               </xsl:call-template>
                                           </xsl:otherwise>
                                       </xsl:choose>
                                   </xsl:with-param>
                                   <xsl:with-param name="location_string" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository"/>
                               </xsl:call-template>
                               <xsl:choose>
                                   <xsl:when test="contains(t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository, 'Literaturarchiv')">
                                       <xsl:text> </xsl:text>
                                       <a href="mailto:literaturarchiv@sbg.ac.at" title="Mail" >
                                           <i class="fas fa-envelope"><xsl:text> </xsl:text></i>
                                       </a>
                                   </xsl:when>
                                   <xsl:otherwise/>
                               </xsl:choose>
                               <br/>
                               <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno"/>
                           </td>
                       </tr>
                   </xsl:if>
	           </tbody>
	    </table>
	    <!-- //////////////////////////////////////////////////////////// -->
	    <!-- card FOOTER -->
	    <xsl:call-template name="getFooter">
	        <xsl:with-param name="locale" select="$locale"/>
	    </xsl:call-template>
	    <!--<div class="card-footer small"><xsl:text>Permalink: </xsl:text><strong><xsl:value-of select="concat('stefanzweig.digital/', //t:publicationStmt//t:idno[@type='PID'], '#', @xml:id)"/></strong></div>-->
	    </div>
	</xsl:template>
	<!-- END SZDMSK_biblFUll -->
    
    
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- SZDAUT -->
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- autohraphs biblFull Entry on o:szd.autographs -->
    <xsl:template name="FillbiblFull_SZDAUT">
        <xsl:param name="locale"/>
        <div class="table-responsive">
        <table class="table table-sm">
            <tbody>
                <!-- ///Verfasser/// -->
                <xsl:if test="t:fileDesc/t:titleStmt/t:author[1][not(@role)]">
                    <tr class="row">
                        <td class="col-3">
                            <xsl:choose>
                                <xsl:when test="t:fileDesc/t:titleStmt/t:title[@type='object']">
                                    <xsl:choose>
                                        <xsl:when test="$locale='en'">
                                            <xsl:text>Creator</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>Schöper/in</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:when>
                                <xsl:otherwise>
                                    <i18n:text>author_szd</i18n:text>
                                </xsl:otherwise>
                            </xsl:choose>
                            
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:fileDesc/t:titleStmt/t:author">
                                <xsl:call-template name="PersonSearch">
                                    <xsl:with-param name="locale" select="$locale"/>
                                </xsl:call-template>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <!-- //////////////////////////////////////////////////////////// -->
                <!-- ///Composer/// -->
                <xsl:if test="t:fileDesc/t:titleStmt/t:author[1][@role = 'composer']">
                    <tr class="row">
                        <td class="col-3">
                            <i18n:text>composer</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:fileDesc/t:titleStmt/t:author">
                                <xsl:call-template name="PersonSearch">
                                    <xsl:with-param name="locale" select="$locale"/>
                                </xsl:call-template>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <!-- //////////////////////////////////////////////////////////// -->
                <!-- ///Betroffene Person/// -->
                <xsl:if test="t:profileDesc/t:textClass/t:keywords/t:term[@type='person_affected']">
                    <tr class="row">
                        <td class="col-3">
                            <i18n:text>person_affected</i18n:text>                            
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:profileDesc/t:textClass/t:keywords/t:term[@type='person_affected']">
                                <xsl:call-template name="PersonSearch">
                                    <xsl:with-param name="locale" select="$locale"/>
                                </xsl:call-template>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <!-- //////////////////////////////////////////////////////////// -->
                <!-- ///Beteilgite Person/// -->
                <xsl:if test="t:profileDesc/t:textClass/t:keywords/t:term[@type='person']">
                    <tr class="row">
                        <td class="col-3">
                            <i18n:text>partiesinvolved</i18n:text>                            
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:profileDesc/t:textClass/t:keywords/t:term[@type='person']">
                                <xsl:call-template name="PersonSearch">
                                    <xsl:with-param name="locale" select="$locale"/>
                                </xsl:call-template>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <!-- //////////////////////////////////////////////////////////// -->
                <!-- ///TITEL/// -->
                <xsl:if test="t:fileDesc/t:titleStmt/t:title[1]">
                    <tr class="row">
                        <td class="col-3">
                            <i18n:text>Titel</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:choose>
                                <xsl:when test="t:fileDesc/t:titleStmt/t:title/@ref">
                                    <a href="{t:fileDesc/t:titleStmt/t:title/@ref}" target="_blank">
                                        <xsl:attribute name="title">
                                            <xsl:choose>
                                                <xsl:when test="$locale ='en'">
                                                    <xsl:text>External Resource</xsl:text>
                                                </xsl:when>
                                                <xsl:otherwise>Externe Ressource</xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:attribute>
                                        <xsl:apply-templates select="t:fileDesc/t:titleStmt/t:title"/>
                                        <xsl:text> </xsl:text>
                                        <i class="fas fa-external-link-alt _icon small pl-1"><xsl:text> </xsl:text></i>
                                    </a>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:apply-templates select="t:fileDesc/t:titleStmt/t:title"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary">
                    <tr class="row">
                        <td class="col-3">
                            <i18n:text>description</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:apply-templates select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary"/>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang/t:lang">
                    <tr class="row">
                        <td class="col-3">
                            <i18n:text>language</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang/t:lang">
                                <xsl:call-template name="languageCode">
                                    <xsl:with-param name="Current" select="@xml:lang"/>
                                    <xsl:with-param name="locale" select="$locale"/>
                                </xsl:call-template>
                                <xsl:if test="not(position() = last())">
                                    <xsl:text>, </xsl:text>
                                </xsl:if>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:if>
                <!-- //////////////////////////////////////////////////////////// -->
                <!-- ///UMFANG/// -->
                <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc">
                    <tr class="group row">
                        <td class="col-3">
                            <!-- SZDAUT -->
                            <i18n:text>physicaldescription</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:variable name="EXTENT" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent"/>
                            <xsl:choose>
                                <!-- if its pages -->
                                <xsl:when test="$EXTENT/t:measure[@type='page']">
                                    <xsl:value-of select="$EXTENT/t:measure[@type='page']"/>
                                    <xsl:text> </xsl:text>
                                    <xsl:choose>
                                        <xsl:when test="$EXTENT/t:measure[@type='page'] = '1'">
                                            <xsl:choose>
                                                <xsl:when test="$locale = 'en'">
                                                    <xsl:text>page</xsl:text>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:text>Seite</xsl:text>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <i18n:text>pages</i18n:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:when>
                                <!-- if its a leaf or leaves -->
                                <xsl:when test="$EXTENT/t:measure[@type='leaf']">
                                    <xsl:value-of select="$EXTENT/t:measure[@type='leaf']"/>
                                    <xsl:text> </xsl:text>
                                    <xsl:choose>
                                        <xsl:when test="$EXTENT/t:measure[@type='leaf'] = '1'">
                                            <i18n:text>leaf</i18n:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:choose>
                                                <xsl:when test="$locale = 'en'">
                                                    <xsl:text>leaves</xsl:text>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:text>Blatt</xsl:text>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:when>
                                <xsl:otherwise/>
                            </xsl:choose>
                            <xsl:text> </xsl:text>
                            <!-- for szd:o.bibliothek -->
                            <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='extent']/t:item">
                                <xsl:text> : </xsl:text>
                            </xsl:if>
                            <!-- illustriert, Karte, Noten -->
                            <xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='extent']/t:item">
                                <xsl:choose>
                                    <xsl:when test="position() = last()">
                                        <xsl:value-of select="."/>
                                        <xsl:text>. </xsl:text>
                                    </xsl:when>
                                    <xsl:otherwise><xsl:value-of select="."/><xsl:text>, </xsl:text></xsl:otherwise>
                                </xsl:choose> 	
                            </xsl:for-each>
                            <xsl:value-of select="$EXTENT/t:measure[@type='format']"/>
                            <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding">
                                <xsl:text>, </xsl:text>
                                <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:bindingDesc/t:binding"/>
                            </xsl:if>
                        </td>
                    </tr>	                                        	 		
                </xsl:if>

                <!-- //////////////////////////////////////////////////////////// -->
                <!-- ////// -->
                <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition">
                    <tr class="group row">
                        <td class="col-3">
                            <i18n:text>acquired</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:apply-templates select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition"/>
                        </td>
                    </tr>
                </xsl:if>
                <!-- //////////////////////////////////////////////////////////// -->
                <!-- ///Provenienz/// -->
                <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance">
                    <tr class="row">
                        <td class="col-3">
                            <i18n:text>currentlocation</i18n:text>
                        </td>
                        <td class="col-9">
                            <!--<xsl:value-of select="t:sourceDesc/t:msDesc/t:history/t:provenance"/>-->
                            <xsl:apply-templates select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance">
                                <xsl:with-param name="locale" select="$locale"/>
                            </xsl:apply-templates>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
        </div>
        <!-- //////////////////////////////////////////////////////////// -->
        <!-- card FOOTER -->
        <xsl:call-template name="getFooter">
            <xsl:with-param name="locale" select="$locale"/>
        </xsl:call-template>
        <!--<div class="card-footer small"><xsl:text>Permalink: </xsl:text><strong><xsl:value-of select="concat('stefanzweig.digital/', //t:publicationStmt//t:idno[@type='PID'], '#', @xml:id)"/></strong></div>-->
    </xsl:template>
    
    
    <!-- /////////////////////////////////////////////////////////// --> 
    <!-- ///EN|DE/// -->
    <!-- this template gets an xpath-selection as input and check if there is a xml:lang, than $locale, otherwise print without @xml:lang -->
    <xsl:template name="printEnDe">
        <xsl:param name="path"/>
        <xsl:param name="locale"/>
        <xsl:choose>
            <xsl:when test="$path/@xml:lang">
                <xsl:value-of select="normalize-space($path[@xml:lang = $locale][1])"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="normalize-space($path[1])"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
   
    <!-- //////////////////////////////////////////////////////////// -->
    <!-- for o:szd.autographs-->
    <xsl:template match="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:orgName[@ref]">
        <xsl:param name="locale"/>
        <xsl:call-template name="LocationSearch">
            <xsl:with-param name="locale" select="$locale"/>
            <xsl:with-param name="SZDSTA">
                <xsl:call-template name="GetStandortList">
                    <xsl:with-param name="Standort" select="@ref"/>
                </xsl:call-template>
            </xsl:with-param>
            <xsl:with-param name="location_string" select="."/>
        </xsl:call-template>
    </xsl:template>
    
    
    <!-- //////////////////////////////////////////////////////////// -->
    <!-- for o:szd.autographs-->
    <xsl:template match="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:idno[@type='signature']">
        <br/><xsl:apply-templates/>
    </xsl:template>

    <!-- /////////////////////////////////////////////////////////// --> 
    <!-- ///LANGUAGES/// -->
    <!-- called when iso-lanuage is found in TEI, checks with $Languages, which is a simple .xml. datastream in context:szd -->
    <xsl:template name="languageCode">
        <xsl:param name="Current"/>
        <xsl:param name="locale"/>
        <xsl:for-each select="$Languages//*:entry">
            <!-- comparing string, iso-code -->
            <xsl:if test="*:code[@type = 'ISO639-2'] = $Current">
                <xsl:choose>
                    <xsl:when test="$locale = 'en'">
                        <xsl:value-of select="*:language[@type = 'english']"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="*:language[@type = 'german']"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template name="getLabelDatabasket">
        <xsl:param name="locale"/>
        <label class="d-none d-sm-block col-1 text-right">
            <input  onClick="add_DB(this)" type="checkbox" class="form-check-input">
                <xsl:choose>
                    <xsl:when test="$locale = 'en'">
                        <xsl:attribute name="title" select="'Save to data cart'"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:attribute name="title" select="'Im Datenkorb ablegen'"/>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:text> </xsl:text>
            </input>
        </label>
    </xsl:template>
    
    <xsl:template name="getEntry_SZDBIB_SZDAUT">
        <xsl:param name="locale"/>
            <!-- data-basket -->
            <xsl:call-template name="AddData-Databasket"/>
            <div class="bg-light row">
                <h4 class="card-title text-left col-11 small">
                    <a data-toggle="collapse" href="{concat('#c' , generate-id())}">
                        <span class="arrow">
                            <xsl:text>&#9660; </xsl:text>
                        </span>
                        
                        <xsl:apply-templates select="t:fileDesc/t:titleStmt/t:title[1]"/>
                        <!--<xsl:choose>
                            <xsl:when test="string-length(t:fileDesc/t:titleStmt/t:title[1]) > 70">
                                
                                <!-\-<span class="font-italic"><xsl:value-of select="normalize-space(substring(t:fileDesc/t:titleStmt/t:title[1], 1, 70))"/><xsl:text>... </xsl:text></span>-\->
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:apply-templates select="t:fileDesc/t:titleStmt/t:title[1]"/>
                                <!-\-<span class="font-italic"><xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[1])"/></span>-\->
                            </xsl:otherwise>
                        </xsl:choose>--> 
                    </a>
                    <xsl:if test="t:fileDesc/t:publicationStmt/t:date">
                        <xsl:text> | </xsl:text><xsl:value-of select="t:fileDesc/t:publicationStmt/t:date"/>
                    </xsl:if>
                </h4>
                    <!-- checkbox databasket -->
                    <xsl:call-template name="getLabelDatabasket">
                        <xsl:with-param name="locale" select="$locale"/>
                    </xsl:call-template>
                    
                   <!-- <label class="col-md-1 float-right">
                        <input  onClick="getData(this.id)"  id="{concat('cb', @xml:id)}" type="checkbox" class="checkbox">
                            <xsl:choose>
                                <xsl:when test="$locale = 'en'">
                                    <xsl:attribute name="title" select="'Save to data cart'"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:attribute name="title" select="'Im Datenkorb ablegen'"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </input>
                    </label> -->
               
            </div>
    </xsl:template>
    
    <!-- /////////////////////// -->
    <!-- this template prints different types of <author> (role="composer"; <persName> or <name>) and prints them in the way: SURNAME, FIRSTNAME
         you can also use $currentAuthor as a input next to the current selected node -->
    <xsl:template name="printAuthor">
        <xsl:param name="currentAuthor"/>
        <xsl:choose>
            <xsl:when test="t:persName/t:surname">
                <xsl:for-each select="t:persName">
                    <xsl:value-of select="normalize-space(t:surname)"/>
                    <xsl:if test="t:forename">
                        <xsl:text>, </xsl:text>
                        <xsl:value-of select="normalize-space(t:forename)"/>
                    </xsl:if>
                </xsl:for-each>
            </xsl:when>
            <xsl:when test="t:persName/t:name">
                <xsl:for-each select="t:persName">
                    <xsl:value-of select="normalize-space(t:name)"/>
                </xsl:for-each>
            </xsl:when>
            <xsl:when test="$currentAuthor">
                <xsl:choose>
                    <xsl:when test="$currentAuthor/t:persName/t:surname">
                        <xsl:for-each select="$currentAuthor/t:persName">
                            <xsl:value-of select="normalize-space(t:surname)"/>
                            <xsl:if test="t:forename">
                                <xsl:text>, </xsl:text>
                                <xsl:value-of select="normalize-space(t:forename)"/>
                            </xsl:if>
                        </xsl:for-each>
                    </xsl:when>
                    <xsl:when test="$currentAuthor/t:persName/t:name">
                        <xsl:for-each select="$currentAuthor/t:persName">
                            <xsl:value-of select="normalize-space(.)"/>
                        </xsl:for-each>
                    </xsl:when>
                    <xsl:when test="$currentAuthor/t:surname">
                        <xsl:value-of select="normalize-space($currentAuthor/t:surname)"/>
                        <xsl:if test="$currentAuthor/t:forename">
                            <xsl:text>, </xsl:text>
                            <xsl:value-of select="normalize-space($currentAuthor/t:forename)"/>
                        </xsl:if>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="normalize-space($currentAuthor)"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="normalize-space(.)"/>
            </xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>
    
    
    <xsl:template name="getfirstforABC">
        <xsl:param name="Persons"/>
        <xsl:param name="CurrentNodes"/>
        <!-- get first alphabetically, href using ABC-Array -->
        <xsl:variable name="firstPerson">
            <xsl:for-each select="$Persons[substring(., 1, 1) = substring($CurrentNodes, 1, 1)]">
                <xsl:sort select="."/>
                <xsl:if test="position() = 1">
                    <xsl:value-of select="."/>
                </xsl:if>
            </xsl:for-each>
        </xsl:variable>
        <!-- empty span to jump from ABC-Nav -->
        <xsl:if test="normalize-space($CurrentNodes) = normalize-space($firstPerson)">
            <div id="{substring($firstPerson,1,1)}"><xsl:text> </xsl:text></div>
        </xsl:if>
    </xsl:template>
    
    
</xsl:stylesheet>