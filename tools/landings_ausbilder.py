#!/usr/bin/env python3
"""Landingseiten 'Ausbilder werden' (Strategie Branchen-Experte, 01.11.2026): L1 Erste-Hilfe-Lehrkraft, L3 Lehrbeauftragter, L4 Multiplikatorenstelle.
Baut aus der Wissensseite 304-003 (Kopf/Fuß/Skripte) neue Seiten; Texte nur aus bestehenden Seiten/Feed/DGUV-Quellen. Idempotent.
Belegsätze neutral ('ermächtigte Stelle ...'), keine Superlative, kein Preisvergleich. Preise: Feed software-wippermann.de/api/kurse?org=bww, Stand 01.11.2026."""
import re, json, os, html, sys

BASE = 'wissen/multiplikatorenstelle-dguv-grundsatz-304-003/index.html'
HOST = 'https://www.multiplikatorenstelle.de'
STAND = '01.11.2026'
esc = lambda s: s.replace('&', '&amp;')
BEL6 = 'BWW bildet betriebliche Ersthelfer aus und fort und ist dafür ermächtigte Stelle der gesetzlichen Unfallversicherung (Kennziffer 8.2122, seit 28.10.2025). Geeignete Stelle ist BWW für die Aus- und Fortbildung von Lehrkräften der Ersten Hilfe (seit 28.10.2025) sowie von Lehrkräften des betrieblichen Sanitätsdienstes und von Betriebssanitätern (seit 29.10.2026). Die ermächtigten bzw. geeigneten Stellen führt die Qualitätssicherungsstelle Erste Hilfe (QSEH) der gesetzlichen Unfallversicherungsträger in einer öffentlichen Liste.'
QL = 'Die ermächtigten bzw. geeigneten Stellen führt die Qualitätssicherungsstelle Erste Hilfe (QSEH) der gesetzlichen Unfallversicherungsträger in einer öffentlichen Liste.'
BELEG = '<!-- Beleg offen: Ermächtigungsbescheid UV-Träger (Kennziffer 8.2122) je Lehrgangsart; Wortlaut vom Jurist -->'

def faq_html(faqs): return ''.join(f'<h3>{esc(q)}</h3><p>{a}</p>' for q, a in faqs)
def strip_tags(s): return re.sub(r'<[^>]+>', '', s)

