﻿<?xml version="1.0" encoding="UTF-8"?>

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
	
	<!--  -->
	<xsl:variable name="PID">
		<xsl:choose>
			<!-- if its not a TEI file get the PID -->
			<xsl:when test="//skos:Schema[1]/@rdf:about">
				<xsl:value-of select="substring-after(//skos:Schema[1]/@rdf:about, 'gams.uni-graz.at/')"/>
			</xsl:when>
			<xsl:when test="//t:teiHeader//t:idno[@type = 'PID']">
				<xsl:value-of select="//t:teiHeader//t:idno[@type = 'PID']"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:comment>error in szd-static.xsl: no PID found</xsl:comment>
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
	<!-- GLOSSA: /gamsdev/pollin/szd/trunk/www | GAMS: /szd -->
    <xsl:variable name="gamsdev">/gamsdev/pollin/szd/trunk/www</xsl:variable> 
	<!-- GAMS -->
	<!--<xsl:variable name="gamsdev">/szd</xsl:variable>-->
	
	<xsl:variable name="projectTitle">
		<xsl:text>Stefan Zweig digital</xsl:text>
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
	<xsl:variable name="printcss">
		<xsl:value-of select="concat($server, $gamsdev, '/css/print.css')"/>
	</xsl:variable>
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
				<meta name="content-language" content="en"/>
				
				<!--Projekttitel-->
				<title>
					<xsl:value-of select="$projectTitle"/>
				</title>
				
				<!-- Bootstrap core CSS  ================================================== -->
				<!-- Bootstrap 4 core CSS -->
				<link href="/lib/2.0/bootstrap-4.5.0-dist/css/bootstrap.min.css" rel="stylesheet"/>
				<!-- Custom styles for this template  ================================================== -->
				<!--<link href="{$printcss}" rel="stylesheet" type="text/css" media="print"/>-->
				<link href="{$projectCss}" rel="stylesheet"/>
				<link href="{$projectNav}" rel="stylesheet"/>
				<!-- Timeline: Lebenskalender -->
				<link href="{$timelineCss}" rel="stylesheet" type="text/css"/>
				<link rel="stylesheet" type="text/css" href="/lib/1.0/plugins/fancybox_v2.1.5/source/jquery.fancybox.css?v=2.1.5"/>
				<link rel="stylesheet" href="/lib/2.0/fa/css/all.css"/>
				<link href="{concat($server, $gamsdev, '/css/dataTables.css')}"  rel="stylesheet" type="text/css"/>
				
				<!-- jQuery core JavaScript ================================================== -->
				<script src="/lib/2.0/jquery-3.5.1.min.js"><xsl:text> </xsl:text></script>
				<!-- Bootstrap core JavaScript ================================================== -->
				<!-- Bootstrap's dropdowns require Popper.js (https://popper.js.org/)  -->
				<script src="{concat($server, $gamsdev, '/js/popper.min.js')}"><xsl:text> </xsl:text></script>
				<script src="/lib/2.0/bootstrap-4.5.0-dist/js/bootstrap.min.js"><xsl:text> </xsl:text></script>
				<!-- projectspecific .js ================================================== -->
				<script src="{concat($server, $gamsdev,'/js/databasket.js')}"><xsl:text> </xsl:text></script>
				<script src="/lib/1.0/plugins/fancybox_v2.1.5/source/jquery.fancybox.js?v=2.1.5"><xsl:text> </xsl:text></script>
				<!-- for fancybox in o:szd.glossar -->
				<script>
					$(document).ready(function(){
					$('a.fancybox').fancybox({'type' : 'image'});
					});
				</script>
				<script src="{concat($server, $gamsdev,'/js/buildquery.js')}"><xsl:text> </xsl:text></script>
				<script src="{concat($server, $gamsdev,'/js/FileSaver.js')}"><xsl:text> </xsl:text></script>
				<!--<script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/1.3.8/FileSaver.js"><xsl:text> </xsl:text></script-->
				<script src="{concat($server, $gamsdev,'/js/jszip.js')}"><xsl:text> </xsl:text></script>
				<script src="{concat($server, $gamsdev,'/js/download_images_iiif_manifest.js')}"><xsl:text> </xsl:text></script>
				<script src="{concat($server, $gamsdev,'/js/szd.js')}"><xsl:text> </xsl:text></script>
				
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
					<nav class="navbar navbar-expand-md fixed-top navbar-dark pt-sm-2 border-bottom">
						<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#nav" aria-controls="nav" aria-expanded="false" aria-label="Toggle navigation">
							<span class="navbar-toggler-icon"><xsl:text> </xsl:text></span>
						</button>
						<span class="d-block d-sm-none">
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
						</span>
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
										<div class="dropdown-menu">
											<a class="dropdown-item text-uppercase" href="/o:szd.werke/sdef:TEI/get?locale={$locale}">
												<i18n:text>works</i18n:text> 
											</a>
											<a class="dropdown-item text-uppercase" href="/o:szd.lebensdokumente/sdef:TEI/get?locale={$locale}">
												<i18n:text>personaldocument</i18n:text>
											</a>
											<!--<a class="dropdown-item text-uppercase" href="/o:szd.korrespondenzen/sdef:TEI/get?locale={$locale}">
												<xsl:value-of select="if($locale='en') then 'Correspondence' else 'Korrespondenzen'"/>
											</a>-->
										</div>
									</li>
									<li class="nav-item dropdown">
										<a class="navtext dropdown-toggle text-uppercase" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
											<i18n:text>collections</i18n:text>
										</a>
										<div class="dropdown-menu">
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
										<div class="dropdown-menu">
											<a class="dropdown-item text-uppercase" href="/o:szd.thema.4/sdef:TEI/get?locale={$locale}">
												<xsl:value-of select="if ($locale = 'en') then ('Stefan Zweigs Autograph Collection') else ('Stefan Zweigs Autographensammlung')"/>
											</a>
											<a class="dropdown-item text-uppercase" href="/o:szd.thema.2/sdef:TEI/get?locale={$locale}">
												<xsl:value-of select="if ($locale = 'en') then ('Stefan Zweig at work') else ('Wie Stefan Zweig schreibt')"/>
											</a>
											<a class="dropdown-item text-uppercase" href="/o:szd.thema.3/sdef:TEI/get?locale={$locale}">
												<xsl:value-of select="if ($locale = 'en') then ('Stefan Zweigs Libraries') else ('Stefan Zweigs Bibliotheken')"/>
											</a>
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
										<div class="dropdown-menu">
											<a class="dropdown-item text-uppercase" href="/o:szd.personen/sdef:TEI/get?locale={$locale}">
												<i18n:text>persons</i18n:text>
											</a>
											<a class="dropdown-item text-uppercase" href="/o:szd.standorte/sdef:TEI/get?locale={$locale}">
												<i18n:text>locations</i18n:text>
											</a>
											<!--<a class="dropdown-item text-uppercase" href="/o:szd.werkindex/sdef:TEI/get?locale={$locale}">
												<xsl:value-of select="if ($locale = 'en') then ('Works') else ('Werke')"/>
											</a>-->
											<a class="dropdown-item text-uppercase" href="https://de.wikisource.org/wiki/Stefan_Zweig/Erstausgaben" target="_blank">
												<i18n:text>firstedition</i18n:text>
											</a>
											<a class="dropdown-item text-uppercase" href="https://zweig.fredonia.edu" target="_blank">
												<i18n:text>bibliography</i18n:text>
											</a>
										</div>
									</li>
									<li class="nav-item">
										<a class="navtext text-uppercase" href="{concat($server, '/archive/objects/o:szd.glossar/methods/sdef:SKOS/get?locale=',$locale)}">
											<i18n:text>glossary</i18n:text>
										</a>
									</li>
									<li class="nav-item dropdown">
										<a class="navtext dropdown-toggle text-uppercase" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
											<xsl:value-of select="if ($locale = 'en') then ('About') else ('Projekt')"/>
										</a>
										<div class="dropdown-menu">
											<a class="dropdown-item text-uppercase" href="{concat($server, '/archive/objects/context:szd/methods/sdef:Context/get?mode=about&amp;locale=',$locale)}">
												<xsl:value-of select="if ($locale = 'en') then ('About') else ('Projekt')"/>
											</a>
											<a class="dropdown-item text-uppercase" href="{concat($server, '/archive/objects/context:szd/methods/sdef:Context/get?mode=miscellaneous&amp;locale=',$locale)}">
												<xsl:value-of select="if ($locale = 'en') then ('Miscellaneous') else ('Verschiedenes')"/>
											</a>
										</div>
									</li>
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
													<input class="form-control border small" id="n$1" name="$1" type="text" lang="{$locale}">
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
													<div class="input-group-prepend small">
														<button type="submit" class="btn small icon_suche">
															<img src="{$Icon_suche}" alt="Search" height="20"/>
														</button>
													</div>
												</div>
											</div>
										</form>
									</li>
									<!-- ////////// -->
									<!-- DATABASKET -->
									<li class="nav-item d-none d-sm-block pt-3 pl-4">
										<a href="{concat('/archive/objects/context:szd/methods/sdef:Context/get?mode=databasket&amp;locale=', $locale)}" style="text-decoration:none;">
											<xsl:choose>
												<xsl:when test="$locale = 'en'">
													<xsl:attribute name="title"><xsl:text>Objects can be saved to the data cart and exported</xsl:text></xsl:attribute>
												</xsl:when>
												<xsl:otherwise>
													<xsl:attribute name="title"><xsl:text>Im Datenkorb können Objekte gespeichert und exportiert werden</xsl:text></xsl:attribute>
												</xsl:otherwise>
											</xsl:choose>
												<img src="{$Icon_datenkorb}" class="img-fluid icon_navbar" alt="Datenkorb"/>
											<span class="small" id="db_static">
												<xsl:text> </xsl:text>
											</span>
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
				</header>
				
				<!-- //////////////////////////////////////////////////////////// -->
				<!-- ///CONTENT/// -->
				<main class="container" >
					<div id="loading">
						<div class="d-flex justify-content-center" >
							<div class="spinner-border" role="status" id="loading_spinner">
								<span class="sr-only">Loading...</span>
							</div>
						</div>
					</div>
					
					<xsl:call-template name="content"/>
				</main>

				<!-- //////////////////////////////////////////////////////////// -->
				<!-- ///FOOTER/// -->
				<footer class="footer d-print-none">
				<div class="container">
					<div class="card">
						<div class="card-body">
							<hr/>
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
										<span class="text-center text-uppercase">
											<xsl:choose>
												<xsl:when test="$locale = 'en'">
													<xsl:text>PROJECT MANAGEMENT</xsl:text>
												</xsl:when>
												<xsl:otherwise>PROJEKTTRÄGER</xsl:otherwise>
											</xsl:choose>
										</span>
									</div>
									<div class="col-sm-3">
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
										<span class="text-center text-uppercase">
											<xsl:choose>
												<xsl:when test="$locale = 'en'">
													<xsl:text>Project partner</xsl:text>
												</xsl:when>
												<xsl:otherwise>Projektpartner</xsl:otherwise>
											</xsl:choose>
										</span>
									</div>
									<div class="col-sm-3">
										<xsl:text> </xsl:text>
									</div>
								</div>
								<div class="row">
									<div class="col-sm-3">
										<a target="_blank">
											<xsl:call-template name="getURL_EN_DE">
												<xsl:with-param name="URL_EN" select="'https://www.uni-salzburg.at/index.php?id=72&amp;L=1'"/>
												<xsl:with-param name="URL_DE" select="'https://www.uni-salzburg.at/index.php?id=72'"/>
											</xsl:call-template>
											<img class="footer_img"   style="max-width: 65%;"
												src="{concat($server, $gamsdev, '/img/LAS_Logo.gif')}"
												alt="Logo LAS"/></a>
									</div>
									<div class="col-sm-3">
										<a href="http://gams.uni-graz.at/archive/objects/context:gams/methods/sdef:Context/get?mode=dataprotection&amp;locale={$locale}"  target="_blank" class="text-uppercase text-center mt-5">
											<i18n:text>privacy</i18n:text>
										</a>
									</div>
									<div class="col-sm-2">
										<a target="_blank">
											<xsl:call-template name="getURL_EN_DE">
												<xsl:with-param name="URL_EN" select="'http://gams.uni-graz.at/archive/objects/context:gams/methods/sdef:Context/get?mode=&amp;locale=en'"/>
												<xsl:with-param name="URL_DE" select="'http://gams.uni-graz.at'"/>
											</xsl:call-template>
											<img class="footer_img"   
												src="/templates/img/gamslogo_schwarz.gif"
												alt="{$gams}"/>
										</a>
									</div>
									<div class="col-sm-2">
										<a href="http://www.fotohof.at" target="_blank">
											<img class="footer_img"
												src="{concat($server, $gamsdev, '/img/Fotohof.jpg')}"
												alt="Fotohof"/>
										</a>
									</div>
									<div class="col-sm-2">
										<a href="https://web.nli.org.il/sites/NLI/english" target="_blank">
											<img class="footer_img"
												src="{concat($server, $gamsdev, '/img/logo_NLI.png')}"
												alt="The National Library of Israel"/>
										</a>
									</div>
								</div>
								<div class="row">
									<div class="col-sm-3">
										<a target="_blank" class="align-self-end">
											<xsl:call-template name="getURL_EN_DE">
												<xsl:with-param name="URL_EN" select="'https://www.uni-salzburg.at/index.php?id=52&amp;L=1'"/>
												<xsl:with-param name="URL_DE" select="'https://www.uni-salzburg.at'"/>
											</xsl:call-template>
											<img class="footer_img" style="max-width: 65%;"
												src="{concat($server, $gamsdev, '/img/uni_salzburg.jpg')}"
												alt="Logo Universität Salzburg"/>
										</a>
									</div>
									<div class="col-sm-3">
										<a target="_blank">
											<xsl:call-template name="getURL_EN_DE">
												<xsl:with-param name="URL_EN" select="'https://creativecommons.org/licenses/by-nc/4.0/deed.en'"/>
												<xsl:with-param name="URL_DE" select="'https://creativecommons.org/licenses/by-nc/4.0/deed.de'"/>
											</xsl:call-template>
											<img class="footer_img" src="/templates/img/by.png" alt="Lizenz" style="max-width: 41%;margin-top: 4%;"/>
										</a>
									</div>
									<div class="col-sm-2">
										<a target="_blank">
											<xsl:call-template name="getURL_EN_DE">
												<xsl:with-param name="URL_EN" select="'https://informationsmodellierung.uni-graz.at/en/'"/>
												<xsl:with-param name="URL_DE" select="'https://informationsmodellierung.uni-graz.at'"/>
											</xsl:call-template>
											<img class="footer_img"  style="max-width: 32%;margin-top:6%"
												src="/templates/img/ZIM_blau.png"
												alt="{$zim-acdh}"/>
										</a>
										<xsl:text> </xsl:text>
										<a target="_blank" >
											<xsl:call-template name="getURL_EN_DE">
												<xsl:with-param name="URL_EN" select="'https://www.uni-graz.at/en/'"/>
												<xsl:with-param name="URL_DE" select="'https://www.uni-graz.at'"/>
											</xsl:call-template>
											<img class="footer_img" src="/templates/img/logo_uni_graz_4c.jpg"  style="max-width: 32%;margin-top:6%" 
												title="Universität Graz" alt="Logo Uni Graz"/>
											<xsl:text> </xsl:text>
										</a>
										
									</div>
									<div class="col-sm-2">
										<a href="http://fredonia.libguides.com/archives/zweig" target="_blank">
											<img class="footer_img"
												src="{concat($server, $gamsdev, '/img/fredonia.png')}"
												alt="Reed Library – Stefan Zweig Collection, Fredonia"/>
										</a>
									</div>
									<div class="col-sm-2">
										<a target="_blank">
											<xsl:call-template name="getURL_EN_DE">
												<xsl:with-param name="URL_EN" select="'https://www.dla-marbach.de/en/'"/>
												<xsl:with-param name="URL_DE" select="'https://www.dla-marbach.de/'"/>
											</xsl:call-template>
											<img class="footer_img" src="{concat($server, $gamsdev, '/img/marbach.jpg')}" style="margin-top:10%" alt="Deutsches Literaturarchiv Marbach"/>
										</a>
									</div>
								</div>
							</div>
						
						</div>
					</div>
				</div>
				</footer>
				
			</body>
		</html>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<!-- @href with url for en and de landing page -->
	<xsl:template name="getURL_EN_DE">
		<xsl:param name="URL_DE"/>
		<xsl:param name="URL_EN"/>
		<xsl:attribute name="href">
			<xsl:choose>
				<xsl:when test="$locale='en'">
					<xsl:value-of select="$URL_EN"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$URL_DE"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:figure[t:graphic/@url]">
		<xsl:choose>
			<xsl:when test="t:caption/t:ref/@target">
				<figure class="text-center pt-4 pb-3">
					<a href="{t:caption/t:ref/@target}">
						<img class="img-fluid mx-auto d-block w-50" src="{t:graphic/@url}" alt="Image"/>
					</a>
					<figcaption>
						<xsl:apply-templates select="t:caption"/>
					</figcaption>
				</figure>
			</xsl:when>
			<xsl:when test="t:caption|t:figDesc/t:caption">
				<figure class="text-center pt-4 pb-3">
					<a class="fancybox" data-fancybox-group="group" href="{concat('https://gams.uni-graz.at/', $PID, '/', t:graphic/@url)}">	
						<img class="img-fluid mx-auto d-block w-50" src="{concat('https://gams.uni-graz.at/', $PID, '/', t:graphic/@url)}" alt="Image"/>
					</a>
					<figcaption>
						<xsl:apply-templates select="t:caption"/>
					</figcaption>					
				</figure>
			</xsl:when>
			<xsl:when test="ancestor::t:div[@type = 'miscellaneous']">
				<figure class="text-center pt-4 pb-3">
					<img class="img-fluid mx-auto d-block w-50" src="{t:graphic/@url}" alt="Image"/>
				</figure>
			</xsl:when>
			<xsl:otherwise>
				<img class="img-fluid mx-auto d-block" src="{t:graphic/@url}" alt="Image"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<!-- /////////////////////////////////////////////////////////// -->
	<!-- person -->
	<xsl:template match="t:name[@type='person']">
		<xsl:variable name="SZDPER" select="substring-after(@ref, '#')"/>
		<xsl:variable name="BaseURL" select="'/archive/objects/query:szd.person_search/methods/sdef:Query/get?params='"/>
		<xsl:variable name="Param" select="encode-for-uri(concat('$1|&lt;https://gams.uni-graz.at/o:szd.personen#', $SZDPER, '&gt;', ';$2|', $locale))"/>
		<xsl:variable name="QueryUrl" select="concat($BaseURL, $Param, '&amp;locale=', $locale)"/>

		<a href="{$QueryUrl}" target="_blank">
			<xsl:choose>
				<xsl:when test="$locale = 'en'">
					<xsl:attribute name="title" select="'Search query'"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="title" select="'Suchanfrage'"/>
				</xsl:otherwise>
			</xsl:choose>
			
			<xsl:apply-templates/>
		</a>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<!-- miscellaneous datastream in context:szd -->
	<xsl:template match="t:div[@type='miscellaneous']">
		<div class="card-body border-bottom">
			<xsl:if test="@n">
				<xsl:attribute name="id" select="concat('miscellaneous.', @n)"/>
			</xsl:if>
			<xsl:apply-templates/>
		</div>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:head[parent::t:div[@type='miscellaneous']]">
		<h2 class="color mt-5">
			<xsl:apply-templates/>
		</h2>
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
	<xsl:template match="t:div[@xml:lang='de'][not(@type)]">
		<xsl:apply-templates/>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:div[@xml:lang='en'][not(@type)]">
		<xsl:apply-templates/>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:head">
		<h3>
			<xsl:apply-templates/>
		</h3>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:note[@type='footnote']">
		<!-- numbering done by css -->
		<a href="#{generate-id()}">
			<xsl:if test="t:bibl">
				<xsl:attribute name="title">
					<xsl:value-of select="normalize-space(t:bibl)"/>
				</xsl:attribute>
			</xsl:if>
			<span class="footnote small"/>
		</a>
	</xsl:template>

	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:p">
		<xsl:if test="@style = 'horizontal'">
			<hr/>
		</xsl:if>
		<p class="card-text">
			<xsl:if test="@style = 'center'">
				<xsl:attribute name="class" select="'text-center'"/>
			</xsl:if>
			<xsl:apply-templates/>
		</p>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:list">
		<ul><xsl:apply-templates/></ul>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:item">
		<li><xsl:apply-templates/></li>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:hi[@style='italic']">
		<i><xsl:apply-templates></xsl:apply-templates></i>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:hi[@style='superscript']">
		<sup><xsl:apply-templates></xsl:apply-templates></sup>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:hi[@style='bold']">
		<strong><xsl:apply-templates></xsl:apply-templates></strong>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:hi[@style='underline']">
		<u><xsl:apply-templates></xsl:apply-templates></u>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:hi[@style='preprint']">
		<span style="font-family: 'Courier', monospace;">
			<xsl:if test="t:note">
				<xsl:attribute name="title" select="normalize-space(t:note)"/>
			</xsl:if>
			<xsl:apply-templates/>
		</span>
	</xsl:template>
		
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:hi[@style='uppercase']">
		<span class="text-uppercase"><xsl:apply-templates></xsl:apply-templates></span>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:del[@rend='strikethrough']">
		<strike>
			<xsl:if test="t:note">
				<xsl:attribute name="title" select="'Streichung'"/>
			</xsl:if>
			<xsl:apply-templates/></strike>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:add">
		<span class="text-secondary">
			<xsl:if test="@place">
					<xsl:choose>
						<xsl:when test="@place = 'above'">
							<xsl:attribute name="title">
								<xsl:text>Einfügung über der Zeile</xsl:text>
							</xsl:attribute>
						</xsl:when>
						<xsl:when test="@place = 'below'">
							<xsl:attribute name="title">
								<xsl:text>Einfügung unter der Zeile</xsl:text>
							</xsl:attribute>
						</xsl:when>
						<xsl:when test="@place = 'pasteover'">
							<xsl:attribute name="title">
								<xsl:text>Über den ursprünglichen Text geschrieben</xsl:text>
							</xsl:attribute>
						</xsl:when>
						<xsl:when test="@place = 'inline'">
							<xsl:attribute name="title">
								<xsl:text>Einfügung innerhalb der Zeile</xsl:text>
							</xsl:attribute>
						</xsl:when>
						<xsl:otherwise/>
					</xsl:choose>		
			</xsl:if>
			<xsl:apply-templates/>
		</span>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:sic">
		<span><xsl:apply-templates/><xsl:text> [sic] </xsl:text></span>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:hi[@rend = 'mark']">
		<mark><xsl:apply-templates></xsl:apply-templates></mark>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:hi[@style = 'color']">
		<span class="color"><xsl:apply-templates></xsl:apply-templates></span>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:media[@mimeType = 'audio/mp3']">
		<audio controls="true">
			<source src="{@url}" type="audio/mpeg"/>
			Your browser does not support the audio element.
		</audio>
	</xsl:template>
	
	<!-- //////////////////////////////////////////////////////////// -->
	<xsl:template match="t:ref[@target]">
		<a target="_blank">
			<xsl:choose>
				<xsl:when test="@type ='issue'">
					<xsl:attribute name="href" select="concat(@target, '/sdef:TEI/get?locale=', $locale)"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="href" select="@target"/>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:if test="@style='italic'">
				<xsl:attribute name="class" select="'font-italic'"/>
			</xsl:if>
			<xsl:if test="@style = 'button'">
				<xsl:attribute name="class"><xsl:value-of select="'btn btn-secondary btn-sm'"/></xsl:attribute>
			</xsl:if>
			<xsl:apply-templates/>
		</a>
	</xsl:template>

	<!-- //////////////////////////////////////////////////////////// -->
	<!-- @href starttext -->
	<xsl:template match="t:span[@type='href']">
		<xsl:choose>
			<xsl:when test="contains(@target, 'mailto:')">
				<a href="{@target}">
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
					<span class="btn-link" onclick="jump_to_id_switching_language('{concat('/', $PID, '/sdef:TEI/get?locale=de')}')">DE</span>
					<span class="text-dark pl-1 pr-1">|</span>
					<span class="btn-link" onclick="jump_to_id_switching_language('{concat('/', $PID, '/sdef:TEI/get?locale=en')}')">EN</span>
				</xsl:otherwise>
			</xsl:choose>
		</span>
	</xsl:template>

</xsl:stylesheet>
