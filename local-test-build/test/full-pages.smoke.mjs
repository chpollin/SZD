import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { root } from '../harness.mjs';
import assert from 'node:assert/strict';
import { JSDOM } from 'jsdom';

import { buildDir as build } from './paths.mjs';
const pages = process.argv.slice(2);
if (!pages.length) throw new Error('Supply full-page HTML fixture filenames');
for (const file of pages) {
  const dom = new JSDOM(readFileSync(resolve(build, file), 'utf8'));
  const document = dom.window.document;
  assert.equal(document.documentElement.lang, file.includes('.en.') ? 'en' : 'de');
  const metadata = [...document.querySelectorAll('.szd-metadata')];
  assert.ok(metadata.length, file + ': no metadata rendered');
  for (const list of metadata) {
    assert.equal(list.tagName, 'DL');
    for (const row of list.children) {
      assert.equal(row.tagName, 'DIV');
      assert.deepEqual([...row.children].map(node => node.tagName), ['DT', 'DD'], file + ': malformed metadata pair');
      assert.ok(row.firstElementChild.textContent.trim(), file + ': empty label');
      assert.ok(!row.querySelector('.text-truncate'), file + ': truncated metadata');
    }
  }
  assert.equal(document.querySelectorAll('[id=""]').length, 0, file + ': empty IDs');
  for (const control of document.querySelectorAll('button[data-target]')) {
    assert.ok(document.getElementById(control.getAttribute('data-target').slice(1)), file + ': missing disclosure target');
    assert.ok(control.getAttribute('aria-label') || control.getAttribute('title') || control.textContent.trim(), file + ': unnamed button');
  }
  for (const link of document.querySelectorAll('a.language-link')) {
    assert.ok(link.href.includes('locale='));
    assert.equal(link.getAttribute('onclick'), null);
  }
  for (const asset of document.querySelectorAll('script[src],link[rel="stylesheet"]')) {
    const path = asset.getAttribute('src') || asset.getAttribute('href');
    if (path.startsWith('/szd/')) assert.ok(existsSync(resolve(root, path.slice(5).split('?')[0])), 'Missing local asset ' + path);
  }
  assert.equal(document.querySelectorAll('script[src$="FileSaver.js"],script[src$="jszip.js"]').length, 0, file + ': eager ZIP dependency');
  assert.ok(document.querySelector('script[data-asset-base="/szd"]'));
  assert.ok(document.querySelector('link[media="print"]'));
  console.log(`PASS ${file}: ${metadata.length} semantic metadata lists, assets and controls`);
  dom.window.close();
}
