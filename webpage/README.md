# SZD webpage content

Static page content of stefanzweig.digital, with about pages, imprint, landing page content, audio files and images.

## Images and links

- `<ref type="entry">` links to a catalogue entry, for instance in the works.
- `<ref type="external">` is an external link that the build leaves as it is, for instance `http://www.stefanzweig.digital/o:szd.thema.5/sdef:TEI/get?locale=de` or `https://verlag.sandstein.de/detailview?no=98-446`.
- A `<ref>` without `@type` but with `@target` links to the facsimile in the Mirador viewer.
- An image without `<ref>` is shown as an image with or without caption.

All images open zoomable on click (fancybox), and all links are rendered as `<a>` in the caption.
