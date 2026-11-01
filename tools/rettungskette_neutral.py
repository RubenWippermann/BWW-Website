#!/usr/bin/env python3
"""Rettungskette neutral (Manager-Befund 02.11.): Zahl der Glieder ist je nach Quelle unterschiedlich -> keine '5 Glieder/5 Schritte'-Behauptung als Fakt.
Quellen gelesen (Suchtreffer, Abruf 02.11.2026): DGUV Information 204-022 (Mai 2017; Laienhilfe, Rettungsdienst, Krankenhaus), DRK 'Die Erste Hilfe Rettungskette' (4 Glieder). Idempotent."""
import re, json, html
def esc(s): return s.replace('&', '&amp;')
TITLE = 'Rettungskette: Glieder und Ablauf der Ersten Hilfe | BWW'
DESC = 'Die Rettungskette: Sofortmaßnahmen, Notruf 112, Erste Hilfe, Rettungsdienst, Krankenhaus. Warum die Zahl der Glieder je nach Quelle variiert.'
assert len(TITLE) <= 60 and len(DESC) <= 155, (len(TITLE), len(DESC))
NOTE = ('<div class="article-note"><strong>Hinweis zur Zahl der Glieder:</strong> Die Rettungskette wird je nach Quelle mit unterschiedlich vielen Gliedern dargestellt: '
        'Die DGUV Information 204-022 (Ausgabe Mai 2017) beschreibt Laienhilfe, Rettungsdienst und Krankenhaus, das Deutsche Rote Kreuz nennt vier Glieder. '
        'Dieser Beitrag verwendet eine Darstellung in fünf Gliedern, um Eigenschutz und Notruf einzeln zu zeigen. Abruf der Quellen: 02.11.2026.</div>')
Q2A = 'Sofortmaßnahmen und Eigenschutz, Notruf 112, Erste Hilfe, Rettungsdienst und Krankenhaus.'
Q2N = 'Das hängt von der Quelle ab: Die DGUV Information 204-022 beschreibt Laienhilfe, Rettungsdienst und Krankenhaus, das DRK nennt vier Glieder. In der Darstellung von BWW: Sofortmaßnahmen und Eigenschutz, Notruf 112, Erste Hilfe, Rettungsdienst und Krankenhaus.'
Q5A = 'Die Rettungskette besteht aus fünf Gliedern: 1. Sofortmaßnahmen und Eigenschutz, 2. Notruf 112, 3. Erste Hilfe durch Anwesende, 4. Rettungsdienst, 5. Krankenhaus. Die ersten drei Glieder liegen in den Händen von Laien.'
Q5N = 'Die Zahl hängt von der Quelle ab (z. B. vier Glieder beim DRK). BWW stellt die Kette in fünf Gliedern dar: 1. Sofortmaßnahmen und Eigenschutz, 2. Notruf 112, 3. Erste Hilfe durch Anwesende, 4. Rettungsdienst, 5. Krankenhaus. Die ersten Glieder liegen in den Händen von Laien.'
n = 0
f = 'wissen/rettungskette/index.html'; h = open(f, encoding='utf8').read(); o = h
h = re.sub(r'<title>.*?</title>', '<title>' + esc(TITLE) + '</title>', h, 1)
h = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + esc(DESC) + '"', h, 1)
for a in ('og:description', 'twitter:description'): h = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*"' % a, lambda m: m.group(1) + esc(DESC) + '"', h, 1)
for a in ('og:title', 'twitter:title'): h = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*"' % a, lambda m: m.group(1) + esc(TITLE.replace(' | BWW', ' | BWW Wissensdatenbank')) + '"', h, 1)
for a, b in (('Die Rettungskette: die fünf Glieder der Ersten Hilfe', 'Die Rettungskette: Glieder und Ablauf in der Ersten Hilfe'),
             ('Was ist die Rettungskette und welche fünf Glieder gehören dazu? Von den Sofortmaßnahmen über den Notruf bis zum Krankenhaus – das Prinzip verständlich erklärt.', 'Was ist die Rettungskette und welche Glieder gehören dazu? Von den Sofortmaßnahmen über den Notruf bis zum Krankenhaus – das Prinzip, mit Hinweis auf unterschiedliche Darstellungen.'),
             ('Stand: 01.11.2026 · Redaktion BWW · Quellen: DGUV Information 204-022', 'Stand: 02.11.2026 · Redaktion BWW · Quellen: DGUV Information 204-022 (Ausgabe Mai 2017), DRK: Die Erste Hilfe Rettungskette (Abruf 02.11.2026)'),
             ('<h2>Die fünf Glieder im Überblick</h2>', '<h2>Die Glieder im Überblick (BWW-Darstellung mit fünf Gliedern)</h2>'),
             ('<h2>Kurz gefasst</h2><ul><li><strong>Glied 1:</strong>', '<h2>Kurz gefasst (Darstellung in fünf Gliedern)</h2><ul><li><strong>Glied 1:</strong>'),
             ('Welche fünf Glieder hat die Rettungskette?', 'Welche Glieder hat die Rettungskette?'), ('Wie lauten die 5 Schritte der Rettungskette?', 'Wie viele Glieder hat die Rettungskette?'),
             (Q5A, Q5N), ('"dateModified":"2026-11-01"', '"dateModified":"2026-11-02"')):
    h = h.replace(a, b)
h = re.sub(r'(?<!In der Darstellung von BWW: )' + re.escape(Q2A), lambda _: Q2N, h)   # idempotent (Q2A ist Teilstring von Q2N)
if NOTE not in h:
    k = h.find('<div class="key-facts">'); assert k > 0
    h = h[:k] + NOTE + h[k:]
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S): json.loads(m.group(1))
if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
for f, a, b in (('wissen/index.html', 'Die Rettungskette: die fünf Glieder', 'Die Rettungskette: Glieder und Ablauf'), ('llms.txt', 'Die Rettungskette: die fünf Glieder', 'Die Rettungskette: Glieder und Ablauf')):
    t = open(f, encoding='utf8').read()
    if a in t: open(f, 'w', encoding='utf8').write(t.replace(a, b)); n += 1
print('geändert:', n)
