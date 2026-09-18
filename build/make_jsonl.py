import json, collections

P = json.load(open('build/products.json'))

# Starter "best seller" picks: the lowest-friction items for a first COD order.
# Cheap, light, easy to say yes to at the door. The owner reassigns these once
# real ad data arrives — it's just a tag.
BEST = {p['handle'] for p in sorted(P, key=lambda x: x['price_min'] or 0)[:8]}

GROUP_TAG = {'grooming':'Grooming', 'watches':'Watches',
             'home':'Home & Bedding', 'accessories':'Accessories'}

def build(p):
    tags = [GROUP_TAG.get(p['group'], 'Other'), p['category'], p['tag'], p['group']]
    if p['price_min'] is not None and p['price_min'] < 2000:
        tags.append('under-2000')
    if p['handle'] in BEST:
        tags.append('best-seller')

    # One option per product in this export. Preserve its real name where the
    # supplier gave one ("color"), otherwise fall back to a single default variant.
    optname = p['variants'][0]['optname'] if p['variants'] else 'Title'
    values, seen = [], set()
    for v in p['variants']:
        if v['option'] not in seen:
            seen.add(v['option']); values.append(v['option'])
    if not values:
        values, optname = ['Default Title'], 'Title'

    variants = []
    for v in p['variants']:
        variants.append({
            'sku': v['sku'],
            'price': v['price'],
            'optionValues': [{'optionName': optname.title(), 'name': v['option']}],
            # We hold no stock — Markaz ships. Untracked so nothing ever reads
            # "sold out" because of an inventory number we don't maintain.
            'inventoryItem': {'tracked': False},
            'inventoryPolicy': 'CONTINUE',
            'taxable': False,
        })
    if not variants:
        variants = [{'price': str(p['price_min'] or 0),
                     'optionValues': [{'optionName': 'Title', 'name': 'Default Title'}],
                     'inventoryItem': {'tracked': False},
                     'inventoryPolicy': 'CONTINUE', 'taxable': False}]

    # "-withcode" images are the supplier's watermarked copies with the Markaz
    # product code printed on them. Never put those in front of a customer.
    imgs = [i for i in p['images'] if 'withcode' not in i['src']]
    files = [{'originalSource': i['src'], 'contentType': 'IMAGE',
              'alt': p['title'][:250]} for i in imgs[:6]]

    return {'input': {
        'handle': p['handle'],
        'title': p['title'],
        'descriptionHtml': p['descriptionHtml'],
        'productType': p['type'],
        'vendor': 'Wired & Warped',
        'status': 'DRAFT',
        'tags': sorted(set(tags)),
        'seo': {'title': f"{p['title'][:60]} | Cash on Delivery Pakistan",
                'description': (f"{p['title']} — delivered across Pakistan with Cash on Delivery. "
                                f"7-day replacement, WhatsApp support 9am-9pm.")[:320]},
        'productOptions': [{'name': optname.title(),
                            'values': [{'name': v} for v in values]}],
        'variants': variants,
        'files': files,
    }}

recs = [build(p) for p in P]
with open('build/products.jsonl','w') as f:
    for r in recs:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

# one-product probe file, to prove Shopify can fetch Markaz-hosted images
probe = next(r for r in recs if r['input']['handle'].startswith('classic-handcrafted'))
open('build/probe.jsonl','w').write(json.dumps(probe, ensure_ascii=False) + '\n')

print(f"jsonl records: {len(recs)}")
print(f"variants:      {sum(len(r['input']['variants']) for r in recs)}")
print(f"files:         {sum(len(r['input']['files'])    for r in recs)}")
t = collections.Counter(t for r in recs for t in r['input']['tags'])
print("\ntag counts:")
for k, v in t.most_common(): print(f"  {v:3}  {k}")
