<?xml version="1.0" encoding="UTF-8"?>

<!-- 
    Project: GAMS Projekttemplate
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
    Author: Christopher Pollin
    Last update: 2019
 -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
	xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:owl="http://www.w3.org/2002/07/owl#" xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:skos="http://www.w3.org/2004/02/skos/core#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" exclude-result-prefixes="#all">

	<xsl:include href="szd-static.xsl"/>
	<xsl:include href="szd-Templates.xsl"/>

	<xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>

	<!-- define this variables according to your ontolog: das könnten dann die params sein für eien Methode-->
	<!-- PID of your Ontology  -->
	<xsl:variable name="PID" select="'o:szd.ontology'"/>
	<!-- URI  -->
	<xsl:variable name="URI" select="concat('http://glossa.uni-graz.at/', $PID, '/ONTOLOGY')"/>
	<!-- LANGUAGE -->
	<xsl:variable name="LANGUAGE">
		<xsl:choose>
			<xsl:when test="$locale = 'de'">
				<xsl:text>de</xsl:text>
			</xsl:when>
			<xsl:when test="$locale = 'en'">
				<xsl:text>en</xsl:text>
			</xsl:when>
			<!-- default langauge is german -->
			<xsl:otherwise>
				<xsl:text>de</xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>

	<!-- ///PERSONENLISTE/// -->
	<xsl:template name="content">
		<section class="row">
			<!-- header -->
			<article class="col-md-12 col-sm-12 panel">
				
				<!-- //////////////////////////////////////////////////////////// -->
				<!-- HEADER -->
				<xsl:call-template name="PageHeader">
					<xsl:with-param name="Titel" select="'NACHLASS-ONTOLOGIE'"/>
					<xsl:with-param name="PID" select="'o:szd.ontology'"/>
				</xsl:call-template>
				
				<!-- //////////////////////////////////////////////////////////// -->
				<!-- /// PAGE-CONTENT /// -->
				<div class="row">
					<!-- CLASS -->
          			<h2 style="font-size:30px; padding-left: 50px; padding-top:40px;">
						<xsl:text>Klassen</xsl:text>
					</h2>
					<xsl:apply-templates select="//rdfs:Class | //owl:Class"/>
				</div>
				<div class="row">
					<!-- OBJECT PROPERTY -->
					<h2 style="font-size:30px; padding-left: 50px; padding-top:40px;">
						<xsl:text>Relationen</xsl:text>
					</h2>
					<xsl:apply-templates select="//rdf:Property  | //owl:ObjectProperty"/>
					
					<!--
        	        <xsl:for-each select="//rdf:Property[contains(rdfs:range/@rdf:resource, 'o:szd.nachlass')]">
        	                    <xsl:variable name="SZDID" select="substring-after(@rdf:about, '#')"/>
        	                    <xsl:variable name="QueryUrl" 
        	                        select="concat('/archive/objects/query:szd.category_search/methods/sdef:Query/get?params=$1|&lt;https%3A%2F%2Fgams.uni-graz.at%2Fo%3Aszd.nachlass%23', $SZDID, '&gt;')"/>
        	           <xsl:choose>
        	                       
        	            <xsl:when test="skos:example">
        	                <a href="{skos:example/@rdf:resource}" target="_blank" data-toggle="tooltip" title="Zum Datensatz" >
        	                    <h3 style="font-size:26px; padding-left: 100px;">
        	                        <xsl:value-of select="rdfs:label[@xml:lang='de']"/>
        	                    </h3>
        	                </a>
        	                <div  style="margin-left: 100px; margin-right: 100px;">
        	                    <p><xsl:value-of select="rdfs:comment[@xml:lang='de']"/></p>
        	                </div>/archive/objects/o:szd.nachlhttp://glossa.uni-graz.at/o:szd.nachlass/ONTOLOGYass/datastreams/ONTOLOGY/content
        	            </xsl:when>
        	            <xsl:otherwise>
        	                <a href="{$QueryUrl}" target="_blank"
        	                    data-toggle="tooltip" title="Suche">
        	                    <h3 style="font-size:26px; padding-left: 100px;">
        	                        <xsl:value-of select="rdfs:label[@xml:lang='de']"/>
        	                        <xsl:text> </xsl:text><img src="{$Icon_suche_template}" class="img-responsive icon" alt="Standort" title="Duche"/>
        	                    </h3>
        	                </a>
        	                <div  style="margin-left: 150px; margin-right: 100px;">
        	                    <p><xsl:value-of select="rdfs:comment[@xml:lang='de']"/></p>
        	                </div>
        	            </xsl:otherwise>
        	           </xsl:choose> 
        	            
        	        </xsl:for-each> 
        	        -->
				</div>

				<!-- ///////////////////////////////////////////////////////////// -->
				<!-- WebVOWL -->
				<div class="row" id="Visualisation">
					<h2>Visualisierung</h2>
					<embed src="{concat('http://visualdataweb.de/webvowl/#iri=', $URI)}" height="1000px" width="100%"/>
				</div>
				
			</article>
		</section>
	</xsl:template>

	<xsl:template match="//rdfs:Class | //owl:Class">
		<div id="{substring-after(rdf:about, '#')}">
			<h3>
				<xsl:value-of select="rdfs:label[@xml:lang = $LANGUAGE]"/>
			</h3>
			<!-- create Table -->
			<xsl:call-template name="createTable"/>
		</div>
	</xsl:template>
	
		<xsl:template match="//rdf:Property | //owl:ObjectProperty">
		<div id="{substring-after(rdf:about, '#')}">
			<h3>
				<xsl:value-of select="rdfs:label[@xml:lang = $LANGUAGE]"/>
			</h3>
			<!-- create Table -->
			<xsl:call-template name="createTable"/>
		</div>
	</xsl:template>


	<!--
 ///////////////////////////////////////////////////////////// 
