# Markaz import — what was built and what was fixed

Source: `data/markaz-export-2026-09-18.csv` (Markaz "Export to my store", 48 products, 268 rows).
Pipeline: `build/transform.py` → `build/make_jsonl.py` → batched `productSet` calls.

## Result
47 products live in Shopify as **DRAFT**, 63 variants, 208 images (all READY on Shopify's CDN),
published to Online Store + Shop channels.

| Collection | Products | Tag rule |
|---|---|---|
| Shaving & Trimming | 15 | `shaving` |
| Watches | 14 | `watches` |
| Home & Bedding | 7 | `bedding` |
| Hair Styling | 7 | `hair-styling` |
| Hair Removal | 2 | `hair-removal` |
| Wallets & Accessories | 2 | `wallets` |
| Best Sellers | 9 | `best-seller` |
| Under Rs 2,000 | 10 | `under-2000` |

All smart collections keyed on tags, not price, so they keep working regardless of currency.

## Problems found in the supplier data and what was done

| Problem | Count | Fix |
|---|---|---|
| **Link back to markaz.app in every description** | 48/48 | Stripped. A customer clicking it buys the same item direct and the store earns nothing. |
| Supplier product codes (`MZ2335200012PRPT`) | 29 | Stripped |
| Descriptions truncated mid-sentence | 23 | Supplier intro discarded, replaced with written copy per product type |
| Watermarked `-withcode` images | 14 | Excluded from the galleries |
| Placeholder specs (`Model Number: Model Number`, `Width: Inches`, `Pack Of Pack Of 1`) | many | Dropped as valueless |
| Emoji bullets mangled into `?` | many | Stripped |
| Roman Urdu in an English store ("banane ke liye") | 1 | Rewritten |
| Duplicate titles — 4 × "Men's Imported Quality Watch" | 4 | Renamed from real specs (strap material, case shape, colour) |
| Duplicate titles — 7 identical blankets | 7 | Renamed by the colour recorded in the export |
| Junk titles ("Comfortable Grip and Ergonomics Design Men's Hair Trimmer 5") | 2 | Rewritten |
| `KM-595Professional` (missing space) | 1 | Fixed |
| Hair dryer claiming a **5000W motor** | 1 | Claim removed — impossible for a hand-held dryer, and not worth a returns dispute |
| Care advice telling people to oil the blades of a corded curling iron | 7 | Care text split per range: blades, heat tools, hair removal |
| Lone women's lawn suit in a gadget store | 1 | Dropped, as agreed |

## Theme fixes (on "Wired & Warped — Dark", still unpublished)
- Product template carried **"Buy 2 Get 1 Free on all Summer Collection items"** — a promo for a
  collection that no longer exists. Removed; it promised something that could not be honoured.
- Removed a leftover phone-case image block from the product page.
- Added a Cash on Delivery trust block directly under Add to Cart. This is where the delivery,
  confirmation and 7-day replacement copy now lives — one place, rather than duplicated into 47
  descriptions.
- Homepage rewired: hero links to Best Sellers and Under Rs 2,000, five real hero products,
  grid bound to `under-2000`.

## Pricing — how it actually works
The CSV `Variant Price` is the **selling price excluding delivery**. Worked example from the owner:

```
Markaz cost        389
selling price      533   <- the CSV number, and the Shopify price
delivery + COD fee 149
customer pays      682
owner earns        144
```

**Shopify prices were left exactly as exported and must stay that way** unless the Markaz price is
changed to match. The courier collects what Markaz has on file; if Shopify quotes a different
number the customer is asked for a different amount at the door.

Delivery is charged **on top**, per product, and varies. Shipping rates are not set yet because
those per-product figures are only visible in Markaz's pricing step.
