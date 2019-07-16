<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:template match="/">
        <TEI>
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title>Title</title>
                    </titleStmt>
                    <publicationStmt>
                        <p>Publication Information</p>
                    </publicationStmt>
                    <sourceDesc>
                        <p>Information about the source</p>
                    </sourceDesc>
                </fileDesc>
            </teiHeader>
            <text>
                <body>
        <listBibl> 
            <xsl:for-each select="//ul[@id='main']/li">
            <xsl:variable name="ID" select="concat('SZDPUP.', position())"/>
            <!-- first  -->
            <bibl xml:id="{$ID}">
               
                <author><xsl:text>Stefan Zweig</xsl:text></author><xsl:text> </xsl:text>
                <xsl:apply-templates/>
                
                <xsl:if test="substring-after(./a/@href, '#')">
                   <xsl:variable name="Href" select="normalize-space(substring-after(./a/@href, '#'))"/>
                    
                       <xsl:for-each select="//li[span/@id = $Href]/ul/li">
                           <xsl:variable name="subID" select="concat($ID, '.', position())"/>
                           <!-- second -->
                           <bibl xml:id="{$subID}">
                               <author><xsl:text>Stefan Zweig</xsl:text></author><xsl:text> </xsl:text>
                               <xsl:apply-templates/>
                           </bibl>
                           <xsl:if test="ul">
                              
                                   <xsl:for-each select="./ul/li">
                                       <!-- third  -->
                                       <bibl xml:id="{concat($subID, '.', position())}">
                                           <author><xsl:text>Stefan Zweig</xsl:text></author><xsl:text> </xsl:text>
                                           <xsl:apply-templates/>
                                       </bibl>
                                   </xsl:for-each>
                               
                           </xsl:if>
                       </xsl:for-each>
                   
               </xsl:if> 
           </bibl>

        </xsl:for-each>
        </listBibl>
                </body>
            </text>
        </TEI>
        
    </xsl:template>
    
    <xsl:template match="a">
        <title>
           <xsl:value-of select="."/>
        </title><xsl:text> </xsl:text>
    </xsl:template>
    
    <!--<xsl:template match="i">
        <span rend="italic">
            <xsl:value-of select="."/>
        </span>
    </xsl:template>-->
   
    
    <xsl:template match="text()">
      
        <xsl:variable name="Bibl" select="normalize-space(substring-after(., '.'))"/>
        <xsl:analyze-string select="$Bibl" regex="\d\d\d\d$">
            <xsl:matching-substring >
                <date>
                    <xsl:attribute name="when"><xsl:value-of select="."/></xsl:attribute>
                    <xsl:value-of select="."/>
                </date>
            </xsl:matching-substring>
            <xsl:non-matching-substring>
                <xsl:analyze-string select="." regex="(\d+) S.">
                    <xsl:matching-substring>
                        <extent type="Umfang">
                            <xsl:value-of select="regex-group(1)"/>
                        </extent>
                    </xsl:matching-substring>
                    <xsl:non-matching-substring>
                        <xsl:value-of select="."/>
                    </xsl:non-matching-substring>
                </xsl:analyze-string>
            </xsl:non-matching-substring>
        </xsl:analyze-string>
    </xsl:template>
    
    
</xsl:stylesheet>