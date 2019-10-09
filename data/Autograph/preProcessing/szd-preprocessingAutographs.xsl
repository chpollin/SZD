<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    xmlns="http://www.tei-c.org/ns/1.0"
    version="2.0">
    
    <!-- author: christopher Pollin
         date: July, 2019
         
         this stylesheet copies SZDAUT.xml and does the following:
         
         * add <msContents><textLang><lang xml:lang="ger"/></textLang></msContents> to all biblFull without an @type="object"
         * this @xml:lang is "Deutsch" with iso, or the language in the input document <lang>
         * every <persName type="person"> becomes a keyword/term (personensuchwort)
         * for every biblFull with an object_pers: delete <author> and copy it to the keyword/term (personensuchwort)
    -->
    
    <!-- VARIABLES -->
    <!-- /////////////////////////////////////////////////////////// -->    
    <xsl:variable name="PersonList">
        <xsl:copy-of select="document('http://glossa.uni-graz.at/o:szd.personen/TEI_SOURCE')"/>
    </xsl:variable>
    
    <xsl:variable name="StandorteList">
        <xsl:copy-of select="document('https://glossa.uni-graz.at/o:szd.standorte/TEI_SOURCE')"/>
    </xsl:variable>
    
    <xsl:variable name="LANGUAGE" select="document('http://glossa.uni-graz.at/archive/objects/context:szd/datastreams/LANGUAGES/content')"/>
    
    <!-- copy all -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- add fileDesc, and profildesc with keyword terms -->
    <xsl:template match="*:biblFull">
            <xsl:copy>
                <xsl:apply-templates select="@*"/>
                <fileDesc>
                    <xsl:apply-templates select="node()"/>
                </fileDesc>
                <profileDesc>
                    <xsl:if test=".//*:persName[@type='person'] or .//*:sourceDesc/*:msDesc/*:msContents/*:msItem/*:ab">
                         <textClass>
                             <keywords>
                                 <xsl:for-each select=".//*:persName[@type='person']">
                                    <term type="person">
                                        <xsl:copy>
                                            <xsl:attribute name="ref">
                                                <xsl:choose>
                                                    <xsl:when test="@ref">
                                                        <xsl:value-of select="@ref"/>
                                                    </xsl:when>
                                                    <xsl:otherwise/>
                                                </xsl:choose>
                                            </xsl:attribute>
                                            <xsl:apply-templates/>
                                        </xsl:copy>
                                        <!--<persName>
                                            <xsl:choose>
                                                <xsl:when test="contains(., ' ')">
                                                    <surname>
                                                        <xsl:value-of select="normalize-space(substring-after(., ' '))"/>
                                                    </surname>
                                                    <forename>
                                                        <xsl:value-of select="normalize-space(substring-before(., ' '))"/>
                                                    </forename>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <name>
                                                        <xsl:value-of select="normalize-space(.)"/>
                                                    </name>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </persName>-->
                                    </term>
                                 </xsl:for-each>
                                 <xsl:if test="./*:titleStmt/*:title/@type = 'object_pers'">
                                     <term type="person_affected">
                                         <xsl:if test="contains(*:titleStmt/*:author/*:persName/@ref, 'gnd')">
                                             <xsl:attribute name="ref">
                                                 <xsl:variable name="SZDPER">
                                                     <xsl:call-template name="GetPersonList">
                                                         <xsl:with-param name="Person" select="*:titleStmt/*:author/*:persName"/>
                                                     </xsl:call-template>
                                                 </xsl:variable>
                                                 <xsl:value-of select="concat('#', $SZDPER)"/>
                                             </xsl:attribute>
                                         </xsl:if>
                                         <persName ref="{*:titleStmt/*:author/*:persName/@ref}">
                                             <surname><xsl:value-of select="*:titleStmt/*:author/*:persName/*:surname"/></surname>
                                             <forename><xsl:value-of select="*:titleStmt/*:author/*:persName/*:forename"/></forename>
                                         </persName>
                                     </term>
                                 </xsl:if>
                                 <xsl:if test=".//*:sourceDesc/*:msDesc/*:msContents/*:msItem/*:ab">
                                     <term type="classification">
                                         <xsl:value-of select="normalize-space(.//*:sourceDesc/*:msDesc/*:msContents/*:msItem/*:ab)"/>
                                     </term>
                                 </xsl:if>
                                 
                             </keywords>
                         </textClass>
                    </xsl:if>
                </profileDesc>
            </xsl:copy>
    </xsl:template>
    
    <xsl:template match="*:title[number(substring-after(ancestor::*:biblFull/@xml:id, '.')) &gt; 812][number(substring-after(ancestor::*:biblFull/@xml:id, '.')) &lt; 992]">
        <xsl:copy>
            <xsl:attribute name="type">
                <xsl:text>music</xsl:text>
            </xsl:attribute>
          <xsl:apply-templates/>  
        </xsl:copy>
    </xsl:template>
    
    
    <!-- in SZDAUT sollten ale orgName die GND-Ref bekommen. -->
  <!--  <xsl:template match="*:orgName[contains(@ref, 'gnd')]">
        <xsl:copy>
            <xsl:attribute name="corresp">
                <xsl:call-template name="GetStandortelist">
                    <xsl:with-param name="Standort" select="@ref"/>
                </xsl:call-template>
            </xsl:attribute>
        </xsl:copy>
    </xsl:template>
    -->
    <xsl:template match="*:author[number(substring-after(ancestor::*:biblFull/@xml:id, '.')) &gt; 812][number(substring-after(ancestor::*:biblFull/@xml:id, '.')) &lt; 992]">
        <xsl:copy>
            <xsl:attribute name="ref">
                <xsl:variable name="SZDPER_ID">
                    <xsl:call-template name="GetPersonList">
                        <xsl:with-param name="Person" select="*:persName"/>
                    </xsl:call-template>
                </xsl:variable>
                <xsl:value-of select="concat('#', $SZDPER_ID)"/>
            </xsl:attribute>
            <xsl:attribute name="role">
                <xsl:text>composer</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>  
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="*:author[number(substring-after(ancestor::*:biblFull/@xml:id, '.')) &lt; 812][not(number(substring-after(ancestor::*:biblFull/@xml:id, '.')) &gt; 992)]">
        <xsl:copy>
            <xsl:attribute name="ref">
                <xsl:variable name="SZDPER_ID">
                    <xsl:call-template name="GetPersonList">
                        <xsl:with-param name="Person" select="*:persName"/>
                    </xsl:call-template>
                </xsl:variable>
                <xsl:value-of select="concat('#', $SZDPER_ID)"/>
            </xsl:attribute>
            <xsl:apply-templates/>  
        </xsl:copy>
    </xsl:template>
    
    
    <!-- adds msContents, where it does not exist, for all biblFull without type=object -->
    <xsl:template match="*:biblFull[*:titleStmt/*:title[not(@type)]]//*:msIdentifier">  
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
        <xsl:if test="not(following-sibling::*:msContents[1])">
            <msContents>
                 <textLang>
                     <lang xml:lang="ger">Deutsch</lang>
                 </textLang>
            </msContents>
        </xsl:if>
    </xsl:template>
    
    <!-- delet author in @type = 'object_pers' elements -->
    <xsl:template match="*:biblFull[*:titleStmt/*:title[@type = 'object_pers']]//*:author">  
        
    </xsl:template>
    
    
    <!-- add iso to language, for all biblFull without type=object -->
    <xsl:template match="*:lang">
        <xsl:copy>
            <!-- //entry[*:language[@type='german']/text() = 'Französisch'] -->
            <xsl:variable name="currentLang" select="normalize-space(string(.))"/>
           
               <!-- <xsl:value-of select="$LANGUAGE//*:entry[*:language[@type='german'] ]"/>-->
               <!-- ToDo: add "Flämisch" to $LANGUAGE -->
                <xsl:choose>
                    <xsl:when test="$LANGUAGE//*:entry[*:language[@type='german']/text() = $currentLang ]">
                        <xsl:attribute name="xml:lang">
                            <xsl:value-of select="$LANGUAGE//*:entry[*:language[@type='german']/text() = $currentLang ]/*:code[@type='ISO639-2'][1]"/>
                        </xsl:attribute>
                    </xsl:when>
                    <xsl:otherwise/>
                </xsl:choose>
            
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- if no lang defined, add german-->
    <xsl:template match="*:biblFull[*:titleStmt/*:title[not(@type)]][not(number(substring-after(@xml:id, '.')) &gt; 812 and number(substring-after(@xml:id, '.')) &lt; 992)]//*:msContents">  
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
            <xsl:if test="not(*:textLang)">
                <textLang>
                    <lang xml:lang="ger">Deutsch</lang>
                </textLang>
            </xsl:if>
        </xsl:copy>
    </xsl:template>
    
    <!-- Ordnugnskategorie Brief oder Zeichnung hier nicht erlaubt -->
    <xsl:template match="*:msItem">
        
    </xsl:template>
    
    
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- param: persName-->    
    <xsl:template name="GetPersonList">
        <xsl:param name="Person"/>
        <xsl:for-each select="$Person">
            <xsl:variable name="GND" select="string(@ref)"/>
            <xsl:variable name="Forename" select="string(*:forename)"/>
            <xsl:variable name="surname" select="string(*:surname)"/>
            <xsl:choose>
                <xsl:when test="contains(@ref, 'gnd')">
                    <xsl:value-of select="$PersonList//*:person[*:persName[contains(@ref, $GND)]]/@xml:id"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="$PersonList//*:person[*:persName/*:surname = $surname]/@xml:id"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
    </xsl:template>
    <!-- /////////////////////////////////////////////////////////// -->
    <!-- param: -->    
    <xsl:template name="GetStandortelist">
        <xsl:param name="Standort"/>
        <xsl:choose>
            <xsl:when test="$Standort = 'Privatbesitz'">
                <xsl:if test="normalize-space($Standort/../*:settlement)">

                        <xsl:variable name="String" select="concat(normalize-space($Standort),', ', normalize-space($Standort/../*:settlement))"/>

                            <xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.standorte#', $StandorteList//*:org[*:orgName = $String]/@xml:id)"/>
                        
                    
                </xsl:if>
            </xsl:when>
          <!--  <xsl:when test="$StandorteList//*:org[*:orgName = normalize-space($Standort)]/@xml:id">

                        <xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.standorte#', $StandorteList//*:org[*:orgName = normalize-space($Standort)]/@xml:id)"/>
            </xsl:when>
            <xsl:when test="$StandorteList//*:org[*:orgName/@ref = $Standort]/@xml:id">

                        <xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.standorte#', $StandorteList//*:org[*:orgName/@ref  = normalize-space($Standort)]/@xml:id)"/>
            </xsl:when>
            <xsl:when test="contains($Standort, '#SZDSTA')">

                        <xsl:value-of select="$Standort"/>
            </xsl:when>-->
            <xsl:otherwise>
                <xsl:value-of select="$Standort"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
  <!--  <xsl:template match="*:summary">  
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="*:textLang">  
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>-->
    
    
    
</xsl:stylesheet>