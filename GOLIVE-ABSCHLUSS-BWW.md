# Go-Live-Abschluss — multiplikatorenstelle.de (BWW)

**Datum:** 2026-08-04 (Go-Live-Tag) · **Finaler Live-Commit:** `ad00835` · **Branch:** codex/live-cleanup → gh-pages
**Zweck:** Referenzdokument für den nächsten BWW-Chat. Alle Deploys, offene Punkte, bewusste Scope-Grenzen.

---

## 1. Deploy-Hashes dieser Session (chronologisch alt → neu)

| # | Commit | Beschreibung |
|---|--------|--------------|
| 1 | `24e9104` | Go-Live-QA: agb.html Meta-Description ergänzt; 2 Wissens-Tabellen in `.table-wrap` (Mobil-@375-Overflow-Schutz) |
| 2 | `bd4ac52` | 4 neue Betriebs-Wissensartikel (EH-Beauftragter, Baustelle, Meldeeinrichtungen, Schichtbetrieb) |
| 3 | `4ec79e1` | 3 weitere Betriebs-Wissensartikel (Leiharbeit/Fremdfirmen, Außendienst/mobil, Material-Prüfung) |
| 4 | `128a15e` | Pre-Go-Live-Audit: llms.txt auf alle 188 Artikel vervollständigt; 8 ungenutzte Bild-Duplikate entfernt |
| 5 | `a88f98e` | 82 Standort-Descriptions einzigartig neu + Umlaut-Fixes (Münster/Osnabrück) |
| 6 | `f95a802` | Interne Verlinkung: 7 Orphan-Artikel eingebunden + Cluster verstärkt |
| 7 | `9048f13` | ⚠️ Firmenname geändert (BWW UG → „Bildungswerk für Wiederbelebung UG") — **war falsch** |
| 8 | `f99d9bf` | ↩️ **Revert** von #7 (kein Handelsregister-Beleg; „BWW UG (haftungsbeschränkt)" ist korrekt) |
| 9 | `1e196d0` | Wissens-Titel geschärft (1 vager Titel: Arbeitsschutz-Grundlagen) |
| 10 | `9b4d7da` | SEO-Fix: /brandschutz/ canonical + og:url selbstreferenziell (statt /kurse/) |
| 11 | `10856af` | Schema: datePublished + dateModified auf allen 188 Wissens-Artikeln (aus git-Historie) |
| 12 | `f80c14c` | Geo-Koordinaten (Worbis/Leinefelde/Duderstadt) + 16 Kurs-Links + 81 Symptom-Cross-Links |
| 13 | `1bca86c` | CWV: Font-Preload site-weit + Hero-LCP-Fix (311 Seiten lazy→fetchpriority) + Homepage-Hero-Preload |
| 14 | `266a7c9` | Social Meta: og:type=article auf 35 Artikeln + twitter:title/description auf 87 Seiten |
| 15 | `1d27dfa` | QUALITAETSNACHWEIS-BWW.md + robots-Disallow |
| 16 | `ef3257c` | DNS-VERIFIKATIONSPLAN-DIENSTAG.md + robots-Disallow |
| 17 | `352a480` | Sitemap: lastmod auf echte git-Daten (statt uniform stale 2026-07-26) |
| 18 | `2e881db` | A11y/CWV (EH-Online-Cross-Check): CTA-Gradient-Kontrast #79bd65→#2f7d5a (5,0:1) + `.termine-list` min-height (CLS) |
| 19 | `ad00835` | Qualitätsnachweis WCAG+CWV-Zeilen ehrlich nachgezogen |

**Vorheriger Live-Stand vor dieser Session:** `7dad36a`.

---

## 2. Offene Punkte — warten auf Ruben / Software / Dienstag

| Punkt | Status | Verantwortlich | Wann |
|-------|--------|----------------|------|
| **SPF + DMARC setzen** | 2 Records fertig vorbereitet; Anleitung `DNS-VERIFIKATIONSPLAN-DIENSTAG.md`. SPF `v=spf1 include:_spf.strato.com ~all`; DMARC `p=quarantine`+rua. DKIM (strato-dkim-0002/0003) bereits aktiv. | **Ruben** (Strato) | **Di 05.08.** |
| **HTTPS-Enforce / Apex-Zert** | **Wurzel = DNS, nicht nur Enforce:** Apex hat nur **1 von 4** GitHub-A-Records (`.108`; `.109/.110/.111` fehlen) → GitHub stellt Apex-Zert nie aus (`CN=*.github.io`), Enforce-Haken oft gesperrt. **www** einwandfrei (Let's Encrypt bis 13.10.2026) → Traffic/Canonical über www, keine Ausfallzeit beim Fix. **Anleitung: `HTTPS-FIX-ANLEITUNG-RUBEN.md`** (Strato: 3 A-Records ergänzen → warten → GitHub Enforce HTTPS). | **Ruben** (Strato Di + GitHub) | offen |
| **Google Search Console** | Verifizierung ausstehend → Städteseiten-Konsolidierung erst danach datenbasiert. | **Ruben** | offen |
| **Nick-Backend endgültig abschalten** | `bww.kurse-verwalten.de` liefert HTTP/2 404 (DNS→GitHub-Pages-IP ohne CNAME = geparkt/tot, nimmt keine Buchungen). Falls separates Backend existiert: final bestätigen. | **Software/Nick** | offen |
| **git-Ref-Housekeeping** | Korrupte lokale Ref `refs/remotes/origin/gh-pages 2` (macOS-Duplikat) im Worktree `bww-website-github`. Pushes funktionieren; .git-Hygiene bereinigen (Ref löschen + gc). | Housekeeping | offen |

---

## 3. Was NICHT im Scope war (bewusst)

- **Firmenname ändern:** geprüft, testweise umgesetzt, **revertiert** — „BWW UG (haftungsbeschränkt)" ist der Handelsregister-Name (HRB 207725, AG Göttingen). Ohne Handelsregisterauszug keine Firmierungsänderung. **Regel: Impressum-/Firmierungsänderung nur mit Beleg.**
- **`bildungswerkwippermann.de` DNS:** Domain ist **nicht registriert** (Whois: frei) → aus DNS-Aufgabe entfernt. (Regel: bei DNS zuerst Whois prüfen.)
- **Resend im BWW-SPF:** gehört NICHT hierher — BWW-Systemversand läuft als `noreply@software-wippermann.de` → in DESSEN SPF. `rsnd.net` (früherer Vorschlag) = HostGator, nicht Resend.
- **Städteseiten löschen/zusammenlegen:** eingefroren bis GSC-Daten (Koordinator-Bremse) — keine Bestandsänderung ohne Zahlen.
- **Standort-Kurs-Links auf ~43 themenfremde Arbeitsschutz-Artikel:** bewusst NICHT gesetzt (kein passender Kurs → wäre Spam statt Relevanz).
- **Preis-Offers auf 5 Inhouse-Kurse:** bewusst offer-los (kein Fixpreis → keinen Preis erfinden).
- **LocalBusiness-Schema:** bewusst nicht — BWW ist reiner Inhouse-Anbieter ohne Ladengeschäft; EducationalOrganization ist korrekt.
- **LetterXpress-Integration:** Spezifikation geliefert (`scratchpad/letterxpress-spec.md`), Implementierung ist Software/Worker-Ressort, nicht Website.
- **interlink-round2-Branch:** obsolet (Symptom-Cross-Links wurden frisch auf dem Live-Branch umgesetzt, f80c14c).

---

## Kennzahlen (Stand ad00835)
- **188** Wissens-Artikel · **18** Kursseiten · **82** Standortseiten (+11 Umlaut-Redirect-Stubs)
- Sitemap **315 URLs** · JSON-LD **>1000 Blöcke, 0 Parse-Fehler** · SSL (www) Let's Encrypt gültig
- Alle Prüf-Kategorien grün — Details in `QUALITAETSNACHWEIS-BWW.md`

*Nächster BWW-Chat: erst `bww-nacht-backlog.md` (Gedächtnis) + dieses Dokument lesen. Live-Stand = `ad00835`.*
