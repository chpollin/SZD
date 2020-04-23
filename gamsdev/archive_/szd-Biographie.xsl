<?xml version="1.0" encoding="UTF-8"?>

<!-- 
    Project: GAMS Projekttemplate
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
    Author: Christopher Pollin
    Last update: 2017
 -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="#all">
    
    <xsl:include href="szd-static.xsl"/>
		<xsl:include href="szd-Templates.xsl"/>
    
    
    
    <xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>
    
        
   <!-- Timeline http://bootsnipp.com/snippets/featured/timeline-responsive -->
    <xsl:template name="content">
        
        <section class="row">
            <article class="col-md-12 panel">
                <!-- //////////////////////////////////////////////////////////// -->
        		<!-- HEADER -->

                <div class="navbar navbar-fixed-top collapse navbar-collapse" style="margin-top: 76px;  padding-left:15px;">
                    <!-- calling onload() in datenkorb.js -->
                    <div class="container hidden-sm hidden-xs" style="background-color:#ffffff;">  
                        
                        <!-- call getStickyNavbar in szd-Templates.xsl -->
                        <xsl:call-template name="getStickyNavbar">
                            <xsl:with-param name="Category" select="//t:body/t:listBibl/t:biblFull/t:profileDesc/t:textClass/t:keywords/t:term[@type='Ordnungskategorie']"/>
                            <xsl:with-param name="Content" select="//t:body/t:listBibl/t:biblFull/t:fileDesc/t:titleStmt/t:title[@type='Einheitssachtitel']"/>
                            <xsl:with-param name="PID" select="$PID"/>
                            <xsl:with-param name="locale" select="$locale"/>
                        </xsl:call-template>
                       
                        
                        <div class="row" style="padding-top: 10px; padding-left: 10px;  margin: auto; max-width: 950px; Zpadding-bottom:10px">
                            <xsl:for-each-group select="//t:listEvent/t:event" group-by="t:head/t:span[1]/t:date/substring(@when | @from, 1, 4)">
                                 <xsl:if test="position() = 1">
                                     <a class="btn" style="padding-right:0px;"  href="{concat('#',translate(current-grouping-key(), ' ', ''))}" onclick="scrolldown(this)">
                                        <xsl:value-of select="current-grouping-key()"/> 
                                    </a>
                                </xsl:if>
                                <xsl:if test="position() mod 2 = 0">
                                    <a class="btn" style="padding-right:0px;" href="{concat('#',translate(current-grouping-key(), ' ', ''))}" onclick="scrolldown(this)">
                                        <xsl:value-of select="current-grouping-key()"/> 
                                    </a>
                                </xsl:if>
                               <!-- <xsl:if test="position() = last()">
                                    <a class="btn" style="padding-right:0px;"  href="{concat('#',translate(current-grouping-key(), ' ', ''))}" onclick="scrolldown(this)" data-toggle="tooltip" title="{concat('Springe zu ', .)}">
                                        <xsl:value-of select="current-grouping-key()"/> 
                                    </a>
                                </xsl:if>-->
                                
                            </xsl:for-each-group>
                        </div>
                    </div>
                </div>

            	<!-- CONTENT -->
            	<div class="row" id="content">		
        			<div class="col-md-12">
                       <ul class="timeline" style="margin: 15px;margin-top: 20x;">
                           <xsl:for-each-group select="//t:listEvent/t:event" group-by="t:head/t:span[1]/t:date/substring(@when | @from, 1, 4)">
                                <xsl:variable name="actualYear" select="current-grouping-key()"/>
                                <xsl:variable name="Position" select="position()"/>
                                <!-- heading YEAR -->
                                <h2 style="text-align: left;" id="{$actualYear}">
                                   <xsl:choose>
                                       <xsl:when test="contains($actualYear, '-')">
                                           <xsl:value-of select="substring-before($actualYear, '-')"/>
                                       </xsl:when>
                                       <xsl:otherwise>
                                           <xsl:value-of select="$actualYear"/>
                                       </xsl:otherwise>
                                   </xsl:choose>
                                    <xsl:text> </xsl:text>
                                </h2>
                                <!-- for each month
                                -->
                                
                               <!-- <xsl:variable name="MonthGroup">
                                    <xsl:if test="contains(t:head/t:date/@when | @from, ('-'))">
                                        <xsl:value-of select="substring(t:head/t:date/@when | @from, 1,7)"/>
                                    </xsl:if>
                                </xsl:variable>-->
                                
                             
                               <xsl:for-each-group select="current-group()" group-by="substring(t:head/t:span[1]/t:date/@when | t:head/t:span[1]/t:date/@from, 1,7)">
                                    <xsl:variable name="currentMonth" select="substring-after(current-grouping-key(), '-')"/>
                                	
                                
                             		<!--<div class="timeline-badge">
                                        <h3>
                                            <!-\-<a data-toggle="collapse" href="{concat('#collapse', $actualYear, $currentMonth)}">-\->
                                                <xsl:choose>
                                                    <xsl:when test=" $currentMonth = '01'">Januar</xsl:when>
                                                    <xsl:when test=" $currentMonth = '02'">Februar</xsl:when>
                                                    <xsl:when test=" $currentMonth = '03'">März</xsl:when>
                                                    <xsl:when test=" $currentMonth = '04'">April</xsl:when>
                                                    <xsl:when test=" $currentMonth = '05'">Mai</xsl:when>
                                                    <xsl:when test=" $currentMonth = '06'">Juni</xsl:when>
                                                    <xsl:when test=" $currentMonth = '07'">Juli</xsl:when>
                                                    <xsl:when test=" $currentMonth = '08'">August</xsl:when>
                                                    <xsl:when test=" $currentMonth = '09'">September</xsl:when>
                                                    <xsl:when test=" $currentMonth = '10'">Oktober</xsl:when>
                                                    <xsl:when test=" $currentMonth = '11'">November</xsl:when>
                                                    <xsl:when test=" $currentMonth = '12'">Dezember</xsl:when>
                                                    <xsl:otherwise><xsl:text> </xsl:text></xsl:otherwise>
                                                </xsl:choose>
                                                <xsl:text> </xsl:text>
                                                <!-\-<span class="glyphicon glyphicon glyphicon-plus"><xsl:text> </xsl:text></span>-\->
                                            <!-\-</a>-\->
                                        </h3>
                                    </div>-->
                                	
                                    <xsl:for-each select="current-group()">
                                        <li id="{@xml:id}">
                                            <xsl:attribute name="class">
                                                <xsl:for-each select="$Position">
                                                    <xsl:if test=". mod 2 = 0">
                                                        <xsl:value-of select="'timeline-inverted'"/>
                                                    </xsl:if>
                                                </xsl:for-each>
                                            </xsl:attribute>
                                            
                                                    <div class="timeline-panel">
                                                        <xsl:apply-templates select="t:head"/>
                                                        <xsl:choose>
                                                            <xsl:when test="$locale = 'en'">
                                                                <xsl:apply-templates select="t:ab[@xml:lang = 'en']"/>
                                                            </xsl:when>
                                                            <xsl:otherwise>
                                                                <xsl:apply-templates select="t:ab[@xml:lang = 'de']"/>
                                                            </xsl:otherwise>
                                                        </xsl:choose>
                                                    </div>
                                                </li>
                                        </xsl:for-each>
                                </xsl:for-each-group>
                            </xsl:for-each-group>
                        </ul>
        			</div>
            	 </div>  
            </article>
        </section>
    </xsl:template>


    <xsl:template match="t:span[@xml:lang = 'en']">
         <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="t:span[@xml:lang = 'de']">
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match="t:ab[@xml:lang = 'en']">
        <div>
            <xsl:apply-templates></xsl:apply-templates>
        </div>  
    </xsl:template>
    
    <xsl:template match="t:ab[@xml:lang = 'de']">
        <div>
            <xsl:apply-templates></xsl:apply-templates>
        </div>  
    </xsl:template>
       
    <!-- ///PERSON/// -->
    <xsl:template match="t:name[@type='person']">
    	<xsl:variable name="SZDPER" select="substring-after(@ref, '#')"/>
        <a href="{concat('/archive/objects/query:szd.person_search/methods/sdef:Query/get?params=$1|&lt;https%3A%2F%2Fgams.uni-graz.at%2Fo%3Aszd.personen%23', $SZDPER, '&gt;')}" target="_blank"
            title="Suche" style="text-decoration:underline;">
			<xsl:apply-templates/>
		</a>
    </xsl:template>
	
	<!-- ///BIBLIOTHEK/// -->
	 <xsl:template match="t:name[@type='book']">
	 	<xsl:variable name="SZDBIB" select="@ref"/>
 	    <a href="{concat('/o:szd.bibliothek', $SZDBIB)}" target="_blank"  title="Zum Eintrag in der Bibliothek" style="text-decoration:underline;">
 	        <xsl:apply-templates/>
		</a>
	 </xsl:template>
    
    <!-- ///WERK/// -->
    <xsl:template match="t:name[@type='work']">
        <xsl:variable name="SZDMSK" select="@ref"/>
        <a href="{concat('/o:szd.werke', $SZDMSK)}" target="_blank" title="Zum Eintrag in den Werken" style="text-decoration:underline;">
            <xsl:apply-templates/>
        </a>
    </xsl:template>
	
	<!-- ///Lebensdokumente/// -->
    <xsl:template match="t:name[@type='personaldocument']">
	 	<xsl:variable name="SZDLEB" select="@ref"/>
	 	<a href="{concat('/o:szd.lebensdokumente', $SZDLEB)}" target="_blank" title="Zum Eintrag in den Lebensdokumenten" style="text-decoration:underline;">
	 	    <xsl:apply-templates/>
		</a>
	 </xsl:template>
	
	
	<!-- ///EXTERN/// -->
	 <xsl:template match="t:name[@type='extern']">
	 	<xsl:variable name="URL" select="@ref"/>
	 	    <a href="{$URL}" target="_blank"   title="Zu einer externen Ressource" style="text-decoration:underline;">
	 	        <xsl:apply-templates/>
			<xsl:text> </xsl:text>
		</a>
	 </xsl:template>
	
	 <!-- ///HREF/// -->
	 <xsl:template match="t:name[@type='href']">
	 	<xsl:variable name="URL" select="@ref"/>
	 	<a href="{$URL}" target="_blank" title="Zum Wikipediaeintrag">
	 	     <xsl:apply-templates/>
		</a>
	 </xsl:template>
	
    <!-- ///HEAD/// -->
    <!--<xsl:template match="t:head">
        <div class="timeline-heading">
            <h3 class="timeline-title">
                <xsl:choose>
                    <xsl:when test="$locale = 'en'">
                        <xsl:apply-templates select="t:span[@xml:lang = 'en']"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:apply-templates select="t:span[@xml:lang = 'de']"/>
                    </xsl:otherwise>
                </xsl:choose>
            </h3>
        </div>
    </xsl:template>
-->
    
</xsl:stylesheet>