import { resolve } from 'node:path';
import { here } from '../harness.mjs';

// The one place where tests find their builds. SZD_TEST_BUILD_DIR holds the full pages
// (default: the working-tree snapshot that test/run-all.mjs builds), SZD_RDF_BUILD_DIR the
// RDF builds under one folder per label (default build-rdf).
export const buildDir = resolve(process.env.SZD_TEST_BUILD_DIR || resolve(here, 'build-snap/worktree'));
export const rdfDir = resolve(process.env.SZD_RDF_BUILD_DIR || resolve(here, 'build-rdf'));
export const rdfCurrentDir = resolve(process.env.SZD_RDF_CURRENT_DIR || resolve(rdfDir, 'current'));
export const rdfBaselineDir = resolve(process.env.SZD_RDF_BASELINE_DIR || resolve(rdfDir, 'baseline'));
