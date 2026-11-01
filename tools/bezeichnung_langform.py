#!/usr/bin/env python3
"""Bezeichnung nach Jurist-Nachtrag 3 (Rubens Aussage: 'BWW heißt Bildungswerk für Wiederbelebung und Erste Hilfe'): Langform nur als erläuternde Geschäftsbezeichnung MIT Rechtsform.
Kopf-Untertitel unverändert. Impressum nur Meta-Description. Unternehmensprofil H1/Einleitung/Schema; Startseite Schema; llms. Idempotent."""
import re, json
L = 'BWW – Bildungswerk für Wiederbelebung und Erste Hilfe'
n = 0
def rw(f, fn):
    global n
    h = open(f, encoding='utf8').read(); o = h; h = fn(h)
    if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
# Impressum: nur Meta-Description
rw('impressum/index.html', lambda h: h.replace('Impressum der BWW UG (haftungsbeschränkt), Bildungsstelle für Erste Hilfe und betrieblichen Sanitätsdienst. Anbieterkennzeichnung und Kontakt.',
                                               'Impressum der BWW UG (haftungsbeschränkt), ' + L + '. Anbieterkennzeichnung und Kontakt.'))
# Schema: name/legalName/alternateName
def schema(h):
    def fix(m):
        j = json.loads(m.group(1)); t = j.get('@type')
        if (isinstance(t, list) and 'EducationalOrganization' in t) or t == 'EducationalOrganization':
            if j.get('name') == 'BWW UG (haftungsbeschränkt)':
                j['legalName'] = 'BWW UG (haftungsbeschränkt)'; j['alternateName'] = ['BWW', 'Bildungswerk für Wiederbelebung und Erste Hilfe']
                return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(',', ':')) + '</script>'
        return m.group(0)
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, h, flags=re.S)
rw('index.html', schema); rw('unternehmensprofil/index.html', schema)
# Unternehmensprofil: H1, Einleitung
def prof(h):
    h = h.replace('<h1>BWW UG (haftungsbeschränkt) – Bildungswerk für Wiederbelebung und Erste Hilfe</h1>', '<h1>' + L + ': Unternehmensprofil der BWW UG (haftungsbeschränkt)</h1>')
    h = h.replace('<strong>BWW UG (haftungsbeschränkt)</strong> (Geschäftsbezeichnung: Bildungswerk für Wiederbelebung und Erste Hilfe) ist eine', '<strong>BWW UG (haftungsbeschränkt)</strong> ist eine')
    h = h.replace('<p>BWW UG (haftungsbeschränkt) ist ein gewerblicher Bildungsanbieter und keine Schule im Sinne der Schulgesetze.</p>',
                  '<p>Die BWW UG (haftungsbeschränkt) führt die Geschäftsbezeichnung „' + L + '“. Wir sind ein gewerblicher Bildungsanbieter und keine Schule im Sinne der Schulgesetze sowie keine öffentliche oder gemeinnützige Einrichtung.</p>')
    return h
rw('unternehmensprofil/index.html', prof)
# llms
rw('llms.txt', lambda h: h.replace('# BWW – Multiplikatorenstelle · Bildungsstelle für Erste Hilfe und betrieblichen Sanitätsdienst', '# BWW UG (haftungsbeschränkt): Multiplikatorenstelle · Bildungsstelle für Erste Hilfe und betrieblichen Sanitätsdienst', 1)
   .replace('> BWW (BWW UG, haftungsbeschränkt) ist ein deutscher Anbieter', '> BWW (BWW UG, haftungsbeschränkt; Geschäftsbezeichnung: ' + L + ') ist ein deutscher Anbieter', 1))
rw('llms-full.txt', lambda h: h.replace('Hauptüberschrift: BWW UG (haftungsbeschränkt) – Bildungswerk für Wiederbelebung und Erste Hilfe', 'Hauptüberschrift: ' + L + ': Unternehmensprofil der BWW UG (haftungsbeschränkt)', 1))
print('geändert:', n)
