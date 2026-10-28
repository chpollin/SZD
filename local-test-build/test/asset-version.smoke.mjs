import { root } from '../harness.mjs';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { JSDOM, VirtualConsole } from 'jsdom';
import { buildDir } from './paths.mjs';

const read = (path) => readFileSync(resolve(root, path), 'utf8');
const shell = read('szd-static.xsl');
const version = shell.match(/name="asset-version" select="'([^']+)'"/)[1];
const pages = readdirSync(buildDir).filter((name) => name.endsWith('.html'));
assert.ok(pages.length, 'render the working-tree snapshot first');
let timelineHtml;
for (const name of pages) {
  const html = readFileSync(join(buildDir, name), 'utf8');
  const dom = new JSDOM(html, { url: 'https://www.stefanzweig.digital/' });
  const d = dom.window.document;
  const assets = [...d.querySelectorAll('link[rel="stylesheet"][href], script[src]')]
    .map((element) => new URL(element.src || element.href))
    .filter((url) => /\/(css|js)\//.test(url.pathname) && !url.pathname.startsWith('/lib/') && !url.pathname.startsWith('/editionviewer/'));
  assert.ok(assets.length, name + ': project assets exist');
  for (const url of assets) {
    assert.equal(url.searchParams.get('v'), version, name + ': ' + url.pathname);
    assert.equal(url.searchParams.getAll('v').length, 1);
  }
  const styles = [...d.querySelectorAll('link[rel="stylesheet"]')].map((link) => new URL(link.href).pathname);
  assert.equal(styles.filter((path) => path.endsWith('/tokens.css')).length, 1, name + ': load tokens once');
  assert.ok(styles.findIndex((path) => path.endsWith('/tokens.css')) > styles.findIndex((path) => path.endsWith('/szd.css')), name + ': layer order is established first');
  assert.equal(d.querySelector('script[src*="download_images_iiif_manifest.js"]').dataset.assetVersion, version);
  if (d.getElementById('zl-app')) {
    assert.equal(d.getElementById('zl-app').dataset.assetVersion, version);
    timelineHtml = html;
  }
  dom.window.close();
}
assert.match(read('css/szd.css'), /@import[^;]*tokens\.css/, 'cached HTML keeps its tokens fallback; the later versioned link overrides it');
assert.match(read('css/szd.css'), /@import[^;]*bootstrap[^;]*layer\(legacy\)/, 'keep Bootstrap in its existing layer');
if (timelineHtml) {
  const dom = new JSDOM(timelineHtml, { url: 'https://www.stefanzweig.digital/o:szd.lebenskalender/sdef:TEI/get?locale=de&mode=timeline', runScripts: 'outside-only', virtualConsole: new VirtualConsole() });
  const requests = [];
  dom.window.fetch = async (url) => { requests.push(new URL(url)); return { ok: false, status: 503 }; };
  dom.window.eval(read('js/lebenskalender-timeline.js'));
  await new Promise((resolve) => setTimeout(resolve, 0));
  assert.ok(requests.length, 'timeline actually requests lane data');
  for (const url of requests) assert.equal(url.searchParams.get('v'), version, 'lazy JSON uses the same release');
  dom.window.close();
} else {
  assert.match(shell, /name="timelineView" select="false\(\)"/, 'missing timeline is allowed only while explicitly disabled');
}
console.log('OK release versions on rendered CSS/JS and tokens; timeline requests checked when enabled');
