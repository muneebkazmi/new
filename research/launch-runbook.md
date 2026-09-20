# Wired & Warped — launch runbook

Status as of 2026-09-18. Branch: `claude/markaz-shopify-store-setup-yuv416`.

## Done

**Backup** — `backup/store-snapshot-2026-09-02.json` holds the full pre-change state
(16 products with descriptions/variants/images, 6 collections, 3 pages, 3 menus).
The live Horizon theme was never modified, so it is its own rollback point.

**Catalogue cleared** — all 16 products set to `ARCHIVED` (15 Printify phone cases +
the Markaz tote). Reversible: Products → filter Archived → select all → set Active.
Deleted the two dead collections `summer-collection` and `leather-engraved-phone-cases`.

**Design built** — theme `Wired & Warped — Dark`, id `198465945977`, UNPUBLISHED.
Dark premium tech: `#08090B` canvas, `#22D3EE` accent, `#F59E0B` for COD/urgency.
Five custom sections (hero, trust bar, hero products, why-us, WhatsApp float) plus a
brand CSS layer. Horizon's own components inherit the dark palette, so cart drawer,
product grids and forms follow without being rewritten.
Every file verified byte-for-byte by md5 after upload.

**Collections created** — all smart and tag-driven, so they self-populate on import:

| Handle | Fills from tag |
|---|---|
| `best-sellers` | `best-seller` |
| `under-1500` | `under-1500` |
| `audio` | `audio` |
| `charging-power` | `charging` |
| `wearables` | `wearables` |

Tag products with these on import and they file themselves. `under-1500` is driven by
tag rather than price so it does not break while base currency is still GBP.

## Blocked on you

1. **Allowlist markaz.app** in the environment's network policy:
   `markaz.app`, `www.markaz.app`, `api.markaz.app`, `shop.markaz.app`, `dropshipping.markaz.app`.
   Public product pages follow `markaz.app/shop/product/<slug>/<id>`.
2. **Install the Markaz Shopify app** and connect your reseller account. This is what
   supplies real SKUs, cost prices and order routing for COD fulfilment. Reseller
   pricing sits behind an app login, so allowlisting alone will not produce margins.
3. **Base currency GBP → PKR** — Settings → General. No API exists for this. Only
   possible because the store has zero lifetime orders; it closes the moment you take one.
   Do it **before** products are loaded or everything needs repricing.
4. **Location UK → Pakistan** — Settings → Locations.
5. **Enable Cash on Delivery** — Settings → Payments → Manual payment methods.
   Shopify Payments does not support Pakistan, so COD is the payment method.
6. **Timezone** → Asia/Karachi. Settings → General.
7. **Store meta description** still reads "free shipping to the US & UK".
   Settings → General → store details. No API for this either.
8. **Publish the theme** once reviewed. Agents are blocked from publishing themes.
9. **Uninstall Printify and CJdropshipping** once you are happy the old catalogue is gone.
   Keep Judge.me — reviews matter a lot for COD trust.

## Preview

`https://www.wiredandwarped.com/?preview_theme_id=198465945977`

I cannot open this myself — the egress policy blocks the storefront domain and
`svnmy0-md.myshopify.com` too, so the design is verified by file integrity and schema
validation, not by a rendered screenshot. Check it on your phone as well as desktop.

The five hero cards currently render as labelled placeholders with the intended price
ladder. They become real products the moment a product is picked in the theme editor,
or when I wire them up after import.

## The price ladder

| # | Product | Price | Tags to apply |
|---|---|---|---|
| 1 | 360° Magnetic Phone Holder | Rs 990 | `best-seller`, `under-1500` |
| 2 | 20W Fast Charger + Type-C Cable | Rs 1,490 | `best-seller`, `under-1500`, `charging` |
| 3 | Bluetooth Neckband | Rs 2,490 | `best-seller`, `audio` |
| 4 | 10,000mAh Power Bank | Rs 3,490 | `best-seller`, `charging` |
| 5 | Smart Watch, BT calling | Rs 4,990 | `best-seller`, `wearables` |

Archetypes, not fixed SKUs — each slot gets the best real Markaz product on margin,
rating and dispatch speed once the catalogue is reachable.

## Gotchas found the hard way

- `themeFilesUpsert` returns an empty `upsertedThemeFiles` list **and no userErrors**
  when it rejects a file. Always re-query `checksumMd5` to confirm a write landed.
  This caught `ww-whatsapp.liquid` silently failing on `"tag": null` in its schema.
