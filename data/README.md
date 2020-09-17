# SZD - Data
## [Autograph](https://github.com/chpollin/SZD/tree/master/data/Autograph), SZDAUT

```xml
<biblFull xml:id="SZDAUT.1">
    <fileDesc>
        <titleStmt>
            <title ref="https://www.nli.org.il/en/archives/NNL_ARCHIVE_AL003432649">
                <hi style="italic">L’escapade</hi>
            </title>
            <author ref="#SZDPER.2">
                <persName ref="http://d-nb.info/gnd/118643746">
                    <forename>Paul</forename>
                    <surname>Adam</surname>
                </persName>
            </author>
        </titleStmt>
        <publicationStmt>
            <ab>Autographen</ab>
        </publicationStmt>
        <sourceDesc>
            <msDesc>
                <msIdentifier>
                    <idno>SZDAUT.1</idno>
                    <altIdentifier>
                        <idno>1</idno>
                        <note>
                            <bibl>
                                <title>Katalog der Sammlung Zweig</title>
                                <ref target="http://d-nb.info/977275620"/>
                            </bibl>
                        </note>
                    </altIdentifier>
                </msIdentifier>
                <msContents>
                    <summary>Eigenhändiges Manuskript mit Unterschrift</summary>
                    <textLang>
                        <lang xml:lang="fre">Französisch</lang>
                    </textLang>
                </msContents>
                <physDesc>
                    <objectDesc>
                        <supportDesc>
                            <extent>
                                <measure type="page">12</measure>
                                <measure type="format">35,4 x 15,7 cm</measure>
                            </extent>
                        </supportDesc>
                    </objectDesc>
                </physDesc>
                <history>
                    <origin>
                        Karteikarte aus der Sammlung Zweig (Privatsammlung Schweiz). Hinterberger XX, Nr. 590a
                    </origin>
                    <provenance>
                        <orgName ref="http://d-nb.info/gnd/1004728-1">
                            The National Library of Israel,
                            <placeName ref="http://www.geonames.org/281184">Jerusalem</placeName>
                        </orgName>
                        <idno type="signature">Arc. Ms. Var. 305 / 93</idno>
                    </provenance>
                    <acquisition>
                        <date>1911</date>
                        ,
                        <orgName>
                            Antiquariat Charavay,
                            <placeName ref="http://www.geonames.org/2988507">Paris</placeName>
                        </orgName>
                    </acquisition>
                </history>
            </msDesc>
        </sourceDesc>
    </fileDesc>
</biblFull>
```

## [Library](https://github.com/chpollin/SZD/tree/master/data/Library), SZDBIB

ana="szdg:InventoryNumberOld" - reference to http://stefanzweig.digital/o:szd.glossar/ONTOLOGY

