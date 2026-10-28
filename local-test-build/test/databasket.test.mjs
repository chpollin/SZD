// Unit tests for js/databasket.js -- the data cart (Datenkorb) is pure
// client-side logic (localStorage + DOM), so it runs in jsdom without the GAMS
// runtime. Covers add/toggle/dedup, remove, keepCheckboxes restore, counter,
// empty-basket guard, delete, clear, and the basket page: CSV content, filter,
// sorting, the table controls and the two exports.
//
//   cd local-test-build && npm install && npm test
import { root } from '../harness.mjs';
import { JSDOM, VirtualConsole } from 'jsdom';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import assert from 'node:assert/strict';

const here = dirname(fileURLToPath(import.meta.url));
const code = readFileSync(resolve(root, 'js/databasket.js'), 'utf8');

// silent console: jsdom emits "Not implemented: navigation" when delet_DB /
// clearData call location.reload() -- harmless here, swallow it
const virtualConsole = new VirtualConsole();

const dom = new JSDOM('<!DOCTYPE html><html><body><span id="db_static"></span></body></html>', {
	url: 'https://gams.uni-graz.at/o:szd.werke',
	runScripts: 'dangerously',
	virtualConsole
});
const { window } = dom;
const { document } = window;

// the script registers its load handler with addEventListener; keep it as
// window.__onLoad so tests can run it, and inject the script so its globals land on window
const script = document.createElement('script');
script.textContent = 'window.addEventListener = (function (add) { return function (type, fn, options) { if (type === "load") { window.__onLoad = fn; } return add.call(window, type, fn, options); }; })(window.addEventListener);\n' + code;
document.body.appendChild(script);
assert.equal(typeof window.$, 'undefined', 'the basket must not need jQuery');
assert.equal(typeof window.__onLoad, 'function', 'load handler not registered');

const PROJECT = 'szd';
const basket = () => JSON.parse(window.localStorage.getItem(PROJECT)) || [];

function reset() {
	window.localStorage.removeItem(PROJECT);
	document.body.innerHTML = '<span id="db_static"></span>';
	Object.assign(window.basketView, { wired: false, key: null, direction: 'ascending', query: '' });
}

// build a .db_entry plus its checkbox (#cb<id>); return the checkbox
function makeEntry(id, data) {
	const entry = document.createElement('div');
	entry.className = 'list-group-item entry db_entry shadow-sm';
	entry.id = id;
	Object.keys(data).forEach((k) => entry.setAttribute('data-' + k, data[k]));
	const span = document.createElement('span');
	const cb = document.createElement('input');
	cb.type = 'checkbox';
	cb.id = 'cb' + id;
	span.appendChild(cb);
	entry.appendChild(span);
	document.body.appendChild(entry);
	return cb;
}

function tbody() {
	const tb = document.createElement('tbody');
	tb.id = 'databasekt_tbody';
	document.body.appendChild(tb);
	return tb;
}

let passed = 0;
const failures = [];
const pending = [];
function test(name, fn) {
	reset();
	try {
		fn();
		passed++;
		console.log('  ok   - ' + name);
	} catch (e) {
		failures.push({ name, e });
		console.log('  FAIL - ' + name + '\n         ' + e.message);
	}
}

test('Anhaken legt einen Eintrag ab', () => {
	const cb = makeEntry('SZDMSK.1', { uri: 'u1', title: 'T1', collection: 'W' });
	cb.checked = true;
	window.add_DB('SZDMSK.1');
	assert.equal(basket().length, 1);
	assert.equal(basket()[0].uri, 'u1');
	assert.equal(basket()[0].title, 'T1');
});

test('Erneutes Anhaken erzeugt kein Duplikat', () => {
	const cb = makeEntry('SZDMSK.1', { uri: 'u1', title: 'T1' });
	cb.checked = true;
	window.add_DB('SZDMSK.1');
	window.add_DB('SZDMSK.1'); // checkbox still checked
	assert.equal(basket().length, 1);
});

