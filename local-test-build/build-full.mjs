import { copyFileSync } from 'node:fs';
import { resolve, basename } from 'node:path';
import { here, materialize, readStylesheets, render } from './harness.mjs';

// Full page with shell and template library, from the working tree. snapshot.mjs builds
// every page type from a chosen revision.
const [pageArg, sourceArg, locale = 'de', mode = ''] = process.argv.slice(2);
if (!pageArg || !sourceArg || !['de', 'en'].includes(locale)) {
  throw new Error('Usage: node build-full.mjs <page> <source.xml> [de|en] [mode]');
}
const page = basename(pageArg).replace(/\.xsl$/, '');
const out = resolve(process.env.SZD_TEST_BUILD_DIR || resolve(here, 'build-full'));
materialize(out, readStylesheets('worktree'), process.env.SZD_LANGUAGES_FILE ? { languages: resolve(process.env.SZD_LANGUAGES_FILE) } : {});
const input = resolve(sourceArg);
const fixturePath = resolve(out, page + '.input.xml');
if (input !== fixturePath) { copyFileSync(input, fixturePath); }
try {
  console.log('OK full page: ' + await render({ xslDir: out, page, input: fixturePath, out, locale, mode }));
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
