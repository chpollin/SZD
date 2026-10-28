import { root } from '../harness.mjs';
import { resolve } from 'node:path';
import { JSDOM } from 'jsdom';
import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';

const script = readFileSync(resolve(root, 'js/szd.js'), 'utf8');
const functionNames = [...script.matchAll(/^function ([A-Za-z_][A-Za-z_0-9]*)\s*\(/gm)].map((match) => match[1]);
assert.equal(new Set(functionNames).size, functionNames.length, 'global functions must be defined only once');
const dom = new JSDOM(`<!doctype html><html><head><base href="https://stefanzweig.digital/"></head><body>
<nav class="navbar fixed-top" style="position:fixed;top:0"></nav>
<header class="header-card-nav" style="position:sticky;top:50px"></header>
<a class="language-link" href="/o:szd.lebenskalender/sdef:TEI/get?locale=en"><span>EN</span></a>
<a class="language-link" href="/o:szd.lebenskalender/sdef:TEI/get?locale=de">DE</a>
<a id="jump" href="#SZD.%C3%96">Jump</a>
<div id="SZD.Ö"><button data-toggle="collapse" data-target="#detail"><span class="arrow">▼</span></button><div class="collapse" id="detail">Text</div></div>
<div id="literal%ZZ">Literal percent sign</div>
<button id="second" data-toggle="collapse" href="#detail"><span class="arrow">▼</span></button>
<div class="collapse" id="other">Other panel</div>
<a class="fancybox" href="image.jpg">Image</a>
</body></html>`, { runScripts: 'outside-only', url: 'https://gams-staging.uni-graz.at/o:szd.lebenskalender/sdef:TEI/get?locale=de&mode=timeline&place=Wien&lanes=autographs&lanes=library#SZD.%C3%96' });
const w = dom.window;
const d = w.document;
const scrolls = [];
const offsets = [];
const scrollMargins = [];
const absoluteScrolls = [];
const collapseCalls = [];
const handlers = new Map();
let fancyboxCalls = 0;
let fancyboxOptions;
let bootstrapRegistrations = 0;
let navbarHeight = 50;
let resizeCallback;
const observedNavbars = [];
w.ResizeObserver = class {
    constructor(callback) { resizeCallback = callback; }
    observe(element) { observedNavbars.push(element); }
};
let headerBottom = 170;
let headerTop = 50;
w.HTMLElement.prototype.scrollIntoView = function () { scrolls.push(this.id); scrollMargins.push(this.style.scrollMarginTop); };
w.scrollTo = (x, y) => absoluteScrolls.push([x, y]);
w.scrollBy = (x, y) => offsets.push([x, y]);
d.querySelector('nav').getBoundingClientRect = () => ({ top: 0, bottom: navbarHeight, height: navbarHeight });
d.querySelector('header').getBoundingClientRect = () => ({ top: headerTop, bottom: headerTop + headerBottom - 50, height: headerBottom - 50 });
// jQuery plugins are platform dependencies; observe the calls and feed their documented events.
function jq(node) {
    return {
        on(events, selector, handler) { bootstrapRegistrations++; events.split(' ').forEach((event) => handlers.set(event, handler)); },
        collapse(command) { collapseCalls.push([node.id, command]); },
        fancybox(options) { fancyboxCalls++; fancyboxOptions = options; }
    };
}
jq.fn = { collapse() {}, fancybox() {} };
w.jQuery = jq;
w.eval(script);
await new Promise((done) => w.setTimeout(done, 0));
assert.equal(fancyboxCalls, 1, 'available fancybox plugin is initialized once');
assert.equal(fancyboxOptions.type, 'image', 'GAMS image datastream URLs have no image extension');
assert.equal(d.documentElement.style.getPropertyValue('--szd-navbar-height'), '50px');
assert.deepEqual(observedNavbars, [d.querySelector('nav')]);
w.initSzd();
assert.equal(fancyboxCalls, 1, 'repeated initialization must not bind plugins again');
assert.equal(bootstrapRegistrations, 1, 'Bootstrap listeners are bound exactly once');
assert.equal(observedNavbars.length, 1, 'only one navbar observer is registered');
navbarHeight = 130;
resizeCallback();
assert.equal(d.documentElement.style.getPropertyValue('--szd-navbar-height'), '130px', 'expanded navigation updates the layout variable');
navbarHeight = 60.2;
w.dispatchEvent(new w.Event('resize'));
assert.equal(d.documentElement.style.getPropertyValue('--szd-navbar-height'), '61px', 'resize fallback rounds up to avoid clipping');
navbarHeight = 50;
resizeCallback();
const beforeHashEvent = scrolls.length;
w.dispatchEvent(new w.Event('hashchange'));
assert.equal(scrolls.length, beforeHashEvent + 1, 'one hashchange must cause exactly one jump');
console.log('ok - initialization runs once and navbar height follows observer and resize measurements');

const english = d.querySelector('.language-link');
let destination = new URL(english.href);
assert.equal(destination.host, w.location.host, 'language link must stay on staging despite the base element');
assert.equal(destination.searchParams.get('locale'), 'en');
assert.equal(destination.searchParams.get('place'), 'Wien');
assert.deepEqual(destination.searchParams.getAll('lanes'), ['autographs', 'library']);
assert.equal(destination.hash, w.location.hash);

w.history.replaceState(null, '', 'https://gams-staging.uni-graz.at/o:szd.lebenskalender/sdef:TEI/get?mode=timeline&locale=de&density=compact&person=Zweig#y1920');
d.addEventListener('click', (event) => event.preventDefault());
english.querySelector('span').dispatchEvent(new w.MouseEvent('click', { bubbles: true, cancelable: true }));
destination = new URL(english.href);
assert.equal(destination.searchParams.get('locale'), 'en');
assert.equal(destination.searchParams.get('density'), 'compact');
assert.equal(destination.searchParams.get('person'), 'Zweig');
assert.equal(destination.searchParams.has('place'), false, 'removed filter must not return from a cached link');
assert.equal(destination.searchParams.has('lanes'), false);
assert.equal(destination.hash, '#y1920');
w.history.replaceState(null, '', 'https://gams-staging.uni-graz.at/o:szd.lebenskalender/sdef:TEI/get?mode=timeline&locale=de&from=1910&to=1930#y1910');
english.dispatchEvent(new w.Event('contextmenu', { bubbles: true }));
assert.equal(new URL(english.href).searchParams.get('from'), '1910', 'open-in-new-tab interaction reads current filters');
assert.equal(new URL(english.href).searchParams.has('person'), false);
console.log('ok - language links preserve current query and hash after replaceState, including staging and removed filters');

w.history.replaceState(null, '', 'https://gams-staging.uni-graz.at/o:szd.lebenskalender/sdef:TEI/get?locale=de#SZD.%C3%96');
scrolls.length = 0;
offsets.length = 0;
collapseCalls.length = 0;
w.applyHashOffset();
assert.equal(scrolls.at(-1), 'SZD.Ö');
assert.equal(scrollMargins.at(-1), '170px', 'native scroll margin is set before scrollIntoView');
assert.equal(offsets.length, 0, 'native anchor scrolling must not be followed by a relative correction');
assert.deepEqual(collapseCalls.at(-1), ['detail', 'show']);
headerTop = 220;
w.history.replaceState(null, '', new URL('#other', w.location.href).href);
d.getElementById('SZD.Ö').style.scrollMarginTop = '';
d.getElementById('jump').dispatchEvent(new w.MouseEvent('click', { bubbles: true, cancelable: true }));
assert.equal(d.getElementById('SZD.Ö').style.scrollMarginTop, '170px', 'first native jump accounts for a header that will become sticky');
headerTop = 50;
w.history.replaceState(null, '', new URL('#SZD.%C3%96', w.location.href).href);
w.applyHashOffset();
assert.ok(collapseCalls.every(([, command]) => command === 'show'), 'repeated jumps must never toggle a panel closed');
headerBottom = 90;
w.applyHashOffset();
assert.equal(scrollMargins.at(-1), '90px', 'scroll margin follows the measured header size');
d.querySelector('header').style.display = 'none';
w.applyHashOffset();
assert.equal(scrollMargins.at(-1), '50px', 'hidden header contributes no offset');
w.history.replaceState(null, '', new URL('#literal%ZZ', w.location.href).href);
assert.doesNotThrow(() => w.applyHashOffset());
assert.equal(scrolls.at(-1), 'literal%ZZ');
w.history.replaceState(null, '', new URL('#missing', w.location.href).href);
const beforeMissing = scrolls.length;
assert.doesNotThrow(() => w.applyHashOffset());
assert.equal(scrolls.length, beforeMissing);
for (const source of [null, undefined, '', d.createElement('a'), '#missing']) assert.doesNotThrow(() => w.scrolldown(source));
w.history.replaceState(null, '', new URL('#SZD.%C3%96', w.location.href).href);
w.scrolldown(d.getElementById('jump'));
assert.equal(scrolls.at(-1), 'SZD.Ö');
const fallbackTarget = d.getElementById('SZD.Ö');
fallbackTarget.scrollIntoView = null;
fallbackTarget.getBoundingClientRect = () => ({ top: 400 });
w.applyHashOffset();
assert.deepEqual(absoluteScrolls.at(-1), [0, 350], 'fallback uses one absolute target position with header offset');
delete fallbackTarget.scrollIntoView;
const timeline = d.createElement('div');
timeline.id = 'zl-app';
timeline.innerHTML = '<section id="y1930"></section>';
d.body.appendChild(timeline);
w.history.replaceState(null, '', new URL('#y1930', w.location.href).href);
const beforeTimeline = scrolls.length;
w.applyHashOffset();
assert.equal(scrolls.length, beforeTimeline, 'timeline owns its own hash navigation');
assert.equal(d.getElementById('y1930').style.scrollMarginTop, '', 'global navigation does not override timeline margins');
console.log('ok - hash jumps decode IDs, use visible header geometry, keep panels open and leave timeline scrolling to its own handler');

const detail = d.getElementById('detail');
const trigger = d.querySelector('[data-target="#detail"]');
trigger.dispatchEvent(new w.MouseEvent('click', { bubbles: true }));
assert.equal(trigger.querySelector('.arrow').textContent.trim(), '▼', 'click alone must not invent an expanded state');
detail.classList.add('show');
handlers.get('shown.bs.collapse')({ target: detail });
for (const control of [trigger, d.getElementById('second')]) {
    assert.equal(control.querySelector('.arrow').textContent.trim(), '▲');
    assert.equal(control.getAttribute('aria-expanded'), 'true');
}
handlers.get('hidden.bs.collapse')({ target: d.getElementById('other') });
assert.equal(trigger.querySelector('.arrow').textContent.trim(), '▲', 'unrelated panel events must not change this arrow');
detail.classList.remove('show');
handlers.get('hidden.bs.collapse')({ target: detail });
assert.equal(trigger.querySelector('.arrow').textContent.trim(), '▼');
assert.equal(trigger.getAttribute('aria-expanded'), 'false');
console.log('ok - arrows follow completed Bootstrap state changes');
w.close();

const plain = new JSDOM('<!doctype html><body><div id="target"></div></body>', { runScripts: 'outside-only', url: 'https://example.org/#target' });
plain.window.scrollTo = () => {};
plain.window.eval(script);
await new Promise((done) => plain.window.setTimeout(done, 0));
assert.doesNotThrow(() => plain.window.applyHashOffset(), 'navigation works without optional jQuery plugins');
plain.window.close();
console.log('ok - pages without fancybox or Bootstrap plugins initialize safely');
