import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { dataRoot } from '../harness.mjs';
import { rdfBaselineDir, rdfCurrentDir } from './paths.mjs';

// Checks the RDF that szd-TORDF.xsl produces for the organisation index and for the
// holdings that reference corporate bodies. Expectations come from the TEI files of the
// data repo, read here alongside the RDF, and from the migration log of the index.
const currentDir = rdfCurrentDir;
const baselineDir = rdfBaselineDir;
const BASE = 'https://gams.uni-graz.at/';
const ORG = BASE + 'o:szd.organisation#';
const PER = BASE + 'o:szd.personen#';
const STA = BASE + 'o:szd.standorte#';

const unescape = (text) => text.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&apos;/g, "'");
const normalize = (text) => unescape(text).replace(/\s+/g, ' ').trim();
const rdf = (name) => {
  const file = resolve(currentDir, name + '.rdf.xml');
  assert.ok(existsSync(file), 'not built: ' + file);
  return readFileSync(file, 'utf8');
};
const tei = (path) => readFileSync(resolve(dataRoot, path), 'utf8');
// One resource block per rdf:about, from the one-element-per-line output of build-rdf.mjs.
const block = (text, about) => {
  const start = text.indexOf('rdf:about="' + about + '"');
  assert.ok(start !== -1, 'no resource ' + about);
  const open = text.lastIndexOf('\n<', start) + 1;
  const tag = text.slice(open + 1, text.indexOf(' ', open));
  const end = text.indexOf('</' + tag + '>', start);
  return text.slice(open, end);
};
const entries = (text, element, idAttr = 'xml:id') =>
  [...text.matchAll(new RegExp('<' + element + '\\b[^>]*' + idAttr + '="([^"]+)"[^>]*>([\\s\\S]*?)</' + element + '>', 'g'))]
    .map(match => ({ id: match[1], body: match[2], head: match[0].slice(0, match[0].indexOf('>')) }));

// The organisation index, as the tests expect it.
const orgIndex = tei('data/Index/Organisation/SZDORG.xml');
const orgs = entries(orgIndex.slice(orgIndex.indexOf('<listOrg>')), 'org').map(org => {
  const names = [...org.body.matchAll(/<orgName([^>]*)>([\s\S]*?)<\/orgName>/g)];
  const main = names.find(name => !name[1].includes('type="variant"'));
  return {
    id: org.id,
    name: normalize(main[2]),
    gnd: (main[1].match(/ref="([^"]+)"/) || [])[1],
    corresp: (org.head.match(/corresp="([^"]+)"/) || [])[1],
    settlement: (org.body.match(/<settlement>([^<]*)<\/settlement>/) || [])[1],
    country: (org.body.match(/<country>([^<]*)<\/country>/) || [])[1],
    standort: (org.body.match(/<idno type="SZDSTA">([^<]*)<\/idno>/) || [])[1],
    superseded: [...org.body.matchAll(/<idno type="SZDPER" subtype="superseded">([^<]*)<\/idno>/g)].map(m => m[1])
  };
});
assert.ok(orgs.length > 50, 'organisation index looks truncated');
const orgByGnd = new Map(orgs.filter(org => org.gnd).map(org => [org.gnd, org.id]));
const superseded = orgs.flatMap(org => org.superseded);
assert.ok(superseded.length, 'no superseded person ids in the index');

