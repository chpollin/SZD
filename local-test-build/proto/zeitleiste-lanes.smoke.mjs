// Smoke test of the Zeitleiste prototype against the lane fixtures in proto/data.
// The page attaches its script through <base>-safe injection, which jsdom does not
// fetch, so the script is evaluated here and the view is started by hand.
import { JSDOM } from 'jsdom';
import { readFileSync } from 'node:fs';

const read = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');
const html = read('./zeitleiste-lanes.html');
const js = read('./zeitleiste-lanes.js');
const LANES = ['biography', 'correspondence', 'personal-documents', 'autographs'];
const data = Object.fromEntries(LANES.map((l) => [l, JSON.parse(read(`./data/${l}.json`))]));
const index = JSON.parse(read('./data/index.json'));
const MAX_YEAR = 1950;

// jsdom knows no IntersectionObserver, so the view renders every group at once and
// the test sees the real rows instead of the placeholders
const PAGE = 'http://localhost:8080/local-test-build/proto/zeitleiste-lanes.html';
const dom = new JSDOM(html, { runScripts: 'dangerously', url: PAGE });
const w = dom.window;
const d = w.document;
w.eval(js);
const total = w.szdZeitleiste(data);

const rows = () => [...d.querySelectorAll('#zl-content .zl-group')].reduce((n, s) => n + (s.rowsToRender ? s.rowsToRender.length : s.rowBox.children.length), 0);
const groups = () => d.querySelectorAll('#zl-content .zl-group').length;
const bars = () => d.querySelectorAll('#zl-plot .zl-lane-row').length;
const laneChip = (lane) => d.querySelector('.zl-lane-' + lane + '.zl-chip');
const placeOptions = () => [...d.querySelectorAll('#zl-place-list button')];

// events dated after 1950 are misread dates of the source and leave the view
const beyond = LANES.flatMap((l) => data[l].filter((e) => e.date && +e.date.slice(0, 4) > MAX_YEAR));
const fromIndex = index.lanes.reduce((n, l) => n + l.events, 0);
console.log('OK  events:', total, ' index.json:', fromIndex, ' withheld after', MAX_YEAR + ':', beyond.map((e) => e.id + ' ' + e.date).join(', '));
console.log('    year groups:', groups(), ' bar rows:', bars(), ' axis cells:', d.querySelectorAll('#zl-axis a').length);
console.log('    lane chips:', LANES.map((l) => laneChip(l).textContent).join(' | '));
if (total !== fromIndex - beyond.length) throw new Error('event count does not match index.json minus the withheld pieces');
if (rows() !== total) throw new Error('rows do not match the event count');
if (beyond.some((e) => d.getElementById(e.id))) throw new Error('a withheld piece reached the list');
const axisYears = [...d.querySelectorAll('#zl-axis a')].map((a) => +a.dataset.year);
if (axisYears[axisYears.length - 1] !== MAX_YEAR) throw new Error('the axis runs past ' + MAX_YEAR);
if (d.querySelectorAll('#zl-plot .zl-bar').length === 0) throw new Error('no bars in the scale');

// the rendered row carries the lane, its icon, the date column and the links
const letter = data.correspondence.find((e) => e.facsimile && e.signature && e.datePrecision === 'day');
const letterRow = d.getElementById(letter.id);
const autograph = data.autographs.find((e) => e.dateOrigin && e.date);
const autographRow = d.getElementById(autograph.id);
const bioRow = d.getElementById(data.biography.find((e) => e.persons.length).id);
console.log('    letter row:', letterRow.className, '|', letterRow.querySelector('.zl-when').textContent, '|', letterRow.querySelector('.zl-meta').textContent.trim());
console.log('    autograph row:', autographRow.querySelector('.zl-when').textContent, '|', autographRow.querySelector('.zl-meta').textContent.trim());
if (!letterRow.querySelector('.zl-lane-icon.fa-envelope')) throw new Error('lane icon missing in the entry');
if (!letterRow.querySelector('.zl-fac[href$="' + letter.facsimile + '"]')) throw new Error('facsimile link missing');
if (letterRow.querySelector('.zl-when').textContent.indexOf(letter.dateLabel.de) < 0) throw new Error('date label missing');
if (autographRow.querySelector('.zl-meta').textContent.indexOf(autograph.dateOriginLabel.de) < 0) throw new Error('origin date missing');
if (!bioRow.querySelector('.zl-persons a[href*="person_search"]')) throw new Error('person link missing in the biography');
if (!laneChip('autographs').querySelector('.zl-icon.fa-feather')) throw new Error('lane icon missing in the chip');
const yearOnly = data.correspondence.find((e) => e.datePrecision === 'year');
if (d.getElementById(yearOnly.id).querySelector('.zl-mark').textContent !== 'nur Jahr') throw new Error('year-only mark missing');

