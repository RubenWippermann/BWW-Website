#!/usr/bin/env python3
"""Telefonnummer sichtbar einheitlich wie im Impressum ('+49 (0) 5527 748 7518'): nur Fußzeile und noscript-Hinweise; tel:-Links bleiben unverändert. Impressum/Rechtsseiten-Fließtext nicht angefasst. Idempotent."""
import glob, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
NEU = '+49 (0) 5527 748 7518'
n_foot = n_nos = 0
for f in glob.glob('**/*.html', recursive=True):
    if f.startswith('tools/'): continue
    h = o = open(f, encoding='utf8').read()
    # Fußzeile: nur der sichtbare Text im tel:-Link des .footer-contact
    h, k = re.subn(r'(<p class="footer-contact"><a href="tel:\+4955277487518">(?:<svg.*?</svg>)?) \+49 5527 748 7518(</a>)', lambda m: m.group(1) + ' ' + NEU + m.group(2), h, flags=re.S)
    n_foot += k
    # noscript: "oder ruf an: 05527 7487518."
    h, k2 = re.subn(r'(<noscript>.*?ruf an: )05527 7487518(\.)', lambda m: m.group(1) + NEU + m.group(2), h, flags=re.S)
    n_nos += k2
    if h != o: open(f, 'w', encoding='utf8').write(h)
print('Fußzeilen:', n_foot, '| noscript:', n_nos)
