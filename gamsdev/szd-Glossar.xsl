<?xml version="1.0" encoding="UTF-8"?>

<!-- 
    Project: GAMS Projekttemplate
    Company: ZIM-ACDH (Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities)
    Author: Christopher Pollin
    Last update: 2019
 -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:s="http://www.w3.org/2001/sw/DataAccess/rf1/result" xmlns="http://www.w3.org/1999/xhtml"
    xmlns:t="http://www.tei-c.org/ns/1.0" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" 
    exclude-result-prefixes="#all">
    
    <xsl:include href="szd-static.xsl"/>
    <xsl:include href="szd-Templates.xsl"/>
    
    <xsl:output method="xml" doctype-system="about:legacy-compat" encoding="UTF-8" indent="no"/>
    
    <!-- ///GLOSSAR/// -->
    <xsl:template name="content">
                <!-- //////////////////////////////////////////////////////////// -->
                <!-- HEADER -->
                <xsl:call-template name="getStickyNavbar">
                    <xsl:with-param name="Title">
                        <xsl:choose>
                            <xsl:when test="$locale = 'en'">
                                <xsl:text>Glossary</xsl:text>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:text>Glossar</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:with-param>
                    <xsl:with-param name="Category" select="//skos:Concept[not(skos:broader)]/skos:prefLabel[@xml:lang= $locale]"/>
                    <xsl:with-param name="PID" select="'o:szd.glossar'"/>
                    <xsl:with-param name="locale" select="$locale"/>
                </xsl:call-template>
                
                <!-- /// PAGE-CONTENT /// -->
                <!-- main categories: Provenienkriterien, Bibliothek etc. -->
                <article class="card">
                <xsl:for-each select="//skos:Concept[not(skos:broader)]">
                    <xsl:sort select="skos:prefLabel[@xml:lang = $locale]"/>
                            <xsl:variable name="hasTopConcept" select="@rdf:about"/>
                            <div class="card-body col-11" id="{substring-after(@rdf:about, '#')}">
                                     <xsl:choose>
                                         <xsl:when test="dc:identifier">
                                            <a href="{dc:identifier/@rdf:resource}" target="_blank">
                                                <h2 class="text-left glossarHead card-title">
                                                   <xsl:value-of select="upper-case(skos:prefLabel[@xml:lang = $locale])"/>
                                                </h2> 
                                            </a>
                                         </xsl:when>
                                         <xsl:otherwise>
                                             <h2 class="text-left glossarHead card-title">
                                                 <xsl:value-of select="upper-case(skos:prefLabel[@xml:lang = $locale])"/>
                                             </h2>
                                         </xsl:otherwise>
                                     </xsl:choose>
                                     <p class="card-text">
                                        <xsl:analyze-string select="skos:definition[@xml:lang= $locale]" regex="\n">
                                            <xsl:matching-substring>
                                                <br/>
                                            </xsl:matching-substring>
                                            <xsl:non-matching-substring>
                                                <xsl:value-of select="."/>
                                            </xsl:non-matching-substring>
                                        </xsl:analyze-string>
                                    </p>
                                 </div>
                                <!-- extern R -->
                               <!-- <xsl:call-template name="ExternRessources"/>-->
                            
                            <!-- subcategories -->
                            <xsl:if test="//skos:Concept[contains(skos:broader/@rdf:resource, $hasTopConcept)]">
                                <div class="col-12 ml-30">
                                    <xsl:for-each select="//skos:Concept[contains(skos:broader/@rdf:resource, $hasTopConcept)]">
                                        <xsl:sort select="skos:prefLabel[@xml:lang = $locale]"/>
                                        <div class="row row-eq-height mt-60 glossarEntry">
                                            <div class="col-9" id="{substring-after(@rdf:about, '#')}">
                                                <xsl:variable name="SZDID" select="substring-after(@rdf:about, '#')"/>
                                                <xsl:variable name="BaseURL" select="'/archive/objects/query:szd.category_search/methods/sdef:Query/get?params='"/>
                                                <xsl:variable name="Param" select="encode-for-uri(concat('$1|&lt;https://gams.uni-graz.at/o:szd.glossar#', $SZDID, '&gt;', ';$2|', $locale))"/>
                                                <xsl:variable name="QueryUrl" select="concat($BaseURL, $Param, '&amp;locale=', $locale)"/>
                                                
                                                <xsl:choose>
                                                    <xsl:when test="contains(@rdf:about, '/o:szd.glossar#OriginalShelfmark')">
                                                        <h3 class="glossarHead">
                                                            <xsl:value-of select="upper-case(normalize-space(skos:prefLabel[@xml:lang = $locale]))"/>
                                                        </h3>
                                                    </xsl:when>
                                                    <xsl:when test="@rdf:about = 'https://gams.uni-graz.at/o:szd.glossar#Title'">
                                                        <h3 class="glossarHead">
                                                            <xsl:value-of select="upper-case(normalize-space(skos:prefLabel[@xml:lang = $locale]))"/>
                                                        </h3>
                                                    </xsl:when>
                                                    <xsl:when test="@rdf:about = 'https://gams.uni-graz.at/o:szd.glossar#PartiesInvolved'">
                                                        <h3 class="glossarHead">
                                                            <xsl:value-of select="upper-case(normalize-space(skos:prefLabel[@xml:lang = $locale]))"/>
                                                        </h3>
                                                    </xsl:when>
                                                    <xsl:when test="@rdf:about = 'https://gams.uni-graz.at/o:szd.glossar#PhysicalDescription'">
                                                        <h3 class="glossarHead">
                                                            <xsl:value-of select="upper-case(normalize-space(skos:prefLabel[@xml:lang = $locale]))"/>
                                                        </h3>
                                                    </xsl:when>
                                                    <xsl:otherwise>
                                                        <a href="{$QueryUrl}" target="_blank" title="Suche">
                                                            <!-- href="{$QueryUrl}" -->
                                                            <h3 class="glossarHead">
                                                                <xsl:value-of select="upper-case(normalize-space(skos:prefLabel[@xml:lang = $locale]))"/>
                                                                <xsl:text> </xsl:text>
                                                                <img src="{$Icon_suche_template}" class="img-responsive icon" alt="Standort" title="Suche"/>
                                                            </h3>
                                                        </a>
                                                    </xsl:otherwise>
                                                </xsl:choose>
                                                <p class="small">
                                                    <xsl:if test="contains($hasTopConcept, '/o:szd.glossar#ProvenanceFeature') and rdfs:seeAlso[contains(@rdf:resource,'T-PRO_Thesaurus_der_Provenienzbegriffe')]">
                                                        <xsl:choose>
                                                            <xsl:when test="$locale = 'en'">
                                                                <a href="{rdfs:seeAlso[contains(@rdf:resource,'T-PRO_Thesaurus_der_Provenienzbegriffe')]/@rdf:resource}" target="_blank" title="T-PRO Thesaurus der Provenienzbegriffe">
                                                                    <xsl:text>(T-PRO library provenance feature)</xsl:text>
                                                                </a>
                                                            </xsl:when>
                                                            <xsl:otherwise>
                                                                <a href="{rdfs:seeAlso[contains(@rdf:resource,'T-PRO_Thesaurus_der_Provenienzbegriffe')]/@rdf:resource}" target="_blank" title="T-PRO Thesaurus der Provenienzbegriffe">
                                                                    <xsl:text>(Provenienzmerkmal in der Bibliothek nach T-PRO)</xsl:text>
                                                                </a>
                                                            </xsl:otherwise>
                                                        </xsl:choose>
                                                    </xsl:if>
                                                </p>
                                                 <p>
                                                     <!--<xsl:value-of select="skos:definition[@xml:lang = $locale]"/>-->
                                                     <xsl:analyze-string select="skos:definition[@xml:lang = $locale]" regex="\n">
                                                         <xsl:matching-substring>
                                                             <br/>
                                                         </xsl:matching-substring>
                                                         <xsl:non-matching-substring>
                                                             <xsl:value-of select="."/>
                                                         </xsl:non-matching-substring>
                                                     </xsl:analyze-string>
                                                     <xsl:text> </xsl:text>
                                                 </p>
                                                <!-- extern R -->
                                               <!-- <xsl:call-template name="ExternRessources"/>-->
                                            </div>
                                             <div class="col-3"> 
                                                 <xsl:for-each select="skos:example/@rdf:resource">
                                                     <div class="row">
         											 <div class="column">
         											     <a class="fancybox" data-fancybox-group="group" href="{.}" title="{normalize-space(../../skos:prefLabel[@xml:lang = $locale])}">
                                                            <img src="{.}" class="img-responsive img-thumbnail"  alt="GlossarBild"/>
                                                         </a>
          											</div>
                                                 	</div>
                                                 </xsl:for-each>
                                                 <xsl:text> </xsl:text>
                                            </div>
                                         </div>
                                        <xsl:if test="contains(@rdf:about, '/o:szd.glossar#OriginalShelfmark')">
                                            <xsl:for-each select="//skos:Concept[contains(skos:broader/@rdf:resource, '/o:szd.glossar#OriginalShelfmark')]">
                                                <!--<xsl:sort select="skos:prefLabel[@xml:lang = $locale]"/>-->
                                                <div class="row row-eq-height mt-60 glossarEntry">
                                                    <div class="col-7" id="{substring-after(@rdf:about, '#')}">
                                                        <xsl:variable name="SZDID" select="substring-after(@rdf:about, '#')"/>
                                                        <xsl:variable name="QueryUrl" 
                                                            select="concat('/archive/objects/query:szd.category_search/methods/sdef:Query/get?params=', encode-for-uri('$1|&lt;https://gams.uni-graz.at/o:szd.glossar#'), encode-for-uri($SZDID), '&gt;', '&amp;locale=', $locale)"/>
                                                        <a href="{$QueryUrl}" target="_blank" title="Suche">
                                                            <h3 class="glossarHead">
                                                                <xsl:value-of select="upper-case(normalize-space(skos:prefLabel[@xml:lang = $locale]))"/>
                                                                <xsl:text> </xsl:text>
                                                                <img src="{$Icon_suche_template}" class="img-responsive icon" alt="Standort" title="Suche"/>
                                                            </h3> 
                                                        </a>
                                                        <p class="small">
                                                            <xsl:if test="contains($hasTopConcept, 'https://gams.uni-graz.at/o:szd.glossar#ProvenanceFeature')">
                                                                <xsl:text>(Provenienzmerkmal in der Bibliothek</xsl:text>
                                                                <xsl:for-each select="rdfs:seeAlso/@rdf:resource">
                                                                    <xsl:choose>
                                                                        <xsl:when test=". ='https://provenienz.gbv.de/T-PRO_Thesaurus_der_Provenienzbegriffe'">
                                                                            <a href="{.}">
                                                                                <xsl:text>nach "T-PRO"</xsl:text>
                                                                            </a>
                                                                        </xsl:when>
                                                                        <xsl:otherwise></xsl:otherwise>
                                                                    </xsl:choose>
                                                                    <xsl:text> </xsl:text>
                                                                </xsl:for-each>
                                                                <xsl:text>)</xsl:text>
                                                            </xsl:if>
                                                        </p>
                                                        <p>
                                                            <xsl:analyze-string select="skos:definition[@xml:lang = $locale]" regex="\n">
                                                                <xsl:matching-substring>
                                                                    <br/>
                                                                </xsl:matching-substring>
                                                                <xsl:non-matching-substring>
                                                                    <xsl:value-of select="."/>
                                                                </xsl:non-matching-substring>
                                                            </xsl:analyze-string>
                                                        </p>
                                                        <!-- extern R -->
                                                        <!--<xsl:call-template name="ExternRessources"/>-->
                                                        <xsl:text> </xsl:text>
                                                    </div>
                                                    <div class="col-5"> 
                                                        <xsl:for-each select="skos:example/@rdf:resource">
                                                            <div class="row text-center">
                                                                <div class="column">
                                                                    <a class="fancybox" data-fancybox-group="group" href="{.}" title="{normalize-space(../../skos:prefLabel[@xml:lang = $locale])}">
                                                                        <img src="{.}" class="img-responsive img-thumbnail"  alt="Glossarbild" width="40%"/>
                                                                    </a>
                                                                    <xsl:text> </xsl:text>
                                                                </div>
                                                            </div>
                                                        </xsl:for-each>
                                                        <xsl:text> </xsl:text>
                                                    </div>
                                                </div>
                                            </xsl:for-each>
                                        </xsl:if>
                                     </xsl:for-each>
                                </div>
                            </xsl:if>
                      </xsl:for-each>
                </article>
    </xsl:template>
    
    <!--<xsl:template name="ExternRessources">
        <xsl:if test="rdfs:seeAlso/@rdf:resource">
            <h4 class="text-left"><xsl:text> </xsl:text>EXTERNE RESSOURCEN</h4>
        <xsl:for-each select="rdfs:seeAlso/@rdf:resource">
            <a href="{.}" target="_blank">
                <xsl:choose>
                    <xsl:when test="contains(.,'kalliope-verbund')">
                        <xsl:text>Regeln zur Erschließung von Nachlässen und Autographen</xsl:text><xsl:text> </xsl:text><span class="glyphicon glyphicon-link"><xsl:text> </xsl:text></span>
                    </xsl:when>
                    <xsl:when test="contains(.,'provenienz')">
                        <xsl:text>Plattform für Provenienzforschung und Provenienzerschließung</xsl:text><xsl:text> </xsl:text><span class="glyphicon glyphicon-link"><xsl:text> </xsl:text></span>
                    </xsl:when>
                    <xsl:when test="contains(.,'d-nb.info')">
                        <xsl:text>GND-Ontologie</xsl:text><xsl:text> </xsl:text><span class="glyphicon glyphicon-link"><xsl:text> </xsl:text></span>
                    </xsl:when>
                    <xsl:when test="contains(.,'wikidata.org')">
                        <xsl:text>Wikidata</xsl:text><xsl:text> </xsl:text><span class="glyphicon glyphicon-link"><xsl:text> </xsl:text></span>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="."/><xsl:text> </xsl:text><span class="glyphicon glyphicon-link"><xsl:text> </xsl:text></span>
                    </xsl:otherwise>
                </xsl:choose>
                <br/>
            </a>
        </xsl:for-each>
        </xsl:if>
    </xsl:template>-->
    
</xsl:stylesheet>
