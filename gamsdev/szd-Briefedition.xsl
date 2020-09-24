<?xml version="1.0" encoding="UTF-8"?>
<!-- 
    Project: GAMS Projekttemplate
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
 -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:i18n="http://apache.org/cocoon/i18n/2.1"
    xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:lido="http://www.lido-schema.org" xmlns:oai="http://www.openarchives.org/OAI/2.0/" exclude-result-prefixes="#all">

    <xsl:include href="szd-static.xsl"/>
    <xsl:include href="szd-Templates.xsl"/>
    <!--<xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>-->
    
  

    <xsl:template name="content">
        <!--für den edition viewer wird das hier eingebunden. bilder müssen im TEI und als datenströme vorhanden sein und ein METS erstellt worden sein. -->
        <xsl:if test="$mode = 'view:editionobject' or $mode=''">
            <div class="col-sm-12">  
                <xsl:call-template name="getNavbar">
                    <xsl:with-param name="Title" select="'Briefedition'"/>
                    <xsl:with-param name="PID" select="$PID"/>
                    <xsl:with-param name="locale" select="$locale"/>
                </xsl:call-template>
            </div>
            <!-- /// PAGE-CONTENT /// -->
            <div class="card">
                <div class="card-body" id="content">	
                        <!-- ////////////////////////////////////////////// -->
                        <!-- t:correspAction -->
                        <!-- //////////////////////////////////////////////////////////// -->
                        <!-- TITLE -->
                    
                        <xsl:variable name="SENT" select="//t:correspAction[@type = 'sent']"/>
                        <xsl:variable name="RECIEVED" select="//t:correspAction[@type = 'received']"/>
                    
                        <div class="list-group mt-4 small ml-2 mr-2">
                            <div class="list-group-item entry db_entry shadow-sm" id="{@xml:id}">
                                <div class="bg-light row">
                                    <h4 class="card-title text-left col-8">
                                         <a data-toggle="collapse" href="{concat('#c' , generate-id())}">
                                             <span class="arrow">
                                                 <xsl:text>▼ </xsl:text>
                                             </span>
                                             <xsl:apply-templates select="//t:fileDesc/t:titleStmt/t:title"/>
                                             <xsl:text> | </xsl:text>
                                             <xsl:value-of select="$SENT/t:date"/>
                                         </a>
                                    </h4>
                                    <span class="col-2 text-center">
                                        <a href="{concat('/archive/objects/', $PID, '/methods/sdef:IIIF/getMirador')}" target="_blank">
                                            <xsl:attribute name="title">
                                                <xsl:choose>
                                                    <xsl:when test="$locale ='en'">
                                                        <!--<xsl:text>Access externally sourced digital facsimile</xsl:text>-->
                                                        <xsl:text>Image</xsl:text>
                                                    </xsl:when>
                                                    <xsl:otherwise>
                                                        <!--<xsl:text>Zur externen Ressource mit digitalem Faksimile</xsl:text>-->
                                                        <xsl:text>Abbildung</xsl:text>
                                                    </xsl:otherwise>
                                                </xsl:choose>
                                            </xsl:attribute>
                                            <xsl:call-template name="printCameraIcon">
                                                <xsl:with-param name="locale" select="$locale"/>
                                            </xsl:call-template>
                                        </a>
                                    </span>
                                    <!-- checkbox databasket -->
                                    <xsl:call-template name="getLabelDatabasket">
                                        <xsl:with-param name="locale" select="$locale"/>
                                        <xsl:with-param name="SZDID" select="@xml:id"/>
                                    </xsl:call-template>
                                </div>
                                <div class="card-body card-collapse collapse" id="{concat('c' , generate-id())}">
                                    <div class="table-responsive">	    
                                        <table class="table table-sm">
                                            <tbody>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <!-- sent -->
                                                <xsl:if test="$SENT">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Verfasser/in</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:for-each select="$SENT/t:persName">
                                                                <xsl:call-template name="PersonSearch">
                                                                    <xsl:with-param name="locale" select="$locale"/>
                                                                </xsl:call-template>
                                                            </xsl:for-each>
                                                           <!--<xsl:value-of select="$SENT/t:persName/t:surname"/>
                                                           <xsl:text>, </xsl:text>
                                                           <xsl:value-of select="$SENT/t:persName/t:forename"/>-->
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <!-- received -->
                                                <xsl:if test="$RECIEVED">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Adressat/in</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:for-each select="$RECIEVED/t:persName">
                                                                <xsl:call-template name="PersonSearch">
                                                                    <xsl:with-param name="locale" select="$locale"/>
                                                                </xsl:call-template>
                                                            </xsl:for-each>
                                                           <!-- <xsl:value-of select="$RECIEVED/t:persName/t:surname"/>
                                                            <xsl:text>, </xsl:text>
                                                            <xsl:value-of select="$RECIEVED/t:persName/t:forename"/>-->
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <xsl:if test="$SENT/t:date">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Datierung</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="$SENT/t:date"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <xsl:if test="//t:correspDesc/t:note/t:stamp">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Poststempel</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="//t:correspDesc/t:note/t:stamp"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <xsl:if test="$SENT/t:placeName">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Entstehungsort</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="$SENT/t:placeName"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <xsl:if test="$RECIEVED/t:placeName">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Empfangsort</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="$RECIEVED/t:placeName"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <xsl:if test="//t:physDesc/t:objectDesc/t:supportDesc/t:extent">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Art/Umfang</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="//t:physDesc/t:objectDesc/t:supportDesc/t:extent"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <xsl:if test="//t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Schreibstoff</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="//t:physDesc/t:objectDesc/t:supportDesc/t:support/t:material"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <xsl:if test="//t:physDesc/t:handDesc">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Schreiberhand</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="//t:physDesc/t:handDesc"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <xsl:if test="//t:history/t:provenance">
                                                    <tr class="group row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Provenienz</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="//t:history/t:provenance"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <xsl:if test="//t:history/t:acquisition">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Erwerbung</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="//t:history/t:acquisition"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <tr class="row">
                                                    <td class="col-3 text-truncate">
                                                        <i18n:text>currentlocation</i18n:text>
                                                    </td>
                                                    <td class="col-9">
                                                        <xsl:call-template name="LocationSearch">
                                                            <xsl:with-param name="locale" select="$locale"/>
                                                            <xsl:with-param name="SZDSTA">
                                                                <xsl:call-template name="GetStandortList">
                                                                    <xsl:with-param name="Standort">
                                                                        <xsl:value-of select="//t:msDesc/t:msIdentifier/t:repository/@ref"/>
                                                                    </xsl:with-param>
                                                                </xsl:call-template>
                                                            </xsl:with-param>
                                                        </xsl:call-template>
                                                      <!--  <xsl:call-template name="printEnDe">
                                                            <xsl:with-param name="locale" select="$locale"/>
                                                            <xsl:with-param name="path" select="//t:msDesc/t:msIdentifier/t:repository"/>
                                                        </xsl:call-template>-->
                                                        <br/>
                                                        <xsl:value-of select="//t:msDesc/t:msIdentifier/t:idno"/>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    <!-- FOOTER -->
                                    <xsl:call-template name="getFooter">
                                        <xsl:with-param name="locale" select="$locale"/>
                                        <xsl:with-param name="PID" select="$PID"/>
                                        <xsl:with-param name="Type" select="'SZDBRI'"/>
                                        <xsl:with-param name="SENT" select="$SENT"/>
                                        <xsl:with-param name="RECIEVED" select="$RECIEVED"/>
                                        <xsl:with-param name="TITLE" select="//t:fileDesc/t:titleStmt/t:title"/>
                                    </xsl:call-template>
                                </div>
                            </div>
                        </div>
                <!--</div>-->
                
                <!-- ///////////////////// -->
                <!-- DETAIL-VIEW -->
                <div class="row">                                    
                <div class="col-sm-6">  
                    <div class="card-body small">
                        <xsl:apply-templates select="//t:body"/>
                    </div>
                </div>
                <div class="col-sm-6 mt-3">
                    <div class="sticky-top" style="top:80px; z-index:100;">
                        <div id="vwr-content" class="toc"
                            style="background-color: #E8E8E8; height:700px;" >
                            <xsl:text> </xsl:text>    
                        </div>
                        <xsl:variable name="Desc" select="t:TEI/t:teiHeader/t:fileDesc/t:sourceDesc/t:msDesc"/>
                       <!-- <div class="card-footer">
                            <xsl:apply-templates select="$Desc/t:msIdentifier/t:settlement"/>
                            <xsl:text>, </xsl:text>
                            <xsl:value-of select="$Desc/t:msIdentifier/t:institution"/>
                            <xsl:if test="$Desc/t:msIdentifier/t:repository">
                                <xsl:text>, </xsl:text>
                                <xsl:value-of select="$Desc/t:msIdentifier/t:repository"/>
                            </xsl:if><xsl:text>, </xsl:text>
                            <xsl:value-of select="$Desc/t:msIdentifier/t:idno"/>
                        </div>-->
                    </div>
                    
                    <!-- SCRIPTS - VIEWER -->
                    <script type="text/javascript" src="/editionviewer/openseadragon.js"><xsl:text> </xsl:text></script>
                    <script type="text/javascript" src="/editionviewer/bs-scroll-the-edition.js"><xsl:text> </xsl:text></script>
                    <script type="text/javascript" src="/editionviewer/gamsEdition.js"><xsl:text> </xsl:text></script>
                    <script type="text/javascript">
                        gamsOsd({
                        id: "vwr-content",
                        prefixUrl: "/osdviewer/images/",
                        showNavigator: false,
                        sequenceMode: true,
                        initialPage: 1,
                        defaultZoomLevel:   0,
                        showSequenceControl: true,
                        showReferenceStrip: false,
                        showRotationControl: false,
                        referenceStripScroll: "horizontal",
                        pid:"<xsl:value-of select="concat('/',$PID)"/>"
                        });
                    </script>
                </div>
                    <!-- //////////////////////////////////////////////////////////// -->
                    <xsl:if test="//t:note[@type='footnote'][1]">
                      
                        <xsl:call-template name="createFootnote">
                            <xsl:with-param name="locale" select="$locale"/>
                        </xsl:call-template>
                    </xsl:if>
            </div>
                
            </div></div>
        </xsl:if>
    </xsl:template>
    
    <!-- prototyp -->
    <xsl:template match="t:fw">
        <p class="text-center">
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    
    
    <xsl:template match="t:opener/t:dateline">
        <h3>
            <xsl:apply-templates/>
        </h3>
    </xsl:template>
    
    <xsl:template match="t:salute">
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    
    <xsl:template match="t:note">
        <i class="fa fa-info-circle info_icon">
            <xsl:attribute name="title" select="normalize-space(.)"/>
            <xsl:text> </xsl:text>
        </i>
    </xsl:template>
    
    
    
    
    
    <!--################Ab hier für Edition Viewer relevant######################-->
    <!-- Seitenumbruch kennzeichnen, Seitenzahl auslesen, Folio auslesen -->
    <xsl:template match="t:pb">
        <span class="page mt-5 mb-5" level="{@xml:id}" id="{@xml:id}">
            <span class="pageNumber">
                <xsl:call-template name="pageNumber">
                    <xsl:with-param name="number" select="@n"/>
                </xsl:call-template>
            </span>
        </span> 
    </xsl:template>
    <xsl:template name="pageNumber">
        <xsl:param name="number"/>
        <xsl:choose>
            <xsl:when test="starts-with($number, '0')">
                <xsl:variable name="saveNumber" select="substring-after($number, '0')"/>
                <xsl:call-template name="pageNumber">
                    <xsl:with-param name="number" select="$saveNumber"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <b>
                    <xsl:text>[</xsl:text>
                    <xsl:value-of select="$number"/>
                    <xsl:text>]</xsl:text>
                </b>
            </xsl:otherwise>
            
        </xsl:choose>
    </xsl:template>
    <xsl:template match="t:lb[@n]">  
        <!-- Zeilennummern schreiben  -->   
        <xsl:if test="not(@n='N001')"><br/></xsl:if><span class="bold"><xsl:value-of select="substring-after(@n,'N0')"/><xsl:text>: </xsl:text></span>
        <xsl:apply-templates/>
    </xsl:template> 
    <xsl:template match="t:lb[not(@n)]">    
        <br/>       
    </xsl:template>
   <!-- ################ END Edition Viewer ################-->
    
    

</xsl:stylesheet>
