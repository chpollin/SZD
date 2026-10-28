import { root } from '../harness.mjs';
import { JSDOM } from 'jsdom';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';

import { buildDir as build } from './paths.mjs';

const script = readFileSync(resolve(root, 'js/list-views.js'), 'utf8');
const sourceFor = (page) => new JSDOM(readFileSync(resolve(build, page + '.input.xml'), 'utf8'), { contentType: 'text/xml' }).window.document;
const idOf = (node) => node.getAttribute('xml:id');

function expectedYear(entry, mode, locale) {
    const dates = [...entry.querySelectorAll(mode === 'erwerbsjahr' ? 'fileDesc > sourceDesc > msDesc > history > acquisition date' : 'fileDesc > publicationStmt > date')];
    const years = [...new Set(dates.map((date) => date.getAttribute('when')).filter((value) => /^\d{4}(-\d{2}(-\d{2})?)?$/.test(value || '')).map((value) => value.slice(0, 4)))];
    if (years.length === 1) return years[0];
    if (locale === 'en') return (years.length ? 'Multiple ' : 'No normalized ') + (mode === 'erwerbsjahr' ? 'acquisition' : 'publication') + (years.length ? ' years' : ' year');
    return (years.length ? 'Mehrere ' : 'Ohne normiertes ') + (mode === 'erwerbsjahr' ? 'Erwerbs' : 'Erscheinungs') + (years.length ? 'jahre' : 'jahr');
}

for (const [page, mode] of [['szd-Autographen', 'erwerbsjahr'], ['szd-Bibliothek', 'erscheinungsjahr']]) {
    const source = sourceFor(page);
    const sourceEntries = [...source.querySelectorAll('body > listBibl > biblFull')];
    for (const locale of ['de', 'en']) {
        const dom = new JSDOM(readFileSync(resolve(build, page + (locale === 'en' ? '.en' : '') + '.html'), 'utf8'), {
            runScripts: 'outside-only', url: 'http://localhost:8080/list?locale=' + locale
        });
        const w = dom.window;
        w.eval(script);
        await new Promise((done) => w.setTimeout(done, 0));
        const d = w.document;
        const list = d.querySelector('.list-views');
        assert.ok(list, page + ' missing list');
        const entries = [...list.querySelectorAll('[data-view-sort]')];
        const expectedIds = sourceEntries.map(idOf).sort();
        assert.deepEqual(entries.map((entry) => entry.id).sort(), expectedIds, page + ' must render every source entry exactly once');
        const original = new Map(entries.map((entry) => [entry.id, entry]));
        const links = new Map(entries.map((entry) => [entry.id, [...entry.querySelectorAll('a[href]')].map((link) => link.getAttribute('href'))]));
        const nav = d.querySelector('.header-card-nav ul.list-inline');
        const initialNav = nav.innerHTML;
        const originalGroups = [...list.querySelectorAll('h2,h3')].map((heading) => heading.textContent.trim());
        assert.ok(originalGroups.every(Boolean), page + ' has an empty creator heading');
        if (page === 'szd-Bibliothek') {
            for (const [letter, creator] of [['B', 'Bach, Johann Sebastian'], ['W', 'Wagner, Ernst']]) {
                const anchors = list.querySelectorAll('[id="' + letter + '"]');
                assert.equal(anchors.length, 1, letter + ' needs one anchor despite creators sharing a surname');
                assert.equal(anchors[0].nextElementSibling.querySelector('h3').textContent.trim(), creator, letter + ' must lead to the first creator group');
            }
            // every library title is italic, also in the group without author, whose entries once lacked the PID
            const withoutAuthor = [...list.querySelectorAll('#withoutAuthor .entry')];
            assert.ok(withoutAuthor.length, 'library has no entry without author');
            for (const entry of entries) assert.ok(entry.querySelector('h4 a > i'), entry.id + ': library title not italic');
        }
        sourceEntries.forEach((entry) => assert.equal(original.get(idOf(entry)).getAttribute('data-view-' + mode), expectedYear(entry, mode, locale), idOf(entry) + ' year differs from the TEI field'));
        const selected = list.querySelector('input[type="checkbox"]');
        assert.ok(selected, page + ' must expose a data basket checkbox');
        selected.checked = true;
        const collapse = list.querySelector('.collapse');
        assert.ok(collapse);
        collapse.classList.add('show');
        for (const targetMode of [mode, 'register', mode, 'register']) {
            w.setListView(targetMode);
            assert.deepEqual([...list.querySelectorAll('[data-view-sort]')].map((entry) => entry.id).sort(), expectedIds);
            for (const [id, node] of original) {
                assert.equal(d.getElementById(id), node, id + ' DOM identity changed');
                assert.deepEqual([...node.querySelectorAll('a[href]')].map((link) => link.getAttribute('href')), links.get(id), id + ' links changed');
            }
            assert.ok(selected.isConnected && selected.checked, 'data basket selection was lost');
            assert.ok(collapse.isConnected && collapse.classList.contains('show'), 'expanded entry was lost');
            const ids = [...d.querySelectorAll('[id]')].map((node) => node.id);
            assert.equal(new Set(ids).size, ids.length, 'duplicate rendered IDs');
            const active = d.querySelector('.list-viewswitch [data-mode="' + targetMode + '"]');
            assert.equal(active.getAttribute('aria-selected'), 'true');
            if (targetMode === mode) {
                const labels = [...list.querySelectorAll('h2')].map((node) => node.textContent.trim());
                assert.deepEqual([...nav.querySelectorAll('a')].map((node) => node.textContent.trim()), labels);
                for (const link of nav.querySelectorAll('a')) assert.ok(d.getElementById(link.getAttribute('href').slice(1)), 'jump target missing');
            } else {
                assert.equal(nav.innerHTML, initialNav);
                assert.deepEqual([...list.querySelectorAll('h2,h3')].map((heading) => heading.textContent.trim()), originalGroups);
            }
        }
        console.log('ok - ' + page + ' ' + locale + ': ' + entries.length + ' entries; source years, links, selection and DOM identity preserved');
        w.close();
    }
}

const workSource = sourceFor('szd-Werkliste');
const workIds = [...workSource.querySelectorAll('body > listBibl > bibl')].map(idOf).sort();
for (const locale of ['de', 'en']) {
    const dom = new JSDOM(readFileSync(resolve(build, 'szd-Werkliste' + (locale === 'en' ? '.en' : '') + '.html'), 'utf8'));
    const d = dom.window.document;
    assert.deepEqual([...d.querySelectorAll('.list-group-item[id]')].map((entry) => entry.id).sort(), workIds);
    assert.equal(d.querySelectorAll('.list-viewswitch').length, 0, 'work index must not imply unrecorded categories or years');
    assert.equal(d.querySelectorAll('.list-group-item h3 a[href]').length, workIds.length);
    assert.equal(d.querySelectorAll('h4').length, 0);
    assert.equal(d.querySelectorAll('span h3').length, 0);
    for (const link of d.querySelectorAll('.list-group-item h3 a[href]')) assert.ok(link.getAttribute('href').endsWith('&locale=' + locale));
    console.log('ok - szd-Werkliste ' + locale + ': ' + workIds.length + ' source entries, heading hierarchy and search links retained');
    dom.window.close();
}