- Push theme files with `stagedUploadsCreate` + a `POST` from disk, then reference the
  staged URL in `themeFilesUpsert`. The GCS ETag comes back as the file's md5, so upload
  integrity is confirmed for free.
- Horizon's `footer-utilities` section painted its background with `color_palette.foreground`.
  On a dark palette that renders a white slab across the page footer. Fixed in
  `sections/footer-group.json`.

---

# LIVE — 2026-09-18

Theme **Wired & Warped — Dark** published. All **47 products ACTIVE**, PKR, published to
Online Store and Shop. 16 old Printify products remain archived and recoverable.

Navigation rebuilt: Grooming (with Shaving & Trimming / Hair Styling / Hair Removal),
Watches, Home & Bedding, Wallets, Under Rs 2,000, Contact.

## Still to do

1. **Policies** — `policies/` holds rewritten Refund and Delivery text to paste at
   Settings → Policies. I lack the `write_legal_policies` scope. This is the most urgent
   item: the current refund policy says "all sales are final, no returns" while every
   product page promises 7-day replacement.
2. **Shipping rates** — not set. Needs the per-product delivery + cash-handling figures
   from Markaz's pricing step. Without a rate, checkout may not charge delivery at all,
   which means the courier collects more than the site quoted.
3. **Store meta description** — still reads "free shipping to the US & UK".
   Settings → General. No API for it.
4. **Location** still United Kingdom; **timezone** still Europe/London. Settings.
5. **Uninstall Printify and CJdropshipping.** Terms of Service still names Printify.
6. **Delete the `top-sellers` collection** (8 archived products) once you are happy.
7. **Rename blankets and the two chain watches** if the photos show something more
   specific than the colour recorded in the export. I could not see the images.

## Operating reality

Every order must be placed manually on Markaz with the customer's address. Nothing
connects Shopify orders to Markaz now that their Shopify app is delisted.

Margins are thin: the worked example earns Rs 144 on a Rs 682 order. One refused COD
parcel wipes out several sales. Worth reviewing Markaz prices before spending on ads.

---

# Menu + image audit — 2026-09-20

## Menus, fixed

- **"Grooming" pointed at `/collections/shaving-trimming`.** The top-level item took you
  to one of its own children, and 9 of the 24 grooming products had no parent listing.
  Created a `grooming` smart collection (tag `grooming`, 24 products) and repointed it.
- **Footer linked to `/pages/data-sharing-opt-out`, which is unpublished** — a 404 for every
  customer who clicked it. Footer rebuilt: About Us, Contact, Delivery, Returns &
  Replacements, Privacy Policy, Terms of Service.
- **About Us was still phone-case copy** ("your phone case should match your mood",
  "Velvet Matte or Mirror Glossy") and the new footer linked straight to it. Rewritten
  around electricals + textiles, COD and the WhatsApp number, UK company block retained.

Main menu now: Grooming (Shaving & Trimming / Hair Styling / Hair Removal), Watches,
Home & Bedding, Wallets, Under Rs 2,000, Contact. Every URL verified against a live
collection or page.

## Images

Audited all 208 across 47 products. The supplier's ratios are all over the place:

| Ratio | Where |
|---|---|
| 1:1 | most grooming, some watches |
| 3:4 | wallets, several watches, most blankets |
| 4:3 | straighteners, some curlers |
| 1080×361 (3:1) | one R-999 curler shot — a banner strip, not a product photo |
| 873×1802 (1:2) | five KM-519A shots — tall spec infographics |

Resolution ranges from 640×640 to 1080×1802. Roughly a dozen featured images are
660×660 or 640×640, which is fine on a card but soft on a full product page. That is
what the supplier provided; nothing to fix short of reshooting.

**Display was inconsistent, and that is fixed.** Horizon's card gallery block exposes an
aspect-ratio setting but no fit, so it cropped everything to fill the square frame and
sliced the top and bottom off every portrait shot. `assets/ww-brand.css` now forces
`object-fit: contain` on card galleries with a white fill and 6% padding, so every card
is the same square and the whole product stays in shot. Collection banners still cover,
because those are meant to fill.

Product page galleries were already correct — square frame, `media_fit: contain`.

Theme **Wired & Warped — Light v2** (`199343735161`) carries the image fix and needs
publishing. Menus, collections and the About page are data, so those are already live.
