"""Turn the Markaz export into branded Wired & Warped listings."""
import csv, re, json, collections, html

SRC = 'data/markaz-export-2026-09-18.csv'

# ---------------------------------------------------------------- categorise
GROOM_SHAVE = {'Hair Trimmer','Hair Shaver','Nose & Ear Hair Trimmer'}
GROOM_STYLE = {'Curling Iron Rod','Hair Straightener','Hair Curler & Straightener','Hair Dryer'}
GROOM_REMOVE= {'Hair Epilator'}
WATCH       = {'Analogue Watch','Chain Watch','Luxury Watch','Sports Watch',
               'Chronograph Watch','Analogue Couple Watches'}
HOME        = {'Blanket'}
ACC         = {'Card Holder'}
DROP_TYPES  = {'Suit'}                       # the lone lawn suit — dropped per decision

def category(t):
    if t in GROOM_SHAVE:  return ('Shaving & Trimming','grooming','shaving')
    if t in GROOM_STYLE:  return ('Hair Styling','grooming','hair-styling')
    if t in GROOM_REMOVE: return ('Hair Removal','grooming','hair-removal')
    if t in WATCH:        return ('Watches','watches','watches')
    if t in HOME:         return ('Home & Bedding','home','bedding')
    if t in ACC:          return ('Wallets & Accessories','accessories','wallets')
    return ('Other','other','other')

# ------------------------------------------------------------------- hooks
# One-line opener per product type. Written for a Pakistani COD buyer:
# concrete benefit, no hype, no promises the product can't keep.
HOOKS = {
 'Hair Trimmer': "A clipper that holds its line through a full cut, instead of dragging and pulling halfway through.",
 'Hair Shaver': "A close shave without the razor burn, and no waiting on blades you have to keep buying.",
 'Nose & Ear Hair Trimmer': "The thirty-second job you keep forgetting until you see a photo of yourself.",
 'Curling Iron Rod': "Curls that are still there at the end of the evening, not twenty minutes after you leave the house.",
 'Hair Straightener': "Straight, smooth and done in one pass, so you are not going back over the same section until it scorches.",
 'Hair Curler & Straightener': "Straight one morning, curled the next, without buying two separate tools.",
 'Hair Dryer': "Dries fast and quietly, and does not leave your hair feeling like straw.",
 'Hair Epilator': "Smooth for weeks rather than days, done at home on your own schedule.",
 'Analogue Watch': "A watch that reads as expensive without costing it.",
 'Chain Watch': "Steel chain, clean dial, dressed up enough for a wedding and plain enough for work.",
 'Luxury Watch': "The heft and finish of something far dearer than what you paid.",
 'Sports Watch': "Built for sweat, rain and being knocked against things.",
 'Chronograph Watch': "Working sub-dials and a proper steel case, at a price that does not need justifying.",
 'Analogue Couple Watches': "A matched pair, boxed and ready to give.",
 'Blanket': "Heavy enough to actually keep the cold out through a Punjab winter night.",
 'Card Holder': "Slim enough for a front pocket, with room for everything you actually carry.",
}

# Keyed on the specific range, not the broad group: telling someone to oil the
# blades of a corded curling iron is nonsense and reads as copy-paste.
CARE = {
 'shaving': ("Charge it fully before the first use and it will hold that charge far longer over its life. "
             "Rinse only the parts the manual says are washable, and oil the blades every few cuts."),
 'hair-styling': ("Let it heat up fully before the first section, and work in small sections rather than "
                  "going over the same piece twice. Wipe the plates or barrel down once cool, never while hot."),
 'hair-removal': ("Use it on clean, dry skin and go against the direction of growth. "
                  "Rinse the head after each use and let it dry fully before storing."),
 'watches':  ("Water resistant is not the same as waterproof — keep it off in the shower unless the dial says otherwise. "
              "A soft cloth is all the strap needs."),
 'home':     ("Machine washable on a cold, gentle cycle. Wash it before first use to soften the fleece and set the colour."),
 'accessories': ("Real leather darkens and softens with use. Keep it out of standing water and it will outlast several wallets."),
}