test('Abhaken entfernt den Eintrag', () => {
	const cb = makeEntry('SZDMSK.1', { uri: 'u1' });
	cb.checked = true;
	window.add_DB('SZDMSK.1');
	cb.checked = false;
	window.add_DB('SZDMSK.1');
	assert.equal(basket().length, 0);
});

test('Zwei verschiedene URIs koexistieren (Dedup nach uri, nicht Signatur)', () => {
	const a = makeEntry('A', { uri: 'u1', signature: 'SZ-AAP/B2.3' });
	const b = makeEntry('B', { uri: 'u2', signature: 'SZ-AAP/B2.3' });
	a.checked = true;
	window.add_DB('A');
	b.checked = true;
	window.add_DB('B');
	assert.equal(basket().length, 2);
});

test('keepCheckboxes hakt abgelegte Eintraege wieder an', () => {
	const cb = makeEntry('SZDMSK.1', { uri: 'u1' });
	cb.checked = true;
	window.add_DB('SZDMSK.1');
	cb.checked = false; // simulate a fresh page load with an unchecked box
	window.keepCheckboxes();
	assert.equal(cb.checked, true);
});

test('countEntrys schreibt den Zaehler', () => {
	const cb = makeEntry('SZDMSK.1', { uri: 'u1' });
	cb.checked = true;
	window.add_DB('SZDMSK.1');
	assert.equal(document.getElementById('db_static').innerHTML, ' (1)');
});

test('Leerer Korb: showData/countEntrys werfen nicht', () => {
	const tb = tbody();
	window.showData();
	window.countEntrys();
	assert.equal(tb.children.length, 0);
	assert.equal(document.getElementById('db_static').innerHTML, '');
});

test('showData rendert eine Zeile pro Eintrag', () => {
	const cb = makeEntry('SZDMSK.1', { uri: 'u1', title: 'T', collection: 'W', signature: 'Sig' });
	cb.checked = true;
	window.add_DB('SZDMSK.1');
	const tb = tbody();
	window.showData();
	assert.equal(tb.querySelectorAll('tr').length, 1);
	assert.equal(tb.querySelector('td').textContent, 'W'); // first cell = collection sigle
});

test('delet_DB entfernt nach uri', () => {
	const a = makeEntry('A', { uri: 'u1' });
	a.checked = true;
	window.add_DB('A');
	const b = makeEntry('B', { uri: 'u2' });
	b.checked = true;
	window.add_DB('B');
	window.delet_DB('u1');
	assert.equal(basket().length, 1);
	assert.equal(basket()[0].uri, 'u2');
});

test('clearData leert den Korb', () => {
	const cb = makeEntry('A', { uri: 'u1' });
	cb.checked = true;
	window.add_DB('A');
	window.clearData();
	assert.equal(basket().length, 0);
});

// storage outside our control: a corrupt or foreign value, or a blocked storage,
// must not break the page; the basket then reads as empty
function withStorage(storage, fn) {
	const original = Object.getOwnPropertyDescriptor(window, 'localStorage');
	Object.defineProperty(window, 'localStorage', { configurable: true, get: storage });
	try { fn(); } finally { Object.defineProperty(window, 'localStorage', original); }
}
const blocked = () => { throw new window.DOMException('blocked', 'SecurityError'); };

for (const raw of ['{not json', '{"a":1}', '"text"', '42', 'null']) {
	test('Kaputter Speicherwert ' + raw + ': Korb gilt als leer, Seite laeuft weiter', () => {
		window.localStorage.setItem(PROJECT, raw);
		const cb = makeEntry('A', { uri: 'u1', title: 'T' });
		const tb = tbody();
		window.__onLoad();
		window.showData();
		assert.equal(tb.children.length, 0);
		assert.equal(document.getElementById('db_static').innerHTML, '');
		cb.checked = true;
		window.add_DB('A'); // replaces the corrupt value with a valid basket
		assert.equal(basket().length, 1);
		assert.equal(basket()[0].uri, 'u1');
	});
}

