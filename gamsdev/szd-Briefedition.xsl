<?xml version="1.0" encoding="UTF-8"?>
<!-- 
    Project: GAMS Projekttemplate
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
 -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
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
                <!--<div class="card-body">-->
                    <!--
                        <a rel="nofollow" href="{concat('/', $PID, '/TEI_SOURCE')}" target="_blank">
                            <xsl:text>TEI Source </xsl:text>
                            <img alt="TEI" height="25" src="/templates/img/tei_icon.jpg"
                                title="TEI"/>
                        </a>
                        <br/>
                        <a href="{concat('/archive/objects/', $PID, '/TEI_SOURCE/methods/sdef:dfgMETS/vget')}" target="_blank">
                            <xsl:text>Viewer </xsl:text>
                            <span class="oi oi-external-link"><xsl:text> </xsl:text></span>
                        </a>
                        <br/>
                       
                        <a>
                            <xsl:attribute name="href">
                                <xsl:value-of
                                    select="substring-after(//t:keywords[@ana = 'correspondence']/t:list/t:item[1]/t:ref/@target, 'info:fedora')"
                                />
                            </xsl:attribute>
                            
                            <xsl:text> Gesamtkorrespondenz </xsl:text>
                            <span class="oi oi-envelope-closed">
                                <xsl:text> </xsl:text>
                            </span>
                        </a>
                        <div id="csLink" data-correspondent-2-name="" data-end-date=""
                            data-range="30000" data-selection-when="before-after"
                            data-selection-span="median-before-after"
                            data-result-max="4" data-exclude-edition="">
                            
                            <xsl:attribute name="data-correspondent-1-id">
                                <xsl:value-of
                                    select="$SENT/t:persName/@ref"
                                />
                            </xsl:attribute>
                            
                            <xsl:attribute name="data-correspondent-1-name">
                                <xsl:value-of
                                    select="concat($SENT/t:persName/t:forename, ' ', $SENT/t:persName/t:surname)"
                                />
                            </xsl:attribute>
                            
                            <xsl:attribute name="data-correspondent-2-id">
                                <xsl:value-of
                                    select="$RECIEVED/t:persName/@ref"
                                />
                            </xsl:attribute>
                            
                            <xsl:attribute name="data-correspondent-2-name">
                                <xsl:value-of
                                    select="concat($RECIEVED/t:persName/t:forename, ' ', $RECIEVED/t:persName/t:surname)"
                                />
                            </xsl:attribute>
                            
                            <xsl:attribute name="data-start-date">
                                <xsl:value-of
                                    select="$SENT/t:date/@when"
                                />
                            </xsl:attribute>
                            
                            
                            
                            <xsl:text> </xsl:text>
                        </div>
                        
                        
                        <script type="text/javascript" src="//glossa.uni-graz.at/gamsdev/steineel/hsa/js/cslink.js"><xsl:text> </xsl:text>
                        </script>-->
                        
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
                                             <xsl:apply-templates select="//t:fileDesc/t:titleStmt/t:title"/>
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
                                <div class="card-body small">
                                    <div class="table-responsive">	    
                                        <table class="table table-sm">
                                            <tbody>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <!-- sent -->
                                                <xsl:if test="$SENT">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Sender</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                           <xsl:value-of select="$SENT/t:persName/t:surname"/>
                                                           <xsl:text>, </xsl:text>
                                                           <xsl:value-of select="$SENT/t:persName/t:forename"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <!-- received -->
                                                <xsl:if test="$RECIEVED">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Empfänger</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="$RECIEVED/t:persName/t:surname"/>
                                                            <xsl:text>, </xsl:text>
                                                            <xsl:value-of select="$RECIEVED/t:persName/t:forename"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <!-- send-date -->
                                                <xsl:if test="$SENT/t:date">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Sendedatum</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="$SENT/t:date"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <!-- send-date -->
                                                <xsl:if test="$RECIEVED/t:date">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Empfangsdatum</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="$RECIEVED/t:date"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <!-- send-place -->
                                                <xsl:if test="$SENT/t:settlement">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Sendeort</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="$SENT/t:settlement"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                                <!-- //////////////////////////////////////////////////////////// -->
                                                <!-- send-date -->
                                                <xsl:if test="$RECIEVED/t:settlement">
                                                    <tr class="row">
                                                        <td class="col-3 text-truncate">
                                                            <xsl:text>Empfangsort</xsl:text>
                                                        </td>
                                                        <td class="col-9">
                                                            <xsl:value-of select="$RECIEVED/t:settlement"/>
                                                        </td>
                                                    </tr>
                                                </xsl:if>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                                <!-- FOOTER -->
                                <xsl:call-template name="getFooter">
                                    <xsl:with-param name="locale" select="$locale"/>
                                    <xsl:with-param name="PID" select="$PID"/>
                                    <xsl:with-param name="Type" select="'SZDBRI'"/>
                                    <xsl:with-param name="SENT" select="$SENT"/>
                                    <xsl:with-param name="RECIEVED" select="$RECIEVED"/>
                                </xsl:call-template> 
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
                        <div class="card-footer">
                            <xsl:apply-templates select="$Desc/t:msIdentifier/t:settlement"/>
                            <xsl:text>, </xsl:text>
                            <xsl:value-of select="$Desc/t:msIdentifier/t:institution"/>
                            <xsl:if test="$Desc/t:msIdentifier/t:repository">
                                <xsl:text>, </xsl:text>
                                <xsl:value-of select="$Desc/t:msIdentifier/t:repository"/>
                            </xsl:if><xsl:text>, </xsl:text>
                            <xsl:value-of select="$Desc/t:msIdentifier/t:idno"/>
                        </div>
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
    
    
    <xsl:template match="t:opener/t:dateline">
        <h3>
            <xsl:apply-templates></xsl:apply-templates>
        </h3>
    </xsl:template>
    
    <xsl:template match="t:salute">
        <p>
            <xsl:apply-templates></xsl:apply-templates>
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
