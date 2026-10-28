import { existsSync, readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { here, dataRoot } from '../harness.mjs';
import { buildSnapshot } from '../snapshot.mjs';
import { buildDir, rdfDir, rdfBaselineDir } from './paths.mjs';

// Runs every suite of the harness: builds the working-tree snapshot of all pages and the RDF
// it needs, then each test, and prints passed, failed and skipped. A test that exits with 2
// counts as skipped.
//   node test/run-all.mjs [--suite unit,proto,pages,rdf] [--no-build]
const argv = process.argv.slice(2);
const suiteArg = argv.includes('--suite') ? (argv[argv.indexOf('--suite') + 1] || '').split(',') : null;
const noBuild = argv.includes('--no-build');
const baselineRev = process.env.SZD_RDF_BASELINE_REV || 'faa784a';
const rdfSources = ['data/Index/Location/SZDSTA.xml', 'data/Index/Organisation/SZDORG.xml', 'data/Correspondence/SZDKOR.xml',
  'data/Library/SZDBIB.xml', 'data/Autograph/SZDAUT.xml', 'data/PersonalDocument/SZDLEB.xml',
  'data/Correspondence/konvolute/szd.korrespondenzen.meiler-friedrich.xml'].map((file) => resolve(dataRoot, file));
const issueDir = resolve(dataRoot, 'data/Issue');
const themes = existsSync(issueDir) ? readdirSync(issueDir, { withFileTypes: true }).filter((entry) => entry.isDirectory())
  .flatMap((entry) => readdirSync(resolve(issueDir, entry.name)).filter((name) => /^szd-thema.*\.xml$/.test(name)).map((name) => resolve(issueDir, entry.name, name))) : [];
// full-pages.smoke.mjs checks metadata lists, so it takes the pages that render them
const fullPages = ['szd-Autographen.html', 'szd-Autographen.en.html', 'szd-Bibliothek.html', 'szd-Bibliothek.en.html',
  'szd-Werke.html', 'szd-Werke.en.html', 'szd-Lebensdokumente.html', 'szd-Lebensdokumente.en.html',
  'szd-Essays.html', 'szd-Essays.en.html', 'szd-Korrespondenzen.html', 'szd-Korrespondenzen.en.html',
  'szd-Konvolut.html', 'szd-Konvolut.en.html', 'szd-Thema1.html', 'szd-Thema1.en.html'];

const suites = {
  unit: ['test/databasket.test.mjs', 'test/szd-navigation.smoke.mjs', 'test/iiif-download.smoke.mjs'],
  proto: ['proto/proto.smoke.mjs', 'proto/lebenskalender.smoke.mjs', 'proto/zeitleiste-lanes.smoke.mjs'],
  pages: ['test/asset-version.smoke.mjs', 'test/extended-list-views.smoke.mjs', 'test/list-views.smoke.mjs', 'test/register-index.smoke.mjs',
    'test/register-index.golden.mjs', 'test/konvolut.smoke.mjs', 'test/stack-link.smoke.mjs',
    'test/konvolut-datum.smoke.mjs', 'test/lebenskalender-timeline.smoke.mjs', ['test/full-pages.smoke.mjs', ...fullPages],
    'test/search-results.smoke.mjs', 'test/page-hygiene.smoke.mjs'],
  rdf: ['test/tordf.golden.mjs', 'test/tordf.smoke.mjs', 'test/tordf-org-fallback.smoke.mjs', 'test/tordf-thema.smoke.mjs', 'test/tordf.strict.mjs']
};
if (suiteArg && suiteArg.some((name) => !Object.hasOwn(suites, name))) {
  console.error('Invalid --suite: expected a comma-separated selection of ' + Object.keys(suites).join(', '));
  process.exit(1);
}
const chosen = Object.keys(suites).filter((name) => !suiteArg || suiteArg.includes(name));
const needsData = (suite) => suite === 'pages' || suite === 'rdf';
const dataPresent = existsSync(resolve(dataRoot, 'data'));

const run = (args, { quiet = true } = {}) => new Promise((done) => {
  const child = spawn(process.execPath, args, { cwd: here, env: { ...process.env, SZD_TEST_BUILD_DIR: buildDir, SZD_RDF_BUILD_DIR: rdfDir } });
  let log = '';
  child.stdout.on('data', (chunk) => { log += chunk; if (!quiet) { process.stdout.write(chunk); } });
  child.stderr.on('data', (chunk) => { log += chunk; if (!quiet) { process.stderr.write(chunk); } });
  child.on('close', (status) => done({ status, log }));
});

const buildRdf = async () => {
  const hash = createHash('sha256');
  for (const file of rdfSources) { hash.update(readFileSync(file)); }
  const stamp = JSON.stringify({ rev: baselineRev, inputs: hash.digest('hex') });
  const stampFile = resolve(rdfBaselineDir, 'stamp.json');
  const steps = [];
  if (!existsSync(stampFile) || readFileSync(stampFile, 'utf8') !== stamp) {
    steps.push(run(['build-rdf.mjs', '--rev', baselineRev, '--label', 'baseline', ...rdfSources]).then((result) => {
      if (result.status === 0) { writeFileSync(stampFile, stamp); }
      return ['RDF baseline ' + baselineRev, result];
    }));
  }
  steps.push(run(['build-rdf.mjs', ...rdfSources]).then((result) => ['RDF current', result]));
  steps.push(run(['build-rdf.mjs', '--label', 'thema', ...themes]).then((result) => ['RDF theme pages', result]));
  const failed = (await Promise.all(steps)).filter(([, result]) => result.status !== 0);
  for (const [label, result] of failed) { console.log(`BUILD FAILED ${label}\n${result.log.slice(-3000)}`); }
  return failed.length === 0;
};

const started = Date.now();
const built = {};
if (!noBuild && dataPresent) {
  const jobs = [];
  if (chosen.includes('pages')) {
    console.log('building the working-tree snapshot into ' + buildDir);
    jobs.push(buildSnapshot({ rev: 'worktree', out: buildDir, quiet: true }).then(() => true, (error) => { console.log('BUILD FAILED pages: ' + error.message); return false; })
      .then((ok) => { built.pages = ok; }));
  }
  if (chosen.includes('rdf')) {
    console.log('building RDF into ' + rdfDir);
    jobs.push(buildRdf().then((ok) => { built.rdf = ok; }));
  }
  await Promise.all(jobs);
  console.log(`builds done in ${Math.round((Date.now() - started) / 1000)} s`);
}

const results = [];
for (const suite of chosen) {
  for (const entry of suites[suite]) {
    const [script, ...args] = Array.isArray(entry) ? entry : [entry];
    const name = suite + ': ' + script;
    if (needsData(suite) && !dataPresent) { results.push([name, 'skipped', 'no data repository at ' + dataRoot]); continue; }
    if (built[suite] === false) { results.push([name, 'failed', 'build failed']); continue; }
    const t = Date.now();
    const { status, log } = await run([script, ...args]);
    const outcome = status === 0 ? 'passed' : status === 2 ? 'skipped' : 'failed';
    results.push([name, outcome, Math.round((Date.now() - t) / 1000) + ' s']);
    console.log(`${outcome.padEnd(7)} ${name}`);
    if (outcome === 'failed') { console.log(log.split('\n').slice(-40).map((line) => '    ' + line).join('\n')); }
    if (/NOT CHECKED/.test(log)) { console.log('    ' + log.split('\n').filter((line) => /NOT CHECKED/.test(line)).join('\n    ')); }
  }
}
const count = (outcome) => results.filter(([, o]) => o === outcome).length;
console.log(`\n${count('passed')} passed, ${count('failed')} failed, ${count('skipped')} skipped (${Math.round((Date.now() - started) / 1000)} s)`);
for (const [name, outcome, note] of results.filter(([, o]) => o !== 'passed')) { console.log(`  ${outcome} ${name}: ${note}`); }
process.exit(count('failed') ? 1 : 0);
