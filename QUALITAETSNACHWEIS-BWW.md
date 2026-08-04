# Qualitätsnachweis — multiplikatorenstelle.de (BWW)

**Stand:** 2026-08-04 · **Live-Commit:** `266a7c9` · **Deploy:** GitHub Pages (Branch gh-pages)
**Zweck:** Faktischer Nachweis der Go-Live-Prüfungen. Kein Marketing — geprüft / gefunden / behoben / Status pro Kategorie.

---

## Prüfmatrix

| # | Kategorie | Geprüft | Gefunden | Behoben | Status | Commit |
|---|-----------|---------|----------|---------|--------|--------|
| 1 | Interne Links (tot) | 329 HTML-Seiten, alle internen Links + Assets | 0 tote Links | – | ✅ grün | (Bestand) |
| 2 | Meta-Descriptions | alle Seiten, Eindeutigkeit | agb.html leer; 0 Dubletten | agb-Description ergänzt | ✅ grün | `24e9104` |
| 3 | Sitemap | Vollständigkeit (Wissen/Kurse/statisch) | – | – | ✅ 315 URLs, alle indexierbaren Seiten | (Bestand) |
| 4 | Canonical-Tags | selbstreferenziell, keine Dubletten | /brandschutz/ zeigte auf /kurse/ | canonical+og:url selbstreferenziell | ✅ grün | `9b4d7da` |
| 5 | FAQ-Schema | alle 188 Wissen + 18 Kurse | 0 Parse-Fehler, FAQ wortidentisch | – | ✅ grün | (Bestand) |
| 6 | Schema.org Course | offers/Preis/provider | 5 Inhouse-Kurse ohne Fixpreis (korrekt) | – | ✅ 12/17 mit Preis-Offer, alle mit provider+hasCredential | (Bestand) |
| 7 | Schema.org hasCredential | Kennziffer 8.2122 als Schema | – | – | ✅ echtes EducationalOccupationalCredential (recognizedBy DGUV), 313× | (Bestand) |
| 8 | Schema.org Article-Daten | datePublished/dateModified | fehlten auf allen 188 | aus git-Historie ergänzt | ✅ 188/188 | `10856af` |
| 9 | GeoCoordinates | lokale Suche | nur Startseite | Worbis/Leinefelde/Duderstadt ergänzt | ✅ grün | `f80c14c` |
| 10 | Social Meta (og/twitter) | og:*, twitter:*, og:type | 35× og:type falsch, 87× twitter:title/desc fehlten | korrigiert/ergänzt | ✅ grün | `266a7c9` |
| 11 | WCAG 2.1 AA | Tastatur, Alt, Kontrast, ARIA, Headings, Labels, Skip-Link | CTA-Gradient heller Stop #79bd65 = Weiß 2,26:1 (via EH-Online-Cross-Check; im Erst-Audit nur dunkler Stop gemessen) | hellen Stop → #2f7d5a (5,0:1) | ✅ grün, alle Text/BG ≥4,5:1 | `2e881db` |
| 12 | Core Web Vitals | LCP/CLS/INP/Assets/Font/Nav | Hero-Bild lazy (LCP), Font nicht preloaded; termine-list ohne Höhen-Reserve (CLS, via EH-Online-Cross-Check) | 311 Seiten fetchpriority, Font+Hero-Preload; termine-list min-height:360px | ✅ grün | `1bca86c`,`2e881db` |
| 13 | Nav-Überlauf 1041–1189 | 1041/1100/1150/1189/1201 px | 0 Overflow (kein Worbis-Bug) | – | ✅ grün | (Bestand) |
| 14 | Buchungsflow | Termine, Formular, Validierung, Konsens | – (Prod-sicher getestet, kein POST) | – | ✅ grün, 42 Live-Termine, DS/AGB-Abstufung | (Bestand) |
| 15 | Kontaktformular | Felder, Validierung, Honeypot | – | – | ✅ grün | (Bestand) |
| 16 | Interne Verlinkung | Orphans, Kurs↔Wissen, Cross-Links, Standort→Kurs | 7 Orphans (neue Artikel), 59 Wissen ohne Kurs-Link | Orphan-Fix + 16 Kurs-Links + 81 Symptom-Cross-Links | ✅ grün | `f95a802`,`f80c14c` |
| 17 | Standort-Descriptions | 82 Seiten, Eindeutigkeit + Ortsbezug | generisch/templatisiert | 82 einzigartig neu | ✅ grün | `a88f98e` |
| 18 | Doorway-Audit Standorte | fingierte Ortspräsenz | 0 (ehrliches Inhouse-Framing, Adresse=Duderstadt) | – | ✅ grün | (Bestand) |
| 19 | Umlaut-Redirects | 11 Paare, Sitemap-Hygiene | – | – | ✅ alle 11 korrekt (canonical+noindex+301-Äquiv.) | (Bestand) |
| 20 | Rechtszitate | §26 Abs., §132 SGB V, SGB-Nummern, EHB-UE | EHB=9 UE bestätigt; §132=0; §26 ohne falschen Abs.; SGB alle korrekt (VII/IX) | – | ✅ grün | (Bestand) |
| 21 | Bilder | Alt-Texte, Format, Größe | 0 ohne Alt; on-page WebP <200KB | 8 ungenutzte Duplikate entfernt | ✅ grün | `128a15e` |
| 22 | llms.txt | Vollständigkeit | nur 73/188 („Auswahl") | auf alle 188 ergänzt | ✅ grün | `128a15e` |
| 23 | Nick-Alt-Domain | bww.kurse-verwalten.de | HTTP/2 404 (DNS→Pages-IP, kein CNAME) | – | ✅ geparkt/tot, nimmt keine Buchungen | – |

---

## Offene Punkte (ehrlich dokumentiert — NICHT im Zuständigkeitsbereich der Website-Session)

| Punkt | Status | Verantwortlich | Wann |
|-------|--------|----------------|------|
| **HTTPS-Enforce / Apex-Zertifikat** | 🟢 **erledigt (04.08. abends verifiziert):** Enforce HTTPS an, Apex+www → 301 https://www, HSTS aktiv, Apex-Zert `CN=www…` bis 02.11.2026. These „braucht alle 4 A-Records" widerlegt — 1/4 genügte + Enforce-Haken. | – | ✅ |
| **SPF / DMARC** | Records vorbereitet (nur multiplikatorenstelle.de): SPF `v=spf1 include:_spf.strato.com ~all`, DMARC `p=quarantine`+rua. DKIM (strato-dkim-0002/0003) bereits aktiv. | Ruben (Strato) | ab Di 05.08. |
| **Google Search Console** | Verifizierung ausstehend → Städteseiten-Konsolidierung datenbasiert erst danach. | Ruben | offen |
| **Nick-Backend endgültig abschalten** | Domain liefert 404 (geparkt). Falls separates Backend existiert: final durch Software/Nick bestätigen. | Software/Nick | offen |
| **git-Ref-Housekeeping** | Korrupte lokale Ref `refs/remotes/origin/gh-pages 2` (macOS-Duplikat) im Worktree bww-website-github. Pushes funktionieren; .git-Hygiene bereinigen. | Housekeeping | offen |
| **Firmierung** | Bleibt **„BWW UG (haftungsbeschränkt)"** (Handelsregister-Name, HRB 207725 Amtsgericht Göttingen). Eine testweise Umbenennung wurde geprüft und wieder revertiert (kein Beleg). | – | geklärt |

---

## Kennzahlen (Stand 266a7c9)
- Wissensdatenbank: **188 Artikel** (alle mit Article+FAQPage+Breadcrumb+EducationalOrganization-JSON-LD, datePublished/dateModified, FAQ schema-wortidentisch)
- Kursseiten: **18** (alle mit Course-Schema, provider BWW UG + hasCredential 8.2122, FAQPage)
- Standortseiten: **82** echte (+ 11 Umlaut-Redirect-Stubs), alle mit einzigartiger ortsbezogener Description
- Sitemap: **315 URLs** · JSON-LD site-weit: **>1000 Blöcke, 0 Parse-Fehler**
- SSL (www): Let's Encrypt, verify ok, HTTP/2

*Dieser Nachweis dokumentiert den geprüften Zustand zum genannten Commit. Er ist kein Ersatz für die verbindliche rechtliche/fachliche Auskunft des Anbieters.*
