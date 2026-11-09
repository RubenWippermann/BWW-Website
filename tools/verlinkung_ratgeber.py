#!/usr/bin/env python3
"""Interne Links von Kurs-/Zielgruppenseiten auf die neuen Ratgeber und schwach verlinkte Wissensseiten (GSC-Lücken 09.11.). Kein Wissensseiten-Inhalt, kein Title. Idempotent."""
import os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
L = lambda t, a: f'<a href="/{t}/">{a}</a>'
A, B, C = 'wissen/betriebssanitaeter-werden-ablauf-voraussetzungen', 'wissen/brandschutzhelfer-ausbilden-dauer-inhalte-zahl', 'wissen/erste-hilfe-lehrkraft-werden-voraussetzungen'
E_ = [('kurse/betriebssanitaeter-grundkurs', A, f'Ablauf und Voraussetzungen im Überblick: {L(A, "Betriebssanitäter werden")}.'),
      ('kurse/betriebssanitaeter-aufbau', A, f'Ablauf und Voraussetzungen im Überblick: {L(A, "Betriebssanitäter werden")}.'),
      ('fuer-sanitaetsdienst', A, f'Ablauf und Voraussetzungen im Überblick: {L(A, "Betriebssanitäter werden")}.'),
      ('kurse/brandschutzhelfer', B, f'Zahl der Helfer, Inhalte und Dauer: {L(B, "Brandschutzhelfer ausbilden")}.'),
      ('kurse/lehrkraefte-ausbildung-lk1', C, f'Voraussetzungen laut DGUV-Angaben: {L(C, "Erste-Hilfe-Lehrkraft werden")}.'),
      ('kurse/lehrkraefte-ausbildung-lk2', C, f'Voraussetzungen laut DGUV-Angaben: {L(C, "Erste-Hilfe-Lehrkraft werden")}.'),
      ('fuer-ausbilder', C, f'Voraussetzungen laut DGUV-Angaben: {L(C, "Erste-Hilfe-Lehrkraft werden")}.'),
      ('ausbilder-werden/erste-hilfe-lehrkraft', C, f'Voraussetzungen laut DGUV-Angaben: {L(C, "Erste-Hilfe-Lehrkraft werden")}.'),
      ('fuer-kitas', 'wissen/erste-hilfe-kita-pflicht', f'Pflichten und Zahl der Ersthelfer in der Kita: {L("wissen/erste-hilfe-kita-pflicht", "Erste Hilfe in der Kita")}.'),
      ('abrechnung', 'wissen/erste-hilfe-kurs-kosten-betrieb', f'Kosten für den Betrieb im Überblick: {L("wissen/erste-hilfe-kurs-kosten-betrieb", "Was kostet der Erste-Hilfe-Kurs den Betrieb wirklich?")}'),
      ('kurse/erste-hilfe-ausbildung', 'wissen/ersthelfer-pflicht-haftung', f'Pflicht, Rechte und Haftung beim Helfen: {L("wissen/ersthelfer-pflicht-haftung", "Erste Hilfe leisten")}.')]
n = 0
for src, tgt, sent in E_:
    f = src + '/index.html'; h = open(f, encoding='utf8').read(); i = h.find('<main')
    if f'href="/{tgt}/"' in h[i:]: continue
    m = re.search(r'<h1>.*?</h1>(?:<p class="article-stand">.*?</p>)?<p>.*?</p>', h[i:], re.S); assert m, src
    k = i + m.end()
    open(f, 'w', encoding='utf8').write(h[:k] + f'<p class="small-note">{sent}</p>' + h[k:]); n += 1
print('eingefügt:', n)