DELIVERY = (
 '<p><strong>Delivery and payment</strong></p>'
 '<ul>'
 '<li>Cash on Delivery anywhere in Pakistan — you pay the courier, not us, and not in advance.</li>'
 '<li>Delivered in 2 to 5 working days depending on your city.</li>'
 '<li>We confirm every order by phone or WhatsApp before it ships, so nothing turns up that you did not order.</li>'
 '<li>Damaged, incomplete or not what you ordered? Message us within 7 days with photos of the item and the packaging and we will replace it.</li>'
 '</ul>'
 '<p>Questions before you order? WhatsApp <strong>+92 305 3488833</strong>, 9am to 9pm, any day.</p>'
)

# --------------------------------------------------------------- spec clean
DROP_SPEC = re.compile(r'^(product code|note)\b', re.I)
# values that are a bare unit or placeholder carry no information
JUNK_VAL = re.compile(r'^(inches|cm|mm|grams?|kg|model number|n/?a|-|\.)$', re.I)
# "Pack of 1" / "Pack of 999" and bare dimensions tell the customer nothing useful
JUNK_LINE = re.compile(r'^(pack of\b|length:|height:|width:)', re.I)

def clean_specs(body):
    """Split the <li> bullets into real specs and feature prose, dropping supplier junk.

    The export mixes three things into one list: genuine key/value specs, marketing
    sentences, and placeholders where the supplier left the field blank
    ("Model Number: Model Number", "Width: Inches"). Only the first is a spec.
    """
    specs, features = [], []
    for m in re.finditer(r'<li>(.*?)</li>', body, re.S):
        t = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
        t = re.sub(r'\s+', ' ', t)
        # the export mangles emoji bullets into literal '?' characters
        t = re.sub(r'^[?\u2022\u2713\u2714\uFFFD]+\s*', '', t).strip()
        if not t or DROP_SPEC.match(t):
            continue
        t = re.sub(r'^Pack Of Pack Of', 'Pack of', t, flags=re.I)
        if JUNK_LINE.match(t):
            continue

        # marketing prose: a long line built as "Claim – explanation"
        if len(t) > 70 and re.search(r'\s[–—-]\s', t):
            head, tail = re.split(r'\s[–—-]\s', t, maxsplit=1)
            features.append((head.strip(), tail.strip()))
            continue

        if ':' in t:
            k, v = (x.strip() for x in t.split(':', 1))
            if not v or JUNK_VAL.match(v) or v.lower() == k.lower():
                continue                      # placeholder, not a spec
            specs.append(f'{k}: {v}')
        else:
            specs.append(t)
    return specs, features

def strip_markaz(body):
    """Remove the backlink that would send our customer to buy direct."""
    return re.sub(r'<p><a href="[^"]*markaz[^"]*"[^>]*>.*?</a></p>', '', body, flags=re.I|re.S)

# ------------------------------------------------------------------- title
# Supplier titles that are duplicates or pure filler. Keyed on the Markaz product
# id in the handle, and differentiated only by specs actually present in the export
# (strap material, case shape, colour) — never by anything invented.
TITLE_OVERRIDES = {
 '753116': "Men's Black Leather Strap Watch, Round Dial",
 '750325': "Men's Black Rubber Strap Watch, 22mm Dial",
 '754811': "Men's Premium Multicolour Chain Watch, Round Dial",
 '756861': "Men's Everyday Chain Strap Watch, Round Dial",
 '752674': "Men's Nose & Ear Hair Trimmer, Ergonomic Grip",
 '758488': "Men's Gold Professional Hair Trimmer, Ergonomic Grip",
}

def clean_title(t):
    """Cut the supplier's feature-dump back to a name a person would say out loud."""
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'\bKEMEI\b', 'Kemei', t)
    t = re.sub(r'\bKM-\s+', 'KM-', t)
    t = re.sub(r'(KM-\s?\d+[A-Z]?)(?=[A-Z])', r'\1 ', t)   # "KM-595Professional" -> "KM-595 Professional"
    # keep everything before the first dash/pipe, if that still names the product
    head = re.split(r'\s*[|–—]\s*|\s+-\s+', t)[0].strip()
    if len(head) >= 22:
        t = head
    return t[:90].rstrip(' ,-–—')

