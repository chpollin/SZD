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
    <xsl:variable name="Icon_gnd" select="concat($Icon_Path_template, 'gnd.png')"/>
    
    
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
        <article class="sticky-top header-card-nav">     
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
                       <xsl:if test="not(contains($PID, 'szd.glossar'))">
                         <a href="{concat('/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=', $locale, '#', $GlossarRef)}">
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
                       </xsl:if>
                    </h2>  
                </div>
               <div class="col-2 text-right">
                   <xsl:choose>
                       <xsl:when test="contains($PID, 'szd.glossar')">
                           <a href="{concat('/',$PID,'/ONTOLOGY')}" target="_blank">
                               <img alt="RDF" height="25" id="rdf" src="/templates/img/RDF_icon.png" title="RDF"/>
                           </a>
                       </xsl:when>
                       <xsl:otherwise>
                           <a href="{concat('/',$PID,'/TEI_SOURCE')}" target="_blank">
                               <img alt="TEI" height="25" id="tei" src="/templates/img/tei_icon.jpg" title="TEI"/>
                           </a>
                           <xsl:text> </xsl:text>
                           <a href="{concat('/',$PID,'/RDF')}"  target="_blank">
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
                                    <button type="button" class="btn pl-1 bg-white dropdown-toggle dropdown-toggle-split text-uppercase" data-toggle="dropdown">
                                        <xsl:value-of select="current-grouping-key()"/>
                                        <xsl:text> </xsl:text>
                                    </button>
                                    <div class="dropdown-menu scrollable-menu" role="menu">
                                        <xsl:for-each select="//skos:Concept[skos:broader/@rdf:resource = $currentRDFABOUT]">
                                            <xsl:sort select="skos:prefLabel[@xml:lang = $locale]"/>
                                            <button class="btn dropdown-item small text-uppercase" href="{concat('#',substring-after(@rdf:about, '#'))}" onclick="scrolldown(this)">
                                                <xsl:value-of select="skos:prefLabel[@xml:lang = $locale]"/>
                                            </button>
                                        </xsl:for-each>
                                    </div> 
                                </xsl:when>
                                <xsl:otherwise>
                                    <button  href="{concat('#',substring-after(../@rdf:about, '#'))}" class="btn pl-1 text-uppercase" onclick="scrolldown(this)">
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
                        <button type="button" class="btn btn-sm bg-white text-uppercase" href="{concat('#', translate(current-grouping-key(),' ',''))}" onclick="scrolldown(this)">
                            <xsl:value-of select="current-grouping-key()"/>
                        </button>
                    </div>
                </xsl:for-each-group>
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
                     </xsl:if>
                 </xsl:for-each>
                 <xsl:if test="not($PID = 'o:szd.personen') and not($PID = 'o:szd.autographen')">
                    <button type="button" class="btn btn-sm list-inline-item" href="#withoutAuthor" onclick="scrolldown(this)">
                        <xsl:choose>
                            <xsl:when test="$locale = 'en'">
                                <xsl:text>N.N.</xsl:text>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:text>o.V.</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
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
   <!-- <xsl:template name="filter">
        <xsl:param name="Filter_search"/>
        
    </xsl:template>-->
    
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- ///ADDDATA-DATABASKET -->
    <!-- Add the data- attributs, used for the databasket: Author or Editor, title and date -->
    <xsl:template name="AddData-Databasket">
        <xsl:param name="locale"/>
        <!--<xsl:attribute name="data-check">
            <xsl:text>unchecked</xsl:text>
        </xsl:attribute>-->
        <!-- URI -->
        <xsl:attribute name="data-uri">
            <xsl:choose>
                <xsl:when test="s:re/@uri">
                    <xsl:value-of select="s:re/@uri"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="normalize-space(concat('https://gams.uni-graz.at/', //t:publicationStmt/t:idno[@type='PID'], '#', @xml:id))"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:attribute>
        <!-- AUTHOR -->
        <xsl:choose>
            <xsl:when test="s:s">
                <xsl:attribute name="data-author">
                    <xsl:value-of select="normalize-space(s:s)"/>
                    <xsl:if test="s:f">
                        <xsl:text>, </xsl:text>
                        <xsl:value-of select="normalize-space(s:f)"/>
                    </xsl:if>
                </xsl:attribute>
            </xsl:when>
            <xsl:when test="t:fileDesc/t:titleStmt/t:author[1]">
                <xsl:attribute name="data-author">
                    <xsl:call-template name="printAuthor">
                        <xsl:with-param name="currentAuthor" select="t:fileDesc/t:titleStmt/t:author[1]"/>
                    </xsl:call-template>
                </xsl:attribute>
            </xsl:when>
           <xsl:otherwise/>
        </xsl:choose>
        <!-- COLLECTION -->
        <xsl:attribute name="data-collection">
            <!-- s:re/@uri for SEARCHRESULT -->
            <xsl:choose>
                <xsl:when test="contains(@xml:id | s:re/@uri, 'SZDMSK')">
                    <xsl:text>W</xsl:text>
                </xsl:when>
                <xsl:when test="contains(@xml:id | s:re/@uri, 'SZDLEB')">
                    <xsl:text>L</xsl:text>
                </xsl:when>
                <xsl:when test="contains(@xml:id | s:re/@uri, 'SZDAUT')">
                    <xsl:text>A</xsl:text>
                </xsl:when>
                <xsl:when test="contains(@xml:id | s:re/@uri, 'SZDBIB')">
                    <xsl:text>B</xsl:text>
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>
        </xsl:attribute>
        <!-- LOCATION -->
        <xsl:attribute name="data-location">
            <xsl:choose>
                <!-- SEARCH -->
                <xsl:when test="s:lo">
                    <xsl:call-template name="GetStandortList">
                        <xsl:with-param name="Standort" select="substring-after(s:lo/@uri, '#')"/>
                    </xsl:call-template>
                </xsl:when>
                <!-- SZDAUT -->
                <xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:orgName">
                    <xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:orgName[1])"/>
                </xsl:when>
                <!-- SZDMSK, SZDLEB -->
                <xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository">
                    <xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository)"/>
                </xsl:when>
                <!-- SZDBIB -->
                <xsl:otherwise>
                    <xsl:text> </xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:attribute>
        <!-- SIGNATURE -->
        <xsl:attribute name="data-signature">
            <xsl:choose>
                <!-- SEARCH -->
                <xsl:when test="s:si">
                    <xsl:value-of select="s:si"/>
                </xsl:when>
                <xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:idno">
                    <xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:idno)"/>
                </xsl:when>
                <xsl:when test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno">
                    <xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:choose>
                        <xsl:when test="s:re/@uri">
                            <xsl:value-of select="substring-after(s:re/@uri, '#')"/>
                        </xsl:when>
                    </xsl:choose>
                    <xsl:value-of select="@xml:id"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:attribute>
        <!-- TITEL -->
        <xsl:choose>
            <xsl:when test="s:t">
                <xsl:attribute name="data-title">
                    <xsl:value-of select="normalize-space(s:t)"/>
                </xsl:attribute>
            </xsl:when>
            <xsl:when test="t:fileDesc/t:titleStmt/t:title[1]">
                <xsl:attribute name="data-title">
                    <xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[1])"/>
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
	<!-- creates header of collection (o:szd.thema) -->
	<xsl:template name="getNavbar">
		<xsl:param name="Title"/>
		<xsl:param name="PID"/>
	    <xsl:param name="locale"/>
	    <xsl:param name="mode"/>
	    <xsl:param name="GlossarRef"/>
	        <!-- tei, rdf button -->
	    <div class="row mt-5">
	            <!-- creates language button DE | EN in the header -->
            <div class="col-2">
                <xsl:text> </xsl:text>
            </div>
	            <div class="col-8">
	            	<xsl:choose>
	            	    <xsl:when test="contains($PID, 'o:szd.thema')">
	            	        <img src="{concat('/', $PID, '/TITELBILD')}" class="img-fluid" alt="Titelbild"/> 
	            	    </xsl:when>
	            		<xsl:otherwise>
	            		    <h2>
	            		    <xsl:choose>
	            		        <xsl:when test="$GlossarRef">
	            		            <xsl:value-of select="upper-case($Title)"/>
	            		            <xsl:text> </xsl:text>
	            		            <a href="{concat('/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=', $locale, '#', $GlossarRef)}">
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
	            		        </xsl:when>
	            		        <xsl:otherwise>
	            		            <xsl:value-of select="upper-case($Title)"/>
	            		        </xsl:otherwise>
	            		    </xsl:choose>
	            		    </h2>
	            		</xsl:otherwise>
	            	</xsl:choose>
	            </div>
	            <!-- creates TEI and/or RDF BUtton on the right side in the header -->
     	        <div class="col-2 text-right">
     	                <xsl:if test="$PID">
     	                        <xsl:choose>
     	                            <!-- this skips TEI and RDF button -->
                	                    <xsl:when test="$PID = 'context:szd'"/>
                	                    <xsl:when test="contains($PID, 'o:szd.glossar') or contains($PID, 'o:szd.ontology')">
                	                        <a href="{concat('/', $PID,'/ONTOLOGY')}" role="button" target="_blank">
                	                            <img alt="RDF" height="25" id="rdf" src="/templates/img/RDF_icon.png" title="RDF"/>
                	                        </a>
                	                    </xsl:when>
     	                            <!-- TEI RDF Button in Search Result -->
     	                            <xsl:when test="$PID ='search'">
     	                               <xsl:text> </xsl:text>
     	                            </xsl:when>
                	                    <xsl:otherwise>
                	                        <a  href="{concat('/',$PID,'/TEI_SOURCE')}" role="button" target="_blank">
                	                            <img alt="TEI" height="25" id="tei" src="/templates/img/tei_icon.jpg" title="TEI"/>
                	                        </a>
                	                        <xsl:text> </xsl:text>
                	                        <a href="{concat('/',$PID,'/RDF')}" role="button" target="_blank">
                	                            <img alt="RDF" height="25" id="rdf" src="/templates/img/RDF_icon.png" title="RDF"/>
                	                        </a>
                	                    </xsl:otherwise>
         	                   </xsl:choose>
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
                 <xsl:if test="t:fileDesc/t:titleStmt/t:author[not(@role)]">
                 <tr class="row">
                       <td class="col-3 text-truncate">
                           <i18n:text>author_szd</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:fileDesc/t:titleStmt/t:author[not(@role)]">
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
                       <td class="col-3 text-truncate">
                           <i18n:text>composer</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:fileDesc/t:titleStmt/t:author[@role='composer']">
                            	<xsl:call-template name="PersonSearch">
                            	    <xsl:with-param name="locale" select="$locale"/>
                            	</xsl:call-template>
                            </xsl:for-each>
                        </td>
                    </tr>
                 </xsl:if>
                 <!-- //////////////////////////////////////////////////////////// -->
                 <!-- ///Herausgeber/// -->
                 <xsl:if test="t:fileDesc/t:titleStmt/t:editor[not(@role)]">
                    <tr class="row">
                        <td class="col-3 text-truncate">
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
                            	    <xsl:with-param name="locale" select="$locale"/>
                            	</xsl:call-template>
                            </xsl:for-each>
                        </td>
                    </tr>
                  </xsl:if>
                  <!-- //////////////////////////////////////////////////////////// -->
                  <!-- ///Illustrator/// -->
                  <xsl:if test="t:fileDesc/t:titleStmt/t:editor[@role='illustrator']">
                     <tr class="row">
                        <td class="col-3 text-truncate">
                            <i18n:text>illustrator</i18n:text>
                         </td>
                         <td class="col-9">
                             <xsl:for-each select="t:fileDesc/t:titleStmt/t:editor[@role='illustrator']">
                                 <xsl:call-template name="PersonSearch">
                                     <xsl:with-param name="locale" select="$locale"/>
                                 </xsl:call-template>
                             </xsl:for-each>
                         </td>
                     </tr>
                  </xsl:if>
                  <!-- //////////////////////////////////////////////////////////// -->
                  <!-- ///Übersetzer/// -->
                  <xsl:if test="t:fileDesc/t:titleStmt/t:editor[@role='translator']">
                     <tr class="row">
                       <td class="col-3 text-truncate">
                           <i18n:text>translator</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:fileDesc/t:titleStmt/t:editor[@role='translator']">
                                <xsl:call-template name="PersonSearch">
                                    <xsl:with-param name="locale" select="$locale"/>
                                </xsl:call-template>
                            </xsl:for-each>
                        </td>
                    </tr>
                 </xsl:if>
                 <!-- //////////////////////////////////////////////////////////// -->
                 <!-- ///Verfasser Vorwort/// -->
                 <xsl:if test="t:fileDesc/t:titleStmt/t:author[@role='preface']">
                     <tr class="row">
                       <td class="col-3 text-truncate">
                           <i18n:text>writerpreface</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:fileDesc/t:titleStmt/t:author[@role='preface']">
                                <xsl:call-template name="PersonSearch">
                                    <xsl:with-param name="locale" select="$locale"/>
                                </xsl:call-template>
                            </xsl:for-each>
                        </td>
                    </tr>
                 </xsl:if>
                 <!-- //////////////////////////////////////////////////////////// -->
                 <!-- ///Verfasser Nachwort/// -->
                 <xsl:if test="t:fileDesc/t:titleStmt/t:author[@role='afterword']">
                     <tr class="row">
                       <td class="col-3 text-truncate">
                           <i18n:text>writerafterword</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:for-each select="t:fileDesc/t:titleStmt/t:author[@role='afterword']">
                                <xsl:call-template name="PersonSearch">
                                    <xsl:with-param name="locale" select="$locale"/>
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
                       <td class="col-3 text-truncate">
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
                           <td class="col-3 text-truncate">
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
                        <td class="col-3 text-truncate">
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
    	                       <td class="col-3 text-truncate">
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
                           <td class="col-3 text-truncate">
                               <i18n:text>language</i18n:text>
                            </td>
                            <td class="col-9">
                                <xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang/t:lang">
                                    <xsl:call-template name="languageCode">
                                        <xsl:with-param name="Current" select="@xml:lang"/>
                                        <xsl:with-param name="locale" select="$locale"/>
                                    </xsl:call-template>
                                    <xsl:if test="not(position()=last())">
                                        <xsl:text>, </xsl:text>
                                    </xsl:if>
                                   	<!--<xsl:choose>
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
                                   	</xsl:choose>-->
                           </xsl:for-each>
                        </td>
                        </tr>
                     </xsl:if>
    			 	  <!-- //////////////////////////////////////////////////////////// -->
                      <!-- ///UMFANG/// -->
    			     <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc">
    			         <tr class="row group_btm">
                             <td class="col-3 text-truncate">
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
                         <tr class="row group">
                           <td class="col-3 text-truncate">
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
                           <td class="col-3 text-truncate">
                               <i18n:text>comment</i18n:text>
                            </td>
                            <td class="col-9">
                                <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:msItem/t:note"/>
                            </td>
                        </tr>
                     </xsl:if>
                         <!-- //////////////////////////////////////////////////////////// --> 
    				 	<!-- ///Provenienzkriterien/// -->
                    <xsl:variable name="Provenance" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='provenance']/t:item[not(t:stamp)]"/>
                    <xsl:for-each select="$Provenance">
                              <tr class="row">
                                  <xsl:if test="position() = 1">
                                      <xsl:attribute name="class" select="'group row'"/>
                                  </xsl:if>
                               <td class="col-3 text-truncate">
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
    				     <xsl:for-each select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:additions/t:list[@type='provenance']/t:item[t:stamp]">
    				         <tr class="row">
    				             <xsl:if test="position() = 1 and not($Provenance)">
    				                 <xsl:attribute name="class" select="'group row'"/>
    				             </xsl:if>
    				             <td class="col-3 text-truncate">
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
    	                       <td class="col-3 text-truncate">
    	                           <a href="{concat('/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=', $locale, '#OriginalShelfmark')}" target="_blank">
    	                                <i18n:text>originalshelfmark</i18n:text>
    	                        		<i class="fa fa-info-circle info_icon" aria-hidden="true"><xsl:text> </xsl:text></i>
    	                        	</a>
    	                        </td>
                                   <td class="col-9">
                                       <!--<xsl:call-template name="Originalsignaturen"/>-->
                                       <div class="row" style="margin-top: 0px; margin-left:-15px;">
                                           <xsl:for-each-group select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:altIdentifier" group-by="@corresp">
                                               <xsl:choose>
                                                   <xsl:when test="current-grouping-key() = 'https://gams.uni-graz.at/o:szd.glossar#InventoryNumberOld'">
                                                       <xsl:for-each select="current-group()">
                                                           <xsl:if test="@n=1 and not(position()=1)">
                                                               <br/>
                                                           </xsl:if>
                                                           <span class="col-4">
                                                               <xsl:value-of select="normalize-space(.)"/>
                                                               <xsl:text> </xsl:text>
                                                           </span>
                                                           
                                                       </xsl:for-each>
                                                   </xsl:when>
                                                   <xsl:otherwise>
                                                       <xsl:for-each select="current-group()">
                                                       <span class="col-12">
                                                           <xsl:value-of select="normalize-space(.)"/>
                                                          
                                                       </span>
                                                          
                                                       </xsl:for-each>
                                                   </xsl:otherwise>
                                               </xsl:choose>
                                             
                                               <br/>
                                               
                                                  <!-- <xsl:for-each select="current-group()">
                                                   
                                                       <div class="col-3">
                                                           <span><xsl:value-of select="normalize-space(.)"/></span>
                                                       </div>
                                                       
                                                   </xsl:for-each>-->
                                               
                                               <!--<xsl:for-each select="current-group()">
                                                   <div class="col-3">
                                               	        <span><xsl:value-of select="normalize-space(.)"/></span>
                                                   </div>
                                                   <xsl:if test="@n=1">
                                                      <p><xsl:text>a</xsl:text></p>
                                                   </xsl:if>
                                               </xsl:for-each>-->
                                           </xsl:for-each-group>
                                           </div>
                                  </td>
                              </tr>
                          </xsl:if>
                        <!-- //////////////////////////////////////////////////////////// -->
                        <!-- ///Provenienz/// -->
                        <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance">
                            <tr class="row group">
                                <td class="col-3 text-truncate">
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
    				         <tr class="row"> 
    				             <xsl:if test="not(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance)">
    				                 <xsl:attribute name="class"><xsl:text>group row</xsl:text></xsl:attribute>
    				             </xsl:if>
    				             <!-- <xsl:if test="not(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance)">
                                      <xsl:attribute name="class" select="'group'"/>
                                  </xsl:if> -->
                                 <td class="col-3 text-truncate">
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
              <xsl:if test="t:fileDesc/t:titleStmt/t:author[not(@role)]">
                  <xsl:for-each select="t:fileDesc/t:titleStmt/t:author[not(@role)]">
                      <xsl:call-template name="printAuthor">
                          <xsl:with-param name="currentAuthor" select="."/>
                      </xsl:call-template>
                      <xsl:if test="not(position()=last())">
                        <xsl:text> / </xsl:text>
                      </xsl:if>
                  </xsl:for-each>
              	 <xsl:text>: </xsl:text>
              </xsl:if>	
              <xsl:if test="t:fileDesc/t:titleStmt/t:author[@role='composer']">
                  <xsl:for-each select="t:fileDesc/t:titleStmt/t:author[@role='composer']">
                      <xsl:call-template name="printAuthor">
                          <xsl:with-param name="currentAuthor" select="."/>
                      </xsl:call-template>
                      <xsl:if test="not(position()=last())">
                          <xsl:text> / </xsl:text>
                      </xsl:if>
                  </xsl:for-each>  
              	 <xsl:text>: </xsl:text>
              </xsl:if>
                <!-- e.g. Geheimnis des Alcovens -->
               <span class="font-italic">
                    <xsl:call-template name="printEnDe">
                        <xsl:with-param name="locale" select="$locale"/>
                        <!-- bibliothek, werke, autograph immer erster titel? -->
                        <xsl:with-param name="path">
                            <xsl:choose>
                                <xsl:when test="t:fileDesc/t:titleStmt/t:title/@xml:lang">
                                    <xsl:value-of select="t:fileDesc/t:titleStmt/t:title[@xml:lang  = $locale][1]"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="t:fileDesc/t:titleStmt/t:title[1]"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:with-param>
                    </xsl:call-template>
                   <xsl:text> </xsl:text>
               </span>
                <!-- Herausgeber -->
                <xsl:if test="t:fileDesc/t:titleStmt/t:editor[not(@role)]">
                    <xsl:text> (</xsl:text>
                    <i18n:text>Hrsg.</i18n:text>
                    <xsl:text> </xsl:text>
                    <xsl:for-each select="t:fileDesc/t:titleStmt/t:editor">
                        <xsl:value-of select="."/>
                        <xsl:if test="not(last()=position())">
                            <xsl:text> / </xsl:text>
                        </xsl:if>
                    </xsl:for-each>
                    <xsl:text>)</xsl:text>
                </xsl:if>	
                <!-- Ordnugnskategorie -->
                <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:span[@xml:lang = $locale]/t:term[@type='objecttyp']">
                    <xsl:text>, </xsl:text>
                    <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:span[@xml:lang = $locale]/t:term[@type='objecttyp']"/>
                </xsl:if>
               <!-- e.g. [Marie Antoinette] -->
                <xsl:if test="t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel'][1]">
	              <xsl:text> [</xsl:text>
                    <xsl:call-template name="printEnDe">
                        <xsl:with-param name="locale" select="$locale"/>
                        <xsl:with-param name="path" select="t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel']"/>
                    </xsl:call-template>
	              <xsl:text>]</xsl:text>
               </xsl:if>
               <xsl:text>. </xsl:text>
                <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository">
                    <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:repository"/>
                    <xsl:text>, </xsl:text>
                </xsl:if>
                <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno">
                    <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno"/>
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
			<xsl:when test="t:persName/@ref">
			    <xsl:variable name="REF" select="t:persName/@ref"/>
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
            <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:settlement">
                <xsl:text>, </xsl:text>
                <xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:settlement)"/>
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
                    <td class="col-3 text-truncate">
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
                          <td class="col-3 text-truncate">
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
                    <td class="col-3 text-truncate">
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
                          <td class="col-3 text-truncate">
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
                            <td class="col-3 text-truncate">
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
                          <td class="col-3 text-truncate">
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
                      <td class="col-3 text-truncate">
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
                          <td class="col-3 text-truncate">
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
                           <td class="col-3 text-truncate">
                              <!-- SZDMSK -->
                              <a href="{concat('/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=', $locale, '#PhysicalDescription')}" target="_blank">
                                  <i18n:text>physicaldescription</i18n:text>
                                  <i class="fa fa-info-circle info_icon" aria-hidden="true"><xsl:text> </xsl:text></i>
                              </a>
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
                          <td class="col-3 text-truncate">
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
                          <td class="col-3 text-truncate">
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
                          <td class="col-3 text-truncate">
                              <i18n:text>secretarialhand</i18n:text>
                           </td>
                           <td class="col-9">
                               <xsl:call-template name="printEnDe">
                                   <xsl:with-param name="locale" select="$locale"/>
                                   <xsl:with-param name="path" select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:handDesc/t:ab"/>
                               </xsl:call-template>
                           </td>
                       </tr>
                   </xsl:if>
                  <!-- //////////////////////////////////////////////////////////// -->
                  <!-- Hinweise -->
	              <xsl:if test="t:fileDesc/t:notesStmt/t:note">
                    <tr class="row">
                      <td class="col-3 text-truncate">
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
                          <td class="col-3 text-truncate">
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
                      <td class="col-3 text-truncate">
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
                          <td class="col-3 text-truncate">
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
                          <td class="col-3 text-truncate">
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
                          <td class="col-3 text-truncate">
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
    <!-- autohraph collection biblFull Entry: o:szd.autographen -->
    <xsl:template name="FillbiblFull_SZDAUT">
        <xsl:param name="locale"/>
        <div class="table-responsive">
        <table class="table table-sm">
            <tbody>
                <!-- ///Verfasser/// -->
                <xsl:if test="t:fileDesc/t:titleStmt/t:author[1][not(@role)]">
                    <tr class="row">
                        <td class="col-3 text-truncate">
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
                        <td class="col-3 text-truncate">
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
                        <td class="col-3 text-truncate">
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
                        <td class="col-3 text-truncate">
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
                        <td class="col-3 text-truncate">
                            <i18n:text>Titel</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:choose>
                                <xsl:when test="t:fileDesc/t:titleStmt/t:title/@ref">
                                    <a href="{t:fileDesc/t:titleStmt/t:title/@ref}" target="_blank">
                                        <xsl:attribute name="title">
                                            <xsl:choose>
                                                <xsl:when test="$locale ='en'">
                                                    <xsl:text>Access externally sourced digital facsimile</xsl:text>
                                                </xsl:when>
                                                <xsl:otherwise><xsl:text>Zur externen Ressource mit digitalem Faksimile</xsl:text></xsl:otherwise>
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
                        <td class="col-3 text-truncate">
                            <i18n:text>description</i18n:text>
                        </td>
                        <td class="col-9">
                            <!--<xsl:call-template name="printEnDe">
                                <xsl:with-param name="locale" select="$locale"/>
                                <xsl:with-param name="path" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary"/>
                            </xsl:call-template>-->
                            <xsl:apply-templates select="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:summary"/>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msContents/t:textLang/t:lang">
                    <tr class="row">
                        <td class="col-3 text-truncate">
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
                        <td class="col-3 text-truncate">
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
                <!-- ///Provenienz/// -->
                <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance[@type='provenance']">
                    <tr class="row group">
          
                        <td class="col-3 text-truncate">
                            <i18n:text>provenance</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance[@type='provenance']"/>
                        </td>
                    </tr>
                </xsl:if>

                <!-- //////////////////////////////////////////////////////////// -->
                <!-- ////// -->
                <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition">
                    <tr class="row">
                        <xsl:if test="not(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance[@type='provenance'])">
                            <xsl:attribute name="class"><xsl:text>row group</xsl:text></xsl:attribute>
                        </xsl:if>
                        <td class="col-3 text-truncate">
                            <i18n:text>acquired</i18n:text>
                        </td>
                        <td class="col-9">
                            <xsl:value-of select="normalize-space(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition)"/>
                            <!--<xsl:apply-templates select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition"/>-->
                        </td>
                    </tr>
                </xsl:if>
         
                <!-- //////////////////////////////////////////////////////////// -->
                <!-- Current Location  -->
                <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance[not(@type)]">
                    <tr class="row">
                        <xsl:if test="not(t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:acquisition)">
                            <xsl:attribute name="class"><xsl:text>group row</xsl:text></xsl:attribute>
                        </xsl:if>
                       
                        <td class="col-3 text-truncate">
                            <i18n:text>currentlocation</i18n:text>
                        </td>
                        <td class="col-9">
                            <!--<xsl:value-of select="t:sourceDesc/t:msDesc/t:history/t:provenance"/>-->
                            <xsl:apply-templates select="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance[not(@type)]">
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
        <br/>
        <xsl:text> </xsl:text>
    </xsl:template>
    
    <!-- //////////////////////////////////////////////////////////// -->
    <!-- for o:szd.autographs -->
    <xsl:template match="t:fileDesc/t:sourceDesc/t:msDesc/t:history/t:provenance/t:idno[@type='signature']">
        <xsl:apply-templates/>
    </xsl:template>

    <!-- /////////////////////////////////////////////////////////// --> 
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
    
    <!-- ///////////////////////////////////////////////////// -->
    <!-- check box for databasket --> 
    <xsl:template name="getLabelDatabasket">
        <xsl:param name="locale"/>
        <xsl:param name="SZDID"/>
        <xsl:variable name="databasketParam">
            <xsl:choose>
                <xsl:when test="$SZDID">
                    <xsl:value-of select="concat('&quot;',$SZDID, '&quot;')"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>this</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <label class="col text-right">
            <input  onClick="add_DB({$databasketParam})" type="checkbox" class="form-check-input">
                <xsl:choose>
                    <xsl:when test="$locale = 'en'">
                        <xsl:attribute name="title" select="'Save to data cart'"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:attribute name="title" select="'Im Datenkorb ablegen'"/>
                    </xsl:otherwise>
                </xsl:choose>
            </input>
        </label>
    </xsl:template>
    
    <!-- ///////////////////////////////////////////////////// -->
    <!-- defines the headings of the entries: author - title - references -->
    <xsl:template name="getEntry_SZDBIB_SZDAUT">
        <xsl:param name="locale"/>
        <xsl:param name="PID"/>
            <!-- data-basket -->
            <xsl:call-template name="AddData-Databasket"/>
            <div class="bg-light row">
                <h4 class="card-title text-left col-9 small">
                    <a data-toggle="collapse" href="{concat('#c' , generate-id())}">
                        <span class="arrow">
                            <xsl:text>&#9660; </xsl:text>
                        </span>
                        <xsl:choose>
                            <!-- every title in o:szd.bibliothek is italic-->
                            <xsl:when test="$PID = 'o:szd.bibliothek'">
                                <xsl:choose>
                                    <xsl:when test="string-length(t:fileDesc/t:titleStmt/t:title[1]) > 70">
                                        <i><xsl:value-of select="normalize-space(substring(t:fileDesc/t:titleStmt/t:title[1], 1, 70))"/><xsl:text>... </xsl:text></i>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <i><xsl:value-of select="normalize-space(t:fileDesc/t:titleStmt/t:title[1])"/></i>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <!-- for mixed content with <hi class="italic"> -->
                            <xsl:otherwise>
                                <xsl:apply-templates select="t:fileDesc/t:titleStmt/t:title[1]"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </a>
                    <xsl:if test="t:fileDesc/t:publicationStmt/t:date">
                        <xsl:text> | </xsl:text><xsl:value-of select="t:fileDesc/t:publicationStmt/t:date"/>
                    </xsl:if>
                </h4>
                
                <xsl:choose>
                    <xsl:when test="t:fileDesc/t:titleStmt/t:title/@ref">
                        <a href="{t:fileDesc/t:titleStmt/t:title/@ref}" target="_blank" class="col-1">
                            <xsl:attribute name="title">
                                <xsl:choose>
                                    <xsl:when test="$locale ='en'">
                                        <xsl:text>Access externally sourced digital facsimile</xsl:text>
                                    </xsl:when>
                                    <xsl:otherwise><xsl:text>Zur externen Ressource mit digitalem Faksimile</xsl:text></xsl:otherwise>
                                </xsl:choose>
                            </xsl:attribute>
                            <xsl:text> </xsl:text>
                            <i class="fas fa-external-link-alt _icon small pl-1"><xsl:text> </xsl:text></i>
                        </a>
                    </xsl:when>
                    <xsl:otherwise>
                    </xsl:otherwise>
                </xsl:choose>                
                <!-- checkbox databasket -->
                <xsl:call-template name="getLabelDatabasket">
                    <xsl:with-param name="locale" select="$locale"/>
                    <xsl:with-param name="SZDID" select="@xml:id"/>
                </xsl:call-template>
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
                        <xsl:value-of select="$currentAuthor/t:surname"/>
                        <xsl:if test="$currentAuthor/t:forename">
                            <xsl:text>, </xsl:text>
                            <xsl:value-of select="$currentAuthor/t:forename"/>
                        </xsl:if>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="normalize-space($currentAuthor)"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>Error in call-template "printAuthor"!</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!-- /////////////////////// -->
    <!-- gets the position of the first person of each char; ABC - Navigation in getstickyNav -->
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