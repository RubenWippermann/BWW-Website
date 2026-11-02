#!/usr/bin/env python3
"""Interne Fließtext-Links auf schwach verlinkte Seiten (GSC 'gefunden - nicht indexiert'). Idempotent."""
import os
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
L = lambda t, a: f'<a href="/{t}/">{a}</a>'
SCH, BEH = 'fuer-schulen', 'fuer-behoerden'
DAT, BES, BIL, ONL, QUA, NAD, NOT = ('wissen/datenschutz-gesundheitsdaten-betrieb', 'wissen/erste-hilfe-bescheinigung-verloren-duplikat',
 'wissen/erste-hilfe-bildungseinrichtungen-dguv-anforderungen', 'wissen/erste-hilfe-kurs-online-anerkannt',
 'wissen/erste-hilfe-kurs-qualitaet-gruppengroesse-ausstattung', 'wissen/nadelstichverletzung-trba-250', 'wissen/notfalldaten-notfallpass-handy')
E_ = [  # (Quellseite, Ziel, Satz)
 ('wissen/erste-hilfe-kita-pflicht', SCH, f'Wie Schulen ihre Lehrkräfte und den Schulsanitätsdienst ausbilden lassen, steht unter {L(SCH, "Erste Hilfe für Schulen")}.'),
 ('wissen/schulsanitaetsdienst', SCH, f'Die Kursformate für Lehrkräfte, Schulsanitätsdienst und Kollegium sind unter {L(SCH, "Erste Hilfe für Schulen")} zusammengefasst.'),
 (BIL, SCH, f'Welche Kurse es für Schulen gibt, zeigt die Seite {L(SCH, "Erste Hilfe für Schulen")}.'),
 ('wissen/zustaendige-berufsgenossenschaft-finden', BEH, f'Für Behörden und Verwaltungen läuft die Abrechnung nicht über eine Berufsgenossenschaft, sondern über die Unfallkasse; unser Angebot dafür steht unter {L(BEH, "Erste Hilfe für Behörden")}.'),
 ('wissen/unfallanzeige-berufsgenossenschaft', BEH, f'Bei Behörden ist die Unfallkasse zuständig. Kurse für Ämter, Verwaltung und den öffentlichen Dienst findet ihr unter {L(BEH, "Erste Hilfe für Behörden")}.'),
 ('wissen/ersthelfer-anzahl-dguv', BEH, f'Angebote für Ämter, Verwaltung und den öffentlichen Dienst stehen unter {L(BEH, "Erste Hilfe für Behörden")}.'),
 ('wissen/verbandbuch-dokumentationspflicht', DAT, f'Welche Datenschutzregeln für die Gesundheitsdaten im Verbandbuch gelten, erklärt der Beitrag {L(DAT, "Gesundheitsdaten und Datenschutz im betrieblichen Notfall")}.'),
 ('wissen/unfallanzeige-berufsgenossenschaft', DAT, f'Auch eine Unfallanzeige enthält Gesundheitsdaten; zum Umgang damit siehe {L(DAT, "Gesundheitsdaten und Datenschutz im betrieblichen Notfall")}.'),
 ('wissen/betriebsarzt-aufgaben', DAT, f'Zu Schweigepflicht und Datenschutz bei Gesundheitsdaten im Betrieb siehe {L(DAT, "Gesundheitsdaten und Datenschutz im betrieblichen Notfall")}.'),
 ('wissen/erste-hilfe-teilnahmebescheinigung', BES, f'Ist die Bescheinigung verloren gegangen, hilft der Beitrag {L(BES, "Erste-Hilfe-Bescheinigung verloren: So kommt ihr an ein Duplikat")}.'),
 ('wissen/erste-hilfe-fuehrerschein', BES, f'Wer die Bescheinigung für den Führerschein nicht mehr findet, liest unter {L(BES, "Erste-Hilfe-Bescheinigung verloren")}, wie ein Duplikat zu bekommen ist.'),
 ('wissen/erste-hilfe-kurs-gueltigkeit', BES, f'Ist der Nachweis nicht mehr auffindbar, steht unter {L(BES, "Erste-Hilfe-Bescheinigung verloren")}, wie ihr an ein Duplikat kommt.'),
 ('wissen/erste-hilfe-kita-pflicht', BIL, f'Welche Anforderungen die DGUV an Schulungen in Kitas und Schulen beschreibt, steht unter {L(BIL, "Erste Hilfe in Kita und Schule")}.'),
 ('wissen/erste-hilfe-kurs-studium', BIL, f'Für Bildungs- und Betreuungseinrichtungen gelten besondere Anforderungen, die der Beitrag {L(BIL, "Erste Hilfe in Kita und Schule")} zusammenfasst.'),
 ('wissen/schulsanitaetsdienst', BIL, f'Welche DGUV-Anforderungen für Schulungen in Kitas und Schulen gelten, beschreibt {L(BIL, "Erste Hilfe in Kita und Schule")}.'),
 ('wissen/erste-hilfe-fuehrerschein', ONL, f'Ob ein reiner Online-Kurs als Nachweis zählt, steht unter {L(ONL, "Erste-Hilfe-Kurs online")}.'),
 ('wissen/erste-hilfe-kurs-gueltigkeit', ONL, f'Zur Frage, ob ein Online-Kurs die Vorgaben erfüllt, siehe {L(ONL, "Erste-Hilfe-Kurs online")}.'),
 ('wissen/erste-hilfe-teilnahmebescheinigung', ONL, f'Was für Betrieb und Führerschein gilt, wenn der Kurs nur online stattfand, erklärt {L(ONL, "Erste-Hilfe-Kurs online")}.'),
 ('wissen/schulungsraum-inhouse-erste-hilfe', QUA, f'Welche Vorgaben zu Gruppengröße und Ausstattung gelten, erklärt der Beitrag {L(QUA, "Qualität im Erste-Hilfe-Kurs")}.'),
 ('wissen/inhouse-erste-hilfe-schulung-ablauf', QUA, f'Woran ihr einen Kurs erkennt, der die Vorgaben der Unfallversicherung erfüllt, steht unter {L(QUA, "Qualität im Erste-Hilfe-Kurs")}.'),
 ('wissen/notfallmanagement-arztpraxis', QUA, f'Zu Gruppengröße, Ausbildungshelfern und Mindestausstattung im Kurs siehe {L(QUA, "Qualität im Erste-Hilfe-Kurs")}.'),
 ('wissen/biostoffe-infektionsschutz-arbeitsplatz', NAD, f'Die Pflichten des Arbeitgebers nach einer Nadelstichverletzung beschreibt {L(NAD, "Nadelstichverletzung: Pflichten nach TRBA 250")}.'),
 ('wissen/infektionsschutzgesetz-meldepflicht', NAD, f'Für den Gesundheitsdienst regelt die TRBA 250 den Umgang mit Stichverletzungen, siehe {L(NAD, "Nadelstichverletzung: Pflichten nach TRBA 250")}.'),
 ('wissen/tetanus-impfschutz-verletzung', NAD, f'Zu Stich- und Schnittverletzungen im Gesundheitsdienst siehe {L(NAD, "Nadelstichverletzung: Pflichten nach TRBA 250")}.'),
 ('wissen/first-responder-helfer-vor-ort', NOT, f'Wie Notfalldaten auf dem Handy hinterlegt werden, damit Helfer sie finden, steht unter {L(NOT, "Notfalldaten und Notfallpass auf dem Handy")}.'),
 ('wissen/erste-hilfe-aussendienst-mobile-beschaeftigte', NOT, f'Wer unterwegs arbeitet, kann Notfalldaten auf dem Handy hinterlegen, siehe {L(NOT, "Notfalldaten und Notfallpass auf dem Handy")}.'),
]
n = 0
for src, tgt, sent in E_:
    f = src + '/index.html'; h = open(f, encoding='utf8').read()
    i = h.find('<main'); k = h.find('<h2>Häufige Fragen', i)
    assert k > 0, src
    if f'href="/{tgt}/"' in h[i:]: continue
    open(f, 'w', encoding='utf8').write(h[:k] + f'<p>{sent}</p>\n' + h[k:]); n += 1
print('eingefügt:', n)
