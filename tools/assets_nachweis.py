#!/usr/bin/env python3
"""Bild-/Schrift-Check (Jurist 02.11.): Hero-Szene als KI-Symbolbild kennzeichnen. OFL.txt und ASSETS-HERKUNFT.md liegen als Dateien im Repo. Idempotent."""
f = 'index.html'; h = open(f, encoding='utf8').read(); o = h
h = h.replace('<p class="bildnachweis">Bild und Video: KI-generiert</p>', '<p class="bildnachweis">Symbolbild, Bild und Video KI-generiert, kein Foto eines BWW-Kursraums</p>')
h = h.replace('alt="Schulungsraum mit Übungspuppen für das Reanimationstraining"', 'alt="Schulungsraum mit Übungspuppen für das Reanimationstraining (KI-generiertes Symbolbild)"')
if h != o: open(f, 'w', encoding='utf8').write(h); print('geändert')
else: print('keine Änderung')
