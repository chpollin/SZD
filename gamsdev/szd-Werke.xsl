<?xml version="1.0" encoding="UTF-8"?>

<!-- 
    Project: Stefan zweig Digital
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
    Author: Christopher Pollin
    Last update: 2017
 -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    exclude-result-prefixes="#all">
    
    <xsl:include href="szd-static.xsl"/>
    <xsl:include href="szd-Templates.xsl"/>
	<xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>
    
    <!-- ///MANUSKRIPTE/// -->
    <xsl:template name="content">
            <section class="card">
                    <!-- call getStickyNavbar in szd-Templates.xsl -->
                    <xsl:call-template name="getStickyNavbar">
                        <xsl:with-param name="Title">
                            <xsl:choose>
                                <xsl:when test="$PID = 'o:szd.werke'">
                                    <xsl:choose>
                                        <xsl:when test="$locale = 'en'">
                                            <xsl:text>Works</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>Werke</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:when>
                                <xsl:when test="$PID = 'o:szd.lebensdokumente'">
                                    <xsl:choose>
                                        <xsl:when test="$locale = 'en'">
                                            <xsl:text>Personal Documents</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>Lebensdokumente</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:when>
                                <xsl:when test="$PID = 'o:szd.nli'">
                                    <xsl:choose>
                                        <xsl:when test="$locale = 'en'">
                                            <xsl:text>NLI DATA</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>NLI DATA</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:when>
                                <xsl:when test="$PID = 'o:szd.marbach'">
                                    <xsl:choose>
                                        <xsl:when test="$locale = 'en'">
                                            <xsl:text>Marbach Werke</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>Marbach Werke</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:when>
                                <xsl:otherwise><xsl:text>Error: check PID</xsl:text></xsl:otherwise>
                            </xsl:choose>
                        </xsl:with-param>
                        <xsl:with-param name="Category" select="//t:body/t:listBibl/t:biblFull/t:profileDesc/t:textClass/t:keywords/t:term[@type='classification'][@xml:lang=$locale]"/>
                        <xsl:with-param name="PID" select="$PID"/>
                        <xsl:with-param name="locale" select="$locale"/>
                        <xsl:with-param name="GlossarRef">
                            <xsl:choose>
                                <xsl:when test="$PID = 'o:szd.lebensdokumente'">
                                    <xsl:text>PersonalDocuments</xsl:text>
                                    <!--<xsl:choose>
                                        <xsl:when test="$locale = 'en'">
                                            <xsl:text>PersonalDocuments</xsl:text>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>Lebensdokumente</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>-->
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:text>Works</xsl:text>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:with-param>
                    </xsl:call-template>

                    <!-- /// PAGE-CONTENT /// -->
                    <div id="content">
                        
                        <!-- for each bibFull group by @type='Ordnungskategorie' (like 'Rede') -->
                        <xsl:for-each-group select="//t:body/t:listBibl/t:biblFull" group-by="t:profileDesc/t:textClass/t:keywords/t:term[@type='classification'][@xml:lang=$locale]">
                            <xsl:sort select="current-grouping-key()"/>
                                <div class="col-12"  id="{translate(current-grouping-key(), ' ', '')}">
                                <!-- ORDNUNGSKATEGORIE -->
                                <h2>
                                    <xsl:choose>
                                        <xsl:when test="position() = 1 ">
                                            <xsl:attribute name="class"><xsl:text>headerEntryList</xsl:text></xsl:attribute>
                                        </xsl:when>
                                        <xsl:otherwise><xsl:attribute name="class"><xsl:text>headerEntryList mt-5</xsl:text></xsl:attribute></xsl:otherwise>
                                    </xsl:choose>
                                    <xsl:value-of select="upper-case(normalize-space(current-grouping-key()))"/>
                                </h2>
 
                                <!-- /////////////////////////////////////////// -->    
                                <!-- for each bibFull group by @type='Einheitssachtitel'
                                     there are Einheitssachtitel with translation and some without-->
                                    <xsl:for-each-group select="current-group()"  group-by="t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel'][@xml:lang = $locale] | 
                                        t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel'][not(@xml:lang)]"> 
                                        <xsl:sort select="t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel'][@xml:lang = $locale] | 
                                            t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel'][not(@xml:lang)]"/>
                                        <div class="list-group mt-4">
                                        <h3 id="{concat('mt', generate-id())}">
                                            <xsl:value-of select="current-grouping-key()"/>
                                        </h3>
                                        <xsl:for-each select="current-group()">
                                            <xsl:sort select="@ana"/>   
                                            <!-- /////////////////////////////////////////// -->
                                            <!-- ENTRY -->
                                            <div class="list-group-item entry db_entry shadow-sm" id="{@xml:id}">
                                                <!-- /////////////////////////////////////////// -->
                                                <xsl:call-template name="AddData-Databasket"/>
                                                
                                                <!-- HREF SCAN -->
                                                <!-- if a PID exists in the TEI make a @href to the viewer and a different col-md-alignment -->
                                                <xsl:variable name="PID_IMAGE" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:altIdentifier/t:idno[@type='PID']"/>
                                                <xsl:variable name="externIIIFManifest" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:altIdentifier[@type='extern_iiif']/t:idno[@type='manifest']"/>
                                                <xsl:variable name="currentCollection" select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:altIdentifier/t:idno[@type='subject']"/>
                                                
                                                <div class="card-heading bg-light row">
                                                   <!-- creating collapse id -->
                                                    <h4 class="card-title text-left col-9 small">
                                                      	<!-- TITEL | Ordnungskategorie | Signatur  -->
                                                      	<xsl:choose>
                                                      	    <xsl:when test="not(t:profileDesc/t:textClass/t:keywords/t:term[@type='classification'][@xml:lang='de'] = 'Werknotizen')">
                                                      			<a data-toggle="collapse" href="{concat('#c' , generate-id())}">
                                                      			    <span class="arrow">
                                                      			       <xsl:text>▼ </xsl:text>
                                                      			    </span>
                                                      			    <span class="font-italic">
                                                      			        <!-- TITLE -->
	                                                       			<xsl:choose>
	                                                       			    <xsl:when test="string-length(t:fileDesc/t:titleStmt/t:title[@xml:lang = $locale][not(@type)]) > 60">
	                                                       			        <xsl:value-of select="substring(t:fileDesc/t:titleStmt/t:title[@xml:lang = $locale][not(@type)], 1, 62)"/>
	                                                       			        <xsl:text>... </xsl:text>
	                                                       			    </xsl:when>
	                                                       			    <xsl:when test="string-length(t:fileDesc/t:titleStmt/t:title[1][not(@type)]) > 60">
	                                                       			        <xsl:value-of select="substring(t:fileDesc/t:titleStmt/t:title[1][not(@type)], 1, 62)"/>
	                                                       			        <xsl:text>... </xsl:text>
		                     											</xsl:when>
	                                                       				<xsl:otherwise>
	                                                       				    <!-- called in szd-Templates.xsl -->
	                                                       				    <xsl:call-template name="printEnDe">
	                                                       				        <xsl:with-param name="path" select="t:fileDesc/t:titleStmt/t:title[not(@type)]"/>
	                                                       				        <xsl:with-param name="locale" select="$locale"/>
	                                                       				    </xsl:call-template>
		                     											</xsl:otherwise>
	                                                       			</xsl:choose>
                                                            	</span>
                                                      			</a>
                                                      	        <!-- Ordnungskategorie =  -->
                                                      			<xsl:text> | </xsl:text>
                                                      			<xsl:choose>
                                                      			    <xsl:when test="t:profileDesc/t:textClass/t:keywords/t:term[@type='classification'][@xml:lang='de'] = 'Werknotizen'">
                                                      			        <span class="font-italic">
                                                      			            <!-- called in szd-Templates.xsl -->
                                                      			            <xsl:call-template name="printEnDe">
                                                      			                <xsl:with-param name="path" select="t:fileDesc/t:titleStmt/t:title"/>
                                                      			                <xsl:with-param name="locale" select="$locale"/>
                                                      			            </xsl:call-template>
                                                      			            <xsl:text>check XSLT ;)</xsl:text>
                                                            			</span>
                                                            		</xsl:when>
                                                            		<xsl:otherwise>
                                                            			<span>
                                                            			    <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:span[@xml:lang = $locale]/t:term"/>
                                                            			</span>
                                                            		</xsl:otherwise>
                                                            	</xsl:choose>
                                                      			<!-- Signatur -->
                                                      	        <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno[@type='signature']">
                                                       			  <xsl:text> | </xsl:text>
                                                      	            <xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno[@type='signature']"/>                                                                     
                                                       		   </xsl:if>
                                                      	        <!-- if the object is an enclosures -->
                                                      	        <xsl:if test="t:profileDesc/t:textClass/t:keywords/t:term[@ana='szdg:Enclosures']">
                                                      	            <xsl:choose>
                                                      	                <xsl:when test="$locale  = 'en'">
                                                      	                    <xsl:text> [Enclosures]</xsl:text>
                                                      	                </xsl:when>
                                                      	                <xsl:otherwise>
                                                      	                    <xsl:text> [Beilage]</xsl:text>
                                                      	                </xsl:otherwise>
                                                      	            </xsl:choose>
                                                      	        </xsl:if>
                                                      		</xsl:when>
                                                      		<!-- WERKNOTIZEN -->
                                                      		<xsl:otherwise>
                                                      			<a data-toggle="collapse" href="{concat('#c' , generate-id())}">
                                                      			    <span class="arrow">
                                                      			        <xsl:text>▼ </xsl:text>
                                                      			    </span>
                                                          			<span class="font-italic">
                                                                	  <xsl:value-of select="t:fileDesc/t:titleStmt/t:title[not(@type)][@xml:lang = $locale]"/>
                                                                	</span>
	                                                      		</a>
                                                      			<xsl:text> </xsl:text>
                                                      			<!-- | Signatur -->
	                                                       		<xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno">
	                                                       			<xsl:text> | </xsl:text>
	                                                       			<xsl:value-of select="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:idno"/>
	                                                       		</xsl:if>
                                                      		    <!-- if the object is an enclosures -->
                                                      		    <xsl:if test="t:profileDesc/t:textClass/t:keywords/t:term[@ana='szdg:Enclosures']">
                                                      		        <xsl:text> [Beilage]</xsl:text>
                                                      		    </xsl:if>
                                                      		</xsl:otherwise>
                                                      	</xsl:choose>
                                                    </h4>
                                                    <!-- scan, extern, thema button -->
                                                    <span class="col-2 text-center">
                                                            <xsl:choose>
                                                                <xsl:when test="$externIIIFManifest">
                                                                    <!-- http://gams.uni-graz.at/o:szd.externiiif/sdef:IIIF/getMirador?manifest=https://iiif.nli.org.il/IIIFv21/DOCID/NNL_ARCHIVE_AL21256393780005171/manifest  -->
                                                                    <xsl:variable name="externIIIFObject" select="concat('/', $PID, '/sdef:IIIF/getMirador?manifest=', $externIIIFManifest)"/>
                                                                     <a href="{$externIIIFObject}" target="_blank">
                                                                         <xsl:choose>
                                                                             <xsl:when test="$locale = 'en'">
                                                                                 <xsl:attribute name="title" select="'Access extern digital facsimile'"/>
                                                                             </xsl:when>
                                                                             <xsl:otherwise>
                                                                                 <xsl:attribute name="title" select="'Zum externen digitalen Faksimile'"/>
                                                                             </xsl:otherwise>
                                                                         </xsl:choose>
                                                                         <xsl:call-template name="printCameraIcon">
                                                                             <xsl:with-param name="locale" select="$locale"/>
                                                                         </xsl:call-template>
                                                                     </a>                                                                    
                                                                </xsl:when>
                                                                <xsl:when test="$PID_IMAGE">
                                                                    <xsl:call-template name="createViewerHref">
                                                                        <xsl:with-param name="PID_IMAGE" select="$PID_IMAGE"/>
                                                                        <xsl:with-param name="locale" select="$locale"/>
                                                                    </xsl:call-template>
                                                                </xsl:when>
                                                                <xsl:otherwise/>
                                                            </xsl:choose>
                                                            <xsl:if test="t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:altIdentifier[1]/t:idno[@type='extern'][1]">
                                                                <a href="{t:fileDesc/t:sourceDesc/t:msDesc/t:msIdentifier/t:altIdentifier[1]/t:idno[@type='extern'][1]}" target="_blank"  class="ml-1 szd_color">
                                                                    <xsl:choose>
                                                                        <xsl:when test="$locale = 'en'">
                                                                            <xsl:attribute name="title" select="'Access external resource'"/>
                                                                        </xsl:when>
                                                                        <xsl:otherwise>
                                                                            <xsl:attribute name="title" select="'Zur externen Ressource'"/>
                                                                        </xsl:otherwise>
                                                                    </xsl:choose>
                                                                    <!--  -->
                                                                    <xsl:call-template name="printCameraIcon">
                                                                        <xsl:with-param name="locale" select="$locale"/>
                                                                    </xsl:call-template>
                                                                </a>
                                                                <xsl:text> </xsl:text>
                                                            </xsl:if>
                                                            <xsl:if test="$currentCollection">
                                                                <a href="{concat('/', $currentCollection, '/sdef:TEI/get?locale=', $locale)}" target="_blank" style="color: #631a34;" class="ml-1">
                                                                    <xsl:choose>
                                                                        <xsl:when test="$locale = 'en'">
                                                                            <xsl:attribute name="title" select="'Access subject page'"/>
                                                                        </xsl:when>
                                                                        <xsl:otherwise>
                                                                            <xsl:attribute name="title" select="'Zur Themenseite'"/>
                                                                        </xsl:otherwise>
                                                                    </xsl:choose>
                                                                    <i class="fas fa-book-reader _icon"><xsl:text> </xsl:text></i>
                                                                </a>
                                                                <xsl:text> </xsl:text>
                                                            </xsl:if>
                                                            <xsl:text> </xsl:text>
                                                        </span>
                                                        <!-- databasket -->
                                                        <xsl:call-template name="getLabelDatabasket">
                                                            <xsl:with-param name="locale" select="$locale"/>
                                                            <xsl:with-param name="SZDID" select="@xml:id"/>
                                                        </xsl:call-template>
                                               </div>
                                               <!-- card which collapses -->
                                                <div class="card-body card-collapse collapse" id="{concat('c' , generate-id())}">
                                                   <!-- ///START CREATING TABLE FOR EACH BIBLFULL -->
                                                   <!-- structure the data in a table based on the TEI-structure-->
                                                   <!-- this template is used for SZDMSK and SZDLEB (Personal Documents) -->
                                                   <xsl:call-template name="FillbiblFull_SZDMSK">
                                                       <xsl:with-param name="locale" select="$locale"/>
                                                       <xsl:with-param name="PID" select="$PID"/>
                                                       <xsl:with-param name="PID_IMAGE" select="$PID_IMAGE"/>
                                                   </xsl:call-template>
                                           </div>
                                       </div>
                                    </xsl:for-each>
                                
                                </div>
                            </xsl:for-each-group>
                           </div>    
                         </xsl:for-each-group>                  
                     </div>
        </section>
    </xsl:template>
    
</xsl:stylesheet>
