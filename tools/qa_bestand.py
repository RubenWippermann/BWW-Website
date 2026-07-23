#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bestandsprüfung für die BWW-Website.

Prüft den gesamten Seitenbestand auf die Fehlerklassen, die am 2026-07-23
gefunden wurden — und vermeidet dabei die sieben Messfallen desselben Tages.

    python3 tools/qa_bestand.py

Die Messfallen, die hier fest eingebaut sind:
  1. Schmales/geschütztes Leerzeichen  -> WS statt " " in jedem Muster
  2. Attribute werden beim Tag-Strippen unsichtbar -> separat gescannt
  3. Muster erkennt die eigene Korrektur nicht -> Vorkontext wird geprüft
  4. Abkürzungen (mind./min.) -> im Muster enthalten
  5. Trennstriche in PDF-Volltext -> enthyphenate() für externe Quellen
  6. scrollWidth ist blind für Überlauf -> gehört in die Browser-Messung,
     hier nur als Hinweis vermerkt
  7. Überraschend hoher Befund -> Verdacht auf defektes Muster, wird gemeldet
"""
import os, re, html, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Jede Whitespace-Stelle in einem Muster: normal, schmal (U+2009), geschützt (U+00A0)
WS = r'[\s  ]*'
WS1 = r'[\s  ]+'

AUSGESCHLOSSEN = {'.git', '.claude', 'media', 'assets', 'tools', 'node_modules'}


def seiten():
    for root, dirs, fs in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in AUSGESCHLOSSEN]
        for f in fs:
            if f == 'index.html':
                yield os.path.join(root, f)


def entext(s):
    """Sichtbarer Text - Skripte raus, Tags raus, Entities auflösen."""
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r'<style.*?</style>', ' ', s, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s)))


def attribute(s):
    """Alle prüfenswerten Attributwerte - die beim Tag-Strippen verschwinden."""
    raus = []
    for attr in ('content', 'alt', 'aria-label', 'title'):
        for m in re.finditer(r'\b' + attr + r'="([^"]*)"', s):
            raus.append((attr, html.unescape(m.group(1))))
    return raus


def entfernen_hyphen(t):
    """Für extrahierte PDFs: Trennstriche am Zeilenende auflösen."""
    return re.sub(r'\s+', ' ', re.sub(r'-\s*\n\s*', '', t))


# ── Prüfungen ────────────────────────────────────────────────────────────────

def pruef_richtwert_als_pflicht(pfad, roh, text, attrs):
    """5-%-Angaben, die als Untergrenze statt als Richtwert formuliert sind."""
    treffer = []
    muster = re.compile(r'(mind\.|mindestens|min\.|wenigstens)' + WS1 + r'\d+' + WS + r'(?:%|Prozent)', re.I)
    for quelle, inhalt in [('text', text)] + [('@' + a, v) for a, v in attrs]:
        for m in muster.finditer(inhalt):
            umfeld = inhalt[max(0, m.start() - 160):m.end() + 160]
            if re.search(r'ausreich|Richtwert|Orientierung', umfeld, re.I):
                continue  # bereits als Richtwert eingeordnet
            treffer.append((quelle, m.group(0), umfeld[:150]))
    return treffer


def pruef_schwellen(pfad, roh, text, attrs):
    """Ausschliessende Normschwellen, die einschliessend beschriftet sind."""
    treffer = []
    # §27: "mehr als 250" / "mehr als 1500" / Baustelle "mehr als 100"
    muster = re.compile(r'(?<!mehr als )(?<!als )\b250' + WS + r'(?:–|-|bis)' + WS + r'1[.   ]?500'
                        r'|\bzwischen' + WS1 + r'250' + WS1 + r'und'
                        r'|\bab' + WS1 + r'(?:1[.   ]?500|100|250)' + WS1 + r'(?:gleichzeitig' + WS1 + r')?(?:anwesenden?' + WS1 + r')?(?:Versicherten|Beschäftigten)', re.I)
    for quelle, inhalt in [('text', text)] + [('@' + a, v) for a, v in attrs]:
        for m in muster.finditer(inhalt):
            vor = inhalt[max(0, m.start() - 40):m.start()]
            if re.search(r'mehr als' + WS1 + r'$', vor, re.I):
                continue  # bereits korrigiert - Vorkontext beachten (Messfalle 3)
            treffer.append((quelle, m.group(0), inhalt[max(0, m.start() - 90):m.end() + 90]))
    return treffer


def pruef_beschreibung(pfad, roh, text, attrs):
    """Textbaustein-Beschreibungen und Beschreibungen, die nur den Titel wiederholen."""
    treffer = []
    t = re.search(r'<title>(.*?)</title>', roh, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', roh)
    if not d:
        return [('fehlt', 'keine description', '')]
    desc = html.unescape(d.group(1))
    if 'verständlich erklärt für Betriebe' in desc:
        treffer.append(('@description', 'Textbaustein', desc[:110]))
    if t:
        titel = html.unescape(t.group(1)).split('|')[0].strip()
        # Nur melden, wenn die Beschreibung ausser dem Titel kaum etwas beitraegt.
        # Eine Beschreibung, die mit dem Thema beginnt und dann informiert, ist gut
        # - sonst produziert die Regel Fehlalarme (Messfalle 3).
        if len(titel) > 18 and desc.lower().startswith(titel.lower()[:28]):
            zusatz = desc[len(titel):].strip(' :–-') if len(desc) > len(titel) else ''
            if len(zusatz) < 45:
                treffer.append(('@description', 'trägt über den Titel hinaus kaum Information', desc[:110]))
    # Einschraenkung muss den Snippet-Schnitt ueberleben.
    # Zwei Faelle, der zweite ist der gefaehrliche:
    #   a) Einschraenkung beginnt erst NACH dem Schnitt -> unsichtbar
    #   b) Einschraenkung wird MITTENDRIN zerschnitten -> unlesbarer Torso,
    #      schlimmer als gar keine, weil sichtbar etwas fehlt
    # Nur melden, wenn KEINE andere Einschraenkung vollstaendig sichtbar bleibt.
    # ACHTUNG: Diese Regel ist bewusst breit und liefert Verdachtsfaelle, keine
    # Befunde - am 2026-07-23 waren 10 von 12 Treffern harmlos (nur ein
    # Folgewort brach ab). Jeder Treffer gehoert einzeln angesehen; NICHT
    # pauschal auf eine Zeichenzahl trimmen.
    GRENZE = 155
    if len(desc) > GRENZE:
        einschr = list(re.finditer(
            r'\b(?:nicht|kein\w*|nur|ausgenommen|ersetzt|dagegen|ohne|sofern)\b[^.;–—]{0,80}', desc, re.I))
        zerschnitten = [e for e in einschr if e.start() < GRENZE < e.end()]
        nach_schnitt = [e for e in einschr if e.start() >= GRENZE]
        ganz_sichtbar = [e for e in einschr if e.end() <= GRENZE]
        if (zerschnitten or nach_schnitt) and not ganz_sichtbar:
            e = (zerschnitten or nach_schnitt)[0]
            treffer.append(('@description',
                            'VERDACHT: Einschränkung überlebt den Snippet-Schnitt nicht – einzeln prüfen',
                            f'sichtbar endet …{desc[max(0,GRENZE-40):GRENZE]}| weg: {desc[GRENZE:e.end()][:50]}'))
    return treffer


def pruef_verweis_ohne_link(pfad, roh, text, attrs):
    """Nennt die Seite ein eigenes Werkzeug, ohne irgendwo darauf zu verlinken?"""
    ZIELE = {r'(?:DGUV-)?Rechner': '/dguv-rechner/',
             r'Arbeitsschutz-Check': '/arbeitsschutz-check/',
             r'Wissensdatenbank': '/wissen/'}
    treffer = []
    for wort, ziel in ZIELE.items():
        if re.search(r'unser\w*' + WS1 + r'(?:\w+' + WS1 + r')?' + wort, text, re.I):
            if f'href="{ziel}"' not in roh:
                treffer.append(('text', f'nennt {ziel} ohne Link', ''))
    return treffer


def pruef_veraltete_norm(pfad, roh, text, attrs):
    """Überholte Norm-Kürzel, die heute anders heißen.

    Bewusst NUR eindeutige Kürzel, die als Zitat immer falsch sind. NICHT
    '16 UE' (bei Betriebssanitäter-/Lehrkräfte-Fortbildung korrekt) und NICHT
    'lebensrettende Sofortmaßnahmen' (allgemeiner Begriff, nicht der alte
    Führerschein-Kursname) - beide waren am 2026-07-23 Fehlalarme.
    """
    UEBERHOLT = {
        r'\bBGV\s*A1\b': 'BGV A1 → heute DGUV Vorschrift 1',
        r'\bBGV\s*A8\b': 'BGV A8 → heute DGUV Vorschrift/ASR A1.3',
        r'\bGUV-?V\s*A1\b': 'GUV-V A1 → heute DGUV Vorschrift 1',
        r'\bBGR\s*\d': 'BGR → heute DGUV Regel',
        r'\bBGI\s*\d': 'BGI → heute DGUV Information',
        r'\bBGG\s*\d': 'BGG → heute DGUV Grundsatz',
    }
    treffer = []
    for quelle, inhalt in [('text', text)] + [('@' + a, v) for a, v in attrs]:
        for rx, hinweis in UEBERHOLT.items():
            for m in re.finditer(rx, inhalt):
                treffer.append((quelle, hinweis, inhalt[max(0, m.start() - 60):m.end() + 60]))
    return treffer


PRUEFUNGEN = [
    ('Richtwert als Pflicht formuliert', pruef_richtwert_als_pflicht),
    ('Normschwelle falsch beschriftet', pruef_schwellen),
    ('Beschreibung schwach oder abgeschnitten', pruef_beschreibung),
    ('Verweis ohne Link (Sackgasse)', pruef_verweis_ohne_link),
    ('Überholte Normbezeichnung', pruef_veraltete_norm),
]


def main():
    alle = list(seiten())
    befunde = defaultdict(list)
    for p in alle:
        roh = open(p, encoding='utf-8', errors='ignore').read()
        text = entext(roh)
        attrs = attribute(roh)
        for name, fn in PRUEFUNGEN:
            for quelle, was, kontext in fn(p, roh, text, attrs):
                befunde[name].append((os.path.relpath(p, ROOT), quelle, was, kontext))

    print(f"Geprüft: {len(alle)} Seiten\n")
    gesamt = 0
    for name, _ in PRUEFUNGEN:
        liste = befunde[name]
        gesamt += len(liste)
        print(f"── {name}: {len(liste)}")
        for pfad, quelle, was, kontext in liste[:12]:
            print(f"     {pfad}  [{quelle}]")
            print(f"       {was}")
            if kontext:
                print(f"       …{kontext.strip()[:130]}…")
        if len(liste) > 12:
            print(f"     … und {len(liste)-12} weitere")
        print()

    # Messfalle 7: ueberraschend hoher Befund -> erst das Muster verdaechtigen
    if gesamt > len(alle) * 0.25:
        print("⚠️  Sehr viele Treffer im Verhältnis zum Bestand.")
        print("    Erst das Suchmuster prüfen, dann den Bestand (Messfalle 7).")
    print(f"Befunde gesamt: {gesamt}")
    return 1 if gesamt else 0


if __name__ == '__main__':
    sys.exit(main())