```xml
<biblFull xml:id="SZDBIB.721">
    <fileDesc>
        <titleStmt>
            <title>Gedichte</title>
            <author ref="#SZDPER.111">
                <persName ref="http://d-nb.info/gnd/119037777">
                    <forename>Margarete</forename>
                    <surname>Beutler</surname>
                </persName>
            </author>
        </titleStmt>
        <publicationStmt>
            <publisher>M. Lilienthal</publisher>
            <date precision="low">1903</date>
            <pubPlace>Berlin</pubPlace>
        </publicationStmt>
        <sourceDesc>
            <msDesc>
                <msIdentifier>
                    <settlement>Deutschland</settlement>
                    <repository ref="https://gams.uni-graz.at/o:szd.standorte#SZDSTA.12">Privatbesitz</repository>
                    <altIdentifier corresp="szdg:InventoryNumberOld" n="1">
                        <idno>IN 514</idno>
                    </altIdentifier>
                    <altIdentifier corresp="szdg:InventoryNumberOld" n="2">
                        <idno>WN 491</idno>
                    </altIdentifier>
                    <altIdentifier corresp="szdg:InventoryNumberOld" n="3">
                        <idno>5a</idno>
                    </altIdentifier>
                    <altIdentifier corresp="szdg:InventoryNumberOld" n="1">
                        <idno>IN 1803</idno>
                    </altIdentifier>
                    <altIdentifier corresp="szdg:InventoryNumberOld" n="2">
                        <idno>WN 1629</idno>
                    </altIdentifier>
                    <altIdentifier corresp="szdg:InventoryNumberOld" n="3">
                        <idno>5cr</idno>
                    </altIdentifier>
                    <altIdentifier corresp="szdg:InventoryNumberNew">
                        <idno>IN 1144</idno>
                    </altIdentifier>
                    <altIdentifier corresp="szdg:SingleLetter" n="1" type="lowercase">
                        <idno>c/7</idno>
                    </altIdentifier>
                </msIdentifier>
                <msContents>
                    <textLang>
                        <lang xml:lang="ger"/>
                    </textLang>
                </msContents>
                <physDesc>
                    <objectDesc>
                        <supportDesc>
                            <extent>
                                <measure type="page">116</measure>
                                <measure type="format">8°</measure>
                            </extent>
                        </supportDesc>
                    </objectDesc>
                    <additions>
                        <list type="extent">
                            <item>
                                <span xml:lang="de">illustriert</span>
                                <span xml:lang="en">illustrated</span>
                            </item>
                        </list>
                        <list type="provenance">
                            <item>
                                <ref target="szdg:Bookplate"/>
                                <term xml:lang="de">Exlibris</term>
                                <term xml:lang="en">Bookplate</term>
                                <desc xml:lang="de">Stefan Zweig</desc>
                                <desc xml:lang="en">Stefan Zweig</desc>
                            </item>
                            <item>
                                <stamp>
                                    <ref target="szdg:Stamp"/>
                                    <term xml:lang="de">Stempel</term>
                                    <term xml:lang="en">Stamp</term>
                                </stamp>
                                <desc xml:lang="de">Rezensionsexemplar</desc>
                                <desc xml:lang="en">Rezensionsexemplar</desc>
                            </item>
                        </list>
                    </additions>
                    <bindingDesc>
                        <binding>
                            <ab xml:lang="de">Leinen</ab>
                            <ab xml:lang="en">cloth</ab>
                        </binding>
                    </bindingDesc>
                </physDesc>
                <history>
                    <provenance>
                        <orgName ref="szdg:LaterOwner" xml:lang="de">Antiquariat Neues Leben, Salzburg</orgName>
                        <orgName ref="szdg:LaterOwner" xml:lang="en">Neues Leben Rare Books, Salzburg</orgName>
                    </provenance>
                </history>
            </msDesc>
        </sourceDesc>
    </fileDesc>
    <profileDesc/>
</biblFull>
```



## [PersonalDocument](https://github.com/chpollin/SZD/tree/master/data/PersonalDocument), SZDLEB

- ana="szdg:WritingMaterial" - reference to http://stefanzweig.digital/o:szd.glossar/ONTOLOGY

