#!/usr/bin/env python3
"""Korrektur nach Jurist-Prüfung der Commits (01.11., bww-commits-pruefung): Führerschein-Aussage, 'amtliche Anerkennung', 'anerkannt'/'DGUV-ermächtigt',
'Rettungsdienstbildungsstelle' (Impressum nur Meta-Description; Pflichtangaben unverändert). Idempotent."""
import glob, re
R = [  # (alt, neu) sitewide in index.html + llms
 ('Als <b>QSEH-ermächtigte Ausbildungsstelle</b> ist unser Erste-Hilfe-Nachweis für alle Führerscheinklassen anerkannt.',
  'Die Erste-Hilfe-Ausbildung nach § 26 DGUV Vorschrift 1 ist gleichwertig zur Schulung in Erster Hilfe nach § 19 Fahrerlaubnis-Verordnung. Achtet darauf, dass der entsprechende Vermerk auf eurer Teilnahmebescheinigung steht.'),
 ('Die Kennziffer <b>8.2122</b> könnt ihr bei eurem Unfallversicherungsträger nachprüfen. Das ist kein Werbeversprechen, sondern eine amtliche Anerkennung.',
  'Die Kennziffer <b>8.2122</b> lässt sich bei der QSEH bzw. bei eurem Unfallversicherungsträger nachprüfen.'),
 ('QSEH-ermächtigter Ausbildungsstelle', 'von der gesetzlichen Unfallversicherung ermächtigter Ausbildungsstelle'),
 ('DGUV-ermächtigte Ausbildungsstelle (Kennziffer 8.2122)', 'von der gesetzlichen Unfallversicherung ermächtigte Ausbildungsstelle für die betriebliche Erste-Hilfe-Aus- und Fortbildung (Kennziffer 8.2122)'),
 ('DGUV-ermächtigte Stelle', 'von der gesetzlichen Unfallversicherung ermächtigte Stelle'),
 ('BWW ist unter der Kennziffer 8.2122 anerkannt', 'BWW ist unter der Kennziffer 8.2122 ermächtigt'),
 ('DGUV-ermächtigt (8.2122)', 'ermächtigt (8.2122)'),
 ('Status als anerkannte Ausbildungsstelle', 'Status als ermächtigte Ausbildungsstelle'),
 ('Das anerkannte Standardformat für Betriebe', 'Das Standardformat für Betriebe'),
 ('Multiplikatoren- und Rettungsdienstbildungsstelle', 'Multiplikatorenstelle und Bildungsstelle für Erste Hilfe und betrieblichen Sanitätsdienst'),
 ('Multiplikatorenstelle und Rettungsdienstbildungsstelle', 'Multiplikatorenstelle und Bildungsstelle für Erste Hilfe und betrieblichen Sanitätsdienst'),
 ('Multiplikatorenstelle & Rettungsdienstbildungsstelle', 'Multiplikatorenstelle · Bildungsstelle für Erste Hilfe und betrieblichen Sanitätsdienst'),
 ('Multiplikatorenstelle &amp; Rettungsdienstbildungsstelle', 'Multiplikatorenstelle · Bildungsstelle für Erste Hilfe und betrieblichen Sanitätsdienst'),
]
DESC = [('unternehmensprofil/index.html', 'BWW-Unternehmensprofil: von der gesetzlichen Unfallversicherung ermächtigte Stelle (Kennziffer 8.2122), bundesweit Inhouse-Kurse für Erste Hilfe, Brandschutz und Betriebssanitäter.', 'BWW-Unternehmensprofil: ermächtigte Stelle der Unfallversicherung (Kennziffer 8.2122), Inhouse-Kurse für Erste Hilfe, Brandschutz und Betriebssanitäter.'),
        ('impressum/index.html', 'Impressum der BWW UG (haftungsbeschränkt), Multiplikatorenstelle und Bildungsstelle für Erste Hilfe und betrieblichen Sanitätsdienst. Anbieterkennzeichnung und Kontakt.', 'Impressum der BWW UG (haftungsbeschränkt), Bildungsstelle für Erste Hilfe und betrieblichen Sanitätsdienst. Anbieterkennzeichnung und Kontakt.'),
        ('unternehmen/index.html', 'inhouse, DGUV-ermächtigt, BG/UK-abrechenbar.', 'inhouse, ermächtigt, BG/UK-abrechenbar.')]
n = 0
for f in glob.glob('**/index.html', recursive=True) + ['404.html', 'llms.txt', 'llms-full.txt']:
    try: h = open(f, encoding='utf8').read()
    except FileNotFoundError: continue
    o = h
    if f == 'impressum/index.html':   # nur Meta-Description, Pflichtangaben im Rechtstext unverändert
        h = re.sub(r'(content="Impressum der BWW UG \(haftungsbeschränkt\), Multiplikatorenstelle und )Rettungsdienstbildungsstelle', r'\1Bildungsstelle für Erste Hilfe und betrieblichen Sanitätsdienst', h)
    elif not f.startswith(('datenschutz/', 'agb/', 'widerruf/')):
        for a, b in R: h = h.replace(a, b)
    if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
for f, a, b in DESC:
    h = open(f, encoding='utf8').read()
    if a in h: open(f, 'w', encoding='utf8').write(h.replace(a, b)); n += 1
print('geändert:', n)
