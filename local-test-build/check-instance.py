"""Read-only check of a GAMS instance against gams-objects.toml.

For every object of the manifest it reads the STYLESHEET, TORDF and QUERY datastreams over
their public URLs, compares them with the expected reference or template, checks that the
RDF datastream of every TEI object exists, and with --data compares the TEI_SOURCE (and the
static datastreams of context:szd) with the files of the data repository. It never logs in
and never writes to GAMS, and it ends with an operator checklist of the deviations.

    python check-instance.py --instance production [--data] [--skip-konvolute] [--pids o:szd.werke ...]
    python check-instance.py --instance staging --checklist checklist.md

Deviations are grouped by what the operator has to do. The data root is SZD_DATA_ROOT or
the `root` of the manifest, relative to the repository root.
"""
import argparse
import os
import re
import sys
import time
import tomllib
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
MANIFEST = HERE / 'gams-objects.toml'
TEI_NS = '{http://www.tei-c.org/ns/1.0}'
PAUSE = 0.15
TIMEOUT = 60


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


opener = urllib.request.build_opener(NoRedirect)
cache = {}


def fetch(url, method='GET'):
    """Status, Location header and body of one request, without following redirects."""
    if (method, url) in cache:
        return cache[(method, url)]
    time.sleep(PAUSE)
    req = urllib.request.Request(url, method=method, headers={'User-Agent': 'szd-check-instance'})
    try:
        with opener.open(req, timeout=TIMEOUT) as res:
            result = (res.status, res.headers.get('Location'), res.read() if method == 'GET' else b'')
    except urllib.error.HTTPError as e:
        body = e.read() if method == 'GET' else b''
        result = (e.code, e.headers.get('Location'), body)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        result = (0, None, str(e).encode())
    cache[(method, url)] = result
    return result


def reference(host, pid, dsid):
    """The redirect target of an R datastream, or a status that explains why there is none."""
    status, location, body = fetch(f'{host}/archive/objects/{pid}/datastreams/{dsid}/content')
    if status in (301, 302, 303, 307, 308) and location:
        return 'redirect', location
    if status == 400 and b'Illegal character' in body:
        return 'illegal', None
    if status == 200:
        return 'inline', body
    return f'http {status}', None


def normalise(text):
    """Canonical XML where the text parses, otherwise the text with line endings and
    declaration removed. Cirilo re-serialises an ingested file with its own attribute order
    and indentation, so only the canonical form tells content changes apart."""
    text = text.decode('utf-8', 'replace') if isinstance(text, bytes) else text
    text = text.lstrip('﻿').replace('\r\n', '\n')
    try:
        # Cirilo and the data scripts also re-wrap mixed text, so whitespace runs collapse.
        return re.sub(r'\s+', ' ', ET.canonicalize(text, strip_text=True))
    except ET.ParseError:
        text = re.sub(r'^<\?xml[^>]*\?>\s*', '', text)
        return '\n'.join(line.rstrip() for line in text.strip().split('\n'))


def squash(text):
    return re.sub(r'\s+', ' ', normalise(text)).strip()


def expand_pids(entry, data_root):
    pids = list(entry.get('pids', []))
    source = entry.get('pids_from')
    if source:
        root = Path(os.environ.get(source['root_env'], '') or (REPO / source['root'])).resolve() if source.get('root_env') else data_root
        files = sorted((root / source['dir']).glob(source['glob']))
        pids += [source['prefix'] + f.stem for f in files]
    excluded = set(entry.get('exclude', []))
    return [p for p in pids if p not in excluded]


