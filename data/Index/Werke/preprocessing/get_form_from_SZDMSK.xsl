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
    
    <xsl:template match="//t:bibl">
        <xsl:variable name="WRK_dnb" select="./t:title/@ref"/>
        <xsl:variable name="WRK_title" select="./t:title"/>
        <xsl:variable name="MSK_title" select="$SZDMSK//t:biblFullt/t:fileDesc/t:titleStmt/t:title[1]"/>
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:apply-templates select="node()"/>
            <xsl:if test="$SZDMSK//t:biblFull/t:fileDesc/t:titleStmt/t:title[@ref=$WRK_dnb]">
                <term type="classification" xml:lang="de">
                    <xsl:value-of select="$SZDMSK//t:biblFull/t:fileDesc/t:titleStmt/t:title[@ref=$WRK_dnb][position() = 1]/ancestor::t:biblFull/t:profileDesc/t:textClass/t:keywords/t:term[@xml:lang='de']"/>
                 </term>
            </xsl:if>
            <!--<xsl:if test="contains($WRK_title, $MSK_title)">
                <term type="classification" xml:lang="de">
                    <xsl:value-of select="$MSK_title/ancestor::t:biblFull/t:profileDesc/t:textClass/t:keywords/t:term[@xml:lang='de']"/>
                </term>
            </xsl:if>-->
        </xsl:copy>
    </xsl:template>
    
</xsl:stylesheet>