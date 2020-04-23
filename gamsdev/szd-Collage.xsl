<?xml version="1.0" encoding="UTF-8"?>

<!-- 
    Project: GAMS Projekttemplate
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
    Author: Christopher Pollin
    Last update: 2017
 -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:i18n="http://apache.org/cocoon/i18n/2.1"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    exclude-result-prefixes="#all">
    
    <xsl:include href="szd-static.xsl"/>
    <xsl:include href="szd-Templates.xsl"/>
    
    <xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>
    
    <!-- ///PERSONENLISTE/// -->
    <xsl:template name="content">
        <article id="content" class="card pt-5">
            
            
            <div class="row">
                
                <xsl:for-each-group select="//s:results/s:result" group-by="substring(s:surname,1,1)">
                    <xsl:sort select="current-grouping-key()"></xsl:sort>
                    <xsl:for-each select="current-group()">
                        <figure class="figure col-2">
                            <img src="{s:img/@uri}" class="img-fluid"><xsl:text> </xsl:text></img> <figcaption class="figure-caption"><xsl:value-of select="s:surname"/></figcaption> 
                        </figure>
                    </xsl:for-each>
                    
                </xsl:for-each-group>    
            </div>   
        </article>
       
        
        
    </xsl:template>
    
</xsl:stylesheet>

