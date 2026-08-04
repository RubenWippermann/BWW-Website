# HTTPS-Fix multiplikatorenstelle.de — Anleitung für Ruben

**Stand der Messung:** 2026-08-04, 12:30 Uhr · **Für:** spätabends, wenig Zeit
**Kernaussage vorab:** Es sind **zwei getrennte Dinge**. Das eigentliche Nadelöhr ist ein **DNS-Defekt** (nur 1 von 4 Apex-Einträgen) — das erledigst du bei **Strato**, zusammen mit der SPF/DMARC-Arbeit am Dienstag. Der GitHub-Klick kommt **danach**.

**Die Seite geht bei keinem der Schritte offline.** Die Live-Seite läuft über `www.` — und die bleibt die ganze Zeit erreichbar.

---

## 1. Aktueller Messstand (heute geprüft)

| Was | Ist-Zustand | Bewertung |
|-----|-------------|-----------|
| `www.multiplikatorenstelle.de` (die echte Seite) | HTTPS gültig, Let's Encrypt bis **13.10.2026**, HTTP/2 200 | ✅ einwandfrei |
| `http://www…` (unverschlüsselt) | liefert **200 OK** (keine Weiterleitung auf HTTPS) | ⚠️ Klartext erreichbar |
| HSTS-Header | **fehlt** überall | ⚠️ „Enforce HTTPS" ist aus |
| `https://multiplikatorenstelle.de` (ohne www) | liefert falsches Zertifikat `CN=*.github.io` → **Browser-Warnung** | ⚠️ Apex-Zert fehlt |
| **Apex-DNS `multiplikatorenstelle.de`** | nur **1 von 4** GitHub-IPs gesetzt (`185.199.108.153`) — **.109/.110/.111 fehlen** | 🔴 **das ist die Wurzel** |

**Warum das zusammenhängt:** GitHub stellt für den Apex nur dann ein eigenes Zertifikat aus, wenn **alle vier** A-Records gesetzt sind. Weil drei fehlen, bleibt das Apex-Zertifikat für immer im Fehlerzustand — und solange das so ist, lässt GitHub den „Enforce HTTPS"-Haken oft gar nicht zu. **Erst DNS reparieren, dann klicken.**

---

## 2. Teil A — Strato DNS (der wichtige Teil, ~3 Minuten)

Bei Strato im **DNS-Verwaltungsbereich von `multiplikatorenstelle.de`**:

**Es existiert schon 1 A-Record für den Apex (Host leer / `@`) auf `185.199.108.153`. Füge die fehlenden drei hinzu:**

| Typ | Host / Name | Wert (Ziel) |
|-----|-------------|-------------|
| A | `@` (bzw. leer) | `185.199.109.153` |
| A | `@` (bzw. leer) | `185.199.110.153` |
| A | `@` (bzw. leer) | `185.199.111.153` |

- **Nichts löschen**, nur die drei neuen A-Records **ergänzen**. Am Ende müssen vier A-Records für den Apex da sein (.108 / .109 / .110 / .111).
- Den bestehenden **`www`-CNAME auf `rubenwippermann.github.io` NICHT anfassen** — der ist korrekt und trägt die ganze Seite.
- Passt gut zum **Dienstag-Termin** (SPF/DMARC ist ohnehin dieselbe Strato-Oberfläche).

Danach braucht GitHub etwas Zeit, um das Apex-Zertifikat auszustellen — **meist 15–60 Min., maximal 24 h**. In der Zeit ist nichts kaputt, die Seite läuft normal weiter.

---

## 3. Teil B — GitHub „Enforce HTTPS" (der Klick, ~1 Minute)

**Erst machen, wenn Teil A ein paar Stunden her ist** (oder am nächsten Abend).

