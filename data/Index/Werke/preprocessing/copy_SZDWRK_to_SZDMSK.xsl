<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet" xmlns:t="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="xs ss t" version="2.0">
    
    <xsl:variable name="SZDWRK">
        <xsl:copy-of select="document('../SZDWRK.xml')"/>
    </xsl:variable>
    <xsl:variable name="SZDWRK_ID" select="$SZDWRK//t:bibl/@xml:id"/>
    <xsl:variable name="SZDMSK_dnb" select="//t:biblFull/t:fileDesc/t:titleStmt/t:title/@ref"/>
    <xsl:variable name="SZDWRK_dnb" select="$SZDWRK//t:bibl/t:title/@ref"/>
    
    <xsl:template match="@*|node()">
        
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
        
    </xsl:template>
    
    <xsl:template match="t:profileDesc/t:textClass/t:keywords">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
            <xsl:choose>
                <xsl:when test="parent::t:biblFull[//t:title[@ref=$SZDWRK_dnb]]">
                <term type="work" ref="{$SZDWRK_ID}"/>
                </xsl:when>
                <xsl:otherwise>
                    <term type="work" ref="ToDo"/>
                </xsl:otherwise>
            </xsl:choose>
            
            <!--<term type="work" ref="{$SZDWRK//t:bibl[t:title[@ref=$SZDMSK_dnb]]/@xml:id}"/>-->
            <!--<xsl:choose>
                <xsl:when test="preceding::t:biblFull[t:fileDesc/t:titleStmt/t:title[@ref=$SZDWRK_dnb]]">
                    <term type="work" ref="{$SZDWRK//t:bibl[t:title[@ref=$SZDMSK_dnb]]/@xml:id}"/>
                </xsl:when>
                <xsl:otherwise>
                    <term type="work" ref="ToDo"/>
                </xsl:otherwise>
            </xsl:choose>-->
            <!--<xsl:for-each select="ancestor::t:biblFull[t:fileDesc/t:titleStmt/t:title[@ref=$SZDWRK_dnb]]">
                <term type="work" ref="{$SZDWRK//t:bibl[t:title[@ref=$SZDMSK_dnb]]/@xml:id}"/>
            </xsl:for-each>-->
        </xsl:copy>
    </xsl:template>
    
</xsl:stylesheet>