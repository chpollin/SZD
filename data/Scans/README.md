# SZD - Scans

## Workflow für Strukturinformationen der Digitalisate, April 2022

Es gibt einen Ordner benannt nach der Signatur “SZ_AAP_W10”. Darin befindet sich: 
* ein weiter Ordner mit dem selben Namen “SZ_AAP_W10”. In diesem Unterordner befinden sich alle Bilder als .jpg. Diese sind nach der Reihenfolge der Bilder nummeriert.
  * SZ_AAP_W10_001.jpg
  * SZ_AAP_W10_002.jpg
  * etc. 
* ein XML File mit dem selben Namen und der XML-Endung: SZ_AAP_W10.xml.

### SZ_AAP_W10.xml

Hat folgende Struktur. Es gibt auch die Möglichkeit von Unterkapiteln, also `<chapter>` in `<chapter>`.

#### Variante mit `<chapter>` in `<chapter>`

```
<?xml version="1.0" encoding="UTF-8"?>
<root>
    <author>Zweig, Stefan</author>
    <titel>Notizbuch Die Welt von Gestern, SZ-AAP/W10</titel>
    <datum>1940-05</datum>
    <filename>SZ_AAP_W10_</filename>
	<idno>o:szd.6815</idno>
	<structure>
		<chapter>
			<title>Buchdeckel</title>
			<from>001</from>
			<to>001</to>
		</chapter>
		<chapter>
			<title>Besitzvermerk [1r]</title>
			<from>002</from>
			<to>003</to>
		</chapter>
		<chapter>
			<title>Textteil [1v–18r]</title>
			<from>004</from>
			<to>005</to>
			<chapter>
				<title>Seite 1v</title>
				<from>004</from>
				<to>004</to>
			</chapter>
			<chapter>
				<title>Seite 1r</title>
				<from>005</from>
				<to>005</to>
			</chapter>
		</chapter>
		<chapter>
			<title>Ende</title>
			<from>006</from>
			<to>006</to>
		</chapter>
	</structure>
</root>
```

#### flache Variante

```
<?xml version="1.0" encoding="UTF-8"?>
<root>
    <author>Zweig, Stefan</author>
    <titel>Notizbuch Die Welt von Gestern, SZ-AAP/W10</titel>
    <datum>1940-05</datum>
    <filename>SZ_AAP_W10_</filename>
    <idno>o:szd.6815</idno>
    <structure>
        <chapter>
            <title>Buchdeckel</title>
            <from>001</from>
            <to>002</to>
        </chapter>
        <chapter>
            <title>Besitzvermerk [1r]</title>
            <from>003</from>
            <to>003</to>
        </chapter>
        <chapter>
            <title>Textteil [1v–18r]</title>
            <from>004</from>
            <to>037</to>
        </chapter>
        <chapter>
            <title>Leerseiten [18v–90v]</title>
            <from>038</from>
            <to>184</to>
        </chapter>
        <chapter>
            <title>Buchdeckel</title>
            <from>185</from>
            <to>186</to>
        </chapter>
        <chapter>
            <title>Ende</title>
            <from>187</from>
            <to>187</to>
        </chapter>
    </structure>
</root>
```

Für jeden Bereich den man markieren möchte erzeugt man ein <chapter>. Das beinhaltet den Title (der in der Navigation angezeigt wird) und ein von/bis, das man mit <from> und <to> ausdrückt. Ist es nur eine Seite, wie beim Besitzvermerk, dann ist <from> und <to> der gleiche Wert. In <from> und <to> steht die Nummer des Bildes

### szd-JPGtoMETS.xsl

Dieses XSLT erzeugt aus den XML-File und den .jpg in dem Ordner dann ein METS-File, das in GAMS ingestiert werden kann. 

### idno

Für Objekte die schon einen PID in der GAMS haben muss ein <idno> Element hinzugefügt werden, das genau den PID des Objektes beinhaltet.

### szd-TOMETS.xsl

Transformation beim Ingest in GAMS, um das METS anzupassen.