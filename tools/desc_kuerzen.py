#!/usr/bin/env python3
"""Descriptions >155 Zeichen von Hand-Regeln kürzen (Standortseiten-Vorlagen), Bedeutung unverändert. Idempotent; zeigt Rest."""
import re, glob, html, sys
R = [('Schulung für Unternehmen in Ludwigshafen', 'Schulung für Firmen in Ludwigshafen'), ('über die BG/UK abrechenbar', 'BG/UK-abrechenbar'), ('über BG/UK abrechenbar', 'BG/UK-abrechenbar'),
     ('kein Anfahrtsweg fürs Team – ', 'kein Anfahrtsweg, '), ('kein Anreisestress, ', ''), ('direkt in eurem Betrieb', 'direkt im Betrieb'),
     ('BWW aus dem nahen Eichsfeld kommt', 'BWW aus dem Eichsfeld kommt'), ('im Eichsfeld zu euch', 'zu euch'), (' Auch Brandschutz.', '')]
def esc(s): return s.replace('&', '&amp;')
n = 0; rest = []
for f in sorted(glob.glob('standorte/*/index.html')):
    h = open(f, encoding='utf8').read(); m = re.search(r'<meta name="description" content="(.*?)"', h)
    if not m: continue
    od = m.group(1); d = html.unescape(od)
    if len(d) <= 155: continue
    nd = d
    for a, b in R:
        if len(nd) <= 155: break
        nd = nd.replace(a, b)
    if len(nd) > 155: rest.append((f, len(nd), nd)); continue
    h = h.replace(od, esc(nd)); open(f, 'w', encoding='utf8').write(h); n += 1
print('gekürzt:', n, 'Rest:', len(rest))
for r in rest: print(r)