PAGES = [
 dict(path='ausbilder-werden/erste-hilfe-lehrkraft/', img='teacher-training', eyebrow='Ausbilder werden',
  title='Erste-Hilfe-Ausbilder werden: Lehrkräfte-Ausbildung | BWW',
  desc='Wer Erste-Hilfe-Kurse leiten will, braucht die Lehrkräfte-Ausbildung nach DGUV Grundsatz 304-003. Voraussetzungen, Dauer, Preis und Termine.',
  h1='Erste-Hilfe-Ausbilder werden: so führt die Lehrkräfte-Ausbildung zum Ziel',
  quellen='DGUV Grundsatz 304-003',
  lead='Wer betriebliche Erste-Hilfe-Kurse leiten will, braucht eine medizinische Grundqualifikation, eine pädagogische Qualifikation und Praxis unter Betreuung. Bei BWW gibt es die Lehrkräfte-Ausbildung in zwei Stufen: Themenbereich I (24 UE) und Themenbereich II (32 UE).',
  cta=[('/kurse/lehrkraefte-ausbildung-lk1/', 'Themenbereich I ansehen', 'primary'), ('/kurse/lehrkraefte-ausbildung-lk2/', 'Themenbereich II ansehen', 'ghost')],
  keyfacts=['<strong>Medizinisch:</strong> Erste-Hilfe-Kurs plus mindestens 48 Unterrichtseinheiten (UE) notfallmedizinische Ausbildung',
            '<strong>Pädagogisch:</strong> mindestens 56 UE',
            '<strong>Praxis:</strong> mindestens zwei Hospitationen',
            '<strong>Fortbildung:</strong> mindestens alle drei Jahre, mindestens 16 UE (8 medizinisch-fachlich, 8 pädagogisch)'],
  body='''<h2>Die Stufen bei BWW</h2>
<ul><li><strong><a href="/kurse/lehrkraefte-ausbildung-lk1/">Lehrkräfte-Ausbildung Themenbereich I (LK1)</a>:</strong> 24 UE, 150 € je Person. Methodik und Didaktik der Erwachsenenbildung, Aufbau von Lernformaten, sichere Demonstration der praktischen Maßnahmen.</li>
<li><strong><a href="/kurse/lehrkraefte-ausbildung-lk2/">Lehrkräfte-Ausbildung Themenbereich II (LK2)</a>:</strong> 32 UE, 200 € je Person. Vertiefte Didaktik, eigene Lehrproben mit Feedback, Qualitätssicherung und Organisation im Kursbetrieb.</li>
<li><strong><a href="/kurse/lehrkraefte-fortbildung/">Lehrkräfte-Fortbildung</a>:</strong> hält die Lehrberechtigung aktuell; Preise und Termine auf der Kursseite.</li></ul>
<p class="small-note">Preise je Person laut Buchungssystem, Stand ''' + STAND + '''. Verbindlich sind die Angaben auf der jeweiligen Kursseite.</p>
<h2>Der Weg in drei Schritten</h2>
<p><strong>1. Medizinisch-fachliche Grundqualifikation:</strong> ein Erste-Hilfe-Kurs und eine notfallmedizinische Ausbildung im Umfang von mindestens 48 UE, zum Beispiel eine sanitäts- oder rettungsdienstliche Ausbildung. <strong>2. Pädagogische Qualifikation:</strong> mindestens 56 UE, bei einer Stelle, deren Eignung für die Lehrkräfte-Ausbildung die Qualitätssicherungsstelle Erste Hilfe (QSEH) festgestellt hat. <strong>3. Praxis:</strong> mindestens zwei Hospitationen unter Betreuung. Die Einzelheiten erklärt der Beitrag <a href="/wissen/erste-hilfe-ausbilder-werden-qualifikation/">Erste-Hilfe-Ausbilder werden: Qualifikationsweg nach DGUV</a>.</p>
<h2>Bei wem man die Lehrkräfte-Ausbildung macht</h2>
<p>Die pädagogische Qualifikation zählt nur, wenn sie bei einer geeigneten Stelle erworben wurde. Prüft deshalb vor der Buchung die Liste ermächtigter Stellen im Bereich „Lehrkräfte Erste Hilfe“. BWW ist ermächtigte Stelle für die Erste-Hilfe-Aus- und Fortbildung im Betrieb (Kennziffer 8.2122) und geeignete Stelle für die Aus- und Fortbildung von Lehrkräften der Ersten Hilfe (seit 28.10.2025). Die ermächtigten bzw. geeigneten Stellen führt die Qualitätssicherungsstelle Erste Hilfe (QSEH) der gesetzlichen Unfallversicherungsträger in einer öffentlichen Liste.</p>''',
  faq=[('Was braucht man, um Erste-Hilfe-Ausbilder zu werden?', 'Medizinisch einen Erste-Hilfe-Kurs plus mindestens 48 Unterrichtseinheiten notfallmedizinische Ausbildung, pädagogisch mindestens 56 Unterrichtseinheiten und mindestens zwei Hospitationen (DGUV Grundsatz 304-003). Die medizinische Qualifikation darf bei Kursbeginn nicht älter als drei Jahre sein, wenn die pädagogische Grundqualifikation nach dem 1. Januar 2020 beginnt.'),
       ('Wie lange dauert die Lehrkräfte-Ausbildung bei BWW?', 'Themenbereich I umfasst 24 Unterrichtseinheiten, Themenbereich II 32 Unterrichtseinheiten. Die aktuellen Termine stehen auf den Kursseiten und sind online buchbar.'),
       ('Wie oft ist eine Fortbildung für Lehrkräfte nötig?', 'Innerhalb der Gültigkeit der Lehrberechtigung, mindestens alle drei Jahre, im Umfang von mindestens 16 Unterrichtseinheiten, davon 8 medizinisch-fachlich und 8 pädagogisch (DGUV Grundsatz 304-003).'),
       ('Woran erkenne ich eine geeignete Stelle für die Lehrkräfte-Ausbildung?', 'Die QSEH stellt die Eignung fest. Maßgeblich ist die Liste der ermächtigten Stellen im Bereich „Lehrkräfte Erste Hilfe“; nur dort erworbene pädagogische Qualifikationen werden anerkannt. BWW ist ermächtigte Stelle für die Erste-Hilfe-Aus- und Fortbildung im Betrieb (Kennziffer 8.2122) und geeignete Stelle für die Aus- und Fortbildung von Lehrkräften der Ersten Hilfe (seit 28.10.2025).')],
  related=[('/fuer-ausbilder/', 'Ausbilder werden: alle Stufen'), ('/ausbilder-werden/lehrbeauftragter/', 'Lehrbeauftragter Erste Hilfe'), ('/multiplikatorenstelle/', 'Multiplikatorenstelle'), ('/wissen/lehrkraefte-erste-hilfe/', 'Lehrkräfte in der Erste-Hilfe-Ausbildung'), ('/wissen/lehrkraefte-fortbildung-16-ue/', 'Lehrkräfte-Fortbildung (16 UE)')]),
 dict(path='ausbilder-werden/betriebssanitaeter-lehrkraft/', img='teacher-training', eyebrow='Ausbilder werden',
  title='Betriebssanitäter-Ausbilder werden: Lehrkraft | BWW',
  desc='Lehrkraft für den betrieblichen Sanitätsdienst werden: zwei einzeln buchbare Teile mit 16 und 8 UE. Dazu die Betriebssanitäter-Lehrgänge, Termine online.',
  h1='Betriebssanitäter-Ausbilder werden: Lehrkraft betrieblicher Sanitätsdienst',
  quellen='DGUV Grundsatz 304-003, DGUV Grundsatz 304-002',
  lead='Wer andere zu Betriebssanitätern ausbilden will, braucht die Qualifikation als Lehrkraft für den betrieblichen Sanitätsdienst. Bei BWW besteht sie aus zwei einzeln buchbaren Teilen: Ausbildung (16 UE, 2 Tage, 100 €) und Arbeitsschutzschulung (8 UE, 1 Tag, 50 €).',
  cta=[('/kurse/lehrkraefte-ausbildung-sanitaetsdienst/', 'Lehrkraft Sanitätsdienst ansehen', 'primary'), ('/kurse/betriebssanitaeter-grundkurs/', 'Betriebssanitäter-Grundkurs', 'ghost')],
  keyfacts=['<strong>Teil a:</strong> Ausbildung Lehrkraft betrieblicher Sanitätsdienst, 16 UE, 2 Tage, 100 € je Person',
            '<strong>Teil b:</strong> Arbeitsschutzschulung Lehrkraft Betriebssanitätsdienst, 8 UE, 1 Tag, 50 € je Person',
            '<strong>Grundlage:</strong> DGUV Grundsatz 304-003 (Teil a: Anhang 4a, Teil b: Anhang 4b)',
            '<strong>Stelle:</strong> geeignete Stelle für Lehrkräfte des betrieblichen Sanitätsdienstes und für Betriebssanitäter, seit 29.10.2026 (Kennziffer 8.2122)'],
  body="""<h2>Die zwei Teile der Lehrkräfte-Qualifikation</h2>
<p>Beide Teile sind einzeln buchbar und finden in Präsenz statt (UE = 45 Minuten). <a href="/kurse/lehrkraefte-ausbildung-sanitaetsdienst/">Teil a und Teil b mit allen Terminen</a> stehen auf der Kursseite.</p>
<p class="small-note">Preise je Person laut Buchungssystem, Stand """ + STAND + """. Verbindlich sind die Angaben auf der jeweiligen Kursseite.</p>
<h2>Die Betriebssanitäter-Lehrgänge bei BWW</h2>
<ul><li><a href="/kurse/betriebssanitaeter-grundkurs/">Grundkurs</a>: 63 UE nach DGUV Grundsatz 304-002 zuzüglich Prüfung, 450 € je Person.</li>
<li><a href="/kurse/betriebssanitaeter-aufbau/">Aufbaulehrgang</a>: 32 UE zuzüglich Prüfung, 250 € je Person.</li>
<li><a href="/kurse/betriebssanitaeter-fortbildung/">Fortbildung</a> für bestehende Betriebssanitäter.</li></ul>
<h2>Zur Einordnung</h2>
<p>BWW ist geeignete Stelle zur Aus- und Fortbildung von Lehrkräften des betrieblichen Sanitätsdienstes und von Betriebssanitätern (seit 29.10.2026, Kennziffer 8.2122). Die Eignung für Lehrkräfte des betrieblichen Sanitätsdienstes gilt nur zusammen mit der Ermächtigung für die Erste-Hilfe-Aus- und Fortbildung und der Eignung für Betriebssanitäter. Die ermächtigten bzw. geeigneten Stellen führt die Qualitätssicherungsstelle Erste Hilfe (QSEH) der gesetzlichen Unfallversicherungsträger in einer öffentlichen Liste.</p>""",
  faq=[('Was ist eine Lehrkraft für den betrieblichen Sanitätsdienst?', 'Eine Person, die Betriebssanitäter ausbildet. Die Qualifikation richtet sich nach DGUV Grundsatz 304-003.'),
       ('Aus welchen Teilen besteht die Qualifikation bei BWW?', 'Aus zwei einzeln buchbaren Teilen: Ausbildung Lehrkraft betrieblicher Sanitätsdienst (16 UE, 2 Tage, 100 €) und Arbeitsschutzschulung für Lehrkräfte im Betriebssanitätsdienst (8 UE, 1 Tag, 50 €).'),
       ('Welche Betriebssanitäter-Lehrgänge bietet BWW an?', 'Den Grundkurs (63 UE zuzüglich Prüfung), den Aufbaulehrgang (32 UE zuzüglich Prüfung) und die Fortbildung für Betriebssanitäter, jeweils nach DGUV Grundsatz 304-002.'),
       ('Seit wann ist BWW dafür geeignete Stelle?', 'Als geeignete Stelle für Lehrkräfte des betrieblichen Sanitätsdienstes und für Betriebssanitäter seit dem 29.10.2026 (Kennziffer 8.2122).')],
  related=[('/fuer-ausbilder/', 'Ausbilder werden: alle Stufen'), ('/ausbilder-werden/erste-hilfe-lehrkraft/', 'Erste-Hilfe-Ausbilder werden'), ('/multiplikatorenstelle/', 'Multiplikatorenstelle'), ('/wissen/betriebssanitaeter-ausbildung/', 'Betriebssanitäter-Ausbildung'), ('/wissen/ersthelfer-oder-betriebssanitaeter/', 'Ersthelfer oder Betriebssanitäter?')]),
 dict(path='ausbilder-werden/lehrbeauftragter/', img='teacher-training', eyebrow='Ausbilder werden',
  title='Künftige Lehrbeauftragte: Voraussetzungen, Hospitation | BWW',
  desc='Voraussetzungen für künftige Lehrbeauftragte Erste Hilfe nach DGUV Grundsatz 304-003 und die Hospitation in der Lehrkräftequalifizierung bei BWW.',
  h1='Künftige Lehrbeauftragte Erste Hilfe: Voraussetzungen und Hospitation',
  topnote='<strong>Hinweis:</strong> „Lehrbeauftragte“ ist die Funktionsbezeichnung der gesetzlichen Unfallversicherung nach DGUV Grundsatz 304-003 (Abschnitt 2.2.2), keine Hochschulfunktion. Über die Funktion entscheidet die jeweilige Ausbildungsstelle. Lehrgänge nach dem Orientierungsrahmen in Anhang 3 sind keine beim QSEH-Portal registrierten Maßnahmen.',
  quellen='DGUV Grundsatz 304-003',
  lead='Angehende Lehrbeauftragte müssen mindestens in einer kompletten Lehrkräftequalifizierung einer Ausbildungsstelle hospitieren. Bei BWW kostet die Hospitation den Kurspreis plus 25 € je Kurstag.',
  cta=[('/kontakt/', 'Hospitation anfragen', 'primary'), ('/ausbilder-werden/erste-hilfe-lehrkraft/', 'Lehrkräfte-Ausbildung ansehen', 'ghost')],
  keyfacts=['<strong>Hospitation:</strong> mindestens eine komplette Lehrkräftequalifizierung einer Ausbildungsstelle',
            '<strong>Kosten bei BWW:</strong> Kurspreis plus 25 € je Kurstag',
            '<strong>Pädagogisch:</strong> Qualifikation als Lehrkraft Erste Hilfe und pädagogische Schulung von insgesamt mindestens 120 UE',
            '<strong>Fortbildung:</strong> mindestens alle drei Jahre, 24 UE (16 pädagogisch, 8 medizinisch-fachlich)'],
  body="""<h2>Voraussetzungen</h2>
<p>Nach DGUV Grundsatz 304-003 (Abschnitt 2.2.2) sind medizinisch-fachlich mindestens eine Erste-Hilfe-Ausbildung (9 UE) und eine Sanitätsausbildung mit bestandener Prüfung (48 UE) nötig. Pädagogisch verlangt der Grundsatz die Qualifikation als Lehrkraft Erste Hilfe sowie eine pädagogische Schulung von insgesamt mindestens 120 UE. Vor Abschluss der 120 UE ist in der Regel ein Nachweis über 12 Aus- oder Fortbildungen in Erster Hilfe (nicht älter als 3 Jahre) zu erbringen.</p>
<h2>Der Weg zur Qualifizierung</h2>
<ul><li>Zuerst die Qualifikation als <a href="/ausbilder-werden/erste-hilfe-lehrkraft/">Lehrkraft Erste Hilfe</a> erwerben.</li>
<li>Hospitation in einer kompletten Lehrkräftequalifizierung einer Ausbildungsstelle. Bei BWW: Kurspreis plus 25 € je Kurstag, Anfrage über den <a href="/kontakt/">Kontakt</a>.</li>
<li>Pädagogische Schulung im Umfang von insgesamt mindestens 120 UE nach dem Orientierungsrahmen in Anhang 3 der DGUV Grundsatz 304-003.</li>
<li>Fortbildung alle drei Jahre im Umfang von 24 UE.</li></ul>""",
  faq=[('Was macht ein Lehrbeauftragter Erste Hilfe?', 'Lehrbeauftragte halten die Lehrgänge zur Aus- und Fortbildung von Lehrkräften in der Ersten Hilfe.'),
       ('Welche Voraussetzungen gelten für Lehrbeauftragte?', 'Nach DGUV Grundsatz 304-003 (Abschnitt 2.2.2) mindestens eine Erste-Hilfe-Ausbildung (9 UE) und eine Sanitätsausbildung mit bestandener Prüfung (48 UE), pädagogisch die Qualifikation als Lehrkraft Erste Hilfe und eine pädagogische Schulung von mindestens 120 UE.'),
       ('Muss ich als angehender Lehrbeauftragter hospitieren?', 'Ja. Verlangt ist mindestens eine Hospitation in einer kompletten Lehrkräftequalifizierung einer Ausbildungsstelle. Bei BWW kostet sie den Kurspreis plus 25 € je Kurstag.'),
       ('Wie oft müssen Lehrbeauftragte sich fortbilden?', 'Mindestens alle drei Jahre im Umfang von 24 Unterrichtseinheiten, davon mindestens 16 pädagogisch und 8 medizinisch-fachlich (DGUV Grundsatz 304-003).')],
  related=[('/fuer-ausbilder/', 'Ausbilder werden: alle Stufen'), ('/ausbilder-werden/erste-hilfe-lehrkraft/', 'Erste-Hilfe-Ausbilder werden'), ('/multiplikatorenstelle/', 'Multiplikatorenstelle'), ('/wissen/lehrkraefte-erste-hilfe/', 'Lehrkräfte in der Erste-Hilfe-Ausbildung'), ('/wissen/lehrberechtigung-erste-hilfe-fortbildung-lehrkraefte/', 'Lehrberechtigung und Fortbildung')]),
 dict(path='ausbilder-werden/lehrberechtigung-verlaengern/', img='teacher-training', eyebrow='Ausbilder werden',
  title='Lehrberechtigung verlängern: Fortbildung Lehrkräfte | BWW',
  desc='Lehrkräfte Erste Hilfe weisen alle drei Jahre 16 UE Fortbildung nach. Wann sie fällig wird, was bei Ablauf gilt und was die Fortbildung bei BWW kostet.',
  h1='Lehrberechtigung verlängern: Fortbildung für Lehrkräfte Erste Hilfe',
  quellen='DGUV Grundsatz 304-003',
  lead='Lehrkräfte der Ersten Hilfe halten ihre Lehrberechtigung, indem sie mindestens alle drei Jahre eine Fortbildung von 16 Unterrichtseinheiten nachweisen, davon 8 medizinisch-fachlich und 8 pädagogisch. Ist die Lehrberechtigung abgelaufen, ist nach den DGUV-Vorgaben eine erneute Schulung im Themenbereich II von mindestens 32 Unterrichtseinheiten nötig.',
  cta=[('/kurse/lehrkraefte-fortbildung/', 'Lehrkräfte-Fortbildung ansehen und buchen', 'primary'), ('/kontakt/', 'Fragen zur Frist? Kontakt', 'ghost')],
  keyfacts=['<strong>Rhythmus:</strong> innerhalb der Gültigkeit der Lehrberechtigung, mindestens alle drei Jahre',
            '<strong>Umfang:</strong> mindestens 16 UE, davon 8 medizinisch-fachlich und 8 pädagogisch',
            '<strong>Frist verpasst:</strong> mindestens 32 UE im Themenbereich II statt 16 UE',
            '<strong>Preis bei BWW:</strong> 100 € je Person (Lehrkräftefortbildung, Stand ' + STAND + ')'],
  body="""<h2>Wer muss was nachweisen?</h2>
<p>Die Fortbildung betrifft Lehrkräfte Erste Hilfe mit gültiger Lehrberechtigung. Für Lehrkräfte des betrieblichen Sanitätsdienstes richten sich die Vorgaben nach der Lehrgangsart; bei der Ausbildungsstelle erfragen.</p>
<h2>Fristen und Planung</h2>
<p>Die Fortbildung muss innerhalb der Gültigkeit der Lehrberechtigung erfolgen. Lehrgänge werden vorab bei der Qualitätssicherungsstelle Erste Hilfe (QSEH) gemeldet und haben begrenzte Plätze; bucht deshalb rechtzeitig vor Fristende. Ob die Fortbildung bei BWW für eure Lehrberechtigung zählt, richtet sich nach den Vorgaben der QSEH und eurer Ausbildungsstelle; fragt dort vor der Buchung nach. Mehr zu Rhythmus und Aufteilung: <a href="/wissen/lehrkraefte-fortbildung-16-ue/">Lehrkräfte-Fortbildung: 16 UE alle drei Jahre</a>.</p>
<h2>Was passiert bei Ablauf?</h2>
<p>Ohne rechtzeitige Fortbildung erlischt die Lehrberechtigung. Um sie wiederzuerlangen, ist grundsätzlich eine erneute Schulung des Themenbereichs II „Fachdidaktische Umsetzung Erste Hilfe“ im Umfang von mindestens 32 UE nötig (DGUV Grundsatz 304-003). Details erklärt der Beitrag <a href="/wissen/lehrberechtigung-erste-hilfe-fortbildung-lehrkraefte/">Lehrberechtigung erhalten</a>.</p>
<h2>Fortbildung bei BWW</h2>
<p>Die <a href="/kurse/lehrkraefte-fortbildung/">Lehrkräfte-Fortbildung</a> kostet 100 € je Person (Preis laut Buchungssystem, Stand """ + STAND + """); Termine und Orte stehen auf der Kursseite. Die Teilnahmebescheinigung gibt es bei regelmäßigem Besuch.</p>
<h2>Zur Einordnung</h2>
<p>Geeignete Stelle zur Aus- und Fortbildung von Lehrkräften der Ersten Hilfe (seit 28.10.2025). Ermächtigte Stelle der gesetzlichen Unfallversicherung für die Aus- und Fortbildung in Erster Hilfe im Betrieb (Kennziffer 8.2122), ermächtigt seit 28.10.2025. """ + QL + """</p>""",
  faq=[('Wie oft muss ich als Lehrkraft Erste Hilfe fortbilden?', 'Innerhalb der Gültigkeit der Lehrberechtigung, mindestens alle drei Jahre, im Umfang von mindestens 16 Unterrichtseinheiten, davon 8 medizinisch-fachlich und 8 pädagogisch (DGUV Grundsatz 304-003).'),
       ('Was ist, wenn die Frist abgelaufen ist?', 'Die Lehrberechtigung erlischt. Zur Wiedererlangung ist grundsätzlich eine erneute Schulung des Themenbereichs II im Umfang von mindestens 32 Unterrichtseinheiten nötig.'),
       ('Gilt die Fortbildung auch für Lehrkräfte des betrieblichen Sanitätsdienstes?', 'Die Vorgaben richten sich nach der Lehrgangsart. Fragt bei der Ausbildungsstelle nach, welche Fortbildung für eure Lehrberechtigung gilt.'),
       ('Was kostet die Lehrkräfte-Fortbildung bei BWW?', 'Laut Buchungssystem 100 € je Person (Stand ' + STAND + ').'),
       ('Wie melde ich mich an?', 'Über die Kursseite der Lehrkräfte-Fortbildung; die Termine sind online buchbar. Bei Fragen zur Frist hilft der Kontakt.')],
  related=[('/fuer-ausbilder/', 'Ausbilder werden: alle Stufen'), ('/ausbilder-werden/erste-hilfe-lehrkraft/', 'Erste-Hilfe-Ausbilder werden'), ('/ausbilder-werden/betriebssanitaeter-lehrkraft/', 'Betriebssanitäter-Lehrkraft'), ('/wissen/lehrkraefte-fortbildung-16-ue/', 'Lehrkräfte-Fortbildung (16 UE)'), ('/wissen/lehrberechtigung-erste-hilfe-fortbildung-lehrkraefte/', 'Lehrberechtigung erhalten')]),
 dict(path='ausbilder-werden/preise/', img='teacher-training', eyebrow='Ausbilder werden',
  title='Preise Lehrkräfte- und Sanitäter-Lehrgänge | BWW',
  desc='Preise je Person für Lehrkräfte-Ausbildung, Fortbildung, Betriebssanitäter-Lehrgänge und Hospitation bei BWW, direkt aus dem Buchungssystem.',
  h1='Preise: Lehrkräfte-, Lehrbeauftragten- und Betriebssanitäter-Lehrgänge',
  quellen='Buchungssystem BWW',
  lead='Alle Preise gelten je Person und stammen aus dem Buchungssystem von BWW (Stand ' + STAND + '). Verbindlich ist der Preis, der bei der Buchung angezeigt wird.',
  cta=[('/kurse/', 'Termine und Buchung', 'primary'), ('/fuer-ausbilder/', 'Ausbilder werden: alle Stufen', 'ghost')],
  keyfacts=['<strong>Lehrkräfte Erste Hilfe:</strong> Themenbereich I 150 €, Themenbereich II 200 €, Fortbildung 100 €',
            '<strong>Betriebssanitäter:</strong> Grundkurs 450 €, Aufbaulehrgang 250 €',
            '<strong>Lehrkraft Sanitätsdienst:</strong> Teil a 100 €, Teil b 50 €',
            '<strong>Hospitation:</strong> Kurspreis plus 25 € je Kurstag'],
  body="""<h2>Lehrkräfte Erste Hilfe</h2>
<ul><li><a href="/kurse/lehrkraefte-ausbildung-lk1/">Lehrkräfte-Ausbildung Themenbereich I (24 UE)</a>: 150 €</li>
<li><a href="/kurse/lehrkraefte-ausbildung-lk2/">Lehrkräfte-Ausbildung Themenbereich II (32 UE)</a>: 200 €</li>
<li><a href="/kurse/lehrkraefte-fortbildung/">Lehrkräfte-Fortbildung (16 UE)</a>: 100 €</li></ul>
<h2>Betriebssanitäter und Lehrkraft Sanitätsdienst</h2>
<ul><li><a href="/kurse/betriebssanitaeter-grundkurs/">Betriebssanitäter-Grundkurs (63 UE zuzüglich Prüfung)</a>: 450 €</li>
<li><a href="/kurse/betriebssanitaeter-aufbau/">Betriebssanitäter-Aufbaulehrgang (32 UE zuzüglich Prüfung)</a>: 250 €</li>
<li><a href="/kurse/lehrkraefte-ausbildung-sanitaetsdienst/">Lehrkraft betrieblicher Sanitätsdienst</a>: Teil a (16 UE) 100 €, Teil b (8 UE) 50 €</li></ul>
<h2>Weitere Angebote</h2>
<ul><li><a href="/kurse/lehrbeauftragten-fortbildung/">Fortbildung für Lehrbeauftragte (24 UE)</a>: 150 €</li>
<li><a href="/kurse/lehrbeauftragter-erste-hilfe/">Lehrbeauftragten-Qualifizierung nach Orientierungsrahmen (mind. 120 UE)</a>: 700 €; keine QSEH-registrierte Maßnahme, keine DGUV-Anerkennung</li>
<li><a href="/ausbilder-werden/lehrbeauftragter/">Hospitation</a> in einer Lehrkräftequalifizierung: Kurspreis plus 25 € je Kurstag</li></ul>
<p class="small-note">Preise je Person laut Buchungssystem, Stand """ + STAND + """. Inhouse-Preise nach Anfrage.</p>""",
  faq=[('Was kostet die Lehrkräfte-Ausbildung bei BWW?', 'Themenbereich I (24 UE) kostet 150 €, Themenbereich II (32 UE) 200 €, die Lehrkräfte-Fortbildung 100 € je Person (Stand ' + STAND + ').'),
       ('Was kostet ein Betriebssanitäter-Lehrgang?', 'Der Grundkurs kostet 450 €, der Aufbaulehrgang 250 € je Person (Stand ' + STAND + ').'),
       ('Was kostet eine Hospitation?', 'Der Kurspreis des Lehrgangs, in dem hospitiert wird, plus 25 € je Kurstag.'),
       ('Wo sehe ich den verbindlichen Preis?', 'Bei der Buchung im Buchungssystem. Dort wird der Preis des gewählten Termins angezeigt.')],
  related=[('/fuer-ausbilder/', 'Ausbilder werden: alle Stufen'), ('/ausbilder-werden/erste-hilfe-lehrkraft/', 'Erste-Hilfe-Ausbilder werden'), ('/ausbilder-werden/betriebssanitaeter-lehrkraft/', 'Betriebssanitäter-Lehrkraft'), ('/ausbilder-werden/lehrberechtigung-verlaengern/', 'Lehrberechtigung verlängern'), ('/multiplikatorenstelle/', 'Multiplikatorenstelle')]),
 dict(path='ausbilder-werden/fuer-hilfsorganisationen/', img='teacher-training', eyebrow='Ausbilder werden',
  title='Lehrkräfte ausbilden lassen: für Hilfsorganisationen | BWW',
  desc='Wie Hilfsorganisationen ihre Ausbilder qualifizieren: Lehrkräfte-Ausbildung, Fortbildung und Hospitation bei BWW, Voraussetzungen nach DGUV 304-003.',
  h1='Angebot für Hilfsorganisationen, die Lehrkräfte qualifizieren lassen möchten',
  quellen='DGUV Grundsatz 304-003',
  lead='Wer in einer Hilfsorganisation selbst Erste-Hilfe- oder Sanitätskurse leiten will, braucht die Lehrkräfte-Qualifikation nach DGUV Grundsatz 304-003. Bei BWW gibt es sie als Lehrkräfte-Ausbildung (Themenbereich I und II) und als Lehrkraft für den betrieblichen Sanitätsdienst, jeweils mit Fortbildung.',
  cta=[('/ausbilder-werden/erste-hilfe-lehrkraft/', 'Erste-Hilfe-Lehrkraft werden', 'primary'), ('/ausbilder-werden/preise/', 'Preise ansehen', 'ghost')],
  keyfacts=['<strong>Wege:</strong> <a href="/ausbilder-werden/erste-hilfe-lehrkraft/">Erste-Hilfe-Lehrkraft</a>, <a href="/ausbilder-werden/betriebssanitaeter-lehrkraft/">Betriebssanitäter-Lehrkraft</a>, <a href="/ausbilder-werden/lehrberechtigung-verlaengern/">Lehrberechtigung verlängern</a>',
            '<strong>Fortbildung:</strong> mindestens alle drei Jahre, 16 UE (8 medizinisch-fachlich, 8 pädagogisch)',
            '<strong>Hospitation:</strong> Kurspreis plus 25 € je Kurstag',
            '<strong>Gruppen:</strong> Inhouse-Termine auf Anfrage'],
  body="""<h2>Voraussetzungen je Person</h2>
<p>Medizinisch: ein Erste-Hilfe-Kurs plus mindestens 48 Unterrichtseinheiten notfallmedizinische Ausbildung. Pädagogisch: mindestens 56 Unterrichtseinheiten und mindestens zwei Hospitationen (DGUV Grundsatz 304-003). Einzelheiten: <a href="/wissen/erste-hilfe-ausbilder-werden-qualifikation/">Erste-Hilfe-Ausbilder werden: Qualifikationsweg</a>.</p>
<h2>Wenn die Organisation selbst ausbilden will</h2>
<p>Wer selbst Erste-Hilfe-Kurse für betriebliche Ersthelfer im Sinn der gesetzlichen Unfallversicherung anbieten möchte, braucht dafür eine eigene Ermächtigung. Sie wird von den Unfallversicherungsträgern bzw. der QSEH erteilt; die Lehrkräfte-Qualifikation allein ersetzt sie nicht. Voraussetzungen und Ablauf: <a href="/wissen/erste-hilfe-ausbildungsstelle-gruenden/">Erste-Hilfe-Ausbildungsstelle gründen</a> und <a href="/wissen/qseh-ermaechtigungsverfahren-ablauf/">Ermächtigungsverfahren bei der QSEH</a>.</p>
<h2>Zur Einordnung</h2>
<p>""" + BEL6 + """</p>""",
  faq=[('Können mehrere Personen gemeinsam teilnehmen?', 'Ja. Inhouse-Termine für Gruppen sind auf Anfrage möglich.'),
       ('Was braucht jede Person vorab?', 'Medizinisch einen Erste-Hilfe-Kurs plus mindestens 48 Unterrichtseinheiten notfallmedizinische Ausbildung, pädagogisch mindestens 56 Unterrichtseinheiten und mindestens zwei Hospitationen (DGUV Grundsatz 304-003).'),
       ('Wo wird die Eignung von BWW geführt?', 'Die ermächtigten bzw. geeigneten Stellen führt die Qualitätssicherungsstelle Erste Hilfe (QSEH) in einer öffentlichen Liste.'),
       ('Was kostet es?', 'Die Preise je Person stehen auf der Seite „Preise der Lehrgänge für Ausbilder“.')],
  related=[('/fuer-ausbilder/', 'Ausbilder werden: alle Stufen'), ('/ausbilder-werden/preise/', 'Preise'), ('/multiplikatorenstelle/', 'Multiplikatorenstelle'), ('/wissen/ermaechtigte-ausbildungsstelle-pflichten/', 'Pflichten ermächtigter Stellen')]),
 dict(path='ausbilder-werden/fuer-ausbildungsstellen/', img='teacher-training', eyebrow='Ausbilder werden',
  title='Lehrkräfte fortbilden lassen: für Ausbildungsstellen | BWW',
  desc='Ausbildungsstellen halten Lehrberechtigungen aktuell: Fortbildung alle drei Jahre (16 UE), Fristen, Ablauf bei Ablauf der Berechtigung. Termine bei BWW.',
  h1='Lehrberechtigungen im Blick behalten: Fortbildung für Lehrkräfte von Ausbildungsstellen',
  quellen='DGUV Grundsatz 304-003',
  lead='Lehrkräfte Erste Hilfe müssen mindestens alle drei Jahre 16 Unterrichtseinheiten Fortbildung nachweisen, davon 8 medizinisch-fachlich und 8 pädagogisch. Ist die Lehrberechtigung abgelaufen, sind mindestens 32 Unterrichtseinheiten im Themenbereich II nötig.',
  cta=[('/ausbilder-werden/lehrberechtigung-verlaengern/', 'Lehrberechtigung verlängern', 'primary'), ('/kurse/lehrkraefte-fortbildung/', 'Fortbildung buchen', 'ghost')],
  keyfacts=['<strong>Rhythmus:</strong> mindestens alle drei Jahre', '<strong>Umfang:</strong> 16 UE, davon 8 medizinisch-fachlich und 8 pädagogisch',
            '<strong>Frist verpasst:</strong> mindestens 32 UE im Themenbereich II', '<strong>Preis bei BWW:</strong> 100 € je Person (Stand ' + STAND + ')'],
  body="""<h2>Fristen und Planung</h2>
<p>Fristen, Umfang und Ablauf bei abgelaufener Lehrberechtigung stehen auf der Seite <a href="/ausbilder-werden/lehrberechtigung-verlaengern/">Lehrberechtigung verlängern</a>. Ob die Fortbildung bei BWW für eure Lehrberechtigung zählt, richtet sich nach den Vorgaben der QSEH und eurer Ausbildungsstelle; fragt dort vor der Buchung nach.</p>
<h2>Pflichten ermächtigter Stellen</h2>
<p>Was eine ermächtigte Stelle laufend leisten muss, erklärt <a href="/wissen/ermaechtigte-ausbildungsstelle-pflichten/">Pflichten ermächtigter Stellen</a>; aktuelle Änderungen: <a href="/wissen/aktuelle-aenderungen-ausbildungsstellen/">Aktuelle Änderungen für Ausbildungsstellen</a>.</p>
<h2>Hospitation für künftige Lehrbeauftragte</h2>
<p>Angehende Lehrbeauftragte hospitieren in einer kompletten Lehrkräftequalifizierung: <a href="/ausbilder-werden/lehrbeauftragter/">Voraussetzungen und Hospitation</a>.</p>
<h2>Zur Einordnung</h2>
<p>""" + BEL6 + """</p>""",
  faq=[('Wie oft müssen Lehrkräfte fortbilden?', 'Mindestens alle drei Jahre im Umfang von mindestens 16 Unterrichtseinheiten, davon 8 medizinisch-fachlich und 8 pädagogisch (DGUV Grundsatz 304-003).'),
       ('Was gilt bei abgelaufener Lehrberechtigung?', 'Zur Wiedererlangung ist grundsätzlich eine erneute Schulung des Themenbereichs II im Umfang von mindestens 32 Unterrichtseinheiten nötig.'),
       ('Zählt die Fortbildung bei BWW für unsere Lehrberechtigung?', 'Das richtet sich nach den Vorgaben der QSEH und eurer Ausbildungsstelle; fragt dort vor der Buchung nach.'),
       ('Was kostet die Fortbildung?', 'Laut Buchungssystem 100 € je Person (Stand ' + STAND + ').')],
  related=[('/fuer-ausbilder/', 'Ausbilder werden: alle Stufen'), ('/ausbilder-werden/lehrberechtigung-verlaengern/', 'Lehrberechtigung verlängern'), ('/wissen/lehrkraefte-fortbildung-16-ue/', 'Lehrkräfte-Fortbildung (16 UE)'), ('/wissen/qseh-ermaechtigungsverfahren-ablauf/', 'Ermächtigungsverfahren bei der QSEH')]),
 dict(path='ausbilder-werden/fuer-betriebe/', img='teacher-training', eyebrow='Ausbilder werden',
  title='Betriebssanitäter und Ersthelfer im Betrieb: Ausbilder | BWW',
  desc='Betriebe, die Ersthelfer oder Betriebssanitäter ausbilden lassen, finden hier die Wege: Kurse inhouse, Fortbildung, Lehrgänge für Ausbilder.',
  h1='Betriebliche Ersthelfer und Betriebssanitäter: Ausbildung im Betrieb und Ausbilder-Qualifikation',
  quellen='DGUV Vorschrift 1, DGUV Grundsatz 304-003',
  lead='BWW bildet betriebliche Ersthelfer aus und fort und ist dafür ermächtigte Stelle der gesetzlichen Unfallversicherung (Kennziffer 8.2122, seit 28.10.2025). Wer im Betrieb selbst Kurse leiten soll, braucht zusätzlich die Lehrkräfte-Qualifikation nach DGUV Grundsatz 304-003.',
  cta=[('/inhouse-kurse/', 'Inhouse-Kurs anfragen', 'primary'), ('/ausbilder-werden/erste-hilfe-lehrkraft/', 'Ausbilder im Betrieb qualifizieren', 'ghost')],
  keyfacts=['<strong>Ersthelfer:</strong> Ausbildung und Fortbildung inhouse oder offen, Bescheinigung digital', '<strong>Betriebssanitäter:</strong> Grund-, Aufbau- und Fortbildungslehrgänge; geeignete Stelle seit 29.10.2026',
            '<strong>Ausbilder im Betrieb:</strong> Lehrkräfte-Qualifikation nach DGUV 304-003', '<strong>Kosten:</strong> Ob und in welcher Höhe der Träger die Kosten übernimmt, entscheidet der Träger'],
  body="""<h2>Ersthelfer</h2>
<p><a href="/kurse/erste-hilfe-ausbildung/">Erste-Hilfe-Ausbildung</a> und <a href="/kurse/erste-hilfe-fortbildung/">Fortbildung</a> für betriebliche Ersthelfer; wie viele Ersthelfer ein Betrieb braucht, erklärt <a href="/wissen/ersthelfer-anzahl-dguv/">Wie viele Ersthelfer braucht ein Betrieb?</a></p>
<h2>Betriebssanitäter</h2>
<p><a href="/ausbilder-werden/betriebssanitaeter-lehrkraft/">Betriebssanitäter-Lehrgänge und Lehrkraft Sanitätsdienst</a>. Aktuelle Termine stehen in der <a href="/kurse/">Terminliste</a> (Stand """ + STAND + """: erster Termin am 13.07.2027).</p>
<h2>Ausbilder im Betrieb</h2>
<p>Wer im Betrieb selbst Kurse leiten soll, findet die Wege unter <a href="/ausbilder-werden/erste-hilfe-lehrkraft/">Erste-Hilfe-Ausbilder werden</a> und <a href="/ausbilder-werden/betriebssanitaeter-lehrkraft/">Betriebssanitäter-Ausbilder werden</a>.</p>
<h2>Abrechnung</h2>
<p>Die Erste-Hilfe-Aus- und Fortbildung betrieblicher Ersthelfer ist über den zuständigen Träger abrechenbar; Einzelheiten auf der Seite <a href="/abrechnung/">Abrechnung</a>. Ob und in welcher Höhe der Träger die Kosten übernimmt, entscheidet der Träger.</p>
<h2>Zur Einordnung</h2>
<p>""" + BEL6 + """</p>""",
  faq=[('Wer trägt die Kosten der Ersthelfer-Ausbildung?', 'Ob und in welcher Höhe der zuständige Träger die Kosten übernimmt, entscheidet der Träger. Einzelheiten stehen im Beitrag „Was kostet der Erste-Hilfe-Kurs den Betrieb wirklich?“.'),
       ('Brauchen wir einen eigenen Ausbilder im Betrieb?', 'Nicht zwingend. Wer im Betrieb selbst Kurse leiten soll, braucht die Lehrkräfte-Qualifikation nach DGUV Grundsatz 304-003; die Wege stehen unter „Ausbilder werden“.'),
       ('Ab wann gibt es Betriebssanitäter-Kurse bei BWW?', 'BWW ist für Betriebssanitäter seit dem 29.10.2026 geeignete Stelle. Aktuelle Termine stehen in der Terminliste (Stand ' + STAND + ': erster Termin am 13.07.2027).')],
  related=[('/fuer-ausbilder/', 'Ausbilder werden: alle Stufen'), ('/inhouse-kurse/', 'Inhouse-Kurse'), ('/abrechnung/', 'Abrechnung'), ('/wissen/ersthelfer-anzahl-dguv/', 'Wie viele Ersthelfer braucht ein Betrieb?'), ('/wissen/erste-hilfe-kurs-kosten-betrieb/', 'Was kostet der Erste-Hilfe-Kurs den Betrieb?')]),
 dict(path='multiplikatorenstelle/', img='legal-docs', eyebrow='Multiplikatorenstelle',
  title='Multiplikatorenstelle: Was sie leistet, was sie darf | BWW',
  desc='Eine Multiplikatorenstelle bildet Lehrkräfte für Erste Hilfe und Sanitätsdienst aus (DGUV Grundsatz 304-003). Aufgaben, Ablauf, Kontakt.',
  h1='Multiplikatorenstelle: Ausbildung für Ausbilder in der Ersten Hilfe',
  quellen='DGUV Grundsatz 304-003, DGUV Grundsatz 304-001, DGUV Grundsatz 304-002',
  lead='Eine Multiplikatorenstelle qualifiziert Ausbilderinnen und Ausbilder für Erste Hilfe und den betrieblichen Sanitätsdienst. Die Regeln dafür bündelt seit 2022 der DGUV Grundsatz 304-003.',
  cta=[('/fuer-ausbilder/', 'Ausbilder werden: alle Stufen', 'primary'), ('/kontakt/', 'Kontakt aufnehmen', 'ghost')],
  keyfacts=['<strong>Aufgabe:</strong> Aus- und Fortbildung von Lehrkräften Erste Hilfe und für den betrieblichen Sanitätsdienst',
            '<strong>Ermächtigung und Eignung:</strong> getrennt zu betrachten; BWW ist ermächtigt für die Erste-Hilfe-Aus- und Fortbildung im Betrieb, geeignet für die Lehrkräfte- und Sanitätsdienst-Lehrgänge (Kennziffer 8.2122)',
            '<strong>Grundlage:</strong> DGUV Grundsatz 304-003, Ausgabe 2022.04',
            '<strong>Eignung:</strong> stellt die Qualitätssicherungsstelle Erste Hilfe (QSEH) fest',
            '<strong>Anerkennung:</strong> pädagogische Qualifikation zählt nur, wenn sie bei einer solchen Stelle erworben wurde'],
  body='''<h2>Was eine Multiplikatorenstelle tut</h2>
<p>Während ermächtigte Stellen nach Grundsatz 304-001 betriebliche Ersthelfende ausbilden, bildet eine Multiplikatorenstelle die aus, die selbst unterrichten: Lehrkräfte für Erste Hilfe und für den betrieblichen Sanitätsdienst. Dazu gehören die Lehrkräfte-Ausbildung und die regelmäßige Fortbildung der Lehrkräfte.</p>
<h2>Die drei Grundsätze</h2>
<ul><li><strong>304-001:</strong> Ermächtigung von Stellen für die Aus- und Fortbildung in der Ersten Hilfe</li>
<li><strong>304-002:</strong> Aus- und Fortbildung für den betrieblichen Sanitätsdienst</li>
<li><strong>304-003:</strong> Aus- und Fortbildung von Lehrkräften in der Ersten Hilfe und für den betrieblichen Sanitätsdienst (Multiplikatorenstellen)</li></ul>
<h2>Das Angebot von BWW</h2>
<p>BWW bietet die <a href="/ausbilder-werden/erste-hilfe-lehrkraft/">Lehrkräfte-Ausbildung Erste Hilfe</a> (Themenbereich I und II), die <a href="/kurse/lehrkraefte-fortbildung/">Lehrkräfte-Fortbildung</a> und Lehrgänge für den <a href="/ausbilder-werden/betriebssanitaeter-lehrkraft/">betrieblichen Sanitätsdienst</a> an. Ermächtigt ist BWW für die Erste-Hilfe-Aus- und Fortbildung im Betrieb (Kennziffer 8.2122, seit 28.10.2025). Geeignete Stelle ist BWW für die Aus- und Fortbildung von Lehrkräften der Ersten Hilfe (seit 28.10.2025) sowie von Lehrkräften des betrieblichen Sanitätsdienstes und von Betriebssanitätern (seit 29.10.2026). Die ermächtigten bzw. geeigneten Stellen führt die Qualitätssicherungsstelle Erste Hilfe (QSEH) der gesetzlichen Unfallversicherungsträger in einer öffentlichen Liste.</p>
<h2>Woran ihr eine geeignete Stelle erkennt</h2>
<p>Die QSEH stellt fest, ob eine Stelle Lehrkräfte ausbilden darf. Maßgeblich ist die Liste der ermächtigten Stellen im Bereich „Lehrkräfte Erste Hilfe“. Die Kennziffer einer Stelle lässt sich beim Unfallversicherungsträger nachprüfen.</p>
<!-- VORBEREITET, NICHT VERÖFFENTLICHEN (Jurist-Freigabe und Filter-Einzelzählung ausstehend, jurist/bww-qseh-liste-lbeh-01-11.md): Die öffentliche Liste der Qualitätssicherungsstelle Erste Hilfe (QSEH) der gesetzlichen Unfallversicherung führt bundesweit 11 Stellen, die in allen vier Bereichen ausbilden: betriebliche Ersthelfer, Betriebssanitäter, Lehrkräfte Erste Hilfe und Lehrkräfte Betriebssanitäter (Abruf am 01.11.2026, 22:16 Uhr, 11 von 2.016 gelisteten Stellen). Die BWW UG (haftungsbeschränkt) ist mit der Kennziffer 8.2122 eine davon. Neuprüfung vierteljährlich, sonst entfernen. -->''',
  faq=[('Was ist eine Multiplikatorenstelle?', 'Eine Stelle, die Lehrkräfte für Erste Hilfe und für den betrieblichen Sanitätsdienst aus- und fortbildet. Sie erbringt diese Leistung selbst. Die Regeln dafür stehen im DGUV Grundsatz 304-003.'),
       ('Wer prüft, ob eine Stelle Lehrkräfte ausbilden darf?', 'Die Qualitätssicherungsstelle Erste Hilfe (QSEH) stellt die Eignung fest. Nur bei solchen Stellen erworbene pädagogische Qualifikationen werden anerkannt.'),
       ('Was unterscheidet 304-003 von 304-001 und 304-002?', '304-001 regelt die Ermächtigung von Stellen für die Erste-Hilfe-Ausbildung, 304-002 die Aus- und Fortbildung für den betrieblichen Sanitätsdienst, 304-003 die Aus- und Fortbildung der Lehrkräfte. Die Kriterien für Multiplikatorenstellen wurden 2022 aus 304-001 und 304-002 in 304-003 überführt.'),
       ('Wie werde ich Erste-Hilfe-Ausbilder?', 'Über eine medizinische Grundqualifikation, eine pädagogische Qualifikation bei einer geeigneten Stelle und Hospitationen. Der Weg steht auf der Seite „Erste-Hilfe-Ausbilder werden“.')],
  related=[('/ausbilder-werden/erste-hilfe-lehrkraft/', 'Erste-Hilfe-Ausbilder werden'), ('/ausbilder-werden/betriebssanitaeter-lehrkraft/', 'Betriebssanitäter-Lehrkraft'), ('/wissen/multiplikatorenstelle-dguv-grundsatz-304-003/', 'Grundsatz 304-003 erklärt'), ('/wissen/ermaechtigte-ausbildungsstelle-pflichten/', 'Pflichten ermächtigter Stellen'), ('/wissen/qseh-ermaechtigungsverfahren-ablauf/', 'Ermächtigungsverfahren bei der QSEH')]),
]
# Seiten, die auf die neuen Landingseiten zurückverlinken (>= 3 eingehende je Landing)
INBOUND = {
 '/ausbilder-werden/erste-hilfe-lehrkraft/': ('Erste-Hilfe-Ausbilder werden: Lehrkräfte-Ausbildung', ['wissen/multiplikatorenstelle-dguv-grundsatz-304-003', 'wissen/erste-hilfe-ausbilder-werden-qualifikation', 'wissen/lehrkraefte-erste-hilfe', 'wissen/lehrberechtigung-erste-hilfe-fortbildung-lehrkraefte']),
 '/ausbilder-werden/betriebssanitaeter-lehrkraft/': ('Betriebssanitäter-Ausbilder werden', ['wissen/betriebssanitaeter-ausbildung', 'wissen/ersthelfer-oder-betriebssanitaeter', 'wissen/betriebssanitaeter-pflicht', 'wissen/was-ist-sanitaetsdienst']),
 '/ausbilder-werden/lehrbeauftragter/': ('Lehrbeauftragter Erste Hilfe', ['wissen/multiplikatorenstelle-dguv-grundsatz-304-003', 'wissen/lehrkraefte-erste-hilfe', 'wissen/lehrkraefte-fortbildung-16-ue', 'wissen/erste-hilfe-ausbilder-werden-qualifikation']),
 '/ausbilder-werden/lehrberechtigung-verlaengern/': ('Lehrberechtigung verlängern', ['wissen/lehrkraefte-fortbildung-16-ue', 'wissen/lehrberechtigung-erste-hilfe-fortbildung-lehrkraefte', 'wissen/lehrkraefte-erste-hilfe', 'wissen/erste-hilfe-ausbilder-werden-qualifikation']),
 '/ausbilder-werden/preise/': ('Preise der Lehrgänge für Ausbilder', ['wissen/erste-hilfe-ausbilder-werden-qualifikation', 'wissen/lehrkraefte-fortbildung-16-ue', 'wissen/betriebssanitaeter-ausbildung', 'wissen/lehrkraefte-erste-hilfe']),
 '/multiplikatorenstelle/': ('Multiplikatorenstelle: Aufgaben und Angebot', ['wissen/erste-hilfe-ausbilder-werden-qualifikation', 'wissen/ermaechtigte-ausbildungsstelle-pflichten', 'wissen/qseh-ermaechtigungsverfahren-ablauf', 'wissen/lehrkraefte-erste-hilfe']),
}

