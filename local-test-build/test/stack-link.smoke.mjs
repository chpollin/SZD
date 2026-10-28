// Stack destinations must be supported by the curated TEI index, independently of heading slugs.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { JSDOM } from 'jsdom';
import { dataRoot } from '../harness.mjs';
import { buildDir } from './paths.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const build = buildDir;
const ns = 'http://www.tei-c.org/ns/1.0';
const normalize = value => value.replace(/\s+/g, ' ').trim().normalize('NFC');
const descendants = (node, name) => [...node.getElementsByTagNameNS(ns, name)];
const index = new JSDOM(readFileSync(resolve(dataRoot, 'data/Correspondence/SZDKOR.xml'), 'utf8'), { contentType: 'text/xml' }).window.document;
const byPartner = new Map();
for (const entry of descendants(index, 'biblFull')) {
  const pids = descendants(entry, 'idno').filter(n => n.getAttribute('type') === 'konvolut').map(n => normalize(n.textContent));
  for (const action of descendants(entry, 'correspAction')) {
    for (const name of [...action.children].filter(n => ['persName', 'orgName'].includes(n.localName))) {
      const surname = descendants(name, 'surname')[0]?.textContent;
      const forename = descendants(name, 'forename')[0]?.textContent;
      const partner = normalize(surname ? [surname, forename].filter(Boolean).join(', ') : name.textContent);
      if (!byPartner.has(partner)) byPartner.set(partner, new Set());
      for (const pid of pids) byPartner.get(partner).add(pid);
    }
  }
}
// Preserve the existing fragment convention while keeping it separate from PID lookup.
const from = 'àáâãäåāăąçćĉčďđèéêëēėęěĝğĥìíîïīĵķĺļľłñńņňòóôõöøōŕřśŝşšțťţùúûüūůųŵýÿŷźżž';
const to = 'aaaaaaaaaccccddeeeeeeeegghiiiiijkllllnnnnooooooorrsssstttuuuuuuuwyyyzzz';
const fold = new Map([...from].map((c, i) => [c, to[i]]));
const anchor = name => [...normalize(name).toLowerCase().replace(/ß/g, 'ss')].map(c => fold.get(c) || c).join('').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
const source = new JSDOM(readFileSync(resolve(build, 'szd-Facsimiles.input.xml'), 'utf8'), { contentType: 'text/xml' }).window.document;
const groups = new Map();
for (const result of source.getElementsByTagNameNS('http://www.w3.org/2001/sw/DataAccess/rf1/result', 'result')) {
  const names = [...result.children].filter(n => n.localName === 'creator' || (n.localName === 'contributor' && n.getAttribute('bound') !== 'false'));
  for (const node of names) {
    const name = normalize(node.textContent);
    if (name && name !== 'Zweig, Stefan') {
      groups.set(anchor(name), name);
      if (name === 'Unidentified') groups.set('withoutAuthor', name);
    }
  }
}
const html = new JSDOM(readFileSync(resolve(build, 'szd-Facsimiles.html'), 'utf8')).window.document;
let linked = 0, unlinked = 0, corrected = 0;
for (const heading of html.querySelectorAll('#facsimiles-gallery h2.mt-5')) {
  if (heading.id === 'withoutPartner') { assert.equal(heading.querySelector('a'), null); continue; }
  const name = groups.get(heading.id);
  assert.ok(name, 'Unrecognized or changed heading anchor: ' + heading.id);
  const pids = [...(byPartner.get(name) || [])];
  const expected = pids.length === 1 && /^o:szd\.korrespondenzen\.[A-Za-z0-9._-]+$/.test(pids[0]) ? pids[0] : null;
  const link = heading.querySelector('a');
  if (expected) {
    assert.ok(link, name + ': missing curated target');
    const url = new URL(link.getAttribute('href'), 'https://gams-staging.uni-graz.at');
    assert.equal(url.pathname, '/' + expected + '/sdef:TEI/get', name);
    assert.equal(url.origin, 'https://gams-staging.uni-graz.at');
    assert.equal(url.searchParams.get('locale'), 'de');
    linked++;
    if (expected !== 'o:szd.korrespondenzen.' + anchor(name)) corrected++;
  } else {
    assert.equal(link, null, name + ': unsupported stack destination');
    unlinked++;
  }
}
assert.ok(linked > 200);
assert.ok(unlinked > 0);
assert.ok(corrected > 0, 'No non-slug PID covered');
console.log(`OK curated gallery: ${linked} verified links, ${unlinked} unsupported targets suppressed, ${corrected} non-slug destinations`);

// Exercise the production lookup with ambiguity, punctuation, organisation names and unavailable input.
const scratch = resolve(buildDir, '../stack-lookup-test');
mkdirSync(scratch, { recursive: true });
const nameEntry = (name, pid, element = 'persName') => `<biblFull><idno type="konvolut">${pid}</idno><profileDesc><correspDesc><correspAction><${element}>${name}</${element}></correspAction></correspDesc></profileDesc></biblFull>`;
writeFileSync(resolve(scratch, 'index.xml'), `<TEI xmlns="${ns}"><text><body><listBibl>` +
  nameEntry('<surname>Exact</surname><forename>A.</forename>', 'o:szd.korrespondenzen.exact-a.') +
  nameEntry('<surname>Exact</surname><forename>A.</forename>', 'o:szd.korrespondenzen.exact-a.') +
  nameEntry('Ambiguous', 'o:szd.korrespondenzen.first') + nameEntry('Ambiguous', 'o:szd.korrespondenzen.second') +
  nameEntry('Café Society', 'o:szd.korrespondenzen.cafe', 'orgName') + nameEntry('Unsafe', 'https://example.org') +
  '</listBibl></body></text></TEI>');
// The lookup runs on the gallery stylesheet as built (xsl/ of the snapshot, GAMS loads
// redirected); the importing test stylesheet only replaces the entry point.
const gallery = pathToFileURL(resolve(buildDir, 'xsl/szd-Facsimiles.xsl')).href;
writeFileSync(resolve(scratch, 'lookup.xsl'), `<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fn="http://my-custom-functions"><xsl:import href="${gallery}"/><xsl:output method="text"/><xsl:template match="/"><xsl:for-each select="('Exact, A.', 'Ambiguous', 'Missing', 'Cafe&#x301; Society', 'Unsafe', 'Zweig, Stefan')"><xsl:value-of select="concat(fn:bundle-pid(.), '|')"/></xsl:for-each></xsl:template></xsl:stylesheet>`);
for (const [indexName, expected] of [['index.xml', 'o:szd.korrespondenzen.exact-a.|||o:szd.korrespondenzen.cafe|||'], ['absent.xml', '||||||']]) {
  const result = spawnSync(process.execPath, [resolve(here, '../node_modules/xslt3/xslt3.js'), '-xsl:' + resolve(scratch, 'lookup.xsl'), '-s:' + resolve(build, 'szd-Facsimiles.input.xml'), '-o:' + resolve(scratch, 'result.txt'), 'correspondence-index-uri=' + pathToFileURL(resolve(scratch, indexName)).href], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr + result.stdout);
  assert.equal(readFileSync(resolve(scratch, 'result.txt'), 'utf8'), expected);
}
console.log('OK production lookup: distinct curated PID, duplicate references, ambiguity, unknown partner, NFC organisation, invalid PID, missing source');
