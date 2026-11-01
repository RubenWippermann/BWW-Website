#!/usr/bin/env python3
"""Hub /fuer-ausbilder/ -> 'Ausbilder werden' (URL bleibt): Title/Description/H1, Antwort in 2 Sätzen, Eignung statt Ermächtigung im Badge,
Wegweiser zu den Landingseiten, LBEH nur als Qualifizierung nach Orientierungsrahmen. Idempotent."""
import re
def esc(s): return s.replace('&', '&amp;')
T = 'Ausbilder werden: Lehrkraft Erste Hilfe & Sanitäter | BWW'
D = 'Ausbilder werden in Erster Hilfe und im Sanitätsdienst: Lehrkräfte-Ausbildung, Fortbildung, Voraussetzungen, Preise und Termine bei BWW.'
assert len(T) <= 60 and len(D) <= 155
P = 'fuer-ausbilder/index.html'
h = open(P, encoding='utf8').read(); o = h
h = re.sub(r'<title>.*?</title>', f'<title>{esc(T)}</title>', h, 1)
h = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + esc(D) + '"', h, 1)
for a, v in (('og:title', T), ('og:description', D), ('twitter:title', T), ('twitter:description', D)):
    h = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*"' % a, lambda m: m.group(1) + esc(v) + '"', h, 1)
R = [('<span>Lehrkräfte und Lehrbeauftragte</span></nav><span class="eyebrow">Lehrkräfte und Lehrbeauftragte</span><h1>Lehrkräfte und Lehrbeauftragte Erste Hilfe: alle Stufen im Überblick.</h1><p>Wer selbst Erste-Hilfe-Kurse leiten will, braucht eine Lehrkräfte-Ausbildung und hält die Lehrbefähigung durch Fortbildung. Hier siehst du alle Stufen mit Dauer, Voraussetzungen und freien Terminen.</p>',
      '<span>Ausbilder werden</span></nav><span class="eyebrow">Ausbilder werden</span><h1>Ausbilder werden: Lehrkraft für Erste Hilfe und Sanitätsdienst.</h1><p>Wer selbst Erste-Hilfe-Kurse leiten will, braucht eine Lehrkräfte-Ausbildung und hält die Lehrberechtigung durch Fortbildung. Für den betrieblichen Sanitätsdienst gibt es eine eigene Lehrkräfte-Qualifikation; hier siehst du alle Stufen mit Dauer, Voraussetzungen und freien Terminen.</p>'),
     ('<span class="trust-badge">Ermächtigte Stelle · Kennziffer 8.2122</span>', '<span class="trust-badge">Geeignete Stelle für Lehrkräfte Erste Hilfe (seit 28.10.2025) · Kennziffer 8.2122</span>'),
     ('<p>Lehrkräfte-Ausbildung, Fortbildung und die Qualifizierung zum Lehrbeauftragten – die genauen Zugangsvoraussetzungen klären wir vor der Anmeldung mit dir.</p>',
      '<p>Lehrkräfte-Ausbildung, Fortbildung und die Lehrbeauftragten-Qualifizierung nach Orientierungsrahmen – die genauen Zugangsvoraussetzungen klären wir vor der Anmeldung mit dir.</p>'),
     ('<span>LBEH · mind. 120 UE</span><h3>Lehrbeauftragter Erste Hilfe</h3><p>Pädagogische Qualifizierung zum Lehrbeauftragten Erste Hilfe an 14 Tagen in Präsenz.</p>',
      '<span>LBEH · mind. 120 UE</span><h3>Lehrbeauftragten-Qualifizierung</h3><p>Qualifizierung nach dem Orientierungsrahmen der DGUV Grundsatz 304-003 an 14 Tagen in Präsenz; keine QSEH-registrierte Maßnahme.</p>'),
     ('<h3>Lehrbeauftragte · mind. 120 UE</h3><p>Pädagogische Qualifizierung nach DGUV Grundsatz 304-003 an 14 Tagen; Fortbildung für Lehrbeauftragte alle drei Jahre (24 UE).</p>',
      '<h3>Lehrbeauftragten-Qualifizierung · mind. 120 UE</h3><p>Qualifizierung nach dem Orientierungsrahmen der DGUV Grundsatz 304-003 an 14 Tagen (keine QSEH-registrierte Maßnahme); Fortbildung für Lehrbeauftragte alle drei Jahre (24 UE).</p>'),
     ('<h2>Der Weg zur Lehrberechtigung</h2>', '<h2>Der Weg zur Lehrberechtigung</h2>')]
for a, b in R: h = h.replace(a, b)
WEG = ('<section class="section" id="wege"><div class="section-head"><span class="eyebrow">Wegweiser</span><h2>Ausbilder werden: die Seiten im Überblick</h2></div>'
       '<ul class="check-list"><li><a href="/ausbilder-werden/erste-hilfe-lehrkraft/">Erste-Hilfe-Ausbilder werden</a>: Qualifikationsweg und Lehrkräfte-Ausbildung</li>'
       '<li><a href="/ausbilder-werden/betriebssanitaeter-lehrkraft/">Betriebssanitäter-Ausbilder werden</a>: lehrkraft für den betrieblichen Sanitätsdienst</li>'
       '<li><a href="/ausbilder-werden/lehrberechtigung-verlaengern/">Lehrberechtigung verlängern</a>: Fortbildung, Frist und Ablauf</li>'
       '<li><a href="/ausbilder-werden/lehrbeauftragter/">Künftige Lehrbeauftragte</a>: Voraussetzungen und Hospitation</li>'
       '<li>Für Zielgruppen: <a href="/ausbilder-werden/fuer-hilfsorganisationen/">Hilfsorganisationen</a>, <a href="/ausbilder-werden/fuer-ausbildungsstellen/">Ausbildungsstellen</a>, <a href="/ausbilder-werden/fuer-betriebe/">Betriebe</a></li>'
       '<li><a href="/ausbilder-werden/preise/">Preise</a>: Lehrkräfte-, Betriebssanitäter- und Hospitationspreise</li>'
       '<li><a href="/multiplikatorenstelle/">Multiplikatorenstelle</a>: Aufgaben und die DGUV-Grundsätze 304-001 bis 304-003</li></ul></section>').replace('lehrkraft für', 'Lehrkraft für')
if 'id="wege"' not in h:
    k = h.find('<section class="section-soft"><div class="section-head"><span class="eyebrow">Ablauf</span>'); assert k > 0
    h = h[:k] + WEG + h[k:]
if h != o: open(P, 'w', encoding='utf8').write(h); print('geändert')
else: print('keine Änderung')