test('Fremde Eintraege im Array (null, Skalar) werden uebergangen', () => {
	window.localStorage.setItem(PROJECT, JSON.stringify([null, 'x', { uri: 'u1', title: 'T' }]));
	const tb = tbody();
	window.showData();
	window.countEntrys();
	assert.equal(tb.querySelectorAll('tr').length, 1);
	assert.equal(document.getElementById('db_static').innerHTML, ' (1)');
});

test('Gueltiger Korb bleibt beim Laden und Lesen erhalten', () => {
	const stored = [{ uri: 'u1', title: 'T1' }, { uri: 'u2', title: 'T2' }];
	window.localStorage.setItem(PROJECT, JSON.stringify(stored));
	const a = makeEntry('A', { uri: 'u1' });
	const tb = tbody();
	window.__onLoad();
	window.showData();
	assert.equal(a.checked, true);
	assert.equal(tb.querySelectorAll('tr').length, 2);
	assert.equal(document.getElementById('db_static').innerHTML, ' (2)');
	assert.deepEqual(basket(), stored);
});

test('Gesperrter Speicher: Laden, Anhaken, Anzeigen, Loeschen und Leeren werfen nicht', () => {
	const cb = makeEntry('A', { uri: 'u1' });
	const tb = tbody();
	withStorage(blocked, () => {
		window.__onLoad();
		cb.checked = true;
		window.add_DB('A');
		window.showData();
		window.delet_DB('u1');
		window.clearData();
	});
	assert.equal(tb.children.length, 0);
	assert.equal(document.getElementById('A').getAttribute('data-check'), 'checked');
});

test('Voller Speicher (setItem wirft): Anhaken wirft nicht, alter Korb bleibt', () => {
	window.localStorage.setItem(PROJECT, JSON.stringify([{ uri: 'u0' }]));
	const real = window.localStorage;
	const full = {
		getItem: (k) => real.getItem(k),
		setItem: () => { throw new window.DOMException('full', 'QuotaExceededError'); },
		removeItem: (k) => real.removeItem(k)
	};
	const cb = makeEntry('A', { uri: 'u1' });
	cb.checked = true;
	withStorage(() => full, () => { window.add_DB('A'); });
	assert.deepEqual(basket(), [{ uri: 'u0' }]);
});

// The basket page, as szd-context.xsl renders it, with the columns of the table and the CSV
const columns = ['collection', 'title', 'author', 'location', 'signature', 'uri'];
function basketPage(items) {
	window.localStorage.setItem(PROJECT, JSON.stringify(items));
	document.body.innerHTML = '<span id="db_static"></span>'
		+ '<input type="search" id="databasket_filter">'
		+ '<button type="button" id="databasket_csv">CSV</button><button type="button" id="databasket_pdf">PDF</button>'
		+ '<p id="databasket_status" role="status"></p><time id="databasket_date"></time>'
		+ '<table id="databasket_table"><thead><tr>'
		+ columns.map((c) => '<th scope="col" data-column="' + c + '"><button type="button" data-sort="' + c + '">' + c + '</button></th>').join('')
		+ '<th class="db-col-remove"></th></tr></thead><tbody id="databasekt_tbody"></tbody></table>';
	window.basketView.wired = false;
	window.basketView.key = null;
	window.basketView.query = '';
	window.showData();
	return document.getElementById('databasekt_tbody');
}
const cells = (tbody, column) => [...tbody.querySelectorAll('tr')].map((tr) => tr.querySelector('.db-col-' + column).textContent);
// entries as the catalogue pages store them (data-* of the entry); the library stores a blank location
const sample = [
	{ uri: 'https://gams.uni-graz.at/o:szd.autographen#SZDAUT.10', collection: 'A', title: 'Dépit', author: 'De Coster, Charles', location: 'Fondation Martin Bodmer', signature: 'SZDAUT.10' },
	{ uri: 'https://gams.uni-graz.at/o:szd.bibliothek#SZDBIB.2', collection: 'B', title: 'Faust; "Der Tragödie" erster Teil', author: 'Goethe, Johann Wolfgang von', location: ' ', signature: 'SZDBIB.2' },
	{ uri: 'https://gams.uni-graz.at/o:szd.autographen#SZDAUT.2', collection: 'A', title: 'Zürcher Brief', author: '', location: 'Zürich', signature: 'SZDAUT.2' },
	{ uri: 'https://gams.uni-graz.at/o:szd.korrespondenzen#SZDKOR.475', collection: 'C', title: '1 Korrespondenzstück AN Stefan Zweig', author: 'Wunderlich, Eva', location: 'Literaturarchiv Salzburg', signature: 'SZ-AP2/B-109' }
];

