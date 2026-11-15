#!/usr/bin/env python3
"""Weiterleitungs-Stubs (Titel 'Weitergeleitet: …', Meta-Refresh auf die richtige Ortsseite): <meta name="robots" content="noindex,follow"> ergaenzen.
GitHub Pages kennt keine serverseitige 301 (_redirects/Header nicht moeglich): Meta-Refresh + JS-replace + canonical bleiben. Nicht in der Sitemap. Idempotent."""
import glob, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
n = 0; ids = []
for p in sorted(glob.glob('**/index.html', recursive=True)):
    if p.startswith('tools/'): continue
    h = open(p, encoding='utf8').read()
    if 'http-equiv="refresh"' not in h or '<title>Weitergeleitet:' not in h: continue
    ids.append(p)
    if 'name="robots"' in h: continue
    a = re.search(r'<link rel="canonical" href="[^"]*">', h); assert a, p
    h = h.replace(a.group(0), a.group(0) + '<meta name="robots" content="noindex,follow">', 1); open(p, 'w', encoding='utf8').write(h); n += 1
print('Stubs gefunden:', len(ids), '| ergänzt:', n)
