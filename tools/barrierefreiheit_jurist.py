#!/usr/bin/env python3
"""Barrierefreiheitserklärung BWW: Tastatur- und Bilderaussage nach Jurist-Wortlaut (jurist/pruefung-barrierefreiheitserklaerungen-09-11.md, Entwurf bis anwaltliche Prüfung). Idempotent."""
import os
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'barrierefreiheit/index.html'; h = open(f, encoding='utf8').read(); n = 0
R = [('Es gibt einen Sprunglink zum Hauptinhalt, die Seiten lassen sich mit der Tastatur bedienen, und der Tastaturfokus ist sichtbar.',
      'Die Seiten sind für die Bedienung mit der Tastatur ausgelegt (sichtbarer Fokus, Sprunglink zum Inhalt); einen vollständigen Test nur mit der Tastatur und mit Screenreadern haben wir noch nicht durchgeführt.'),
     (' Die Bedienung nur mit der Tastatur und mit Screenreadern haben wir nicht abschließend geprüft.', ''),
     ('Bilder haben Alternativtexte; rein dekorative Bilder sind für Screenreader ausgeblendet.',
      'Inhaltstragende Bilder haben Alternativtexte; rein dekorative Bilder sind ausgeblendet.')]
for a, b in R:
    if a in h: n += h.count(a); h = h.replace(a, b)
open(f, 'w', encoding='utf8').write(h); print('Ersetzungen:', n)
