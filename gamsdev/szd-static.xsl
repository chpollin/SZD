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
	xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:lido="http://www.lido-schema.org" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	xmlns:skos="http://www.w3.org/2004/02/skos/core#"
	xmlns:bibtex="http://bibtexml.sf.net/" exclude-result-prefixes="#all">

	<!-- about:legacy-compat -->
	<xsl:output method="xml" encoding="UTF-8" indent="no"/>

	<!-- ///VARIABELN/// -->
	<xsl:param name="mode"/>
	<xsl:param name="search"/>
	<xsl:param name="locale"/>
	
	<xsl:variable name="lang">
		<xsl:value-of select="substring-before(concat($locale, '_'), '_')"/>
	</xsl:variable>
	
	<xsl:variable name="model"
		select="substring-after(/s:sparql/s:results/s:result/s:model/@uri, '/')"/>
	
	<xsl:variable name="cid">
		<xsl:value-of select="/s:sparql/s:results/s:result[1]/s:cid"/>
	</xsl:variable>
	
	<xsl:variable name="PID">
		<xsl:choose>
			<!-- if its not a TEI file get the PID -->
			<xsl:when test="//skos:Schema[1]/@rdf:about">
				<xsl:value-of select="substring-after(//skos:Schema[1]/@rdf:about, 'gams.uni-graz.at/')"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="//t:teiHeader//t:idno[@type = 'PID']"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>

	<!-- GAMS variables -->
	<xsl:variable name="zim">Zentrum für Informationsmodellierung - Austrian Centre for Digital
		Humanities</xsl:variable>
	<xsl:variable name="zim-acdh">ZIM-ACDH</xsl:variable>
	<xsl:variable name="gams">Geisteswissenschaftliches Asset Management System</xsl:variable>
	<xsl:variable name="uniGraz">Universität Graz</xsl:variable>

	<!-- project-specific variables -->
	<xsl:variable name="server"></xsl:variable>
	<xsl:variable name="gamsdev">/gamsdev/pollin/szd/trunk/www</xsl:variable>

	<xsl:variable name="projectTitle">
		<xsl:text>Stefan Zweig digital</xsl:text>
	</xsl:variable>
	<xsl:variable name="subTitle">
		<xsl:text>Alpha-Version</xsl:text>
	</xsl:variable>

	<!-- whole project .css -->
	<xsl:variable name="projectCss">
		<xsl:value-of select="concat($server, $gamsdev, '/css/szd.css')"/>
	</xsl:variable>
	<!-- navbar .css-->
	<xsl:variable name="projectNav">
		<xsl:value-of select="concat($server, $gamsdev, '/css/navbar.css')"/>
	</xsl:variable>
	<!-- print .css-->
	<!--<xsl:variable name="printcss">
		<xsl:value-of select="concat($server, $gamsdev, '/css/print.css')"/>
	</xsl:variable>-->
	<!-- timeline, lebenskalender .css -->
	<xsl:variable name="timelineCss">
		<xsl:value-of select="concat($server, $gamsdev, '/css/lebenskalender.css')"/>
	</xsl:variable>


	<!-- ICONS: path to .png's  ================================================== -->
	<xsl:variable name="Icon_Path" select="concat($server, $gamsdev, '/icons/')"/>
	<xsl:variable name="Icon_bibliothek" select="concat($Icon_Path, 'biblothek.png')"/>
	<xsl:variable name="Icon_bilder" select="concat($Icon_Path, 'bilder.png')"/>
	<xsl:variable name="Icon_datenkorb" select="concat($Icon_Path, 'datenkorb.png')"/>
	<xsl:variable name="Icon_korrespodenzen" select="concat($Icon_Path, 'korrespodenzen.png')"/>
	<xsl:variable name="Icon_mail" select="concat($Icon_Path, 'mail.png')"/>
	<xsl:variable name="Icon_manuskript" select="concat($Icon_Path, 'manuskripthell.png')"/>
	<xsl:variable name="Icon_markieren" select="concat($Icon_Path, 'markieren.png')"/>
	<xsl:variable name="Icon_person" select="concat($Icon_Path, 'person.png')"/>
	<xsl:variable name="Icon_pfeil" select="concat($Icon_Path, 'pfeil.png')"/>
	<xsl:variable name="Icon_suche" select="concat($Icon_Path, 'suche.png')"/>
	<xsl:variable name="Icon_viewer" select="concat($Icon_Path, 'viewer.png')"/>
	<xsl:variable name="Icon_telefon" select="concat($Icon_Path, 'telefon.png')"/>
	<xsl:variable name="Icon_x" select="concat($Icon_Path, 'x.png')"/>
	<xsl:variable name="Icon_wiki" select="concat($Icon_Path, 'wiki.jpg')"/>
	<xsl:variable name="Icon_wikidata" select="concat($Icon_Path, 'wikidata.png')"/>

	<!-- //////////////////////////////////////////////////////////// -->
	<!-- TEMPLATE -->
	<xsl:template match="/">
		<html lang="de">
			<head class="hidden-print">
				<meta charset="utf-8"/>
				<meta http-equiv="X-UA-Compatible" content="IE=edge"/>
				<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>
				<!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
				<meta name="keywords"
					content="Stefan Zweig digital, Zweig, GAMS, ZIM, Nachlass, Rekonstruktion, Literaturarchiv Salzburg, Graz, Informations- und Forschungsportal"/>
				<meta name="description"
					content="Das internationale Projekt STEFAN ZWEIG DIGITAL ist eine Initiative des Literaturarchivs Salzburg und dient als virtuelle Informations- und Forschungsportal zu Leben und Werk des österreichischen Schriftstellers Stefan Zweig. Im Zentrum des Projekts steht die Rekonstruktion von Stefan Zweigs weltweit verstreutem Nachlass. Hierzu sind bereits die umfangreichen Manuskriptbestände aus dem Literaturarchiv Salzburg und der Daniel Reed Library in Fredonia/New York verzeichnet und teilweise mit digitalen Faksimiles ergänzt worden. Hinzu kommt das Verzeichnis von Zweigs Bibliothek, das all jene heute noch nachweisbaren Buchbestände enthält, die er im Lauf seines Lebens an verschiedenen Orten zusammengetragen hat. STEFAN ZWEIG DIGITAL bietet umfangreiche Recherchemöglichkeiten, die durch besondere Themenseiten ergänzt werden. Eine Präsentation zu Stefan Zweigs Werk Marie Antoinette bildet den Auftakt dieser Reihe."/>
	    		<meta name="publisher"
					content="Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities"/>
				<meta name="publisher" content="Literaturarchiv Salzburg"/>
				<meta name="author" content="Christopher Pollin"/>
				<meta name="content-language" content="de"/>
			
				<!--Projekttitel-->
				<title>
					<xsl:value-of select="$projectTitle"/>
				</title>
				
				<!-- Bootstrap core CSS  ================================================== -->
				<!-- Bootstrap 4 core CSS -->
				<link href="/lib/2.0/bootstrap-4.3.1-dist/css/bootstrap.min.css" rel="stylesheet"/>
				
				<!-- fixed navbar-side -->
				<!--<link href="{concat($server, $gamsdev, '/css/navbar-fixed-side.css')}" rel="stylesheet"/>-->

				<!-- Custom styles for this template  ================================================== -->
				<!--<link href="{$printcss}" rel="stylesheet" type="text/css" media="print"/>-->
				<link href="{$projectCss}" rel="stylesheet"/>
				<link href="{$projectNav}" rel="stylesheet"/>
				
				<!-- Timeline: Lebenskalender -->
				<link href="{$timelineCss}" rel="stylesheet" type="text/css"/>
				<link type="text/css" rel="stylesheet" href="/lib/1.0/plugins/fancybox_v2.1.5/source/jquery.fancybox.css?v=2.1.5"/>
				<link rel="stylesheet" href="/lib/2.0/fa/css/all.css"/>
				
				<link href="https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css"  rel="stylesheet" type="text/css"/>
				<!-- jQuery core JavaScript ================================================== -->
				<script src="/lib/2.0/jquery-3.4.0.min.js"><xsl:text> </xsl:text></script>

				<!-- Bootstrap core JavaScript ================================================== -->
				<!-- Bootstrap's dropdowns require Popper.js (https://popper.js.org/)  -->
				<script src="{concat($server, $gamsdev, '/js/popper.min.js')}"><xsl:text> </xsl:text></script>
				<script src="/lib/2.0/bootstrap-4.3.1-dist/js/bootstrap.min.js"><xsl:text> </xsl:text></script>
				
				<!-- projectspecific .js ================================================== -->
				<script src="{concat($server, $gamsdev,'/js/databasket.js')}"><xsl:text> </xsl:text></script>
				<script src="/lib/1.0/plugins/fancybox_v2.1.5/source/jquery.fancybox.js?v=2.1.5"><xsl:text> </xsl:text></script>
				<!-- SCROLLDOWN -->
				<!-- for fancybox in o:szd.glossar -->
				<script>
					$(document).ready(function(){
					$('a.fancybox').fancybox({'type' : 'image'});
					});
				</script>
				<!-- datatables.js -->
				<script src="{concat($gamsdev,'/js/datatable.js')}"><xsl:text> </xsl:text></script>
				<!-- needed for datatale excel export -->
				<script src="{concat($gamsdev,'/js/jszip.js')}"><xsl:text> </xsl:text></script>
				<script src="{concat($gamsdev,'/js/dataTables.buttons.min.js')}"><xsl:text> </xsl:text></script>
				<script src="{concat($gamsdev,'/js/pdfmake.min.js')}"><xsl:text> </xsl:text></script>
				<script src="{concat($gamsdev,'/js//vfs_fonts.js')}"><xsl:text> </xsl:text></script>
				<script src="{concat($gamsdev,'/js/buttons.html5.min.js')}"><xsl:text> </xsl:text></script>
				<script src="{concat($server, $gamsdev,'/js/buildquery.js')}"><xsl:text> </xsl:text></script>
			</head>

			<!-- //////////////////////////////////////////////////////////// -->
			<!-- ///BODY/// -->
			<body>
				<noscript>
					<p>JavaScript ist im Browser deaktiviert oder wird nicht unterstützt. Aktivieren
						Sie JavaScript um die Seite richtig darzustellen.</p>
				</noscript>
				<!-- ///HEADER/// -->
				<header>
				<!-- ///NAVBAR/// -->
					<nav class="navbar navbar-expand-md fixed-top navbar-dark"><!-- fixed/sticky nav benötigt; muss noch nach rechts angepasst werden (margin) -->
						<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#nav" aria-controls="nav" aria-expanded="false" aria-label="Toggle navigation">
							<span class="navbar-toggler-icon"><xsl:text> </xsl:text></span>
						</button>
						<div class="container">
							<div class="collapse navbar-collapse" id="nav">
								<ul class="navbar-nav">
									<li class="nav-item">
										<a href="/context:szd/sdef:Context/get?locale={$locale}">
											<img 
												src="{concat($server, $gamsdev, '/img/SZlogo.png')}"
												title="Home" alt="SZ Logo" height="60"/>
											<xsl:text> </xsl:text>
										</a>
									</li>
									<li class="nav-item dropdown">
										<a class="navtext dropdown-toggle text-uppercase" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
											<i18n:text>estate</i18n:text>
										</a>
										<div class="dropdown-menu" aria-labelledby="navbarDropdown">
											<a class="dropdown-item text-uppercase" href="/o:szd.werke/sdef:TEI/get?locale={$locale}">
												<i18n:text>works</i18n:text>
											</a>
											<a class="dropdown-item text-uppercase" href="/o:szd.lebensdokumente/sdef:TEI/get?locale={$locale}">
												<i18n:text>personaldocument</i18n:text>
											</a>
											<!--<a class="dropdown-item" href="/o:szd.korrespodenzen"><xsl:text>KORRESPONDENZEN</xsl:text></a>-->
										</div>
									</li>
									<li class="nav-item dropdown">
										<a class="navtext dropdown-toggle text-uppercase" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
											<i18n:text>collection</i18n:text>
										</a>
										<div class="dropdown-menu" aria-labelledby="navbarDropdown">
											<a class="dropdown-item text-uppercase" href="/o:szd.autographen/sdef:TEI/get?locale={$locale}">
												<i18n:text>autograph</i18n:text>
											</a>
											<a class="dropdown-item text-uppercase" href="/o:szd.bibliothek/sdef:TEI/get?locale={$locale}">
												<i18n:text>library_szd</i18n:text>
											</a>
										</div>
									</li>
									<li class="nav-item dropdown">
										<a class="navtext dropdown-toggle text-uppercase" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
											<i18n:text>subjects</i18n:text>
										</a>
										<div class="dropdown-menu" aria-labelledby="navbarDropdown">
											<a class="dropdown-item text-uppercase" href="/o:szd.thema.1/sdef:TEI/get?locale={$locale}"><xsl:text>Marie Antoinette</xsl:text></a>
										</div>
									</li>
									<li class="nav-item">
										<a class="navtext text-uppercase" href="/o:szd.lebenskalender/sdef:TEI/get?locale={$locale}">
											<i18n:text>biography</i18n:text>
										</a>
									</li>
									<!-- INDEX -->
									<li class="nav-item dropdown">
										<a class="navtext dropdown-toggle text-uppercase" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
											<xsl:text>Index</xsl:text>
										</a>
										<div class="dropdown-menu" aria-labelledby="navbarDropdown">
											<a class="dropdown-item text-uppercase" href="/o:szd.personen/sdef:TEI/get?locale={$locale}">
												<i18n:text>persons</i18n:text>
											</a>
											<!--<a class="dropdown-item" href="{concat($server, '/archive/objects/query:szd.getstandorte/methods/sdef:Query/get?')}"><xsl:text>STANDORTE</xsl:text></a>-->
											<a class="dropdown-item text-uppercase" href="/o:szd.standorte/sdef:TEI/get?locale={$locale}">
												<i18n:text>locations</i18n:text>
											</a>
											<a class="dropdown-item text-uppercase" href="https://de.wikisource.org/wiki/Stefan_Zweig/Erstausgaben" target="_blank">
												<i18n:text>firstedition</i18n:text>
											</a>
											<!--<a class="dropdown-item text-uppercase" href="/o:szd.publikation">
												<i18n:text>firstedition</i18n:text>
											</a>-->
										</div>
									</li>
									<li class="nav-item">
										<a class="navtext text-uppercase" href="/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=en">
											<i18n:text>glossary</i18n:text>
										</a>
									</li>
									<li class="nav-item">
										<a class="navtext text-uppercase" href="{concat($server, '/archive/objects/context:szd/methods/sdef:Context/get?mode=about&amp;locale=',$locale)}">
											<i18n:text>about</i18n:text>
										</a>
									</li>
									<!--<li class="nav-item dropdown">
										<a class="dropdown-toggle navtext text-uppercase" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
											<i18n:text>project</i18n:text>
										</a>
										<div class="dropdown-menu" aria-labelledby="navbarDropdown">
											<a class="dropdown-item text-uppercase" href="{concat($server, '/archive/objects/context:szd/methods/sdef:Context/get?mode=about&amp;locale=',$locale)}">
												<i18n:text>description</i18n:text>
											</a>
											<!-\-<a class="dropdown-item text-uppercase" href="/archive/objects/o:szd.ontology/methods/sdef:Ontology/get?locale=en">
												<i18n:text>ontology_szd</i18n:text>
											</a>-\->
										</div>
									</li>-->
									<li class="nav-item">
										<form class="navbar-form navtext" id="fulltext_search" method="get">
											<xsl:choose>
												<xsl:when test="$locale = 'en'">
													<xsl:attribute name="action" select="'/archive/objects/query:szd.fulltext/methods/sdef:Query/get?locale=en&amp;'"/>
												</xsl:when>
												<xsl:otherwise>
													<xsl:attribute name="action" select="'/archive/objects/query:szd.fulltext/methods/sdef:Query/get?locale=de&amp;'"/>
												</xsl:otherwise>
											</xsl:choose>
											<div class="form-row">
												<div class="input-group">
													<input class="form-control border" id="n$1" name="$1" type="text" lang="{$locale}">
														<xsl:attribute name="placeholder">
															<xsl:choose>
																<xsl:when test="$locale = 'en'">
																	<xsl:text>FULL-TEXT SEARCH</xsl:text>
																</xsl:when>
																<xsl:otherwise>
																	<xsl:text>VOLLTEXTSUCHE</xsl:text>
																</xsl:otherwise>
															</xsl:choose>
														</xsl:attribute>
													</input>
													<div class="input-group-prepend">
														<button type="submit" class="btn icon_suche">
															<img src="{$Icon_suche}" alt="Search" height="20"/>
														</button>
													</div>
												</div>
											</div>
										</form>
									</li>
									<!-- ////////// -->
									<!-- DATABASKET -->
									<li class="nav-item">
										<a class="navtext" href="{concat('/archive/objects/context:szd/methods/sdef:Context/get?mode=databasket&amp;locale=', $locale)}">
											<xsl:choose>
												<xsl:when test="$locale = 'en'">
													<xsl:attribute name="title"><xsl:text>Objects can be saved to the data cart and exported</xsl:text></xsl:attribute>
												</xsl:when>
												<xsl:otherwise>
													<xsl:attribute name="title"><xsl:text>Im Datenkorb können Objekte gespeichert und exportiert werden</xsl:text></xsl:attribute>
												</xsl:otherwise>
											</xsl:choose>
											<img src="{$Icon_datenkorb}" class="img-fluid icon_navbar" alt="Datenkorb"/>
											<xsl:text> </xsl:text>
										</a>
									</li>
									<li class="nav-item">
										<xsl:call-template name="languageButton">
											<xsl:with-param name="PID">
												<xsl:choose>
													<xsl:when test="not($PID = '')">
														<xsl:value-of select="$PID"/>
													</xsl:when>
													<xsl:otherwise>
														<xsl:text>context:szd</xsl:text>
													</xsl:otherwise>
												</xsl:choose>
											</xsl:with-param>
											<xsl:with-param name="mode" select="$mode"/>
										</xsl:call-template>
									</li>
								</ul>
							</div>
						</div>
					</nav>
					<!--  -->
					<script src="{concat($server, $gamsdev,'/js/scrolldown.js')}"><xsl:text> </xsl:text></script>
					<script src="{concat($server, $gamsdev,'/js/scrolldown_search.js')}"><xsl:text> </xsl:text></script>
				</header>
				
				<!-- //////////////////////////////////////////////////////////// -->
				<!-- ///CONTENT/// -->
				<main class="container">
					<!-- <choose> checks actual 'position' on the page -->
					<xsl:choose>
						<xsl:when test="$mode = '' and $cid = 'context:szd'">
						<xsl:text>exception szd-static.xsl</xsl:text>
						</xsl:when>
						<!-- //////////////////////////////////////////////////////////// -->
						<!-- /// /// -->
						<!-- call further content, e.g. databasket view -->
						<xsl:otherwise>
							<xsl:call-template name="content"/>
						</xsl:otherwise>
					</xsl:choose>
				</main>

				<!-- //////////////////////////////////////////////////////////// -->
				<!-- ///FOOTER/// -->
				<footer class="footer" >
				<div class="container">
					<div class="card">
						<div class="card-body">
							
							<div class="col-12 text-center">
								<xsl:choose>
									<xsl:when test="$locale='en'">
									<p>
										<xsl:text>STEFAN ZWEIG DIGITAL | A project developed on the initiative of the Literature Archive Salzburg</xsl:text>
										<br/>
										<xsl:text>Residenzplatz 9/2 | 5020 Salzburg  |  Austria | +43 (0) 662 / 8044-4910 | </xsl:text> <a href="mailto:info@stefanzweig.digital">info@stefanzweig.digital</a>
									</p>
									</xsl:when>
									<xsl:otherwise>
										<p>
											<xsl:text>STEFAN ZWEIG DIGITAL | Eine Initiative des Literaturarchivs Salzburg</xsl:text>
											<br/>
											<xsl:text>Residenzplatz 9/2 | 5020 Salzburg  |  Austria | +43 (0) 662 / 8044-4910 | </xsl:text> <a href="mailto:info@stefanzweig.digital">info@stefanzweig.digital</a>
										</p>
									</xsl:otherwise>
								</xsl:choose>
							</div>
							<hr/>
							

							<div class="col-12 text-center">
								<div class="row">
									<div class="col-sm-3">
										<a href="https://www.uni-salzburg.at/index.php?id=72" target="_blank">
											<img class="footer_img"   style="max-width: 60%;"
												src="{concat($server, $gamsdev, '/img/LAS_Logo.gif')}"
												alt="Logo LAS"/></a>
									</div>
									<div class="col-sm-3">
										<a href="https://creativecommons.org/licenses/by-nc/4.0/deed.de"
											target="_blank">
											<img class="footer_img" src="/templates/img/by-nc.png" alt="Lizenz" style="max-width: 40%;margin-top: 3%;"/>
										</a>
									</div>
									<div class="col-sm-3">
										<a class="text-center text-uppercase" href="/archive/objects/context:szd/methods/sdef:Context/get?mode=about&amp;locale={$locale}" target="_blank">
											<xsl:choose>
												<xsl:when test="$locale = 'en'">
													<xsl:text>Project partner</xsl:text>
												</xsl:when>
												<xsl:otherwise>Projektpartner</xsl:otherwise>
											</xsl:choose>
										</a>
										
									</div>
									<div class="col-sm-3">
										<a href="http://www.fotohof.at" target="_blank" >
											<img class="footer_img"
												src="{concat($server, $gamsdev, '/img/Fotohof.jpg')}"
												alt="Fotohof"/>
										</a>
									</div>
								</div>
								<div class="row">
									<div class="col-sm-3">
										<xsl:text> </xsl:text>
									</div>
									<div class="col-sm-3">
										<xsl:text></xsl:text>
										<a href="/archive/objects/context:szd/methods/sdef:Context/get?mode=imprint&amp;locale={$locale}" target="_blank" class="text-uppercase text-center mt-5">
											<xsl:choose>
												<xsl:when test="$locale = 'en'">
													<xsl:text>Site notice</xsl:text>
												</xsl:when>
												<xsl:otherwise>Impressum</xsl:otherwise>
											</xsl:choose>
										</a>
										
									</div>
									<div class="col-sm-3">
										<a href="http://gams.uni-graz.at" target="_blank">
											<img class="footer_img"   
												src="/templates/img/gamslogo_schwarz.gif"
												alt="{$gams}"/>
										</a>
										
									</div>
									<div class="col-sm-3">
										
										<a href="https://web.nli.org.il" target="_blank">
											<img class="footer_img"
												src="{concat($server, $gamsdev, '/img/logo_NLI.png')}"
												alt="The National Library of Israel"/>
										</a>
									</div>
								</div>
								<div class="row">
									<div class="col-sm-3">
										<a href="https://www.uni-salzburg.at" target="_blank" class="align-self-end">
											<img class="footer_img"   style="max-width: 60%;"
												src="https://www.uni-salzburg.at/fileadmin/oracle_file_imports/553397.JPG"
												alt="Logo Universität Salzburg"/></a>
									</div>
									<div class="col-sm-3">
										<a href="http://gams.uni-graz.at/archive/objects/context:gams/methods/sdef:Context/get?mode=dataprotection&amp;locale={$locale}"  target="_blank" class="text-uppercase text-center mt-5">
											<i18n:text>privacy</i18n:text>
										</a>
									</div>
									<div class="col-sm-3">
										
										<a href="https://informationsmodellierung.uni-graz.at" 
											target="_blank">
											<img class="footer_img"  style="max-width: 20%;margin-top:3%"
												src="/templates/img/ZIM_blau.png"
												alt="{$zim-acdh}"/>
										</a>
										<xsl:text> </xsl:text>
										<a href="https://www.uni-graz.at" target="_blank" >
											<img class="footer_img" src="/templates/img/logo_uni_graz_4c.jpg"  style="max-width: 20%;margin-top:3%" 
												title="Universität Graz" alt="Logo Uni Graz"/>
											<xsl:text> </xsl:text>
										</a>
										
									</div>
									<div class="col-sm-3">
										<a href="http://fredonia.libguides.com/archives/zweig" target="_blank">
											<img class="footer_img"
												src="{concat($server, $gamsdev, '/img/fredonia.png')}"
												alt="Reed Library – Stefan Zweig Collection, Fredonia"/>
										</a>
										
									</div>
								</div>
								
							
							<!--	<div class="col-sm-3 text-center">
									
										
										<br/>
								
								</div>
								<div class="col-sm-3">
									
									<span class="row">
									
									</span>
									<span class="row">
										<span class="col-sm-6">
											
										</span>
										<xsl:text> </xsl:text>
										<span class="col-sm-6">
											
										</span>
									</span>
									
								</div>
								<div class="col-sm-3">
									
									
								</div>-->
							</div>
						
						</div>
					</div>
						
					</div>
				</footer>
				<!-- switches <arrow ▲ down to up on collapse -->
				<script>
					$('a[data-toggle="collapse"]').click(function(){
					$(this).find("span.arrow").text(function(i,old){
					return old=='&#9660; ' ?  '&#9650; ' : '&#9660; ';
					});
					}); 
				</script>
				<script>
					window.onload = function () {
						var hash = window.location.hash.substr(1);
						<!--var substring1 = 'SZDMSK';
						var substring2 = "SZDBIB";
						var substring3 = "SZDLEB";
						var substring3 = "SZDAUT";
						if(hash.includes(substring1) || hash.includes(substring2) || hash.includes(substring3))
						{-->
					    if(location.hash){
							location.hash = "#" + hash;
							window.scrollBy(0, -250);
							$(document.getElementById(hash).getElementsByClassName("collapse")).collapse() ;}
					}
				</script>
			</body>
		</html>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<!-- en | de text for ABOUT, IMPRINT etc. -->
	<xsl:template match="t:div[@type='main']">
			<xsl:choose>
	            <xsl:when test="$locale = 'en'">
	                <xsl:apply-templates select="t:div[@xml:lang = 'en']"/>
	            </xsl:when>
	            <xsl:otherwise>
	                <xsl:apply-templates select="t:div[@xml:lang = 'de']"/>
	            </xsl:otherwise>
      		</xsl:choose>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:div[@xml:lang='de']">
		<xsl:apply-templates/>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:div[@xml:lang='en']">
		<xsl:apply-templates/>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:head">
		<h3>
			<xsl:apply-templates></xsl:apply-templates>
		</h3>
	</xsl:template>

	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:p">
		<p class="card-text"><xsl:apply-templates></xsl:apply-templates></p>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:hi[@style='italic']">
		<i><xsl:apply-templates></xsl:apply-templates></i>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:ref[@target]">
		<a href="{@target}"><xsl:apply-templates></xsl:apply-templates></a>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<!-- @href starttext -->
	<xsl:template match="t:span[@type='href']">
		<xsl:choose>
			<xsl:when test="contains(@target, 'mailto:')">
				<a href="{concat('/',@target)}">
					<xsl:apply-templates/>
				</a>
			</xsl:when>
			<xsl:otherwise>
				<a href="{@target}">
					<xsl:apply-templates/>
				</a>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:lb">
		<br/>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<!-- creates EN | DE button for languages, locale=en|de mode=about -->
	<xsl:template name="languageButton">
		<xsl:param name="PID"/>
		<xsl:param name="mode"/>
		<span class="language navtext text-right">
			<xsl:choose>
				<!-- for contex objects -->
				<xsl:when test="$PID = 'context:szd'">
					<a href="{concat('/archive/objects/', $PID, '/methods/sdef:Context/get?locale=de&amp;mode=', $mode)}">DE</a>
					<span class="text-dark pl-1 pr-1">|</span>
					<a href="{concat('/archive/objects/', $PID, '/methods/sdef:Context/get?locale=en&amp;mode=', $mode)}">EN</a>
				</xsl:when>
				<!-- for ontology objects -->
				<xsl:when test="$PID = 'o:szd.ontology'">
					<a href="{concat('/archive/objects/', $PID, '/methods/sdef:Ontology/get?locale=de&amp;mode=', $mode)}">DE</a>
					<span class="text-dark pl-1 pr-1">|</span>
					<a href="{concat('/archive/objects/', $PID, '/methods/sdef:Ontology/get?locale=en&amp;mode=', $mode)}">EN</a>
				</xsl:when>
				<!-- for skos objetcs -->
				<xsl:when test="$PID = 'o:szd.glossar'">
					<a href="{concat('/archive/objects/', $PID, '/methods/sdef:SKOS/get?locale=de&amp;mode=', $mode)}">DE</a>
					<span class="text-dark pl-1 pr-1">|</span>
					<a href="{concat('/archive/objects/', $PID, '/methods/sdef:SKOS/get?locale=en&amp;mode=', $mode)}">EN</a>
				</xsl:when>
				<!-- for TEI objects -->
				<xsl:otherwise>
					<a href="{concat('/', $PID, '/sdef:TEI/get?locale=de')}">DE</a>
					<span class="text-dark pl-1 pr-1">|</span>
					<a href="{concat('/', $PID, '/sdef:TEI/get?locale=en')}">EN</a>
				</xsl:otherwise>
			</xsl:choose>
		</span>
	</xsl:template>
	

	
	
</xsl:stylesheet>
