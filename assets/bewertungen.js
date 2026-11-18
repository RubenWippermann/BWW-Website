/* Stimmen unserer Teilnehmenden: freigegebene Bewertungen der BWW (org=bww).
   Platzierung: Block steht am Seitenende (unterhalb des ersten Bildschirms), bei 0 Bewertungen hidden = kein Rahmen; CLS mit 6 Mock-Bewertungen max. 0,018.   Ein Request je Seitenaufruf, kein Browser-Speicher (§ 25 TDDDG), Block bleibt ohne Daten/bei Fehler verborgen.
   Kein JSON-LD / AggregateRating: Bewertungen gelten fuer die Firma, nicht fuer eine einzelne Kursseite (Selbstbewertungs-Richtlinie).
   Keine Gesamtnote/Anzahl (Jurist 03.11.2026): nur ausgewaehlte Stimmen. */
(function () {
  /* Sterne als SVG (currentColor) statt Textzeichen: gleiche Bedeutung, auf allen Systemen gleiche Form */
  function sternSvg(n, gap) {
    n = Math.max(0, Math.min(5, parseInt(n, 10) || 0));
    var path = 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z';
    var out = '';
    for (var i = 0; i < 5; i++) {
      out += '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" style="display:inline-block;width:1em;height:1em;vertical-align:-.15em;margin-right:' + gap + '">' +
        '<path d="' + path + '" fill="' + (i < n ? 'currentColor' : 'none') + '" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>';
    }
    return out;
  }
  var sec = document.getElementById('stimmen');
  if (!sec) return;
  var URL = 'https://software-wippermann.de/api/bewertungen?org=bww';
  var MAXLEN = 280, MAXN = 6;

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
        var vis = el('span', null);
        vis.innerHTML = sternSvg(n, '.12em');
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
    sec.hidden = false;
  }

  var ctl = window.AbortController ? new AbortController() : null;
  var to = ctl ? setTimeout(function () { ctl.abort(); }, 6000) : null;
  fetch(URL, ctl ? { signal: ctl.signal } : {})
    .then(function (r) { if (!r.ok) throw 0; return r.json(); })
    .then(function (d) { render(d); })
    .catch(function () { /* Block bleibt verborgen */ })
    .then(function () { if (to) clearTimeout(to); });
})();
