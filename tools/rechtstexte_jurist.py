#!/usr/bin/env python3
"""Rechtstexte BWW nach Jurist-Soll (jurist/rechtsseiten-ist-soll-02-11.md, Abschnitt B), Freigabe Betriebsleitung 02.11.: nur diese Stellen, Seitenrahmen unverändert.
AGB (B1-B4, Stand 02.11.2026, gilt für neue Buchungen) und Datenschutz (Einleitung, § 5.2, § 6/6.1). Widerruf, Impressum, Aufrechnung unverändert. Idempotent."""
import re, textwrap, sys
def flex(old):  # Zeilenumbrüche/Leerraum im <pre> tolerieren
    return re.compile(r'\s+'.join(re.escape(w) for w in old.split()))
def wrap(t): return '\n'.join(textwrap.wrap(t, width=104, break_long_words=False, break_on_hyphens=False))
n = 0
def apply(path, pairs, wrapnew=True):
    global n
    h = open(path, encoding='utf8').read(); o = h; miss = []
    for old, new in pairs:
        rx = flex(old)
        if rx.search(h): h = rx.sub(lambda m: wrap(new) if wrapnew else new, h, count=1)
        elif new.split()[0] not in h and flex(new).search(h) is None: miss.append(old[:50])
    if miss: print('FEHLT in', path, miss)
    if h != o: open(path, 'w', encoding='utf8').write(h); n += 1
AGB = [
 ('Dies umfasst insbesondere staatlich und berufsgenossenschaftlich akkreditierte Erste-Hilfe-Kurse (z.B. für betriebliche Ersthelfer gemäß DGUV Vorschrift 1, Führerscheinbewerber gemäß § 19 FeV, Bildungs- und Betreuungseinrichtungen) sowie weiterführende sanitätsdienstliche und pädagogische Fachseminare.',
  'Dies umfasst insbesondere Erste-Hilfe-Kurse, darunter Kurse für betriebliche Ersthelfer nach DGUV Vorschrift 1, für Führerscheinbewerber nach § 19 FeV und für Bildungs- und Betreuungseinrichtungen, soweit die BWW UG (haftungsbeschränkt) dafür als Stelle der gesetzlichen Unfallversicherung ermächtigt (Kennziffer 8.2122) oder anderweitig anerkannt ist, sowie weiterführende sanitätsdienstliche und pädagogische Fachseminare.'),
 ('Erstellung, Lizenzierung und Veräußerung von standardisierten sowie individualisierten Curricula, fachspezifischen Lehrplänen, Präsentationsmedien, QM-Handbüchern und didaktischen Unterrichtsmaterialien in digitaler oder physischer Form.',
  'Erstellung, Einräumung von Nutzungsrechten (Lizenzierung der Unterrichtsmaterialien) und Veräußerung von standardisierten sowie individualisierten Curricula, fachspezifischen Lehrplänen, Präsentationsmedien, QM-Handbüchern und didaktischen Unterrichtsmaterialien in digitaler oder physischer Form; dies umfasst keine Übertragung oder Lizenzierung der Ermächtigung der BWW UG (haftungsbeschränkt).'),
 ('Begleitung von Genehmigungs- und Anerkennungsverfahren: Fachliche Begleitung und administrative Unterstützung bei der Beantragung behördlicher oder berufsgenossenschaftlicher Genehmigungen (z.B. Anerkennung als ermächtigte Stelle für die Erste-Hilfe-Ausbildung nach den Richtlinien der Qualitätssicherungsstelle Erste Hilfe der DGUV oder landesrechtlichen Vorgaben).',
  'Beratung und Begleitung bei Ermächtigungs- und Anerkennungsverfahren Dritter: Fachliche Begleitung und administrative Unterstützung bei der Beantragung behördlicher oder berufsgenossenschaftlicher Genehmigungen (z.B. Ermächtigung als Stelle für die Erste-Hilfe-Aus- und Fortbildung durch die gesetzliche Unfallversicherung nach den Vorgaben der Qualitätssicherungsstelle Erste Hilfe der gesetzlichen Unfallversicherungsträger oder landesrechtlichen Vorgaben). Die Entscheidung trifft die zuständige Stelle; ein Erfolg wird nicht geschuldet; es erfolgt keine Rechtsberatung.'),
 ('Zentrales Regelwerk für Aus- und Weiterbildung, Beratung, Fachkonzepte und Anerkennungsverfahren',
  'Zentrales Regelwerk für Aus- und Weiterbildung, Beratung, Fachkonzepte und Ermächtigungs- und Anerkennungsverfahren (Beratung für Dritte)'),
 ('§ 7 Beratungsverträge, Unterstützung bei Anerkennungsverfahren und Haftungsausschluss',
  '§ 7 Beratungsverträge, Unterstützung bei Ermächtigungs- und Anerkennungsverfahren Dritter und Haftungsausschluss'),
 ('Verträge über strategische Strukturberatungen oder die Begleitung von Anerkennungsverfahren (z. B. der Aufbau einer eigenen Multiplikatorenstelle für Erste Hilfe)',
  'Verträge über strategische Strukturberatungen oder die Begleitung von Ermächtigungs- und Anerkennungsverfahren (z. B. der Aufbau einer eigenen Multiplikatorenstelle für Erste Hilfe)'),
 ('Erteilung von offiziellen Genehmigungen, staatlichen Anerkennungen (z. B. nach § 68 FeV) oder berufsgenossenschaftlichen Ermächtigungen',
  'Erteilung von offiziellen Genehmigungen, behördlichen Anerkennungen (z. B. nach § 68 FeV) oder Ermächtigungen der gesetzlichen Unfallversicherung'),
]
apply('agb/index.html', AGB)
# 7.1-Zusatz (neu) vor 7.2
h = open('agb/index.html', encoding='utf8').read()
ZUS = 'Die Beratung begründet keinen Anspruch darauf, unter der Ermächtigung der BWW UG (haftungsbeschränkt) Kurse durchzuführen; eine Übertragung der Ermächtigung an Dritte ist nicht möglich.'
if 'keinen Anspruch darauf, unter der Ermächtigung' not in h:
    m = re.search(r'\n7\.2 ', h); assert m
    h = h[:m.start()] + '\n' + wrap(ZUS) + h[m.start():]
    open('agb/index.html', 'w', encoding='utf8').write(h); n += 1
