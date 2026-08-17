#!/usr/bin/env python3
"""BWW build-time JSON-LD generator.

Zieht den Software-Feed und schreibt schema.org-Event+Offer-Auszeichnung
zwischen idempotente Marker in eine statische Kursseite.

Constraints (mit Software-Ressort vereinbart 2026-08-10):
  * NUR Datum + Preis  -> KEINE `availability` (plaetze_frei ist noch nicht belastbar)
  * `?mit_abgesagten=1` abrufen; eventStatus cancelled -> schema EventCancelled
  * buchungs_url UNVERAENDERT uebernehmen (traegt org -> Zahlungsrouting)
  * stabile `id` als Schluessel
Läuft VOR `git push ...:gh-pages`. Reine Standardbibliothek (kein npm/pip).
"""
import json, re, sys, os, hashlib, urllib.request
from datetime import datetime, date
from zoneinfo import ZoneInfo

FEED = "https://software-wippermann.de/api/kurse?org=bww&mit_abgesagten=1"
TZ = ZoneInfo("Europe/Berlin")
# Veranstalter: PRIMÄR aus dem Feld feed["veranstalter"] lesen (autoritativ, mandantenspezifisch).
# Ist es leer/null, Rückfall NICHT auf einen erfundenen Kurznamen ("BWW Deutschland"), sondern auf
# den VERIFIZIERTEN rechtlichen Namen aus dem Impressum + Organization/provider-Block der Seiten.
ORG_URL = "https://www.multiplikatorenstelle.de/"
LEGAL_NAME = "BWW UG (haftungsbeschränkt)"  # Impressum, verifiziert 2026-08-11

def organizer_from(feed):
    v = feed.get("veranstalter") or {}
    name = (v.get("name") or LEGAL_NAME).replace("\u00a0", " ")  # kein Kurznamen-Fallback; NBSP->Space (kanonisch = Space)
    org = {"@type": "Organization", "name": name, "url": v.get("url") or ORG_URL}
    return org
STATUS = {"scheduled": "https://schema.org/EventScheduled",
          "cancelled": "https://schema.org/EventCancelled",
          "postponed": "https://schema.org/EventPostponed",
          "rescheduled": "https://schema.org/EventRescheduled"}
START = "<!-- BWW-FEED-EVENTS:START (auto-generiert, nicht von Hand editieren) -->"
END = "<!-- BWW-FEED-EVENTS:END -->"

# Prerender-Schalter (analog erstehilfekurse.online TERMINE_PRERENDER):
# False = KEINE Termin-Auszeichnung ins HTML backen (Block wird entfernt, Stempel gelöscht),
#         Besucher sehen Termine weiter live per JS. Verhindert veraltete Snapshots an Google,
#         solange KEIN täglicher Cron scharf ist.
# Wieder True setzen, ERST wenn der tägliche Rebuild läuft und den Stempel frisch hält.
PRERENDER = False

def iso(datum, uhrzeit):
    """'2026-08-11','09:00' -> '2026-08-11T09:00:00+02:00' (DST-korrekt via Europe/Berlin)."""
    if not datum:
        return None
    hh, mm = (uhrzeit or "00:00").split(":")[:2]
    dt = datetime(int(datum[:4]), int(datum[5:7]), int(datum[8:10]), int(hh), int(mm), tzinfo=TZ)
    return dt.isoformat()

def parse_addr(adresse, stadt):
    a = {"@type": "PostalAddress", "addressCountry": "DE", "addressLocality": stadt}
    m = re.match(r"^(.*?),\s*(\d{5})\s+(.*)$", adresse or "")
    if m:
        a["streetAddress"], a["postalCode"], a["addressLocality"] = m.group(1), m.group(2), m.group(3)
    return a

def is_past(k, today):
    """endDate (bzw. datum) liegt VOR today -> Vergangenheit, nicht vorrendern."""
    de = k.get("datum_ende") or k.get("datum")
    try:
        return datetime(int(de[:4]), int(de[5:7]), int(de[8:10]), tzinfo=TZ).date() < today
    except Exception:
        return False  # unparsbar -> lieber behalten als still schlucken

def anzeige_titel(t):
    # Anzeige-Guard (gemeinsam mit erstehilfe-duderstadt.de): der interne Auftraggeber-Trenner
    # ' · ' (Leerzeichen-Mittelpunkt-Leerzeichen) haengt den Kundennamen an -> im OEFFENTLICHEN
    # Titel abschneiden. NUR Anzeige: id/buchungs_url/Bewegungs-Hash bleiben roh. Klammern/en-dash bleiben.
    s = str("" if t is None else t)
    return re.split(r"\s+[·•]\s+", s, 1)[0].strip() or s

