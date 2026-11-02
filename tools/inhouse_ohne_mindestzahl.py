#!/usr/bin/env python3
"""Inhouse hat keine Mindestteilnehmerzahl: Aussagen auf BWW-Seiten neutral gefasst (idempotent)."""
import os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
NEU = 'Für Inhouse-Kurse gibt es keine Mindestteilnehmerzahl.'
R = {
 'standorte/erste-hilfe-kurs-hessen': [
  ('Anfahrt ab Duderstadt und ab wann sich Inhouse rechnet', 'Anfahrt ab Duderstadt und Inhouse-Termine'),
  ('Ein Inhouse-Kurs rechnet sich in der Regel ab etwa <strong>8–10 Teilnehmenden</strong> (eine Gruppe umfasst bis zu 20 Personen).', NEU + ' Eine Gruppe umfasst bis zu 20 Personen.'),
  ('Für einzelne Beschäftigte aus dem Rhein-Main-Gebiet sind unsere offenen Kurse oft der schnellere Weg.', 'Einzelne Beschäftigte aus dem Rhein-Main-Gebiet können auch einen unserer offenen Kurse besuchen.')],
 'standorte/erste-hilfe-kurs-nordrhein-westfalen': [
  ('ab wann sich Inhouse rechnet', 'Inhouse-Termine'),
  ('Ab etwa 10 Teilnehmenden trägt sich ein Inhouse-Kurs klar.', NEU),
  ('Ab etwa <strong>10 Teilnehmenden</strong> trägt sich ein Inhouse-Kurs klar.', NEU),
  ('einzelne Personen verweisen wir auf offene Kurse.', 'einzelne Personen können auch einen offenen Kurs besuchen.')],
 'standorte/erste-hilfe-kurs-bayern': [
  ('ab wann sich Inhouse rechnet', 'Inhouse-Termine'),
  ('Ob sich ein eigener Inhouse-Termin trägt, hängt bei euch weniger an einer festen Zahl als an der Bündelung: Ein gefüllter Kurstag ist das Ziel, notfalls über mehrere Standorte oder Betriebe hinweg zusammengestellt. Für Einzelanmeldungen bleiben die offenen Kurse die schlankere Lösung.',
   NEU + ' Wir planen den Termin gemeinsam mit euch und legen bei Bedarf mehrere Kurse auf denselben Aufenthalt. Einzelne Beschäftigte können auch einen offenen Kurs besuchen.')],
 '.': [
  ('Ab wie vielen Teilnehmenden lohnt sich ein Inhouse-Kurs?', 'Gibt es eine Mindestteilnehmerzahl für Inhouse-Kurse?'),
  ('Das stimmen wir individuell mit euch ab. Meist rechnet sich ein Inhouse-Kurs schon für kleinere Teams, weil ihr Anfahrt und Ausfallzeiten spart.', 'Nein, für Inhouse-Kurse gibt es keine Mindestteilnehmerzahl. Gruppengröße und Termin stimmen wir individuell mit euch ab.')],
}
n = 0
for p, subs in R.items():
    f = (p + '/index.html') if p != '.' else 'index.html'; h = open(f, encoding='utf8').read(); o = h
    for a, b in subs:
        if a in h: n += h.count(a); h = h.replace(a, b)
    if h != o: open(f, 'w', encoding='utf8').write(h)
print('Ersetzungen:', n)