# Stand/Datum
h = open('agb/index.html', encoding='utf8').read(); o = h
h = h.replace('(Stand: August 2026)', '(Stand: 02.11.2026)')
h = re.sub(r'Stand: August 2026\. Die nachfolgenden', 'Stand: 02.11.2026 (gilt für Buchungen ab diesem Datum). Die nachfolgenden', h, count=1)
if h != o: open('agb/index.html', 'w', encoding='utf8').write(h); n += 1
DSG = [
 ('Beratungsdienstleistungen sowie Anerkennungsverfahren erheben', 'Beratungsdienstleistungen sowie Beratung bei Ermächtigungs- und Anerkennungsverfahren Dritter erheben'),
 ('zur Ausstellung der amtlichen Teilnahmebescheinigung zwingend erforderlich sind', 'zur Ausstellung der Teilnahmebescheinigung zwingend erforderlich sind'),
 ('§ 6 Datenverarbeitung bei Strukturberatungen und Anerkennungsverfahren', '§ 6 Datenverarbeitung bei Strukturberatungen und der Begleitung von Ermächtigungs- und Anerkennungsverfahren Dritter'),
 ('der Begleitung von behördlichen Anerkennungsverfahren (z. B. Zulassung als ermächtigte Stelle nach § 68 FeV oder DGUV)', 'der Begleitung von behördlichen Ermächtigungs- bzw. Anerkennungsverfahren Dritter (z. B. Ermächtigung als Stelle der gesetzlichen Unfallversicherung oder amtliche Anerkennung nach § 68 FeV)'),
]
apply('datenschutz/index.html', DSG)
h = open('datenschutz/index.html', encoding='utf8').read()
A53 = 'Qualitätssicherungsstelle Erste Hilfe der DGUV bzw. die jeweilige BG zu übermitteln.'
if A53 in h: open('datenschutz/index.html', 'w', encoding='utf8').write(h.replace(A53, 'Qualitätssicherungsstelle Erste Hilfe der gesetzlichen Unfallversicherungsträger bzw. den jeweiligen Unfallversicherungsträger zu übermitteln.', 1)); n += 1   # Jurist-OK 02.11.
print('geändert:', n)