def to_event(k, organizer):
    ev = {
        "@type": "EducationEvent",
        "@id": f"https://www.multiplikatorenstelle.de/kurse/offene-kurse-worbis/#{k['id']}",
        "name": anzeige_titel(k["titel"]),
        "startDate": iso(k.get("datum"), k.get("uhrzeit")),
        "endDate": iso(k.get("datum_ende") or k.get("datum"), k.get("uhrzeit_ende")),
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "eventStatus": STATUS.get(k.get("eventStatus", "scheduled"), STATUS["scheduled"]),
        "location": {"@type": "Place", "name": k.get("stadt"),
                     "address": parse_addr(k.get("adresse"), k.get("stadt"))},
        "organizer": organizer,
        "offers": {
            "@type": "Offer",
            "price": f"{int(k['preis'])}.00",
            "priceCurrency": "EUR",
            "url": k["buchungs_url"],          # unveraendert, traegt org
            "category": "Kursgebühr pro Person",
            # BEWUSST OHNE availability (plaetze_frei noch nicht belastbar)
        },
    }
    return {kk: vv for kk, vv in ev.items() if vv is not None}

def build_graph():
    # Feed blockt den Default-urllib-UA (403) -> expliziten UA setzen.
    req = urllib.request.Request(FEED, headers={"User-Agent": "BWW-Deploy-JSONLD/1.0 (+multiplikatorenstelle.de)"})
    with urllib.request.urlopen(req, timeout=25) as r:
        data = json.load(r)
    kurse = data.get("kurse", data if isinstance(data, list) else [])
    organizer = organizer_from(data if isinstance(data, dict) else {})
    today = datetime.now(TZ).date()
    upcoming = [k for k in kurse if not is_past(k, today)]        # Vergangenheit build-seitig raus
    events = [to_event(k, organizer) for k in upcoming]
    # Bewegungs-Erkennung je Termin-ID (NICHT Voll-Hash). Grund (gemessen 2026-08-17): mein Feed
    # ist serverseitig zukunftsgefiltert (ab_datum=2020 liefert keine Vergangenheit) -> ein Hash
    # ueber die ganze Antwort kippt taeglich, sobald ein Kurs vorbeizieht, und meldete NIE
    # 'eingefroren'. Korrektur von erstehilfe-duderstadt.de: Feldhash je kuenftigem Termin, Key=id.
    # NEU oder GEAENDERT = Bewegung; reines WEGFALLEN (Zeitablauf) zaehlt NICHT. plaetze_frei NICHT
    # im Hash (eine Buchung darf die Uhr nicht zuruecksetzen).
    hashes = term_hashes(upcoming)
    spaetester = max((k.get("datum", "") for k in upcoming), default="")
    return {"@context": "https://schema.org", "@graph": events}, len(events), hashes, spaetester

def term_hashes(kuenftige):
    h = {}
    for t in kuenftige:
        felder = [t.get("datum"), t.get("datum_ende"), t.get("uhrzeit"), t.get("uhrzeit_ende"),
                  t.get("preis"), t.get("eventStatus"), t.get("plaetze_gesamt"),
                  t.get("ausgebucht"), t.get("kursart"), t.get("stadt")]  # id=Key, plaetze_frei NICHT
        h[str(t.get("id"))] = hashlib.sha1(
            json.dumps(felder, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]
    return h

def inject(html, block):
    payload = f'{START}\n<script type="application/ld+json">\n{block}\n</script>\n{END}'
    if START in html and END in html:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: payload, html, flags=re.S)
    return html.replace("</body>", payload + "\n</body>", 1)

def strip(html):
    """Entfernt den Auszeichnungs-Block wieder (Prerender aus)."""
    return re.sub(r"\n?" + re.escape(START) + r".*?" + re.escape(END) + r"\n?", "\n", html, flags=re.S)

