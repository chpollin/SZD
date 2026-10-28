import { readFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { JSDOM } from 'jsdom';
import { buildDir } from './paths.mjs';

// Checks every built page of the snapshot for the defect classes the live audit of
// 2026-10-13 found across the site: page links that drop the locale, jump links without a
// target, duplicate ids, non-void elements the XML serialiser self-closed (an HTML parser
// keeps them open and swallows what follows), placeholder or inverted alt texts, metadata
// rows with an empty value, links to retired or staging hosts, and entries that one language
// renders and the other drops. It reports counts per page and fails on any violation.
//   node test/page-hygiene.smoke.mjs [<page>.html ...]   (default: every page of the snapshot)
const argv = process.argv.slice(2);
const files = argv.length ? argv : readdirSync(buildDir).filter((f) => f.endsWith('.html')).sort();

// Raw datastreams, viewer and image addresses are not pages and carry no locale.
const nonPage = /\/(TEI_SOURCE|RDF|ONTOLOGY|IMG\.\d+)$|\/datastreams\/|\/sdef:IIIF\/|\/methods\/sdef:(IIIF|Query)\//;
// HTML void elements and the SVG shapes of the inline icons, which may self-close.
const voidTags = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr',
  'path', 'circle', 'rect', 'line', 'polyline', 'polygon', 'ellipse', 'use', 'stop', 'image']);
const selfClosedPattern = /<([a-zA-Z][a-zA-Z0-9]*)(\s[^<>]*?)?\/>/g;
const badAlt = /^(|STARTBILD_TITLE|React|Angular|Vue|Svelte|Faksimile fehlt im Objekt .*|Facsimile missing in object .*)$/;
const deadHosts = /^(https?:)?\/\/(glossa\.uni-graz\.at|gams-staging\.uni-graz\.at|localhost)/;
const entryId = /^SZD[A-Z]+\.\d+$/;

function pageLinksWithoutLocale(document) {
  return [...document.querySelectorAll('a[href]')].map((a) => a.getAttribute('href'))
    .filter((h) => /^\/(o|context|query):/.test(h) && !nonPage.test(h) && !/[?&]locale=/.test(h));
}

function deadAnchors(document) {
  const ids = new Set([...document.querySelectorAll('[id]')].map((e) => e.id));
  return [...document.querySelectorAll('a[href^="#"]')].map((a) => a.getAttribute('href'))
    .filter((h) => h.length > 1 && !ids.has(decodeURIComponent(h.slice(1))));
}

function duplicateIds(document) {
  const seen = new Set(); const dup = new Set();
  for (const e of document.querySelectorAll('[id]')) { if (seen.has(e.id)) dup.add(e.id); seen.add(e.id); }
  return [...dup];
}

// GAMS serialises an empty element as <div/> whatever the page's xsl:output says, so an
// element that the local XHTML output writes as <div></div> breaks on the server. The page
// shell fills every empty non-void element with a comment; an empty pair means that failed.
const emptyPairPattern = /<([a-zA-Z][a-zA-Z0-9]*)(\s[^<>]*?)?><\/\1>/g;

function selfClosedNonVoid(html) {
  const hits = [];
  for (const pattern of [selfClosedPattern, emptyPairPattern]) {
    for (const m of html.matchAll(pattern)) { if (!voidTags.has(m[1].toLowerCase())) hits.push(m[0].slice(0, 60)); }
  }
  return hits;
}

function badAltTexts(document) {
  return [...document.querySelectorAll('img')].map((img) => img.getAttribute('alt'))
    .filter((alt) => alt === null || badAlt.test(alt.trim())).map((alt) => alt === null ? '(missing)' : alt);
}

function emptyMetadataValues(document) {
  return [...document.querySelectorAll('.szd-metadata dd')].filter((dd) => !dd.textContent.trim() && !dd.children.length)
    .map((dd) => dd.previousElementSibling?.textContent.trim() || '(no label)');
}

function deadHostLinks(document) {
  return [...document.querySelectorAll('a[href],img[src],script[src],link[href]')]
    .map((e) => e.getAttribute('href') || e.getAttribute('src')).filter((u) => deadHosts.test(u));
}

function entryIds(document) {
  return new Set([...document.querySelectorAll('[id]')].map((e) => e.id).filter((id) => entryId.test(id)));
}

function sample(list, n = 3) { return [...new Set(list)].slice(0, n).join(', '); }

let failed = 0;
const entries = new Map();
for (const file of files) {
  const html = readFileSync(resolve(buildDir, file), 'utf8');
  const dom = new JSDOM(html);
  const document = dom.window.document;
  const findings = {
    'links without locale': pageLinksWithoutLocale(document),
    'dead anchors': deadAnchors(document),
    'duplicate ids': duplicateIds(document),
    'self-closed elements': selfClosedNonVoid(html),
    'bad alt texts': badAltTexts(document),
    'empty metadata values': emptyMetadataValues(document),
    'dead host links': deadHostLinks(document),
  };
  entries.set(file, entryIds(document));
  dom.window.close();
  // jsdom frees a closed window only after the event loop turns; without the yield the
  // library and autograph pages pile up beyond the default heap
  await new Promise((done) => setImmediate(done));
  const open = Object.entries(findings).filter(([, list]) => list.length);
  if (open.length) {
    failed++;
    console.log(`FAIL ${file}: ` + open.map(([name, list]) => `${list.length} ${name} (${sample(list)})`).join('; '));
  } else {
    console.log(`PASS ${file}`);
  }
}

// Language parity: the German and the English page of one input render the same entries.
for (const [file, ids] of entries) {
  if (!file.endsWith('.en.html')) continue;
  const german = file.replace(/\.en\.html$/, '.html');
  if (!entries.has(german)) continue;
  const other = entries.get(german);
  const onlyDe = [...other].filter((id) => !ids.has(id));
  const onlyEn = [...ids].filter((id) => !other.has(id));
  if (onlyDe.length || onlyEn.length) {
    failed++;
    console.log(`FAIL ${german} vs ${file}: ${onlyDe.length} entries only in German (${sample(onlyDe)}), ${onlyEn.length} only in English (${sample(onlyEn)})`);
  }
}

console.log(failed ? `${failed} page(s) with findings` : 'all pages clean');
process.exit(failed ? 1 : 0);