def build(p, base):
    url = f"{HOST}/{p['path']}"; t, d = esc(p['title']), esc(p['desc'])
    assert len(p['title']) <= 60 and len(p['desc']) <= 155, (p['path'], len(p['title']), len(p['desc']))
    h = base
    h = re.sub(r'<title>.*?</title>', f'<title>{t}</title>', h, 1, re.S)
    h = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + d + '"', h, 1)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*"', lambda m: m.group(1) + url + '"', h, 1)
    for a, v in (('og:title', t), ('og:description', d), ('og:url', url), ('twitter:title', t), ('twitter:description', d)):
        h = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*"' % a, lambda m: m.group(1) + v + '"', h, 1)
    h = h.replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">')
    h = re.sub(r'<meta property="article:[a-z_]+" content="[^"]*">', '', h)
    # JSON-LD: Organisation behalten, Rest neu
    blocks = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S))
    org = blocks[0].group(0)
    for b in blocks[1:]: h = h.replace(b.group(0), '', 1)
    crumbs = [("Start", HOST + "/"), ("Ausbilder werden", HOST + "/fuer-ausbilder/")] if p['path'] != 'multiplikatorenstelle/' else [("Start", HOST + "/")]
    crumbs.append((strip_tags(p['h1']).split(':')[0] if p['path'] == 'multiplikatorenstelle/' else p['title'].split(' | ')[0], url))
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}
    wp = {"@context": "https://schema.org", "@type": "WebPage", "name": p['title'].split(' | ')[0], "description": p['desc'], "url": url, "inLanguage": "de-DE", "dateModified": "2026-11-01",
          "publisher": {"@type": "Organization", "name": "BWW UG (haftungsbeschränkt)", "url": HOST + "/"}}
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in p['faq']]}
    ld = ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False, separators=(',', ':')) + '</script>' for x in (bc, wp, fq))
    h = h.replace(org, org + ld, 1)
    # Hauptinhalt
    i = h.find('<main'); j = h.find('</main>')
    cta_block = h[h.find('<section class="section home-final">', i):j]
    ph = re.search(r'<img class="bww-ill"[^>]*>', h[i:j]).group(0)
    img = f'<img class="bww-ill" src="/media/illustrations/bww/{p["img"]}.webp" width="450" height="388" alt="{esc(p["h1"])}" fetchpriority="high">'
    bcrumb = '<nav class="breadcrumbs" aria-label="Brotkrümel"><a href="/">Start</a><span class="sep" aria-hidden="true">›</span>' + \
        ('' if p['path'] == 'multiplikatorenstelle/' else '<a href="/fuer-ausbilder/">Ausbilder werden</a><span class="sep" aria-hidden="true">›</span>') + \
        f'<span class="current">{esc(crumbs[-1][0])}</span></nav>'
    acts = ''.join(f'<a class="btn {c}" href="{u}">{esc(l)}</a>' for u, l, c in p['cta'])
    topn = f'<div class="article-note">{p["topnote"]}</div>' if p.get('topnote') else ''
    kf = '<div class="key-facts"><h2>Kurz gefasst</h2><ul>' + ''.join(f'<li>{k}</li>' for k in p['keyfacts']) + '</ul></div>'
    rel = '<p class="article-related">' + ''.join(f'<a href="{u}">{esc(l)}</a>' for u, l in p['related']) + '</p>'
    src = f'<p class="article-sources"><strong>Offizielle Quellen:</strong> {esc(p["quellen"])}. Stand: {STAND}. Dieser Beitrag ersetzt keine Rechtsberatung; verbindlich sind die jeweils geltenden Vorgaben der DGUV und der QSEH.</p>'
    main = (f'<main id="hauptinhalt" tabindex="-1">{bcrumb}<section class="page-hero"><div><span class="eyebrow">{esc(p["eyebrow"])}</span><h1>{esc(p["h1"])}</h1>'
            f'<p class="article-stand">Stand: {STAND} · Redaktion BWW · Quellen: {esc(p["quellen"])}</p><p>{p["lead"]}</p><div class="hero-actions">{acts}</div></div>{img}</section>'
            f'<section class="section article-body">{topn}{kf}{p["body"]}<h2>Häufige Fragen</h2>{faq_html(p["faq"])}{rel}{src}</section>{cta_block}')
    h = h[:i] + main + h[j:]
    return h