```xml
<biblFull xml:id="SZDLEB.1">
    <fileDesc>
        <titleStmt>
            <title ana="assigned" xml:lang="de">Notizbuch Russlandreise</title>
            <title ana="assigned" xml:lang="en">Notebook Russian journey</title>
            <title type="Einheitssachtitel" xml:lang="de">Tagebücher</title>
            <title type="Einheitssachtitel" xml:lang="en">Diaries</title>
            <title type="Gesamttitel">Stefan Zweig - Sammlung Adolf Haslinger</title>
            <author ref="#SZDPER.1560">
                <persName ref="http://d-nb.info/gnd/118637479">
                    <surname>Zweig</surname>
                    <forename>Stefan</forename>
                </persName>
            </author>
        </titleStmt>
        <publicationStmt>
            <ab>Archivmaterial</ab>
        </publicationStmt>
        <sourceDesc>
            <msDesc>
                <msIdentifier>
                    <country>Österreich</country>
                    <settlement>Salzburg</settlement>
                    <repository ref="http://d-nb.info/gnd/1047604132">
                        Adolf Haslinger Literaturstiftung im Literaturarchiv Salzburg
                    </repository>
                    <idno type="signature">SZ-SAH/L1</idno>
                </msIdentifier>
                <msContents>
                    <summary>
                        <ab xml:lang="de">
                            Notizen aus der Zeit des Aufenthalts in Russland 1928
                        </ab>
                        <ab xml:lang="en">Notes from 1928 sojourn in Russia</ab>
                    </summary>
                    <textLang>
                        <lang xml:lang="ger">Deutsch</lang>
                    </textLang>
                </msContents>
                <physDesc>
                    <objectDesc>
                        <supportDesc>
                            <support>
                                <material ana="szdg:WritingMaterial" xml:lang="de">Kariertes Papier, Label „ELASTIC No. 1610“</material>
                                <material ana="szdg:WritingMaterial" xml:lang="en">Squared paper, label „ELASTIC No. 1610“</material>
                                <material ana="szdg:WritingInstrument" xml:lang="de">Violette Tinte, Bleistift</material>
                                <material ana="szdg:WritingInstrument" xml:lang="en">Purple ink, pencil</material>
                            </support>
                            <extent>
                                <span xml:lang="de">
                                    <term type="objecttyp">Notizbuch</term>
                                    ,
                                    <measure type="leaf">
                                        38 Blatt, 18 Blatt beschrieben, eingelegt: Manuskript, 2 Blatt; Theaterkarte
                                    </measure>
                                </span>
                                <span xml:lang="en">
                                    <term type="objecttyp">Notebook</term>
                                    ,
                                    <measure type="leaf">
                                        38 leaves, writing on 18 leaves, inserted: manuscript, 2 leaves; theatre ticket
                                    </measure>
                                </span>
                                <measure type="format">20x13 cm</measure>
                            </extent>
                            <foliation>
                                <ab xml:lang="de">Durchgehend nur recto paginiert</ab>
                                <ab xml:lang="en">Only rectos counted throughout</ab>
                            </foliation>
                        </supportDesc>
                    </objectDesc>
                    <handDesc>
                        <ab>Stefan Zweig</ab>
                    </handDesc>
                    <bindingDesc>
                        <binding>
                            <ab xml:lang="de">Metallrücken, Kunstlederumschlag</ab>
                            <ab xml:lang="en">Metal spine, leatherette covers</ab>
                        </binding>
                    </bindingDesc>
                    <accMat>
                        <list>
                            <item ana="szdg:Enclosures">
                                <desc xml:lang="de">
                                    Eingelegtes Manuskript, 1 Blatt, mit Adresse eigenhändig in violetter Tinte
                                </desc>
                                <desc xml:lang="en">
                                    Inserted manuscript, 1 leaf, with address, holograph in purple ink
                                </desc>
                                <measure type="format">11x8 cm</measure>
                            </item>
                            <item ana="szdg:Enclosures">
                                <desc xml:lang="de">
                                    Eingelegtes Manuskript, 1 Blatt, mit Notiz „Bajaderka von M. Petipa Musik von G. Minkus Semjenowa“ eigenhändig (?) in Bleistift
                                </desc>
                                <desc xml:lang="en">
                                    Inserted manuscript, 1 leaf, with note „Bajaderka von M. Petipa Musik von G. Minkus Semjenowa“, holograph (?) in pencil
                                </desc>
                                <measure type="format">16x10 cm</measure>
                            </item>
                            <item ana="szdg:Enclosures">
                                <desc xml:lang="de">
                                    Theaterkarten des Moskauer Kunsttheaters, No 10 und No 11 auf einem Bogen, verso Datumsstempel 14. September 1928
                                </desc>
                                <desc xml:lang="en">
                                    Theatre tickets for the Moscow Art Theatre, nos. 10 & 11 on a single sheet, stamped 14 Sept. 1928 on reverse
                                </desc>
                                <measure type="format">12x11 cm</measure>
                            </item>
                        </list>
                    </accMat>
                </physDesc>
                <history>
                    <origin>
                        <origDate>[1928]</origDate>
                    </origin>
                    <provenance>
                        <ab xml:lang="de">Dr. Werner, Wien</ab>
                        <ab xml:lang="en">Dr. Werner, Wien</ab>
                    </provenance>
                </history>
            </msDesc>
        </sourceDesc>
    </fileDesc>
    <profileDesc>
        <textClass>
            <keywords>
                <term type="classification" xml:lang="de">Tagebücher</term>
                <term type="classification" xml:lang="en">Diaries</term>
            </keywords>
        </textClass>
    </profileDesc>
</biblFull>
```



