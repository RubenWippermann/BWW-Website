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

def to_event(k, organizer):
    ev = {
        "@type": "EducationEvent",
        "@id": f"https://www.multiplikatorenstelle.de/kurse/offene-kurse-worbis/#{k['id']}",
        "name": k["titel"],
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
    # Fingerabdruck ueber den ROHEN Feed (VOR dem Vergangenheits-Filter): die gefilterte Liste
    # verliert taeglich Vergangenes und meldete darum ewig 'frisch'. Feldliste = was ein gesunder
    # Feed real aendert; deckungsgleich mit erstehilfe-duderstadt.de, damit Stempel vergleichbar.
    fp = fingerabdruck(kurse)
    spaetester = max((k.get("datum", "") for k in upcoming), default="")
    return {"@context": "https://schema.org", "@graph": events}, len(events), fp, spaetester

def fingerabdruck(roh_kurse):
    kanon = json.dumps(
        sorted([[t.get("id"), t.get("datum"), t.get("uhrzeit"), t.get("uhrzeit_ende"),
                 t.get("preis"), t.get("eventStatus"), t.get("plaetze_gesamt"), t.get("ausgebucht")]
                for t in roh_kurse], key=lambda r: str(r[0])),
        ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(kanon.encode("utf-8")).hexdigest()[:12]

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
                import os
                sp = args[args.index("--stamp") + 1]
                if os.path.exists(sp):
                    os.remove(sp)
            sys.stderr.write("[PRERENDER=False] Auszeichnung entfernt, Stempel gelöscht. Termine bleiben live per JS.\n")
        else:
            sys.stderr.write("[PRERENDER=False] Prerender abgeschaltet — nichts zu tun.\n")
        return
    # FRISCHE-WÄCHTER (nicht verhandelbar): toter/leerer Feed -> ABBRUCH, kein Schreiben,
    # Exit!=0, damit der Deploy-Schritt den letzten guten Stand stehen lässt (nie leer pushen).
    # Exit-Code 3 = "Feed tot/leer, Bau abgebrochen". BEWUSST NICHT 2 — im Termin-Verbund ist
    # 2 = "nicht messbar" (Prüfskript), das darf nicht mit "Feed weg" (Bau) kollidieren.
    try:
        graph, n, fp, spaetester = build_graph()
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
        # Carry-forward: alten Stempel lesen; wenn Fingerabdruck gleich -> altes 'seit'-Datum halten,
        # sonst heute. Kein externer State: der Wert reist IM Stempel mit (Repo-Checkout liefert ihn).
        alt_fp = alt_seit = None
        try:
            alt = open(sp, encoding="utf-8").read()
            m1 = re.search(r"# fingerabdruck=(\w+)", alt)
            m2 = re.search(r"# fingerabdruck_seit=(\d{4}-\d{2}-\d{2})", alt)
            alt_fp = m1.group(1) if m1 else None
            alt_seit = m2.group(1) if m2 else None
        except OSError:
            pass
        seit = alt_seit if (alt_fp == fp and alt_seit) else today_iso
        unv_tage = (date.fromisoformat(today_iso) - date.fromisoformat(seit)).days
        lines = [f"{ts}\t{n}",
                 "# startdate_ausgezeichnet=ja",
                 f"# fingerabdruck={fp}",
                 f"# fingerabdruck_seit={seit}",
                 f"# unveraendert_seit_tagen={unv_tage}",
                 f"# spaetester_termin={spaetester}"]
        with open(sp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        # Frozen-Warnung: ab 10 Tagen unveraendert WARNEN, aber NICHT blockieren (fremder Fehler
        # darf den Deploy nicht kippen). Dead/leer bleibt exit 3; eingefroren ist nur eine Warnung.
        if unv_tage >= 10:
            print(f"::warning::Feed unveraendert seit {unv_tage} Tagen (Fingerabdruck {fp} seit {seit}) — moeglicherweise eingefroren, Neubauen hilft nicht.")
        sys.stderr.write(f"[Stempel: {sp} @ {ts}, {n} Events, fp={fp}, unveraendert_seit_tagen={unv_tage}]\n")

if __name__ == "__main__":
    main()