-->
	<!-- createTable -->
	<xsl:template name="createTable">
		<div class="table-responsive">
			<table class="table table-bordered" id="{current-grouping-key()}">
				<tbody>
					<xsl:if test="rdfs:subClassOf">
						<tr class="d-flex">
							<td class="col-md-2" style="font-weight: bold;">Subclass of</td>
							<td class="col-md-10">
								<xsl:for-each select="rdfs:subClassOf/@rdf:resource">
									<a href="{.}">
									  <xsl:choose>
											<xsl:when test="contains(., 'cidoc-crm')">
												<xsl:value-of select="substring-after(., 'cidoc-crm/')"/>
											</xsl:when>
											<xsl:when test="contains(., '#')">
												<xsl:value-of select="substring-after(., '#')"/>
											</xsl:when>
											<xsl:otherwise>
												<xsl:variable name="currentClass" select="."/>
												<xsl:value-of select="//rdfs:Class[@rdf:about = $currentClass]/rdfs:label[@xml:lang = $LANGUAGE]"/>
											</xsl:otherwise>
										</xsl:choose> 
									</a>
									<br/>
								</xsl:for-each>
							</td>
						</tr>
					</xsl:if>
					<!-- DESCRIPTION -->
					<xsl:if test="rdfs:comment[@xml:lang = $LANGUAGE]">
					<tr class="d-flex">
						<td class="col-md-2" style="font-weight: bold;">Description</td>
						<td class="col-md-10">
							<xsl:value-of select="rdfs:comment[@xml:lang = $LANGUAGE]"/>
						</td>
					</tr>
					</xsl:if>
					<!-- EXAMPLE -->
					<xsl:if test="skos:example">
						<tr class="d-flex">
							<td class="col-md-2" style="font-weight: bold;">Usage</td>
							<td class="col-md-10">
								<xsl:text> </xsl:text>
							</td>
						</tr>
					</xsl:if>
					<!-- seeAlso -->
					<xsl:if test="rdfs:seeAlso/@rdf:resource">
						<tr class="d-flex">
							<td class="col-md-2" style="font-weight: bold;">seeAlso</td>
							<td class="col-md-10">
								<xsl:for-each select="rdfs:seeAlso/@rdf:resource">
									<a href="{.}" target="_blank">
										<xsl:value-of select="substring-before(substring-after(., '.'), '/')"/>
									</a>
								</xsl:for-each>
							</td>
						</tr>
					</xsl:if>
					<!-- DOMAIN -->
					<xsl:variable name="Domain" select="rdfs:domain/@rdf:resource | //rdf:Property[rdfs:domain/@rdf:resource = current-grouping-key()]"/>
					<xsl:if test="$Domain">
						<tr class="d-flex">
							<td class="col-md-2" style="font-weight: bold;">Domain</td>
							<td class="col-md-10">
								<xsl:for-each select="//rdfs:Class[@rdf:about = $Domain]/rdfs:label[@xml:lang = $LANGUAGE]">
									<a href="{concat('#', translate(.,' ',''))}" onclick="scrolldown(this)" style="margin-right: 40px;">
										<xsl:value-of select="."/>
									</a>
									<xsl:text> </xsl:text>
								</xsl:for-each>
								<xsl:for-each select="$Domain/rdfs:label[@xml:lang = $LANGUAGE]">
									<a href="{concat('#', translate(.,' ',''))}" onclick="scrolldown(this)" style="margin-right: 40px;">
										<xsl:value-of select="."/>
									</a>
									<xsl:text> </xsl:text>
								</xsl:for-each>
							</td>
						</tr>
					</xsl:if>
					<!-- RANGE -->
					<xsl:variable name="Range" select="rdfs:range/@rdf:resource | //rdf:Property[rdfs:range/@rdf:resource = current-grouping-key()]"/>
					<xsl:if test="$Range">
						<tr class="d-flex">
							<td class="col-md-2" style="font-weight: bold;">Range</td>
							<td class="col-md-10">
								<xsl:choose>
									<xsl:when test="//rdfs:Class[@rdf:about = $Range]/rdfs:label[@xml:lang = $LANGUAGE]">
										<xsl:for-each select="//rdfs:Class[@rdf:about = $Range]/rdfs:label[@xml:lang = $LANGUAGE]">
											<a href="{concat('#', translate(.,' ',''))}" onclick="scrolldown(this)" style="margin-right: 40px;">
												<xsl:value-of select="."/>
											</a>
											<xsl:text> </xsl:text>
										</xsl:for-each>
									</xsl:when>
									<xsl:when test="$Range/rdfs:label[@xml:lang = $LANGUAGE]">
										<xsl:for-each select="$Range/rdfs:label[@xml:lang = $LANGUAGE]">
											<a href="{concat('#', translate(.,' ',''))}" onclick="scrolldown(this)" style="margin-right: 40px;">
												<xsl:value-of select="."/>
											</a>
											<xsl:text> </xsl:text>
										</xsl:for-each>
									</xsl:when>
									<xsl:otherwise>
										<xsl:for-each select="$Range">
											<a href="{.}" style="margin-right: 40px;">
												<xsl:value-of select="substring-after(., '#')"/>
											</a>
										</xsl:for-each>
									</xsl:otherwise>
								</xsl:choose>
							</td>
						</tr>
					</xsl:if>
				</tbody>
			</table>
		</div>
	</xsl:template>

</xsl:stylesheet>
