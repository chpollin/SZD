// Integration checks use the rendered GAMS page and the deployed lane snapshots.
import { root } from '../harness.mjs';
import { JSDOM } from 'jsdom';
import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';
import { join, resolve } from 'node:path';
import { buildDir as build } from './paths.mjs';

const read = (path) => readFileSync(resolve(root, path), 'utf8');
// the timeline is unpublished while szd-static.xsl sets timelineView to false(); exit 2 counts as skipped
if (/name="timelineView" select="false\(\)"/.test(read('szd-static.xsl'))) {
  console.log('skipped: timeline view disabled in szd-static.xsl');
  process.exit(2);
}
const js = read('js/lebenskalender-timeline.js');
const html = readFileSync(process.env.TIMELINE_HTML || join(build, 'szd-Lebenskalender.timeline.html'), 'utf8');
const lanes = ['biography', 'correspondence', 'personal-documents', 'autographs'];
const data = Object.fromEntries(lanes.map((lane) => [lane, JSON.parse(read('data/lebenskalender/' + lane + '.json'))]));
const index = JSON.parse(read('data/lebenskalender/index.json'));
const all = Object.values(data).flat();
const withheld = all.filter((e) => e.date && +e.date.slice(0, 4) > 1950);
const visible = all.filter((e) => !withheld.includes(e));
const page = 'https://gams-staging.uni-graz.at/o:szd.lebenskalender/sdef:TEI/get';
const tick = () => new Promise((resolve) => setTimeout(resolve, 0));
const filters = href => new URLSearchParams(new URL(href).hash.split('?')[1] || '');

async function load(query = '?locale=de&mode=timeline', options = {}) {
	const dom = new JSDOM(html, { runScripts: 'outside-only', url: page + query });
	const w = dom.window;
	const d = w.document;
	const errors = [];
	const requests = [];
	w.console.warn = () => {};
	w.console.error = (...args) => errors.push(args);
	w.IntersectionObserver = class { observe() {} disconnect() {} };
	w.HTMLElement.prototype.scrollIntoView = function () { w.lastScroll = this.id; };
	w.fetch = async (url) => {
		requests.push(String(url));
		if (options.fail) return { ok: false, status: 503 };
		const lane = new URL(url).pathname.split('/').at(-1).replace('.json', '');
		return { ok: true, json: async () => structuredClone(data[lane]) };
	};
	w.eval(js);
	await tick();
	await tick();
	return { w, d, requests, errors, close: () => w.close() };
}

const { w, d, requests, errors, close } = await load('?locale=de&mode=timeline&extra=keep#SZDBIO.1');
const rows = () => [...d.querySelectorAll('.zl-ev')];
const laneChip = (lane) => d.querySelector('#zl-lane-chips .zl-lane-' + lane);
const reset = (query = '?locale=de&mode=timeline&extra=keep') => {
	w.history.replaceState(null, '', page + query);
	w.dispatchEvent(new w.PopStateEvent('popstate'));
};
assert.equal(index.lanes.reduce((sum, lane) => sum + lane.events, 0), all.length);
assert.equal(errors.length, 0);
assert.equal(requests.length, 4);
assert.ok(requests.every((url) => url.startsWith(new URL(d.getElementById('zl-app').dataset.laneBase, page).href)));
assert.ok(requests.every((url) => !url.includes('github')));
assert.equal(rows().length, visible.length, 'all entries remain in DOM even with IntersectionObserver');
assert.equal(w.lastScroll, 'SZDBIO.1', 'initial event fragment is available');
assert.deepEqual([...new URL(w.location.href).searchParams.keys()].sort(), ['locale', 'mode'], 'GAMS receives only declared service parameters');
assert.equal(d.getElementById('zl-app').getAttribute('aria-busy'), 'false');
assert.match(d.getElementById('zl-status').textContent, new RegExp(String(visible.length)));
assert.match(d.getElementById('zl-notice').textContent, new RegExp(String(withheld.length)));
withheld.forEach((event) => assert.equal(d.getElementById(event.id), null));
assert.equal(d.querySelector('#zl-axis a:last-child').dataset.year, '1950');
assert.equal(d.querySelectorAll('#zl-plot .zl-lane-row').length, 4);
const undated = visible.filter((e) => !e.date).length;
assert.equal(d.querySelectorAll('.zl-undated .zl-ev').length, undated);
assert.ok(rows().slice(-undated).every((row) => row.closest('.zl-undated')));
const scaleCount = [...d.querySelectorAll('#zl-axis a')].reduce((sum, a) => sum + (a.getAttribute('aria-label').match(/\d+/g) || []).slice(1).reduce((n, c) => n + +c, 0), 0);
assert.equal(scaleCount, visible.length - undated);
const ids = [...d.querySelectorAll('#zl-app [id]')].map((el) => el.id);
assert.equal(new Set(ids).size, ids.length);