## [Work](https://github.com/chpollin/SZD/tree/master/data/Work), SZDMSK

- ana="szdg:WritingMaterial" - reference to http://stefanzweig.digital/o:szd.glossar/ONTOLOGY

```xml
<biblFull xml:id="SZDMSK.2">
    <fileDesc>
        <titleStmt>
            <title ana="supplied/verified">Clarissa</title>
            <title type="Einheitssachtitel">Clarissa</title>
            <title type="Gesamttitel">Stefan Zweig - Archiv Atrium Press</title>
            <author ref="SZDPER.1560">
                <persName ref="http://d-nb.info/gnd/118637479">
                    <surname>Zweig</surname>
                    <forename>Stefan</forename>
                </persName>
            </author>
        </titleStmt>
        <publicationStmt>
            <ab>Archivmaterial</ab>
        </publicationStmt>
        <sourceDesc>
            <msDesc>
                <msIdentifier>
                    <country>Österreich</country>
                    <settlement>Salzburg</settlement>
                    <repository ref="http://d-nb.info/gnd/1047605287">Literaturarchiv Salzburg</repository>
                    <idno type="signature">SZ-AAP/W1</idno>
                    <altIdentifier>
                        <idno type="PID">o:szd.6814</idno>
                    </altIdentifier>
                </msIdentifier>
                <msContents>
                    <textLang>
                        <lang xml:lang="ger">Deutsch</lang>
                    </textLang>
                </msContents>
                <physDesc>
                    <objectDesc>
                        <supportDesc>
                            <support>
                                <material ana="szdg:WritingMaterial" xml:lang="de">
                                    Notizbuch mit Händlermarke PAPELARIA DO POVO [...] A. M. GEOFFROY Petropolis;
                                </material>
                                <material ana="szdg:WritingMaterial" xml:lang="en">
                                    Notebook with stationer's label "PAPELARIA DO POVO [...] A. M. GEOFFROY Petropolis"
                                </material>
                                <material ana="szdg:WritingInstrument" xml:lang="de">Dunkelblaue, rote und schwarze Tinte, Bleistift</material>
                                <material ana="szdg:WritingInstrument" xml:lang="en">Navy, red, and black ink, pencil</material>
                            </support>
                            <extent>
                                <span xml:lang="de">
                                    <term type="objecttyp">Notizbuch</term>
                                    ,
                                    <measure ana="corrected" type="leaf">
                                        154 Blatt, 99 Blatt beschrieben, korrigiert; 1 Kuvert
                                    </measure>
                                </span>
                                <span xml:lang="en">
                                    <term type="objecttyp">Notebook</term>
                                    ,
                                    <measure ana="corrected" type="leaf">
                                        154 leaves, writing on 99 leaves, corrected; 1 envelope
                                    </measure>
                                </span>
                                <measure type="format">33x22 cm</measure>
                            </extent>
                        </supportDesc>
                    </objectDesc>
                    <handDesc>
                        <ab xml:lang="de">Stefan Zweig</ab>
                        <ab xml:lang="en">Stefan Zweig</ab>
                    </handDesc>
                    <bindingDesc>
                        <binding>
                            <ab xml:lang="de">Lederimitat mit schwarzem Leinenrücken</ab>
                            <ab xml:lang="en">Faux leather with black cloth spine</ab>
                        </binding>
                    </bindingDesc>
                    <accMat>
                        <list>
                            <item ana="szdg:Enclosures">
                                <desc xml:lang="de">
                                    Eingelegt ein Kuvert mit Aufschrift „Propriedade Stefan Zweig dezasete contos“ eigenhändig in schwarzer Tinte und „Last unfinished novel 1st sketch“ auf der Rückseite von Richard Friedenthals Hand
                                </desc>
                                <desc xml:lang="en">
                                    Inserted envelope inscribed "Propriedade Stefan Zweig dezasete contos", holograph in black ink, and "Last unfinished novel 1st sketch" on verso in Richard Friedenthal's hand
                                </desc>
                                <measure type="format">23x15 cm</measure>
                            </item>
                        </list>
                    </accMat>
                </physDesc>
                <history>
                    <origin>
                        <origPlace>Petropolis</origPlace>
                        <origDate when="1941-11-01">1. Nov. 1941</origDate>
                    </origin>
                    <provenance>
                        <ab xml:lang="de">Archiv Atrium Press</ab>
                        <ab xml:lang="en">Atrium Press</ab>
                    </provenance>
                    <acquisition>
                        <ab xml:lang="de">Ankauf Christie's London 2014</ab>
                        <ab xml:lang="en">Acquisition from Christie's London 2014</ab>
                    </acquisition>
                </history>
            </msDesc>
        </sourceDesc>
    </fileDesc>
    <profileDesc>
        <textClass>
            <keywords>
                <term type="classification" xml:lang="de">Romane/Erzählungen</term>
                <term type="classification" xml:lang="en">Novels/Stories</term>
            </keywords>
        </textClass>
    </profileDesc>
</biblFull>
```

