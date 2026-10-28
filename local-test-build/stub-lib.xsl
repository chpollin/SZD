<?xml version="1.0" encoding="UTF-8"?>
<!--
    Local test harness stub library for Stefan Zweig Digital.

    Replaces the two production includes of a page stylesheet (szd-static.xsl and
    szd-Templates.xsl) by imports of the same two files, as materialised by run.sh with
    every GAMS load redirected to local data. The whole template library, the global
    parameters and variables of the page shell and every template of szd-Templates.xsl
    therefore run as in production. Only the entry point (match="/") is replaced, because
    the production page shell needs the Cocoon i18n catalogue and the /lib assets: the
    preview loads styles and card images from the live site through <base>, while the
    local js under test comes from the local web server (absolute URL, not rewritten by
    <base>). Templates defined here take precedence over the imported ones.
-->
<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml"
    exclude-result-prefixes="#all">

    <xsl:import href="szd-static.xsl"/>
    <xsl:import href="szd-Templates.xsl"/>

    <xsl:template match="/">
        <html lang="{$lang}">
            <head>
                <meta charset="utf-8"/>
                <base href="https://stefanzweig.digital/"/>
                <link rel="stylesheet" href="/lib/2.0/bootstrap-4.5.0-dist/css/bootstrap.min.css"/>
                <link rel="stylesheet" href="/szd/css/szd.css"/>
                <link rel="stylesheet" href="/szd/css/cards-gallery.css"/>
                <title>local test build</title>
            </head>
            <body>
                <xsl:call-template name="content"/>
                <script src="http://localhost:8080/js/facsimiles-konvolut.js"><xsl:text> </xsl:text></script>
                <script src="http://localhost:8080/js/list-views.js"><xsl:text> </xsl:text></script>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
