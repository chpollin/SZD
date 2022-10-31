<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:file="http://expath.org/ns/file"
	exclude-result-prefixes="xs" version="2.0">
	<!-- xml/tei files -->
	<xsl:variable name="WERKE"
		select="document('http://stefanzweig.digital/o:szd.werke/TEI_SOURCE')"/>
	<xsl:variable name="LEBENSDOKUMENTE"
		select="document('http://stefanzweig.digital/o:szd.lebensdokumente/TEI_SOURCE')"/>
	<xsl:variable name="ROOT" select="/"/>
	<xsl:template match="/">
		<book xmlns="http://gams.uni-graz.at/viewer" xmlns:xlink="http://www.w3.org/1999/xlink">
			<!--  -->
			<xsl:if test="//titel">
				<title>
					<xsl:value-of select="//titel"/>
				</title>
			</xsl:if>
			<!--  -->
			<xsl:if test="//idno">
				<idno>
					<xsl:value-of select="//idno"/>
				</idno>
			</xsl:if>
			<!--  -->
			<xsl:if test="//author">
				<author>
					<xsl:value-of select="//author"/>
				</author>
			</xsl:if>
			<!--  -->
			<xsl:for-each select="$WERKE//*:biblFull | $LEBENSDOKUMENTE//*:biblFull">
				<xsl:variable name="SIGNATURE" select="substring-after($ROOT//titel, ', ')"/>
				<xsl:if test="$SIGNATURE = .//*:idno[@type = 'signature']">
					<relation>
						<xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.werke#', @xml:id)"/>
					</relation>
				</xsl:if>
			</xsl:for-each>
			<!--  -->
			<xsl:variable name="date" select="//datum[1]"/>
			<xsl:if test="$date">
				<date>
					<xsl:choose>
						<xsl:when test="$date castable as xs:date">
							<xsl:value-of select="format-date(//datum[1], '[D].[M].[Y]')"/>
						</xsl:when>
						<!-- 1940-05 -->
						<xsl:when test="matches($date, '\d{4}-\d{2}')">
							<xsl:value-of
								select="concat(substring-after($date, '-'), '.', substring-before($date, '-'))"
							/>
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="$date"/>
						</xsl:otherwise>
					</xsl:choose>
				</date>
			</xsl:if>
			<!-- category; for navigation in context:szd.facsimiles.lebensdokumente -->
			<xsl:choose>
				<xsl:when test="//category[@xml:lang='en']">
					<category xml:lang="en">
						<xsl:value-of select="//category[@xml:lang='en']"/>
					</category>
				</xsl:when>
				<xsl:when test="//category[@xml:lang='de']">
					<category xml:lang="de">
						<xsl:value-of select="//category[@xml:lang='de']"/>
					</category>
				</xsl:when>
				<xsl:otherwise>
					<category>
						<xsl:value-of select="//category[1]"/>
					</category>
				</xsl:otherwise>
			</xsl:choose>
			<!--  -->
			<owner>
				<name>Literaturarchiv Salzburg, https://stefanzweig.digital, CC-BY</name>
			</owner>
			<!--  -->
			<structure>
				<xsl:variable name="FolderName"
					select="normalize-space(substring-before(substring-after(base-uri(), 'Scans/'), '.xml'))"/>
				<xsl:choose>
					<!-- if there is a <structure> to further define structure inside the document -->
					<xsl:when test="//structure">
						<xsl:variable name="filename" select="//filename[1]"/>
						<xsl:for-each select="//structure/chapter">
							<div type="{title}">
								<xsl:variable name="page_begin" select="from"/>
								<xsl:variable name="page_end" select="to"/>
								<xsl:choose>
									<xsl:when test="chapter">
										<xsl:for-each select="chapter">
											<div type="{title}">
												<xsl:variable name="number_with_leading_zero"
												select="substring(string(1000 + from), 2)"/>
												<page
												xlink:href="{concat($filename, $number_with_leading_zero, '.jpg')}"
												/>
											</div>
										</xsl:for-each>
									</xsl:when>
									<xsl:otherwise>
										<xsl:for-each select="$page_begin to $page_end">
											<xsl:variable name="number_with_leading_zero"
												select="substring(string(1000 + .), 2)"/>
											<page
												xlink:href="{concat($filename, $number_with_leading_zero, '.jpg')}"
											/>
										</xsl:for-each>
									</xsl:otherwise>
								</xsl:choose>
							</div>
						</xsl:for-each>
					</xsl:when>
					<!-- otherwise there is no TOC -->
					<xsl:otherwise>
						<div>
							<xsl:for-each
								select="file:list(concat('Y:\data\projekte\szd\data\Scans\', $FolderName), true())">
								<xsl:if test="contains(., '.jpg')">
									<page xlink:href="{.}"/>
								</xsl:if>
							</xsl:for-each>
						</div>
					</xsl:otherwise>
				</xsl:choose>
			</structure>
		</book>
	</xsl:template>
</xsl:stylesheet>
