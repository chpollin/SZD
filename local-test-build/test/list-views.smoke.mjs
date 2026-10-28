// Smoke test of the list-view switcher (js/list-views.js) against the really rendered
// pages of the Aufsatzablage and the personal documents (szd-Werke.xsl on
// o:szd.lebensdokumente, built as szd-Lebensdokumente by snapshot.mjs). The expected entry
// and category counts are read from the input the page was built from, so a page rendered
// from another object fails.
//
// Checked per page: the server-rendered default structure, that switching changes the
// groups and the jump navigation, that switching back restores the default byte for
// byte, and that the number of entries is the same in every mode.
import { root } from '../harness.mjs';
import { resolve } from 'node:path';
import { JSDOM } from 'jsdom';
import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
import { buildDir } from './paths.mjs';

const js = readFileSync(resolve(root, 'js/list-views.js'), 'utf8');

const build = pathToFileURL(buildDir + '/');
const source = (page) => new JSDOM(readFileSync(new URL(page + '.input.xml', build), 'utf8'), { contentType: 'text/xml' }).window.document;
const sourceEntries = (page) => source(page).getElementsByTagName('biblFull').length;
// fn:kategorie of szd-Essays.xsl groups by the German classification term, else the first one
const sourceCategories = (page) => new Set([...source(page).getElementsByTagName('biblFull')].map((entry) => {
	const terms = [...entry.getElementsByTagName('term')].filter((t) => t.getAttribute('type') === 'classification');
	return ((terms.find((t) => t.getAttribute('xml:lang') === 'de') || terms[0])?.textContent || '').trim();
})).size;

function load(file) {
	const html = readFileSync(new URL(file, build), 'utf8');
	const dom = new JSDOM(html, { runScripts: 'outside-only', url: 'http://localhost:8080/x?locale=de' });
	dom.window.eval(js);
	return dom.window;
}

const shape = (w) => {
	const list = w.document.querySelector('.list-views');
	const nav = w.document.querySelector('.header-card-nav ul.list-inline');
	return {
		groups: [...list.querySelectorAll('h2')].map((h) => h.textContent.trim()),
		subs: list.querySelectorAll('h3').length,
		entries: list.querySelectorAll('[data-view-sort]').length,
		nav: [...nav.querySelectorAll('a')].map((a) => a.textContent.trim()),
		html: list.innerHTML,
		navHTML: nav.innerHTML
	};
};

let failures = 0;
async function check(name, file, defaultMode, otherMode, expect) {
	const w = load(file);
	await new Promise((r) => setTimeout(r, 50));
	try {
		const base = shape(w);
		assert.equal(typeof w.setListView, 'function', 'setListView not exposed');
		assert.equal(w.document.querySelector('.list-views').getAttribute('data-view'), defaultMode);
		assert.deepEqual(base.groups, expect.groups, 'default groups');
		assert.equal(base.entries, expect.entries, 'default entry count');

		w.setListView(otherMode);
		const other = shape(w);
		assert.equal(other.entries, base.entries, 'entry count changed when switching');
		assert.notDeepEqual(other.groups, base.groups, 'groups did not change');
		assert.notDeepEqual(other.nav, base.nav, 'jump navigation did not change');
		assert.deepEqual(other.nav, other.groups, 'jump navigation does not match the groups');
		assert.equal(other.groups.length, expect.otherGroups, 'group count in the other mode');
		assert.equal(
			w.document.querySelector('.list-viewswitch [data-mode="' + otherMode + '"]').classList.contains('active'),
			true, 'button not marked active');

		w.setListView(defaultMode);
		const back = shape(w);
		assert.equal(back.html, base.html, 'default structure not restored');
		assert.equal(back.navHTML, base.navHTML, 'jump navigation not restored');

		console.log('  ok   - ' + name);
		console.log('         ' + defaultMode + ': ' + base.groups.length + ' Gruppen, ' + base.subs +
			' Untergruppen, ' + base.entries + ' Eintraege');
		console.log('         ' + otherMode + ': ' + other.groups.length + ' Gruppen, ' + other.subs +
			' Untergruppen, ' + other.entries + ' Eintraege');
		console.log('         ' + otherMode + ' Gruppen: ' + other.groups.join(' | '));
	} catch (e) {
		failures++;
		console.log('  FAIL - ' + name + '\n         ' + e.message);
	}
}

// Aufsatzablage: alphabetical register (default) against category. SCH and ST keep
// their own group and stand where their label belongs, between S and T.
await check('Aufsatzablage (szd-Essays)', 'szd-Essays.html', 'register', 'kategorie', {
	groups: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R',
		'S', 'SCH', 'ST', 'T', 'U', 'V', 'W', 'Y', 'Y-Z', 'Z'],
	entries: sourceEntries('szd-Essays'),
	otherGroups: sourceCategories('szd-Essays')
});

// Lebensdokumente: category plus Einheitssachtitel (default) against year, which is a
// flat view without the Einheitssachtitel level.
await check('Lebensdokumente (szd-Werke)', 'szd-Lebensdokumente.html', 'kategorie', 'chronologie', {
	groups: ['ABSCHIEDSBRIEF', 'ADRESSBÜCHER', 'BÜROMATERIALIEN', 'DIVERSES', 'FINANZEN', 'KALENDER',
		'RECHTSDOKUMENTE', 'TAGEBÜCHER', 'VERLAGSVERTRÄGE', 'VERZEICHNISSE'],
	entries: sourceEntries('szd-Lebensdokumente'),
	otherGroups: 25
});

console.log('\n' + (failures ? failures + ' fehlgeschlagen.' : 'alle bestanden.'));
if (failures) { process.exit(1); }
