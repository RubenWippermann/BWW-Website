# Übergabe — multiplikatorenstelle.de (BWW)

**Für den nächsten Chat / Menschen, der hier weiterarbeitet.** Kein Statusbericht (der steht im Gedächtnis-Backlog + `GOLIVE-ABSCHLUSS-BWW.md`), sondern die **nicht-offensichtlichen Dinge, die man versehentlich kaputt macht**, wenn man sie nicht kennt. Jeder Punkt hier ist ein „sieht falsch aus, ist aber korrekt so" oder eine Werkzeug-Falle.

---

## 1. „Geschäftsführer" ist RICHTIG — nicht zu „Inhaber" ändern
BWW ist eine **UG (haftungsbeschränkt)** → das Impressum sagt korrekt **„Geschäftsführer: Ruben Wippermann"**. 
- Bei den Schwestersites **PePa und Duderstadt** (e.K. → Einzelkaufmann) heißt es dagegen korrekt **„Inhaber"**. 
- **Nicht angleichen!** Wer BWW auf „Inhaber" ändert, macht es falsch (§ 35 GmbHG/UG). Wer PePa/Duderstadt auf „Geschäftsführer" ändert, ebenso.
- Merkregel: **Rechtsform bestimmt die Bezeichnung.** UG/GmbH → Geschäftsführer; e.K. → Inhaber.

## 2. BWW hat KEINE Zweigniederlassung — und das ist aktiv so dokumentiert
- Impressum: 0× „Zweigniederlassung". Unternehmensprofil sagt ausdrücklich: „BWW unterhält keine weiteren eigenen Standorte oder Zweigstellen."
- Die 82 Standortseiten sind **Inhouse-Einzugsgebiet**, keine Niederlassungen (§ 13 HGB). Adresse überall = Sitz Duderstadt (Worbiser Str. 2).
- Wer „Standort Kassel" o.ä. als eigene Niederlassung darstellt, erzeugt eine Falschangabe. Framing bleibt: „Wir kommen zu Ihnen."

## 3. BG/UK-Abrechenbarkeit — nur Erste-Hilfe-Aus-/Fortbildung, exact-match im Code
**Fachlich:** Über BG/UK (Berufsgenossenschaft/Unfallkasse) abrechenbar sind **nur** die betriebliche **Erste-Hilfe-Aus- und -Fortbildung** (§ 23 Abs. 2 SGB VII, ermächtigte Stelle 8.2122). **Nicht** Brandschutzhelfer, Betriebssanitäter, Evakuierungshelfer, Lehrkräfte, Sanitätshelfer — die trägt der Arbeitgeber (steuerlich absetzbar).
- Diese Fehlerklasse steckte an mehreren Stellen und wurde site-weit korrigiert: Kursseiten-Faktenboxen, `unternehmensprofil/index.html` **und das verlinkte `media/bww-unternehmensprofil.pdf`** (mit ReportLab neu erzeugt, Generator: `scratchpad/gen_profil_pdf.py`).
- **Lehre: verlinkte PDFs/Flyer mitprüfen** — `grep` über HTML findet PDF-Inhalte NICHT. Extraktion via `python3 -c "import pypdf; …"`.

**Im Code** (`assets/booking.js`, Live-Termine-Badges):
```js
var BG_UK_ALLOW = { EHA:1, EHF:1, EHB:1 };
function bgUk(k){ return !!(k && k.bg_uk_abrechenbar && BG_UK_ALLOW[k.kursart]); }
```
- **Feed-Flag UND Allowlist** (subtraktiv): Wenn das Software-Feed bei einem EHA-Termin bewusst `false` setzt, respektiert der Guard das. Nur-Allowlist wäre falsch.
- **EXACT-MATCH auf `kursart`, kein `startsWith`!** `"EHBK".startsWith("EHB")` ist `true` → EHBK (Erste Hilfe am Kind, Baby/Kleinkind) ist **nicht** DGUV-anerkannt, EHB (Bildungs-/Pflegeeinrichtungen) schon. `BG_UK_ALLOW["EHBK"]` = undefined → korrekt ausgeschlossen. Ein `startsWith` würde EHBK fälschlich einschließen.
- Identische Semantik auf allen Schwestersites (EH Online `istBgUk`). Feed-Quellfix ist Software-Ressort; der Guard ist der Schutzwall.