# -------------------------------------------------------------------- build
def main():
    rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
    prod = collections.OrderedDict()
    for r in rows:
        h = r['Handle']
        p = prod.setdefault(h, {'handle':h,'title':'','type':'','body':'','vendor':'',
                                'variants':[], 'images':[]})
        if r['Title'].strip(): p['title'] = r['Title']
        if r['Type'].strip():  p['type']  = r['Type']
        if r['Body (HTML)'].strip(): p['body'] = r['Body (HTML)']
        if r['Variant SKU'].strip():
            p['variants'].append({
                'sku': r['Variant SKU'],
                'option': r['Option1 Value'].strip() or 'Default',
                'optname': r['Option1 Name'].strip() or 'Title',
                'price': r['Variant Price'].strip(),
            })
        if r['Image Src'].strip():
            p['images'].append({'src': r['Image Src'], 'alt': r['Image Alt Text'].strip()})

    blanket_n = 0
    seen_cols = {}
    out = []
    for h, p in prod.items():
        if p['type'] in DROP_TYPES:
            continue
        cat, group, tag = category(p['type'])
        pid = re.search(r'mkz-(\d+)$', h)
        title = clean_title(p['title'])
        if pid and pid.group(1) in TITLE_OVERRIDES:
            title = TITLE_OVERRIDES[pid.group(1)]

        # All 7 blankets ship under one supplier title. Name them by the colour the
        # export actually records, so "brown blanket" finds the brown one. Two colours
        # repeat, so those get a suffix rather than a made-up shade name.
        if p['type'] == 'Blanket':
            blanket_n += 1
            col = re.search(r'<li>Color:\s*([^<]+)</li>', p['body'])
            col = col.group(1).strip() if col else f'Design {blanket_n}'
            seen_cols.setdefault(col, 0)
            seen_cols[col] += 1
            suffix = col if seen_cols[col] == 1 else f'{col}, Design {seen_cols[col]}'
            title = f"Fleece Printed Double Bed Blanket — {suffix}"

        specs, features = clean_specs(p['body'])
        hook  = HOOKS.get(p['type'], "Chosen because it does the job it claims to do.")
        care  = CARE.get(tag, CARE.get(group, ''))

        body = [f'<p>{hook}</p>']
        if features:
            body.append('<p><strong>Why this one</strong></p><ul>')
            body += [f'<li><strong>{html.escape(k)}.</strong> {html.escape(v)}</li>'
                     for k, v in features[:4]]
            body.append('</ul>')
        if specs:
            body.append('<p><strong>Specifications</strong></p><ul>')
            body += [f'<li>{html.escape(s)}</li>' for s in specs]
            body.append('</ul>')
        if care:
            body.append(f'<p><strong>Looking after it</strong></p><p>{care}</p>')

        prices = sorted({float(v['price']) for v in p['variants'] if v['price']})
        out.append({
            'handle': h, 'title': title, 'type': p['type'], 'category': cat,
            'group': group, 'tag': tag,
            'descriptionHtml': ''.join(body),
            'variants': p['variants'], 'images': p['images'],
            'price_min': prices[0] if prices else None,
        })

    json.dump(out, open('build/products.json','w'), indent=1)
    print(f"products built: {len(out)} (dropped {len(prod)-len(out)})")
    by = collections.Counter(p['category'] for p in out)
    for c,n in by.most_common(): print(f"  {n:3}  {c}")
    print(f"\ntotal variants: {sum(len(p['variants']) for p in out)}")
    print(f"total images:   {sum(len(p['images'])   for p in out)}")
    print(f"markaz links remaining: {sum('markaz' in p['descriptionHtml'].lower() for p in out)}")
    print(f"supplier codes remaining: {sum('Product Code' in p['descriptionHtml'] for p in out)}")

main()
