#!/usr/bin/env bash
# Run a single SZD page stylesheet locally against real GAMS data, without the
# GAMS runtime. The page XSLT includes stub-lib.xsl instead of its two production
# includes, and the stub imports both, so only the page shell is simplified.
#
# Usage:
#   bash run.sh <PageStylesheet> <data-url-or-file> [locale] [mode]
#     <PageStylesheet>   name of the page XSLT in the repo root, with or without
#                        .xsl (e.g. szd-Facsimiles)
#     <data-url-or-file> a GAMS datastream URL or a local XML file
#     [locale]           de (default) or en
#     [mode]             value of the mode parameter for a subview of the page
#                        (e.g. timeline for the Zeitleiste of the biography)
#
# Outputs are named after the stylesheet (build/<Stylesheet>.html and, for a URL,
# build/<Stylesheet>.input.xml), so building one page does not overwrite another.
# With a mode the page output carries it (build/<Stylesheet>.<mode>.html), so a
# subview does not overwrite the default view.
#
# Example:
#   bash run.sh szd-Facsimiles \
#     "https://gams.uni-graz.at/archive/objects/context:szd.facsimiles.korrespondenzen/datastreams/METADATA/content"
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "${SZD_WWW:-$here/../../ZIMLAB/szd}" && pwd)"
build="$here/build"

xsl_name="${1:?usage: bash run.sh <PageStylesheet> <data-url-or-file> [locale] [mode]}"
xsl_name="${xsl_name%.xsl}"
src="${2:?missing data url or file}"
locale="${3:-de}"
mode="${4:-}"
out_name="$xsl_name${mode:+.$mode}"

mkdir -p "$build"

# fetch data if a URL was given
if [[ "$src" == http* ]]; then
    echo "Fetching $src"
    curl -sL "$src" -o "$build/$xsl_name.input.xml"
else
    # keep a local input next to the output as well, so a test reads its expectations
    # from the file the page was built from
    [[ "$src" -ef "$build/$xsl_name.input.xml" ]] || cp "$src" "$build/$xsl_name.input.xml"
fi
data="$build/$xsl_name.input.xml"

# every project stylesheet goes to build/ with its GAMS loads redirected to local data,
# the same materialisation build-full.mjs and snapshot.mjs use
(cd "$here" && node --input-type=module -e "import { materialize, readStylesheets } from './harness.mjs'; materialize(process.argv[1], readStylesheets('worktree'));" "$build")
# the page includes stub-lib.xsl instead of its two production includes; the stub
# imports both, so only the page shell differs from production
sed -E \
    -e 's#<xsl:include href="szd-static\.xsl"/>#<xsl:include href="stub-lib.xsl"/>#' \
    -e '\#<xsl:include href="szd-Templates\.xsl"/>#d' \
    "$build/$xsl_name.xsl" > "$build/$xsl_name.test.xsl"
cp "$here/stub-lib.xsl" "$build/stub-lib.xsl"

# prefer a locally installed xslt3, fall back to npx
if [[ -x "$here/node_modules/.bin/xslt3" ]]; then
    xslt3="$here/node_modules/.bin/xslt3"
else
    xslt3="npx --yes xslt3"
fi

# mode is only passed when given, so a run without it leaves $mode unbound in the
# stylesheet, exactly as before
params=("locale=$locale")
if [[ "$xsl_name" == "szd-Facsimiles" ]]; then
    index="${SZD_DATA_ROOT:-$here/..}/data/Correspondence/SZDKOR.xml"
    cp "$index" "$build/korrespondenzen-index.xml"
    params+=("correspondence-index-uri=korrespondenzen-index.xml")
fi
if [[ -n "$mode" ]]; then
    params+=("mode=$mode")
fi

$xslt3 -xsl:"$build/$xsl_name.test.xsl" -s:"$data" -o:"$build/$out_name.html" "${params[@]}"
echo "Done -> $build/$out_name.html"
