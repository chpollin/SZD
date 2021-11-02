<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet" xmlns:t="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="xs ss t" version="2.0">
    
    <xsl:variable name="SZDWRK">
        <xsl:copy-of select="document('../SZDWRK.xml')"/>
    </xsl:variable>
    <xsl:variable name="SZDWRK_bibl" select="$SZDWRK//t:bibl"/>
    
    <xsl:template match="@*|node()">
        
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
        
    </xsl:template>
    
    <xsl:template match="t:profileDesc/t:textClass/t:keywords">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
            <xsl:variable name="GND_MSK" select="ancestor::t:biblFull[1]/t:fileDesc/t:titleStmt"/>
             
            <xsl:for-each select="$SZDWRK_bibl/t:title">
                <xsl:choose>
                    <xsl:when test="$GND_MSK/t:title[1]/@ref = .[1]/@ref">
                        <term type="work" ref="{concat('#', ancestor::t:bibl/@xml:id)}"><xsl:value-of select="normalize-space(ancestor::t:bibl/t:title)"/></term>
                </xsl:when>
                    <xsl:when test="normalize-space($GND_MSK/t:title[@type='Einheitssachtitel'][1]) = normalize-space(.[1])">
                        <term type="work" ref="{concat('#', ancestor::t:bibl/@xml:id)}"><xsl:value-of select="normalize-space(ancestor::t:bibl/t:title)"/></term>
                    </xsl:when>
                </xsl:choose>
            </xsl:for-each>
        </xsl:copy>
    </xsl:template>
    
</xsl:stylesheet>