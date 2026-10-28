<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" exclude-result-prefixes="xs" version="1.0">
	<xsl:template match="/">
		<oai_dc:dc xmlns:mets="http://www.loc.gov/METS/" xmlns:mods="http://www.loc.gov/mods/v3"
			xmlns:dc="http://purl.org/dc/elements/1.1/"
			xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
			xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
			xmlns:ex="http://external.namespace.uri">
			
			<xsl:variable name="PID">
				<xsl:for-each select="//dc:identifier">
					<xsl:if test="not(contains(., 'info:fedora/'))">
						<xsl:value-of select="normalize-space(.)"/>
					</xsl:if>
				</xsl:for-each>
			</xsl:variable>
			<xsl:if test="$PID">
				<xsl:variable name="URL"
					select="concat('https://gams.uni-graz.at/', $PID, '/METS_SOURCE')"/>
				
				
				
				<xsl:variable name="METS_SOURCE" select="document($URL)//mets:mets"/>
				<xsl:variable name="titleText" select="normalize-space($METS_SOURCE//mods:title)"/>
				<dc:title>
					<xsl:value-of select="$titleText"/>
					<xsl:if test="contains($METS_SOURCE//mods:note[@type='signature'], '/W')">
						<xsl:if test="not(contains($titleText, ', '))">
							<xsl:text>, </xsl:text>
							<xsl:value-of select="$METS_SOURCE//mods:note[@type='signature']"/>
						</xsl:if>
					</xsl:if>
				</dc:title>
				<dc:relation>STEFAN ZWEIG DIGITAL</dc:relation>
				<dc:relation>https://stefanzweig.digital/</dc:relation>
				<dc:publisher>Literaturarchiv Salzburg, Paris Lodron Universität
					Salzburg</dc:publisher>
				<dc:rights>Creative Commons BY 4.0</dc:rights>
				<dc:rights>https://creativecommons.org/licenses/by/4.0</dc:rights>
				<dc:format>text/xml</dc:format>
				
				<xsl:if test="$METS_SOURCE//mods:name[@type = 'personal']/mods:displayForm/text()">
					<dc:creator>
						<xsl:value-of
							select="normalize-space($METS_SOURCE//mods:name[@type = 'personal']/mods:displayForm)"
						/>
					</dc:creator>
				</xsl:if>
				
				<dc:identifier>
					<xsl:value-of select="normalize-space($PID)"/>
				</dc:identifier>
				
				<xsl:if test="$METS_SOURCE//mods:dateIssued/text()">
					<dc:date>
						<xsl:variable name="date"
							select="normalize-space($METS_SOURCE//mods:dateIssued)"/>
						<xsl:value-of select="$date"/>
					</dc:date>
				</xsl:if>
				
				<!-- the signature contains the information about the type: SZ-AAP/B1.42 -->
				<xsl:choose>
					<xsl:when test="contains($titleText, '/W')">
						<dc:type>Work</dc:type>
					</xsl:when>
					<xsl:when test="contains($titleText, '/L')">
						<dc:type>Personal Document</dc:type>
					</xsl:when>
					<xsl:when test="contains($titleText, '/AK')">
						<dc:type>Postcard</dc:type>
					</xsl:when>
					<xsl:when test="contains($titleText, '/B')">
						<dc:type>Letter</dc:type>
					</xsl:when>
					<xsl:otherwise/>
				</xsl:choose>
				<dc:type>Text</dc:type>
				<xsl:if test="$METS_SOURCE//mods:place/mods:placeTerm/text()">
					<dc:coverage>
						<xsl:value-of select="$METS_SOURCE//mods:place/mods:placeTerm"/>
					</dc:coverage>
				</xsl:if>
				<xsl:if test="$METS_SOURCE//mods:subject/mods:genre/text()">
					<dc:subject>
						<xsl:value-of select="$METS_SOURCE//mods:subject/mods:genre[1]"/>
					</dc:subject>
				</xsl:if>
				<!--  -->
				<xsl:variable name="afterAn" select="substring-after($titleText, ' an ')"/>
				
				<xsl:choose>
					<xsl:when test="$METS_SOURCE//mods:note[@type='signature']">
						<dc:source>Literaturarchiv Salzburg <xsl:if test="$METS_SOURCE//mods:note[@type='signature']"><xsl:value-of select="$METS_SOURCE//mods:note[@type='signature']"/></xsl:if></dc:source>
					</xsl:when>
					<xsl:when test="contains($titleText, ', S')">
						<dc:source>Literaturarchiv Salzburg, <xsl:value-of select="substring-after($titleText, ', ')"/></dc:source>
					</xsl:when>
					<xsl:otherwise/>
				</xsl:choose>

				<xsl:choose>
					<xsl:when test="$METS_SOURCE//mods:language/languageTerm[@type='code']/text()">
						<dc:language>
							<xsl:value-of select="$METS_SOURCE//mods:language/languageTerm[@type='code']/text()"/>
						</dc:language>
					</xsl:when>
					<xsl:otherwise>
						<dc:language>
							<xsl:text>de</xsl:text>
						</dc:language>
					</xsl:otherwise>
				</xsl:choose>
				
				<xsl:choose>
					<xsl:when
						test="$METS_SOURCE//mods:name[@type = 'contributor']/mods:displayForm/text()">
						<dc:contributor>
							<xsl:value-of
								select="normalize-space($METS_SOURCE//mods:name[@type = 'contributor']/mods:displayForm/text())"
							/>
						</dc:contributor>
					</xsl:when>
					<xsl:when test="string-length($afterAn) > 0">
						<!-- Extract the name up to the first delimiter -->
						<xsl:variable name="potentialName">
							<xsl:choose>
								<xsl:when test="contains($afterAn, ' vom ')">
									<xsl:value-of select="substring-before($afterAn, ' vom ')"/>
								</xsl:when>
								<xsl:when test="contains($afterAn, ' Verlag ')">
									<xsl:value-of select="substring-before($afterAn, ' Verlag ')"/>
								</xsl:when>
								<xsl:when test="contains($afterAn, ',')">
									<xsl:value-of select="substring-before($afterAn, ',')"/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="normalize-space('')"/>
								</xsl:otherwise>
							</xsl:choose>
						</xsl:variable>
						<xsl:if
							test="string-length(normalize-space($potentialName)) > 0 and not($potentialName = 'Stefan Zweig')">
							<dc:contributor>
								<xsl:value-of select="normalize-space($potentialName)"/>
							</dc:contributor>
						</xsl:if>
					</xsl:when>
					<xsl:otherwise/>
				</xsl:choose>
				
				<xsl:if test="contains($METS_SOURCE//mods:note[@type='signature'], '/L')">
					<dc:subject>
						<xsl:choose>

							<xsl:when test="contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'abschied')">
								<xsl:text>Abschiedsbrief</xsl:text>
							</xsl:when>
							<xsl:when test="contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'brief')">
								<xsl:text>Briefe</xsl:text>
							</xsl:when>
							<xsl:when test="contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'adressbuch') or 
								contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'address book')">
								<xsl:text>Adressbücher</xsl:text>
							</xsl:when>
							<xsl:when test="contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'büromaterial') or 
								contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'office supply')">
								<xsl:text>Büromaterialien</xsl:text>
							</xsl:when>
							<xsl:when test="contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'finanz') or 
								contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'bankkontoauszüge') or 
								contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'scheckheft')">
								<xsl:text>Finanzen</xsl:text>
							</xsl:when>
							<xsl:when test="contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'kalender')">
								<xsl:text>Kalender</xsl:text>
							</xsl:when>
							<xsl:when test="contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'rechtsdokument') or 
								contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'legal document') or
								contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'vollmacht') or
								contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'certificate')">
								<xsl:text>Rechtsdokumente</xsl:text>
							</xsl:when>
							<xsl:when test="contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'tagebuch') or 
								contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'diary')">
								<xsl:text>Tagebücher</xsl:text>
							</xsl:when>
							<xsl:when test="contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'verlagsvertrag') or 
								contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'publishing contract') or 
								contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agreement')">
								<xsl:text>Verlagsverträge</xsl:text>
							</xsl:when>
							<xsl:when test="contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'verzeichnis') or 
								contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'index') or
								contains(translate($titleText, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'register')">
								<xsl:text>Verzeichnisse</xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>Diverses</xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</dc:subject>
				</xsl:if>
				
			</xsl:if>
		</oai_dc:dc>
	</xsl:template>
</xsl:stylesheet>