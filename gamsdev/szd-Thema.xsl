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
    xmlns:i18n="http://apache.org/cocoon/i18n/2.1"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    exclude-result-prefixes="#all">
    
    <xsl:include href="szd-static.xsl"/>
	<xsl:include href="szd-Templates.xsl"/>
    <xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>

    <xsl:template name="content">
        <section class="card">
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
        <!-- ///SUBJECTS/// -->
        	<article class="card-body">
		        <xsl:call-template name="getNavbar">
		        	<xsl:with-param name="Title" select="upper-case(//t:titleStmt/t:title)"/>
		        	<xsl:with-param name="PID" select="$PID"/>
		            <xsl:with-param name="locale" select="$locale"/>
		        </xsl:call-template>
        	    <!-- //////////////////////////////////////////////////////////// -->
        		<!-- EINTRAG -->
        	    <div class="col-12">
        	    	 <xsl:choose>
        	    	 	<!-- [@xml:lang = 'en'] -->
		                    <xsl:when test="$locale = 'en'">
		                    	<!-- had problems with matching template as div[@xml:lang] is already defined in static.xsl-->
		                    	<xsl:call-template name="getThema">
		                    		<xsl:with-param name="local" select="'en'"/>
		                    	</xsl:call-template>
		                    </xsl:when>
		                    <xsl:otherwise>
		                    	<xsl:call-template name="getThema">
		                    		<xsl:with-param name="local" select="'de'"/>
		                    	</xsl:call-template>
		                    </xsl:otherwise>
				      </xsl:choose>
        	    </div>
        	</article>
        	<!-- weniger - mehr Button -->
            <script>
                $('a[data-toggle="collapse"]').click(function(){
                $(this).text(function(i,old){
                return old=='&#9650;' ?  '&#9660;' : '&#9650;';});
                }); 
            </script>
        </section>
    </xsl:template>

    <!-- //////////////////////////////////////////////////////////// -->
    <!--  -->
	<xsl:template name="getThema">
		<xsl:param name="local"/>
	    <!-- //////////////////////////////////////////////////////////// -->
	    <!-- EINLEITUNG -->
        <div class="col-12 mt-5">
            <xsl:apply-templates select="//t:body/t:div[@type = 'introduction'][@xml:lang = $local]/t:p[1]"/>
            <div class="collapse" id="{concat('viewdetails', generate-id(//t:body/t:div[@type = 'introduction'][@xml:lang = $local]/t:p[2]))}">
                <xsl:apply-templates select="//t:body/t:div[@type = 'introduction'][@xml:lang = $local]/t:p[not(position() = 1)]"/>
            </div>
            <a type="button" data-toggle="collapse" data-target="{concat('#viewdetails', generate-id(//t:body/t:div[@type = 'introduction'][@xml:lang = $local]/t:p[2]))}" style="color:#C2A360; font-size: 30px;">
                <xsl:text>&#9660;</xsl:text>
            </a>
        </div>
	    
	    <xsl:choose>
	        <xsl:when test="//t:body/t:div[@type = 'col-2']">
	            <xsl:call-template name="getSubject2Columns">
	                <xsl:with-param name="local" select="$local"/>
	            </xsl:call-template>
	        </xsl:when>
	        <xsl:otherwise>
	            <xsl:apply-templates select="//t:body/t:div[@type = 'col-1'][@xml:lang = $local]"/>
	        </xsl:otherwise>
	    </xsl:choose>
	</xsl:template>
    
    <xsl:template name="getSubject2Columns">
        <xsl:param name="local"/>
        <xsl:for-each select="//t:body/t:div[@type = 'col-2'][@xml:lang = $local]">
        <xsl:variable name="SZDID">
            <xsl:choose>
                <xsl:when test="contains(t:head/t:title/@ref, ' ')">
                    <xsl:value-of select="tokenize(normalize-space(t:head/t:title/@ref), ' ')"/>
                </xsl:when>
                <xsl:when test="contains(t:head/t:title/@ref, 'SZD')">
                    <xsl:value-of select="substring-after(t:head/t:title/@ref, '#')"/>
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>
        </xsl:variable>
        
        <!-- //////////////////////////////////////////////////////////// -->
        <!-- entry with text on the left and metadata on the right. -->   
        <div class="row mt-5">
            <!-- HEAD -->
            <div class="col-6">
                <h2 style="line-height: 35px;">
                    <xsl:apply-templates select="t:head/t:title[1]"/>
                    <br/>
                    <xsl:apply-templates select="t:head/t:title[@type='Untertitel'][1]"/>
                </h2>
            </div>
            <!-- IMAGE -->
            <div class="col-6">
                <xsl:choose>
                    <xsl:when test="t:head/t:ref">
                        <a href="{t:head/t:ref}" target="_blank" title="To extern resource" class="text-uppercase">
                            <h3>
                                <i18n:text>toexternresource</i18n:text>
                                <!--ZUR EXTERNEN RESSOURCE--> 
                                <xsl:text> </xsl:text>
                                <i class="fas fa-external-link-alt _icon"><xsl:text> </xsl:text></i>
                            </h3>
                        </a>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:for-each select="tokenize(t:head/t:title[not(@type='Untertitel')]/@facs, ' ')">
                            <xsl:if test="position() = 1">
                                <a href="{concat('/', ., '/sdef:IIIF/getMirador')}" target="_blank" title="Viewer">
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
        <div class="row">
            <xsl:choose>
                <xsl:when test="contains(normalize-space(t:head/t:title/@ref), ' ')">
                    <xsl:attribute name="id" select="substring-before(substring-after(t:head/t:title/@ref, '#'), ' ')"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="id" select="substring-after(t:head/t:title/@ref, '#')"/>
                </xsl:otherwise>
            </xsl:choose>
            <div class="col-sm-6">
                <!-- //////////////////////////////////////////////////////////// -->
                <!-- Über das Original -->
                <h3 class="text-uppercase">
                    <i18n:text>aboutoriginal</i18n:text>
                </h3>
                <div>
                    <xsl:apply-templates select="t:p"/>
                </div>
                <!--<xsl:apply-templates select="t:p[1]"></xsl:apply-templates>
                <xsl:if test="t:p[not(position() = 1)]">
                    <div class="collapse" id="{concat('viewdetails', generate-id(t:p[2]))}">
                        <xsl:apply-templates select="t:p[not(position() = 1)]"></xsl:apply-templates>
                    </div>
                    <a type="button" data-toggle="collapse" data-target="{concat('#viewdetails', generate-id(t:p[2]))}" style="color:#C2A360;">&#9660;</a>
                 </xsl:if>-->
                <xsl:if test="not($SZDID = '')">
                    <!-- //////////////////////////////////////////////////////////// -->
                    <!-- Zum Katalog -->
                    <div class="mt-5">
                        <h3 class="text-uppercase">
                            <i18n:text>tocatalog</i18n:text>
                        </h3>
                        <xsl:for-each select="tokenize($SZDID, '\s')">
                            <xsl:variable name="helpSZDID">
                                <xsl:choose>
                                    <xsl:when test="contains(., '#')">
                                        <xsl:value-of select="substring-after(., '#')"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select="."/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:variable>
                            <xsl:choose>
                                <xsl:when test="contains(., 'SZDMSK')">
                                    <a href="{concat('/o:szd.werke/sdef:TEI/get?locale=', $locale, '#', $helpSZDID)}" target="_blank">
                                        <!-- if a lanuage tag exists, otherwise just the first title -->
                                        <xsl:call-template name="printEnDe">
                                            <xsl:with-param name="locale" select="$locale"/>
                                            <xsl:with-param name="path" select="$MANUSKRIPTE//t:listBibl/t:biblFull[@xml:id = $helpSZDID]//t:title"/>
                                        </xsl:call-template>
                                        <xsl:text>, </xsl:text>
                                        <xsl:value-of select="$MANUSKRIPTE//t:listBibl/t:biblFull[@xml:id = $helpSZDID]//t:idno[@type='signature'][1]"/>
                                    </a>
                                </xsl:when>
                                <xsl:when test="contains(., 'SZDLEB')">
                                    <a href="{concat('/o:szd.lebensdokumente/sdef:TEI/get?locale=', $locale, '#', $helpSZDID)}" target="_blank">
                                        <xsl:call-template name="printEnDe">
                                            <xsl:with-param name="locale" select="$locale"/>
                                            <xsl:with-param name="path" select="$LEBENSDOKUMENTE//t:listBibl/t:biblFull[@xml:id = $helpSZDID]//t:title"/>
                                        </xsl:call-template>
                                        <xsl:text>, </xsl:text>
                                        <xsl:value-of select="$LEBENSDOKUMENTE//t:listBibl/t:biblFull[@xml:id = $helpSZDID]//t:idno[@type='signature'][1]"/>
                                    </a>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:comment>ERROR: resource not found! Sry! :(</xsl:comment>
                                </xsl:otherwise>
                            </xsl:choose>
                            <!-- for each reference -->
                            <br/>
                        </xsl:for-each>
                    </div>
                </xsl:if>
            </div>
            <!-- //////////////////////////////////////////////////////////// -->
            <div class="col-sm-6">
                <h3 class="text-uppercase">
                    <i18n:text>metadata</i18n:text>
                </h3>        	            	    
                <xsl:choose>
                    <!-- for all resources with a SZD. - ID -->
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
                                            <div class="small"><xsl:call-template name="FillbiblFull_SZDMSK">
                                                <xsl:with-param name="locale" select="$locale"/>
                                            </xsl:call-template></div>
                                        </xsl:for-each>
                                    </xsl:when>
                                    <xsl:when test="contains(., 'SZDLEB')">
                                        <div class="small"><xsl:for-each select="$LEBENSDOKUMENTE//t:listBibl/t:biblFull[@xml:id = $helpSZDID]">
                                            <!-- this template is also used for the metadata representation für Collections in szd-templates -->
                                            <xsl:call-template name="FillbiblFull_SZDMSK">
                                                <xsl:with-param name="locale" select="$locale"/>
                                            </xsl:call-template>
                                        </xsl:for-each></div>
                                    </xsl:when>
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
            </div>
        </div>
        </xsl:for-each>
    </xsl:template>
    
    
    <!-- //////////////////////////////////////////////////////////// -->
    <xsl:template match="t:body/t:div[@type = 'col-1']">
        <div class="mt-4">
            <xsl:apply-templates/>
        </div>
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
    <xsl:template  match="t:ref"/>
    
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
    <xsl:template match="t:bibl/t:author">
            <xsl:apply-templates></xsl:apply-templates><xsl:text> : </xsl:text>
    </xsl:template>
    
    <!-- //////////////////////////////////////////////////////////// -->
    <xsl:template match="t:figure">
        <figure class="text-center">
            <xsl:choose>
                <xsl:when test="t:figDesc/t:ref">
                    <a href="{t:figDesc/t:ref/@target}" title="{t:figDesc/t:ref}" target="_blank">
                        <img src="{concat('/', $PID, '/', t:graphic/@url)}" class="figure-img img-fluid w-50 mx-auto">
                            <xsl:if test="t:figDesc">
                                <xsl:attribute name="alt"><xsl:value-of select="t:figDesc"/></xsl:attribute>
                            </xsl:if>
                            <xsl:text> </xsl:text>
                        </img>
                    </a>
                </xsl:when>
                <xsl:otherwise>
                    <img src="{concat('/', $PID, '/', t:graphic/@url)}" class="figure-img img-fluid w-50 mx-auto">
                        <xsl:if test="t:figDesc">
                            <xsl:attribute name="alt"><xsl:value-of select="t:figDesc"/></xsl:attribute>
                        </xsl:if>
                        <xsl:text> </xsl:text>
                    </img>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:if test="t:figDesc/t:caption">
                <figcaption>
                    <xsl:value-of select="t:figDesc/t:caption"/>
                </figcaption>
            </xsl:if>
        </figure>
       
    </xsl:template>
    
</xsl:stylesheet>
