const frontend = ['unit', 'proto', 'pages'];

// Paths are gams-www paths from Git, not shell-expanded user input. Unknown code needs both gates.
export function suitesForPaths(paths) {
  const suites = new Set();
  for (const path of paths) {
    if (/\.md$|(^|\/)LICENSE$/.test(path)) continue;
    if (path === 'szd-TORDF.xsl') {
      suites.add('rdf');
    } else if (/^(css|js|fonts|icons|img|data\/lebenskalender)\//.test(path) || /^szd-.*\.xsl$/.test(path)) {
      frontend.forEach((suite) => suites.add(suite));
    } else {
      [...frontend, 'rdf'].forEach((suite) => suites.add(suite));
    }
  }
  return [...frontend, 'rdf'].filter((suite) => suites.has(suite));
}
