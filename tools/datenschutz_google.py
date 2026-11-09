#!/usr/bin/env python3
"""Datenschutzerklärung: neuer § 15 'Werbung bei Google und Auswertung' (Variante A), Wortlaut wörtlich aus jurist/pruefung-google-ads-09-11.md Abschnitt (2) (Entwurf bis anwaltliche Prüfung). Sonst nichts geändert. Idempotent."""
import os, re, textwrap
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
J = open(os.path.expanduser('~/Claude/Koordinator/jurist/pruefung-google-ads-09-11.md'), encoding='utf8').read()
m = re.search(r'Abschnitt „Werbung bei Google und Auswertung“:\*\*\n„(.*?)“\n\*\*Variante B', J, re.S); assert m
absaetze = [a.strip() for a in m.group(1).split('\n') if a.strip()]; assert len(absaetze) == 2
f = 'datenschutz/index.html'; h = open(f, encoding='utf8').read()
if '§ 15 Werbung bei Google' in h: print('bereits'); raise SystemExit
text = '§ 15 Werbung bei Google und Auswertung\n' + '\n'.join('\n'.join(textwrap.wrap(a, 108, break_long_words=False, break_on_hyphens=False)) for a in absaetze) + '\n'
import html as H; text = H.escape(text, quote=False)
anker = 'BWW UG (haftungsbeschränkt) — Datenschutzerklärung (Stand: '
k = h.rindex(anker); assert h[k-1] == '\n'
h = h[:k] + text + h[k:]
open(f, 'w', encoding='utf8').write(h); print('eingefügt')
