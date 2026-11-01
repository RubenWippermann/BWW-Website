#!/usr/bin/env python3
"""Schritt C/D (SEO 01.11.): Stand-Datum der inhaltlich geänderten Seite, Marke 'BWW' im WebSite-/Organization-Schema der Startseite. Idempotent."""
import re, json, sys, os
root = sys.argv[1] if len(sys.argv) > 1 else '.'
n = 0
f = os.path.join(root, 'wissen/rettungskette/index.html'); h = open(f, encoding='utf8').read(); o = h
h = h.replace('article-stand">Stand: 03.08.2026 ·', 'article-stand">Stand: 01.11.2026 ·', 1)
h = h.replace('"dateModified":"2026-08-03"', '"dateModified":"2026-11-01"', 1)
if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
f = os.path.join(root, 'index.html'); h = open(f, encoding='utf8').read(); o = h
ALT = 'BWW – Multiplikatorenstelle & Rettungsdienstbildungsstelle'
def fix(m):
    j = json.loads(m.group(1)); t = j.get('@type')
    if t == 'WebSite' and j.get('name') != 'BWW':
        j['alternateName'] = j['name']; j['name'] = 'BWW'
    elif isinstance(t, list) and 'EducationalOrganization' in t and j.get('alternateName') == ALT:
        j['alternateName'] = ['BWW', ALT]
    else: return m.group(0)
    return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(',', ':')) + '</script>'
h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, h, flags=re.S)
if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
print('geändert:', n)
