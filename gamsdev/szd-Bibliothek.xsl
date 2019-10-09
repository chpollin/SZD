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
    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:i18n="http://apache.org/cocoon/i18n/2.1"
    exclude-result-prefixes="#all">
    
    <xsl:include href="szd-static.xsl"/>
	<xsl:include href="szd-Templates.xsl"/>
    <xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>

	<!-- ///BIBLIOTHEK/// -->
    <xsl:template name="content">    	
        <section class="card">
            <xsl:variable name="biblFull" select="//t:body/t:listBibl/t:biblFull"/>
            <xsl:variable name="AuthorsEditorsComposer" select="$biblFull/t:fileDesc/t:titleStmt/t:author[not(@role)] | 
                $biblFull/t:fileDesc/t:titleStmt/t:editor[not(@role)][not(preceding-sibling::t:author[not(@role)])]  |
                $biblFull/t:fileDesc/t:titleStmt/t:author[@role = 'composer'][not(preceding-sibling::t:author[not(@role)])]"/>
           
            
           
        	<!--///CALL getStickyNavbar/// called in szd-Templates -->
        	<xsl:call-template name="getStickyNavbar">
        	    <xsl:with-param name="Title">
        	        <xsl:choose>
        	            <xsl:when test="$locale = 'en'">
        	                <xsl:text>Library</xsl:text>
        	            </xsl:when>
        	            <xsl:otherwise>
        	                <xsl:text>Bibliothek</xsl:text>
        	            </xsl:otherwise>
        	        </xsl:choose>
        	    </xsl:with-param>
        	    <xsl:with-param name="Content" select="$AuthorsEditorsComposer"/>
        		<xsl:with-param name="PID" select="$PID"/>
        	    <xsl:with-param name="locale" select="$locale"/>
        	</xsl:call-template>
            
           
        		
             <!-- /// PAGE-CONTENT /// -->
            <article class="card-body" id="content">	
        	<!-- select every biblFull and group t:author[@role='Verfasser'][1] and all t:editor[@role='Herausgeber'] if no author is mentioned, -->
                <xsl:for-each-group select="$biblFull" group-by="t:fileDesc/t:titleStmt/t:author[not(@role)] | t:fileDesc/t:titleStmt/t:editor[not(@role)][not(preceding-sibling::t:author[not(@role)])] | t:fileDesc/t:titleStmt/t:author[@role = 'composer'][not(preceding-sibling::t:author[not(@role)])]"> 
                    <xsl:sort select="current-grouping-key()"/>
                    
                    <xsl:call-template name="getfirstforABC">
                        <xsl:with-param name="Persons" select="$AuthorsEditorsComposer"/>
                        <xsl:with-param name="CurrentNodes" select="current-grouping-key()"/>
                    </xsl:call-template>
                   
                   
                        <!-- Go through all entries connected to xpath selection in group-by -->
                        <!-- list ccontent -->
                          <div class="list-group">
                              <xsl:if test="not(position()=1)">
                                  <xsl:attribute name="class">
                                      <xsl:text>list-group mt-5</xsl:text>
                                  </xsl:attribute>
                              </xsl:if>
                           <h3>
                              <xsl:value-of select="normalize-space(current-grouping-key())"/>
                          </h3>
                           <xsl:for-each select="current-group()">
                               <xsl:sort select="normalize-space(t:fileDesc/t:titleStmt/t:title[1])"/>
                               <!-- /////////////////////////////////////////// -->
                               <!-- ENTRY -->
                               <div class="list-group-item entry db_entry shadow-sm" id="{@xml:id}">
                                   <!-- //// -->
                                   <!-- getEntry_SZDBIB_SZDAUT -->
                                    <xsl:call-template name="getEntry_SZDBIB_SZDAUT">
                                        <xsl:with-param name="locale" select="$locale"/>
                                    </xsl:call-template>
                                   <!-- //// -->
                                   <!-- FillbiblFull_SZDBIB -->
                                    <div class="card-body card-collapse collapse" id="{concat('c' , generate-id())}">
                                        <xsl:call-template name="FillbiblFull_SZDBIB">
                                            <xsl:with-param name="locale" select="$locale"/>
                                        </xsl:call-template>
                                    </div>
                               </div>
                           </xsl:for-each>
                      </div>
                    </xsl:for-each-group>
        			
        			<!-- /////////////////////////////////////////////////// -->
            		<!-- All biblFull without an author[@role = "Verfasser"] -->
                
        			<div class="list-group mt-5" id="withoutAuthor">  
                  		<h3>
                  		    <i18n:text>without_author</i18n:text>
                        </h3>
         			    <!-- select all biblFull without @Verfasser/@Herausgeber -->
        			    <xsl:for-each select="$biblFull[t:fileDesc/t:titleStmt[not(t:author[not(@role)])][not(t:editor[not(@role)])][not(t:author[@role ='composer'])]]">
						  <xsl:sort select="normalize-space(t:fileDesc/t:titleStmt/t:title[1])"/>
            		      <!-- GETENTRY -->
        			        <div class="list-group-item entry shadow-sm" id="{@xml:id}">
        			            <!-- //// -->
        			            <!-- getEntry_SZDBIB_SZDAUT -->
                			      <xsl:call-template name="getEntry_SZDBIB_SZDAUT">
                			          <xsl:with-param name="locale" select="$locale"/>
                			      </xsl:call-template>
        			            <!-- //// -->
        			            <!-- FillbiblFull_SZDBIB -->
                			        <div class="card-body card-collapse collapse" id="{concat('c' , generate-id())}">
                			            <xsl:call-template name="FillbiblFull_SZDBIB">
                			                <xsl:with-param name="locale" select="$locale"/>
                			            </xsl:call-template>
                			        </div> 
        			        </div>
            		    </xsl:for-each>
        			 </div>
            </article>
        </section>

    </xsl:template>
    
    

</xsl:stylesheet>
