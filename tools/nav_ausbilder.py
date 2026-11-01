#!/usr/bin/env python3
"""Hauptnavigation: 'Lehrbeauftragte' -> 'Ausbilder werden' (Hub /fuer-ausbilder/) direkt nach 'Kurse'. Idempotent. Kein Dropdown (Unterseiten stehen im Hub)."""
import glob, re
PAT = re.compile(r'<a class="(\w*)" href="/fuer-sanitaetsdienst/">Betriebssanitäter</a><a class="(\w*)" href="/fuer-ausbilder/">Lehrbeauftragte</a>')
n = 0
for f in glob.glob('**/index.html', recursive=True) + ['404.html']:
    try: h = open(f, encoding='utf8').read()
    except FileNotFoundError: continue
    nh = PAT.sub(lambda m: f'<a class="{m.group(2)}" href="/fuer-ausbilder/">Ausbilder werden</a><a class="{m.group(1)}" href="/fuer-sanitaetsdienst/">Betriebssanitäter</a>', h)
    if nh != h: open(f, 'w', encoding='utf8').write(nh); n += 1
s = open('scripts/sync_headers.py', encoding='utf8').read()
old = "    ('/kurse/', 'Kurse'),\n    ('/inhouse-kurse/', 'Inhouse'),"
new = "    ('/kurse/', 'Kurse'),\n    ('/fuer-ausbilder/', 'Ausbilder werden'),\n    ('/fuer-sanitaetsdienst/', 'Betriebssanitäter'),\n    ('/inhouse-kurse/', 'Inhouse'),"
if old in s: open('scripts/sync_headers.py', 'w', encoding='utf8').write(s.replace(old, new)); n += 1
print('geändert:', n)
