// Reactivated dating block in szd-Konvolut.xsl, checked against the real Konvolut TEI the
// page was built from (szd-Konvolut.input.xml next to szd-Konvolut.html in SZD_TEST_BUILD_DIR,
// by default the Konvolut named in snapshot.manifest.json).
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { buildDir } from './paths.mjs';

const html = readFileSync(resolve(buildDir, 'szd-Konvolut.html'), 'utf8');
const tei = readFileSync(resolve(buildDir, 'szd-Konvolut.input.xml'), 'utf8');
const locale = (html.match(/<html[^>]*\slang="([^"]*)"/) || [, 'de'])[1];

const entries = [...html.matchAll(/<h4 class="card-title text-left col-9 small">(.*?)<\/h4>/gs)]
	.map((m) => m[1].replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim().replace(/^▼\s*/, ''))
	.map((text) => {
		const parts = text.split(' | ');
		return { text, title: parts[0], date: parts.length >= 3 ? parts[1] : null };
	});

// every piece of the konvolut is rendered
const pieces = (tei.match(/<biblFull\b/g) || []).length;
assert.equal(entries.length, pieces, 'entries rendered');

const dated = entries.filter((e) => e.date);
assert.ok(dated.length > 100, 'hardly any entry carries a dating: ' + dated.length);

// the machine date must not reach the page
const raw = dated.filter((e) => /^\d{4}-\d{2}(-\d{2})?$/.test(e.date));
assert.equal(raw.length, 0, 'machine date on the page: ' + raw.slice(0, 3).map((e) => e.text).join(' | '));

// and no entry may say its dating twice
const twice = dated.filter((e) => e.title.includes(e.date));
assert.equal(twice.length, 0, 'dating twice: ' + twice.slice(0, 3).map((e) => e.text).join(' | '));

// pieces whose TEI carries @when must show a formatted date
const formatted = dated.filter((e) => locale === 'en'
	? /^\d{1,2} [A-Z][a-z]+ \d{4}$|^[A-Z][a-z]+ \d{4}$|^\d{4}$/.test(e.date)
	: /^\d{2}\.\d{2}\.\d{4}$|^\d{2}\.\d{4}$|^\d{4}$/.test(e.date));
assert.ok(formatted.length > 100, 'hardly any formatted date: ' + formatted.length);

console.log('OK  locale:', locale, ' entries:', entries.length, ' with a dating:', dated.length,
	' of those formatted from @when:', formatted.length);
console.log('    sample:', dated.slice(0, 3).map((e) => e.date).join(' | '),
	'--', formatted.slice(0, 3).map((e) => e.date).join(' | '));
