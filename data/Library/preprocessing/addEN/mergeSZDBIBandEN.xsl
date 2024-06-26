<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet" xmlns:t="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="xs ss t" version="2.0">

    <!--///////////////////////////    
        author: Chistopher Pollin
        date: 2020

    ///////////////////////////  -->
        
      
    <xsl:variable name="SZDBIB">
        <xsl:copy-of select="document('SZDBIB_2020_06_29_engl.xml')"/>
    </xsl:variable>
    
    <xsl:template match="@*|node()">
        
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- Ausgabevermerk -->
    <xsl:template match="t:editionStmt/t:edition">
        <xsl:variable name="SZDBIB_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDBIB_EN_CONTENT" select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]/*:Cell[17]"/>
        <xsl:copy>
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <span xml:lang="en">
                <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT)"/>
            </span>
        </xsl:copy>
    </xsl:template>
    
    <!-- add en|de for all dates which have not the datatype number (like 1930) -->
    <xsl:template match="t:date[not(number(text()) = .)][not(text() = 's.d.')]">
        <xsl:variable name="SZDBIB_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDBIB_EN_CONTENT" select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]/*:Cell[20]"/>
        
        <xsl:copy>
            <!--  -->
            <xsl:if test="not(@when) and contains(., 'um ')">
                <xsl:attribute name="when" select="normalize-space(substring-after(., ' '))"/>
                <xsl:attribute name="precision" select="'low'"/>
            </xsl:if>
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <span xml:lang="en">
                <xsl:choose>
                    <xsl:when test="contains($SZDBIB_EN_CONTENT, '[')">
                        <xsl:value-of select="substring-before(substring-after(normalize-space($SZDBIB_EN_CONTENT), '['), ']')"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT)"/>
                    </xsl:otherwise>
                </xsl:choose>
               
            </span>
        </xsl:copy>
        
       
    </xsl:template>
    
    <xsl:template match="t:publicationStmt/t:publisher[contains(text(),'[ohne Verlag]')]">
        <xsl:copy>
          <span xml:lang="de">
              <xsl:text>[ohne Verlag]</xsl:text>
          </span>
          <span xml:lang="en">
              <xsl:text>[s.n.]</xsl:text>
          </span>
        </xsl:copy>
    </xsl:template>
    
    
    <xsl:template match="t:publicationStmt/t:pubPlace[contains(text(),'[u.a.]')]">
    <xsl:copy>
        <span xml:lang="de">
            <xsl:text>[u.a.]</xsl:text>
        </span>
        <span xml:lang="en">
            <xsl:text>[et al.]</xsl:text>
        </span>
    </xsl:copy>
    </xsl:template>
    
    <!-- Einband
     <bindingDesc>
        <binding>
          <ab>Broschur</ab>
        </binding>
      </bindingDesc>
    -->
    <xsl:template match="t:bindingDesc/t:binding/t:ab">
        <xsl:variable name="SZDBIB_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDBIB_EN_CONTENT" select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]/*:Cell[33]"/>
        
        <xsl:copy>
            <xsl:attribute name="xml:lang" select="'de'"/>
            <xsl:apply-templates/>
        </xsl:copy>
        <ab xml:lang="en">
            <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT)"/>
        </ab>
    </xsl:template>
    
    <!-- illustriert, karten noten -->
    <xsl:template match="t:additions/t:list[@type='extent']/t:item[@ana]">
        <xsl:variable name="SZDBIB_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDBIB_EN_CONTENT" select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]"/>

        <xsl:copy>
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <span xml:lang="en">
                <xsl:choose>
                    <xsl:when test="@ana='illustrated'">
                        <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT/*:Cell[23])"/>
                    </xsl:when>
                    <xsl:when test="@ana='map'">
                        <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT/*:Cell[24])"/>
                    </xsl:when>
                    <xsl:when test="@ana='note'">
                        <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT/*:Cell[25])"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:comment>ERROR: t:additions/t:list[@type='extent']/t:item[@ana]</xsl:comment>
                    </xsl:otherwise>
                </xsl:choose>
            </span>
        </xsl:copy>
    </xsl:template>
    

    <xsl:template match="t:measure[@type='page'][contains(text(), 'Ungezählte')]">
        <xsl:variable name="SZDBIB_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDBIB_EN_CONTENT" select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]/*:Cell[21]"/>
        <measure type="page">
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <span xml:lang="en">
                <xsl:value-of select="$SZDBIB_EN_CONTENT"/>
            </span>
        </measure>
    </xsl:template>

    <xsl:template match="t:measure[@type='page'][contains(text(), '[Zählung:]')]">
        <xsl:variable name="SZDBIB_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDBIB_EN_CONTENT" select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]/*:Cell[21]"/>
        <measure type="page">
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <span xml:lang="en">
                <xsl:value-of select="$SZDBIB_EN_CONTENT"/>
            </span>
        </measure>
    </xsl:template>
    
    <!-- //altIdentifier[@corresp]/idno[text() = '[Hausexemplar ungekennzeichnet]'] -->    
    <xsl:template match="t:msIdentifier/t:altIdentifier[@corresp]/t:idno[text() = '[Hausexemplar ungekennzeichnet]']">
        <idno/>
        <note>
            <span xml:lang="de">
                <xsl:text>Hausexemplar ungekennzeichnet</xsl:text>
            </span>
            <span xml:lang="en">
                <xsl:text>Unmarked Hausexemplar</xsl:text>
            </span>
        </note>
    </xsl:template>
        
    <xsl:template match="t:msIdentifier/t:altIdentifier[@corresp]/t:idno[contains(text(), ' [im Stempel]')]">
        <xsl:copy>
            <xsl:value-of select="substring-before(., ' [im Stempel]')"/>
        </xsl:copy>
        <note>
            <span xml:lang="de"><xsl:text>im Stempel</xsl:text></span>
            <span xml:lang="en"><xsl:text>within stamp</xsl:text></span>
        </note>
    </xsl:template>
    
    <!--  -->
    <xsl:template match="t:msIdentifier/t:altIdentifier[@corresp]/t:idno[contains(text(), ' [handschriftlich]')]">
        <xsl:copy>
            <xsl:value-of select="substring-before(., ' [handschriftlich]')"/>
        </xsl:copy>
        <note>
            <span xml:lang="de"><xsl:text>handschriftlich</xsl:text></span>
            <span xml:lang="en"><xsl:text>handwritten</xsl:text></span>
        </note>
    </xsl:template>
    
    <!-- Nr. Hausexemplar  
        <altIdentifier corresp="szdg:Hausexemplar">
        <idno>Hausexemplar 502</idno>
        <note>
          <span xml:lang="de">[handschriftlich]</span>
          <span xml:lang="en">[handwritten]</span>
          </note>
      </altIdentifier> -->
    <!--<xsl:template match="t:msIdentifier/t:altIdentifier[@corresp]/t:idno">
        <xsl:variable name="SZDBIB_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDBIB_EN_CONTENT" select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]/*:Cell[54]"/>
        
        <xsl:copy>
            <xsl:choose>
                <xsl:when test="contains(., '[')">
                    <xsl:value-of select="normalize-space(substring-before(., '['))"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:copy>
        <xsl:if test="contains(., '[')">
            <note>
                <span xml:lang="de">
                    <xsl:value-of select="normalize-space(substring-before(substring-after(., '['), ']'))"/>
                </span>
                <span xml:lang="en">
                    <xsl:value-of select="$SZDBIB_EN_CONTENT"/>
                    <xsl:choose>
                        <xsl:when test="contains($SZDBIB_EN_CONTENT, '[')">
                            <xsl:choose>
                                <xsl:when test="substring-before(substring-after($SZDBIB_EN_CONTENT, '['), ']')">
                                    <xsl:value-of select="normalize-space(substring-before(substring-after($SZDBIB_EN_CONTENT, '['), ']'))"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="$SZDBIB_EN_CONTENT"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT)"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </span>
            </note>
        </xsl:if>
    </xsl:template>-->
    
    
    <xsl:template match="t:item[t:ref/@target = ('szdg:Insertion', 'szdg:Bookplate', 'szdg:Marginalia',
        'szdg:Marker', 'szdg:Note', 'szdg:Overpasting','szdg:RemovedPage', 'szdg:Autograph', 'szdg:PresentationInscription')]/t:desc">
        <xsl:variable name="SZDBIB_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDBIB_EN_CONTENT" select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]"/>
        <xsl:variable name="target" select="../t:ref/@target"/>
        
        <xsl:copy>
            <xsl:attribute name="xml:lang" select="'de'"/>
            <xsl:apply-templates/>
        </xsl:copy>
        <desc xml:lang="en">
            <xsl:choose>
                <xsl:when test="$target = 'szdg:Autograph'">
                    <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT/*:Cell[55])"/>
                </xsl:when>
                <xsl:when test="$target = 'szdg:Insertion'">
                    <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT/*:Cell[56])"/>
                </xsl:when>
                <xsl:when test="$target = 'szdg:Bookplate'">
                    <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT/*:Cell[57])"/>
                </xsl:when>
                <xsl:when test="$target = 'szdg:Marginalia'">
                    <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT/*:Cell[58])"/>
                </xsl:when>
                <xsl:when test="$target = 'szdg:Marker'">
                    <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT/*:Cell[59])"/>
                </xsl:when>
                <xsl:when test="$target = 'szdg:Note'">
                    <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT/*:Cell[60])"/>
                </xsl:when>
                <xsl:when test="$target = 'szdg:Overpasting'">
                    <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT/*:Cell[63])"/>
                </xsl:when>
                <xsl:when test="$target = 'szdg:RemovedPage'">
                    <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT/*:Cell[64])"/>
                </xsl:when>
                <xsl:when test="$target = 'szdg:PresentationInscription'">
                    <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT/*:Cell[65])"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>nope: </xsl:text><xsl:value-of select="$target"/>
                </xsl:otherwise>
            </xsl:choose>
           
        </desc>
    </xsl:template>
    
    <!-- Nachbesitzer; later owner -->
    <xsl:template match="t:msDesc/t:history/t:provenance/t:ab">
        <xsl:variable name="SZDBIB_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDBIB_EN_CONTENT" select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]/*:Cell[76]"/>
        
        <orgName ref="szdg:LaterOwner" xml:lang="de">
            <xsl:value-of select="normalize-space(.)"/>
        </orgName>
        <orgName ref="szdg:LaterOwner" xml:lang="en">
            <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT)"/>
        </orgName>
        
    </xsl:template>
    
    
    <xsl:template match="t:msDesc/t:msContents/t:msItem/t:note">
        <xsl:variable name="SZDBIB_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDBIB_EN_CONTENT" select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]/*:Cell[66]"/>
        
        <xsl:copy>
            <xsl:attribute name="xml:lang">
                <xsl:text>de</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:copy>
        <note xml:lang="en">
            <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT)"/>
        </note>
    </xsl:template>
    
    <!-- Heutiger Standort -->
   
   <!-- stamp ; column 61 und 62 -->
    <xsl:template match="t:item[t:stamp[t:ref/@target = 'szdg:Stamp']]/t:desc">
        <xsl:variable name="SZDBIB_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDBIB_EN_CONTENT">
            <xsl:choose>
                <xsl:when test="../following-sibling::t:item[t:stamp]"> 
                    <xsl:value-of select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]/*:Cell[62]"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]/*:Cell[61]"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
 
        <xsl:copy>
            <xsl:attribute name="xml:lang" select="'de'"/>
            <xsl:apply-templates/>
        </xsl:copy>
        <desc xml:lang="en">
            <xsl:value-of select="normalize-space($SZDBIB_EN_CONTENT)"/>
        </desc>
    </xsl:template>
   

</xsl:stylesheet>
