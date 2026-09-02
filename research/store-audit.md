# Wired & Warped — store audit (2026-09-02)

Baseline captured before any changes. Live theme is untouched and unmodifiable by
this agent (Shopify blocks writes/publish on MAIN), so it is its own backup.

## Store
| Field | Value | Action |
|---|---|---|
| Domain | www.wiredandwarped.com | keep |
| Plan | Basic | keep |
| Base currency | **GBP** | → PKR (owner, admin only) |
| Presentment currency | PKR | already correct |
| Primary market | **Pakistan** (UK/EU/US disabled) | already correct |
| Location | Shop location, **United Kingdom** | → Pakistan (owner) |
| Orders, all time | **0** | this is why base currency can still be changed |
| Timezone | Europe/London | → Asia/Karachi (owner) |
| Contact email | support@wiredandwarped.com | keep |
| Meta description | still advertises "free shipping to the US & UK" | rewrite |

## Theme
- **Horizon** (themeStoreId 2481), role MAIN, the only theme.
- Palette: background `#ffffff`, foreground `#000000`, color1 `#333333`, color2 `#DFDFDF`.
- Fonts: Inter throughout (body n4, subheading n5, heading n7). H1 56px, H2 48px.
- `page_width: narrow`, cart drawer, card hover lift, badge radius 100, button radius 14.
- Logo: `shopify://shop_images/Logo_no_BG.png` — reuse.
- Homepage = 2 sections: `hero` (two videos, "Protect it. Style it. Wrap it.")
  and `product-list` bound to the **top-sellers** collection.
  → deleting top-sellers would break this section; repoint before deleting.

## Catalogue (16 products, all ACTIVE)
- 15 × Printify phone cases, £22.99–£32.99, 43–52 variants each.
- 1 × `The Everyday Work Tote`, SKU `MKZ-657383-WINERED`, £14.99, vendor "Wired and Warped".
  Already a Markaz product with Pakistan/COD copy — priced in GBP, which is the bug.

## Collections
| Handle | Products | Type | Plan |
|---|---|---|---|
| frontpage | 0 | manual | keep |
| leather-engraved-phone-cases | 1 | manual | delete |
| summer-collection | 14 | manual | delete |
| entire-product-catalogue | 16 | smart (price > 0) | keep, reuse |
| top-sellers | 8 | manual | repoint homepage first, then rebuild |
| pakistan-collection | 1 | manual | keep, becomes the core |

## Pages / menus
- Pages: contact, about-us (published), data-sharing-opt-out (unpublished).
- main-menu: Home, Products, Contact, About us — rebuild.
- footer: Search, Your Privacy Choices — rebuild with policies.

## Apps installed
Messaging, **Printify**, Judge.me Reviews, **CJdropshipping**, Globo Product Options,
Hulk Product Options, Shopify Claude Connector.
→ Printify and CJdropshipping are leftovers; Judge.me is worth keeping for reviews.
→ Hulk injects `hulk_po_vd` into `layout/theme.liquid` head; harmless but note it.

## Agent capability boundaries (verified against the live schema)
Available: `themeDuplicate`, `themeFilesUpsert` (unpublished themes only), `productSet`,
`collectionCreate`, `pageCreate`, `menuUpdate`, `shopPolicyUpdate`, `urlRedirectCreate`,
`stagedUploadsCreate` + `fileCreate` (so original artwork can be uploaded, not just linked),
`discountAutomaticBasicCreate`, `inventorySetQuantities`, `bulkOperationRunMutation`.

Blocked, owner must do in admin: publishing a theme, writing to the live theme,
changing base currency, changing location, enabling Cash on Delivery, uninstalling apps.

## Network
`markaz.app`, `www.markaz.app`, `api.markaz.app`, `shop.markaz.app` all resolve in DNS but the
egress gateway answers **403 to CONNECT** — an org policy denial. Not bypassed.
Public product URLs follow `markaz.app/shop/product/<slug>/<id>`, so the catalogue is
scrapeable once allowlisted. Reseller cost prices stay behind an app login regardless.
