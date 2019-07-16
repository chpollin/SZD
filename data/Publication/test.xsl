<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    
    <xsl:variable name="QUERY" select="document('query(1).xml')"/>
    
    

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
   <xsl:template match="*:bibl">
       <xsl:if test="contains(., 'Amok')">
           <xsl:element name="ref">
               <xsl:value-of select="$QUERY"/>
           </xsl:element>
       </xsl:if>
       <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
           
       </xsl:copy>
   </xsl:template>

    
    
</xsl:stylesheet>