# Warm dark premium rebuild — built, not yet uploaded

Modelled on the Northridge reference. **All files are built and validated in
`storefront/theme/` but NOT on Shopify** — the Shopify connection needs
re-authorising before they can be pushed.

## Design decisions

| | Reference | Applied |
|---|---|---|
| Canvas | warm near-black | `#100D0B` — brown undertone, not pure black, or the amber dies |
| Accent | amber / tan | `#C87A45`, hover `#D98D57` |
| Text | cream | `#F3ECE1`, muted `#A4968A` |
| Display face | condensed uppercase | **Oswald** 400–700 |
| Corners | near-square | 2px buttons, 4px cards |
| Hero | full-bleed photo, text left | full-bleed with a left-weighted scrim |
| Eyebrows | small amber caps | `.ww-eyebrow`, 0.26em tracking |
| Feature row | bordered plates | `.ww-why__item`, hairline borders, no fill |

### Why the font is loaded in CSS, not Shopify's font picker
A wrong font handle in `settings_data.json` fails silently to a fallback, and this
environment cannot open the storefront to check. Loading Oswald via `@import` in
`ww-brand.css` is deterministic. Horizon keys every heading off
`--font-h1--family` … `--font-h6--family`, so overriding those on `:root` restyles
the whole storefront — collection pages, cart, search — not just our sections.

### The white-background problem
Supplier photography has white backgrounds baked into the pixels. On a dark page
there is no way to make those transparent, so a "dark product tile" is not
available. The tile is therefore deliberately **warm paper `#F7F3EC`** — it reads
as a gallery mount rather than an accident, and it sits inside the amber palette
instead of fighting it as clinical white would.

### Hero image
The reference's impact comes largely from its photograph. There is no equivalent
shot in this catalogue — the supplier images are products on white, which would
look wrong full-bleed. The hero falls back to a warm radial gradient, which holds
up on its own, and the image slot is wired and waiting.

**This is the single biggest gap between this build and the reference.** One good
dark, moody lifestyle photograph would close most of it.

## Files changed
- `assets/ww-brand.css` — full rewrite
- `sections/ww-hero.liquid` — full-bleed background, scrim, left-aligned content
- `config/settings_data.json` — dark warm palette, uppercase headings, square corners
- `sections/footer-group.json` — dark surfaces, amber signup button
- `templates/product.json` — COD block back to a dark surface
- `templates/index.json` — hero rewritten; copy matched to the reference's voice

Also still carried from the previous round and not yet live: the `object-fit:
contain` fix for card galleries.
