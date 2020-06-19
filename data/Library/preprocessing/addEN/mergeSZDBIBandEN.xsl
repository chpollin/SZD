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
        <xsl:copy-of select="document('SZDBIB_2020_06_17_engl.xml')"/>
    </xsl:variable>
    
    <xsl:template match="@*|node()">
        
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- Ausgabevermerk -->
    <xsl:template match="t:editionStmt/t:edition">
        <xsl:variable name="SZDBIB_ID" select="./ancestor::t:biblFull[1]/@xml:id"/>
        <xsl:variable name="SZDBIB_ID_EN_RAW" select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]/*:Cell[17]"/>
        <xsl:copy>
            <span xml:lang="de">
                <xsl:apply-templates/>
            </span>
            <span xml:lang="en">
               <xsl:value-of select="normalize-space($SZDBIB_ID_EN_RAW)"/>
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
        <xsl:variable name="SZDBIB_ID_EN_RAW" select="$SZDBIB//*:Row[*:Cell[79]/*:Data = substring-after($SZDBIB_ID, 'SZDBIB.')]/*:Cell[33]"/>
        
        <xsl:copy>
            <xsl:attribute name="xml:lang" select="'de'"/>
            <xsl:apply-templates/>
        </xsl:copy>
        <ab xml:lang="en">
            <xsl:value-of select="normalize-space($SZDBIB_ID_EN_RAW)"/>
        </ab>
    </xsl:template>
    
    
    <!-- Nr. Hausexemplar  
        <altIdentifier corresp="szdg:Hausexemplar">
        <idno>Hausexemplar 502</idno>
        <note>
          <span xml:lang="de">[handschriftlich]</span>
          <span xml:lang="en">[handwritten]</span>
          </note>
      </altIdentifier> -->
    <!--<xsl:template match="t:msIdentifier/t:altIdentifier[@corresp='szdg:Hausexemplar']/t:idno">
        <xsl:copy>
            <xsl:choose>
                <xsl:when test="contains(., '[')">
                    <xsl:value-of select="substring-before(., ' [')"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:copy>
        <note>
            <span xml:lang="de">ToDo</span>
            <span xml:lang="en">[handwritten]</span>
        </note>
    </xsl:template>-->
    
    
    <!--<xsl:template match=""></xsl:template>-->
    
    <!-- illustriert	Karten	Noten -->
    
    <!-- Einband -->
    
    <!-- Nr. Hausexemplar -->	
    
    <!--Autogramm-->	
    
    <!--Einlage-->	
    
    <!--Exlibris-->	
    
    <!--Marginalie-->	
    
    <!--Merkzeichen-->	
    
    <!--Notiz-->	
    
    <!--Stempel 01-->
    
    

</xsl:stylesheet>
