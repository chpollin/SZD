<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet" xmlns:t="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="xs ss t" version="2.0">

    <xsl:variable name="SZDEN">
        <xsl:copy-of select="document('2021_02_25_SZDAUT_rev.xml')"/>
    </xsl:variable>
    
    <xsl:template match="@*|node()">
        
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template name="fix_hi">
        <xsl:param name="SZDAUT_EN_CONTENT"/>
        <xsl:value-of select="normalize-space(substring-before($SZDAUT_EN_CONTENT, '&lt;hi&gt;'))"/>
        <xsl:text> </xsl:text>
        <xsl:element name="hi">
            <xsl:attribute name="style"><xsl:text>italic</xsl:text></xsl:attribute>
            <xsl:value-of select="normalize-space(substring-before(substring-after($SZDAUT_EN_CONTENT, '&lt;hi&gt;'), '&lt;/hi&gt;' ))"/>
        </xsl:element>
        <xsl:if test="substring-after($SZDAUT_EN_CONTENT, '&lt;/hi&gt;')">
            <xsl:text> </xsl:text>
            <xsl:value-of select="normalize-space(substring-after($SZDAUT_EN_CONTENT, '&lt;/hi&gt;'))"/>
        </xsl:if>
    </xsl:template>
    
    <!-- Title, wenn keine englische Übersetzung, bleibt <span xml:lang="en"> weg-->
    <xsl:template match="t:fileDesc/t:titleStmt/t:title">
        <xsl:variable name="SZDAUT_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDAUT_EN_CONTENT" select="$SZDEN//*:Row[*:Cell[1]/*:Data = $SZDAUT_ID]/*:Cell[4]"/>
        <xsl:copy><xsl:attribute name="xml:lang">de</xsl:attribute>
            <xsl:apply-templates select="@*"/>
            <xsl:apply-templates select="node()"/>
        </xsl:copy>
            <xsl:if test="$SZDAUT_EN_CONTENT != 'xxx'">
                <title xml:lang="en">
                    <xsl:value-of select="normalize-space($SZDAUT_EN_CONTENT)"/>
                </title>
            </xsl:if>
    </xsl:template>
    
    <!-- Summary
    wie umgehen mit dates, die irgendwo drin sind?-->
    <xsl:template match="t:msDesc/t:msContents/t:summary">
        <xsl:variable name="SZDAUT_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDAUT_EN_CONTENT" select="$SZDEN//*:Row[*:Cell[1]/*:Data = $SZDAUT_ID]/*:Cell[6]"/>
        <xsl:copy>
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <xsl:if test="$SZDAUT_EN_CONTENT != 'xxx'">
                <span xml:lang="en">
                    <xsl:choose>
                        <xsl:when test="contains($SZDAUT_EN_CONTENT, '&lt;hi&gt;')">
                            <xsl:call-template name="fix_hi">
                                <xsl:with-param name="SZDAUT_EN_CONTENT" select="$SZDAUT_EN_CONTENT"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="normalize-space($SZDAUT_EN_CONTENT)"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </span>
            </xsl:if>
        </xsl:copy>
    </xsl:template>
        
    <!-- Measure/Extent 
    manchmal gibt es englischen Eintrag für Maße, aber meistens nicht!
    measure verliert sein type Attribut bei der Transformation?? deshalb xsl:attribute-->
    <xsl:template match="t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type='format']">
        <xsl:variable name="SZDAUT_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDAUT_DE_CONTENT" select="."/>
        <xsl:variable name="SZDAUT_EN_CONTENT" select="$SZDEN//*:Row[*:Cell[1]/*:Data = $SZDAUT_ID]/*:Cell[8]"/>
        <xsl:copy><xsl:attribute name="type">format</xsl:attribute>
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <xsl:choose>
                <xsl:when test="contains($SZDAUT_EN_CONTENT, 'cms')"><!-- wenn cms Angabe, dann ist measure englisch vollständig ausgefüllt -->
                    <span xml:lang="en">
                        <xsl:value-of select="normalize-space($SZDAUT_EN_CONTENT)"/>
                    </span>
                </xsl:when>
                <xsl:when test="(not(contains($SZDAUT_EN_CONTENT, 'cms'))) and ($SZDAUT_EN_CONTENT != 'xxx') and (contains($SZDAUT_DE_CONTENT, 'cm'))"><!-- keine cms Angabe, aber Information vorhanden, z.B. "boards", kopiert deutsche cm Angabe -->
                    <span xml:lang="en">
                        <xsl:value-of select="concat(substring-before($SZDAUT_DE_CONTENT, ', '),', ',$SZDAUT_EN_CONTENT)"/>
                    </span>
                </xsl:when>
                <xsl:when test="($SZDAUT_EN_CONTENT='xxx' and (contains($SZDAUT_DE_CONTENT, 'cm') or contains($SZDAUT_DE_CONTENT, '°')))"><!-- keine englischsprachige Information vorhanden, aber wir wollen Größenangaben auch im Englischen -->
                    <span xml:lang="en">
                        <xsl:value-of select="$SZDAUT_DE_CONTENT"/>
                    </span>
                </xsl:when><!--
                <xsl:otherwise>
                    <span xml:lang="en">
                        <xsl:value-of select="normalize-space($SZDAUT_EN_CONTENT)"/>
                    </span>
                </xsl:otherwise>-->
            </xsl:choose>
        </xsl:copy>
    </xsl:template>
    
    <!-- Acquisition
    Achtung: wie umgehen mit jetzt fehlenden Informationen in Attributen im EN Text (date, usw) und fehlenden inneren Elementen (orgName, placeName)
    Vielleicht irgendwie anhand der Beistriche im deutschen Text, aber schwierig, weil Informationseinheiten nicht immer gleich oder an gleicher Stelle -->
    <xsl:template match="t:msDesc/t:history/t:acquisition">
        <xsl:variable name="SZDAUT_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDAUT_EN_CONTENT" select="$SZDEN//*:Row[*:Cell[1]/*:Data = $SZDAUT_ID]/*:Cell[10]"/>
        <xsl:copy>
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <xsl:if test="$SZDAUT_EN_CONTENT != 'xxx'">
                <span xml:lang="en">
                    <xsl:choose>
                        <xsl:when test="contains($SZDAUT_EN_CONTENT, '&lt;hi&gt;')">
                            <xsl:call-template name="fix_hi">
                                <xsl:with-param name="SZDAUT_EN_CONTENT" select="$SZDAUT_EN_CONTENT"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="normalize-space($SZDAUT_EN_CONTENT)"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </span>
            </xsl:if>
        </xsl:copy>
    </xsl:template>
    
    <!-- Provenance-->
    <xsl:template match="t:msDesc/t:history/t:provenance[not(@type)]">
        <xsl:variable name="SZDAUT_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDAUT_EN_CONTENT" select="$SZDEN//*:Row[*:Cell[1]/*:Data = $SZDAUT_ID]/*:Cell[12]"/>
        <xsl:copy>
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <xsl:if test="$SZDAUT_EN_CONTENT != 'xxx'">
                <span xml:lang="en">
                    <xsl:choose>
                        <xsl:when test="contains($SZDAUT_EN_CONTENT, '&lt;hi&gt;')">
                            <xsl:call-template name="fix_hi">
                                <xsl:with-param name="SZDAUT_EN_CONTENT" select="$SZDAUT_EN_CONTENT"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="normalize-space($SZDAUT_EN_CONTENT)"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </span>
            </xsl:if>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>
