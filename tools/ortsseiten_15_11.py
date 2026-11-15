#!/usr/bin/env python3
"""Ortsseiten (BL 15.11.): Duesseldorf/Koeln/Hannover noindex,follow + Sitemap-Eintraege raus (kein belegter Kursort); Leinefelde-Worbis: ein Absatz zum Kursraum nur aus belegten Angaben
(Adresse Nordhaeuser Strasse 38 laut Datenblatt/Impressum der Worbis-Seite, offene Kurse im Feed ausschliesslich Leinefelde-Worbis); keine Fahrzeiten/Entfernungen. Titel/H1 unveraendert. Idempotent. Arbeitet im Verzeichnis des Aufrufs."""
import os, re
ROOT = os.getcwd()
for c in ('duesseldorf', 'koeln', 'hannover'):
    p = os.path.join(ROOT, 'standorte', 'erste-hilfe-kurs-' + c, 'index.html'); h = open(p, encoding='utf8').read()
    r = re.search(r'<meta name="robots" content="([^"]*)">', h); assert r, c
    if 'noindex' not in r.group(1): open(p, 'w', encoding='utf8').write(h.replace(r.group(0), '<meta name="robots" content="noindex,follow">', 1))
sp = os.path.join(ROOT, 'sitemap.xml'); sm = open(sp, encoding='utf8').read()
for c in ('duesseldorf', 'koeln', 'hannover'):
    sm = re.sub(r'<url><loc>https://www\.multiplikatorenstelle\.de/standorte/erste-hilfe-kurs-' + c + r'/</loc>.*?</url>\n?', '', sm)
open(sp, 'w', encoding='utf8').write(sm)
p = os.path.join(ROOT, 'standorte', 'erste-hilfe-kurs-leinefelde-worbis', 'index.html'); h = open(p, encoding='utf8').read()
ANK = 'und stimmen Termin, Zielgruppe und Inhalte sauber auf euren Standort ab.</p><div class="hero-actions">'
NEU = ('und stimmen Termin, Zielgruppe und Inhalte sauber auf euren Standort ab.</p>'
       '<p>Offene Kurse finden in unserem Kursraum in Leinefelde-Worbis statt (Nordhäuser Straße 38, 37339 Leinefelde-Worbis). Aktuelle Termine, Preise und die Buchung stehen in der '
       '<a href="/kurse/offene-kurse-worbis/">Liste der offenen Kurse</a>.</p><div class="hero-actions">')
if 'Kursraum in Leinefelde-Worbis' not in h:
    assert h.count(ANK) == 1; open(p, 'w', encoding='utf8').write(h.replace(ANK, NEU))
print('ok')