test('CSV: BOM, Semikolon, CRLF, Kopfzeile und sechs getrennte Spalten', () => {
	const csv = window.basketToCsv(sample, 'de');
	assert.ok(csv.startsWith('﻿'), 'BOM');
	assert.ok(csv.endsWith('\r\n'));
	assert.ok(!csv.replace(/\r\n/g, '').includes('\n'), 'only CRLF line ends');
	const lines = csv.slice(1).split('\r\n');
	assert.equal(lines.pop(), '');
	assert.equal(lines.length, sample.length + 1);
	assert.equal(lines[0], '"Sigle";"Titel";"Autor/in";"Standort";"Signatur";"URI"');
	assert.equal(lines[1], '"A";"Dépit";"De Coster, Charles";"Fondation Martin Bodmer";"SZDAUT.10";"https://gams.uni-graz.at/o:szd.autographen#SZDAUT.10"');
	assert.equal(window.basketToCsv([], 'en'), '﻿"Collection";"Title";"Author";"Location";"Signature";"URI"\r\n');
});

test('CSV: Anführungszeichen verdoppelt, Semikolon im Feld, leerer Standort, Zeilenumbruch', () => {
	const lines = window.basketToCsv([sample[1], { uri: 'u', title: 'zwei\nZeilen', collection: 'W' }], 'de').slice(1).split('\r\n');
	assert.equal(lines[1], '"B";"Faust; ""Der Tragödie"" erster Teil";"Goethe, Johann Wolfgang von";"";"SZDBIB.2";"https://gams.uni-graz.at/o:szd.bibliothek#SZDBIB.2"');
	assert.equal(lines[2], '"W";"zwei Zeilen";"";"";"";"u"');
});

test('CSV: Werte, die eine Tabellenformel beginnen, werden entschärft', () => {
	const line = window.basketToCsv([{ uri: 'u', title: '=HYPERLINK("x")', author: '+1', signature: '-12', location: '@a' }], 'de').slice(1).split('\r\n')[1];
	assert.equal(line, `"";"'=HYPERLINK(""x"")";"'+1";"'@a";"-12";"u"`);
});

test('CSV: sprechender Dateiname mit Datum', () => {
	assert.equal(window.basketCsvName(new Date(2026, 9, 21), 'de'), 'szd-datenkorb-2026-10-21.csv');
	assert.equal(window.basketCsvName(new Date(2026, 0, 5), 'en'), 'szd-databasket-2026-01-05.csv');
});

test('Filter: alle Wörter, ohne Groß- und Kleinschreibung, Diakritika und Umlautschreibung', () => {
	const ids = (rows) => rows.map((item) => item.signature);
	assert.deepEqual(ids(window.filterBasket(sample, '')), ids(sample));
	assert.deepEqual(ids(window.filterBasket(sample, '  ')), ids(sample));
	assert.deepEqual(ids(window.filterBasket(sample, 'zurich')), ['SZDAUT.2']);
	assert.deepEqual(ids(window.filterBasket(sample, 'ZUERICH')), ['SZDAUT.2']);
	assert.deepEqual(ids(window.filterBasket(sample, 'depit coster')), ['SZDAUT.10']);
	assert.deepEqual(ids(window.filterBasket(sample, 'goethe tragoedie')), ['SZDBIB.2']);
	assert.deepEqual(ids(window.filterBasket(sample, 'B-109')), ['SZ-AP2/B-109']);
	assert.deepEqual(ids(window.filterBasket(sample, 'goethe zweig')), []);
});

