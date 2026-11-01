#!/usr/bin/env python3
"""Schritt A (SEO 01.11.): Title (<=60) und Meta Description (<=155) der 20 meistgezeigten Seiten. Idempotent."""
import re, html, sys, os
S = {
 '': ("BWW: Erste Hilfe & Brandschutz inhouse, Kennziffer 8.2122",
      "BWW schult Betriebe, Schulen und Kitas deutschlandweit in Erster Hilfe, Brandschutz und AED. Inhouse oder offen, DGUV-ermächtigt, Bescheinigung digital."),
 'kurse/': ("Alle Kurse: Erste Hilfe, Brandschutz, Sanitäter | BWW",
      "Erste-Hilfe-Ausbildung und -Fortbildung, Brandschutzhelfer, Betriebssanitäter, Lehrkräfte: alle BWW-Kurse im Überblick, freie Termine direkt buchen."),
 'kurse/erste-hilfe-ausbildung/': ("Ersthelfer-Ausbildung im Betrieb, 9 UE, inhouse | BWW",
      "Betriebliche Ersthelfer ausbilden: 9 UE bei euch vor Ort, deutschlandweit, DGUV-ermächtigt (8.2122), Bescheinigung digital. Inhouse-Angebot anfragen."),
 'kurse/erste-hilfe-fortbildung/': ("Erste-Hilfe-Fortbildung für Ersthelfer, 9 UE | BWW",
      "Auffrischung für betriebliche Ersthelfer, in der Regel alle zwei Jahre: 9 UE in Präsenz, inhouse oder offen, Bescheinigung digital direkt nach dem Kurs."),
 'kurse/brandschutzhelfer/': ("Brandschutzhelfer ausbilden, 4 UE nach ASR A2.2 | BWW",
      "Brandschutzhelfer-Ausbildung nach ASR A2.2 (4 UE): Alarmierung, Fluchtwege, Löschübung. In Präsenz, inhouse oder offen, Bescheinigung digital danach."),
 'kurse/betriebssanitaeter-grundkurs/': ("Betriebssanitäter Grundkurs, 63 UE, DGUV 304-002 | BWW",
      "Betriebssanitäter-Grundkurs (63 UE zzgl. Prüfung) für Betriebe mit Sanitäterpflicht: in Präsenz, inhouse oder offen, Bescheinigung digital danach."),
 'inhouse-kurse/': ("Inhouse-Kurse: Erste Hilfe & Brandschutz bei euch | BWW",
      "Erste Hilfe, Brandschutz, Evakuierung, AED und Notfallmedizin bei euch vor Ort: für Unternehmen, Schulen, Kitas und Vereine, deutschlandweit."),
 'notruf-simulator/': ("Notruf-Simulator 112: kostenlos üben, ohne Anmeldung | BWW",
      "Den Notruf 112 üben: Erwachsene oder Kinder spielen den Anruf durch, die Leitstelle fragt nach, am Ende kommt die Auswertung der 5 W-Fragen. Kostenlos."),
 'wissen/kosten-rettungsdienst-krankenwagen/': ("Was kostet der Krankenwagen? Wer RTW & Notarzt zahlt | BWW",
      "Im Notfall zahlt in aller Regel die Krankenkasse, bei Arbeits- und Wegeunfall die BG/UK. Der Notruf 112 ist kostenlos: nie aus Kostenangst zögern."),
 'wissen/erste-hilfe-kurs-inhalte/': ("Erste-Hilfe-Kurs: Inhalte & Ablauf in 9 UE | BWW",
      "Was lernt man im Erste-Hilfe-Kurs? Ablauf, Dauer (9 Unterrichtseinheiten), typische Inhalte und für wen der Kurs anerkannt ist."),
 'wissen/fahrzeuge-rettungsdienst/': ("RTW, KTW, NEF, RTH: Rettungsfahrzeuge erklärt | BWW",
      "Unterschied zwischen RTW, KTW, NEF und Rettungshubschrauber: Aufgabe jedes Fahrzeugs im Rettungsdienst und die Norm DIN EN 1789 dahinter."),
 'wissen/erste-hilfe-teilnahmebescheinigung/': ("Erste-Hilfe-Bescheinigung: Pflichtangaben nach DGUV | BWW",
      "Was muss auf der Erste-Hilfe-Bescheinigung stehen? Pflichtangaben nach DGUV Grundsatz 304-001, Gültigkeit und woran ihr eine ermächtigte Stelle erkennt."),
 'wissen/rettungskette/': ("Rettungskette: die 5 Glieder der Ersten Hilfe | BWW",
      "Die Rettungskette hat fünf Glieder: Sofortmaßnahmen, Notruf 112, Erste Hilfe, Rettungsdienst, Krankenhaus. Das Prinzip kurz und verständlich erklärt."),
 'wissen/notruf-112/': ("Notruf 112: die 5 W-Fragen und was dann passiert | BWW",
      "Wo ist der Notfall, was ist passiert, wie viele Betroffene, welche Verletzungen, auf Rückfragen warten: die 5 W-Fragen. Warum man nie zuerst auflegt."),
 'wissen/erste-hilfe-kurs-gueltigkeit/': ("Wie lange ist ein Erste-Hilfe-Kurs gültig? | BWW",
      "§ 19 FeV nennt für den Führerschein keine Gültigkeitsfrist. Für betriebliche Ersthelfer ist alle zwei Jahre eine Fortbildung nötig. Fristen im Überblick."),
 'wissen/erste-hilfe-fuehrerschein/': ("Erste-Hilfe-Kurs für den Führerschein: 9 UE | BWW",
      "Der Kurs für alle Führerscheinklassen: 9 Unterrichtseinheiten an einem Tag, § 19 FeV ohne Gültigkeitsfrist. Derselbe Kurs zählt als betrieblicher Nachweis."),
 'wissen/reanimation/': ("Reanimation: prüfen, rufen, drücken, AED | BWW",
      "Prüfen, rufen, drücken: 100–120 Kompressionen pro Minute, etwa 5–6 cm tief, Mitte des Brustkorbs. Wann der AED zum Einsatz kommt."),
 'wissen/aed-anwenden-schritt-fuer-schritt/': ("AED anwenden: Schritt für Schritt erklärt | BWW",
      "Ein AED führt per Sprachansage durch die Anwendung: einschalten, Elektroden kleben, Anweisungen folgen und weiter drücken. Der Ablauf im Überblick."),
 'wissen/ersthelfer-anzahl-dguv/': ("Wie viele Ersthelfer braucht ein Betrieb? DGUV | BWW",
      "Ab 2 anwesenden Versicherten mindestens 1 Ersthelfer, über 20 dann 5 % (Verwaltung/Handel) bzw. 10 % (sonstige Betriebe), zu jeder Betriebszeit."),
 'kurse/erste-hilfe-baby-kind/': ("Erste Hilfe am Kind: Kurs für Eltern & Großeltern | BWW",
      "Erste Hilfe bei Baby und Kind (4 UE, Abendkurs): Verschlucken, Fieberkrampf, Reanimation. Für Eltern, Großeltern und Betreuung, mit Übung an Puppen."),
 'wissen/erste-hilfe-bescheinigung-verloren-duplikat/': ("Erste-Hilfe-Bescheinigung verloren? Duplikat anfordern | BWW",
      "Die ausbildende Stelle bewahrt die Kursaufzeichnungen fünf Jahre auf. Mit Name, Geburtsdatum und ungefährem Kursdatum kommt ihr an den Nachweis."),
}
def esc(s): return s.replace('&', '&amp;')
root = sys.argv[1] if len(sys.argv) > 1 else '.'
bad = 0
for p, (t, d) in S.items():
    if len(t) > 60 or len(d) > 155: print('LAENGE', p, len(t), len(d)); bad += 1
if len({t for t, _ in S.values()}) != len(S) or len({d for _, d in S.values()}) != len(S): print('DOPPELT'); bad += 1
if bad: sys.exit(1)
n = 0
for p, (t, d) in S.items():
    f = os.path.join(root, p, 'index.html'); h = open(f, encoding='utf8').read(); o = h
    mt = re.search(r'<title>(.*?)</title>', h, re.S); md = re.search(r'<meta name="description" content="(.*?)"', h)
    ot, od = mt.group(1), md.group(1)
    h = h.replace(f'<title>{ot}</title>', f'<title>{esc(t)}</title>', 1)
    h = h.replace(f'name="description" content="{od}"', f'name="description" content="{esc(d)}"', 1)
    for a, old, new in (('og:title', ot, t), ('twitter:title', ot, t), ('og:description', od, d), ('twitter:description', od, d)):
        h = re.sub(r'(<meta (?:property|name)="%s" content=")%s"' % (a, re.escape(old)), lambda m: m.group(1) + esc(new) + '"', h)
    if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
print('geändert:', n, 'von', len(S))
