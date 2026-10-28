import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync, spawn } from 'node:child_process';

// Shared page-build logic of build-full.mjs, snapshot.mjs and the tests: the project
// stylesheets are materialised with every GAMS load redirected to the data repository or
// to a versioned GAMS input under fixtures/, and a page is rendered with SaxonJS.
export const here = dirname(fileURLToPath(import.meta.url));
// root is the gams-www checkout with the served files, by default ZIMLAB/szd beside this repository.
export const root = resolve(process.env.SZD_WWW || resolve(here, '../../ZIMLAB/szd'));
export const dataRoot = resolve(process.env.SZD_DATA_ROOT || resolve(here, '..'));
export const fixtureDir = resolve(here, 'fixtures');
const xslt3 = resolve(here, 'node_modules/xslt3/xslt3.js');

const dataSources = {
  "document('/o:szd.personen/TEI_SOURCE')": 'data/Index/Person/SZDPER.xml',
  "document('/o:szd.standorte/TEI_SOURCE')": 'data/Index/Location/SZDSTA.xml',
  // szd-Thema.xsl; o:szd.bibliothek is loaded without a datastream name, its TEI is SZDBIB
  "document('/o:szd.bibliothek')": 'data/Library/SZDBIB.xml',
  "document('/o:szd.werke/TEI_SOURCE')": 'data/Work/SZDMSK.xml',
  "document('/o:szd.lebensdokumente/TEI_SOURCE')": 'data/PersonalDocument/SZDLEB.xml'
};
// datastreams of context:szd, read by szd-context.xsl and szd-Suche.xsl
const contextStreams = ['STARTSEITE', 'ABOUT', 'IMPRINT', 'MISCELLANEOUS', 'SEARCH_HELP'];

// Revision label for a git revision, or 'worktree' for the files on disk.
export function revLabel(rev) {
  if (!rev || rev === 'worktree') { return 'worktree'; }
  return git(['rev-parse', '--short', rev + '^{commit}']).trim();
}

function git(args, cwd = root) {
  return execFileSync('git', args, { cwd, encoding: 'utf8', maxBuffer: 256 * 1024 * 1024 });
}

// Every szd-*.xsl of the revision, as text.
export function readStylesheets(rev) {
  if (!rev || rev === 'worktree') {
    const names = git(['ls-files', '--cached', '--others', '--exclude-standard', 'szd-*.xsl']).split('\n').filter(Boolean);
    return Object.fromEntries(names.filter((name) => existsSync(resolve(root, name))).map((name) => [name, readFileSync(resolve(root, name), 'utf8')]));
  }
  const names = git(['ls-tree', '--name-only', rev, '--', '.']).split('\n').filter((name) => /^szd-[^/]+\.xsl$/.test(name));
  return Object.fromEntries(names.map((name) => [name, git(['show', rev + ':' + name])]));
}

// SaxonJS 2.7 raises XTDE1071 "no current grouping key" when an xsl:for-each-group has
// two sort keys that call current-grouping-key(); Saxon on GAMS renders them. Two keys on
// the codepoint collation sort exactly like one key joined by a tab, because the filing key
// is normalize-space()d and so holds no character below the space. Harness only.
const twoGroupSorts = /<xsl:sort select="([^"]*current-grouping-key\(\)[^"]*)" data-type="text"\s+collation="(http:\/\/www\.w3\.org\/2005\/xpath-functions\/collation\/codepoint)"\/>\s*<xsl:sort select="(current-grouping-key\(\))" data-type="text"\s+collation="\2"\/>/g;

// Writes the stylesheets into xslDir with all loads redirected and returns the file names.
export function materialize(xslDir, stylesheets, { languages = resolve(fixtureDir, 'context-szd.LANGUAGES.xml') } = {}) {
  mkdirSync(xslDir, { recursive: true });
  for (const file of Object.values(dataSources)) {
    if (!existsSync(resolve(dataRoot, file))) { throw new Error('Missing SZD fixture: ' + resolve(dataRoot, file)); }
  }
  const url = (path) => pathToFileURL(path).href;
  const metadata = resolve(xslDir, 'metadata.xml');
  // the server-side modification date stays empty, see local-test-build/README.md
  writeFileSync(metadata, '<sparql xmlns="http://www.w3.org/2001/sw/DataAccess/rf1/result"><results/></sparql>');
  for (const [name, text] of Object.entries(stylesheets)) {
    let source = text;
    for (const [call, file] of Object.entries(dataSources)) {
      source = source.replaceAll(call, "document('" + url(resolve(dataRoot, file)) + "')");
    }
    source = source.replaceAll("document('/archive/objects/context:szd/datastreams/LANGUAGES/content')", "document('" + url(languages) + "')");
    source = source.replaceAll("document(concat('/archive/objects/', $PID, '/methods/sdef:Object/getMetadata'))", "document('" + url(metadata) + "')");
    for (const stream of contextStreams) {
      const target = "document('" + url(resolve(fixtureDir, 'context-szd.' + stream + '.xml')) + "')";
      source = source.replaceAll("document(concat('/context:szd/', '" + stream + "'))", target).replaceAll("document('/context:szd/" + stream + "')", target);
    }
    source = source.replace(twoGroupSorts, (match, first, collation, second) =>
      `<xsl:sort select="concat(${first}, codepoints-to-string(9), ${second})" data-type="text" collation="${collation}"/>`);
    writeFileSync(resolve(xslDir, name), source);
  }
  return Object.keys(stylesheets);
}

// File name of a rendered page, for instance szd-Werke.timeline.en.html.
export const outputName = (name, locale, mode) => name + (mode ? '.' + mode : '') + (locale === 'en' ? '.en' : '') + '.html';

// Renders one page. Resolves with the output path, rejects with the processor output.
export function render({ xslDir, page, input, out, name = page, locale = 'de', mode = '' }) {
  const output = resolve(out, outputName(name, locale, mode));
  const args = [xslt3, '-xsl:' + resolve(xslDir, page + '.xsl'), '-s:' + input, '-o:' + output, 'locale=' + locale];
  if (mode) { args.push('mode=' + mode); }
  if (page === 'szd-Facsimiles') {
    args.push('correspondence-index-uri=' + pathToFileURL(resolve(dataRoot, 'data/Correspondence/SZDKOR.xml')).href);
  }
  return new Promise((done, fail) => {
    const child = spawn(process.execPath, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let log = '';
    child.stdout.on('data', (chunk) => { log += chunk; });
    child.stderr.on('data', (chunk) => { log += chunk; });
    child.on('close', (status) => status === 0 ? done(output) : fail(new Error(outputName(name, locale, mode) + ' failed:\n' + log)));
  });
}

// Runs the async jobs with at most `limit` at a time and collects every failure.
export async function pool(jobs, limit) {
  const failures = [];
  let next = 0;
  const worker = async () => {
    while (next < jobs.length) {
      const job = jobs[next++];
      try { await job(); } catch (error) { failures.push(error); }
    }
  };
  await Promise.all(Array.from({ length: Math.min(limit, jobs.length) }, worker));
  return failures;
}