def main():
    base = open(BASE, encoding='utf8').read()
    n = 0
    for p in PAGES:
        f = p['path'] + 'index.html'; h = build(p, base)
        os.makedirs(os.path.dirname(f), exist_ok=True)
        if not os.path.exists(f) or open(f, encoding='utf8').read() != h: open(f, 'w', encoding='utf8').write(h); n += 1
    # eingehende Links
    for tgt, (label, srcs) in INBOUND.items():
        a = f'<a href="{tgt}">{esc(label)}</a>'
        for s in srcs:
            f = s + '/index.html'; h = open(f, encoding='utf8').read()
            if f'href="{tgt}"' in h.split('<footer')[0]: continue
            m = re.search(r'<p class="article-related">(.*?)</p>', h, re.S)
            if not m: print('KEIN article-related:', s); continue
            open(f, 'w', encoding='utf8').write(h.replace(m.group(0), m.group(0).replace('</p>', a + '</p>'), 1)); n += 1
    # Sitemap, llms.txt
    sm = open('sitemap.xml', encoding='utf8').read(); add = ''
    for p in PAGES:
        loc = f"<loc>{HOST}/{p['path']}</loc>"
        if loc not in sm: add += f"<url>{loc}<lastmod>2026-11-01</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n"
    if add: open('sitemap.xml', 'w', encoding='utf8').write(sm.replace('</urlset>', add + '</urlset>')); n += 1
    ll = open('llms.txt', encoding='utf8').read(); o = ll
    LL = [("/ausbilder-werden/erste-hilfe-lehrkraft/", "Erste-Hilfe-Ausbilder werden", "Qualifikationsweg und Lehrkräfte-Ausbildung"),
          ("/ausbilder-werden/betriebssanitaeter-lehrkraft/", "Betriebssanitäter-Ausbilder werden", "Lehrkraft betrieblicher Sanitätsdienst und Betriebssanitäter-Lehrgänge"),
          ("/ausbilder-werden/fuer-hilfsorganisationen/", "Für Hilfsorganisationen", "Lehrkräfte qualifizieren lassen: Wege, Voraussetzungen, Hospitation"),
          ("/ausbilder-werden/fuer-ausbildungsstellen/", "Für Ausbildungsstellen", "Lehrberechtigungen aktuell halten: Fortbildung, Fristen"),
          ("/ausbilder-werden/fuer-betriebe/", "Für Betriebe", "Ersthelfer, Betriebssanitäter und Ausbilder im Betrieb"),
          ("/ausbilder-werden/preise/", "Preise der Lehrgänge für Ausbilder", "Lehrkräfte-, Betriebssanitäter- und Hospitationspreise aus dem Buchungssystem"),
          ("/ausbilder-werden/lehrberechtigung-verlaengern/", "Lehrberechtigung verlängern", "Fortbildung für Lehrkräfte Erste Hilfe: Frist, Umfang, Ablauf"),
          ("/ausbilder-werden/lehrbeauftragter/", "Künftige Lehrbeauftragte", "Voraussetzungen und Weg über die Hospitation"),
          ("/multiplikatorenstelle/", "Multiplikatorenstelle", "Aufgaben, Grundsätze 304-001 bis 304-003, Angebot")]
    ll = re.sub(r"- \[Lehrbeauftragter Erste Hilfe\]\(" + re.escape(HOST) + r"/ausbilder-werden/lehrbeauftragter/\):[^\n]*\n", "", ll)
    for u, t, d in LL:
        line = f"- [{t}]({HOST}{u}): {d}\n"
        ll = re.sub(r"- \[[^\]]*\]\(" + re.escape(HOST + u) + r"\):[^\n]*\n", "", ll)
        k = ll.find('- [Für Kitas und Betreuung]'); ll = ll[:k] + line + ll[k:]
    if ll != o: open('llms.txt', 'w', encoding='utf8').write(ll); n += 1
    print('geändert/neu:', n)

if __name__ == '__main__':
    main()
