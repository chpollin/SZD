import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { JSDOM } from 'jsdom';
import { buildDir } from './paths.mjs';

// Checks the full-text result page of szd-Suche.xsl against the hit list it was built from:
// every object of a holding the renderer knows gets exactly one card or block entry, the
// header counts them, and organisations, which szd-Suche.xsl once dropped, get a block of their
// own that links to their entry in the organisation index.
const page = 'szd-Suche-Volltext';
const input = resolve(buildDir, page + '.input.xml');
if (!existsSync(input)) { console.log('SKIP: ' + page + ' not built'); process.exit(2); }
const hits = readFileSync(input, 'utf8');
const uris = [...new Set([...hits.matchAll(/<re uri="([^"]+)"/g)].map(m => m[1]))];
const organisations = uris.filter(uri => uri.includes('/o:szd.organisation#'));
assert.ok(organisations.length, 'the fixture holds no organisation hit');
for (const [file, locale, heading] of [[page + '.html', 'de', 'Organisationen'], [page + '.en.html', 'en', 'Organisations']]) {
  const document = new JSDOM(readFileSync(resolve(buildDir, file), 'utf8')).window.document;
  assert.equal(document.getElementById('query_result').textContent.trim(), String(uris.length), file + ': hit count');
  const block = document.getElementById('organisation_search');
  assert.ok(block, file + ': no organisation block');
  assert.equal(block.querySelector('h3').textContent.trim(), heading, file + ': heading');
  const links = [...block.querySelectorAll('li > a')];
  assert.equal(links.length, organisations.length, file + ': one entry per organisation');
  for (const uri of organisations) {
    const id = uri.split('#')[1];
    assert.ok(links.some(a => a.getAttribute('href') === '/o:szd.organisation/sdef:TEI/get?locale=' + locale + '#' + id && a.textContent.trim()), file + ': link to ' + id);
  }
  const radio = document.getElementById('organisation_radio');
  assert.ok(radio && radio.value === 'organisation_search', file + ': filter button of the organisations');
  for (const uri of uris.filter(uri => !organisations.includes(uri))) {
    assert.equal(document.querySelectorAll('[data-uri="' + uri + '"]').length, 1, file + ': one card for ' + uri);
  }
}
console.log(`PASS ${page}: ${uris.length} objects, ${organisations.length} organisation(s) shown and counted in both languages`);
