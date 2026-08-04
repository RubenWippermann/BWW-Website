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
- **EXACT-MATCH auf `kursart`, kein `startsWith`!** Rein als Code-Sicherheit: `"EHBK".startsWith("EHB")` ist `true` — ein `startsWith` würde EHBK (Erste Hilfe am Kind, nicht DGUV-anerkannt) fälschlich einschließen. Der Objekt-Lookup `BG_UK_ALLOW["EHBK"]` = undefined schließt es korrekt aus. **Wichtig:** Das ist ein hypothetischer Code-Punkt, **kein** realer Datenvorfall — der Software-Chat hat auf der Produktionsdatenbank gemessen: **71 EHBK-Kurse, 0 mit falschem BG/UK-Flag**. EHBK war nie betroffen; nicht als vergangenen Fehler weiterschreiben.
- **Echte Ursache (an der Quelle gefixt, `61feedaa`):** Die Software hat *keine* Negativ-Logik, alles läuft über eine Positivliste. Der Fehler war ein **klebendes BG-Flag beim Kursart-Wechsel** — Kurs als Erste-Hilfe anlegen (BG-Flag automatisch gesetzt) → auf z. B. Brandschutzhelfer umstellen → Titel/Zeiten/Preis wurden überschrieben, aber das BG-Flag mit dem **alten Wert verodert** und blieb stehen. Das erklärt, wie eine falsche Rechtsaussage auf mehreren Sites lief, obwohl Code und Formattabelle korrekt waren.
- Identische Guard-Semantik auf allen Schwestersites (EH Online `istBgUk`). Quellfix ist erfolgt; der Client-Guard bleibt als **redundanter Schutzwall** für Rechtsaussagen sinnvoll.

## 4. DNS-Apex-Defekt (HTTPS) — Status & Ursache
- `multiplikatorenstelle.de` (Apex) hatte nur **1 von 4** GitHub-A-Records → Apex-Zert wird nie ausgestellt (`CN=*.github.io`, Browser-Warnung), „Enforce HTTPS" gesperrt.
- **www ist einwandfrei** (Let's Encrypt) und trägt die ganze Seite (CNAME-Datei = www, Canonical = www).
- **Fix vorbereitet, wartet auf Ruben (Di):** `STRATO-DIENSTAG-BWW.md` (3 A-Records ergänzen) + `HTTPS-FIX-ANLEITUNG-RUBEN.md` (GitHub-Haken danach). Null Ausfallzeit.

## 5. resize_window / innerWidth — richtig verstanden
- **`innerWidth ≠ Zielbreite` ist das DIAGNOSEWERKZEUG, nicht das Hindernis.** Überlaufender Inhalt zieht `innerWidth` selbst mit hoch: ein 900-px-Element in einer 375-px-Seite lässt `innerWidth` von 375 auf 900 springen. Die **Differenz gibt die Größenordnung des Überlaufs**. (Reales Beispiel: ein 486-px-Select + Container-Padding = exakt die berüchtigten 508 px; nach dem Fix stand `innerWidth` wieder auf 375.)
- Es gibt **keinen** festen 508-Clamp, und es ist auch nicht primär „Panel nicht gerendert" — **beide früheren Erklärungen waren falsch**. Ein nicht gerendertes Panel / Hintergrund-Tab kann *zusätzlich* verhindern, dass der Resize greift (meldet dann `innerWidth 0`); dieselbe Prüfung fängt beides ab.
- **Regel: nach jedem `resize_window` `innerWidth` gegenprüfen** — aber als Befund lesen, nicht als Werkzeug-Verdacht:
  ```js
  if (innerWidth !== 375) throw new Error('innerWidth=' + innerWidth + ' → hier läuft etwas über ODER Resize griff nicht');
  ```
- Fallback (nur wenn nötig): Container per JS hart auf 375 px, Elementränder gegen den Containerrand messen, `overflow-x:auto`-Vorfahren ausnehmen (sonst Fehlalarme bei absichtlich scrollenden Tabellen).
- **Meta-Lehre (Worbis, teuer gelernt):** Vor einer neuen Werkzeug-Theorie erst im Gedächtnis nachsehen, ob das Phänomen schon beschrieben ist — die richtige Erklärung stand seit 23.07. dort; zwei erfundene Begründungen kosteten 3 Korrekturrunden über 5 Chats. Eine falsche Begründung führt vom Befund weg: wer das Tool verdächtigt, sucht nicht nach dem Überlauf.
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
- **Software-Feed** `/api/kurse` `bg_uk_abrechenbar` — Quellfix erfolgt (`61feedaa`, klebendes Flag beim Kursart-Wechsel); Client-Guard bleibt als Schutzwall — Software (erledigt, Beobachtung).

## Erledigt in dieser Runde (Kontext, kein offener Punkt)
- **2 verwaiste, veraltete Legal-PDFs** (AGB/Datenschutz, Stand Juni 2026, ohne Erfüllungsort, nirgends verlinkt) **aus dem Deploy genommen** (`git rm` aus `legal/`), aber **nicht gelöscht**: archiviert außerhalb des ausgelieferten Baums unter `Documents/Software PePa und BWW/archiv-legal-bww/` (mit „Stand-Juni-2026"-Dateinamen als Beleg der damals geltenden Fassung). Grund: eine per URL erreichbare alte AGB-Fassung ist im Streitfall angreifbar — es soll nur **eine** Fassung erreichbar sein (die HTML-AGB August 2026). Eine PDF-Fassung der aktuellen AGB würde bei Bedarf aus dem geltenden HTML erzeugt (kann dann nicht driften).
- **Nebenartefakt-Audit** (PDFs/llms.txt/favicon/OG-Bilder) auf Fremdfirma/Kennziffer + Ligaturen: sauber (Details im Backlog).

## Referenzdokumente im Repo (robots-disallowed)
`GOLIVE-ABSCHLUSS-BWW.md` · `QUALITAETSNACHWEIS-BWW.md` · `STRATO-DIENSTAG-BWW.md` · `HTTPS-FIX-ANLEITUNG-RUBEN.md` · `DNS-VERIFIKATIONSPLAN-DIENSTAG.md` (Detailhintergrund SPF/DMARC).
