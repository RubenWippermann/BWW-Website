#!/usr/bin/env python3
"""Datenschutzerklärung: neuer § 14 'Kundenbereich' mit Verweisabsatz auf die Datenschutzerklärung der Kursverwaltung (Wortlaut Jurist/Website Manager 09.11.2026, Entwurf bis anwaltliche Prüfung). Sonst nichts geändert. Idempotent."""
import os, textwrap
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'datenschutz/index.html'; h = open(f, encoding='utf8').read()
if '§ 14 Kundenbereich' in h: print('bereits'); raise SystemExit
LINK = '<a href="https://software-wippermann.de/datenschutz">software-wippermann.de/datenschutz</a>'
ABS = 'Kundenbereich: Die Anmeldung und Sicherheitsmitteilungen sind in der Datenschutzerklärung der Kursverwaltung (' + LINK + ') beschrieben.'
# Umbruch auf Sichtlänge ohne den Link zu zerreißen
sichtbar = ABS.replace(LINK, 'XXLINKXX'); zeilen = textwrap.wrap(sichtbar, 108, break_long_words=False, break_on_hyphens=False)
text = '\n'.join(zeilen).replace('XXLINKXX', LINK)
anker = '\nBWW UG (haftungsbeschränkt) — Datenschutzerklärung (Stand: 02.11.2026) Seite 5 von 5</pre>'
assert h.count(anker) == 1
h = h.replace(anker, '\n§ 14 Kundenbereich\n' + text + anker)
open(f, 'w', encoding='utf8').write(h); print('eingefügt')