def data_pids(data_root):
    """PID of every TEI file of the data repository, from publicationStmt/idno[@type='PID']."""
    found = {}
    for file in sorted((data_root / 'data').rglob('*.xml')):
        try:
            for event, el in ET.iterparse(file, events=('end',)):
                if el.tag == f'{TEI_NS}publicationStmt':
                    idno = el.find(f'{TEI_NS}idno[@type="PID"]')
                    if idno is not None and idno.text:
                        found[idno.text.strip()] = file
                    break
        except ET.ParseError:
            continue
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--instance', required=True, choices=['production', 'staging'])
    parser.add_argument('--data', action='store_true', help='compare TEI_SOURCE and the static datastreams with the data repository')
    parser.add_argument('--skip-konvolute', action='store_true', help='leave out the objects expanded from the data repository')
    parser.add_argument('--pids', nargs='*', help='check only these PIDs')
    parser.add_argument('--checklist', help='write the operator checklist to this Markdown file')
    args = parser.parse_args()

    manifest = tomllib.loads(MANIFEST.read_text(encoding='utf-8'))
    base = manifest['instances'][args.instance]['base'].rstrip('/') + '/'
    host = re.match(r'https?://[^/]+', base).group(0)
    generic = manifest.get('generic', [])
    data_root = Path(os.environ.get('SZD_DATA_ROOT') or (REPO / manifest.get('data_root', '.'))).resolve()
    deviations = []
    counts = {'objects': 0, 'ok': 0}

    def note(kind, pid, text):
        deviations.append((kind, pid, text))

    resolved = {}
    objects = []
    for entry in manifest['objects']:
        if args.skip_konvolute and 'pids_from' in entry:
            continue
        for pid in expand_pids(entry, data_root):
            if args.pids and pid not in args.pids:
                continue
            objects.append((pid, entry))

    for pid, entry in objects:
        counts['objects'] += 1
        clean = True
        status, _, _ = fetch(f'{host}/archive/objects/{pid}?format=xml')
        if status == 404:
            note('missing object', pid, 'object does not exist on this instance')
            print(f'MISSING {pid}')
            continue
        for dsid in ('STYLESHEET', 'TORDF'):
            expected = entry.get(dsid)
            if expected is None:
                continue
            kind, target = reference(host, pid, dsid)
            if kind == 'illegal':
                note('reference with illegal character', pid, f'{dsid} answers HTTP 400, trailing character after .xsl')
                clean = False
                continue
            if kind != 'redirect':
                note('reference unreadable', pid, f'{dsid}: {kind}')
                clean = False
                continue
            if isinstance(expected, dict) and 'inherit' in expected:
                want = resolved.get((expected['inherit'], dsid))
                if want is None:
                    _, want = reference(host, expected['inherit'], dsid)
                    resolved[(expected['inherit'], dsid)] = want
            elif isinstance(expected, dict) and 'gams' in expected:
                want = expected['gams']
            else:
                want = base + expected
            resolved[(pid, dsid)] = target
            if want is None:
                note('reference unreadable', pid, f'{dsid}: inherited value could not be read')
                clean = False
            elif target == want or (isinstance(expected, dict) and 'gams' in expected and want in target):
                pass
            elif target.replace('http://', 'https://', 1) == want:
                note('reference over http', pid, f'{dsid} = {target}')
            elif any(g in target for g in generic):
                note('generic stylesheet', pid, f'{dsid} = {target}')
                clean = False
            else:
                note('wrong reference', pid, f'{dsid} = {target}, expected {want}')
                clean = False
            if target and target.startswith('http') and 'cirilo:' not in target:
                tstatus, tlocation, _ = fetch(target, 'HEAD')
                if tstatus in (301, 302, 307, 308) and tlocation:
                    tstatus, _, _ = fetch(tlocation, 'HEAD')
                if tstatus != 200:
                    note('dead reference target', pid, f'{dsid} target {target} answers HTTP {tstatus}')
                    clean = False
        query = entry.get('QUERY')
        if query:
            kind, body = reference(host, pid, 'QUERY')
            template = (HERE / query['template']).read_text(encoding='utf-8')
            if kind != 'inline':
                note('query unreadable', pid, f'QUERY: {kind}')
                clean = False
            elif squash(body) != squash(template):
                note('query differs from template', pid, f'QUERY differs from {query["template"]}')
                clean = False
        if entry.get('TORDF') is not None and not pid.startswith('cirilo:'):
            rstatus, _, _ = fetch(f'{host}/archive/objects/{pid}/datastreams/RDF/content', 'HEAD')
            if rstatus != 200:
                note('RDF missing', pid, f'RDF datastream answers HTTP {rstatus}')
                clean = False
        if clean:
            counts['ok'] += 1
        print(f'{"OK" if clean else "DEVIATION"} {pid}')

    if args.data:
        pids = data_pids(data_root)
        checked = [(pid, entry) for pid, entry in objects if pid in pids]
        for pid, entry in objects:
            if pid not in pids and entry.get('TORDF') is not None and not pid.startswith('cirilo:'):
                note('no source file', pid, 'the data repository has no TEI file with this PID')
        for pid, _ in checked:
            status, _, body = fetch(f'{host}/archive/objects/{pid}/datastreams/TEI_SOURCE/content')
            if status != 200:
                note('TEI_SOURCE unreadable', pid, f'HTTP {status}')
                continue
            # Cirilo uploads a file:/// graphic it finds beside the TEI as a datastream and
            # rewrites the reference to info:fedora/<pid>; one it does not find stays as written.
            # Both forms name the same graphic, so both sides compare with one placeholder.
            graphic = re.compile(r'url="(?:file:///[^"]*|info:fedora/[^"]*)"')
            local = graphic.sub('url="graphic"', pids[pid].read_text(encoding='utf-8'))
            if normalise(graphic.sub('url="graphic"', body.decode('utf-8', 'replace'))) != normalise(local):
                _, _, profile = fetch(f'{host}/archive/objects/{pid}?format=xml')
                modified = re.search(r'<objLastModDate>([^<]*)', profile.decode('utf-8', 'replace'))
                note('TEI_SOURCE differs from data repository', pid, f'ingested {modified.group(1)[:10] if modified else "?"}, file {pids[pid].relative_to(data_root)}')
                print(f'STALE {pid}')
            else:
                print(f'CURRENT {pid}')
        for entry in manifest.get('datastreams', []):
            for dsid, source in entry['sources'].items():
                status, _, body = fetch(f'{host}/archive/objects/{entry["pid"]}/datastreams/{dsid}/content')
                local = (data_root / source).read_text(encoding='utf-8')
                if status != 200:
                    note('datastream unreadable', entry['pid'], f'{dsid}: HTTP {status}')
                elif normalise(body) != normalise(local):
                    note('datastream differs from data repository', entry['pid'], f'{dsid} differs from {source}')
                    print(f'STALE {entry["pid"]}/{dsid}')
                else:
                    print(f'CURRENT {entry["pid"]}/{dsid}')

    print(f'\n{counts["objects"]} objects checked on {args.instance}, {counts["ok"]} without deviation, {len(deviations)} deviations')
    groups = {}
    for kind, pid, text in deviations:
        groups.setdefault(kind, []).append((pid, text))
    lines = [f'# Operator checklist, {args.instance}', '']
    for kind, items in groups.items():
        lines.append(f'## {kind} ({len(items)})')
        lines += [f'- `{pid}`: {text}' for pid, text in items]
        lines.append('')
    print('\n'.join(lines))
    if args.checklist:
        Path(args.checklist).write_text('\n'.join(lines), encoding='utf-8')
    sys.exit(1 if any(kind not in ('reference over http',) for kind, _, _ in deviations) else 0)


if __name__ == '__main__':
    main()
