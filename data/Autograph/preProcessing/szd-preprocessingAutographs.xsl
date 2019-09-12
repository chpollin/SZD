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
                                        <xsl:attribute name="ref">
                                            <xsl:choose>
                                                <xsl:when test="@ref">
                                                    <xsl:value-of select="@ref"/>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:text>ToDo</xsl:text>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:attribute>
                                        <xsl:value-of select="normalize-space(.)"/>
                                    </term>
                                 </xsl:for-each>
                                 <xsl:if test="./*:titleStmt/*:title/@type = 'object_pers'">
                                     <term type="person_affected">
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
                    <xsl:when test="contains(*:lang,  'Flämisch')">
                        <xsl:attribute name="xml:lang">
                            <xsl:value-of select="'dut'"/>
                        </xsl:attribute>
                        <xsl:text>Niederländisch, Flämisch</xsl:text>
                    </xsl:when>
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
    <xsl:template match="*:biblFull[*:titleStmt/*:title[not(@type)]]//*:msContents">  
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