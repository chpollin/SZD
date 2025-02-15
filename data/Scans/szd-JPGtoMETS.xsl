<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:file="http://expath.org/ns/file"
	exclude-result-prefixes="xs"
	version="2.0">
	
	<!-- references to remote TEI sources -->
	<xsl:variable name="WERKE" select="document('http://stefanzweig.digital/o:szd.werke/TEI_SOURCE')"/>
	<xsl:variable name="LEBENSDOKUMENTE" select="document('http://stefanzweig.digital/o:szd.lebensdokumente/TEI_SOURCE')"/>
	<xsl:variable name="ROOT" select="/"/>
	
	<xsl:template match="/">
		<book xmlns="http://gams.uni-graz.at/viewer" xmlns:xlink="http://www.w3.org/1999/xlink">
			<!-- title -->
			<xsl:if test="//titel">
				<title>
					<xsl:value-of select="//titel"/>
				</title>
			</xsl:if>
			
			<!-- idno -->
			<xsl:if test="//idno">
				<idno>
					<xsl:value-of select="//idno"/>
				</idno>
			</xsl:if>
			
			<!-- author -->
			<xsl:if test="//author">
				<author>
					<xsl:value-of select="//author"/>
				</author>
			</xsl:if>
			
			<!-- relation -->
			<xsl:choose>
				<xsl:when test="//relation">
					<!-- If a <relation> is already in the source, do something here if needed -->
				</xsl:when>
				<xsl:otherwise>
					<xsl:for-each select="$WERKE//*:biblFull | $LEBENSDOKUMENTE//*:biblFull">
						<!-- use the part after ', ' in <titel> as "signature" -->
						<xsl:variable name="SIGNATURE" select="substring-after($ROOT//titel, ', ')"/>
						<xsl:if test="$SIGNATURE = .//*:idno[@type = 'signature']">
							<relation>
								<xsl:value-of select="concat('https://gams.uni-graz.at/o:szd.werke#', @xml:id)"/>
							</relation>
						</xsl:if>
					</xsl:for-each>
				</xsl:otherwise>
			</xsl:choose>
			
			<!-- date -->
			<xsl:variable name="date" select="//datum[1]"/>
			<xsl:if test="$date">
				<date>
					<xsl:choose>
						<!-- If <datum> is a valid xs:date, format as D.M.Y -->
						<xsl:when test="$date castable as xs:date">
							<xsl:value-of select="format-date(//datum[1], '[D].[M].[Y]')"/>
						</xsl:when>
						<!-- If <datum> matches YYYY-MM, transform to MM.YYYY -->
						<xsl:when test="matches($date, '\d{4}-\d{2}')">
							<xsl:value-of
								select="concat(substring-after($date, '-'), '.', substring-before($date, '-'))"/>
						</xsl:when>
						<!-- Otherwise just output whatever is in <datum> -->
						<xsl:otherwise>
							<xsl:value-of select="$date"/>
						</xsl:otherwise>
					</xsl:choose>
				</date>
			</xsl:if>
			
			<!-- category -->
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
			
			<!-- owner -->
			<owner>
				<name>Literaturarchiv Salzburg, https://stefanzweig.digital, CC-BY</name>
			</owner>
			
			<!-- structure -->
			<structure>
				<!-- folder name is the .xml filename minus extension -->
				<xsl:variable name="FolderName"
					select="normalize-space(substring-before(substring-after(base-uri(), 'Scans/'), '.xml'))"/>
				<xsl:choose>
					<!-- if <structure> is present, create "chapters" -->
					<xsl:when test="//structure">
						<xsl:variable name="filename" select="//filename[1]"/>
						<xsl:for-each select="//structure/chapter">
							<div type="{title}">
								<xsl:variable name="page_begin" select="from"/>
								<xsl:variable name="page_end" select="to"/>
								<xsl:choose>
									<!-- if there's nested chapters -->
									<xsl:when test="chapter">
										<xsl:for-each select="chapter">
											<div type="{title}">
												<xsl:variable name="number_with_leading_zero"
													select="substring(string(1000 + from), 2)"/>
												<page xlink:href="{concat($filename, $number_with_leading_zero, '.jpg')}"/>
											</div>
										</xsl:for-each>
									</xsl:when>
									<!-- otherwise generate pages from $page_begin..$page_end -->
									<xsl:otherwise>
										<xsl:for-each select="$page_begin to $page_end">
											<xsl:variable name="number_with_leading_zero"
												select="substring(string(1000 + .), 2)"/>
											<page xlink:href="{concat($filename, $number_with_leading_zero, '.jpg')}"/>
										</xsl:for-each>
									</xsl:otherwise>
								</xsl:choose>
							</div>
						</xsl:for-each>
					</xsl:when>
					<!-- otherwise, just list .jpg files from the folder -->
					<xsl:otherwise>
						<div>
							<xsl:for-each select="file:list(concat('Y:\data\projekte\szd\data\Scans\', $FolderName), true())">
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