def main():
    args = sys.argv[1:]

    # PRERENDER=False: Block entfernen statt bauen, Stempel löschen, fertig. Kein Feed-Abruf nötig.
    if not PRERENDER:
        target = args[0] if args and not args[0].startswith("--") else None
        if target and "--write" in args:
            with open(target, encoding="utf-8") as f:
                html = f.read()
            with open(target, "w", encoding="utf-8") as f:
                f.write(strip(html))
            if "--stamp" in args:
                sp = args[args.index("--stamp") + 1]
                if os.path.exists(sp):
                    os.remove(sp)
                state_path = os.path.join(os.path.dirname(sp) or ".", "termine-bewegung.json")
                if os.path.exists(state_path):
                    os.remove(state_path)
            sys.stderr.write("[PRERENDER=False] Auszeichnung entfernt, Stempel gelöscht. Termine bleiben live per JS.\n")
        else:
            sys.stderr.write("[PRERENDER=False] Prerender abgeschaltet — nichts zu tun.\n")
        return
    # FRISCHE-WÄCHTER (nicht verhandelbar): toter/leerer Feed -> ABBRUCH, kein Schreiben,
    # Exit!=0, damit der Deploy-Schritt den letzten guten Stand stehen lässt (nie leer pushen).
    # Exit-Code 3 = "Feed tot/leer, Bau abgebrochen". BEWUSST NICHT 2 — im Termin-Verbund ist
    # 2 = "nicht messbar" (Prüfskript), das darf nicht mit "Feed weg" (Bau) kollidieren.
    try:
        graph, n, hashes, spaetester = build_graph()
    except Exception as e:
        sys.stderr.write(f"[ABBRUCH] Feed nicht abrufbar ({e}) — kein Schreiben, letzter Stand bleibt.\n")
        sys.exit(3)
    if n == 0:
        sys.stderr.write("[ABBRUCH] Feed lieferte 0 Kurse — kein Schreiben, letzter Stand bleibt.\n")
        sys.exit(3)

    block = json.dumps(graph, ensure_ascii=False, indent=1)
    target = args[0] if args else None
    if not target or target == "--print":
        print(block)
        sys.stderr.write(f"\n[{n} Events generiert]\n")
        return

    with open(target, encoding="utf-8") as f:
        html = f.read()
    out = inject(html, block)
    write = "--write" in args
    if write:
        with open(target, "w", encoding="utf-8") as f:
            f.write(out)
        sys.stderr.write(f"[geschrieben: {target}, {n} Events]\n")
    else:
        sys.stdout.write(out)
        sys.stderr.write(f"[DRY-RUN {target}: {n} Events, kein Schreiben]\n")

    # Extern prüfbarer Frischestempel (nur bei nachweislich frischem Feed geschrieben).
    # Zeile 1 = gemeinsamer Wächter-Kontrakt: <iso-mit-Zone>\t<anzahl> (Monitore parst NUR die).
    # Danach additive #-Kommentarzeilen (u.a. Frozen-Detection, Mechanik von erstehilfe-duderstadt.de).
    if "--stamp" in args:
        sp = args[args.index("--stamp") + 1]
        ts = datetime.now(TZ).isoformat(timespec="seconds")
        today_iso = date.today().isoformat()
        # Bewegungs-State neben dem Stempel (termine-bewegung.json), im Repo versioniert. Kein
        # externer Speicher: der Repo-Checkout liefert den letzten Stand. Landet auf gh-pages
        # (nicht auf dem Trigger-Branch main) -> kein Selbst-Ausloesen des Workflows.
        state_path = os.path.join(os.path.dirname(sp) or ".", "termine-bewegung.json")
        alt = {}
        try:
            alt = json.load(open(state_path, encoding="utf-8"))
        except (OSError, ValueError):
            pass
        alt_hashes = alt.get("hashes", {}) if isinstance(alt, dict) else {}
        # BEWEGUNG = mind. eine id NEU oder GEAENDERT. Reines Wegfallen (id war da, jetzt weg)
        # zaehlt NICHT -> Zeitablauf, keine Redaktion. Erst-Lauf (kein State) = Bewegung heute.
        bewegt = (not alt_hashes) or any(nid not in alt_hashes or hashes[nid] != alt_hashes[nid]
                                         for nid in hashes)
        bewegung_zuletzt = today_iso if bewegt else alt.get("bewegung_zuletzt", today_iso)
        unv_tage = (date.fromisoformat(today_iso) - date.fromisoformat(bewegung_zuletzt)).days
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump({"bewegung_zuletzt": bewegung_zuletzt, "hashes": hashes}, f,
                      ensure_ascii=False, sort_keys=True)
        lines = [f"{ts}\t{n}",
                 "# startdate_ausgezeichnet=ja",
                 f"# bewegung_zuletzt={bewegung_zuletzt}",
                 f"# unveraendert_seit_tagen={unv_tage}",
                 f"# spaetester_termin={spaetester}"]
        with open(sp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        # Frozen-Warnung: ab 10 Tagen ohne Termin-Bewegung WARNEN, NICHT blockieren (fremder Fehler
        # darf den Deploy nicht kippen). Dead/leer bleibt exit 3; eingefroren ist nur eine Warnung.
        if unv_tage >= 10:
            print(f"::warning::Termine seit {unv_tage} Tagen ohne Bewegung (letzte am {bewegung_zuletzt}) — moeglicherweise eingefrorener Feed, Neubauen hilft nicht.")
        sys.stderr.write(f"[Stempel: {sp} @ {ts}, {n} Events, bewegung_zuletzt={bewegung_zuletzt}, unveraendert_seit_tagen={unv_tage}]\n")

if __name__ == "__main__":
    main()