## [Biography](https://github.com/chpollin/SZD/tree/master/data/Biography), SZDBIO

- <name ref="#SZDPER.1559" type="person"> - person search query
- <name ref="#SZDLEB.1" type="personaldocument|work|book">notebook</name> - URL to object

````XML
<event xml:id="SZDBIO.1">
    <head>
        <span xml:lang="de">Wien <date when="1881-11-28">28. November 1881</date>
        </span>
        <span xml:lang="en">Vienna, <date when="1881-11-28">28 November 1881</date>
        </span>
    </head>
    <ab xml:lang="de">
        <name>Stefan Zweig</name> wird als zweiter Sohn von <name ref="#SZDPER.1558" type="person">Ida</name> und <name ref="#SZDPER.1559" type="person">Moriz Zweig</name> im Haus Schottenring 14 geboren.</ab>
    <ab xml:lang="en">
        <name>Stefan Zweig</name> is born the second son of <name ref="#SZDPER.1558" type="person">Ida</name> and <name ref="#SZDPER.1559" type="person">Moriz Zweig</name> at 14, Schottenring.</ab>
</event>
````

## [Glossary](https://github.com/chpollin/SZD/tree/master/data/Glossary) 

## [Index](https://github.com/chpollin/SZD/tree/master/data/Index)

### [Person](https://github.com/chpollin/SZD/tree/master/data/Index/Person), SZDPER

- @corresp - URL to wikipedia

``` xml
<person corresp="https://de.wikipedia.org/wiki/Pierre_Abraham" xml:id="SZDPER.1">
    <persName ref="http://d-nb.info/gnd/12490310X">
        <surname>Abraham</surname>
        <forename>Pierre</forename>
    </persName>
    <note type="variants">Bloch, Pierre Abraham</note>
    <birth when="1892"/>
    <death when="1974"/>
    <idno type="wikidata">http://www.wikidata.org/entity/Q3383636</idno>
</person>
```

### [Location](https://github.com/chpollin/SZD/tree/master/data/Index/Location), SZDSTA

- @corresp - URL to institution web page
- t:location/t:geo - coordination for maps visualisation

```xml
<org corresp="https://www.uni-salzburg.at/index.php?id=72" xml:id="SZDSTA.1">
    <orgName ref="http://d-nb.info/gnd/1047605287">Literaturarchiv Salzburg</orgName>
    <country>Österreich</country>
    <settlement>Salzburg</settlement>
    <location>
        <geo>47.798, 13.048</geo>
    </location>
</org>
```

## [Issue](https://github.com/chpollin/SZD/tree/master/data/Issue)

```xml

```

