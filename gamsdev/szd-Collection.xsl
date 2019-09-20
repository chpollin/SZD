<?xml version="1.0" encoding="UTF-8"?>
<!-- 
    Project: Stefan zweig Digital
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
    Author: Christopher Pollin
    Last update: 2018
 -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    exclude-result-prefixes="#all">
    
    <xsl:include href="szd-static.xsl"/>
	<xsl:include href="szd-Templates.xsl"/>
    <xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>


    <xsl:template name="content">
    	<!-- script for jumping to the correct place -->
    	<script>
    		 window.onload = function () {
    		var hash = window.location.hash.substr(1);
    		if(hash)
    		{
    		console.log(hash);
    		location.hash = "#" + hash;
    		window.scrollBy(0, -200);
    		}
    		 }
    	</script>
    	
    	<!-- //////////////////////////////////////////////////////////// -->
        <!-- ///COLLECTION/// -->
    	<!-- /// PAGE-CONTENT /// -->
        <section class="row">
            <!-- HEADER -->
        	<article class="col-md-12 col-sm-12 panel">
		        <xsl:call-template name="PageHeader">
		        	<xsl:with-param name="Titel" select="upper-case(//t:titleStmt/t:title)"/>
		        	<xsl:with-param name="PID" select="$teipid"/>
		        </xsl:call-template>
		    	
        		<!-- //////////////////////////////////////////////////////////// -->
        		<!-- EINLEITUNG -->
        		<div class="row" style="margin: 15px;">
        			<div class="col-md-12">
        				<xsl:apply-templates select="//t:body/t:div[@type = 'Einleitung']/t:p[1]"></xsl:apply-templates>
        			    <div class="collapse" id="{concat('viewdetails', generate-id(//t:body/t:div[@type = 'Einleitung']/t:p[2]))}">
                    	   <xsl:apply-templates select="//t:body/t:div[@type = 'Einleitung']/t:p[not(position() = 1)]"></xsl:apply-templates>
                    	</div>
                    	<xsl:text> </xsl:text>
        			    <a type="button" data-toggle="collapse" data-target="{concat('#viewdetails', generate-id(//t:body/t:div[@type = 'Einleitung']/t:p[2]))}" style="color:#C2A360;">Mehr erfahren</a> 
        			</div>
        		</div>
				
        	    <!-- //////////////////////////////////////////////////////////// -->
        		<!-- EINTRAG -->
        	    <div class="col-md-12">
        	        <xsl:for-each select="//t:body/t:div[@type = 'Eintrag']">
        	        	<xsl:variable name="SZDID">
        	        	    <xsl:choose>
        	        	        <xsl:when test="contains(t:head/t:title/@ref, ' ')">
        	        	            <xsl:value-of select="tokenize(normalize-space(t:head/t:title/@ref), ' ')"/>
        	        	        </xsl:when>
        	        	        <xsl:when test="contains(t:head/t:title/@ref, 'SZD')">
        	        	            <xsl:value-of select="substring-after(t:head/t:title/@ref, '#')"/>
        	        	        </xsl:when>
        	        	        <xsl:otherwise></xsl:otherwise>
        	        	    </xsl:choose>
        	        	</xsl:variable>
        	            <div class="row" style="margin: 25px; padding-top:70px;">
        	                   <!-- HEAD -->
        	                <div class="col-md-6">
        	                    <h2 style="line-height: 35px;">
        	                        <xsl:apply-templates select="t:head/t:title[1]"/>
        	                   	    <br/>
        	                   	    <xsl:apply-templates select="t:head/t:title[@type='Untertitel'][1]"/>
        						</h2>
        	                   </div>
        	                	<!-- IMAGE -->
        	                	<div class="col-md-6">
        	                	    <xsl:choose>
        	                	        <xsl:when test="t:head/t:ref">
        	                	            <a href="{t:head/t:ref}" target="_blank" style="padding-left:15px;"><h3 style="padding-left: 15px;">ZUR EXTERNEN RESSOURCE <span class="glyphicon glyphicon-link" ><xsl:text> </xsl:text></span></h3></a>
        	                	        </xsl:when>
        	                	        <xsl:otherwise>
        	                	            <xsl:for-each select="tokenize(t:head/t:title[not(@type='Untertitel')]/@facs, ' ')">
        	                	                <xsl:if test="position() = 1"><a href="{concat('/', ., '/sdef:IIIF/getMirador')}" target="_blank" title="Ansicht im Viewer">
        	                	                    <img  class="img-fluid rounded center-block" src="{concat('/', ., '/IMG.1')}" 
        	                	                        alt="{.}" width="50%"/>
        	                	                </a>
        	                	                </xsl:if>
        	                	            </xsl:for-each>
        	                	        </xsl:otherwise>
        	                	    </xsl:choose>
        	                	    <xsl:text> </xsl:text> 
        	                	</div>
        	            </div>   
        	            <div class="row" style="margin: 1px;">
        	                <xsl:choose>
        	                    <xsl:when test="contains(normalize-space(t:head/t:title/@ref), ' ')">
        	                        <xsl:attribute name="id" select="substring-before(substring-after(t:head/t:title/@ref, '#'), ' ')"/>
        	                    </xsl:when>
        	                    <xsl:otherwise>
        	                        <xsl:attribute name="id" select="substring-after(t:head/t:title/@ref, '#')"/>
        	                    </xsl:otherwise>
        	                </xsl:choose>
        	            	<div class="col-md-6">
        	            		<!-- TEXT -->
        	            		<h3>ÜBER DAS ORIGINAL</h3>
        	               		 <xsl:apply-templates select="t:p[1]"></xsl:apply-templates>
        	            		 <xsl:if test="t:p[not(position() = 1)]">
        	            		     <div class="collapse" id="{concat('viewdetails', generate-id(t:p[2]))}">
        	            		 	   <xsl:apply-templates select="t:p[not(position() = 1)]"></xsl:apply-templates>
        	            		     </div>
        	            		     <xsl:text> </xsl:text>
        	            		     <a type="button" data-toggle="collapse" data-target="{concat('#viewdetails', generate-id(t:p[2]))}" style="color:#C2A360;">Mehr erfahren</a>
        	            		 </xsl:if>
        	            	    <xsl:if test="not($SZDID = '')">
        	            	        <div style="margin-top:100px;">
        	            	            <h3>ZUM KATALOG </h3>
              	            	        <xsl:for-each select="tokenize($SZDID, '\s')">
              	            	            <xsl:variable name="helpSZDID">
              	            	                <xsl:choose>
              	            	                <xsl:when test="contains(., '#')">
              	            	                    <xsl:value-of select="substring-after(., '#')"/>
              	            	                </xsl:when>
              	            	                <xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
              	            	            </xsl:choose>
              	            	            </xsl:variable>
              	            	            <xsl:choose>
              	            	                <xsl:when test="contains(., 'SZDMSK')">
              	            	                    <a href="{concat('/o:szd.werke#', $helpSZDID)}">
              	            	                        <xsl:value-of select="$MANUSKRIPTE//t:listBibl/t:biblFull[@xml:id = $helpSZDID]//t:title[1]"/><xsl:text>, </xsl:text><xsl:value-of select="$MANUSKRIPTE//t:listBibl/t:biblFull[@xml:id = $helpSZDID]//t:idno[@type='Signatur']"/>
              	            	                    </a>
              	            	                </xsl:when>
              	            	                <xsl:when test="contains(., 'SZDLEB')">
              	            	                    <a href="{concat('/o:szd.lebensdokumente#', $helpSZDID)}">
              	            	                        <xsl:value-of select="$LEBENSDOKUMENTE//t:listBibl/t:biblFull[@xml:id = $helpSZDID]//t:title[1]"/><xsl:text>, </xsl:text><xsl:value-of select="$LEBENSDOKUMENTE//t:listBibl/t:biblFull[@xml:id = $helpSZDID]//t:idno[@type='Signatur']"/>
              	            	                    </a>
              	            	                </xsl:when>
              	            	                <!-- <xsl:when test="contains(., 'SZDBIB')">
              	            	                    <a href="{concat('/o:szd.bibliothek#',.)}">
              	            	                        bibliothek
              	            	                    </a>
              	            	                </xsl:when>-->
              	            	                <xsl:otherwise>
              	            	                    <xsl:comment>Resource not found:</xsl:comment>
              	            	                </xsl:otherwise>
              	            	            </xsl:choose>
              	            	            <br/>
              	            	        </xsl:for-each>
        	            	     </div>
        	            	    </xsl:if>
        	            	</div>
        	            	<div class="col-md-6">
        	            	    <h3>METADATEN</h3>        	            	    
        	            	    <xsl:choose>
        	            	        <xsl:when test="contains($SZDID, 'SZD')">
        	            	    <xsl:for-each select="tokenize($SZDID, '\s')">
        	            	        <xsl:variable name="helpSZDID">
        	            	            <xsl:choose>
        	            	                <xsl:when test="contains(., '#')">
        	            	                    <xsl:value-of select="substring-after(., '#')"/>
        	            	                </xsl:when>
        	            	                <xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
        	            	            </xsl:choose>
        	            	        </xsl:variable>
                    				<!-- //////////////////////////////////////////////////////////// -->
                    				<!-- METADATEN -->
                    			<xsl:if test="position()=1">
			        	            		<xsl:choose>
			        	            		    <xsl:when test="contains(., 'SZDMSK')">
			        	            		        <xsl:for-each select="$MANUSKRIPTE//t:listBibl/t:biblFull[@xml:id= $helpSZDID]">
			        	            					<!-- this template is also used for the metadata representation für Collections in szd-templates -->
			        	            					<xsl:call-template name="FillbiblFull_SZDMSK"/>
			        	            				</xsl:for-each>
			        	            			</xsl:when>
			        	            		    <xsl:when test="contains(., 'SZDLEB')">
			        	            		        
			        	            		        <xsl:for-each select="$LEBENSDOKUMENTE//t:listBibl/t:biblFull[@xml:id = $helpSZDID]">
			        	            					<!-- this template is also used for the metadata representation für Collections in szd-templates -->
			        	            					<xsl:call-template name="FillbiblFull_SZDMSK"/>
			        	            				</xsl:for-each>
			        	            			</xsl:when>
			        	            			<!--<xsl:when test="substring-before($SZDID, '.') = 'SZDBIB'">
			        	            				<xsl:value-of select="$BIBLIOTHEK//t:listBibl/t:biblFull[@xml:id= $SZDID]"/>
			        	            			
			        	            			</xsl:when>-->
			        	            			<xsl:otherwise>
			        	            				<xsl:comment>Resource not found:</xsl:comment>
			        	            			</xsl:otherwise>
			        	            		</xsl:choose>
	                    					
	                    				
                    			</xsl:if>	
        	            			
        	            	    </xsl:for-each>
        	            	    </xsl:when>
	                    				<xsl:otherwise>
	                    				   <xsl:text> </xsl:text>
	                    				</xsl:otherwise>
                    		        </xsl:choose>
        	            		<xsl:text> </xsl:text>
        	            		
        	            	</div>
        	            </div>
        	           	         
        	        </xsl:for-each>
        	    </div>
        		
        		<!-- //////////////////////////////////////////////////////////// -->
        		<!-- AUTOGRAPHEN -->
        		<!--<hr></hr>
        	    <div class="col-md-2"><a href="#top" class="small pull-right"><span class="glyphicon glyphicon-triangle-top"><xsl:text> Übersicht</xsl:text></span></a></div>
        		<h2 id="Autographen">AUTOGRAPHEN</h2>
        		<div class="row">
        			<xsl:apply-templates select="//t:listBibl"/>
        		</div>-->
        		
        	</article>
            <script>
                $('a[data-toggle="collapse"]').click(function(){
                $(this).text(function(i,old){
                return old=='weniger' ?  'Mehr erfahren' : 'weniger';
                });
                });
                
            </script>
        </section>
    </xsl:template>
    
    
    
    <!-- //////////////////////////////////////////////////////////// -->
    <xsl:template match="t:head/t:title[@type='Untertitel'][1]">
        <xsl:apply-templates/>
    </xsl:template>
    
    <!-- //////////////////////////////////////////////////////////// -->
    <xsl:template match="t:head/t:title[1]">
        <xsl:apply-templates/>
    </xsl:template>

      
    <!-- //////////////////////////////////////////////////////////// -->
    <xsl:template  match="t:ref">
        
    </xsl:template>
    
    <!-- //////////////////////////////////////////////////////////// -->
    <xsl:template match="t:name">
        <xsl:choose>
            <xsl:when test="@type = 'person'">
                <!--<a href="{@ref}" target="_blank">-->
                    <xsl:apply-templates></xsl:apply-templates>
                <!--</a>-->
            </xsl:when>
            <xsl:when test="@type = 'work'">
                <a href="{@ref}" target="_blank">
                    <xsl:apply-templates></xsl:apply-templates>
                </a>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
	
    <!-- //////////////////////////////////////////////////////////// -->    
    <!--<xsl:template match="t:listBibl">
        <xsl:apply-templates select="t:head"></xsl:apply-templates>
        <ul class="list-group">
            <xsl:for-each-group select="t:bibl" group-by="t:author/@ref">
                <xsl:variable name="SZDPER" select="substring-after(t:author/@ref, '#')"/>
                <xsl:variable name="QueryUrl" select="concat('/archive/objects/query:szd.person_search/methods/sdef:Query/get?params=$1|&lt;https%3A%2F%2Fgams.uni-graz.at%2Fo%3Aszd.personen%23', $SZDPER, '&gt;')"/>
                <h3><a  href="{$QueryUrl}"  target="_blank" title="Personensuche">
                    <xsl:value-of select="t:author"/> <xsl:text> </xsl:text>
                    <img src="{$Icon_person}" class="img-responsive icon" alt="Person" title="Personensuche"/>
                </a></h3>
               <xsl:for-each select="current-group()">
                    <a  href="{t:title/@ref}" class="list-group-item" target="_blank" title="Zum Datensatz des Autographendokuments">
                        <xsl:value-of select="t:title[not(@type='Untertitel')]"/>
                    </a>
                </xsl:for-each> 
            </xsl:for-each-group>
        </ul>
    </xsl:template>-->

    <!-- //////////////////////////////////////////////////////////// -->
    <xsl:template match="t:bibl/t:author">
            <xsl:apply-templates></xsl:apply-templates><xsl:text> : </xsl:text>
    </xsl:template>
    
</xsl:stylesheet>