const merged = visible.filter((event) => event.sources?.length > 1);
assert.ok(merged.length > 0, 'real merged facsimile records are covered');
for (const event of merged) {
	const detail = d.getElementById(event.id).querySelector('.zl-sources');
	assert.equal(detail.querySelector('summary').textContent, event.sources.length + ' Quelleneinträge');
	assert.equal(detail.querySelectorAll('li').length, event.sources.length);
	for (const source of event.sources) {
		const item = [...detail.querySelectorAll('li')].find((li) => li.dataset.sourceId === source.id);
		assert.ok(item.textContent.includes(source.title.de), 'original source title remains available');
		assert.ok([...item.querySelectorAll('a')].some((a) => new URL(a.href).hash === new URL(source.href, page).hash), 'every original source permalink remains reachable');
	}
}
const alias = merged[0].sources.find((source) => source.id !== merged[0].id).id;
w.history.replaceState(null, '', page + '?locale=de&mode=timeline&extra=keep#' + alias);
w.dispatchEvent(new w.HashChangeEvent('hashchange'));
assert.ok(d.getElementById(alias).closest('details').open, 'source fragment reveals the original record');
assert.equal(w.lastScroll, alias);

const letter = visible.find((e) => e.lane === 'correspondence' && e.facsimile);
const letterRow = d.getElementById(letter.id);
assert.ok(letterRow.querySelector('.fa-envelope'));
assert.match(letterRow.querySelector('.zl-lane-label').textContent, /Briefe/);
for (const a of d.querySelectorAll('.zl-meta a, .zl-text a')) {
	assert.equal(new URL(a.href).origin, new URL(page).origin, 'detail and search links keep staging host');
	assert.equal(new URL(a.href).searchParams.get('locale'), 'de');
}
// an index bundle is titled by its extent only; the correspondents, the repository and the
// Konvolut with the single pieces must be reachable from the row
const bundle = d.getElementById('SZDKOR.45');
assert.deepEqual([...bundle.querySelectorAll('.zl-text a')].map((a) => a.textContent), ['Bojer, Johan', 'Zweig, Stefan']);
assert.match(bundle.querySelector('.zl-text').textContent, /^Bojer, Johan → Zweig, Stefan\. 55 Korrespondenzstücke/);
for (const event of visible.filter((e) => e.konvolut)) {
	assert.ok([...d.getElementById(event.id).querySelectorAll('.zl-meta a')].some((a) => new URL(a.href).pathname === event.konvolut), event.id + ' links its Konvolut');
}
for (const event of visible.filter((e) => e.repository)) {
	assert.ok(d.getElementById(event.id).querySelector('.zl-meta').textContent.includes(event.repository.name), event.id + ' names its repository');
}
const yearOnly = visible.find((e) => e.datePrecision === 'year' && visible.some((other) => other.date && other.date.slice(0, 4) === e.date.slice(0, 4) && ['day', 'month'].includes(other.datePrecision)));
assert.match(d.getElementById(yearOnly.id).querySelector('.zl-mark').textContent, /nur Jahr/);
const yearGroup = d.getElementById(yearOnly.id).closest('.zl-group');
const yearEvents = [...yearGroup.querySelectorAll('.zl-ev')].map((row) => visible.find((e) => e.id === row.id));
assert.ok(yearEvents.findIndex((e) => ['day', 'month'].includes(e.datePrecision)) > yearEvents.findIndex((e) => e.datePrecision === 'year'));

laneChip('autographs').focus();
laneChip('autographs').click();
assert.equal(rows().length, visible.length - data.autographs.length);
assert.equal(d.querySelectorAll('#zl-plot .zl-lane-row').length, 3);
assert.equal(d.activeElement, laneChip('autographs'), 'focus survives regenerated lane chips');
assert.equal(filters(w.location.href).get('extra'), 'keep');
assert.equal(new URL(w.location.href).searchParams.get('mode'), 'timeline');
assert.ok([...d.querySelectorAll('#zl-axis a')].every(a => filters(a.href).get('lanes') === filters(w.location.href).get('lanes')), 'year links retain the current filters');
laneChip('autographs').click();
for (const lane of lanes) laneChip(lane).click();
assert.equal(rows().length, 0);
assert.equal(filters(w.location.href).get('lanes'), '');
w.dispatchEvent(new w.PopStateEvent('popstate'));
assert.equal(rows().length, 0, 'all lanes off survives URL restoration');
reset();

const place = d.getElementById('zl-place-button');
place.click();
const search = d.getElementById('zl-place-search');
assert.equal(d.activeElement, search);
search.value = 'Ber';
search.dispatchEvent(new w.Event('input'));
assert.ok([...d.querySelectorAll('#zl-place-list button')].slice(1).every((button) => /ber/i.test(button.textContent)));
search.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
assert.ok(d.getElementById('zl-place-popup').hidden);
assert.equal(d.activeElement, place);
place.click();
assert.ok([...d.querySelectorAll('#zl-place-list button')].some((button) => /^Wien/.test(button.textContent)));
const berlin = [...d.querySelectorAll('#zl-place-list button')].find((button) => /^Berlin/.test(button.textContent));
berlin.click();
assert.equal(rows().length, visible.filter((e) => e.place === 'Berlin').length);
assert.equal(d.activeElement, place);
d.querySelector('#zl-active button').click();
assert.equal(rows().length, visible.length);
place.click();
d.getElementById('zl-person').focus();
assert.ok(d.getElementById('zl-place-popup').hidden, 'Tab out closes the popup');

