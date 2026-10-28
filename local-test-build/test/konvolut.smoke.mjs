// Smoke test of the konvolut switcher (js/facsimiles-konvolut.js) against the real
// rendered gallery szd-Facsimiles.html in SZD_TEST_BUILD_DIR, or the page in FACSIMILES_HTML.
// Recreated 2026-09-10 from the README description after the local clone was lost.
import { root } from '../harness.mjs';
import { JSDOM } from 'jsdom';
import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';
import { resolve } from 'node:path';
import { buildDir } from './paths.mjs';

const html = readFileSync(process.env.FACSIMILES_HTML || resolve(buildDir, 'szd-Facsimiles.html'), 'utf8');
const js = readFileSync(resolve(root, 'js/facsimiles-konvolut.js'), 'utf8');

// a curated title must win the heading of its bundle
const curated = js.replace('var KONVOLUT_TITLES = {};', "var KONVOLUT_TITLES = { 'SZ-LAS/B7': { de: 'Korrespondenz Sigmund Freud und Stefan Zweig', en: 'Correspondence Sigmund Freud and Stefan Zweig' } };");
if (curated === js) throw new Error('KONVOLUT_TITLES hook not found');

const dom = new JSDOM(html, { runScripts: 'outside-only', url: 'http://localhost:8080/x?locale=de' });
const w = dom.window;
w.eval(curated);
await new Promise(r => setTimeout(r, 50));
const g = w.document.getElementById('facsimiles-gallery');
const personCards = g.querySelectorAll('[data-pid]').length;
const distinct = new Set([...g.querySelectorAll('[data-pid]')].map(c => c.getAttribute('data-pid'))).size;

w.setFacsimilesView('konvolut');
const headings = [...g.querySelectorAll('h2.facsimiles-konvolut-heading')].map(h => h.textContent.trim());
const keys = [...g.querySelectorAll('[data-konvolut]')].map(c => c.getAttribute('data-konvolut'));
const bad = keys.filter(k => !/^[A-Z]+-[A-Z0-9]+\/(B\d+|AK|L)$/.test(k));
if (bad.length) throw new Error('unexpected konvolut keys: ' + [...new Set(bad)].slice(0, 5).join(', '));
if (!keys.some(k => /\/B\d+$/.test(k))) throw new Error('no B-level keys');
const akHeadings = headings.filter(h => /^Konvolut .*\/(AK|L)$/.test(h));
if (akHeadings.length) throw new Error('AK/L labelled as Konvolut: ' + akHeadings.slice(0, 3).join(' | '));
if (!headings.some(h => /^Ansichtskarten /.test(h))) throw new Error('no Ansichtskarten heading');
if (!headings.includes('Korrespondenz Sigmund Freud und Stefan Zweig')) throw new Error('curated title did not win');
const konvolutCards = g.querySelectorAll('[data-pid]').length;
if (konvolutCards !== distinct) throw new Error('pid dedup failed: ' + konvolutCards + ' cards vs ' + distinct + ' distinct pids');

w.setFacsimilesView('person');
if (g.querySelectorAll('[data-pid]').length !== personCards) throw new Error('person view not restored');
console.log('OK  person cards:', personCards, ' konvolut cards:', konvolutCards, ' headings:', headings.length);
console.log('    sample:', headings.slice(0, 6).join(' | '));

// thumbnails: the XSLT must write the IIIF derivative, not the IMG.1 master
const imgs = [...g.querySelectorAll('img.card-img-top')];
const iiif = imgs.filter(i => /^https:\/\/gams\.uni-graz\.at\/iiif\/o:szd\.[^/]+\/IMG\.1\/full\/400,\/0\/default\.jpg$/.test(i.getAttribute('src'))).length;
const srcset = imgs.filter(i => /400w/.test(i.getAttribute('srcset') || '') && /800w/.test(i.getAttribute('srcset') || '')).length;
const lazy = imgs.filter(i => i.getAttribute('loading') === 'lazy').length;
if (iiif !== imgs.length) throw new Error('not all cards on the IIIF derivative: ' + iiif + '/' + imgs.length);
if (srcset !== imgs.length) throw new Error('srcset missing on ' + (imgs.length - srcset) + ' cards');
if (lazy !== imgs.length) throw new Error('loading=lazy missing on ' + (imgs.length - lazy) + ' cards');

// collapsing: in both views a group of more than eight cards shows eight and a button
function collapseState() {
	const rows = [...g.querySelectorAll('.gallery-block .row')];
	const big = rows.filter(r => r.querySelectorAll('[data-pid]').length > 8);
	return {
		big: big.length,
		buttons: g.querySelectorAll('.gallery-block .facsimiles-showall').length,
		visibleInBig: [...new Set(big.map(r => r.querySelectorAll('[data-pid]:not([hidden])').length))],
		hidden: g.querySelectorAll('[data-pid][hidden]').length
	};
}
for (const mode of ['person', 'konvolut', 'person']) {
	w.setFacsimilesView(mode);
	const s = collapseState();
	if (!s.big) throw new Error('no group above the threshold in mode ' + mode);
	if (s.buttons !== s.big) throw new Error(mode + ': ' + s.buttons + ' buttons for ' + s.big + ' large groups');
	if (s.visibleInBig.length !== 1 || s.visibleInBig[0] !== 8) throw new Error(mode + ': large groups show ' + s.visibleInBig);
	console.log('OK  ' + mode + ' -- large groups:', s.big, ' collapse buttons:', s.buttons, ' hidden cards:', s.hidden);
}

