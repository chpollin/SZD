import { root } from '../harness.mjs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { JSDOM } from 'jsdom';

const source = readFileSync(resolve(root, 'js/download_images_iiif_manifest.js'), 'utf8');
const pause = () => new Promise((resolve) => setTimeout(resolve, 2));
const pid = 'o:szd.6814';

function manifest(count = 7) {
  return {
    sequences: [{ canvases: Array.from({ length: count }, (_, index) => ({
      '@id': 'https://gams.uni-graz.at/o:szd.6814/canvas/DIV.unrelated-' + index,
      images: [{ resource: { '@id': 'https://gams.uni-graz.at/iiif/source-' + index + '/full/full/0/default.jpg' } }]
    })) }]
  };
}

function setup(options = {}) {
  const dom = new JSDOM('<html lang="de"><head><script data-asset-base="https://gams-staging.uni-graz.at/gamsdev/pollin/szd/gams-www" src="https://gams-staging.uni-graz.at/gamsdev/pollin/szd/gams-www/js/download_images_iiif_manifest.js"></script></head><body><main></main><div id="loading" style="display:none"></div></body></html>', {
    url: (options.origin || 'https://stefanzweig.digital') + '/object?locale=' + (options.locale || 'de'), runScripts: 'outside-only'
  });
  const window = dom.window;
  const state = { scripts: [], fetches: [], saves: [], archives: [], generated: 0, active: 0, peak: 0, failedLibrary: false };
  class MockZip {
    constructor() { this.files = []; state.archives.push(this); }
    file(name, blob) { this.files.push({ name, blob }); }
    async generateAsync() {
      state.generated += 1;
      if (options.zipFailure) throw new Error('zip failed');
      return new window.Blob(['zip'], { type: 'application/zip' });
    }
  }
  const saveAs = (blob, name) => { state.saves.push({ blob, name }); };
  if (options.preloaded) { window.JSZip = MockZip; window.saveAs = saveAs; }
  const append = window.document.head.appendChild.bind(window.document.head);
  window.document.head.appendChild = function (element) {
    append(element);
    state.scripts.push(element.src);
    queueMicrotask(() => {
      if (options.libraryFailure && !state.failedLibrary && new URL(element.src).pathname.endsWith('jszip.js')) {
        state.failedLibrary = true;
        element.onerror();
        return;
      }
      if (new URL(element.src).pathname.endsWith('jszip.js')) window.JSZip = MockZip;
      if (new URL(element.src).pathname.endsWith('FileSaver.js')) window.saveAs = saveAs;
      element.onload();
    });
    return element;
  };
  window.fetch = async (url) => {
    state.fetches.push(url);
    if (url.includes('/methods/sdef:IIIF/getManifest')) {
      if (options.manifestHttpFailure) return { ok: false, status: 503 };
      return { ok: true, json: async () => {
        if (options.invalidJson) throw new SyntaxError('invalid JSON');
        return options.manifest || manifest();
      } };
    }
    if (options.enforceCors && new URL(url, window.location.href).origin === 'https://gams.uni-graz.at') throw new TypeError('Failed to fetch: missing CORS header');
    state.active += 1;
    state.peak = Math.max(state.peak, state.active);
    await pause();
    state.active -= 1;
    if (options.imageFailure && url.includes('source-1')) return { ok: false, status: 404 };
    return { ok: true, blob: async () => new window.Blob(['image'], { type: options.imageMime || 'image/jpeg' }) };
  };
  if (options.assetVersion) window.document.querySelector('script').setAttribute('data-asset-version', options.assetVersion);
  window.eval(source);
  return { dom, window, state };
}

function finished(window, success) {
  assert.equal(window.document.querySelector('#loading').style.display, 'none');
  const status = window.document.querySelector('#iiif-download-status');
  assert.ok(status && status.textContent);
  assert.equal(status.getAttribute('role'), success ? 'status' : 'alert');
}

