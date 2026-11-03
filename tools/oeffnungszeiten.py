#!/usr/bin/env python3
"""Öffnungszeiten Mo–Fr 09:00–17:00 (Ruben 02.11.2026): Footer-Zeile, Kontaktseite, Organization-Schema (openingHoursSpecification). Idempotent."""
import glob, json, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
SPEC = {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:00"}
ADR = '<span>Worbiser Straße 2 · 37115 Duderstadt</span>'
ZEIT = '<span>Mo–Fr 09–17 Uhr</span>'
st = {'footer': 0, 'kontakt': 0, 'schema': 0}
def schema(m):
    j = json.loads(m.group(2))
    if j.get('@id', '').endswith('#organization') and 'telephone' in j and 'openingHoursSpecification' not in j:
        j['openingHoursSpecification'] = [SPEC]; st['schema'] += 1
        return m.group(1) + json.dumps(j, ensure_ascii=False, separators=(',', ':')) + m.group(3)
    return m.group(0)
for f in glob.glob('**/*.html', recursive=True):
    if f.startswith('tools/'): continue
    h = o = open(f, encoding='utf8').read()
    h = re.sub(r'(<script type="application/ld\+json">)(\{.*?\})(</script>)', schema, h, flags=re.S)
    if ADR in h and ADR + ZEIT not in h:
        h = h.replace(ADR, ADR + ZEIT); st['footer'] += 1
    if f == 'kontakt/index.html' and 'contact-lines' in h and 'Mo–Fr 09–17 Uhr</span></p>' not in h:
        h = h.replace('<span>Worbiser Straße 2 · 37115 Duderstadt</span></p>', '<span>Worbiser Straße 2 · 37115 Duderstadt</span><span>Mo–Fr 09–17 Uhr</span></p>'); st['kontakt'] += 1
    if h != o: open(f, 'w', encoding='utf8').write(h)
print(st)
