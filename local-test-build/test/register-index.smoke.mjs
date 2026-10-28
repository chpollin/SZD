// The four registers rendered by szd-Index.xsl as full pages: Personen, Standorte and
// Werkindex and Organisationen through their wrapper stylesheets.
// Checks ids, jump targets, view switch, search links, the fields of each register, the menu item and
// the country arrangement of the two listOrg registers with the real list-views.js.
import { root } from '../harness.mjs';
import { JSDOM } from 'jsdom';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';

import { buildDir as build } from './paths.mjs';
const script = readFileSync(resolve(root, 'js/list-views.js'), 'utf8');
const registers = [
    { page: 'szd-Personenliste', list: 'listPerson > person', pid: 'o:szd.personen', search: 'query:szd.person_search', modes: [] },
    { page: 'szd-Standortliste', list: 'listOrg > org', pid: 'o:szd.standorte', search: 'query:szd.standort_search', modes: ['register', 'land'] },
    // a repository links the standort search, any other body the person search with its own id
    { page: 'szd-Organisationen', list: 'listOrg > org', pid: 'o:szd.organisation', search: 'by-role', modes: ['register', 'land'] },
    { page: 'szd-Werkliste', list: 'listBibl > bibl', pid: 'o:szd.werkindex', search: 'query:szd.work_search', modes: [] }
];
const focusable = (node) => !node.hasAttribute('disabled') && node.getAttribute('tabindex') !== '-1' && (node.tagName === 'BUTTON' || node.hasAttribute('href'));
const uniqueIds = (d, label) => {
    const ids = [...d.querySelectorAll('[id]')].map((node) => node.id);
    assert.equal(new Set(ids).size, ids.length, label + ': duplicate ids');
    assert.ok(!ids.includes(''), label + ': empty id');
};

