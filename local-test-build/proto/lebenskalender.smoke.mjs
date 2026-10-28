// Smoke test of the Lebenskalender prototype against the real TEI in build/.
import { JSDOM } from 'jsdom';
import { readFileSync, existsSync } from 'node:fs';

// build/lebenskalender.xml is fetched by hand with run.sh (proto/README.md); without it the test counts as skipped
if (!existsSync(new URL('../build/lebenskalender.xml', import.meta.url))) { console.log('SKIP build/lebenskalender.xml is not fetched, see proto/README.md'); process.exit(2); }
const html = readFileSync(new URL('./lebenskalender-proto.html', import.meta.url), 'utf8');
const xml = readFileSync(new URL('../build/lebenskalender.xml', import.meta.url), 'utf8');
const dom = new JSDOM(html, { runScripts: 'dangerously' });
const w = dom.window;
const n = w.lebenskalenderInit(xml);
const d = w.document;
const years = d.querySelectorAll('h2.year').length;
const arts = d.querySelectorAll('article.ev').length;
const links = d.querySelectorAll('article.ev .text a[href*="person_search"]').length;
const chips = [...d.querySelectorAll('#places .chip')].map(c => c.firstChild.textContent + ':' + c.querySelector('small').textContent);
const scale = d.querySelectorAll('#scale a').length;
const noPlace = [...d.querySelectorAll('article.ev')].filter(a => !a.querySelector('.where').textContent).map(a => a.id);
console.log('OK  events:', n, ' years:', years, ' articles:', arts, ' person links:', links, ' scale cells:', scale);
console.log('    places:', chips.join(' | '));
console.log('    without place:', noPlace.length, noPlace.slice(0, 6).join(','));
d.querySelectorAll('#places .chip')[1].click();
const shown = d.querySelectorAll('article.ev').length, hiddenYears = d.querySelectorAll('h2.year[hidden]').length;
console.log('    after filter on first place: articles', shown, ' hidden years', hiddenYears);
d.querySelector('[data-lang="en"]').click();
console.log('    EN heading sample:', d.querySelector('article.ev .where').textContent, '|', d.querySelector('article.ev .when').textContent, '| title', d.getElementById('title').textContent);
if (arts !== n || shown >= n || links === 0) throw new Error('unexpected counts');
