/* BWW – Anbindung Kurs-/Buchungs-API (software-wippermann.de) */
(function () {
  var API = 'https://software-wippermann.de';
  var ORG = 'bww';
  var TEL = '+49 5527 748 7518';
  var MONTHS = ['Jan.', 'Feb.', 'März', 'Apr.', 'Mai', 'Juni', 'Juli', 'Aug.', 'Sep.', 'Okt.', 'Nov.', 'Dez.'];

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }
  function today() { var d = new Date(); function p(n){return (n<10?'0':'')+n;} return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()); }
  function fmtDate(d) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(d || '');
    if (!m) return esc(d);
    return parseInt(m[3], 10) + '. ' + MONTHS[parseInt(m[2], 10) - 1] + ' ' + m[1];
  }

  /* ---------- Live-Termine ---------- */
  function loadTermine() {
    var el = document.getElementById('live-termine');
    if (!el) return;
    var limitAttr = el.getAttribute('data-limit');
    // data-limit="all" (oder 0/leer) => alle Termine anzeigen; sonst auf die Zahl begrenzen
    var limit = (!limitAttr || limitAttr === 'all') ? 0 : parseInt(limitAttr, 10);
    var stadt = el.getAttribute('data-stadt') || '';
    // ab_datum=heute IMMER mitgeben — sonst liefert der Feed auch vergangene Termine
    var url = API + '/api/kurse?org=' + ORG + '&ab_datum=' + today() + (stadt ? '&stadt=' + encodeURIComponent(stadt) : '');
    fetch(url).then(function (r) { return r.json(); }).then(function (data) {
      var all = (data && data.kurse) ? data.kurse : [];
      var kurse = (limit > 0) ? all.slice(0, limit) : all;
      if (!kurse.length) {
        el.innerHTML = '<p class="termine-empty">Aktuell sind hier keine offenen Termine gelistet. Fragt gern einen Wunschtermin oder <a href="/inhouse-kurse/">Inhouse-Kurs</a> an.</p>';
        return;
      }
      el.innerHTML = kurse.map(function (k) {
        var tags = [k.stadt, k.kursart];
        if (k.fuehrerschein_geeignet) tags.push('Führerschein');
        if (k.bg_uk_abrechenbar) tags.push('BG/UK abrechenbar');
        // org=bww nur anhängen, falls die API es nicht schon liefert (sonst Dublette)
        var burl = k.buchungs_url || '';
        if (burl.indexOf('org=') === -1) burl += (burl.indexOf('?') > -1 ? '&' : '?') + 'org=' + ORG;
        var voll = !!k.ausgebucht;
        var zeit = k.uhrzeit ? esc(k.uhrzeit) + ' Uhr' : '';
        var preis = (k.preis != null && k.preis !== '') ? esc(k.preis) + ' €' : '';
        return '<a class="termin-row' + (voll ? ' is-full' : '') + '" href="' + esc(burl) + '" target="_blank" rel="noopener">' +
          '<span class="termin-date"><b>' + fmtDate(k.datum) + '</b>' + (zeit ? '<small>' + zeit + '</small>' : '') + '</span>' +
          '<span class="termin-info"><b>' + esc(k.titel) + '</b><small>' + tags.filter(Boolean).map(esc).join(' · ') + '</small></span>' +
          '<span class="termin-meta"><b>' + preis + '</b><small>' + (voll ? 'Ausgebucht' : 'Plätze frei') + '</small></span>' +
          '<span class="termin-cta">' + (voll ? 'Warteliste →' : 'Buchen →') + '</span></a>';
      }).join('');
    }).catch(function () {
      el.innerHTML = '<p class="termine-empty">Termine konnten gerade nicht geladen werden. Bitte später erneut versuchen oder <a href="/inhouse-kurse/">Wunschtermin anfragen →</a></p>';
    });
  }

  /* ---------- Formulare (Inhouse, Dozent, Kurs-Buchung) ---------- */
  function wireForms() {
    var forms = document.querySelectorAll('form[data-api]');
    Array.prototype.forEach.call(forms, function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var status = form.querySelector('.form-status');
        // Honeypot: ausgefülltes "website"-Feld => stiller Abbruch (Bot)
        var hp = form.querySelector('input[name="website"]');
        if (hp && hp.value) { if (status) status.textContent = 'Danke!'; return; }
        var payload = { org: ORG, website: '' };
        Array.prototype.forEach.call(form.querySelectorAll('[name]'), function (f) {
          var n = f.getAttribute('name');
          if (n === 'website' || n === 'consent') return; // Consent nur clientseitig erzwungen, nicht senden
          if (f.type === 'checkbox') {
            if (f.checked) { (payload[n] = payload[n] || []).push(f.value); }
          } else {
            payload[n] = f.value;
          }
        });
        var btn = form.querySelector('button[type="submit"]');
        var origTxt = btn ? btn.textContent : '';
        if (btn) { btn.disabled = true; btn.textContent = 'Wird gesendet …'; }
        if (status) { status.className = 'form-status'; status.textContent = ''; }
        var httpStatus = 0;
        fetch(API + '/api/' + form.getAttribute('data-api'), {
          method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
        }).then(function (r) { httpStatus = r.status; return r.json().catch(function () { return {}; }); }).then(function (res) {
          if (res && res.ok) {
            form.innerHTML = '<div class="form-success"><span class="form-success-ic">✓</span><h3>Danke – wir haben eure Anfrage erhalten!</h3><p>Wir melden uns zeitnah persönlich bei euch.' + (res.ticket_id ? ' Vorgangsnummer: <b>' + esc(res.ticket_id) + '</b>.' : '') + '</p></div>';
            return;
          }
          var msg;
          if (httpStatus === 429 || (res && res.error === 'too_many_requests')) {
            msg = 'Zu viele Anfragen in kurzer Zeit. Bitte in etwa einer Stunde erneut versuchen – oder ruft uns an: ' + TEL + '.';
          } else if (res && res.error === 'invalid_input') {
            msg = 'Bitte prüft eure Eingaben (Pflichtfelder, gültige E-Mail) und versucht es erneut.';
          } else {
            msg = 'Das hat leider nicht geklappt. Bitte versucht es erneut oder ruft uns an: ' + TEL + '.';
          }
          if (status) { status.className = 'form-status is-error'; status.textContent = msg; }
          if (btn) { btn.disabled = false; btn.textContent = origTxt; }
        }).catch(function () {
          if (status) { status.className = 'form-status is-error'; status.textContent = 'Verbindung fehlgeschlagen. Bitte später erneut versuchen oder anrufen: ' + TEL + '.'; }
          if (btn) { btn.disabled = false; btn.textContent = origTxt; }
        });
      });
    });
  }

  function init() { loadTermine(); wireForms(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
