#!/usr/bin/env python3
"""Fixes aus dem Seiten-Audit (02.11.): F1 beschreibende Ankertexte in Kurskarten, F2 'Anerkanntes Standardformat' -> 'Standardformat' (Belegsatz),
F3 /kurse/ Title+H1 mit 'Erste-Hilfe-Kurse', F4 /inhouse-kurse/ FAQ (Seitenquellen) + FAQPage + Kurslinks, F5 /kontakt/ H1 + Links. Rechtsseiten unberührt. Idempotent."""
import re, json, glob, html
n = 0
def rw(f, fn):
    global n
    h = open(f, encoding='utf8').read(); o = h; h = fn(h)
    if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
def esc(s): return s.replace('&', '&amp;')
# F1: beschreibende Ankertexte
def f1(h):
    def card(m):
        c = m.group(0); t = re.search(r'<h3>(.*?)</h3>', c)
        if not t: return c
        name = t.group(1)
        c = c.replace('>Termin buchen →</a>', f'>Termin buchen: {name} →</a>')
        c = c.replace('>Auch als Inhouse-Kurs buchbar →</a>', f'>{name} auch als Inhouse-Kurs →</a>')
        return c
    return re.sub(r'<article class="course-card".*?</article>', card, h, flags=re.S)
for f in ('index.html', 'kurse/index.html', 'fuer-sanitaetsdienst/index.html', 'fuer-ausbilder/index.html'): rw(f, f1)
# F2: Belegsatz
for f in glob.glob('**/index.html', recursive=True):
    if f.startswith(('agb/', 'datenschutz/', 'impressum/', 'widerruf/')): continue
    rw(f, lambda h: h.replace('Anerkanntes Standardformat mit viel Praxis', 'Standardformat mit viel Praxis').replace('anerkanntes Standardformat', 'Standardformat'))
# F3: /kurse/
T_OLD = 'Alle Kurse: Erste Hilfe, Brandschutz, Sanitäter | BWW'; T_NEW = 'Erste-Hilfe-Kurse, Brandschutz, Sanitäter: alle Kurse | BWW'
assert len(T_NEW) <= 60
rw('kurse/index.html', lambda h: h.replace(T_OLD, T_NEW).replace(esc(T_OLD), esc(T_NEW)).replace('<h1>Der passende Kurs für Team, Betrieb, Führerschein und Notfallmedizin.</h1>', '<h1>Erste-Hilfe-Kurse und mehr: der passende Kurs für Team, Betrieb, Führerschein und Notfallmedizin.</h1>'))
# F4: /inhouse-kurse/
FAQ = [('Was müssen wir für einen Inhouse-Kurs bereitstellen?', 'Ihr braucht nur einen geeigneten Raum mit mindestens 50 m² freier Fläche. Übungspuppen, AED-Trainer, Beatmungsmasken und Verbandmaterial bringen wir mit.'),
       ('Wohin kommt BWW für Inhouse-Kurse?', 'Wir kommen deutschlandweit direkt zu euch, in Betrieb, Schule, Kita oder Verein.'),
       ('Können Inhouse-Kurse online stattfinden?', 'Nein. Die Kurse leben von praktischen Übungen und finden in Präsenz statt, vor Ort bei euch.'),
       ('Wie schnell melden wir uns nach einer Anfrage?', 'In der Regel innerhalb eines Werktags.')]
def f4(h):
    if 'id="inhouse-faq"' in h: return h
    qa = ''.join(f'<h3>{esc(q)}</h3><p>{esc(a)}</p>' for q, a in FAQ)
    rel = ('<p class="article-related"><a href="/kurse/erste-hilfe-ausbildung/">Erste-Hilfe-Ausbildung inhouse</a><a href="/kurse/erste-hilfe-fortbildung/">Erste-Hilfe-Fortbildung inhouse</a>'
           '<a href="/kurse/brandschutzhelfer/">Brandschutzhelfer inhouse</a><a href="/fuer-sanitaetsdienst/">Betriebssanitäter-Lehrgänge</a><a href="/fuer-ausbilder/">Ausbilder werden</a><a href="/abrechnung/">Abrechnung über die Berufsgenossenschaft</a></p>')
    sec = f'<section class="section" id="inhouse-faq"><div class="section-head"><span class="eyebrow">Fragen</span><h2>Häufige Fragen zu Inhouse-Kursen</h2></div>{qa}{rel}</section>'
    k = h.find('<section class="section" id="anfrage">'); assert k > 0
    h = h[:k] + sec + h[k:]
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    return h.replace('</head>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + '</script></head>', 1)
rw('inhouse-kurse/index.html', f4)
# F5: /kontakt/
def f5(h):
    h = h.replace('<h1>Schreib uns – wir sind für dich da.</h1>', '<h1>Kontakt: Schreib uns – wir sind für dich da.</h1>')
    a = 'Wir melden uns in der Regel innerhalb eines Werktags.</p></div><img class="bww-ill" src="/media/illustrations/bww/care-emergency.webp"'
    b = 'Wir melden uns in der Regel innerhalb eines Werktags. Direkt zu den <a href="/kurse/">Kursen</a>, den <a href="/inhouse-kurse/">Inhouse-Kursen</a> oder zu <a href="/fuer-ausbilder/">Ausbilder werden</a>.</p></div><img class="bww-ill" src="/media/illustrations/bww/care-emergency.webp"'
    return h.replace(a, b, 1) if 'Direkt zu den <a href="/kurse/">Kursen</a>' not in h else h
rw('kontakt/index.html', f5)
print('geändert:', n)
