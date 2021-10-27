<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet" xmlns:t="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="xs ss t" version="2.0">
    
    <xsl:variable name="SZDMSK">
        <xsl:copy-of select="document('../../../Work/SZDMSK_plusDLA.xml')"/>
    </xsl:variable>
    
    <xsl:template match="@*|node()">
        
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
        
    </xsl:template>
    
    <xsl:template match="t:bibl">
        <xsl:variable name="WRK_dnb" select="./t:title/@ref"/>
        <!--<xsl:variable name="WRK_title" select="./t:title"/>-->
        <!--<xsl:variable name="MSK_title" select="$SZDMSK//t:biblFullt/t:fileDesc/t:titleStmt/t:title[1]"/>-->
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
            
            <xsl:for-each-group select="$SZDMSK//t:biblFull" group-by="t:fileDesc/t:titleStmt/t:title[@ref=$WRK_dnb]">
                <xsl:if test="position() = 1"><term type="classification" xml:lang="de">
                    <xsl:value-of select="t:profileDesc/t:textClass/t:keywords/t:term[@xml:lang='de']"/>
                </term></xsl:if>
            </xsl:for-each-group>
        </xsl:copy>
    </xsl:template>
    
</xsl:stylesheet>