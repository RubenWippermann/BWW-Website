#!/usr/bin/env python3
"""Belege auf der Seite (BL-Auftrag 02.11.): Überzogenes auf den Belegsatz kürzen. Nur Nicht-Rechtsseiten. Idempotent."""
import glob
n = 0
def rw(f, pairs):
    global n
    h = open(f, encoding='utf8').read(); o = h
    for a, b in pairs: h = h.replace(a, b)
    if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
FS = 'Ja. Unsere Erste-Hilfe-Ausbildung (9 UE) ist für die Führerscheinzulassung geeignet und zugleich als betrieblicher Erste-Hilfe-Kurs anerkannt.'
FN = 'Ja. Die Erste-Hilfe-Ausbildung nach § 26 DGUV Vorschrift 1 ist gleichwertig zur Schulung in Erster Hilfe nach § 19 Fahrerlaubnis-Verordnung. Achtet darauf, dass der entsprechende Vermerk auf eurer Teilnahmebescheinigung steht.'
rw('index.html', [(FS, FN), ('Einblicke aus Ausbildung, Rettungsdienstbildung und Kursalltag', 'Einblicke aus Ausbildung, Sanitätsdienst und Kursalltag')])
for f in ('index.html', 'kurse/index.html'): rw(f, [('Alle Stufen: Grundkurs, Aufbau, Fortbildung und Sanitätshelfer.', 'Alle Stufen: Grundkurs, Aufbau und Fortbildung.')])
rw('unternehmensprofil/index.html', [('<h2>Alleinstellungsmerkmale</h2>', '<h2>Auf einen Blick</h2>'),
    ('von der Deutschen Gesetzlichen Unfallversicherung (DGUV) ermächtigte Ausbildungsstelle', 'von der gesetzlichen Unfallversicherung ermächtigte Stelle')])
B = '<span class="trust-badge">Ermächtigte Stelle · Kennziffer 8.2122</span>'
rw('fuer-pflege/index.html', [(B, '<span class="trust-badge">Ermächtigte Stelle für Erste Hilfe im Betrieb · Kennziffer 8.2122</span>')])
rw('fuer-kitas/index.html', [(B, '<span class="trust-badge">Ermächtigte Stelle für Erste Hilfe im Betrieb · Kennziffer 8.2122</span>')])
rw('fuer-sanitaetsdienst/index.html', [(B, '<span class="trust-badge">Betriebssanitäter-Lehrgänge: geeignete Stelle (seit 29.10.2026) · Kennziffer 8.2122</span>')])
print('geändert:', n)
