#!/usr/bin/env python3
"""Datenschutzerklärung § 10: neuer Absatz 10.3 zum lokalen Speicher-Eintrag 'bww-privacy-ok', Wortlaut wörtlich aus jurist/antwort-localstorage-und-shop-hinweis-09-11.md (Teil 1). Sonst kein Rechtstext geändert. Idempotent."""
import os, textwrap
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'datenschutz/index.html'; h = open(f, encoding='utf8').read()
if '10.3 ' in h and 'bww-privacy-ok' in h: print('bereits'); raise SystemExit
TXT = ('10.3 Auf dieser Website speichern wir in Ihrem Browser (lokaler Speicher) einen Eintrag ‚bww-privacy-ok‘ mit dem Wert ‚1‘, '
       'sobald Sie den Hinweis zum Datenschutz wegklicken. Er dient allein dazu, den Hinweis nicht bei jedem Seitenaufruf erneut anzuzeigen, '
       'enthält keine Angaben zu Ihrer Person und wird nicht an uns übermittelt. Der Eintrag ist technisch erforderlich, damit Ihre Auswahl '
       'berücksichtigt wird (§ 25 Abs. 2 Nr. 2 TDDDG; Art. 6 Abs. 1 lit. f DSGVO). Sie können ihn jederzeit in den Einstellungen Ihres Browsers löschen.')
ZEILEN = '\n'.join(textwrap.wrap(TXT, 108, break_long_words=False, break_on_hyphens=False))
anker = 'Speicher jederzeit über die Einstellungen Ihres Browsers löschen.\n§ 11 '
assert h.count(anker) == 1
h = h.replace(anker, 'Speicher jederzeit über die Einstellungen Ihres Browsers löschen.\n' + ZEILEN + '\n§ 11 ')
open(f, 'w', encoding='utf8').write(h); print('eingefügt')
