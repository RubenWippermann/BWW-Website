#!/usr/bin/env python3
"""Ratgeber 'Brandschutzhelfer ausbilden: Dauer, Inhalte, Zahl' (idempotent)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ratgeber_lib import publish
FAQ = [
 ('Wie viele Brandschutzhelfer braucht ein Betrieb?',
  'Die Zahl ergibt sich aus der Gefährdungsbeurteilung. Bei normaler Brandgefährdung, etwa im Büro, nennt die DGUV fünf Prozent der Beschäftigten, bei erhöhter Gefährdung mehr.'),
 ('Wie lange dauert die Ausbildung?',
  'Die DGUV nennt mindestens zwei Unterrichtseinheiten à 45 Minuten Theorie plus praktische Übung. Ein Unfallversicherungsträger empfiehlt mindestens vier Stunden mit Löschübung.'),
 ('Wie oft wird aufgefrischt?',
  'Die DGUV empfiehlt eine Auffrischung im Abstand von zwei bis fünf Jahren, außerdem nach einem Brand oder bei geänderter Brandgefährdung.'),
]
BODY = '''<p class="answer-lead"><strong>Direkt beantwortet:</strong> Wie viele Brandschutzhelfer ein Betrieb braucht, legt die Gefährdungsbeurteilung fest. Als Ausgangswert nennt die DGUV bei normaler Brandgefährdung fünf Prozent der Beschäftigten. Die Ausbildung besteht aus Theorie von mindestens zwei Unterrichtseinheiten à 45 Minuten und einer praktischen Löschübung.</p>
<h2>Was Brandschutzhelfer tun</h2>
<p>Brandschutzhelfer bedienen Feuerlöscheinrichtungen und bekämpfen Entstehungsbrände, ohne sich selbst zu gefährden. Gemeint sind Brände mit so wenig Rauch und Wärme, dass man sich gefahrlos nähern kann. Alles darüber hinaus ist Sache der Feuerwehr. Sie kennen die Brandgefahren im Betrieb und helfen mit, dass sich alle Beschäftigten selbstständig in Sicherheit bringen können.</p>
<p>Der Arbeitgeber ist dafür verantwortlich. § 10 des Arbeitsschutzgesetzes verlangt Maßnahmen für Erste Hilfe, Brandbekämpfung und Evakuierung. Er muss dafür Beschäftigte benennen, und Anzahl, Ausbildung und Ausrüstung dieser Personen müssen zur Zahl der Beschäftigten und zu den besonderen Gefahren passen. Vor der Benennung ist der Betriebs- oder Personalrat zu hören.</p>
<h2>Zahl der Helfer</h2>
<p>Die DGUV nennt bei normaler Brandgefährdung, etwa in Büros, fünf Prozent der Beschäftigten als Ausgangswert. Bei erhöhter Gefährdung, zum Beispiel beim Schweißen oder Löten, können es mehr sein. Entscheidend ist immer die Gefährdungsbeurteilung des eigenen Betriebs.</p>
<p>Sie muss weitere Umstände einbeziehen: betriebsfremde Personen im Gebäude, Menschen mit eingeschränkter Mobilität, Schichtarbeit und flexible Arbeitszeiten oder Homeoffice. Es müssen jederzeit ausgebildete Personen vor Ort sein. Das spricht dafür, die Zahl nicht knapp zu planen. Den Rechner für den eigenen Betrieb findet ihr im <a href="/dguv-rechner/">DGUV-Rechner</a>.</p>
<h2>Inhalte und Dauer der Ausbildung</h2>
<p>Die Theorie behandelt die Grundzüge des vorbeugenden Brandschutzes, die Brandschutzorganisation des Betriebs, die Funktionsweise von Feuerlöschern, Brandgefahren und das Verhalten im Brandfall. Dafür sieht die DGUV mindestens zwei Unterrichtseinheiten à 45 Minuten vor, also mindestens 90 Minuten.</p>
<p>Dazu kommt die Praxis: Übungen mit verschiedenen Feuerlöschern, zum Beispiel mit Wasser oder CO₂. Wie lange sie dauert, nennt die DGUV nicht; sie hängt unter anderem von der Gruppengröße ab. Ein Unfallversicherungsträger schreibt, der Kurs sollte mindestens vier Stunden umfassen und eine praktische Löschübung enthalten.</p>
<p>Zusätzlich braucht es eine Einweisung in die betrieblichen Zuständigkeiten und Brandschutzmaßnahmen. Eine rein elektronische Schulung kann die persönliche mündliche Unterweisung nicht ersetzen.</p>
<h2>Wer ausbildet und wer zahlt</h2>
<p>Die Ausbildung übernehmen dafür geeignete Einrichtungen. Die Feuerwehr berät dabei, Hersteller und Wartungsfirmen von Feuerlöschern bieten praktische Löschübungen an. Die Kosten trägt der Arbeitgeber, anders als bei der Ausbildung in Erster Hilfe, die der Unfallversicherungsträger übernimmt. Prüft vor der Buchung, ob Theorie, Löschübung und die Einweisung in die eigenen Betriebsabläufe zusammen abgedeckt sind. Fehlt die Einweisung, muss sie im Betrieb nachgeholt werden.</p>
<h2>Auffrischung</h2>
<p>Die DGUV empfiehlt, die Ausbildung im Abstand von zwei bis fünf Jahren aufzufrischen. Zusätzlich bietet sich eine Auffrischung nach einem Brand an, bei Änderungen der Brandschutzordnung oder wenn sich die Brandgefährdung ändert. Unabhängig davon müssen alle Beschäftigten mindestens einmal im Jahr unterwiesen werden.</p>
<h2>Kurs bei BWW</h2>
<p>Der <a href="/kurse/brandschutzhelfer/">Brandschutzhelfer-Kurs</a> umfasst 4 Unterrichtseinheiten mit Theorie und Löschübung. Nach der Terminliste vom 02.11.2026 findet er am 10.12.2026 in Leinefelde-Worbis statt (50 € je Teilnehmer:in); weitere Termine sind der 18.03.2027 und der 26.06.2027. Die Kosten trägt in der Regel der Arbeitgeber, anders als bei der Ersten-Hilfe-Ausbildung. Wer mehrere Beschäftigte ausbilden will, kann den Kurs auch im eigenen Betrieb anfragen. Vertiefend: <a href="/wissen/brandschutzhelfer-anzahl/">Brandschutzhelfer: Anzahl und Aufgaben</a> und <a href="/wissen/brandschutzhelfer-ausbildung/">Brandschutzhelfer-Ausbildung</a>.</p>
'''
SRC = ('DGUV Arbeit &amp; Gesundheit: „Die Aufgaben von Brandschutzhelfern und Brandschutzhelferinnen“ (aug.dguv.de, 12.09.2022) · DGUV PlusPunkt (pluspunkt.dguv.de, 04.02.2025) · '
       'DGUV Information 205-023 „Brandschutzhelfer“ (publikationen.dguv.de) · § 10 ArbSchG (gesetze-im-internet.de) · VBG: Brandschutzhelfer (vbg.de). '
       'Die ASR A2.2 (Abschnitt 7.3) liegt als PDF vor; dieser Artikel stützt sich auf die genannten Webseiten. Abgerufen am 02.11.2026. Kein Ersatz für Rechtsberatung.')
publish(dict(
 base='wissen/brandschutzhelfer-ausbildung', slug='wissen/brandschutzhelfer-ausbilden-dauer-inhalte-zahl',
 title='Brandschutzhelfer ausbilden: Dauer, Inhalte, Zahl',
 desc='Brandschutzhelfer ausbilden: Wie viele ihr braucht (Gefährdungsbeurteilung, ca. 5 %), was die Ausbildung enthält und wie lange sie dauert. Mit Quellen.',
 day='2026-11-02', stand='02.11.2026', eyebrow='Ratgeber · Brandschutz',
 stand_src='DGUV Arbeit &amp; Gesundheit, DGUV PlusPunkt, DGUV Information 205-023, § 10 ArbSchG',
 lead='Brandschutzhelfer ausbilden lassen: Wie viele ein Betrieb braucht, was die Ausbildung enthält und wie lange sie dauert, nach den Angaben der DGUV.',
 cta=('/kurse/brandschutzhelfer/', 'Zum Brandschutzhelfer-Kurs'), faq=FAQ, body=BODY, src=SRC,
 related=[('/wissen/brandschutzhelfer-anzahl/', 'Anzahl und Aufgaben'), ('/wissen/brandschutzhelfer-ausbildung/', 'Brandschutzhelfer-Ausbildung'),
          ('/kurse/brandschutzhelfer/', 'Kurs Brandschutzhelfer'), ('/dguv-rechner/', 'DGUV-Rechner'), ('/wissen/brandschutzordnung/', 'Brandschutzordnung')],
 backlinks=['wissen/brandschutzhelfer-anzahl', 'wissen/brandschutzhelfer-ausbildung'], backlink_text='Brandschutzhelfer ausbilden: Dauer, Inhalte, Zahl'))