1. github.com → Repository **`rubenwippermann/…`** (das BWW-Repo) öffnen
2. Oben **Settings** (Zahnrad-Reiter)
3. Linke Leiste ganz unten: **Pages**
4. Abschnitt **„Custom domain"** — dort steht `www.multiplikatorenstelle.de`.
   → Wenn darunter grün **„DNS check successful"** steht: weiter zu Schritt 5.
5. Häkchen **„Enforce HTTPS"** setzen. **Fertig.**

Sobald der Haken sitzt, leitet GitHub jeden Klartext-Aufruf automatisch auf HTTPS um und setzt den HSTS-Header.

---

## 4. Was Besucher währenddessen sehen

- **Teil A (DNS):** nichts. Die Seite läuft über `www.` unverändert weiter — **keine Ausfallzeit**.
- **Teil B (Häkchen):** nichts Negatives. Ab dem Moment landen HTTP-Aufrufe auf HTTPS. **Keine Ausfallzeit.**
- **Einzige Ausnahme = Rückfallplan** (Punkt 6, nur falls nötig): Beim kurzen Entfernen+Neu-Setzen der Custom Domain ist die Domain für **wenige Minuten** unerreichbar (dann 404), bis sie wieder eingetragen ist. **Nur nutzen, wenn Teil A+B nicht greifen.**

---

## 5. Danach prüfen (kopieren & im Terminal ausführen)

```bash
# 1. Apex-Zertifikat — sollte jetzt CN=multiplikatorenstelle.de zeigen (NICHT *.github.io)
echo | openssl s_client -servername multiplikatorenstelle.de -connect multiplikatorenstelle.de:443 2>/dev/null | openssl x509 -noout -subject

# 2. HTTP → muss auf HTTPS umleiten (Location: https://…)
curl -sI http://www.multiplikatorenstelle.de | grep -iE "^(HTTP|Location)"

# 3. HSTS-Header muss jetzt da sein (Strict-Transport-Security: max-age=…)
curl -sI https://www.multiplikatorenstelle.de | grep -i strict-transport

# 4. Alle 4 Apex-IPs gesetzt?
dig +short multiplikatorenstelle.de A
```

**Erfolg =** (1) zeigt `multiplikatorenstelle.de`, (2) zeigt `Location: https://…`, (3) liefert eine `Strict-Transport-Security`-Zeile, (4) listet vier IPs.

---

## 6. Rückfallplan — falls das Zertifikat nach 24 h nicht kommt

1. **DNS gegenprüfen:** `dig +short multiplikatorenstelle.de A` muss **vier** IPs zeigen. Wenn nicht → bei Strato die fehlenden A-Records wirklich gespeichert? (Strato-Änderungen brauchen teils bis zu 24 h Propagierung.)
2. **Provisionierung neu anstoßen** (GitHub → Settings → Pages):
   - Im Feld **Custom domain** den Eintrag **leeren** → **Save**.
   - 1–2 Minuten warten, dann wieder `www.multiplikatorenstelle.de` eintragen → **Save**.
   - Das zwingt GitHub, das Zertifikat neu auszustellen. (In diesen ~2 Minuten ist die Domain kurz offline — s. Punkt 4.)
3. **Wenn „Enforce HTTPS" grau/nicht klickbar bleibt:** Das Apex-Zert ist noch nicht fertig — 24 h abwarten, dann erneut. Kein Grund zur Eile: `www.` läuft die ganze Zeit sicher über HTTPS.
4. **Notausgang, falls der Apex hartnäckig bleibt:** Der Apex ist reiner Komfort (Besucher, die „www" weglassen). Die komplette Seite, alle Links, Canonicals und der Traffic laufen über `www.` — **die Seite ist auch ohne Apex-Fix voll funktionsfähig und sicher.** Der Apex-Fix ist „schön zu haben", kein Blocker für den Betrieb.

---

*Reihenfolge in einem Satz: **Strato → 3 A-Records ergänzen (Dienstag), ein paar Stunden warten, dann bei GitHub den Enforce-HTTPS-Haken setzen.** Kein Schritt nimmt die Seite offline.*