test('Sortierung: numerisch, stabil, leere Werte zuletzt, beide Richtungen', () => {
	const ids = (rows) => rows.map((item) => item.signature);
	assert.deepEqual(ids(window.sortBasket(sample, 'signature', 'ascending')), ['SZ-AP2/B-109', 'SZDAUT.2', 'SZDAUT.10', 'SZDBIB.2']);
	assert.deepEqual(ids(window.sortBasket(sample, 'signature', 'descending')), ['SZDBIB.2', 'SZDAUT.10', 'SZDAUT.2', 'SZ-AP2/B-109']);
	assert.deepEqual(ids(window.sortBasket(sample, 'author', 'ascending')), ['SZDAUT.10', 'SZDBIB.2', 'SZ-AP2/B-109', 'SZDAUT.2']);
	assert.deepEqual(ids(window.sortBasket(sample, 'author', 'descending')), ['SZ-AP2/B-109', 'SZDBIB.2', 'SZDAUT.10', 'SZDAUT.2']);
	assert.deepEqual(ids(window.sortBasket(sample, 'collection', 'ascending')), ['SZDAUT.10', 'SZDAUT.2', 'SZDBIB.2', 'SZ-AP2/B-109']);
	assert.deepEqual(ids(window.sortBasket(sample, 'unknown', 'ascending')), ids(sample));
});

test('Korbseite: Tabelle, Filterfeld und Statuszeile', () => {
	const tb = basketPage(sample);
	assert.deepEqual(cells(tb, 'signature'), sample.map((item) => item.signature), 'stored order without a sort');
	assert.equal(cells(tb, 'location')[1], '', 'blank library location');
	assert.equal(tb.querySelector('.db-col-uri a').getAttribute('href'), sample[0].uri);
	assert.equal(document.getElementById('databasket_status').textContent, '4 Einträge');
	const filter = document.getElementById('databasket_filter');
	filter.value = 'autographen';
	filter.dispatchEvent(new window.Event('input'));
	assert.deepEqual(cells(tb, 'signature'), ['SZDAUT.10', 'SZDAUT.2']);
	assert.equal(document.getElementById('databasket_status').textContent, '2 von 4 Einträgen');
	filter.value = 'nichts';
	filter.dispatchEvent(new window.Event('input'));
	assert.equal(tb.children.length, 0);
	assert.equal(document.getElementById('databasket_status').textContent, 'Kein Eintrag entspricht dem Filter.');
	assert.equal(document.getElementById('databasket_csv').disabled, true);
	assert.equal(document.getElementById('databasket_pdf').disabled, true);
});

test('Korbseite: Spaltenkopf sortiert auf- und absteigend, aria-sort folgt', () => {
	const tb = basketPage(sample);
	const button = document.querySelector('[data-sort="title"]');
	const th = button.closest('th');
	button.click();
	assert.equal(th.getAttribute('aria-sort'), 'ascending');
	assert.deepEqual(cells(tb, 'title'), ['1 Korrespondenzstück AN Stefan Zweig', 'Dépit', 'Faust; "Der Tragödie" erster Teil', 'Zürcher Brief']);
	button.click();
	assert.equal(th.getAttribute('aria-sort'), 'descending');
	assert.equal(cells(tb, 'title')[0], 'Zürcher Brief');
	document.querySelector('[data-sort="author"]').click();
	assert.equal(th.hasAttribute('aria-sort'), false, 'only the sorted column carries aria-sort');
	assert.equal(document.querySelector('th[data-column="author"]').getAttribute('aria-sort'), 'ascending');
});

