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

  // Datum bzw. Datumsbereich (mehrtägige Kurse: datum_ende aus dem Feed)
  function fmtRange(k) {
    var a = /^(\d{4})-(\d{2})-(\d{2})$/.exec(k.datum || '');
    var b = /^(\d{4})-(\d{2})-(\d{2})$/.exec(k.datum_ende || '');
    if (!a) return esc(k.datum);
    if (!b || k.datum_ende === k.datum) return fmtDate(k.datum);
    var d1 = parseInt(a[3], 10), m1 = parseInt(a[2], 10), y1 = a[1];
    var d2 = parseInt(b[3], 10), m2 = parseInt(b[2], 10), y2 = b[1];
    if (y1 === y2 && m1 === m2) return d1 + '.–' + d2 + '. ' + MONTHS[m1 - 1] + ' ' + y1;
    if (y1 === y2) return d1 + '. ' + MONTHS[m1 - 1] + ' – ' + d2 + '. ' + MONTHS[m2 - 1] + ' ' + y1;
    return fmtDate(k.datum) + ' – ' + fmtDate(k.datum_ende);
  }

  /* ---------- Live-Termine ---------- */
  function cleanLabel(t) { return String(t == null ? '' : t).replace(/\s*\([^)]*\)/g, '').trim(); }

  function rowHTML(k) {
    var tags = [k.stadt];
    if (k.fuehrerschein_geeignet) tags.push('Führerschein');
    if (k.bg_uk_abrechenbar) tags.push('BG/UK abrechenbar');
    if (k.mehrtaegig) tags.push('mehrtägig');
    // org=bww nur anhängen, falls die API es nicht schon liefert (sonst Dublette)
    var burl = k.buchungs_url || '';
    if (burl.indexOf('org=') === -1) burl += (burl.indexOf('?') > -1 ? '&' : '?') + 'org=' + ORG;
    var voll = !!k.ausgebucht;
    var zeit = k.uhrzeit ? esc(k.uhrzeit) + ' Uhr' : '';
    var preis = (k.preis != null && k.preis !== '') ? esc(k.preis) + ' €' : '';
    var inner =
      '<span class="termin-date"><b>' + fmtRange(k) + '</b>' + (zeit ? '<small>' + zeit + '</small>' : '') + '</span>' +
      '<span class="termin-info"><b>' + esc(k.titel) + '</b><small>' + tags.filter(Boolean).map(esc).join(' · ') + '</small></span>' +
      '<span class="termin-meta"><b>' + preis + '</b><small>' + (voll ? 'Ausgebucht' : 'Plätze frei') + '</small></span>';
    if (voll) {
      // Ausgebucht: echte Warteliste (POST /api/warteliste), kein Link zur Buchung
      return '<div class="termin-row is-full">' + inner +
        '<button type="button" class="termin-cta waitlist-toggle" data-termin="' + esc(k.id) + '" data-titel="' + esc(k.titel) + '" data-datum="' + esc(fmtRange(k)) + (k.stadt ? ' · ' + esc(k.stadt) : '') + '">Warteliste →</button></div>';
    }
    return '<a class="termin-row" href="' + esc(burl) + '" target="_blank" rel="noopener">' + inner +
      '<span class="termin-cta">Buchen →</span></a>';
  }

  var EMPTY_MSG = '<p class="termine-empty">Aktuell sind hier keine offenen Termine gelistet. Fragt gern einen Wunschtermin oder <a href="/inhouse-kurse/">Inhouse-Kurs</a> an.</p>';

  function renderWithFilter(el, all) {
    // eindeutige Kursarten (Code -> lesbares Label aus dem Titel) und Städte
    var arten = {}, staedte = {};
    all.forEach(function (k) {
      if (k.kursart && !arten[k.kursart]) arten[k.kursart] = cleanLabel(k.titel);
      if (k.stadt) staedte[k.stadt] = 1;
    });
    var artKeys = Object.keys(arten).sort(function (a, b) { return arten[a].localeCompare(arten[b]); });
    var stadtKeys = Object.keys(staedte).sort();
    var showArt = artKeys.length > 1, showStadt = stadtKeys.length > 1;
    var bar = '';
    if (showArt || showStadt) {
      bar = '<div class="termine-filter">' +
        (showArt ? '<select class="tf-art" aria-label="Nach Kursart filtern"><option value="">Alle Kursarten</option>' + artKeys.map(function (c) { return '<option value="' + esc(c) + '">' + esc(arten[c]) + '</option>'; }).join('') + '</select>' : '') +
        (showStadt ? '<select class="tf-stadt" aria-label="Nach Ort filtern"><option value="">Alle Orte</option>' + stadtKeys.map(function (s) { return '<option value="' + esc(s) + '">' + esc(s) + '</option>'; }).join('') + '</select>' : '') +
        '<span class="tf-count" aria-live="polite"></span></div>';
    }
    el.innerHTML = bar + '<div class="termine-rows"></div>';
    var artSel = el.querySelector('.tf-art'), stadtSel = el.querySelector('.tf-stadt');
    var rowsEl = el.querySelector('.termine-rows'), countEl = el.querySelector('.tf-count');
    function apply() {
      var a = artSel ? artSel.value : '', s = stadtSel ? stadtSel.value : '';
      var f = all.filter(function (k) { return (!a || k.kursart === a) && (!s || k.stadt === s); });
      rowsEl.innerHTML = f.length ? f.map(rowHTML).join('') : '<p class="termine-empty">Für diese Auswahl sind aktuell keine Termine frei. <a href="/inhouse-kurse/">Wunschtermin anfragen →</a></p>';
      if (countEl) countEl.textContent = f.length + (f.length === 1 ? ' Termin' : ' Termine');
    }
    if (artSel) artSel.addEventListener('change', apply);
    if (stadtSel) stadtSel.addEventListener('change', apply);
    apply();
  }

  function loadTermine() {
    var el = document.getElementById('live-termine');
    if (!el) return;
    var limitAttr = el.getAttribute('data-limit');
    // data-limit="all" (oder 0/leer) => alle Termine + Filter; sonst begrenzte Teaser-Liste
    var limit = (!limitAttr || limitAttr === 'all') ? 0 : parseInt(limitAttr, 10);
    var stadt = el.getAttribute('data-stadt') || '';
    // data-art="EHA" (oder mehrere per Komma) => nur diese Kursformate, ohne Filter-Dropdown (dedizierte Kursseite)
    var art = (el.getAttribute('data-art') || '').split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    // ab_datum=heute IMMER mitgeben — sonst liefert der Feed auch vergangene Termine
    var url = API + '/api/kurse?org=' + ORG + '&ab_datum=' + today() + (stadt ? '&stadt=' + encodeURIComponent(stadt) : '');
    fetch(url).then(function (r) { return r.json(); }).then(function (data) {
      var all = (data && data.kurse) ? data.kurse : [];
      if (art.length) {
        all = all.filter(function (k) { return art.indexOf(String(k.kursart || '')) !== -1; });
        if (!all.length) { el.innerHTML = '<p class="termine-empty">Für dieses Format sind aktuell keine offenen Termine gelistet. Als Inhouse-Kurs jederzeit buchbar — <a href="#anfrage">Wunschtermin anfragen →</a></p>'; return; }
        el.innerHTML = (limit > 0 ? all.slice(0, limit) : all).map(rowHTML).join('');
        return;
      }
      if (!all.length) { el.innerHTML = EMPTY_MSG; return; }
      if (limit > 0) { el.innerHTML = all.slice(0, limit).map(rowHTML).join(''); return; }
      renderWithFilter(el, all);
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

  /* ---------- Warteliste (ausgebuchte Termine -> POST /api/warteliste) ---------- */
  function ensureWaitlistModal() {
    if (document.getElementById('wlModal')) return;
    var o = document.createElement('div');
    o.id = 'wlModal'; o.className = 'wl-overlay'; o.hidden = true;
    o.innerHTML =
      '<div class="wl-box" role="dialog" aria-modal="true" aria-labelledby="wlTitle">' +
        '<button type="button" class="wl-close" aria-label="Schließen">×</button>' +
        '<h3 id="wlTitle">Auf die Warteliste</h3>' +
        '<p class="wl-course"></p>' +
        '<form class="wl-form" novalidate>' +
          '<label for="wl-name">Name *</label><input id="wl-name" name="name" required>' +
          '<label for="wl-mail">E-Mail *</label><input id="wl-mail" name="email" type="email" required>' +
          '<label class="wl-consent"><input type="checkbox" name="consent" required><span>Ich habe die <a href="/datenschutz/" target="_blank" rel="noopener">Datenschutzerklärung</a> gelesen und stimme der Verarbeitung meiner Daten zu.</span></label>' +
          '<div class="hp"><label>Bitte frei lassen<input name="website" tabindex="-1" autocomplete="off"></label></div>' +
          '<button type="submit" class="btn primary">Eintragen</button>' +
          '<p class="wl-status" role="status"></p>' +
        '</form>' +
      '</div>';
    document.body.appendChild(o);
    function close() { o.hidden = true; document.body.classList.remove('wl-open'); }
    o.querySelector('.wl-close').addEventListener('click', close);
    o.addEventListener('click', function (e) { if (e.target === o) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !o.hidden) close(); });
    o.querySelector('.wl-form').addEventListener('submit', function (e) {
      e.preventDefault();
      var form = e.target, status = form.querySelector('.wl-status');
      var hp = form.querySelector('input[name="website"]');
      if (hp && hp.value) { close(); return; }
      var name = form.querySelector('input[name="name"]').value.trim();
      var email = form.querySelector('input[name="email"]').value.trim();
      var consent = form.querySelector('input[name="consent"]').checked;
      if (!name || !email || !consent) { status.className = 'wl-status is-error'; status.textContent = 'Bitte Name, E-Mail und Einwilligung ausfüllen.'; return; }
      var btn = form.querySelector('button[type="submit"]'); var orig = btn.textContent;
      btn.disabled = true; btn.textContent = 'Wird gesendet …'; status.textContent = ''; status.className = 'wl-status';
      var httpStatus = 0;
      fetch(API + '/api/warteliste', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ org: ORG, termin: o.dataset.termin || '', name: name, email: email, website: '' })
      }).then(function (r) { httpStatus = r.status; return r.json().catch(function () { return {}; }); }).then(function (res) {
        if (res && res.ok) {
          form.innerHTML = '<div class="form-success"><span class="form-success-ic">✓</span><h3>Du stehst auf der Warteliste!</h3><p>Wir melden uns, sobald ein Platz frei wird.' + (res.ticket_id ? ' Vorgang: <b>' + esc(res.ticket_id) + '</b>.' : '') + '</p></div>';
          return;
        }
        var msg = (httpStatus === 429 || (res && res.error === 'too_many_requests'))
          ? 'Zu viele Anfragen. Bitte später erneut versuchen oder anrufen: ' + TEL + '.'
          : 'Das hat nicht geklappt. Bitte erneut versuchen oder anrufen: ' + TEL + '.';
        status.className = 'wl-status is-error'; status.textContent = msg;
        btn.disabled = false; btn.textContent = orig;
      }).catch(function () {
        status.className = 'wl-status is-error'; status.textContent = 'Verbindung fehlgeschlagen. Bitte später erneut versuchen oder anrufen: ' + TEL + '.';
        btn.disabled = false; btn.textContent = orig;
      });
    });
  }
  function wireWaitlist() {
    document.addEventListener('click', function (e) {
      var t = e.target.closest ? e.target.closest('.waitlist-toggle') : null;
      if (!t) return;
      e.preventDefault();
      ensureWaitlistModal();
      var o = document.getElementById('wlModal');
      o.dataset.termin = t.getAttribute('data-termin') || '';
      o.querySelector('.wl-course').textContent = (t.getAttribute('data-titel') || '') + (t.getAttribute('data-datum') ? ' – ' + t.getAttribute('data-datum') : '');
      // Formular zurücksetzen (falls zuvor abgeschickt)
      var f = o.querySelector('.wl-form'); if (f && f.querySelector('.form-success')) { o.remove(); ensureWaitlistModal(); o = document.getElementById('wlModal'); o.dataset.termin = t.getAttribute('data-termin') || ''; o.querySelector('.wl-course').textContent = (t.getAttribute('data-titel') || '') + (t.getAttribute('data-datum') ? ' – ' + t.getAttribute('data-datum') : ''); }
      o.hidden = false; document.body.classList.add('wl-open');
      var ni = o.querySelector('input[name="name"]'); if (ni) ni.focus();
    });
  }

  function init() { loadTermine(); wireForms(); wireWaitlist(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
