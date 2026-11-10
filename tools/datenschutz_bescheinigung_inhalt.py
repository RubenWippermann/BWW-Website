#!/usr/bin/env python3
"""Datenschutzerklaerung § 16: ein Ergaenzungssatz (Wortlaut Leitstelle/BL 10.11.) direkt hinter dem Sammelzustell-Satz. Entwurf bis anwaltliche Pruefung. Stand-Zeile unveraendert (erst am Push-Tag). Idempotent."""
import html as H, os, re, textwrap
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
NEU = ('Jede Bescheinigung enthält Ihren Namen, die Kursdaten und Ihr Geburtsdatum; wir senden sie so nur an Firmen- oder Einrichtungsadressen '
       '(nicht an Adressen von E-Mail-Anbietern wie gmail.com oder web.de) und ohne Abruf-Link. Wenn Sie nur persönlich beliefert werden möchten, '
       'geben Sie eine eigene Adresse an oder widersprechen Sie (Art. 21 DSGVO).')
VOR = 'Haben mehrere Teilnehmende eines Kurses dieselbe Firmen- oder Einrichtungsadresse angegeben, senden wir die Bescheinigungen gebündelt an diese Adresse (eine E-Mail mit je einer Bescheinigung pro Person).'
f = 'datenschutz/index.html'; h = open(f, encoding='utf8').read()
K = '§ 16 Kursabwicklung und Teilnahmebescheinigung\n'
a = h.index(K) + len(K); b = h.index('BWW UG (haftungsbeschränkt) — Datenschutzerklärung (Stand:', a)
flach = re.sub(r'\s+', ' ', h[a:b]).strip()
if NEU in H.unescape(flach): print('bereits'); raise SystemExit
assert VOR in H.unescape(flach)
neu = H.unescape(flach).replace(VOR, VOR + ' ' + NEU, 1)
neu = H.escape(neu, quote=False).replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')
KOPF = '<b>Zustellung der Teilnahmebescheinigung.</b>'
assert neu.startswith(KOPF)
z = textwrap.wrap(neu.replace(KOPF, 'KOPFXX', 1), 108, break_long_words=False, break_on_hyphens=False)
open(f, 'w', encoding='utf8').write(h[:a] + '\n'.join(z).replace('KOPFXX', KOPF, 1) + '\n' + h[b:]); print('eingefügt')