{
  const { dom, window, state } = setup();
  assert.equal(state.scripts.length, 0, 'libraries must stay lazy');
  assert.equal(await window.download_images_iiif_manifest(pid), true);
  finished(window, true);
  assert.deepEqual(state.scripts.sort(), [
    'https://gams-staging.uni-graz.at/gamsdev/pollin/szd/gams-www/js/FileSaver.js',
    'https://gams-staging.uni-graz.at/gamsdev/pollin/szd/gams-www/js/jszip.js'
  ]);
  assert.equal(state.peak, 4, 'image requests must be bounded');
  assert.equal(state.saves.length, 1);
  assert.equal(state.generated, 1);
  assert.equal(state.saves[0].name, 'szd_6814_images.zip');
  assert.equal(state.archives[0].files.length, 7);
  assert.equal(new Set(state.archives[0].files.map((file) => file.name)).size, 7);
  assert.deepEqual(state.fetches.slice(1).sort(), manifest().sequences[0].canvases.map((canvas) => canvas.images[0].resource['@id']).sort());
  assert.equal(await window.download_images_iiif_manifest(pid), true);
  assert.equal(state.scripts.length, 2, 'loaded dependencies must be reused');
  dom.window.close();
}

{
  const { dom, window, state } = setup({ preloaded: true });
  assert.equal(await window.download_images_iiif_manifest(pid), true);
  assert.equal(state.scripts.length, 0, 'existing globals must be reused');
  dom.window.close();
}

{
  const { dom, window, state } = setup();
  const results = await Promise.all([window.download_images_iiif_manifest(pid), window.download_images_iiif_manifest('context:szd.example')]);
  assert.ok(results.every(Boolean));
  assert.equal(state.scripts.length, 2, 'concurrent calls share one dependency load');
  assert.equal(state.saves.length, 2);
  finished(window, true);
  dom.window.close();
}

{
  const { dom, window, state } = setup({ libraryFailure: true, locale: 'en' });
  assert.equal(await window.download_images_iiif_manifest(pid), false);
  finished(window, false);
  assert.match(window.document.querySelector('#iiif-download-status').textContent, /libraries could not be loaded/);
  assert.equal(state.saves.length, 0);
  assert.equal(await window.download_images_iiif_manifest(pid), true, 'failed dependency load must be retryable');
  assert.equal(state.scripts.filter((url) => url.endsWith('jszip.js')).length, 2);
  assert.equal(state.scripts.filter((url) => url.endsWith('FileSaver.js')).length, 1);
  dom.window.close();
}

for (const invalidPID of ['o:', 'o:valid/path', 'o:valid?x=1', 'junkcontext:szd.test', 'o:valid\n', '<o:szd.1>', null]) {
  const { dom, window, state } = setup();
  assert.equal(await window.download_images_iiif_manifest(invalidPID), false, String(invalidPID));
  assert.equal(state.fetches.length, 0);
  assert.equal(state.scripts.length, 0);
  finished(window, false);
  assert.match(window.document.querySelector('#iiif-download-status').textContent, /Objektkennung/);
  dom.window.close();
}

for (const options of [
  { manifestHttpFailure: true },
  { invalidJson: true },
  { manifest: {} },
  { manifest: { sequences: [{ canvases: [] }] } },
  { manifest: { sequences: [{ canvases: [{ '@id': 'https://example.org/canvas/DIV.1' }] }] } },
  { manifest: { sequences: [{ canvases: [{ images: [{ resource: { '@id': 'javascript:bad()' } }] }] }] } },
  { imageFailure: true },
  { imageMime: 'text/html' },
  { zipFailure: true }
]) {
  const { dom, window, state } = setup(options);
  assert.equal(await window.download_images_iiif_manifest(pid), false, JSON.stringify(options));
  assert.equal(state.saves.length, 0, 'failed download must never save a partial ZIP');
  assert.equal(state.generated, options.zipFailure ? 1 : 0);
  assert.equal(state.active, 0, 'all active image workers must settle before completion');
  assert.ok(state.peak <= 4);
  finished(window, false);
  dom.window.close();
}

