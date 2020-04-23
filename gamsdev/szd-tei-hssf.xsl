<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:gmr="http://www.gnome.org/gnumeric/v7" xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs" xmlns:t="http://www.tei-c.org/ns/1.0" version="2.0">

    <xsl:template match="/">
        <xsl:variable name="PID" select="//t:idno[@type='PID']"/>
        
        <gmr:Workbook>
            <gmr:Sheets>
                <gmr:Sheet>
                    <gmr:Name>
                        <xsl:text>SZD: </xsl:text><xsl:value-of select="//t:teiHeader/t:titleStmt/t:title"/>
                    </gmr:Name>
                    <gmr:MaxCol>22</gmr:MaxCol>
                    <!-- HEADER -->
                    <gmr:Cells>
                        <!-- SZDID -->
                        <gmr:Cell Col="0" Row="0" ValueType="60">
                            <gmr:Content>Collection</gmr:Content>
                        </gmr:Cell>
                        <gmr:Cell Col="1" Row="0" ValueType="60">
                            <gmr:Content>SZDID</gmr:Content>
                        </gmr:Cell>
                        <!-- Verfasser/in -->
                        <gmr:Cell Col="2" Row="0" ValueType="60">
                            <gmr:Content>Verfasser/in</gmr:Content>
                        </gmr:Cell>
                        <!-- SZDPER Verfasser -->
                        <gmr:Cell Col="3" Row="0" ValueType="60">
                            <gmr:Content>SZDPER</gmr:Content>
                        </gmr:Cell>
                        <!-- Titel -->
                        <gmr:Cell Col="4" Row="0" ValueType="60">
                            <gmr:Content>Titel</gmr:Content>
                        </gmr:Cell>
                        <!-- Objekttyp -->
                        <gmr:Cell Col="5" Row="0" ValueType="60">
                            <gmr:Content>Objekttyp</gmr:Content>
                        </gmr:Cell>
                        <!-- Standort -->
                        <gmr:Cell Col="6" Row="0" ValueType="60">
                            <gmr:Content>Standort</gmr:Content>
                        </gmr:Cell>
                        <!-- SPRACHE -->
                        <gmr:Cell Col="7" Row="0" ValueType="60">
                            <gmr:Content>Sprache</gmr:Content>
                        </gmr:Cell>
                        <!-- Date -->
                        <gmr:Cell Col="8" Row="0" ValueType="60">
                            <gmr:Content>Datum</gmr:Content>
                        </gmr:Cell>
                    </gmr:Cells> 
                <xsl:choose>
                    <xsl:when test="$PID = 'o:szd.werke' or $PID = 'o:szd.lebensdokumente'">
                        <xsl:call-template name="getRows">
                            <xsl:with-param name="PID" select="$PID"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="$PID = 'o:szd.bibliothek' or $PID = 'o:szd.autographen'">
                        <xsl:call-template name="getRows">
                            <xsl:with-param name="PID" select="$PID"/>
                        </xsl:call-template>
                    </xsl:when>
                   <!-- <xsl:when test="$PID = 'o:szd.lebenskalender'">
                        <xsl:call-template name="getRows"/>
                    </xsl:when>-->
                    <xsl:otherwise/>
                </xsl:choose>
                </gmr:Sheet>
            </gmr:Sheets>
        </gmr:Workbook>
    </xsl:template>
    
    <xsl:template name="getRows">
        <xsl:param name="PID"/>
        <xsl:for-each select="//t:listBibl/t:biblFull|t:listEvent/t:event">
            <xsl:variable name="row" select="position()"/>
            <!-- COLLECTION -->
            <gmr:Cell Col="0" Row="{$row}" ValueType="60">
                <gmr:Content>
                    <xsl:choose>
                        <xsl:when test="@xml:id">
                            <xsl:value-of select="substring-before(@xml:id, '.')"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>nope</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>  
                </gmr:Content>
            </gmr:Cell>
            <!-- SZDID -->
            <gmr:Cell Col="1" Row="{$row}" ValueType="60">
                <gmr:Content>
                    <xsl:choose>
                        <xsl:when test="@xml:id">
                            <xsl:value-of select="@xml:id"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>nope</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </gmr:Content>
            </gmr:Cell>
            <gmr:Cell Col="2" Row="{$row}" ValueType="60">
                <gmr:Content>
                    <xsl:choose>
                        <xsl:when test=".//t:author[1]/t:persName/t:surname|.//t:author[1]/t:persName/t:name">
                            <xsl:value-of select=".//t:author[1]/t:persName/t:surname|.//t:author[1]/t:persName/t:name"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>nope</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </gmr:Content>
            </gmr:Cell>
            <gmr:Cell Col="3" Row="{$row}" ValueType="60">
                <gmr:Content>
                    <xsl:choose>
                        <xsl:when test=".//t:author[1]/@ref">
                            <xsl:value-of select=".//t:author[1]/@ref"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>nope</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </gmr:Content>
            </gmr:Cell>
            <gmr:Cell Col="4" Row="{$row}" ValueType="60">
                <gmr:Content>
                    <xsl:choose>
                        <xsl:when test=".//t:title[1]">
                            <xsl:apply-templates select=".//t:title[1]"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>nope</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </gmr:Content>
            </gmr:Cell>
            <!-- Objekttyp -->
            <gmr:Cell Col="5" Row="{$row}" ValueType="60">
                <gmr:Content>
                    <xsl:choose>
                        <xsl:when test="$PID = 'o:szd.bibliothek'">
                            <xsl:text>nope</xsl:text>
                        </xsl:when>
                        <xsl:when test=".//t:keywords/t:term[1]">
                            <xsl:apply-templates select=".//t:keywords/t:term[1]"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>nope</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </gmr:Content>
            </gmr:Cell>
            <!-- STANDORT -->
            <gmr:Cell Col="6" Row="{$row}" ValueType="60">
                <gmr:Content>
                    <xsl:choose>
                        <xsl:when test=".//t:msIdentifier/t:repository[1]">
                            <xsl:apply-templates select=".//t:msIdentifier/t:repository[1]"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>nope</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </gmr:Content>
            </gmr:Cell>
            <!-- SPRACHE -->
            <gmr:Cell Col="7" Row="{$row}" ValueType="60">
                <gmr:Content>
                    <xsl:choose>
                        <xsl:when test=".//t:textLang/t:lang[1]/@xml:lang">
                            <xsl:apply-templates select=".//t:textLang/t:lang[1]/@xml:lang"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>nope</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </gmr:Content>
            </gmr:Cell>
            <!-- DATE -->
            <xsl:variable name="Date" select=".//t:acquisition/t:date[1] |  .//t:publicationStmt/t:date[1] | .//t:origDate"/>
            <gmr:Cell Col="8" Row="{$row}" ValueType="60">
                <gmr:Content>
                    <xsl:choose>
                        <xsl:when test="$Date/@when">
                            <xsl:apply-templates select="$Date/@when"/>
                        </xsl:when>
                        <xsl:when test="$Date castable as xs:date">
                            <xsl:apply-templates select="$Date"/>
                        </xsl:when>
                        <xsl:when test="matches($Date, '\d{4}') and $Date castable as xs:integer">
                            <xsl:apply-templates select="$Date"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>nope</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </gmr:Content>
            </gmr:Cell>
            
        </xsl:for-each>
    </xsl:template>
        
        
        <!--<gmr:Workbook>
            <gmr:Sheets>
                <gmr:Sheet>
                    <gmr:Name>SZD Excel Export</gmr:Name>
                    <gmr:MaxCol>22</gmr:MaxCol>
                    <!-\- HEADER -\->
                    <gmr:Cells>
                        <!-\- SZDID -\->
                        <gmr:Cell Col="0" Row="0" ValueType="60">
                            <gmr:Content>SZDID</gmr:Content>
                        </gmr:Cell>
                        <!-\- Verfasser/in -\->
                        <gmr:Cell Col="1" Row="0" ValueType="60">
                            <gmr:Content>Verfasser/in</gmr:Content>
                        </gmr:Cell>
                        <!-\- Titel -\->
                        <gmr:Cell Col="2" Row="0" ValueType="60">
                            <gmr:Content>Titel</gmr:Content>
                        </gmr:Cell>
                        <!-\- Beschreibung -\->
                        <gmr:Cell Col="3" Row="0" ValueType="60">
                            <gmr:Content>Beschreibung</gmr:Content>
                        </gmr:Cell>
                        <!-\- Sprache -\->
                        <gmr:Cell Col="4" Row="0" ValueType="60">
                            <gmr:Content>Umfang/Einband</gmr:Content>
                        </gmr:Cell>
                        <!-\- Umfang/Einband -\->
                        <gmr:Cell Col="5" Row="0" ValueType="60">
                            <gmr:Content>Erwerbung</gmr:Content>
                        </gmr:Cell>
                        <!-\- Erwerbung -\->
                        <gmr:Cell Col="6" Row="0" ValueType="60">
                            <gmr:Content>Heutiger Standort</gmr:Content>
                        </gmr:Cell>
                        <!-\- Heutiger Standort -\->
                       <!-\- <gmr:Cell Col="7" Row="0" ValueType="60">
                            <gmr:Content></gmr:Content>
                        </gmr:Cell>-\->
                    </gmr:Cells>
                    <!-\- ROWS -\->
                    <xsl:for-each select="//t:listBibl/t:biblFull">
                        <xsl:variable name="row" select="position()"/>
                        <!-\- SZDID -\->
                        <gmr:Cell Col="0" Row="{$row}" ValueType="60">
                            <gmr:Content>
                                <xsl:value-of select="@xml:id"/>
                            </gmr:Content>
                        </gmr:Cell>
                        <!-\- Verfasser/in -\->
                        <gmr:Cell Col="1" Row="{$row}" ValueType="60">
                            <gmr:Content>
                                <xsl:choose>
                                    <xsl:when test=".//t:author[1]//t:name">
                                        <xsl:value-of select=".//t:author[1]//t:name"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select=".//t:author[1]/t:persName/t:surname"/>
                                        <xsl:text>, </xsl:text>
                                        <xsl:value-of select=".//t:author[1]/t:persName/t:forename"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                           
                                <!-\-<xsl:value-of select="normalize-space(.//t:author[1])"/>-\->
                               <!-\- <xsl:call-template name="print">
                                    <xsl:with-param name="path" select=".//t:author"/>
                                </xsl:call-template>-\->
                            </gmr:Content>
                        </gmr:Cell>
                        <!-\- Titel -\->
                        <gmr:Cell Col="2" Row="{$row}" ValueType="60">
                            <gmr:Content>
                                <xsl:choose>
                                    <xsl:when test=".//t:titleStmt/t:title[1]/t:hi[position()>1]">
                                        <xsl:call-template name="print">
                                            <xsl:with-param name="path" select=".//t:titleStmt/t:title[1]"/>
                                        </xsl:call-template>
                                    </xsl:when>
                                    <xsl:when test=".//t:titleStmt/t:title[1][matches(text()[1], '\w')]">
                                        <xsl:call-template name="print">
                                            <xsl:with-param name="path" select=".//t:titleStmt/t:title[1]"/>
                                        </xsl:call-template>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:text>nope</xsl:text>
                                    </xsl:otherwise>
                                </xsl:choose>
                               
                               <!-\- <xsl:apply-templates select=".//t:titleStmt/t:title[1]"/>-\->
                                <!-\-<xsl:value-of select="normalize-space(.//t:titleStmt/t:title[1])"/>-\->
                            </gmr:Content>
                        </gmr:Cell>
                        <!-\- Beschreibung -\->
                        <gmr:Cell Col="3" Row="{$row}" ValueType="60">
                            <gmr:Content>
                                <!-\-<xsl:call-template name="print">
                                    <xsl:with-param name="path" select=".//t:msContents/t:summary[1]"/>
                                </xsl:call-template>-\->
                                <xsl:apply-templates select=".//t:msContents/t:summary[1]"/>
                                <!-\-<xsl:value-of select="normalize-space(.//t:msContents/t:summary[1])"/>-\->
                            </gmr:Content>
                        </gmr:Cell>
                        <!-\- Sprache -\->
                       <!-\- <gmr:Cell Col="4" Row="{$row}" ValueType="60">
                            <gmr:Content>
                                <xsl:call-template name="print">
                                    <xsl:with-param name="path" select=".//t:lang"/>
                                </xsl:call-template>
                               <!-\\- <xsl:apply-templates select=".//t:lang"/>-\\->
                            </gmr:Content>
                        </gmr:Cell>-\->
                        <!-\- Umfang/Einband -\->
                        <gmr:Cell Col="4" Row="{$row}" ValueType="60">
                            <gmr:Content>
                                <!-\-<xsl:call-template name="print">
                                    <xsl:with-param name="path" select=".//t:physDesc//t:measure[@type='format']"/>
                                </xsl:call-template>-\->
                                <xsl:apply-templates select=".//t:physDesc//t:measure[@type='format']"/>
                            </gmr:Content>
                        </gmr:Cell>
                         <!-\-Erwerbung-\-> 
                        <gmr:Cell Col="5" Row="{$row}" ValueType="60">
                            <gmr:Content>
                                <!-\-<xsl:call-template name="print">
                                    <xsl:with-param name="path" select=".//t:history/t:acquisition[1]"/>
                                </xsl:call-template>-\->
                               <!-\- <xsl:choose>
                                    <xsl:when test=".//t:history/t:acquisition[1]">
                                        <xsl:apply-templates select=".//t:history/t:acquisition[1]"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:text>nope</xsl:text>
                                    </xsl:otherwise>
                                </xsl:choose>-\->
                                <xsl:apply-templates select=".//t:history/t:acquisition[1]"/>
                                <!-\-<xsl:value-of select="normalize-space(.//t:history/t:acquisition[1])"/>-\->
                            </gmr:Content>
                        </gmr:Cell>
                        <!-\- Heutiger Standort -\->
                        <gmr:Cell Col="6" Row="{$row}" ValueType="60">
                            <gmr:Content>
                                <!-\-<xsl:call-template name="print">
                                    <xsl:with-param name="path" select=".//t:history/t:provenance[1]"/>
                                </xsl:call-template>-\->
                                <xsl:choose>
                                    <xsl:when test=".//t:history/t:provenance[1]">
                                        <xsl:apply-templates select=".//t:history/t:provenance[1]"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:text>nope</xsl:text>
                                    </xsl:otherwise>
                                </xsl:choose>
                               
                                <!-\-<xsl:value-of select="normalize-space(.//t:history/t:provenance[1])"/>-\->
                            </gmr:Content>
                        </gmr:Cell>
                    </xsl:for-each>
                </gmr:Sheet>
            </gmr:Sheets>
        </gmr:Workbook>
    </xsl:template>-->
    
    <xsl:template match="t:idno">
        <xsl:text> </xsl:text>
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match="t:date">
        <xsl:text> </xsl:text>
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="t:placeName">
        <xsl:text> </xsl:text>
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match="t:orgName">
        <xsl:text> </xsl:text>
        <xsl:apply-templates/>
    </xsl:template>
    

    <xsl:template name="print">
        <xsl:param name="path"/>
        <xsl:choose>
            <xsl:when test="$path">
                <xsl:text> </xsl:text>
                <xsl:apply-templates select="$path"/>
                <xsl:text> </xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>nope</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
   <!-- <xsl:template match="t:persName">
        <xsl:text> <![CDATA[<p>]]></xsl:text>
        <xsl:apply-templates/>
        <xsl:text><![CDATA[</p>]]></xsl:text>
    </xsl:template>-->
 <!--   
    <xsl:template match="t:orgName">
        <xsl:text> <![CDATA[<o>]]></xsl:text>
        <xsl:apply-templates/>
        <xsl:text><![CDATA[</o>]]></xsl:text>
    </xsl:template>-->
    
  <!--  <xsl:template match="t:placeName">
        <xsl:text> <![CDATA[<pl>]]></xsl:text>
        <xsl:apply-templates/>
        <xsl:text><![CDATA[</pl>]]></xsl:text>
    </xsl:template>-->
    
   <!-- <xsl:template match="t:date">
        <xsl:text> <![CDATA[<d>]]></xsl:text>
        <xsl:apply-templates/>
        <xsl:text><![CDATA[</d>]]></xsl:text>
    </xsl:template>-->
    
    <!--<xsl:template match="t:extent">
        <!-\-<xsl:apply-templates select="t:measure[@type='format']"/>-\->
        <xsl:apply-templates/>
    </xsl:template>-->
    
   <!-- <xsl:template match="t:measure[@type='format']">
        <xsl:text> <![CDATA[<format>]]></xsl:text>
        <xsl:apply-templates/>
        <xsl:text><![CDATA[</format>]]></xsl:text>
    </xsl:template>-->
    
   <!-- <xsl:template match="t:measure[@type='page']">
        <xsl:text> <![CDATA[<page>]]></xsl:text>
        <xsl:apply-templates/>
        <xsl:text><![CDATA[</page>]]></xsl:text>
    </xsl:template>-->
    
    <!--<xsl:template match="t:idno">
        <xsl:text> <![CDATA[<i>]]></xsl:text>
        <xsl:apply-templates/>
        <xsl:text><![CDATA[</i>]]></xsl:text>
    </xsl:template>-->
    
   <!-- <xsl:template match="t:hi">
        <xsl:text> <![CDATA[<hi>]]></xsl:text>
            <xsl:apply-templates/>
        <xsl:text><![CDATA[</hi>]]></xsl:text>
    </xsl:template>-->
    
    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>
    
</xsl:stylesheet>