#!/usr/bin/env bash
# Serve gams-www as site root and this harness under /local-test-build/ on :8080, so a built
# page can load the local js under test. Same server as serve-full.py, on the old port.
#   bash serve.sh
#   http://localhost:8080/local-test-build/build/szd-Facsimiles.html
set -euo pipefail
cd "$(dirname "$0")"
echo "Open: http://localhost:8080/local-test-build/build/<Stylesheet>.html"
exec python serve-full.py --port 8080
