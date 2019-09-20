<?xml version="1.0" encoding="UTF-8"?>

<!-- 
    Project: Stefan Zweig Digital
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
    		 Literaturarchiv Salzburg	
    Author: Christopher Pollin
    Last update: 2017
 -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:i18n="http://apache.org/cocoon/i18n/2.1"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    exclude-result-prefixes="#all">

    <xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>


    <xsl:include href="szd-static.xsl"/>
    <xsl:include href="szd-Templates.xsl"/>


    <!-- ///CONTENT/// -->
    <!-- called in szd-static.xsl -->
    <xsl:template name="content">
        
        <!-- CHOOSE MODE, param in URL-->
        <xsl:choose>
            <!-- ///DATENKORB/// -->
            <xsl:when test="$mode = 'databasket'">
                <xsl:call-template name="databasket"/>
            </xsl:when>
            <!-- //////////////////////////////////////////////////////////// -->
            <!--  ABOUT static datastream in context:szd -->
            <xsl:when test="$mode = 'about'">
                <article class="card">
                     <xsl:call-template name="getNavbar">
                         <xsl:with-param name="Title" select="'STEFAN ZWEIG DIGITAL'"/>
                         <xsl:with-param name="PID" select="'context:szd'"/>
                         <xsl:with-param name="mode" select="$mode"/>
                     </xsl:call-template>
                     <div class="card-body">
                         <xsl:apply-templates select="document(concat('/context:szd/', 'ABOUT'))/t:TEI/t:text/t:body/t:div"/>
                     </div>
                </article>
            </xsl:when>
            <!-- //////////////////////////////////////////////////////////// -->
            <!-- IMPRESSUM static datastream in context:szd -->
            <xsl:when test="$mode = 'imprint'">
                <article class="card">
                    <xsl:call-template name="getNavbar">
                        <xsl:with-param name="Title">
                            <xsl:choose>
                                <xsl:when test="$locale = 'en'">
                                    <xsl:text>Imprint</xsl:text>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:text>Imprerssum</xsl:text>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:with-param>
                        <xsl:with-param name="PID" select="'context:szd'"/>
                        <xsl:with-param name="mode" select="$mode"/>
                    </xsl:call-template>
                    <div class="card-body">
                        <xsl:apply-templates select="document('/context:szd/IMPRINT')/t:TEI/t:text/t:body/t:div"/>
                    </div>
                </article>
            </xsl:when>
            <!-- //////////////////////////////////////////////////////////// -->
        	<!-- HOME $mode = '' -->
            <xsl:otherwise>
                <section>
                    <article>
                        <!-- start img and text -->
                        <div class="card">
                            <div class="card-body">
                                <img class="img-fluid mx-auto d-block" src="https://gams.uni-graz.at/archive/objects/context:szd/datastreams/STARTBILD/content" alt="Titelbild"/>
                                 <div class="mt-5">
                                       <xsl:apply-templates select="document(concat('/context:szd/', 'STARTSEITE'))/t:TEI/t:text/t:body/t:div"/> 
                                 </div>
                            </div>
                        </div>
                    </article>
                </section>
            </xsl:otherwise>
        </xsl:choose>        
    </xsl:template>
   
    <!-- ///DATENKORB/// -->
    <!-- ///$mode = 'databasket'/// -->
    <xsl:template name="databasket">
        <section class="card">
            <!-- navbar -->
            <xsl:call-template name="getNavbar">
                <xsl:with-param name="Title">
                    <xsl:choose>
                        <xsl:when test="$locale = 'en'">
                            <xsl:text>DATABASKET</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>DATENKORB</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:with-param>
                <xsl:with-param name="PID" select="$PID"/>
                <xsl:with-param name="mode" select="$mode"/>
            </xsl:call-template>
            
            <article class="card-body" id="content">
                <div>
                    <p>
                        <xsl:text>Data entries can be added to the data basket.</xsl:text><br/>
                    </p>
                    <div class="btn-group" role="group" aria-label="Sortieren">
                        <button type="button" class="btn hidden-print" style="font-size:18px; background: none"  onclick="window.print()"><xsl:text>PRINT</xsl:text><span class="glyphicon glyphicon-print" aria-hidden="true"><xsl:text> </xsl:text></span></button>
                        <button class="btn disabled" href="#" role="button" style="margin: 10px;">
                            <img alt="Excel" height="25" id="rdf" src="{concat($gamsdev, '/img/TABELLENSYMBOL.png')}" title="HSSF"/>
                        </button>
                        
                        <button type="button" class="btn" style="font-size:18px; background: none;"  onclick="clearData()"><xsl:text>CLEAR</xsl:text><span class="glyphicon glyphicon-remove"><xsl:text> </xsl:text></span></button>
                    </div>
                    <xsl:variable name="Table-ID" select="concat('table_id', position())"/>
                    <!-- call DataTable -->
                    <script>
                        $(document).ready(function() {
                        $('#databasket_table').DataTable();
                        } );
                    </script>
                    <table id="databasket_table" class="table table-bordered" style="width:100%">
                        <thead>
                            <tr>
                                <th><xsl:text>TITLE</xsl:text></th>
                                <th><xsl:text>AUTHOR</xsl:text></th>
                                <th><xsl:text>WHEN</xsl:text></th>
                                <th><xsl:text></xsl:text></th>
                            </tr>
                        </thead>
                        <tbody id="databasekt_tbody">
                            <xsl:text> </xsl:text>
                        </tbody>
                    </table>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div id="databasekt_content">
                            <xsl:text> </xsl:text>
                        </div>
                        <script>
                            showData();
                        </script>
                    </div>    
                </div>
            </article>
	            	<!-- in datenkorb.js fibt im localStorage befindliche Einträge aus -->
	                <!--<div class="col-md-12 row hidden-print center-block">
	                    <div class="btn-group" role="group" aria-label="Sortieren">
	                        <xsl:choose>
	                            <xsl:when test="$locale = 'en'">
	                                <p>Objects can be saved to the data cart and displayed as a list</p>
	                                <button type="button" class="btn" onclick="sortPersonDatabasket()"><xsl:text>Sort person</xsl:text></button>
	                                <button type="button" class="btn" onclick="sortTitleDatabasket()"><xsl:text>Sort Title</xsl:text></button>
	                                <button type="button" class="btn" onclick="sortDateDatabasket()"><xsl:text>Sort Date</xsl:text></button>
	                                <button type="button" class="btn hidden-print"  onclick="window.print()"><xsl:text>Print</xsl:text><span class="glyphicon glyphicon-print" aria-hidden="true"><xsl:text> </xsl:text></span></button>
	                                <button type="button" class="btn" onclick="clearData()"><xsl:text>Clear</xsl:text><span class="glyphicon glyphicon-remove"><xsl:text> </xsl:text></span></button>
	                                <!-\-<button type="button" class="btn szdbutton hidden-print" onclick="printDatabasket()">Datenkorb Drucken <span class="glyphicon glyphicon-print" aria-hidden="true"><xsl:text> </xsl:text></span></button>-\->
	                                <!-\-<button type="button" class="btn szdbutton" onclick="exportData()" id="DownloadExcel">Excel erzeugen<span><img src="/archive/objects/context:ufbas/datastreams/TABELLENSYMBOL/content" alt="Tabellensymbol" height="15px"/><xsl:text> </xsl:text></span></button>-\->
	                                <span type="button" class="btn btn-success hidden" id="results"><xsl:text> </xsl:text></span>
	                            </xsl:when>
	                            <xsl:otherwise>
	                                <p> Im Datenkorb können Objekte gespeichert und als Liste ausgegeben werden</p>
	                                <button type="button" class="btn"  onclick="sortPersonDatabasket()"><xsl:text>Nach Personen sortieren </xsl:text></button>
	                                <button type="button" class="btn" onclick="sortTitleDatabasket()"><xsl:text>Nach Titel sortieren </xsl:text></button>
	                                <button type="button" class="btn" onclick="sortDateDatabasket()"><xsl:text>Nach Datum sortieren </xsl:text></button>
	                                <button type="button" class="btn hidden-print" onclick="window.print()"><xsl:text>Datenkorb drucken </xsl:text><span class="glyphicon glyphicon-print" aria-hidden="true"><xsl:text> </xsl:text></span></button>
	                                <button type="button" class="btn" onclick="clearData()"><xsl:text>Datenkorb leeren </xsl:text><span class="glyphicon glyphicon-remove"><xsl:text> </xsl:text></span></button>
	                                <!-\-<button type="button" class="btn szdbutton hidden-print" onclick="printDatabasket()">Datenkorb Drucken <span class="glyphicon glyphicon-print" aria-hidden="true"><xsl:text> </xsl:text></span></button>-\->
	                                <!-\-<button type="button" class="btn szdbutton" onclick="exportData()" id="DownloadExcel">Excel erzeugen<span><img src="/archive/objects/context:ufbas/datastreams/TABELLENSYMBOL/content" alt="Tabellensymbol" height="15px"/><xsl:text> </xsl:text></span></button>-\->
	                                <span type="button" class="btn btn-success hidden" id="results"><xsl:text> </xsl:text></span>
	                            </xsl:otherwise>
	                        </xsl:choose>
	                    </div>      
	                </div>
	                <div class="col-md-12 row">
	                     <div id="datenkorbInhalt">
	                         <xsl:text> </xsl:text>
	                     </div>
	                     <script>
	                         showData();
	                     </script>
	                </div>  -->     
        </section>
    </xsl:template>                    
    

</xsl:stylesheet>
