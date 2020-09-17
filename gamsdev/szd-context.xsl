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
            <!-- ///MEMORY/// -->
            <xsl:when test="$mode = 'objectbasket'">
                <xsl:call-template name="objectbasket"/>
            </xsl:when>
            <!-- ///DATENKORB/// -->
            <xsl:when test="$mode = 'databasket'">
                <xsl:call-template name="databasket"/>
            </xsl:when>
            <!-- ///MEMORY/// -->
            <xsl:when test="$mode = 'memory'">
                <xsl:call-template name="memory"/>
            </xsl:when>
            <!-- ///MEMORY/// -->
            <xsl:when test="$mode = 'map'">
                <xsl:call-template name="map"/>
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
                                    <xsl:text>Impressum</xsl:text>
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

    <!-- ////////////////////////////// -->
    <!-- map InfoVis -->
    <xsl:template name="map">
      <link rel="stylesheet" href="/lib/2.0/leaflet/leaflet.css"/>
      <script src="/lib/2.0/leaflet/leaflet.js"><xsl:text> </xsl:text></script>

      <xsl:variable name="LocationTypes" select="document('/archive/objects/query:szd.getlocationtypes/methods/sdef:Query/getXML')"/>
      <xsl:variable name="RESULTS" select="$LocationTypes//s:results/s:result"/>
      <xsl:variable name="AllResources" select="sum($RESULTS/s:resources)"/>
      <div class="card mt-5">
          <div class="card-body">
            <h1>
                <xsl:text>Übersicht</xsl:text>
            </h1>
            <ul>
               <li><xsl:text>Gesamt: </xsl:text><xsl:value-of select="$AllResources"/></li>
               <xsl:for-each-group select="$RESULTS" group-by="s:type/@uri">
                   <li>
                     <xsl:value-of select="substring-after(current-grouping-key(), '#')"/><xsl:text>: </xsl:text>
                     <xsl:value-of select="sum(current-group()/s:resources)"/>
                   </li>
               </xsl:for-each-group>
            </ul>
            <!--<xsl:for-each-group select="$RESULTS" group-by="s:name">
            <h3>
                <xsl:value-of select="current-grouping-key()"/>
                <xsl:text> </xsl:text>
            </h3>
                <ul>
                    <xsl:for-each-group select="current-group()" group-by="s:type/@uri">
                        <li>
                            <xsl:value-of select="substring-after(current-grouping-key(), '#')"/>:<xsl:value-of select="s:resources"/>
                            <xsl:text> </xsl:text>
                        </li>
                    </xsl:for-each-group>
                    <xsl:text> </xsl:text>
                </ul>
            </xsl:for-each-group>-->
            <h3>
                <xsl:text>Map</xsl:text>
            </h3>
            <div class="table-responsive">
              <div class="mt-4 mb-4" id="mapid" style="width: 85em; height: 40em;">
                <xsl:text> </xsl:text>
              </div>
          </div>
          </div>
      </div>
 <script>
   var map = L.map('mapid', {
		minZoom: 2,
		maxZoom: 15,
		zoomSnap: 0,
		zoomDelta: 0.25
	});

	var cartodbAttribution = '&amp;copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &amp;copy; <a href="https://carto.com/attribution">CARTO</a>';

	var positron = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
		attribution: cartodbAttribution
	}).addTo(map);

	var ZoomViewer = L.Control.extend({
		onAdd: function(){

			var container= L.DomUtil.create('div');
			var gauge = L.DomUtil.create('div');
			container.style.width = '200px';
			container.style.background = 'rgba(255,255,255,0.5)';
			container.style.textAlign = 'left';
			map.on('zoomstart zoom zoomend', function(ev){
				gauge.innerHTML = 'Zoom level: ' + map.getZoom();
			})
			container.appendChild(gauge);

			return container;
		}
	});

	(new ZoomViewer).addTo(map);

	map.setView([0, 0], 0);

  // add a circle
  //load JSON result with location, sum of resources for each location and type (book, work etc.)
  $.getJSON('/archive/objects/query:szd.getlocationoverview/methods/sdef:Query/getJSON?params=', function(json) {
    //create a circle for every location
    Object.keys(json).forEach(function(key){
        let SZDSTA = json[key].lo;
        let baseURL = "/archive/objects/query:szd.standort_search/methods/sdef:Query/get?params=";

        let QueryURL = baseURL + '$1|%3C' + encodeURIComponent(SZDSTA) + '%3E' + ';$2|de&amp;locale=de';
        console.log(QueryURL);
        L.circleMarker([json[key].lat, json[key].long],{
          radius: json[key].resources / 10,
          color: '#917a47',
          fillColor: '#c2a360',
          fillOpacity: 0.5
        }).addTo(map).bindPopup('<a href="' + QueryURL +'">' + json[key].name + "</a><br></br>" + json[key].resources);


     });
   });



 </script>


    </xsl:template>

    <!--static memory game -->
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
        </section>
        </div>
        <!-- JS -->
        <script src="{concat($server, $gamsdev,'/js/memory.js')}"><xsl:text> </xsl:text></script>
    </xsl:template>


    <xsl:template name="objectbasket">
        <div class="mt-5">
            <h1 class="mt-5">Object Basket</h1>
            <p id="o:iiw.interpreters">o:iiw.interpreters (TEI) 
                <input type="checkbox" onclick="addObject(this)"><xsl:text> </xsl:text></input>
            </p>
            <p id="o:szd.werke">o:szd.werke (TEI)
                <input type="checkbox" onclick="addObject(this)"><xsl:text> </xsl:text></input></p>
            <p id="o:roth.601129">o:roth.601129 (LIDO)
                <input type="checkbox" onclick="addObject(this)"><xsl:text> </xsl:text></input></p>
            <p id="o:depcha.schlitz.1">o:depcha.schlitz.1 (TEI)
                <input type="checkbox" onclick="addObject(this)"><xsl:text> </xsl:text></input></p>
            <p id="o:htx.WR1">o:htx.WR1 (TEI)
                <input type="checkbox" onclick="addObject(this)"><xsl:text> </xsl:text></input></p>
            <p id="o:szd.2087">o:szd.2087 (METS)
                <input type="checkbox" onclick="addObject(this)"><xsl:text> </xsl:text></input></p>
            <p id="context:depcha.schlitz">context:depcha.schlitz (not working)
                <input type="checkbox" onclick="addObject(this)"><xsl:text> </xsl:text></input></p>
         <div>
             <p>Enter PID here</p>
             <input id="input1" type="text" value=""/>
             <button onclick="addObject()">Add</button>
             <button type="button" onclick="clearData()">Clear Objectbasket</button>
             <button type="button" onclick="showData()">Show Objectbasket</button>
             <button type="button" onclick="zipAndDownload()">ZIP and Download</button>
             <table id="objectbasket_table" class="table table-bordered dt-responsive text-left">
                 <thead>
                     <tr class="card-header">
                         <th>pid</th>
                         <th>title</th>
                         <th>model</th>
                         <th>ownerId</th>
                         <th>lastModifiedDate</th>
                         <th><xsl:text> </xsl:text></th>
                     </tr>
                 </thead>
                 <tbody id="objectbasket_tbody" onload="console.log('test');"/>
                 
             </table>
             
         </div>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.2/FileSaver.min.js"><xsl:text> </xsl:text></script>       
            <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.5.0/jszip.min.js"><xsl:text> </xsl:text></script>
            <script src="https://glossa.uni-graz.at/gamsdev/pollin/szd/trunk/www/js/objectbasket.js"><xsl:text> </xsl:text></script>
            <script type="text/javascript">
                checkCheckBoxes();
            </script>
        </div>
    </xsl:template>

</xsl:stylesheet>
