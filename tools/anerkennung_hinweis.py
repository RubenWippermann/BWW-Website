#!/usr/bin/env python3
"""Lehrbeauftragten-Format: Verneinung des Anerkennungsstatus durch die NEUTRALE AUSKUNFTSFORMEL ersetzen (Jurist-Wortlaut 15.11., Sie, Entwurf Vorbehalt Anwalt).
5 Seiten inkl. JSON-LD (FAQ-Antworten, description). Nicht geschrieben: anerkannt/offiziell/zugelassen/QSEH-registriert/keine Anerkennung als Behauptung. Idempotent. Arbeitet im Verzeichnis des Aufrufs."""
import os, sys
ROOT = os.getcwd()
KONTAKT = 'info@multiplikatorenstelle.de oder +49 (0) 5527 748 7518'
BODY = 'Ob und in welchem Umfang dieser Lehrgang von den Unfallversicherungsträgern anerkannt ist (z. B. nach DGUV Grundsatz 304-003), teilen wir Ihnen vor der Buchung auf Anfrage verbindlich mit: ' + KONTAKT + '. Bitte klären Sie das vorab, wenn die Anerkennung für Sie Voraussetzung ist.'
KURZ = 'Anerkennungsstatus: Auskunft vor Buchung auf Anfrage.'
QN = 'Wie steht es um die Anerkennung des Kurses?'
OLD_Q = 'Ist der Kurs eine von der DGUV anerkannte Maßnahme?'
OLD_A1 = 'Nein. Der Orientierungsrahmen in Anhang 3 der DGUV Grundsatz 304-003 ist eine Empfehlung für Stellen, die Lehrbeauftragte aus- und fortbilden. Der Kurs ist keine beim QSEH-Portal registrierte Maßnahme; die Bescheinigung enthält deshalb keine DGUV-Anerkennung.'
OLD_A2 = 'Nein. Der Aufbau folgt einem Orientierungsrahmen der DGUV für Stellen, die Lehrbeauftragte fortbilden. Der Kurs ist keine beim QSEH-Portal registrierte Maßnahme; die Bescheinigung enthält deshalb keine DGUV-Anerkennung.'
OLD_TL = 'Dieser Lehrgang ist nach dem Orientierungsrahmen in Anhang 3 gestaltet und keine beim QSEH-Portal registrierte Maßnahme.'
OLD_META = '700 €. Keine QSEH-registrierte Maßnahme, keine DGUV-Anerkennung.'
OLD_DESC = ' Keine QSEH-registrierte Maßnahme, keine DGUV-Anerkennung.'
PAGES = {
 'kurse/lehrbeauftragter-erste-hilfe': [
   (OLD_META, '700 €. ' + KURZ, 3), (OLD_DESC, '', 2), (OLD_Q, QN, 2), (OLD_A1, BODY, 2),
   ('<strong>Wichtig: Dieser Lehrgang ist keine bei der QSEH registrierte oder von der DGUV anerkannte Maßnahme.</strong>', '<strong>Hinweis zur Anerkennung.</strong> ' + BODY, 1),
   (OLD_TL, 'Dieser Lehrgang ist nach dem Orientierungsrahmen in Anhang 3 gestaltet. ' + KURZ, 1)],
 'ausbilder-werden/preise': [('700 €; keine QSEH-registrierte Maßnahme, keine DGUV-Anerkennung</li>', '700 €; Anerkennungsstatus: Auskunft vor Buchung auf Anfrage</li>', 1)],
 'ausbilder-werden/lehrbeauftragter': [('Lehrgänge nach dem Orientierungsrahmen in Anhang 3 sind keine beim QSEH-Portal registrierten Maßnahmen.', KURZ, 1)],
 'kurse/lehrbeauftragten-fortbildung': [(OLD_Q, QN, 2), (OLD_A2, BODY, 2), (OLD_TL, 'Dieser Lehrgang ist nach dem Orientierungsrahmen in Anhang 3 gestaltet. ' + KURZ, 1)],
 'fuer-ausbilder': [('Ist der Kurs für Lehrbeauftragte eine von der DGUV anerkannte Maßnahme?', 'Wie steht es um die Anerkennung des Kurses für Lehrbeauftragte?', 2), (OLD_A1, BODY, 2),
   ('an 14 Tagen in Präsenz; keine QSEH-registrierte Maßnahme.</p>', 'an 14 Tagen in Präsenz. ' + KURZ + '</p>', 1),
   ('an 14 Tagen (keine QSEH-registrierte Maßnahme); Fortbildung', 'an 14 Tagen (' + KURZ.rstrip('.') + '); Fortbildung', 1)],
}
for page, reps in PAGES.items():
    p = os.path.join(ROOT, page, 'index.html'); h = open(p, encoding='utf8').read(); h0 = h
    for a, b, n in reps:
        c = h.count(a)
        if c == 0: continue                                   # schon umgesetzt (oder durch Nachzug-Skript veraendert)
        assert c == n, (page, a[:60], c, n)
        h = h.replace(a, b)
    if h != h0: open(p, 'w', encoding='utf8').write(h)
import re
bad = []
for page in PAGES:
    t = open(os.path.join(ROOT, page, 'index.html'), encoding='utf8').read()
    for w in ('QSEH-registrierte', 'QSEH registrierte', 'beim QSEH-Portal registrierte', 'keine DGUV-Anerkennung', 'von der DGUV anerkannte'):
        if w in t: bad.append((page, w))
print('ok; Reste:', bad)
