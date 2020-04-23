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
            <xsl:when test="$mode = 'memory'">
                <xsl:call-template name="memory"/>
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
                                <img class="img-fluid mx-auto d-block" src="/archive/objects/context:szd/datastreams/STARTBILD/content" alt="Titelbild"/>
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
                <!-- datatables.js -->
                <script src="{concat($gamsdev,'/js/datatable.js')}"><xsl:text> </xsl:text></script>
                <!-- needed for datatale excel export -->
                <script src="{concat($gamsdev,'/js/jszip.js')}"><xsl:text> </xsl:text></script>
                <script src="{concat($gamsdev,'/js/dataTables.buttons.min.js')}"><xsl:text> </xsl:text></script>
                <script src="{concat($gamsdev,'/js/pdfmake.min.js')}"><xsl:text> </xsl:text></script>
                <script src="{concat($gamsdev,'/js/vfs_fonts.js')}"><xsl:text> </xsl:text></script>
                <script src="{concat($gamsdev,'/js/buttons.html5.min.js')}"><xsl:text> </xsl:text></script>
                
                    <xsl:choose>
                        <xsl:when test="$locale='en'">
                            <p class="card-text row">
                                 <xsl:text>Records can be saved to the data cart by ticking the checkbox in the catalogue lists and search results. Entries will be stored in the browser for future sessions.</xsl:text>
                            </p>
                            <p>
                                <xsl:text>Abbreviations used for object categories:</xsl:text><br/>
                                <xsl:text>(W) Works (L) Personal Documents ("Lebensdokumente") (A) Autograph Collection(B) Library ("Bibliothek")</xsl:text>
                            </p>
                            <div class="row mb-3 float-right">
                                <button type="button"  onclick="clearData()">
                                    <xsl:text>CLEAR DATA </xsl:text>
                                    <i class="fas fa-trash" style="color:#631a34"><xsl:text> </xsl:text></i>
                                </button>
                            </div>
                        </xsl:when>
                        <xsl:otherwise>
                            <p class="card-text row">
                                <xsl:text>Im Datenkorb können Datensätze durch Ankreuzen des Auswahlkastens in den Kataloglisten und Suchergebnissen abgelegt werden. Die Einträge bleiben im Browser für weitere Arbeitssitzungen erhalten. </xsl:text>
                            </p>
                            <p>
                                <xsl:text>Siglen der Objektkategorien</xsl:text>
                                <br/>
                                <xsl:text>(W) Werke	(L) Lebensdokumente	(A) Autographensammlung	(B) Bibliothek</xsl:text>
                            </p>
                            <div class="row mb-3 float-right small">
                                <button type="button" onclick="clearData()">
                                <xsl:text>DATENKORB LEEREN  </xsl:text>
                                    <i class="fas fa-trash"  style="color:#631a34"><xsl:text> </xsl:text></i>
                                </button>
                            </div>
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
                    
                    "columns": [
                    { "width": "5%" },
                    { "width": "25%" },
                    { "width": "20%" },
                    null,
                    null
                    ],
                     dom: 'Bfrtip',
                    <!--      buttons: ['pdf', 'excel', 'csv'],-->
                    buttons: [
                    {
                    extend: 'pdfHtml5',
                    messageTop: "(W) Werke/Work (L) Lebensdokumente/Personal document (A) Autographen/Autograph collection (B) Bibliothek/Library",
                    orientation: 'landscape',
                    pageSize: 'LEGAL'
                    }
                    , 'excel', 'csv'
                    ],
                    "pageLength": 50,
                    "order": [[ 0, "desc" ]]  
                    }
                    );
                    } );
                </script>
                <div class="table-responsive">
                    <table id="databasket_table" class="table table-bordered dt-responsive nowra text-left">
                        <thead>
                            <tr class="card-header">
                                <th>
                                    <xsl:text> </xsl:text>
                                </th>
                                <th class="text-uppercase">
                                    <xsl:choose>
                                        <xsl:when test="$locale = 'en'">
                                            <xsl:text>Title</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>Titel</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </th>
                                <th class="text-uppercase">
                                    <i18n:text>author_szd</i18n:text>
                                </th>
                                <th class="text-uppercase">
                                    <xsl:choose>
                                        <xsl:when test="$locale = 'en'">
                                            <xsl:text>Location, Signature, URL</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>Standort, Signatur, URL</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </th>
                                <th>
                                    <xsl:text> </xsl:text>
                                </th>
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
        </section>
    </xsl:template>     
    
    <xsl:template name="memory">
        <!-- insert memopry.css and memory.js only when "get?mode=memory" -->
        <link href="{concat($server, $gamsdev, '/css/memory.css')}" rel="stylesheet" type="text/css"/>
       
        
        <xsl:variable name="pathIMG" select="concat($server, $gamsdev,'/img/memory')"/>
        
        <div class="card">
            <div class="card-body">
                <h1>Sternstunden des Memorys</h1>
            </div>
        
        <section class="memory_game mt-4 mb-4">
                
                     <div class="memory_card" data-framework="1">
                         <img class="front-face" src="{concat($pathIMG,'/1.jpg')}" alt="React"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="1">
                         <img class="front-face" src="{concat($pathIMG,'/1.jpg')}" alt="React"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="2">
                         <img class="front-face" src="{concat($pathIMG,'/2.jpg')}" alt="Angular"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="2">
                         <img class="front-face" src="{concat($pathIMG,'/2.jpg')}" alt="Angular"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="3">
                         <img class="front-face" src="{concat($pathIMG,'/3.jpg')}" alt="Ember"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="3">
                         <img class="front-face" src="{concat($pathIMG,'/3.jpg')}" alt="Ember"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="4">
                         <img class="front-face" src="{concat($pathIMG,'/4.jpg')}" alt="Vue"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="4">
                         <img class="front-face" src="{concat($pathIMG,'/4.jpg')}" alt="Vue"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="5">
                         <img class="front-face" src="{concat($pathIMG,'/5.jpg')}" alt="Backbone"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="5">
                         <img class="front-face" src="{concat($pathIMG,'/5.jpg')}" alt="Backbone"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="6">
                         <img class="front-face" src="{concat($pathIMG,'/6.jpg')}" alt="Aurelia"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="6">
                         <img class="front-face" src="{concat($pathIMG,'/6.jpg')}" alt="Aurelia"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     <div class="memory_card" data-framework="7">
                         <img class="front-face" src="{concat($pathIMG,'/7.jpg')}" alt="Aurelia"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="7">
                         <img class="front-face" src="{concat($pathIMG,'/7.jpg')}" alt="Aurelia"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="8">
                         <img class="front-face" src="{concat($pathIMG,'/8.jpg')}" alt="Aurelia"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>
                     
                     <div class="memory_card" data-framework="8">
                         <img class="front-face" src="{concat($pathIMG,'/8.jpg')}" alt="Aurelia"/>
                         <img class="back-face" src="{concat($pathIMG,'/back.jpg')}" alt="Memory Card"/>
                     </div>      
                
            
            
            
            <!--<div class="memory_card" data-framework="aurelia">
                <img class="front-face" src="img/memory/9.jpg" alt="Aurelia"/>
                <img class="back-face" src="img/memory/back.jpg" alt="Memory Card"/>
            </div>
            
            <div class="memory_card" data-framework="aurelia">
                <img class="front-face" src="img/memory/9.jpg" alt="Aurelia"/>
                <img class="back-face" src="img/memory/back.jpg" alt="Memory Card"/>
            </div>-->
        </section>
        </div>
        <!-- JS -->
        <script src="{concat($server, $gamsdev,'/js/memory.js')}"><xsl:text> </xsl:text></script>
    </xsl:template>
    

</xsl:stylesheet>
