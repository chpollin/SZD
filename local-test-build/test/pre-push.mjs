import { readFileSync } from 'node:fs';
import { execFileSync, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { suitesForPaths } from './scope.mjs';
import { root } from '../harness.mjs';

const here = fileURLToPath(new URL('../', import.meta.url));
const paths = new Set();
const updates = readFileSync(0, 'utf8').trim();
for (const line of updates ? updates.split('\n') : []) {
  const [, local, , remote] = line.trim().split(/\s+/);
  if (!/^[a-f0-9]+$/.test(local || '') || !/^[a-f0-9]+$/.test(remote || '')) {
    throw new Error('Invalid pre-push ref input');
  }
  if (/^0+$/.test(local)) continue;
  // A new remote branch has no baseline: check all files in its tree.
  const args = /^0+$/.test(remote)
    ? ['ls-tree', '-r', '--name-only', '-z', local]
    : ['diff', '--no-renames', '--name-only', '-z', remote, local];
  for (const path of execFileSync('git', args, { cwd: root, encoding: 'utf8' }).split('\0').filter(Boolean)) paths.add(path);
}
const routing = spawnSync(process.execPath, ['test/test-scope.test.mjs'], { cwd: here, stdio: 'inherit' });
if (routing.status !== 0) process.exit(routing.status || 1);
const suites = suitesForPaths([...paths]);
if (!suites.length) {
  console.log('No frontend or RDF changes; no rendering build required.');
} else {
  console.log('Pre-push suites: ' + suites.join(', '));
  const result = spawnSync(process.execPath, ['test/run-all.mjs', '--suite', suites.join(',')], { cwd: here, stdio: 'inherit' });
  process.exit(result.status ?? 1);
}
