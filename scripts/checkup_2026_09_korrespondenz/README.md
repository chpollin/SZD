# Bundle signatures for the correspondence index

A group of aggregate entries in [`data/Correspondence/SZDKOR.xml`](../../data/Correspondence/SZDKOR.xml)
carries no `msIdentifier/idno[@type="signature"]`, namely the contiguous block `SZDKOR.928` to
`SZDKOR.970` created with the SZ-AAL/B ingest of June 2026, and a smaller set of older entries,
which the dry run of this script lists in full. The September 2026 archive checkup reports most
of them as duplicate correspondent headings. They are not duplicates. The two-level model of
[`knowledge/COLLECTIONS.md`](../../knowledge/COLLECTIONS.md) allows a correspondent several
index entries, one per archival bundle, and the signature is what distinguishes them. Without
it the second entry of a person reads as a repetition of the first.

`add_bundle_signatures.py` writes that signature where the konvolut object the entry points
to proves it, and nowhere else.

## The rule

For one signature-less entry, take the signature of every piece of its konvolut object, drop
the item number, drop the group `SZ-SAM/AK`, and if exactly one group is left, write it as the
entry's signature.

The item number is a dot, digits and at most one disambiguating letter, so `SZ-AAL/B1.110a`
belongs to the group `SZ-AAL/B1` and `SZ-AAL/B13`, which carries no item number, is already a
group. `SZ-SAM/AK` is dropped because that picture-postcard series runs across the whole
collection and holds an index entry of its own under that bare signature for a large number of
correspondents, so it is never the bundle a signature-less second entry describes.

Where the arithmetic leaves zero groups or more than one, the entry stays untouched and the
run lists it with its groups. Then the konvolut merges several bundles and which of them the
aggregate counts is an editorial question that the data does not answer. Nothing is derived
from a name, a title or a piece count.

## Source of the konvolut evidence

Konvolut objects that exist as files under
[`data/Correspondence/konvolute/`](../../data/Correspondence/konvolute/) are read locally.
The remaining pointers are resolved by one HTTP GET of
`https://gams.uni-graz.at/archive/objects/<pid>/datastreams/TEI_SOURCE/content`, cached on
disk outside the repository, so a repeated run makes no request. GAMS is read-only here, the
script never writes to it, and `--offline` refuses to make any request at all.

## Run

```bash
# 1) dry run, showing what would be written and every untouched entry with its reason
python scripts/checkup_2026_09_korrespondenz/add_bundle_signatures.py

# 2) apply
python scripts/checkup_2026_09_korrespondenz/add_bundle_signatures.py --apply

# 3) check
python scripts/checkup_2026_09_korrespondenz/add_bundle_signatures.py --verify
```

`--cache` sets the directory for the fetched konvolut sources, by default a folder in the
system temp directory. The run is idempotent, so a second dry run after `--apply` reports zero
entries.

`--verify` parses the index, compares it against `HEAD` to find exactly the entries this
script can have written, re-derives each of their signatures from the konvolut, and fails on
any mismatch. It also fails if a signature-less entry is left that the rule could resolve.
Edits to the same file that this script did not make are outside what it checks.

## Serialisation

One line carrying the new `idno` element is inserted before the first `altIdentifier` of the
entry's `msIdentifier`, which is where every entry that has a signature carries it, with
the indentation of that line. The rest of the file text is untouched, so indentation,
attribute order and line endings stay byte-identical.

## Scope

The script leaves these alone.

- Entries whose konvolut merges several bundles. Among them every entry whose konvolut is a
  large person object such as Anna Meingast, Lotte Zweig, Friderike Zweig or the unidentified
  senders. The checkup report proposes a signature for some of them from outside evidence, and
  this script does not act on evidence it cannot derive.
- The piece counts. `measure[@type="correspondence"]` is not touched, although several of
  the reported counts contradict the konvolut. Whether an aggregate entry counts an archival
  bundle or a correspondence relationship is an open operator ruling.
- The title suffixes `u. a.` and `aus dem Nachlass Stefan Zweigs` stay as they are.
- `correspDesc/@type`. The index uses `toZweig` and `fromZweig` only. Where a corrected
  entry names neither Stefan Zweig as sender nor as recipient, as in `SZDKOR.856` with Alfred
  Einstein to Anna Meingast, the index holds no third value and no older entry without Stefan
  Zweig to follow. The direction of the `correspAction` pair does not change in any of those
  entries, so `@type` was left as it stands. Which value such an entry should carry is open.
- The konvolut objects themselves. Their pieces, PIDs and titles belong to the ingest
  source and to `scripts/korrespondenz_titel/`.

## Related

- [`scripts/korrespondenz_titel/`](../korrespondenz_titel/) rebuilds the entry titles of the
  konvolut objects from `correspDesc` and the physical extent.
- The section "Archive checkup (September 2026)" of [`knowledge/DATA.md`](../../knowledge/DATA.md#archive-checkup-september-2026)
  summarises the checkup this script answers. The file-and-line diagnosis is an
  archive-internal note outside the repository.
