# BWW Website

Website der BWW UG (haftungsbeschränkt) für die Multiplikatorenstelle und Rettungsdienstbildungsstelle.

Schwerpunkt: Erste Hilfe, medizinische Breitenausbildung und Ausbildung in der Notfallmedizin.

## Inhalte

- Startseite mit Reanimationsvideo
- Kursbereiche für Erste Hilfe, Erste Hilfe am Kind, Führerschein und Rettungsdienst/Notfallmedizin
- Kursanfrage mit Übergangslösung per E-Mail
- Rechtliche Seiten und PDF-Dokumente
- Vorbereitung für die spätere Anbindung an Software Wippermann

## Entwicklung

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

## Veröffentlichung

Dieses Repository ist als Quelle für die Veröffentlichung gedacht.

Empfohlen ist ein Hosting, das Serverfunktionen unterstützt, zum Beispiel Cloudflare Pages/Workers. GitHub Pages allein ist nur für statische Seiten geeignet und kann die Buchungs-API nicht ausführen.

Bis zur vollständigen Software-Schnittstelle öffnet das Buchungsformular bei fehlender API automatisch eine vorbereitete E-Mail an `info@multiplikatorenstelle.de`.
