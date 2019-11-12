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
                                    <xsl:text>Site Notice</xsl:text>
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
                <xsl:with-param name="PID" select="'context:szd'"/>
                <xsl:with-param name="mode" select="$mode"/>
            </xsl:call-template>
            
            <article class="card-body" id="content">
                    <xsl:choose>
                        <xsl:when test="$locale='en'">
                            <p class="card-text">
                                 <xsl:text> This virtual document displays the information that you have currently stored in the data basket on this computer and browser (local storage).
                                 To transfer data to your data basket, select a check box in the catalog views. 
                                 You can delete individual entries (x) or empty (CLEAR) the entire data basket. In addition, several export options are offered.
                                 </xsl:text>
                                <br/>
                                <button type="button" class="btn" onclick="clearData()"><xsl:text>CLEAR DATA </xsl:text><i class="fas fa-trash"><xsl:text> </xsl:text></i></button>
                            </p>
                        </xsl:when>
                        <xsl:otherwise>
                           <p class="card-text">
                                <xsl:text>
                                Dieses virtuelle Dokument zeigt die Informationen an, die Sie aktuell im Datenkorb auf diesem Computer und diesem Browser (local storage) abgelegt haben.
                                Um Daten in Ihren Datenkorb zu übernehmen, wählen Sie ein Auswahlkästchen in den Katalogansichten. 
                                Sie können einzelne Einträge (x) löschen oder den ganzen Datenkorb leeren. Weiters werden mehrer Exportmöglichkeiten angeboten.
                                </xsl:text>
                               <br/>
                               <button type="button" class="btn" onclick="clearData()"><xsl:text>DATENKORB LEEREN </xsl:text><i class="fas fa-trash"><xsl:text> </xsl:text></i></button>
                           </p>
                        </xsl:otherwise>
                    </xsl:choose>
                <xsl:variable name="Table-ID" select="concat('table_id', position())"/>
                <!-- call DataTable -->
               <!-- <script>
                    $(document).ready(function() {
                    $('#databasket_table').DataTable();
                    } );
                </script>-->
                <script>
                    $(document).ready(function(){
                    $('#databasket_table').DataTable({
                    columnDefs: [
                    { type: 'formatted-num', targets: 0 }
                    ],
                    dom: 'Bfrtip',
                    buttons: ['csv', 'excel', 'pdf'],
                    "pageLength": 50,
                    <!-- ordering -->
                    "order": [[ 0, "asc" ]]  
                    }
                    );
                    } );
                </script>
                <table id="databasket_table" class="table table-bordered dt-responsive nowra text-left">
                    <thead>
                        <tr class="card-header">
                            <th class="text-uppercase">
                                <i18n:text>Titel</i18n:text>
                            </th>
                            <th class="text-uppercase">
                                <i18n:text>author_szd</i18n:text>
                            </th>
                            <th class="text-uppercase">
                                <i18n:text>partiesinvolved</i18n:text>
                            </th>
                            <th class="text-uppercase">
                                <xsl:choose>
                                    <xsl:when test="$locale = 'en'">
                                        <xsl:text>Date</xsl:text>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:text>Datum</xsl:text>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </th>
                            <th class="text-uppercase">URL</th>
                            <th><xsl:text> </xsl:text> </th>
                        </tr>
                    </thead>
                    <tbody id="databasekt_tbody">
                        <xsl:text> </xsl:text>
                    </tbody>
                </table>
            
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
        </section>
    </xsl:template>                    
    

</xsl:stylesheet>
