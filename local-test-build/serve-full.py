# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Serve full-page fixtures and the local SZD assets for browser verification."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen
import argparse
import os
import mimetypes

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("SZD_WWW") or HERE.parents[1] / "ZIMLAB" / "szd").resolve()
CACHE = HERE / "build-full" / "lib-cache"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if path.startswith(("/lib/", "/templates/")):
            target = (CACHE / path.removeprefix("/lib/").lstrip("/")).resolve()
            if not target.is_relative_to(CACHE.resolve()):
                self.send_error(400)
                return
            try:
                if not target.exists():
                    request = Request(
                        "https://gams.uni-graz.at" + path,
                        headers={"User-Agent": "SZD-local-preview/1.0"},
                    )
                    with urlopen(request, timeout=25) as response:
                        content = response.read()
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content)
                content = target.read_bytes()
            except (OSError, ValueError) as error:
                self.send_error(502, str(error))
                return
            self.send_response(200)
            self.send_header(
                "Content-Type",
                mimetypes.guess_type(target.name)[0] or "application/octet-stream",
            )
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return
        if path.startswith("/szd/"):
            self.path = self.path.removeprefix("/szd")
        super().do_GET()

    def translate_path(self, path):
        if urlsplit(path).path.startswith("/local-test-build/"):
            rel = unquote(urlsplit(path).path).removeprefix("/local-test-build/")
            target = (HERE / rel).resolve()
            return str(target) if target.is_relative_to(HERE) else str(HERE / "nonexistent")
        return super().translate_path(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8769)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(
        f"Local preview: http://127.0.0.1:{args.port}/local-test-build/build-full/",
        flush=True,
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
