#!/usr/bin/env python3
"""ItemList-JSON-LD ohne eingebettete Course-Objekte: nur ListItem mit position, url, name (idempotent)."""
import glob, json, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
RX = re.compile(r'(<script type="application/ld\+json">)(\{[^<]*"@type":"ItemList"[^<]*\})(</script>)')
n = 0
for f in glob.glob('**/index.html', recursive=True) + ['index.html']:
    if f.startswith('tools/'): continue
    h = open(f, encoding='utf8').read()
    def fix(m):
        global n
        j = json.loads(m.group(2)); neu = []
        for i, it in enumerate(j['itemListElement'], 1):
            c = it.get('item')
            neu.append({"@type": "ListItem", "position": it.get('position', i), "url": c['url'], "name": c['name']} if c else it)
        if neu == j['itemListElement']: return m.group(0)
        j['itemListElement'] = neu; n += 1
        return m.group(1) + json.dumps(j, ensure_ascii=False, separators=(',', ':')) + m.group(3)
    h2 = RX.sub(fix, h)
    if h2 != h: open(f, 'w', encoding='utf8').write(h2); print('geändert:', f)
print('ItemList umgestellt:', n)
