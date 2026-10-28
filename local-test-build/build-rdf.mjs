import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, resolve, basename } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawnSync, execFileSync } from 'node:child_process';

// Runs szd-TORDF.xsl locally against TEI files of the data repo. The index objects that
// the stylesheet loads from GAMS are redirected to the local index files, so the run is
// offline and reproducible. With --rev the stylesheet of that git revision is used, which
// gives the baseline for the golden comparison in test/tordf.golden.mjs. --unavailable
// <host>/<pid>[,...] lets that host lack the index object, as GAMS does for an object not
// yet ingested there: doc-available() answers false and document() aborts the build.
const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(process.env.SZD_WWW || resolve(here, '../../ZIMLAB/szd'));
const argv = process.argv.slice(2);
const option = (name) => { const i = argv.indexOf(name); return i === -1 ? '' : argv.splice(i, 2)[1]; };
const rev = option('--rev');
const label = option('--label') || (rev ? rev : 'current');
const unavailable = option('--unavailable').split(',').filter(Boolean);
const sources = argv;
if (!sources.length) {
  throw new Error('Usage: node build-rdf.mjs [--rev <git-rev>] [--label <name>] [--unavailable <host>/<pid>,...] <tei.xml> [<tei.xml> ...]');
}
const out = resolve(process.env.SZD_RDF_BUILD_DIR || resolve(here, 'build-rdf'), label);
const dataRoot = resolve(process.env.SZD_DATA_ROOT || resolve(here, '..'));
mkdirSync(out, { recursive: true });

const indices = {
  'o:szd.personen': 'data/Index/Person/SZDPER.xml',
  'o:szd.organisation': 'data/Index/Organisation/SZDORG.xml',
  'o:szd.standorte': 'data/Index/Location/SZDSTA.xml',
  'o:szd.werkindex': 'data/Index/Werke/SZDWRK.xml'
};
for (const file of Object.values(indices)) {
  if (!existsSync(resolve(dataRoot, file))) { throw new Error('Missing SZD fixture: ' + file); }
}
// the language catalogue of context:szd, versioned as a GAMS input
const languageFile = resolve(here, 'fixtures', 'context-szd.LANGUAGES.xml');

let stylesheet = rev
  ? execFileSync('git', ['show', rev + ':szd-TORDF.xsl'], { cwd: root, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 })
  : readFileSync(resolve(root, 'szd-TORDF.xsl'), 'utf8');
// Every spelling of an index URL is redirected: the fixed production URL of the older
// stylesheet and each concat($host, '/<pid>/TEI_SOURCE') of the current one, which covers
// the host-derived loads and the host loop of the organisation list.
const missing = pathToFileURL(resolve(out, 'unavailable.xml')).href;
const indexTarget = (pid, host, hostIsLiteral) => {
  if (!indices[pid]) { throw new Error('No local fixture for ' + pid); }
  const fixture = "'" + pathToFileURL(resolve(dataRoot, indices[pid])).href + "'";
  const lacking = unavailable.filter(entry => entry.endsWith('/' + pid))
    .map(entry => entry.slice(0, -pid.length - 1).replace(/^https?:\/\//, ''));
  if (!lacking.length) { return fixture; }
  if (hostIsLiteral) { return lacking.includes(host.replace(/^https?:\/\//, '')) ? "'" + missing + "'" : fixture; }
  // compared without scheme, so that no http literal reaches a fetch call and trips the check below
  return "(if (substring-after(" + host + ", '//') = ('" + lacking.join("', '") + "')) then '" + missing + "' else " + fixture + ')';
};
for (const entry of unavailable) {
  if (!Object.keys(indices).some(pid => entry.endsWith('/' + pid))) { throw new Error('--unavailable names no index object: ' + entry); }
}
stylesheet = stylesheet
  .replace(/'(https:\/\/(?:gams|glossa)\.uni-graz\.at)\/(o:szd\.[a-z]+)\/TEI_SOURCE'/g,
    (match, host, pid) => indexTarget(pid, host, true))
  .replace(/concat\((\$[\w-]+), '\/(o:szd\.[a-z]+)\/TEI_SOURCE'\)/g,
    (match, host, pid) => indexTarget(pid, host, false));
stylesheet = stylesheet.replaceAll(
  "document('https://gams.uni-graz.at/archive/objects/context:szd/datastreams/LANGUAGES/content')",
  "document('" + pathToFileURL(languageFile).href + "')");
// Offline guard. No GAMS datastream URL may remain outside comments, and no argument of a
// loading function may name an http URL or a variable other than a rewritten local file.
const code = stylesheet.replace(/<!--[\s\S]*?-->/g, '');
const leftovers = code.match(/[^'"\s]*(?:TEI_SOURCE|\/datastreams\/)[^'"\s]*/g) || [];
for (const call of code.matchAll(/\b(?:document|doc|doc-available|unparsed-text(?:-lines|-available)?|json-doc|collection)\(/g)) {
  let depth = 1;
  let end = call.index + call[0].length;
  while (depth && end < code.length) { const c = code[end++]; depth += c === '(' ? 1 : c === ')' ? -1 : 0; }
  const argument = code.slice(call.index + call[0].length, end - 1).trim();
  if (argument !== '.' && (/https?:/.test(argument) || !argument.includes("'file:"))) { leftovers.push(call[0] + argument + ')'); }
}
if (leftovers.length) { throw new Error('Unredirected index or network loads: ' + leftovers.join(', ')); }
const stylesheetCopy = resolve(out, 'szd-TORDF.xsl');
writeFileSync(stylesheetCopy, stylesheet);

for (const source of sources) {
  const input = resolve(source);
  const name = basename(input).replace(/\.xml$/, '');
  const raw = resolve(out, name + '.raw.xml');
  const result = spawnSync(process.execPath, [resolve(here, 'node_modules/xslt3/xslt3.js'),
    '-xsl:' + stylesheetCopy, '-s:' + input, '-o:' + raw], { stdio: 'inherit' });
  if (result.status !== 0) { process.exit(result.status || 1); }
  // One element per line, so that the golden diff and the tests work on lines.
  const output = resolve(out, name + '.rdf.xml');
  writeFileSync(output, readFileSync(raw, 'utf8').replace(/></g, '>\n<') + '\n');
  console.log('OK RDF: ' + output);
}
