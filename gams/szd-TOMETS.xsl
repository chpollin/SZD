
<xsl:stylesheet xmlns:mets="http://www.loc.gov/METS/" xmlns:vi="http://gams.uni-graz.at/viewer" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:template match="vi:book">
    <mets:mets>
      <mets:dmdSec ID="DMD.1">
        <mets:mdWrap MDTYPE="MODS" MIMETYPE="text/xml">
          <mets:xmlData>
            <mods:mods xmlns:mods="http://www.loc.gov/mods/v3">
              <mods:titleInfo>
                <mods:title>
                  <xsl:value-of select="vi:title"></xsl:value-of>
                </mods:title>
                <xsl:if test="vi:subtitle">
                  <mods:subTitle>
                    <xsl:value-of select="vi:subtitle"></xsl:value-of>
                  </mods:subTitle>
                </xsl:if>
                <xsl:if test="vi:source">
                  <mods:note type="signature">
                    <xsl:value-of select="vi:source"></xsl:value-of>
                  </mods:note>
                </xsl:if>
              </mods:titleInfo>
              <xsl:if test="vi:relation">
                <mods:relatedItem type="otherFormat">
                  <mods:location>
                    <mods:url>
                      <xsl:value-of select="vi:relation"></xsl:value-of>
                    </mods:url>
                  </mods:location>
                </mods:relatedItem>
              </xsl:if>
              <mods:name type="personal">
                <mods:displayForm>
                  <xsl:value-of select="vi:author"></xsl:value-of>
                </mods:displayForm>
                <mods:role>
                  <mods:roleTerm type="text">author</mods:roleTerm>
                </mods:role>
              </mods:name>
              <xsl:if test="vi:contributor">
                <mods:name type="personal">
                  <mods:displayForm>
                    <xsl:value-of select="vi:contributor"></xsl:value-of>
                  </mods:displayForm>
                  <mods:role>
                    <mods:roleTerm type="text">contributor</mods:roleTerm>
                  </mods:role>
                </mods:name>
              </xsl:if>
              <xsl:choose>
                <xsl:when test="vi:language">
                  <mods:language>
                    <mods:languageTerm type="text">
                      <xsl:value-of select="vi:language"></xsl:value-of>
                    </mods:languageTerm>
                    <xsl:if test="vi:languageCode">
                      <mods:languageTerm authority="iso639-1" type="code">
                        <xsl:value-of select="vi:languageCode"></xsl:value-of>
                      </mods:languageTerm>
                    </xsl:if>
                  </mods:language>
                </xsl:when>
                <xsl:otherwise>
                  <mods:language>
                    <mods:languageTerm type="text">
                      <xsl:text>Deutsch</xsl:text>
                    </mods:languageTerm>
                    <mods:languageTerm authority="iso639-1" type="code">
                      <xsl:text>de</xsl:text>
                    </mods:languageTerm>
                  </mods:language>
                </xsl:otherwise>
              </xsl:choose>
              <mods:originInfo>
                <xsl:if test="vi:place">
                  <mods:place>
                    <mods:placeTerm type="text">
                      <xsl:value-of select="vi:place"></xsl:value-of>
                    </mods:placeTerm>
                  </mods:place>
                </xsl:if>
                <xsl:if test="vi:date">
                  <mods:dateIssued>
                    <xsl:value-of select="vi:date"></xsl:value-of>
                  </mods:dateIssued>
                </xsl:if>
              </mods:originInfo>
              <xsl:if test="vi:category">
                <mods:subject>
                  <mods:genre>
                    <xsl:if test="vi:category/@xml:lang">
                      <xsl:attribute name="xml:lang">
                        <xsl:value-of select="vi:category/@xml:lang"></xsl:value-of>
                      </xsl:attribute>
                    </xsl:if>
                    <xsl:value-of select="vi:category"></xsl:value-of>
                  </mods:genre>
                </mods:subject>
              </xsl:if>
            </mods:mods>
          </mets:xmlData>
        </mets:mdWrap>
      </mets:dmdSec>
      <mets:amdSec ID="AMD.1">
        <mets:rightsMD ID="RMD.1">
          <mets:mdWrap MDTYPE="OTHER" MIMETYPE="text/xml" OTHERMDTYPE="DVRIGHTS">
            <mets:xmlData>
              <dv:rights xmlns:dv="http://dfg-viewer.de/">
                <dv:owner>
                  <xsl:value-of select="vi:owner/vi:name"></xsl:value-of>
                </dv:owner>
                <dv:ownerContact></dv:ownerContact>
                <dv:ownerLogo></dv:ownerLogo>
                <dv:ownerSiteURL>
                  <xsl:value-of select="vi:owner/vi:site"></xsl:value-of>
                </dv:ownerSiteURL>
              </dv:rights>
            </mets:xmlData>
          </mets:mdWrap>
        </mets:rightsMD>
        <mets:digiprovMD ID="PMD.1">
          <mets:mdWrap MDTYPE="OTHER" MIMETYPE="text/xml" OTHERMDTYPE="DVLINKS">
            <mets:xmlData>
              <dv:links xmlns:dv="http://dfg-viewer.de/">
                <dv:reference></dv:reference>
                <dv:presentation></dv:presentation>
              </dv:links>
            </mets:xmlData>
          </mets:mdWrap>
        </mets:digiprovMD>
      </mets:amdSec>
      <mets:fileSec>
        <mets:fileGrp USE="DEFAULT">
          <xsl:for-each select="//vi:page">
            <mets:file ID="{concat(&apos;IMG.&apos;, position())}" MIMETYPE="image/jpeg">
              <mets:FLocat LOCTYPE="URL" xlink:href="{@xlink:href}"></mets:FLocat>
            </mets:file>
          </xsl:for-each>
        </mets:fileGrp>
      </mets:fileSec>
      <mets:structMap TYPE="PHYSICAL">
        <mets:div ID="PHY.1" TYPE="physSequence">
          <xsl:for-each select="//vi:page">
            <mets:div ID="{concat(&apos;DIV.&apos;, position())}" ORDER="{position()}" TYPE="page">
              <mets:fptr FILEID="{concat(&apos;IMG.&apos;, position())}"></mets:fptr>
            </mets:div>
          </xsl:for-each>
        </mets:div>
      </mets:structMap>
      <mets:structMap TYPE="LOGICAL">
        <mets:div ADMID="AMD.1" DMDID="DMD.1" ID="LOG.1" TYPE="monograph">
          <xsl:for-each select="vi:structure/vi:div">
            <xsl:variable name="outer_position" select="position()"></xsl:variable>
            <mets:div ID="{concat(&apos;U.&apos;, $outer_position)}">
              <xsl:choose>
                <xsl:when test="@label">
                  <xsl:attribute name="LABEL">
                    <xsl:value-of select="@label"></xsl:value-of>
                  </xsl:attribute>
                </xsl:when>
                <xsl:when test="@type">
                  <xsl:attribute name="TYPE">
                    <xsl:value-of select="@type"></xsl:value-of>
                  </xsl:attribute>
                </xsl:when>
              </xsl:choose>
              <xsl:for-each select="vi:div">
                <mets:div ID="{concat(&apos;U.&apos;, $outer_position, &apos;.&apos;, position())}">
                  <xsl:choose>
                    <xsl:when test="@label">
                      <xsl:attribute name="LABEL">
                        <xsl:value-of select="@label"></xsl:value-of>
                      </xsl:attribute>
                    </xsl:when>
                    <xsl:when test="@type">
                      <xsl:attribute name="TYPE">
                        <xsl:value-of select="@type"></xsl:value-of>
                      </xsl:attribute>
                    </xsl:when>
                  </xsl:choose>
                </mets:div>
              </xsl:for-each>
            </mets:div>
          </xsl:for-each>
        </mets:div>
      </mets:structMap>
      <mets:structLink>
        <xsl:for-each select="vi:structure/vi:div">
          <xsl:variable name="unit" select="position()"></xsl:variable>
          <xsl:choose>
            <xsl:when test="vi:page">
              <xsl:for-each select="vi:page">
                <xsl:call-template name="smLink">
                  <xsl:with-param name="unit" select="$unit"></xsl:with-param>
                </xsl:call-template>
              </xsl:for-each>
            </xsl:when>
            <xsl:otherwise>
              <xsl:call-template name="smLink">
                <xsl:with-param name="unit" select="$unit"></xsl:with-param>
              </xsl:call-template>
            </xsl:otherwise>
          </xsl:choose>
          <xsl:for-each select="vi:div">
            <xsl:variable name="inner_unit" select="concat($unit, &apos;.&apos;, position())"></xsl:variable>
            <xsl:for-each select="vi:page">
              <xsl:call-template name="smLink">
                <xsl:with-param name="unit" select="$inner_unit"></xsl:with-param>
              </xsl:call-template>
            </xsl:for-each>
          </xsl:for-each>
        </xsl:for-each>
      </mets:structLink>
    </mets:mets>
  </xsl:template>
  <xsl:template name="smLink">
    <xsl:param name="unit"></xsl:param>
    <xsl:variable name="page">
      <xsl:number count="vi:page" level="any"></xsl:number>
    </xsl:variable>
    <mets:smLink xlink:from="{concat(&apos;U.&apos;,$unit)}" xlink:to="{concat(&apos;DIV.&apos;,$page)}"></mets:smLink>
  </xsl:template>
</xsl:stylesheet>
