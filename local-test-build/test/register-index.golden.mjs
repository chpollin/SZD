// Golden comparison of the four indexes. The golden pages are not stored: the snapshot
// driver renders them from the stylesheets of a named commit (SZD_GOLDEN_REV, default
// HEAD) with the same data, and the candidates are the full-page builds of the working
// tree (SZD_TEST_BUILD_DIR). Apart from asset release metadata, pages must be byte-identical. All failures are
// collected; for a differing page the entry ids and the order are compared as well, so
// the report says whether entries went missing or only moved.
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { JSDOM } from 'jsdom';
import { buildSnapshot, report } from '../snapshot.mjs';
import { buildDir } from './paths.mjs';

const rev = process.env.SZD_GOLDEN_REV || 'HEAD';
const names = ['szd-Personenliste', 'szd-Standortliste', 'szd-Organisationen', 'szd-Werkliste'];
const missing = names.flatMap((name) => [name + '.html', name + '.en.html']).filter((file) => !existsSync(resolve(buildDir, file)));
if (missing.length) {
  console.log(`FAIL not built in ${buildDir}: ${missing.join(', ')} (node snapshot.mjs --only ${names.join(',')})`);
  process.exit(1);
}
const golden = await buildSnapshot({ rev, only: names.join(','), quiet: true });
// Asset URLs and the explicit tokens link are checked by asset-version.smoke.mjs.
// Preserve byte comparison for all remaining markup, including the rest of the head.
const withoutAssetRelease = (html) => html
  .replace(/<link\b[^>]*href="\/szd\/css\/tokens\.css\?v=[^"]+"[^>]*\/?>/g, '')
  .replace(/((?:src|href)="\/szd\/(?:css|js)\/[^"?]+)\?v=[^"&]+"/g, '$1"')
  .replace(/ data-asset-version="[^"]+"/g, '');
const result = { compared: names.length * 2, differences: [], notes: ['Asset release metadata is verified separately; all remaining markup is compared byte for byte.'] };
for (const name of names) {
  for (const suffix of ['.html', '.en.html']) {
    const file = name + suffix;
    if (withoutAssetRelease(readFileSync(resolve(golden, file), 'utf8')) !== withoutAssetRelease(readFileSync(resolve(buildDir, file), 'utf8'))) {
      result.differences.push(file + ': markup differs beyond asset release metadata');
    }
  }
}
report(result, golden, buildDir);
const ids = (file, dir) => [...new JSDOM(readFileSync(resolve(dir, file), 'utf8')).window.document.querySelectorAll('.list-group-item[id]')].map((e) => e.id);
for (const difference of result.differences) {
  const file = difference.slice(0, difference.indexOf(':'));
  if (!existsSync(resolve(golden, file)) || !existsSync(resolve(buildDir, file))) { continue; }
  const [before, after] = [ids(file, golden), ids(file, buildDir)];
  const gone = before.filter((id) => !after.includes(id));
  const added = after.filter((id) => !before.includes(id));
  const kept = before.filter((id) => after.includes(id));
  const moved = after.filter((id) => kept.includes(id)).filter((id, i) => id !== kept[i]).length;
  console.log(`  ${file}: ${gone.length} entries gone${gone.length ? ' (' + gone.slice(0, 10).join(' ') + ')' : ''}, ${added.length} added${added.length ? ' (' + added.slice(0, 10).join(' ') + ')' : ''}, ${moved} moved`);
}
process.exit(result.differences.length ? 1 : 0);