// the year heading counts in a language-correct plural
const singles = [...d.querySelectorAll('#zl-content .zl-group')].filter((s) => (s.rowsToRender || s.rowBox.children).length === 1);
console.log('    single-entry heading:', singles.length ? singles[0].querySelector('.zl-year-count').textContent : 'none');
if (singles.length && singles[0].querySelector('.zl-year-count').textContent !== '1 Eintrag') throw new Error('plural of the entry count is wrong');
if (d.body.textContent.indexOf('Eintraege') >= 0 || d.body.textContent.indexOf('fuer') >= 0) throw new Error('umlaut written as a digraph');

// the tooltip replaces the standing readout line
if (d.getElementById('zl-readout')) throw new Error('the standing readout line is still there');
const tip = d.getElementById('zl-tip');
if (!tip.hidden) throw new Error('tooltip visible without hover or focus');
const cell = [...d.querySelectorAll('#zl-axis a')].find((a) => a.dataset.year === '1933');
cell.dispatchEvent(new w.FocusEvent('focusin', { bubbles: true }));
console.log('    tooltip on 1933:', tip.textContent, '| hidden before focus: true');
if (tip.hidden || tip.textContent.indexOf('1933') !== 0) throw new Error('tooltip does not follow the focus');
d.getElementById('zl-axis').dispatchEvent(new w.FocusEvent('focusout', { bubbles: true }));
if (!tip.hidden) throw new Error('tooltip stays after focus has left');

// lane off and on again
const before = { rows: rows(), bars: bars() };
laneChip('autographs').click();
const off = { rows: rows(), bars: bars() };
console.log('    autographs off: rows', before.rows, '->', off.rows, ' bar rows', before.bars, '->', off.bars);
if (off.rows !== before.rows - data.autographs.length) throw new Error('switching the lane off did not change the list');
if (off.bars !== before.bars - 1) throw new Error('switching the lane off did not change the scale');
if (laneChip('autographs').getAttribute('aria-pressed') !== 'false') throw new Error('aria-pressed not updated');
laneChip('autographs').click();
if (rows() !== before.rows) throw new Error('switching the lane on again did not restore the list');

// place filter through the dropdown, no chip wall any more
if (d.getElementById('zl-places')) throw new Error('the place chip bar is still there');
const placeButton = d.getElementById('zl-place-button');
placeButton.click();
if (d.getElementById('zl-place-popup').hidden) throw new Error('place popup did not open');
const search = d.getElementById('zl-place-search');
search.value = 'Ber';
search.dispatchEvent(new w.Event('input'));
const found = placeOptions().map((b) => b.textContent);
console.log('    place popup filtered by "Ber":', found.join(' | '));
const berlin = placeOptions().find((b) => b.textContent.indexOf('Berlin') === 0);
berlin.click();
const placeRows = rows();
console.log('    place Berlin:', placeRows, 'rows,', groups(), 'groups, button:', placeButton.textContent);
if (placeRows >= before.rows || placeRows === 0) throw new Error('place filter without effect');
if (!d.getElementById('zl-place-popup').hidden) throw new Error('place popup did not close');
if (placeButton.textContent.indexOf('Berlin') < 0) throw new Error('the button does not name the chosen place');

// an active filter appears as a removable chip in the second line
const active = [...d.querySelectorAll('#zl-active .zl-chip')];
console.log('    active filters:', active.map((c) => c.textContent).join(' | '));
if (active.length !== 1) throw new Error('the active filter is not shown as a chip');
active[0].click();
if (rows() !== before.rows) throw new Error('removing the chip did not clear the filter');
if (d.querySelectorAll('#zl-active .zl-chip').length !== 0) throw new Error('the second line stays without a filter');