// 2. Organisation index
{
  const out = rdf('SZDORG');
  assert.equal((out.match(/<szd:Organisation /g) || []).length, orgs.length, 'one szd:Organisation per org');
  assert.ok(!out.includes('<szd:Location '), 'organisation index typed as szd:Location');
  for (const org of orgs) {
    const resource = block(out, ORG + org.id);
    assert.ok(resource.startsWith('<szd:Organisation '), org.id + ': wrong class');
    const name = resource.match(/<szd:name(?: xml:lang="[a-z]+")?>([^<]*)<\/szd:name>/);
    assert.ok(name, org.id + ': no szd:name');
    assert.equal(normalize(name[1]), org.name, org.id + ': name');
    const expect = (present, line, label) => assert.equal(resource.includes(line), Boolean(present), org.id + ': ' + label);
    expect(org.gnd, '<szd:gnd rdf:resource="' + org.gnd + '"/>', 'gnd');
    expect(org.corresp, '<rdfs:seeAlso rdf:resource="' + org.corresp + '"/>', 'corresp');
    expect(org.settlement, '<szd:settlement>' + org.settlement + '</szd:settlement>', 'settlement');
    expect(org.country, '<szd:country>' + org.country + '</szd:country>', 'country');
    expect(org.standort, '<rdfs:seeAlso rdf:resource="' + STA + org.standort + '"/>', 'repository link');
    for (const id of org.superseded) assert.ok(resource.includes('<dcterms:replaces rdf:resource="' + PER + id + '"/>'), org.id + ': replaces ' + id);
    assert.equal((resource.match(/<dcterms:replaces /g) || []).length, org.superseded.length, org.id + ': replaces count');
    const fulltext = resource.match(/<gams:textualContent>([^<]*)<\/gams:textualContent>/);
    assert.ok(fulltext && normalize(fulltext[1]).includes(org.name) && fulltext[1].includes(org.id), org.id + ': fulltext');
    assert.ok(resource.includes('<gams:isMemberOfCollection rdf:resource="https://gams.uni-graz.at/o:szd.organisation"/>'), org.id + ': collection');
  }
  console.log(`PASS SZDORG: ${orgs.length} organisations with name, authority data, links and fulltext`);
}