test('Korbseite: Entfernen-Knopf mit Namen, ohne Neuladen, Fokus bleibt in der Tabelle', () => {
	const tb = basketPage(sample);
	const buttons = tb.querySelectorAll('button');
	assert.equal(buttons[0].getAttribute('aria-label'), 'Aus dem Datenkorb entfernen: Dépit');
	assert.equal(buttons[0].getAttribute('onclick'), null, 'no inline handler built from stored data');
	buttons[1].focus();
	buttons[1].click();
	assert.deepEqual(basket().map((item) => item.signature), ['SZDAUT.10', 'SZDAUT.2', 'SZ-AP2/B-109']);
	assert.equal(tb.children.length, 3);
	assert.equal(document.activeElement, tb.querySelectorAll('button')[1], 'focus moves to the next remove button');
	assert.equal(document.getElementById('db_static').textContent, ' (3)');
	window.clearData();
	assert.equal(tb.children.length, 0);
	assert.equal(document.getElementById('databasket_status').textContent, 'Der Datenkorb ist leer.');
	assert.equal(document.getElementById('databasket_table').hidden, true);
});

test('Korbseite: CSV-Knopf lädt die angezeigten Einträge als Datei herunter', () => {
	const tb = basketPage(sample);
	const filter = document.getElementById('databasket_filter');
	filter.value = 'korrespondenz';
	filter.dispatchEvent(new window.Event('input'));
	let blob = null;
	let name = null;
	window.URL.createObjectURL = (b) => { blob = b; return 'blob:test'; };
	window.URL.revokeObjectURL = () => {};
	const click = window.HTMLAnchorElement.prototype.click;
	window.HTMLAnchorElement.prototype.click = function () { name = this.download; };
	try { document.getElementById('databasket_csv').click(); } finally { window.HTMLAnchorElement.prototype.click = click; }
	assert.equal(tb.children.length, 1);
	assert.match(name, /^szd-datenkorb-\d{4}-\d{2}-\d{2}\.csv$/);
	assert.equal(blob.type, 'text/csv;charset=utf-8');
	pending.push(['CSV-Datei enthält genau die angezeigten Einträge', new Promise((done, fail) => {
		// jsdom's Blob has no arrayBuffer(), its FileReader reads the bytes
		const reader = new window.FileReader();
		reader.onload = () => done(reader.result);
		reader.onerror = () => fail(reader.error);
		reader.readAsArrayBuffer(blob);
	}).then((buffer) => {
		const bytes = new Uint8Array(buffer);
		assert.deepEqual([...bytes.slice(0, 3)], [0xEF, 0xBB, 0xBF], 'UTF-8 BOM in the file');
		const text = new TextDecoder().decode(bytes);
		assert.equal(text.split('\r\n').length, 3, 'header, the one shown entry, final line end');
		assert.ok(text.includes('SZDKOR.475'));
	})]);
});

test('Korbseite: PDF-Knopf öffnet den Druckdialog, das Druckdatum steht', () => {
	basketPage(sample);
	let printed = 0;
	window.print = () => { printed++; };
	document.getElementById('databasket_pdf').click();
	assert.equal(printed, 1);
	assert.match(document.getElementById('databasket_date').getAttribute('datetime'), /^\d{4}-\d{2}-\d{2}$/);
	assert.ok(document.getElementById('databasket_date').textContent.trim());
});

for (const [name, promise] of pending) {
	try {
		await promise;
		passed++;
		console.log('  ok   - ' + name);
	} catch (e) {
		failures.push({ name, e });
		console.log('  FAIL - ' + name + '\n         ' + e.message);
	}
}

console.log('\n' + passed + ' bestanden, ' + failures.length + ' fehlgeschlagen.');
if (failures.length) { process.exit(1); }
