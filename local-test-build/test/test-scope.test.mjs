import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { suitesForPaths } from './scope.mjs';

const frontend = ['unit', 'proto', 'pages'];
const all = [...frontend, 'rdf'];
for (const path of ['css/szd.css', 'js/download_images_iiif_manifest.js', 'szd-static.xsl', 'szd-context.xsl',
  'fonts/SourceSansPro-Light.woff2', 'data/lebenskalender/biography.json']) {
  assert.deepEqual(suitesForPaths([path]), frontend, path);
}
assert.deepEqual(suitesForPaths(['szd-TORDF.xsl']), ['rdf']);
assert.deepEqual(suitesForPaths(['README.md', 'LICENSE']), []);
assert.deepEqual(suitesForPaths(['szd-static.xsl', 'szd-TORDF.xsl']), all);
assert.deepEqual(suitesForPaths(['unexpected-source-file']), all);
assert.deepEqual(suitesForPaths([]), []);
const scripts = JSON.parse(readFileSync(new URL('../package.json', import.meta.url))).scripts;
assert.equal(scripts['test:frontend'], 'node test/run-all.mjs --suite unit,proto,pages');
assert.equal(scripts['test:data'], 'node test/run-all.mjs --suite rdf');
assert.equal(scripts.test, 'node test/run-all.mjs');
const runner = fileURLToPath(new URL('./run-all.mjs', import.meta.url));
for (const selection of [[], [''], ['frnotend'], ['unit,unknown'], ['unit,']]) {
  const result = spawnSync(process.execPath, [runner, '--no-build', '--suite', ...selection], { encoding: 'utf8' });
  assert.equal(result.status, 1, 'reject --suite ' + JSON.stringify(selection));
  assert.match(result.stderr, /Invalid --suite/, result.stderr);
  assert.equal(result.stdout, '', 'invalid selection must not start builds or tests');
}
console.log('OK test scope: frontend excludes RDF; data excludes pages; shared code runs both');
