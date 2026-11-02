#!/usr/bin/env python3
"""Ratgeber 'Erste-Hilfe-Lehrkraft werden: Voraussetzungen' (idempotent)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ratgeber_lib import publish
FAQ = [
 ('Was braucht man, um Erste-Hilfe-Lehrkraft zu werden?',
  'Eine medizinisch-fachliche Grundqualifikation (Erste-Hilfe-Kurs und notfallmedizinische Ausbildung von mindestens 48 Unterrichtseinheiten) und eine pädagogische Grundqualifikation von mindestens 56 Unterrichtseinheiten. Dazu kommen mindestens zwei Hospitationen.'),
 ('Wie lange gilt die Lehrberechtigung?',
  'Lehrkräfte müssen innerhalb ihrer Lehrberechtigung alle drei Jahre mindestens 16 Unterrichtseinheiten fortgebildet werden: 8 medizinisch-fachlich und 8 pädagogisch.'),
 ('Was passiert, wenn die Fortbildung versäumt wird?',
  'Die Lehrberechtigung erlischt. In der Regel ist dann eine erneute Schulung zum Themenbereich II „Fachdidaktische Umsetzung Erste Hilfe“ mit mindestens 32 Unterrichtseinheiten nötig.'),
]
BODY = '''<p class="answer-lead"><strong>Direkt beantwortet:</strong> Erste-Hilfe-Lehrkraft wird, wer eine medizinisch-fachliche und eine pädagogische Grundqualifikation nachweist und mindestens zwei Hospitationen absolviert. Die DGUV nennt dafür mindestens 48 Unterrichtseinheiten notfallmedizinische Ausbildung und mindestens 56 Unterrichtseinheiten Pädagogik. Die pädagogische Qualifikation zählt nur bei einer Stelle, die dafür in der öffentlichen Liste der Unfallversicherung steht.</p>
<h2>Die medizinisch-fachliche Grundqualifikation</h2>
<p>Verlangt werden ein Erste-Hilfe-Kurs und eine notfallmedizinische Ausbildung von mindestens 48 Unterrichtseinheiten, zum Beispiel aus dem Sanitäts- oder Rettungsdienst. Einzelne Gesundheitsberufe kann die Qualitätssicherungsstelle gesondert beurteilen. Approbierte Ärztinnen und Ärzte müssen vor der pädagogischen Grundqualifikation keine medizinische Fortbildung nachweisen.</p>
<p>Das Alter dieser Qualifikation spielt eine Rolle. Wurde die pädagogische Grundqualifikation nach dem 01.01.2020 begonnen, darf die medizinische Qualifikation bei Kursbeginn höchstens drei Jahre alt sein. Ist sie älter, sind mindestens 16 Unterrichtseinheiten medizinisch-fachliche Fortbildung nachzuweisen. Alternativ genügt eine Bescheinigung über regelmäßige Erste-Hilfe-Maßnahmen im Beruf oder Ehrenamt.</p>
<h2>Die pädagogische Grundqualifikation</h2>
<p>Hier sind mindestens 56 Unterrichtseinheiten gefordert, aufbauend auf der medizinischen Qualifikation. Ein pädagogisches Studium oder eine gleichwertige Qualifikation von mindestens 200 Unterrichtseinheiten kann teilweise angerechnet werden. Dann müssen mindestens 32 Unterrichtseinheiten zum Themenbereich II „Fachdidaktische Umsetzung Erste Hilfe“ nachgewiesen werden.</p>
<p>Wichtig ist, wo ihr die Qualifikation erwerbt: Sie zählt nur, wenn die Stelle dafür von der Qualitätssicherungsstelle als geeignet festgestellt wurde und in der Liste unter „Lehrkräfte Erste Hilfe“ steht. Schaut vor der Buchung in diese Liste auf bg-qseh.de.</p>
<h2>Hospitation</h2>
<p>Vorgesehen sind mindestens zwei Hospitationen. Dabei sollen alle Themen der Erste-Hilfe-Ausbildung selbstständig und unter Betreuung erfahrener Mentorinnen und Mentoren gehalten werden. Grundsätzlich findet die Hospitation bei der Stelle statt, bei der die Lehrkraft später eingesetzt werden soll. Ist das nicht möglich, etwa bei der Neugründung eines Einzelunternehmens, kann sie bei der Stelle stattfinden, bei der die pädagogische Grundqualifikation absolviert wurde.</p>
<h2>Fortbildung und Verlängerung</h2>
<p>Innerhalb der Lehrberechtigung sind alle drei Jahre mindestens 16 Unterrichtseinheiten Fortbildung nötig, je 8 medizinisch-fachlich und pädagogisch. Mindestens 8 Unterrichtseinheiten müssen in Präsenz stattfinden, die übrigen können E-Learning enthalten.</p>
<p>Wer die Frist versäumt, verliert die Lehrberechtigung. Grundsätzlich ist dann eine erneute Schulung zum Themenbereich II mit mindestens 32 Unterrichtseinheiten nötig. Eine Ausnahme gibt es für alle, die im Berechtigungszeitraum mindestens 8 Unterrichtseinheiten anrechenbarer Fortbildungen besucht haben: Dann lassen sich die 32 Unterrichtseinheiten durch zusätzliche Fortbildungen aufsummieren, sofern alle in einen Drei-Jahres-Zeitraum fallen. Mehr dazu unter <a href="/ausbilder-werden/lehrberechtigung-verlaengern/">Lehrberechtigung verlängern</a>.</p>
<h2>Was die DGUV-Seite offen lässt</h2>
<p>Die Fragen und Antworten der DGUV nennen weder die Gesamtdauer des Weges noch die Kosten. Beides hängt davon ab, welche Teile der Grundqualifikation ihr bereits mitbringt und bei welcher Stelle ihr sie absolviert. Auch ein Datum trägt die Seite nicht. Bevor ihr plant, lohnt deshalb ein Blick in die aktuellen Vorgaben und eine Rückfrage bei der Stelle, bei der ihr später eingesetzt werden sollt.</p>
<h2>Kurse bei BWW</h2>
<p>Bei BWW gibt es die Lehrkräfte-Ausbildung in zwei Teilen. Nach der Terminliste vom 02.11.2026 beginnt die <a href="/kurse/lehrkraefte-ausbildung-lk1/">Lehrkräfte-Ausbildung Themenbereich I (24 UE)</a> am 31.01.2027 in Leinefelde-Worbis (150 € je Teilnehmer:in), die <a href="/kurse/lehrkraefte-ausbildung-lk2/">Themenbereich II (32 UE)</a> am 13.03.2027 (200 €). Die <a href="/kurse/lehrkraefte-fortbildung/">Lehrkräftefortbildung</a> kostet 100 € je Teilnehmer:in, der nächste Termin ist der 06.02.2027. Ob ein Kurs für eure Lehrberechtigung zählt, richtet sich nach den Vorgaben der Unfallversicherung und eurer Ausbildungsstelle. Fragt vor der Buchung nach.</p>
<p>Einen Überblick über Wege und Stufen findet ihr unter <a href="/ausbilder-werden/erste-hilfe-lehrkraft/">Erste-Hilfe-Ausbilder werden</a>, die fachlichen Hintergründe unter <a href="/wissen/erste-hilfe-ausbilder-werden-qualifikation/">Erste-Hilfe-Ausbilder werden: Qualifikation nach DGUV</a>.</p>
'''
SRC = ('DGUV Fachbereich Erste Hilfe: Fragen und Antworten zu Ausbildungsstellen, Abschnitt 4 „Lehrkräfte“ (dguv.de/fb-erstehilfe/ausbildungsstellen/fragen-und-antworten, ohne Datumsangabe der Seite) · '
       'Liste der Stellen: bg-qseh.de. Abgerufen am 02.11.2026. Maßgeblich sind die jeweils aktuellen Vorgaben der Unfallversicherung. Kein Ersatz für Rechtsberatung.')
publish(dict(
 base='wissen/erste-hilfe-ausbilder-werden-qualifikation', slug='wissen/erste-hilfe-lehrkraft-werden-voraussetzungen',
 title='Erste-Hilfe-Lehrkraft werden: Voraussetzungen',
 desc='Erste-Hilfe-Lehrkraft werden: medizinische und pädagogische Grundqualifikation, Hospitation und Fortbildung alle drei Jahre. Nach den Angaben der DGUV.',
 day='2026-11-02', stand='02.11.2026', eyebrow='Ratgeber · Ausbilder werden',
 stand_src='DGUV Fachbereich Erste Hilfe (Fragen und Antworten zu Ausbildungsstellen)',
 lead='Erste-Hilfe-Lehrkraft werden: welche medizinische und pädagogische Qualifikation verlangt wird, wie die Hospitation abläuft und wann die Lehrberechtigung erlischt.',
 cta=('/kurse/lehrkraefte-ausbildung-lk1/', 'Zur Lehrkräfte-Ausbildung'), faq=FAQ, body=BODY, src=SRC,
 related=[('/ausbilder-werden/erste-hilfe-lehrkraft/', 'Erste-Hilfe-Ausbilder werden'), ('/wissen/erste-hilfe-ausbilder-werden-qualifikation/', 'Qualifikation nach DGUV'),
          ('/ausbilder-werden/lehrberechtigung-verlaengern/', 'Lehrberechtigung verlängern'), ('/kurse/lehrkraefte-ausbildung-lk1/', 'Kurs LK1'),
          ('/kurse/lehrkraefte-ausbildung-lk2/', 'Kurs LK2'), ('/wissen/lehrkraefte-fortbildung-16-ue/', 'Fortbildung 16 UE')],
 backlinks=['wissen/erste-hilfe-ausbilder-werden-qualifikation'], backlink_text='Erste-Hilfe-Lehrkraft werden: Voraussetzungen'))
