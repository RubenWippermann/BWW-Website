# Strato-Dienstag (05.08.) — EINE Liste für multiplikatorenstelle.de

**Alles in derselben Strato-Oberfläche** (DNS-Verwaltung von `multiplikatorenstelle.de`), in einer Sitzung, in dieser Reihenfolge. Nur `multiplikatorenstelle.de` (nicht bildungswerkwippermann.de — nicht registriert). **Keine Ausfallzeit**: Die Website läuft über `www.` durchgehend weiter.

Zwei Ziele in einem Rutsch:
- **A** = HTTPS-Reparatur am Apex (3 fehlende A-Records)
- **B** = E-Mail-Sicherheit (SPF + DMARC)

---

## 🚫 NICHT ANFASSEN (sonst geht Mail oder die Domain kaputt)
| Eintrag | Wert (bleibt exakt so) | Warum |
|---|---|---|
| **MX** | `5 smtpin.rzone.de.` | Das ist der Mailempfang. Ändern = keine Mails mehr. |
| **TXT google-site-verification** | `google-site-verification=MKGCCJ…Esi8o` | Search-Console-Nachweis. |
| **CNAME `www`** | `rubenwippermann.github.io` | Trägt die ganze Website. |
| **A `@` = `185.199.108.153`** | (bestehend) | Ist einer der 4 GitHub-IPs — **behalten**, nur ergänzen. |

---

## Schritt 0 — Weiterleitung anlegen (1×, zuerst)
Bei Strato: **Weiterleitung** `dmarc@multiplikatorenstelle.de` → `info@multiplikatorenstelle.de`. (Sammelt später die DMARC-Reports.)

---

## Schritt A — 3 A-Records für HTTPS ergänzen (nur hinzufügen, nichts löschen)
Am Ende müssen **vier** A-Records für den Apex da sein (`.108` existiert schon):

| Typ | Host / Name | Wert |
|---|---|---|
| A | `@` (leer) | `185.199.109.153` |
| A | `@` (leer) | `185.199.110.153` |
| A | `@` (leer) | `185.199.111.153` |

*(Das behebt die Zertifikatswarnung am Apex. Der GitHub-Haken „Enforce HTTPS" kommt später — siehe unten „Teil 2".)*

---

## Schritt B — SPF + DMARC (TXT-Records)
```
Host: @        Typ: TXT   TTL: 3600     ← NEU anlegen (es gibt noch keinen SPF)
Wert: v=spf1 include:_spf.strato.com ~all

Host: _dmarc   Typ: TXT   TTL: 3600     ← bestehenden Eintrag BEARBEITEN (nicht zweiten anlegen!)
Wert: v=DMARC1; p=quarantine; rua=mailto:dmarc@multiplikatorenstelle.de; fo=1
```
- Der `_dmarc` steht heute auf `p=reject` **ohne** SPF — das ist der gefährliche Zustand. Auf obigen Wert **ändern** (`quarantine` = sanfter Zwischenschritt).
- Der SPF-`@`-TXT ist ein **zusätzlicher** TXT neben dem google-site-verification — beide TXT dürfen nebeneinander existieren.

---

## Warten (~30–60 Min), dann prüfen — im Terminal
```bash
# A) Alle 4 Apex-IPs da? (HTTPS-Voraussetzung)
dig +short multiplikatorenstelle.de A
#   erwartet: 185.199.108.153 / .109.153 / .110.153 / .111.153

# B) SPF veröffentlicht?
dig +short TXT multiplikatorenstelle.de
#   muss enthalten: "v=spf1 include:_spf.strato.com ~all"

# C) DMARC korrekt?
dig +short TXT _dmarc.multiplikatorenstelle.de
#   erwartet: "v=DMARC1; p=quarantine; rua=mailto:dmarc@multiplikatorenstelle.de; fo=1"

# D) MX unverändert? (Kontrolle, dass nichts kaputt ging)
dig +short MX multiplikatorenstelle.de
#   muss weiterhin sein: 5 smtpin.rzone.de.
```
Ohne Terminal: mxtoolbox.com/spf und mxtoolbox.com/dmarc → Domain eingeben → grün.

---

## Mail-Funktionstest (kurz)
1. Von `info@multiplikatorenstelle.de` an eine **Gmail**-Adresse mailen → in Gmail „Original anzeigen" → **SPF: PASS, DKIM: PASS, DMARC: PASS**.
2. Aus Gmail zurück an `info@…` antworten → kommt im Strato-Postfach an (Empfang läuft weiter).

---

## Teil 2 — HTTPS-Haken bei GitHub (NICHT bei Strato, erst wenn Schritt A ein paar Stunden her ist)
Sobald `dig` vier Apex-IPs zeigt, stellt GitHub das Apex-Zertifikat aus (meist <1 h). **Danach:**
1. github.com → Repo `rubenwippermann/…` → **Settings** → **Pages**
2. Unter „Custom domain" (`www.multiplikatorenstelle.de`) auf **„DNS check successful"** warten
3. Haken **„Enforce HTTPS"** setzen → fertig.

Prüfen: `curl -sI https://www.multiplikatorenstelle.de | grep -i strict-transport` → muss eine `Strict-Transport-Security`-Zeile liefern. Details + Rückfallplan: **`HTTPS-FIX-ANLEITUNG-RUBEN.md`**.

---

## Rollback (nur falls Mailprobleme)
- DMARC zurück auf `v=DMARC1; p=none; rua=mailto:dmarc@multiplikatorenstelle.de` (beobachtet, blockiert nichts) — sicherer als der alte `p=reject`.
- SPF-TXT wieder entfernen = Ausgangszustand. TTL 3600 → Änderungen greifen binnen 1 Std.
- A-Records `.109/.110/.111` wieder entfernen schadet nicht (www bleibt unberührt), ist aber unnötig.

## Später auf `p=reject` (nicht Dienstag)
Erst nach 1–2 Wochen DMARC-Reports, wenn **alle** legitimen Versender SPF-/DKIM-PASS zeigen und keine echte Mail in Quarantäne landet. Dann `_dmarc`: `quarantine` → `reject`.

## Nicht Teil davon
**Resend** gehört NICHT in diesen SPF — BWW-Systemmail läuft als `noreply@software-wippermann.de` (→ in DESSEN Domain). Falls später Resend für multiplikatorenstelle.de: eigene Records aus dem Resend-Dashboard, nicht raten.
```
DKIM ist bereits aktiv (strato-dkim-0002 RSA + -0003 ed25519) — nichts zu tun.
```
