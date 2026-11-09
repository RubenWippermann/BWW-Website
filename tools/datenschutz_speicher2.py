#!/usr/bin/env python3
"""Datenschutzerklärung § 10 (10.1-10.3) wörtlich nach jurist/wortlaut-bww-ds-10-cookies-speicher-09-11.md (Entwurf bis anwaltliche Prüfung). Nur § 10 wird ersetzt. Idempotent."""
import os, re, textwrap
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
J = open(os.path.expanduser('~/Claude/Koordinator/jurist/wortlaut-bww-ds-10-cookies-speicher-09-11.md'), encoding='utf8').read()
teile = {n: re.search(r'\*\*' + re.escape(n) + r'\*\* (.*?)(?:\n|$)', J).group(1).strip() for n in ('10.1', '10.2', '10.3')}
f = 'datenschutz/index.html'; h = open(f, encoding='utf8').read()
a = h.index('§ 10 Cookies und lokale Speicherung im Browser\n') + len('§ 10 Cookies und lokale Speicherung im Browser\n'); b = h.index('§ 11 ', a)
neu = '\n'.join('\n'.join(textwrap.wrap(n + ' ' + t, 108, break_long_words=False, break_on_hyphens=False)) for n, t in teile.items()) + '\n'
if h[a:b] == neu: print('bereits'); raise SystemExit
open(f, 'w', encoding='utf8').write(h[:a] + neu + h[b:]); print('§ 10 ersetzt')
