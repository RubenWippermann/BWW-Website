#!/usr/bin/env python3
"""Nachzug zur Neutralformel (Jurist-Bedingung): Anerkennungstext NIE in meta/og/twitter/JSON-LD; sichtbar direkt neben dem Preis. Idempotent."""
import os, re
ROOT = os.getcwd(); KURZ = 'Anerkennungsstatus: Auskunft vor Buchung auf Anfrage'
def rw(page, fn):
    p = os.path.join(ROOT, page, 'index.html'); h = open(p, encoding='utf8').read(); h2 = fn(h)
    if h2 != h: open(p, 'w', encoding='utf8').write(h2)
def jsonld_ohne_frage(h):
    # FAQPage-Eintrag zur Anerkennung aus dem JSON-LD entfernen (sichtbares FAQ im Fliesstext bleibt)
    h2, n = re.subn(r',\{"@type":"Question","name":"Wie steht es um die Anerkennung[^"]*","acceptedAnswer":\{"@type":"Answer","text":"[^"]*"\}\}', '', h)
    h2, m = re.subn(r'\{"@type":"Question","name":"Wie steht es um die Anerkennung[^"]*","acceptedAnswer":\{"@type":"Answer","text":"[^"]*"\}\},', '', h2)
    return h2
def meta_ohne(h): return h.replace('700 €. ' + KURZ + '.', '700 €.')
def preis(alt, neu):
    return lambda h: h.replace('<span class="fact-k">Preis</span><span class="fact-v">' + alt + '</span>', '<span class="fact-k">Preis</span><span class="fact-v">' + neu + '</span>')
rw('kurse/lehrbeauftragter-erste-hilfe', lambda h: preis('700 €', '700 € (' + KURZ + ')')(jsonld_ohne_frage(meta_ohne(h))))
rw('kurse/lehrbeauftragten-fortbildung', lambda h: preis('150 €', '150 € (' + KURZ + ')')(jsonld_ohne_frage(h)))
rw('fuer-ausbilder', jsonld_ohne_frage)
bad = []
for page in ('kurse/lehrbeauftragter-erste-hilfe', 'kurse/lehrbeauftragten-fortbildung', 'fuer-ausbilder', 'ausbilder-werden/preise', 'ausbilder-werden/lehrbeauftragter'):
    h = open(os.path.join(ROOT, page, 'index.html'), encoding='utf8').read()
    for t in re.findall(r'<meta[^>]*(?:description|og:|twitter:)[^>]*>', h):
        if re.search(r'Anerkennung|anerkannt|QSEH', t): bad.append((page, 'meta', t[:60]))
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        if re.search(r'Anerkennung|anerkannt|QSEH-?\s?reg', j) and 'hasCredential' not in j: bad.append((page, 'jsonld', re.search(r'.{40}(Anerkennung|anerkannt).{40}', j).group(0)))
print('ok; Reste in meta/og/twitter/JSON-LD:', bad)
