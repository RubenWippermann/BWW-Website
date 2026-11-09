#!/usr/bin/env python3
"""booking.js: beim Seitenaufruf auch den früheren Schlüssel 'bww-bewertungen-v1' (Sitzungs- und lokaler Speicher) entfernen, damit die Aussage in Datenschutz § 10.1 stimmt. Token auf den Seiten mit booking.js. Idempotent."""
import glob, hashlib, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'assets/booking.js'; s = open(f, encoding='utf8').read()
if 'bww-bewertungen-v1' in s: print('bereits'); raise SystemExit
a = "    alt.forEach(function (k) { localStorage.removeItem(k); });\n  } catch (e) {}\n"
assert s.count(a) == 1
s = s.replace(a, a + "  try { sessionStorage.removeItem('bww-bewertungen-v1'); localStorage.removeItem('bww-bewertungen-v1'); } catch (e) {}   // abgeschaffter Bewertungs-Cache früherer Fassungen\n")
open(f, 'w', encoding='utf8').write(s)
tok = hashlib.sha1(s.encode()).hexdigest()[:8]; n = 0
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith('tools/'): continue
    h = open(p, encoding='utf8').read(); h2 = re.sub(r'(assets/booking\.js\?v=)[0-9a-f]+', lambda m: m.group(1) + tok, h)
    if h2 != h: open(p, 'w', encoding='utf8').write(h2); n += 1
print('angewendet; Token', tok, 'Seiten', n)