## 4. DNS-Apex-Defekt (HTTPS) — Status & Ursache
- `multiplikatorenstelle.de` (Apex) hatte nur **1 von 4** GitHub-A-Records → Apex-Zert wird nie ausgestellt (`CN=*.github.io`, Browser-Warnung), „Enforce HTTPS" gesperrt.
- **www ist einwandfrei** (Let's Encrypt) und trägt die ganze Seite (CNAME-Datei = www, Canonical = www).
- **Fix vorbereitet, wartet auf Ruben (Di):** `STRATO-DIENSTAG-BWW.md` (3 A-Records ergänzen) + `HTTPS-FIX-ANLEITUNG-RUBEN.md` (GitHub-Haken danach). Null Ausfallzeit.

## 5. resize_window-Falle (KORRIGIERTE Fassung)
- **Es gibt KEINEN festen 508-px-Clamp** (frühere Behauptung war zu stark, von Worbis selbst widerrufen). 375 rendert echt.
- Die echte Falle: `resize_window` **greift nicht, solange das Panel nicht gerendert ist** („The Browser pane is currently hidden") — **meldet aber trotzdem Erfolg**.
- **Regel: nach jedem `resize_window` `innerWidth` gegenprüfen, bevor gemessen wird:**
  ```js
  if (innerWidth !== 375) throw new Error('Viewport ist ' + innerWidth + ', nicht 375');
  ```
- Fallback, wenn der Viewport partout nicht umschaltet: Container per JS hart auf 375 px setzen, Elementränder gegen den Containerrand messen, `overflow-x:auto`-Vorfahren ausnehmen (sonst Fehlalarme bei absichtlich scrollenden Tabellen).
- BWW @375 ist überlaufsicher: `.tf-stadt`-Select trägt `max-width:100%` (kann Container mathematisch nicht überschreiten, rendert nur bei >1 Stadt), Überschriften `overflow-wrap:break-word;hyphens:auto`.

## 6. Live-CSS immer per curl über den HTML-Pfad prüfen, nicht lokal
Nach CSS-Änderungen den **im HTML referenzierten** Stylesheet-Pfad ziehen (`curl … | grep`), nicht die lokale Datei — sonst misst man bei Cache-Buster-Hash-Wechsel den alten Stand und hält den Fix für wirkungslos.

## 7. Deploy & Git-Hygiene
- Deploy: `git push origin codex/live-cleanup:gh-pages` (Worktree `bww-website-live`).
- Die früher korrupten macOS-Duplikat-Refs (`gh-pages 2`, `index 2`) + gc.log sind **entfernt**; `git gc`/`fsck` laufen sauber. Falls wieder `* 2`-Dateien im `.git` auftauchen (Finder/Backup): gefahrlos löschen, es sind Duplikate.

---

## Offene Punkte (extern, nicht Website-Chat)
- **Strato Di:** A-Records + SPF/DMARC (`STRATO-DIENSTAG-BWW.md`) — Ruben.
- **GitHub:** Enforce HTTPS nach Apex-Zert (`HTTPS-FIX-ANLEITUNG-RUBEN.md`) — Ruben.
- **GSC-Verifizierung** → erst danach Städteseiten-Konsolidierung datenbasiert — Ruben.
- **Software-Feed** `/api/kurse` `bg_uk_abrechenbar` an der Quelle korrigieren (Guard ist nur Schutzwall) — Software.
- **2 verwaiste, veraltete Legal-PDFs** `legal/AGB_BWW.pdf` + `legal/Datenschutz_BWW.pdf` (Stand Juni 2026, ohne Erfüllungsort; **nirgends verlinkt**). Live-Recht ist die HTML-AGB (August 2026). Entscheidung offen: neu erzeugen oder entfernen — bewusst nicht eigenmächtig gelöscht (Rechtsdokumente).

## Referenzdokumente im Repo (robots-disallowed)
`GOLIVE-ABSCHLUSS-BWW.md` · `QUALITAETSNACHWEIS-BWW.md` · `STRATO-DIENSTAG-BWW.md` · `HTTPS-FIX-ANLEITUNG-RUBEN.md` · `DNS-VERIFIKATIONSPLAN-DIENSTAG.md` (Detailhintergrund SPF/DMARC).