// GAMS serves some manifests as invalid JSON (unescaped quotes in structure labels):
// the user gets a specific message naming the object, in the page language
for (const [locale, expected] of [['de', /Bildverzeichnis \(IIIF-Manifest\) von o:szd\.2409 ist fehlerhaft/], ['en', /manifest \(IIIF manifest\) of o:szd\.2409 is defective/]]) {
  const { dom, window, state } = setup({ invalidJson: true, locale });
  assert.equal(await window.download_images_iiif_manifest('o:szd.2409'), false);
  finished(window, false);
  assert.match(window.document.querySelector('#iiif-download-status').textContent, expected);
  assert.equal(state.saves.length, 0);
  assert.equal(state.scripts.length, 0, 'no libraries load for a defective manifest');
  dom.window.close();
}

{
  // an HTTP failure keeps the generic manifest message
  const { dom, window } = setup({ manifestHttpFailure: true, locale: 'en' });
  assert.equal(await window.download_images_iiif_manifest(pid), false);
  assert.match(window.document.querySelector('#iiif-download-status').textContent, /^The image manifest could not be read/);
  dom.window.close();
}

{
  const { dom, window, state } = setup({ preloaded: true, imageMime: 'image/png' });
  const canvases = manifest(1).sequences[0].canvases;
  canvases[0].images.push({ resource: { '@id': 'https://gams.uni-graz.at/actual-second.png' } });
  await window.build_zip_download(canvases, pid);
  assert.equal(state.archives[0].files.length, 2, 'every image resource must be included');
  assert.ok(state.archives[0].files.every((file) => file.name.endsWith('.png')));
  assert.equal(typeof window.downloadImage, 'function');
  dom.window.close();
}

console.log('OK IIIF ZIP download: lazy dependencies, retries, exact resource URLs, bounded workers, complete archives and bilingual errors');

// Production manifest of o:szd.260, read on 2026-10-15: the raw datastream
// lacks CORS, while the SZD alias serves the identical image without redirect.
const imageURL = 'https://gams.uni-graz.at/o:szd.260/IMG.1';
const realManifest = { sequences: [{ canvases: [{ images: [{ resource: {
  '@id': imageURL, format: 'image/jpeg',
  service: { '@id': 'https://gams.uni-graz.at/iiif/o:szd.260%2FIMG.1' }
} }] }] }] };
for (const origin of ['https://stefanzweig.digital', 'https://www.stefanzweig.digital']) {
  const { dom, window, state } = setup({ origin, manifest: realManifest, enforceCors: true, assetVersion: '20261015' });
  assert.equal(await window.download_images_iiif_manifest('o:szd.260'), true);
  assert.equal(state.fetches[1], origin + '/o:szd.260/IMG.1');
  assert.equal(state.saves.length, 1);
  assert.ok(state.scripts.every((url) => new URL(url).searchParams.get('v') === '20261015'));
  dom.window.close();
}
for (const origin of ['https://gams-staging.uni-graz.at', 'https://gams.uni-graz.at', 'http://127.0.0.1:8769']) {
  const { dom, window, state } = setup({ origin, manifest: realManifest });
  await window.download_images_iiif_manifest('o:szd.260');
  assert.equal(state.fetches[1], imageURL, 'other environments keep the manifest origin');
  dom.window.close();
}
for (const url of ['https://example.org/o:szd.260/IMG.1', 'https://gams-staging.uni-graz.at/o:szd.260/IMG.1',
  'https://gams.uni-graz.at/iiif/o:szd.260%2FIMG.1/full/full/0/default.jpg',
  'https://gams.uni-graz.at/o:other.260/IMG.1', 'https://gams.uni-graz.at.evil.example/o:szd.260/IMG.1']) {
  const { dom, window, state } = setup();
  await window.build_zip_download([{ images: [{ resource: { '@id': url } }] }], 'o:szd.260');
  assert.equal(state.fetches[0], url, 'unrelated URLs must not be rewritten');
  dom.window.close();
}
console.log('OK production CORS regression, host boundaries and versioned lazy libraries');