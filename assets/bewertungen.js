/* Stimmen unserer Teilnehmenden: freigegebene Bewertungen der BWW (org=bww).
   Platzierung: Block steht am Seitenende (unterhalb des ersten Bildschirms), bei 0 Bewertungen hidden = kein Rahmen; CLS mit 6 Mock-Bewertungen max. 0,018.   Ein Request je Seitenaufruf, Kurzzeit-Cache im sessionStorage, Block bleibt ohne Daten/bei Fehler verborgen.
   Kein JSON-LD / AggregateRating: Bewertungen gelten fuer die Firma, nicht fuer eine einzelne Kursseite (Selbstbewertungs-Richtlinie). */
(function () {
  var sec = document.getElementById('stimmen');
  if (!sec) return;
  var URL = 'https://software-wippermann.de/api/bewertungen?org=bww';
  var KEY = 'bww-bewertungen-v1', TTL = 10 * 60 * 1000, MAXLEN = 280, MAXN = 6;

  function fromCache() {
    try {
      var c = JSON.parse(sessionStorage.getItem(KEY) || 'null');
      if (c && c.t && Date.now() - c.t < TTL) return c.d;
    } catch (e) {}
    return null;
  }
  function toCache(d) { try { sessionStorage.setItem(KEY, JSON.stringify({ t: Date.now(), d: d })); } catch (e) {} }

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }
  function kuerzen(s) {
    s = String(s || '').replace(/\s+/g, ' ').trim();
    if (s.length <= MAXLEN) return s;
    var t = s.slice(0, MAXLEN), i = t.lastIndexOf(' ');
    return (i > 200 ? t.slice(0, i) : t) + ' …';
  }
  function render(d) {
    var list = d && Array.isArray(d.bewertungen) ? d.bewertungen.filter(function (b) { return b && String(b.text || '').trim(); }) : [];
    if (!list.length) return;
    var box = document.getElementById('stimmen-list');
    if (!box) return;
    list.slice(0, MAXN).forEach(function (b) {
      var fig = el('figure', 'stimme');
      var n = Math.round(Number(b.sterne));
      if (n >= 1 && n <= 5) {
        var st = el('div', 'stimme-sterne');
        var vis = el('span', null, '★★★★★'.slice(0, n) + '☆☆☆☆☆'.slice(0, 5 - n));
        vis.setAttribute('aria-hidden', 'true');
        st.appendChild(vis);
        st.appendChild(el('span', 'sr-only', n + ' von 5 Sternen'));
        fig.appendChild(st);
      }
      var bq = el('blockquote');
      bq.appendChild(el('p', null, kuerzen(b.text)));
      fig.appendChild(bq);
      fig.appendChild(el('figcaption', null, String(b.name || '').trim() || 'Teilnehmer:in'));
      box.appendChild(fig);
    });
    var a = d.aggregat, agg = document.getElementById('stimmen-agg');
    if (agg && a && a.anzahl >= 1 && typeof a.durchschnitt === 'number') {
      agg.textContent = 'Durchschnitt ' + String(a.durchschnitt).replace('.', ',') + ' von 5 Sternen aus ' + a.anzahl + (a.anzahl === 1 ? ' Bewertung' : ' Bewertungen') + '.';
    }
    sec.hidden = false;
  }

  var c = fromCache();
  if (c) { render(c); return; }
  var ctl = window.AbortController ? new AbortController() : null;
  var to = ctl ? setTimeout(function () { ctl.abort(); }, 6000) : null;
  fetch(URL, ctl ? { signal: ctl.signal } : {})
    .then(function (r) { if (!r.ok) throw 0; return r.json(); })
    .then(function (d) { toCache(d); render(d); })
    .catch(function () { /* Block bleibt verborgen */ })
    .then(function () { if (to) clearTimeout(to); });
})();
