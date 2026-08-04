# DNS-Verifikationsplan — Dienstag 05.08. (multiplikatorenstelle.de)

Kurz & operativ. Nur `multiplikatorenstelle.de` (bildungswerkwippermann.de ist nicht registriert → entfällt). Gesamtdauer ~5 Min + 30 Min Wartezeit für Propagation.

---

## 0. Vorab (1×, vor allem anderen)
Bei Strato eine **Weiterleitung** `dmarc@multiplikatorenstelle.de` → auf `info@multiplikatorenstelle.de` anlegen. (Sammelt die DMARC-Reports.)

---

## 1. BASELINE — Ist-Zustand (heute gemessen, 2026-08-04)
| Record | Wert JETZT |
|---|---|
| TXT (root) | `google-site-verification=MKGCCJZNzIYbtptyg_RWXWeoNDeqh-XYoH9fzREsi8o` (KEIN SPF) |
| MX | `5 smtpin.rzone.de.` (Strato) |
| `_dmarc` TXT | `v=DMARC1;p=reject;` (ohne rua) |
| DKIM | `strato-dkim-0002` (RSA) + `strato-dkim-0003` (ed25519) — aktiv |

→ Problem: `p=reject` OHNE SPF. Diese Baseline vor der Änderung notieren = jederzeit zurückdrehbar.

---

## 2. ÄNDERUNG — 2 Records bei Strato (DNS-Verwaltung → TXT)
```
Host: @        Typ: TXT   TTL: 3600
Wert: v=spf1 include:_spf.strato.com ~all

Host: _dmarc   Typ: TXT   TTL: 3600   (bestehenden Eintrag BEARBEITEN, nicht zweiten anlegen!)
Wert: v=DMARC1; p=quarantine; rua=mailto:dmarc@multiplikatorenstelle.de; fo=1
```
- SPF: `@` = neuer Eintrag (es gibt noch keinen).
- DMARC: den vorhandenen `p=reject`-Eintrag auf obigen Wert **ändern**.
- Google-site-verification-TXT NICHT anfassen (bleibt).

---

## 3. NACH DER ÄNDERUNG (nach ~30 Min warten) — greifen die Records?
Im Terminal:
```
dig +short TXT multiplikatorenstelle.de
   → muss enthalten:  "v=spf1 include:_spf.strato.com ~all"
dig +short TXT _dmarc.multiplikatorenstelle.de
   → muss sein:       "v=DMARC1; p=quarantine; rua=mailto:dmarc@multiplikatorenstelle.de; fo=1"
```
Alternativ ohne Terminal (Online-Tools):
- SPF: mxtoolbox.com/spf → `multiplikatorenstelle.de` → „SPF Record Published" grün.
- DMARC: dmarcian.com/dmarc-inspector oder mxtoolbox.com/dmarc → `p=quarantine` + rua sichtbar.

**Wenn beide Werte erscheinen: Records greifen.** (Falls nicht → weitere 30–60 Min Propagation abwarten.)

---

## 4. FUNKTIONSTEST — Postfach empfängt + Auth passt
1. **Ausgehend/Auth:** Vom Strato-Postfach `info@multiplikatorenstelle.de` eine Mail an eine **Gmail-Adresse** senden. In Gmail: Mail öffnen → ⋮ → „Original anzeigen". Erwartung:
   - `SPF: PASS`
   - `DKIM: 'PASS' with domain multiplikatorenstelle.de`
   - `DMARC: 'PASS'`
2. **Eingehend:** Von der Gmail-Adresse eine Antwort an `info@multiplikatorenstelle.de` schicken → muss im Strato-Postfach ankommen (bestätigt: Empfang läuft weiter).

Wenn 1) alle drei PASS zeigt und 2) ankommt → Setup funktioniert.

---

## 5. MONITORING (48h)
- DMARC-Reports (tägliche XML) laufen an **`dmarc@multiplikatorenstelle.de`** → weitergeleitet auf `info@`.
- Optional bequemer: kostenlosen DMARC-Report-Reader nutzen (z.B. dmarcian, postmarkapp.com/dmarc) und `rua` dorthin zeigen lassen — dann Reports als Dashboard statt XML.
- Worauf achten: Tauchen **legitime** Versender auf, die SPF/DKIM NICHT bestehen? (z.B. ein Newsletter-Tool, das noch nicht im SPF steht.) Diese müssten ergänzt werden.

---

## 6. ESKALATION — wann von quarantine auf reject?
`p=quarantine` bleibt der Zwischenschritt. Auf **`p=reject`** wechseln, wenn ALLE erfüllt:
- [ ] Mind. **1–2 Wochen** DMARC-Reports ausgewertet.
- [ ] **Alle legitimen Versender** zeigen in den Reports SPF- ODER DKIM-Alignment = PASS (Strato-Postfach: DKIM+SPF pass; ggf. weitere Dienste ergänzt).
- [ ] **Keine** legitime Mail landet fälschlich in Quarantäne.

Dann `_dmarc` erneut bearbeiten: `p=quarantine` → `p=reject` (rua beibehalten).

---

## Rollback (falls Mail-Probleme)
- DMARC zurück auf die Baseline `v=DMARC1;p=reject;` ODER (sicherer bei Unklarheit) `v=DMARC1;p=none;rua=mailto:dmarc@multiplikatorenstelle.de` (nur beobachten, nichts blockieren).
- SPF-TXT entfernen stellt den Ausgangszustand her. TTL 3600 = Änderungen greifen binnen 1 Std.

## Nicht Teil dieser Aufgabe (separat)
- **Resend** gehört NICHT in diesen SPF (BWW sendet Systemmail als `noreply@software-wippermann.de` → dort). Falls später doch Resend für multiplikatorenstelle.de: eigene Records (`send.`-Subdomain + `resend._domainkey`) aus dem Resend-Dashboard, NICHT raten.
