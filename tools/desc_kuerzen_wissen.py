#!/usr/bin/env python3
"""Descriptions der Wissensseiten (+unternehmen) von Hand auf <=155 Zeichen gekürzt: je Seite eine Streichung/Umstellung, Aussage bleibt. Idempotent."""
import re, html, sys
E_ = [  # (slug, alt, neu)
 ('adrenalin-autoinjektor-anwenden','und was danach passieren muss','und was danach folgt'),
 ('arbeiten-enge-raeume-behaelter','Warum sind Arbeiten in Behältern, Silos und Schächten so gefährlich?','Behälter, Silos, Schächte: warum so gefährlich?'),
 ('arbeitgeberpflichten-haftung',' erklärt.','.'),
 ('arbeitsmedizinische-vorsorge','nach der ArbMedVV verständlich erklärt','nach ArbMedVV erklärt'),
 ('arbeitsschutzgesetz-arbschg','Pflichten des Arbeitgebers, Rechte','Arbeitgeberpflichten, Rechte'),
 ('arbeitsstaettenverordnung','Was die Arbeitsstättenverordnung (ArbStättV) für','Was die ArbStättV für'),
 ('betrieblicher-ersthelfer-aufgaben','verständlich erklärt','erklärt'),
 ('betriebliches-eingliederungsmanagement-bem','SGB IX verständlich erklärt','SGB IX erklärt'),
 ('betriebliches-gesundheitsmanagement-bgm','Nutzen für Betriebe, Abgrenzung','Nutzen, Abgrenzung'),
 ('betriebssicherheitsverordnung','von der Gefährdungsbeurteilung über','von Gefährdungsbeurteilung über'),
 ('dguv-vorschrift-2-betreuung','Was die DGUV Vorschrift 2 verlangt, welche Betreuungsmodelle','Was DGUV Vorschrift 2 verlangt, welche Modelle'),
 ('ermaechtigte-ausbildungsstelle-pflichten','laufend leisten','leisten'),
 ('erste-hilfe-alkohol-drogennotfall','Warum die stabile Seitenlage lebensrettend ist','Warum die stabile Seitenlage hilft'),
 ('erste-hilfe-am-kind','Fieberkrampf, Sturz und Vergiftung','Fieberkrampf und Vergiftung'),
 ('erste-hilfe-amputationsverletzung',': die richtigen Schritte.','.'),
 ('erste-hilfe-augenverletzung','Umgang mit Fremdkörpern','Fremdkörper'),
 ('erste-hilfe-ausbildungsstelle-gruenden',' – Schritt für Schritt.','.'),
 ('erste-hilfe-aussendienst-mobile-beschaeftigte','Wie Betriebe Erste Hilfe','Erste Hilfe'),
 ('erste-hilfe-baustelle','wie die Notfallmeldung funktioniert','wie die Notfallmeldung läuft'),
 ('erste-hilfe-beauftragter',' Aufgaben im Überblick.',''),
 ('erste-hilfe-bildungseinrichtungen-dguv-anforderungen','Kinder, Handbuch 204-008 und Bagatellverletzungen: Was die DGUV für Erste-Hilfe-Schulungen in Bildungs- und Betreuungseinrichtungen festlegt','Kinder, Handbuch 204-008, Bagatellverletzungen: Was die DGUV für Erste-Hilfe-Schulungen in Bildungs- und Betreuungseinrichtungen vorgibt'),
 ('erste-hilfe-fieberkrampf-kind','Das Kind krampft bei Fieber','Kind krampft bei Fieber'),
 ('erste-hilfe-fieberkrampf-kind','wie man das Kind schützt','wie man es schützt'),
 ('erste-hilfe-fortbildung-intervalle','alle Fristen der Fortbildung im Überblick','alle Fristen im Überblick'),
 ('erste-hilfe-grundausbildung-oder-fortbildung','Welchen Kurs ihr braucht und','Welcher Kurs passt und'),
 ('erste-hilfe-insektenstich','Stachel richtig entfernen','Stachel entfernen'),
 ('erste-hilfe-knopfzelle-verschluckt','Knopfzellen-Batterie verschluckt','Knopfzelle verschluckt'),
 ('erste-hilfe-kurs-kosten-betrieb','Betrieb wirklich zahlt','Betrieb zahlt'),
 ('erste-hilfe-kurs-qualitaet-gruppengroesse-ausstattung','die Qualitätsvorgaben der DGUV für','die DGUV-Qualitätsvorgaben für'),
 ('erste-hilfe-pflanzen-pilzvergiftung','oder jemand hat verdorbene Pilze','oder verdorbene Pilze'),
 ('erste-hilfe-raum','Regelungen nach DGUV Vorschrift 1 und ASR A4.3 erklärt','Regeln nach DGUV Vorschrift 1 und ASR A4.3'),
 ('erste-hilfe-schock',' – Erste Hilfe beim Schock erklärt.','.'),
 ('erste-hilfe-sportverein','Versicherung über die VBG','VBG-Versicherung'),
 ('erste-hilfe-strassenverkehr','Hilfeleistungspflicht nach StGB und StVO','Hilfeleistungspflicht (StGB, StVO)'),
 ('erste-hilfe-tierbiss','warum immer ein Arztbesuch','warum der Arztbesuch'),
 ('erste-hilfe-ueberzuckerung-hyperglykaemie','Anzeichen erkennen, richtig handeln und den Unterschied zur Unterzuckerung kennen.','Anzeichen, richtiges Handeln und der Unterschied zur Unterzuckerung.'),
 ('erste-hilfe-unterzuckerung-diabetes','Symptome von Hypoglykämie,','Hypoglykämie-Symptome,'),
 ('erste-hilfe-veraetzung-haut','kontaminierte Kleidung entfernen','Kleidung entfernen'),
 ('evakuierungshelfer','Brandschutzhelfer und Grundlagen der Gefährdungsbeurteilung','Brandschutzhelfer und Gefährdungsbeurteilung'),
 ('flurfoerderzeuge-stapler-sicherheit',' Sicherheitsregeln für Flurförderzeuge.',''),
 ('fremdfirmen-koordination','Wenn mehrere Firmen an einem Ort arbeiten:','Mehrere Firmen an einem Ort:'),
 ('gefaehrdungsbeurteilung','verständlich erklärt','erklärt'),
 ('gefahrstoffe-haushalt','Quelle: das Sicherheitsdatenblatt','Quelle: Sicherheitsdatenblatt'),
 ('homeoffice-arbeitsschutz','Unfallversicherung erklärt.','Unfallversicherung.'),
 ('leitern-tritte-sicher','Stürze von Leitern gehören','Leiterstürze gehören'),
 ('multiplikatorenstelle-dguv-grundsatz-304-003','Überblick über die drei Grundsätze 304','Überblick: die drei Grundsätze 304'),
 ('notfallmanagement-betrieb','Bausteine und wie man sie übt','Bausteine und Übungen'),
 ('persoenliche-schutzausruestung-psa','Grundlagen der persönlichen Schutzausrüstung nach','Grundlagen der PSA nach'),
 ('qseh-ermaechtigungsverfahren-ablauf','eine Ausbildungsstelle für Erste Hilfe ermächtigt','eine Erste-Hilfe-Ausbildungsstelle ermächtigt'),
 ('reanimation-kind-saeugling','Unterschiede zur Reanimation bei Erwachsenen','Unterschiede zu Erwachsenen'),
 ('schulungsraum-inhouse-erste-hilfe','damit die Erste-Hilfe-Ausbildung im Betrieb','damit die Ausbildung im Betrieb'),
 ('sicherheitsbeauftragter','verständlich erklärt','erklärt'),
 ('sicherheitsdatenblatt-lesen','Sicherheitsdatenblatt beschreibt Gefahren','Sicherheitsdatenblatt nennt Gefahren'),
 ('sicherheitsdatenblatt-lesen','zählen und wie es','zählen, wie es'),
 ('sonnenschutz-uv-arbeitsplatz','das TOP-Prinzip beim UV-Schutz','das TOP-Prinzip'),
 ('was-ist-katastrophenschutz','THW und die Warnung der Bevölkerung','THW und Bevölkerungswarnung'),
 ('../unternehmen','per BG/UK abrechenbar','BG/UK-abrechenbar'),
]
def esc(s): return s.replace('&', '&amp;')
n = 0; bad = []
for slug, a, b in E_:
    f = f'wissen/{slug}/index.html' if not slug.startswith('..') else 'unternehmen/index.html'
    h = open(f, encoding='utf8').read(); m = re.search(r'<meta name="description" content="(.*?)"', h); od = m.group(1)
    d = html.unescape(od).replace('­', '­')
    if a not in d.replace('­', '') and a not in d: 
        if a in d.replace('­', ''): d = d.replace('­', '')
        else: continue   # schon gekürzt
    d = d.replace('­', '') if a not in d else d
    nd = d.replace(a, b, 1)
    h = h.replace(od, esc(nd)); open(f, 'w', encoding='utf8').write(h); n += 1
import glob
for f in glob.glob('wissen/*/index.html') + ['unternehmen/index.html']:
    d = html.unescape(re.search(r'<meta name="description" content="(.*?)"', open(f, encoding='utf8').read()).group(1))
    if len(d) > 155: bad.append((f, len(d), d))
print('Änderungen:', n, 'Rest >155:', len(bad))
for r in bad: print(r)
