// Smoke test of the prototype view against the real rendered build/szd-Facsimiles.html.
import { root } from '../harness.mjs';
import { resolve } from 'node:path';
import { JSDOM } from 'jsdom';
import { readFileSync, existsSync } from 'node:fs';

// the preview page is built by hand with run.sh (proto/README.md); without it the test counts as skipped
if (!existsSync(new URL('../build/szd-Facsimiles.html', import.meta.url))) { console.log('SKIP build/szd-Facsimiles.html is not built, see proto/README.md'); process.exit(2); }
const html = readFileSync(new URL('../build/szd-Facsimiles.html', import.meta.url), 'utf8');
const map = JSON.parse(readFileSync(new URL('./konvolut-map.json', import.meta.url), 'utf8'));
const prod = readFileSync(resolve(root, 'js/facsimiles-konvolut.js'), 'utf8');
const proto = readFileSync(new URL('./facsimiles-konvolut-proto.js', import.meta.url), 'utf8');

// runScripts outside-only keeps the page's own script tags inert; we load the scripts ourselves and stub fetch
const dom = new JSDOM(html, { runScripts: 'outside-only', url: 'http://localhost:8080/x?locale=de' });
const w = dom.window;
w.fetch = () => Promise.resolve({ json: () => Promise.resolve(map) });
w.eval(prod);
w.eval(proto);
await new Promise(r => setTimeout(r, 50));

const btn = w.document.querySelector('[data-mode="erschliessung"]');
if (!btn) throw new Error('third button missing');
w.setFacsimilesView('erschliessung');
const g = w.document.getElementById('facsimiles-gallery');
const heads = [...g.querySelectorAll('h2.facsimiles-konvolut-heading')];
const curated = heads.filter(h => h.querySelector('a'));
const cards = g.querySelectorAll('[data-pid]').length;
const distinct = new Set([...g.querySelectorAll('[data-pid]')].map(c => c.getAttribute('data-pid'))).size;
console.log('OK  konvolut headings:', curated.length, ' unmapped persons:', heads.length - curated.length, ' cards:', cards, ' distinct pids:', distinct);
console.log('    first titles:', curated.slice(0, 4).map(h => h.firstChild.textContent.trim()).join(' | '));
const freud = heads.find(h => /Freud, Sigmund|Sigmund Freud/.test(h.textContent));
console.log('    Freud:', freud ? freud.textContent.trim() + ' -- ' + freud.parentNode.querySelector('p').textContent : 'MISSING');
w.setFacsimilesView('person');
console.log('    back to person, headings:', g.querySelectorAll('h2').length);
w.setFacsimilesView('konvolut');
console.log('    production konvolut mode, headings:', g.querySelectorAll('h2').length);

// thumbnails and collapsing
w.setFacsimilesView('erschliessung');
const imgs = [...g.querySelectorAll('img.card-img-top')];
const iiif = imgs.filter(i => /gams\.uni-graz\.at\/iiif\/o:szd\.[^/]+\/IMG\.\d+\/full\/400,\/0\/default\.jpg$/.test(i.src)).length;
const hiddenCards = g.querySelectorAll('[data-pid][hidden]').length;
const buttons = [...g.querySelectorAll('.gallery-block .facsimiles-showall')];
const rowsOver8 = [...g.querySelectorAll('.gallery-block .row')].filter(r => r.querySelectorAll('[data-pid]').length > 8).length;
if (iiif !== imgs.length) throw new Error('not all images rewritten: ' + iiif + '/' + imgs.length);
if (buttons.length !== rowsOver8) throw new Error('collapse buttons ' + buttons.length + ' vs rows>8 ' + rowsOver8);
const visibleInBig = [...g.querySelectorAll('.gallery-block .row')].filter(r => r.querySelectorAll('[data-pid]').length > 8).map(r => r.querySelectorAll('[data-pid]:not([hidden])').length);
if (visibleInBig.some(n => n !== 8)) throw new Error('big rows show ' + visibleInBig);
buttons[0].click();
const afterClick = buttons[0].closest('.row') ? 'button still attached' : 'button removed';
console.log('OK  iiif thumbs:', iiif, ' collapsed rows:', buttons.length, ' hidden cards:', hiddenCards, ' after click:', afterClick, ' first button text:', buttons[0].textContent);
w.setFacsimilesView('person');
console.log('    person view iiif thumbs:', [...g.querySelectorAll('img.card-img-top')].filter(i => i.src.indexOf('/iiif/') > 0).length, ' collapse buttons:', g.querySelectorAll('.gallery-block .facsimiles-showall').length);