// 3. Resolution in the holdings
const agentLine = (property, target) => '<' + property + ' rdf:resource="' + target + '"/>';
{
  const out = rdf('SZDKOR');
  const source = tei('data/Correspondence/SZDKOR.xml');
  let resolved = 0;
  let unresolved = 0;
  for (const entry of entries(source, 'biblFull')) {
    const resource = block(out, BASE + 'o:szd.korrespondenzen#' + entry.id);
    for (const action of entry.body.matchAll(/<correspAction type="(sent|received)">([\s\S]*?)<\/correspAction>/g)) {
      const property = action[1] === 'sent' ? 'szd:sender' : 'szd:receiver';
      for (const ref of action[2].matchAll(/<orgName[^>]*ref="([^"]+)"/g)) {
        if (orgByGnd.has(ref[1])) {
          assert.ok(resource.includes(agentLine(property, ORG + orgByGnd.get(ref[1]))), entry.id + ': ' + property + ' ' + ref[1]);
          resolved++;
        } else {
          assert.ok(!resource.includes(ref[1]), entry.id + ': unresolvable GND ' + ref[1] + ' leaked into the RDF');
          unresolved++;
        }
      }
    }
  }
  assert.ok(resolved, 'no corporate sender or receiver resolved');
  // SZDKOR.41: corporate sender with GND 5158511-X next to the person SZDPER.1983
  const sample = block(out, BASE + 'o:szd.korrespondenzen#SZDKOR.41');
  assert.ok(sample.includes(agentLine('szd:sender', ORG + orgByGnd.get('http://d-nb.info/gnd/5158511-X'))));
  assert.ok(sample.includes(agentLine('szd:sender', PER + 'SZDPER.1983')), 'person sender of SZDKOR.41 lost');
  // The only GND without index entry, 117322695, stands on a keyword term[@type='organization'];
  // no agent position in the current data carries an unresolvable GND.
  assert.ok(!/rdf:resource="[^"]*117322695/.test(out), 'GND without index entry leaked as a resource');
  console.log(`PASS SZDKOR: ${resolved} corporate senders or receivers resolved, ${unresolved} unresolvable GND in agent positions, the unresolvable keyword GND produces no resource`);
}
{
  const out = rdf('SZDBIB');
  // the four entries the migration log names, with the targets it recorded
  const migrated = { 'SZDBIB.92': 'SZDORG.51', 'SZDBIB.410': 'SZDORG.38', 'SZDBIB.502': 'SZDORG.60', 'SZDBIB.664': 'SZDORG.36' };
  for (const [id, org] of Object.entries(migrated)) {
    assert.ok(block(out, BASE + 'o:szd.bibliothek#' + id).includes(agentLine('szd:editor', ORG + org)), id + ': editor ' + org);
  }
  assert.ok(block(out, BASE + 'o:szd.bibliothek#SZDBIB.92').includes(agentLine('szd:author', PER + 'SZDPER.1560')), 'person author of SZDBIB.92 lost');
  const source = tei('data/Library/SZDBIB.xml');
  let count = 0;
  for (const entry of entries(source, 'biblFull')) {
    const title = entry.body.match(/<titleStmt>([\s\S]*?)<\/titleStmt>/)[1];
    for (const editor of title.matchAll(/<editor(?![^>]*role=)[^>]*>([\s\S]*?)<\/editor>/g)) {
      const ref = editor[1].match(/<orgName[^>]*ref="([^"]+)"/);
      if (!ref) continue;
      const target = ref[1].startsWith(ORG) ? ref[1] : ORG + orgByGnd.get(ref[1]);
      assert.ok(block(out, BASE + 'o:szd.bibliothek#' + entry.id).includes(agentLine('szd:editor', target)), entry.id + ': editor');
      count++;
    }
  }
  assert.equal(count, Object.keys(migrated).length, 'corporate editors in SZDBIB');
  console.log(`PASS SZDBIB: ${count} corporate editors resolved, GND lookup and SZDORG pass-through`);
}
{
  const out = rdf('SZDLEB');
  const source = tei('data/PersonalDocument/SZDLEB.xml');
  let count = 0;
  for (const entry of entries(source, 'biblFull')) {
    const title = entry.body.match(/<titleStmt>([\s\S]*?)<\/titleStmt>/)[1];
    const resource = block(out, BASE + 'o:szd.lebensdokumente#' + entry.id);
    for (const ref of title.matchAll(/<editor role="contributor"[^>]*><orgName[^>]*ref="([^"]+)"/g)) {
      assert.ok(orgByGnd.has(ref[1]), entry.id + ': contributor GND missing in the index ' + ref[1]);
      assert.ok(resource.includes(agentLine('szd:partyInvolved', ORG + orgByGnd.get(ref[1]))), entry.id + ': partyInvolved');
      count++;
    }
    if (title.includes('ref="#SZDPER.1560"')) assert.ok(resource.includes(PER + 'SZDPER.1560'), entry.id + ': person contributor lost');
  }
  assert.ok(count, 'no corporate party involved in SZDLEB');
  console.log(`PASS SZDLEB: ${count} corporate parties involved resolved, persons unchanged`);
}
{
  const out = rdf('SZDAUT');
  assert.ok(!out.includes(ORG), 'SZDAUT carries no corporate agents in its title statements');
  assert.ok(out.includes('<szd:location rdf:resource="' + STA + 'SZDSTA.4"/>'), 'repository resolution of SZDAUT (Fondation Martin Bodmer) lost');
  console.log('PASS SZDAUT: repositories still resolve to o:szd.standorte, no organisation URI');
}
// Every person of a multi-valued @ref and every GND in the https spelling yields its person
// URI, because the person search matches nothing else. GetPersonlist once read only the first
// blank-separated token, so a leading blank or tab lost the only one, and compared GNDs with
// their scheme. A persName inside an author or editor that
// carries its own @ref is not transformed, the outer @ref wins.
{
  const gnds = (ref) => ref.split(/[\s;,]+/).filter(token => token.includes('d-nb.info/gnd/'))
    .map(token => token.split('d-nb.info/gnd/')[1].replace(/\/+$/, '')).filter(Boolean);
  const personsByGnd = new Map();
  for (const person of entries(tei('data/Index/Person/SZDPER.xml'), 'person')) {
    for (const ref of person.body.matchAll(/<persName[^>]*ref="([^"]*)"/g)) {
      for (const gnd of gnds(ref[1])) personsByGnd.set(gnd, [...(personsByGnd.get(gnd) || []), person.id]);
    }
  }
  const holdings = [['SZDBIB', 'Library', 'bibliothek'], ['SZDKOR', 'Correspondence', 'korrespondenzen'],
    ['SZDLEB', 'PersonalDocument', 'lebensdokumente'], ['SZDESS', 'Aufsatzablage', 'aufsatzablage'], ['SZDMSK', 'Work', 'werke']];
  for (const [name, folder, collection] of holdings) {
    if (['SZDESS', 'SZDMSK'].includes(name) && !existsSync(resolve(currentDir, name + '.rdf.xml'))) continue;
    const out = rdf(name);
    let count = 0;
    for (const entry of entries(tei('data/' + folder + '/' + name + '.xml'), 'biblFull')) {
      const body = entry.body.replace(/(<(author|editor)\b[^>]*\sref="[^"]*"[^>]*>)([\s\S]*?)(<\/\2>)/g,
        (match, open, tag, inner, close) => open + inner.replace(/ ref="[^"]*"/g, '') + close);
      let resource;
      for (const ref of body.matchAll(/<(?:author|editor|persName|term)\b[^>]*\sref="([^"]*)"/g)) {
        const value = ref[1].replace(/&#\d+;/g, ' ');
        const tokens = value.trim().split(/[\s;,]+/);
        if (tokens.length < 2 && !value.includes('https://d-nb.info/gnd/') && !/^\s/.test(value)) continue;
        const ids = [...tokens.filter(token => /^#SZDPER\.\d+$/.test(token)).map(token => token.slice(1)),
          ...gnds(value).flatMap(gnd => personsByGnd.get(gnd) || [])];
        resource ??= block(out, BASE + 'o:szd.' + collection + '#' + entry.id);
        for (const id of ids) {
          assert.ok(resource.includes('rdf:resource="' + PER + id + '"'), entry.id + ': ' + id + ' from @ref "' + ref[1] + '" has no triple');
          count++;
        }
      }
    }
    assert.ok(count, name + ': no multi-valued or https person reference checked');
    console.log(`PASS ${name}: ${count} persons from multi-valued or https references resolved`);
  }
}

// Corrections of refactoring phase 1 (2026-10-21), each checked against the TEI it comes from.
{
  // the work search matches szd:relationToWork against …/o:szd.werkindex#SZDWRK.n
  const out = rdf('SZDBIB');
  let count = 0;
  for (const entry of entries(tei('data/Library/SZDBIB.xml'), 'biblFull')) {
    const refs = [...entry.body.matchAll(/<term type="work" ref="#?(SZDWRK\.\d+)"/g)].map(m => m[1]);
    if (!refs.length) continue;
    const resource = block(out, BASE + 'o:szd.bibliothek#' + entry.id);
    for (const id of refs) assert.ok(resource.includes('<szd:relationToWork rdf:resource="' + BASE + 'o:szd.werkindex#' + id + '"/>'), entry.id + ': relationToWork ' + id);
    count += refs.length;
  }
  assert.ok(!out.includes('werkindex##'), 'SZDBIB: work reference with a double #');
  assert.ok(count, 'SZDBIB: no work reference checked');
  console.log(`PASS SZDBIB: ${count} work references resolve to o:szd.werkindex`);
}
{
  // the English extent text counts the pieces of correspondence in singular or plural
  const out = rdf('SZDKOR');
  let count = 0;
  for (const entry of entries(tei('data/Correspondence/SZDKOR.xml'), 'biblFull')) {
    const pieces = [...entry.body.matchAll(/<measure type="correspondence"[^>]*>\s*(\d+)\s*<\/measure>/g)].reduce((sum, m) => sum + Number(m[1]), 0);
    if (!pieces) continue;
    const extent = block(out, BASE + 'o:szd.korrespondenzen#' + entry.id + 'EX');
    assert.ok(extent.includes('<szd:text xml:lang="en">' + pieces + (pieces > 1 ? ' Pieces' : ' Piece') + ' of Correspondence'), entry.id + ': English extent for ' + pieces);
    assert.ok(extent.includes('<szd:text xml:lang="de">' + pieces + (pieces > 1 ? ' Korrespondenzstücke' : ' Korrespondenzstück')), entry.id + ': German extent for ' + pieces);
    count++;
  }
  assert.ok(count > 700, 'SZDKOR: too few extents checked');
  console.log(`PASS SZDKOR: ${count} extents count their pieces in singular or plural in both languages`);
}
for (const [name, path, collection] of [['SZDBIB', 'data/Library/SZDBIB.xml', 'bibliothek'], ['SZDAUT', 'data/Autograph/SZDAUT.xml', 'autographen']]) {
  // the English extent says leaf or leaves, the German one Blatt
  const out = rdf(name);
  let count = 0;
  for (const entry of entries(tei(path), 'biblFull')) {
    const leaf = entry.body.match(/<measure type="leaf"[^>]*>\s*([^<]*?)\s*<\/measure>/);
    if (!leaf) continue;
    const extent = block(out, BASE + 'o:szd.' + collection + '#' + entry.id + 'EX');
    const en = (extent.match(/<szd:text xml:lang="en">([^<]*)<\/szd:text>/) || [])[1] || '';
    const de = (extent.match(/<szd:text xml:lang="de">([^<]*)<\/szd:text>/) || [])[1] || '';
    assert.ok(en.includes(leaf[1] + '  ' + (leaf[1] === '1' ? 'leaf' : 'leaves') + ' '), entry.id + ': English leaf count "' + en + '"');
    assert.ok(!en.includes('Blatt'), entry.id + ': German word in the English extent');
    assert.ok(de.includes(leaf[1] + '  Blatt '), entry.id + ': German leaf count');
    count++;
  }
  assert.ok(count, name + ': no leaf extent checked');
  console.log(`PASS ${name}: ${count} leaf extents in English and German`);
}

// 4. Negative cases and 5. structure, over every built file
const outputs = readdirSync(currentDir).filter(name => name.endsWith('.rdf.xml'));
for (const file of outputs) {
  const out = readFileSync(resolve(currentDir, file), 'utf8');
  assert.ok(!/rdf:resource=""/.test(out), file + ': empty resource');
  assert.ok(!/<szd:location rdf:resource="[^"]*o:szd\.organisation#/.test(out), file + ': location pointing at an organisation');
  assert.ok(!/<szd:(sender|receiver|editor|author|partyInvolved|affectedPerson|relationToPerson) rdf:resource="[^"]*o:szd\.standorte#/.test(out), file + ': agent pointing at a repository');
  for (const id of superseded) {
    const pattern = new RegExp('rdf:resource="[^"]*#' + id.replace('.', '\\.') + '"');
    for (const line of out.split('\n')) {
      if (pattern.test(line)) assert.ok(line.startsWith('<dcterms:replaces '), file + ': superseded ' + id + ' used as resource: ' + line);
    }
  }
  const errors = (text) => (text.match(/Error: no GND or SZDPER found/g) || []).length;
  const baselineFile = resolve(baselineDir, file);
  if (existsSync(baselineFile)) assert.equal(errors(out), errors(readFileSync(baselineFile, 'utf8')), file + ': more unresolved agents than the baseline');
  const abouts = out.match(/rdf:about="[^"]*"/g) || [];
  const duplicates = abouts.filter((about, i) => abouts.indexOf(about) !== i);
  if (file === 'SZDORG.rdf.xml') {
    assert.deepEqual(duplicates, [], 'duplicate rdf:about');
  } else if (existsSync(baselineFile)) {
    const known = readFileSync(baselineFile, 'utf8').match(/rdf:about="[^"]*"/g) || [];
    const knownDuplicates = new Set(known.filter((about, i) => known.indexOf(about) !== i));
    assert.deepEqual(duplicates.filter(about => !knownDuplicates.has(about)), [], file + ': new duplicate rdf:about');
  }
  console.log(`PASS ${file}: no empty or superseded resources, ${abouts.length} rdf:about, ${new Set(duplicates).size} duplicates known from the baseline`);
}

// RDF/XML parse with rdflib, which is installed system-wide and not a harness dependency.
const parser = spawnSync('python', ['-c', [
  'import sys, rdflib',
  'for path in sys.argv[1:]:',
  '    graph = rdflib.Graph(); graph.parse(path, format="xml")',
  '    print(f"{path.split(chr(92))[-1].split(chr(47))[-1]}: {len(graph)} triples")'
].join('\n'), ...outputs.map(file => resolve(currentDir, file))], { encoding: 'utf8' });
if (parser.status === 0) {
  console.log('PASS rdflib parse:\n' + parser.stdout.trim());
} else if (/No module named|not found|not recognized/i.test(parser.stderr + parser.stdout)) {
  console.log('NOT CHECKED: RDF/XML parse skipped, python with rdflib is not available');
} else {
  throw new Error('RDF/XML parse failed: ' + parser.stderr);
}