// person filter
const person = d.getElementById('zl-person');
const sample = data.correspondence.find((e) => e.persons.length > 1 && e.persons[0].name !== 'Zweig, Stefan').persons[0].name;
person.value = sample;
person.dispatchEvent(new w.Event('input'));
const personRows = rows();
console.log('    person', sample + ':', personRows, 'rows, chips:', [...d.querySelectorAll('#zl-active .zl-chip')].map((c) => c.textContent).join(''));
if (personRows === 0 || personRows >= before.rows) throw new Error('person filter without effect');
person.value = '';
person.dispatchEvent(new w.Event('input'));

// period filter through the URL state the brush writes
w.history.replaceState(null, '', PAGE + '?from=1930&to=1935');
w.szdZeitleiste(data);
const rangeGroups = [...d.querySelectorAll('#zl-content .zl-group h3')].map((h) => h.id);
console.log('    period 1930 to 1935:', rows(), 'rows in', rangeGroups.join(', '), '| chip:', d.querySelector('#zl-active .zl-chip').textContent);
if (rangeGroups.some((id) => /^y\d+$/.test(id) && (+id.slice(1) < 1930 || +id.slice(1) > 1935))) throw new Error('period filter leaks years');
w.history.replaceState(null, '', PAGE);
w.szdZeitleiste(data);

// language switch without reload
d.querySelector('[data-lang="en"]').click();
console.log('    EN title:', d.getElementById('zl-title').textContent.trim(), '| lanes:', LANES.map((l) => laneChip(l).textContent).join(', '));
if (d.getElementById('zl-title').textContent.trim().indexOf('Timeline') !== 0) throw new Error('language switch did not reach the title');
if (d.documentElement.lang !== 'en') throw new Error('document language not switched');
const enSingle = [...d.querySelectorAll('#zl-content .zl-group')].find((s) => (s.rowsToRender || s.rowBox.children).length === 1);
if (enSingle && enSingle.querySelector('.zl-year-count').textContent !== '1 entry') throw new Error('english plural is wrong');
d.querySelector('[data-lang="de"]').click();

// undated pieces close the list and are not counted in the scale
const sections = [...d.querySelectorAll('#zl-content .zl-group')];
const last = sections.slice(-3).map((s) => s.querySelector('h3').id);
const undatedTotal = LANES.reduce((n, l) => n + data[l].filter((e) => e.datePrecision === 'undated').length, 0);
const undatedShown = sections.filter((s) => s.classList.contains('zl-undated')).reduce((n, s) => n + (s.rowsToRender ? s.rowsToRender.length : s.rowBox.children.length), 0);
console.log('    last groups:', last.join(', '), ' undated:', undatedShown, 'of', undatedTotal);
if (!last[last.length - 1].startsWith('y-undated')) throw new Error('undated pieces are not at the end');
if (undatedShown !== undatedTotal) throw new Error('undated count does not match the data');
const scaleTotal = [...d.querySelectorAll('#zl-axis a')].reduce((n, a) => {
	const m = a.getAttribute('aria-label').match(/\d+/g) || [];
	return n + m.slice(1).reduce((s, x) => s + +x, 0);
}, 0);
console.log('    scale counts', scaleTotal, '= events minus undated', total - undatedTotal, ' years', axisYears[0], 'to', axisYears[axisYears.length - 1]);
if (scaleTotal !== total - undatedTotal) throw new Error('the scale counts undated pieces');

// density switch keeps the biography untouched and the compact class on the body
d.querySelector('[data-density="compact"]').click();
if (!d.body.classList.contains('zl-compact')) throw new Error('compact class missing');
d.querySelector('[data-density="full"]').click();

// the control line folds away on a narrow screen
const toggle = d.getElementById('zl-filter-toggle');
if (!d.getElementById('zl-head').classList.contains('zl-collapsed')) throw new Error('the control line does not start folded');
toggle.click();
if (d.getElementById('zl-head').classList.contains('zl-collapsed') || toggle.getAttribute('aria-expanded') !== 'true') throw new Error('the filter toggle does not open');
toggle.click();
console.log('    all checks passed');
