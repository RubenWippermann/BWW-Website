#!/usr/bin/env python3
"""Marke an das Impressum angleichen (01.11.): Footer nennt die Firma wie im Impressum; Schema alternateName nur 'BWW'. Idempotent."""
import glob, re, json, os
n = 0
for f in glob.glob('**/index.html', recursive=True) + ['404.html']:
    if not os.path.exists(f): continue
    h = open(f, encoding='utf8').read(); o = h
    h = h.replace('BWW – Bildungswerk für Wiederbelebung und Erste Hilfe.', 'BWW UG (haftungsbeschränkt).')
    if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
f = 'index.html'; h = open(f, encoding='utf8').read(); o = h
LONG = 'BWW – Multiplikatorenstelle & Rettungsdienstbildungsstelle'
def fix(m):
    j = json.loads(m.group(1))
    if j.get('alternateName') == LONG and j.get('@type') == 'WebSite': j['alternateName'] = 'BWW UG (haftungsbeschränkt)'
    elif isinstance(j.get('alternateName'), list) and LONG in j['alternateName']: j['alternateName'] = ['BWW']
    elif j.get('alternateName') == LONG: j['alternateName'] = 'BWW'
    else: return m.group(0)
    return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(',', ':')) + '</script>'
h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, h, flags=re.S)
if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
print('geändert:', n)
