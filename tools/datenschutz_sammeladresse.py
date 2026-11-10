#!/usr/bin/env python3
"""Datenschutzerklärung § 16: Zusatzsatz zur gebündelten Zustellung an eine gemeinsame Firmen-/Einrichtungsadresse, wörtlich aus jurist/entscheidung-sammeladresse-bescheinigungen-09-11.md (Wortlaut-Ergänzung); steht direkt nach dem ersten Satz des Absatzes. Entwurf bis anwaltliche Prüfung, NICHT gepusht ohne BL. Stand-Zeile unverändert (erst am Push-Tag). Idempotent."""
import html as H, os, re, textwrap
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
J = open(os.path.expanduser('~/Claude/Koordinator/jurist/entscheidung-sammeladresse-bescheinigungen-09-11.md'), encoding='utf8').read()
SATZ = re.search(r'## Wortlaut-Ergänzung.*?\n„(.*?)“\n', J, re.S).group(1).strip()
f = 'datenschutz/index.html'; h = open(f, encoding='utf8').read()
K = '§ 16 Kursabwicklung und Teilnahmebescheinigung\n'
a = h.index(K) + len(K); b = h.index('BWW UG (haftungsbeschränkt) — Datenschutzerklärung (Stand:', a)
alt = h[a:b]; flach = re.sub(r'\s+', ' ', alt).strip()
if SATZ in H.unescape(flach): print('bereits'); raise SystemExit
ERSTER = 'Nach dem Kurs stellen wir Ihre Teilnahmebescheinigung aus und senden sie an die E-Mail-Adresse, die Sie angegeben haben.'
assert ERSTER in flach
neu = flach.replace(ERSTER, ERSTER + ' ' + H.escape(SATZ, quote=False), 1)
KOPF = '<b>Zustellung der Teilnahmebescheinigung.</b>'
assert neu.startswith(KOPF)
zeilen = textwrap.wrap(neu.replace(KOPF, 'KOPFXX', 1), 108, break_long_words=False, break_on_hyphens=False)
text = '\n'.join(zeilen).replace('KOPFXX', KOPF, 1) + '\n'
open(f, 'w', encoding='utf8').write(h[:a] + text + h[b:]); print('eingefügt')