for (const register of registers) {
    const source = new JSDOM(readFileSync(resolve(build, register.page + '.input.xml'), 'utf8'), { contentType: 'text/xml' }).window.document;
    const sourceEntries = [...source.querySelectorAll('body > ' + register.list)];
    const sourceIds = sourceEntries.map((entry) => entry.getAttribute('xml:id')).sort();
    for (const locale of ['de', 'en']) {
        const label = register.page + ' ' + locale;
        const dom = new JSDOM(readFileSync(resolve(build, register.page + (locale === 'en' ? '.en' : '') + '.html'), 'utf8'), {
            runScripts: 'outside-only', url: 'http://localhost:8080/' + register.pid + '/sdef:TEI/get?locale=' + locale
        });
        const w = dom.window;
        const d = w.document;
        assert.equal(d.documentElement.lang, locale);
        uniqueIds(d, label);

        const entries = [...d.querySelectorAll('.list-group-item[id]')];
        assert.deepEqual(entries.map((entry) => entry.id).sort(), sourceIds, label + ': every source entry rendered exactly once');
        for (const entry of entries) {
            const heading = entry.querySelector('h3');
            assert.ok(heading && heading.textContent.trim(), entry.id + ': heading missing');
            const link = heading.querySelector('a[href]');
            let search = register.search;
            let target = encodeURIComponent(register.pid) + '%23' + entry.id;
            if (search === 'by-role') {
                const repository = sourceEntries.find((org) => org.getAttribute('xml:id') === entry.id).querySelector('idno[type="SZDSTA"]');
                search = repository ? 'query:szd.standort_search' : 'query:szd.person_search';
                target = repository ? encodeURIComponent('o:szd.standorte') + '%23' + repository.textContent.trim() : target;
            }
            assert.ok(link && link.getAttribute('href').includes(search) && link.getAttribute('href').includes(target) && link.getAttribute('href').endsWith('&locale=' + locale), entry.id + ': search link');
            for (const list of entry.querySelectorAll('dl')) {
                assert.ok(list.classList.contains('szd-metadata'));
                for (const row of list.children) {
                    assert.equal(row.tagName, 'DIV');
                    assert.deepEqual([...row.children].map((node) => node.tagName), ['DT', 'DD'], entry.id + ': malformed metadata row');
                    assert.ok(row.firstElementChild.textContent.trim() && row.lastElementChild.textContent.trim(), entry.id + ': empty metadata cell');
                }
            }
            assert.ok(!entry.textContent.includes('SZDPER.'), entry.id + ': superseded person ids must stay hidden');
        }

        // sticky header: every jump target exists and every jump link and tab is focusable
        const header = d.querySelector('.header-card-nav');
        assert.ok(header, label + ': sticky header');
        const jumps = [...header.querySelectorAll('nav.header-jump a[href^="#"]')];
        assert.ok(jumps.length, label + ': jump navigation empty');
        for (const jump of jumps) {
            assert.ok(d.getElementById(decodeURIComponent(jump.getAttribute('href').slice(1))), label + ': jump target ' + jump.getAttribute('href') + ' missing');
            assert.ok(focusable(jump), label + ': jump link not focusable');
        }
        const tabs = [...header.querySelectorAll('.list-viewswitch [data-mode]')];
        assert.deepEqual(tabs.map((tab) => tab.getAttribute('data-mode')), register.modes, label + ': view switch modes');
        for (const tab of tabs) {
            assert.equal(tab.tagName, 'BUTTON');
            assert.ok(tab.textContent.trim(), label + ': unnamed tab');
        }

        // menu item in the INDEX dropdown, between Standorte and Werke
        const menu = [...d.querySelectorAll('a.dropdown-item')];
        const organisations = menu.find((item) => item.getAttribute('href') === '/o:szd.organisation/sdef:TEI/get?locale=' + locale);
        assert.ok(organisations, label + ': Organisationen menu item missing');
        assert.equal(organisations.textContent.trim(), locale === 'en' ? 'Organisations' : 'Organisationen');
        const around = menu.slice(menu.indexOf(organisations) - 1, menu.indexOf(organisations) + 2).map((item) => item.getAttribute('href'));
        assert.deepEqual(around, ['/o:szd.standorte/sdef:TEI/get?locale=' + locale, organisations.getAttribute('href'), '/o:szd.werkindex/sdef:TEI/get?locale=' + locale]);

        // register-specific fields, checked against the source entries
        if (register.pid === 'o:szd.personen') {
            const first = d.getElementById('SZDPER.1');
            assert.equal(first.querySelector('h3 a').textContent.trim().replace(/\s+$/, ''), 'Abraham, Pierre');
            assert.equal(first.querySelector('h3 span').textContent, '(1892–1974)');
            assert.ok(first.querySelector('a[href="http://d-nb.info/gnd/12490310X"][title="GND"]'));
            assert.ok(first.querySelector('a[href="http://www.wikidata.org/entity/Q3383636"]'));
            assert.ok(first.querySelector('a[href="https://de.wikipedia.org/wiki/Pierre_Abraham"]'));
            const unknown = sourceEntries.find((entry) => entry.querySelector('forename[cert="unknown"]'));
            assert.ok(d.getElementById(unknown.getAttribute('xml:id')).querySelector('h3 a').textContent.includes(locale === 'en' ? ', [unknown]' : ', [unbekannt]'));
            assert.equal(d.querySelectorAll('.list-group-item dl').length, 0);
        }
        if (register.pid === 'o:szd.standorte') {
            const first = d.getElementById('SZDSTA.1');
            assert.equal(first.querySelector('h3 a').childNodes[0].textContent, 'Literaturarchiv Salzburg');
            // the settlement is already part of the name and is not repeated
            assert.equal(first.querySelector('h3 span.szd-place').textContent, '(Österreich)');
            assert.ok(first.querySelector('a[href="http://d-nb.info/gnd/1047605287"][title="GND"]'));
            assert.ok(first.querySelector('.col-2 a[href="https://www.uni-salzburg.at/index.php?id=72"] i.fa-link'));
            const privat = d.getElementById('SZDSTA.12');
            assert.equal(privat.querySelector('h3 a').childNodes[0].textContent, locale === 'en' ? 'Private collection, Germany' : 'Privatbesitz, Deutschland');
            assert.equal(privat.querySelector('h3 span.szd-place'), null, 'the country is already part of the name');
            assert.equal(d.querySelectorAll('.list-group-item dl').length, 0, 'place and country stand in the heading line');
        }
        if (register.pid === 'o:szd.organisation') {
            const first = d.getElementById('SZDORG.1');
            assert.equal(first.querySelector('h3 a').textContent.trim(), 'Adolf Haslinger Literaturstiftung im Literaturarchiv Salzburg');
            assert.equal(first.querySelector('h3 span.szd-place').textContent, '(Österreich)');
            assert.ok(first.querySelector('.col-2 a[href="http://d-nb.info/gnd/1047604132"][title="GND"]'));
            assert.ok(first.querySelector('.col-2 a[href="http://ahl.sbg.ac.at/"] i.fa-link'));
            assert.ok(first.querySelector('.col-2 a.szd-repository-pin[href="/o:szd.standorte/sdef:TEI/get?locale=' + locale + '#SZDSTA.17"] i.fa-map-marker-alt'), 'pin to the Standorte entry');
            const withLocation = sourceEntries.filter((entry) => entry.querySelector('idno[type="SZDSTA"]'));
            assert.equal(d.querySelectorAll('.col-2 a.szd-repository-pin').length, withLocation.length, 'one pin per repository');
            assert.equal(d.querySelectorAll('.list-group-item dl').length, 0, 'no metadata rows, place and country stand in the heading line');
            const plain = d.getElementById('SZDORG.2');
            assert.equal(plain.querySelector('.szd-repository-pin'), null, 'no pin for a body that is not a repository');
            assert.ok(plain.querySelector('.col-2 a[href="http://d-nb.info/gnd/2131189-4"]'));
            const variants = d.getElementById('SZDORG.4');
            assert.equal(variants.querySelector('h3').textContent.trim(), 'Authors Guild', 'the variant name is not the heading');
        }
        if (register.pid === 'o:szd.werkindex') {
            const first = d.getElementById('SZDWRK.1');
            assert.equal(first.querySelector('h3 a').childNodes[0].textContent.trim(), 'Clarissa');
            assert.ok(first.querySelector('.col-2 a[href="http://d-nb.info/gnd/1207786888"][title="GND"]'));
            assert.equal(d.querySelectorAll('.list-viewswitch').length, 0);
        }

        // the country arrangement with the real script: regroup, jump targets, focus, back
        if (register.modes.length) {
            w.eval(script);
            await new Promise((done) => w.setTimeout(done, 0));
            const list = d.querySelector('.list-views');
            const nav = header.querySelector('nav.header-jump ul');
            const originalNav = nav.innerHTML;
            const original = new Map(entries.map((entry) => [entry.id, entry]));
            assert.equal(typeof w.setListView, 'function');
            w.setListView('land');
            uniqueIds(d, label + ' land');
            const groups = [...list.querySelectorAll('h2')].map((h) => h.textContent);
            const countries = [...new Set(sourceEntries.map((entry) => (entry.querySelector('country') || { textContent: '' }).textContent.trim()))];
            assert.equal(groups.length, countries.length, label + ': one group per country');
            assert.equal(groups.at(-1), countries.includes('') ? (locale === 'en' ? 'No country given' : 'Ohne Landesangabe') : groups.at(-1));
            assert.ok(!list.querySelector('.col-10 > .list-group-item'), label + ': entries must not be wrapped in a column');
            for (const jump of nav.querySelectorAll('a[href^="#"]')) {
                assert.ok(d.getElementById(jump.getAttribute('href').slice(1)), label + ': country jump target missing');
                assert.equal(jump.getAttribute('title'), null, label + ': stale letter title on a country link');
                assert.ok(focusable(jump));
            }
            assert.deepEqual([...nav.querySelectorAll('a')].map((a) => a.textContent), groups);
            for (const [id, node] of original) { assert.equal(d.getElementById(id), node, id + ': DOM identity changed'); }
            const active = header.querySelector('.list-viewswitch [data-mode="land"]');
            assert.equal(active.getAttribute('aria-selected'), 'true');
            assert.equal(header.querySelectorAll('[role="tab"][aria-pressed]').length, 0, 'tabs carry aria-selected, not aria-pressed');
            assert.equal(active.tabIndex, 0, 'active tab reachable by keyboard');
            active.focus();
            active.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'ArrowLeft', bubbles: true }));
            assert.equal(d.activeElement.getAttribute('data-mode'), 'register', 'arrow keys move between tabs');
            assert.equal(nav.innerHTML, originalNav, label + ': default navigation restored');
            assert.deepEqual([...list.querySelectorAll('.list-group-item[id]')].map((entry) => entry.id), entries.map((entry) => entry.id), label + ': default order restored');
        }
        console.log('ok - ' + label + ': ' + entries.length + ' entries, ' + jumps.length + ' jump targets, ' + tabs.length + ' tabs, menu item present');
        w.close();
    }
}
