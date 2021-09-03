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
    
    <!-- Title, wenn keine englische Übersetzung, bleibt <span xml:lang="en"> weg-->
    <xsl:template match="t:fileDesc/t:titleStmt/t:title">
        <xsl:variable name="SZDAUT_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDAUT_EN_CONTENT" select="$SZDEN//*:Row[*:Cell[1]/*:Data = $SZDAUT_ID]/*:Cell[4]"/>
        <xsl:copy>
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <xsl:choose>
                <xsl:when test="$SZDAUT_EN_CONTENT != 'xxx'">
                    <span xml:lang="en">
                        <xsl:value-of select="normalize-space($SZDAUT_EN_CONTENT)"/>
                    </span>
                </xsl:when>
                <xsl:otherwise>
                    <!-- show nothing -->
                </xsl:otherwise>
            </xsl:choose>
        </xsl:copy>
    </xsl:template>
    
    <!-- Summary
    wie umgehen mit dates, die irgendwo drin sind? test und dann Element und copy Attribut?-->
    <xsl:template match="t:msDesc/t:msContents/t:summary">
        <xsl:variable name="SZDAUT_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDAUT_EN_CONTENT" select="$SZDEN//*:Row[*:Cell[1]/*:Data = $SZDAUT_ID]/*:Cell[6]"/>
        <xsl:copy>
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <xsl:choose>
                <xsl:when test="$SZDAUT_EN_CONTENT != 'xxx'">
                    <span xml:lang="en">
                        <xsl:value-of select="normalize-space($SZDAUT_EN_CONTENT)"/>
                    </span>
                </xsl:when>
                <xsl:otherwise>
                    <!-- show nothing -->
                </xsl:otherwise>
            </xsl:choose>
        </xsl:copy>
    </xsl:template>

    <!-- Measure/Extent 
    manchmal gibt es englischen Eintrag für Maße, aber meistens nicht!-->
    <xsl:template match="t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type='format']">
        <xsl:variable name="SZDAUT_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDAUT_EN_CONTENT" select="$SZDEN//*:Row[*:Cell[1]/*:Data = $SZDAUT_ID]/*:Cell[8]"/>
        <xsl:copy>
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <xsl:choose>
                <xsl:when test="$SZDAUT_EN_CONTENT != 'xxx'">
                    <span xml:lang="en">
                        <xsl:value-of select="normalize-space($SZDAUT_EN_CONTENT)"/>
                    </span>
                </xsl:when>
                <xsl:otherwise>
                    <!-- show nothing -->
                </xsl:otherwise>
            </xsl:choose>
        </xsl:copy>
        
        <!-- man könnte cm Angabe aus de in die en kopieren, aber klappt aus irgendeinem Grund nicht,
        er schmeißt mir den type="format" aus dem measure raus?-->
        <!--<xsl:variable name="SZDAUT_DE_CONTENT" select="t:TEI//t:msDesc/t:physDesc/t:objectDesc/t:supportDesc/t:extent/t:measure[@type='format']"/>-->
        <!--<xsl:copy>
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <xsl:choose>
                <xsl:when test="contains($SZDAUT_EN_CONTENT, 'cms')"><!-\- wenn cm Angabe, dann ist measure vollständig ausgefüllt -\->
                    <span xml:lang="en">
                        <xsl:value-of select="normalize-space($SZDAUT_EN_CONTENT)"/>
                    </span>
                </xsl:when>
                <xsl:when test="(not(contains($SZDAUT_EN_CONTENT, 'cms'))) and ($SZDAUT_EN_CONTENT != 'xxx')"><!-\- xxx = kein <span en> (de könnte man kopieren) -\->
                    <span xml:lang="en">
                        <xsl:value-of select="concat($SZDAUT_DE_CONTENT,', ',$SZDAUT_EN_CONTENT)"/>
                    </span>
                </xsl:when>
            </xsl:choose>
        </xsl:copy>-->
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
            <xsl:choose>
                <xsl:when test="$SZDAUT_EN_CONTENT != 'xxx'">
                    <span xml:lang="en">
                        <xsl:value-of select="normalize-space($SZDAUT_EN_CONTENT)"/>
                    </span>
                </xsl:when>
                <xsl:otherwise>
                    <!-- show nothing -->
                </xsl:otherwise>
            </xsl:choose>
        </xsl:copy>
    </xsl:template>
    
    <!-- Provenance
    Achtung: ähnliches Problem wie oben
    AUSSERDEM provenance von SZDAUT.603 schmeißt alles durcheinander, weil hat 2 provenance Element - wozu? das zweite:
    <provenance type="provenance">Herzog de La Rochefoucauld</provenance>???-->
    <xsl:template match="t:msDesc/t:history/t:provenance">
        <xsl:variable name="SZDAUT_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDAUT_EN_CONTENT" select="$SZDEN//*:Row[*:Cell[1]/*:Data = $SZDAUT_ID]/*:Cell[12]"/>
        <xsl:copy>
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <xsl:choose>
                <xsl:when test="$SZDAUT_EN_CONTENT != 'xxx'">
                    <span xml:lang="en">
                        <xsl:value-of select="normalize-space($SZDAUT_EN_CONTENT)"/>
                    </span>
                </xsl:when>
                <xsl:otherwise>
                    <!-- show nothing -->
                </xsl:otherwise>
            </xsl:choose>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>