const person = d.getElementById('zl-person');
person.value = 'Zweig';
person.dispatchEvent(new w.Event('input'));
assert.ok(rows().length > 0 && rows().length < visible.length);
d.querySelector('#zl-active button').click();
d.getElementById('zl-from').value = '1935';
d.getElementById('zl-to').value = '1930';
d.getElementById('zl-range').dispatchEvent(new w.Event('submit', { bubbles: true, cancelable: true }));
assert.ok(rows().length > 0);
assert.ok(rows().every((row) => {
	const e = visible.find((event) => event.id === row.id);
	return e.date && +e.date.slice(0, 4) >= 1930 && +e.date.slice(0, 4) <= 1935;
}));
assert.equal(filters(w.location.href).get('from'), '1930');
const rangeUrl = new URL(w.location.href);
const rangeCount = rows().length;
reset();
reset(rangeUrl.search + rangeUrl.hash);
assert.equal(rows().length, rangeCount, 'shared fragment restores the period after navigation');
d.querySelector('#zl-active button').click();
assert.equal(rows().length, visible.length);
reset('?locale=de&mode=timeline&from=not-a-year&to=9000');
assert.equal(rows().length, visible.length);

const axis = d.querySelector('#zl-axis a[data-year="1933"]');
axis.focus();
assert.equal(d.getElementById('zl-tip').hidden, false);
axis.click();
assert.equal(w.lastScroll, 'y1933');
assert.equal(d.activeElement.id, 'y1933');
w.setLebenskalenderDensity('compact');
assert.ok(d.body.classList.contains('zl-compact'));
assert.equal(filters(w.location.href).get('density'), 'compact');
assert.equal(d.querySelector('[data-density="compact"]').getAttribute('aria-pressed'), 'true');
w.setLebenskalenderDensity('full');
const toggle = d.getElementById('zl-filter-toggle');
toggle.click();
assert.equal(toggle.getAttribute('aria-expanded'), 'true');
toggle.click();
assert.equal(toggle.getAttribute('aria-expanded'), 'false');
close();

const en = await load('?locale=en&mode=timeline#SZDKOR.unidentified.113?density=compact&lanes=biography,correspondence');
assert.equal(en.errors.length, 0);
assert.ok(en.d.getElementById('SZDKOR.unidentified.113').closest('details').open, 'shared fragment opens original source after reload');
assert.match(en.d.getElementById('zl-from-label').textContent, /From year/);
assert.equal(en.d.querySelectorAll('.zl-ev').length, visible.filter((e) => ['biography', 'correspondence'].includes(e.lane)).length);
assert.ok(en.d.querySelector('.zl-lane-biography.zl-ev .zl-text').textContent.includes(data.biography[0].title.en.slice(0, 15)));
assert.match(en.d.querySelector('.zl-sources summary').textContent, /source records/);
for (const link of en.d.querySelectorAll('.zl-sources a')) {
	assert.equal(new URL(link.href).origin, new URL(page).origin);
	assert.equal(new URL(link.href).searchParams.get('locale'), 'en');
}
assert.ok(en.d.body.classList.contains('zl-compact'));
en.close();

const failureOptions = { fail: true };
const failing = await load('?locale=en&mode=timeline', failureOptions);
assert.equal(failing.d.getElementById('zl-app').getAttribute('aria-busy'), 'false');
assert.match(failing.d.getElementById('zl-status').textContent, /could not be loaded/);
assert.equal(failing.d.querySelector('#zl-status button').textContent, 'Try again');
failureOptions.fail = false;
failing.d.querySelector('#zl-status button').click();
await tick();
await tick();
assert.equal(failing.d.querySelectorAll('.zl-ev').length, visible.length, 'retry restores the complete view');
assert.equal(failing.requests.length, 8, 'retry requests each lane once');
failing.close();

const safe = await load('?locale=de&mode=timeline&lanes=biography');
const bad = structuredClone(data);
bad.biography[0].title.de = '<img src=x onerror="alert(1)">';
bad.biography[0].href = 'javascript:alert(1)';
bad.biography[0].facsimile = 'javascript:alert(1)';
safe.w.szdZeitleiste(bad);
assert.equal(safe.d.querySelector('.zl-text img'), null);
assert.match(safe.d.querySelector('.zl-text').textContent, /<img/);
assert.equal(safe.d.querySelector('a[href^="javascript:"]'), null);
safe.close();
console.log('OK timeline: ' + visible.length + ' real entries, ' + withheld.length + ' withheld, ' + undated + ' undated; lanes, filters, keyboard, URL, EN, loading failure and safe text.');