// the button reveals its own group and disappears
const firstButton = g.querySelector('.gallery-block .facsimiles-showall');
const buttonLabel = firstButton.textContent;
const ownRow = firstButton.closest('.row');
firstButton.click();
if (ownRow.querySelectorAll('[data-pid][hidden]').length) throw new Error('cards still hidden after the click');
if (ownRow.querySelector('.facsimiles-showall')) throw new Error('button still there after the click');
console.log('OK  button label:', buttonLabel, '-- after the click the group is complete');

const switcher = w.document.querySelector('.facsimiles-modeswitch');
const tabs = [...switcher.querySelectorAll('[role="tab"]')];
assert.equal(switcher.getAttribute('role'), 'tablist');
assert.equal(tabs.length, 2);
assert.equal(g.getAttribute('role'), 'tabpanel');
for (const link of w.document.querySelectorAll('a.language-link')) {
	assert.ok(link.getAttribute('href').includes('/context:szd.facsimiles.korrespondenzen/'), 'language switch stays on this gallery');
}
function selected(mode) {
	const active = tabs.find(tab => tab.dataset.mode === mode);
	assert.equal(switcher.querySelectorAll('[aria-selected="true"]').length, 1);
	assert.equal(active.getAttribute('aria-selected'), 'true');
	assert.equal(active.tabIndex, 0);
	assert.ok(tabs.filter(tab => tab !== active).every(tab => tab.tabIndex === -1));
	assert.equal(g.getAttribute('aria-labelledby'), active.id);
	assert.equal(g.dataset.view, mode);
}
selected('person');
const firstCard = g.querySelector('[data-pid]');
const historyLength = w.history.length;
w.setFacsimilesView('person');
assert.equal(w.history.length, historyLength, 'clicking the active view does not add history');
assert.equal(g.querySelector('[data-pid]'), firstCard);
assert.equal(ownRow.querySelectorAll('[data-pid][hidden]').length, 0);
w.setFacsimilesView('konvolut');
w.setFacsimilesView('person');
assert.equal(g.querySelector('[data-pid]'), firstCard, 'view switching preserves the original nodes');
assert.equal(ownRow.querySelectorAll('[data-pid][hidden]').length, 0, 'expanded group stays expanded');

for (const [key, mode] of [['ArrowRight','konvolut'], ['ArrowRight','person'], ['End','konvolut'], ['Home','person'], ['ArrowLeft','konvolut']]) {
	const current = tabs.find(tab => tab.getAttribute('aria-selected') === 'true');
	current.dispatchEvent(new w.KeyboardEvent('keydown', { key, bubbles: true }));
	selected(mode);
	assert.equal(w.document.activeElement.dataset.mode, mode);
}
w.setFacsimilesView('person');
w.history.replaceState(null, '', 'http://localhost:8080/x?locale=de&extra=keep#A');
w.setFacsimilesView('konvolut');
assert.equal(new URL(w.location.href).searchParams.get('mode'), 'konvolut');
assert.equal(new URL(w.location.href).searchParams.get('extra'), 'keep');
assert.equal(w.location.hash, '#A');
const personNav = w.document.querySelector('.header-card-nav .header-jump') || w.document.querySelector('.header-card-nav ul.list-inline');
assert.equal(personNav.style.display, 'none');
async function travel(method) {
	await new Promise((resolve, reject) => {
		const timeout = setTimeout(() => reject(new Error('history traversal timed out')), 2000);
		w.addEventListener('popstate', () => { clearTimeout(timeout); resolve(); }, { once: true });
		w.history[method]();
	});
}
await travel('back');
selected('person');
assert.equal(personNav.style.display, '');
await travel('forward');
selected('konvolut');
const beforeInvalid = w.history.length;
w.setFacsimilesView('unknown');
selected('konvolut');
assert.equal(w.history.length, beforeInvalid);
w.eval(curated);
selected('konvolut');

const direct = new JSDOM(html, { runScripts: 'outside-only', url: 'https://gams-staging.uni-graz.at/context:szd.facsimiles.korrespondenzen/sdef:Context/get?locale=en&mode=konvolut' });
direct.window.eval(js);
await new Promise(resolve => setTimeout(resolve, 0));
assert.equal(direct.window.document.getElementById('facsimiles-gallery').dataset.view, 'konvolut');
assert.equal(direct.window.history.length, 1, 'initial mode does not add history');
assert.ok([...direct.window.document.querySelectorAll('.facsimiles-konvolut-heading')].some(node => /^Bundle /.test(node.textContent)));
direct.window.close();
dom.window.close();
console.log('OK  tabs, keyboard, direct URL, history, preserved expansion and duplicate initialization');
