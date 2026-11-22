#!/usr/bin/env python3
"""BWW /notruf-simulator/: WebApplication-JSON-LD nur mit belegten Feldern (23.11.2026, BL-Go SEO-Hebel).
name/url/description aus der Seite (canonical, Meta-Description), Offer 0 EUR nur, weil die Seite 'kostenlose Uebung ohne Anmeldung' sichtbar sagt.
Idempotent."""
import re, json
f = 'notruf-simulator/index.html'
t = open(f, encoding='utf-8').read()
if '"@type":"WebApplication"' in t:
    print('schon vorhanden'); raise SystemExit
desc = re.search(r'name="description" content="([^"]*)"', t).group(1)
url = re.search(r'rel="canonical" href="([^"]*)"', t).group(1)
assert 'kostenlose Übung ohne Anmeldung' in t
d = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Notruf-Simulator 112", "url": url,
     "description": desc, "inLanguage": "de", "applicationCategory": "EducationalApplication",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
     "provider": {"@type": "EducationalOrganization", "name": "BWW UG (haftungsbeschränkt)", "url": "https://www.multiplikatorenstelle.de/"}}
a = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage"'
assert t.count(a) == 1
t = t.replace(a, '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + '</script>' + a, 1)
open(f, 'w', encoding='utf-8').write(t); print('eingefuegt')
