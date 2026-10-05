/* Effekt-Ebene (FX) - BWW. Vanilla-JS, keine externen Skripte.
   Laeuft nur ohne prefers-reduced-motion. Ohne JS bleibt alles wie bisher. */
(function () {
  "use strict";
  var mm = window.matchMedia;
  if (!mm || mm("(prefers-reduced-motion: reduce)").matches) return;
  var fine = mm("(hover: hover) and (pointer: fine)").matches;
  var doc = document, root = doc.documentElement, ns = "http://www.w3.org/2000/svg";
  var raf = window.requestAnimationFrame.bind(window);
  var hasIO = "IntersectionObserver" in window;
  var deep = location.hash && location.hash.length > 1;

  function svgEl(name, attrs) {
    var e = doc.createElementNS(ns, name);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }

  /* Lese-Fortschritt */
  var bar = doc.createElement("div");
  bar.className = "fx-progress";
  bar.setAttribute("aria-hidden", "true");
  doc.body.appendChild(bar);
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    raf(function () {
      var max = root.scrollHeight - window.innerHeight;
      bar.style.transform = "scaleX(" + (max > 0 ? Math.min(1, window.scrollY / max) : 0) + ")";
      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
  onScroll();

  /* Hero (Startseite .apple-hero, Unterseiten .page-hero) */
  var hero = doc.querySelector(".hero.apple-hero, .page-hero");
  var h1 = hero && hero.querySelector("h1");
  if (hero && h1) {
    if (getComputedStyle(hero).position === "static") hero.style.position = "relative";
    hero.classList.add("fx-hero");

    var aur = doc.createElement("div");
    aur.className = "fx-aurora";
    aur.setAttribute("aria-hidden", "true");
    aur.innerHTML = '<i class="fx-blob b1"></i><i class="fx-blob b2"></i><i class="fx-blob b3"></i>';
    var spot = null;
    if (fine) {
      spot = doc.createElement("div");
      spot.className = "fx-spot";
      aur.appendChild(spot);
    }
    hero.insertBefore(aur, hero.firstChild);

    /* Buchstaben-Auftritt: Text-Knoten teilen, vorhandene Elemente (z. B. .hl-green) bleiben */
    if (!h1.querySelector(".fx-word")) {
      h1.setAttribute("aria-label", h1.textContent.replace(/\s+/g, " ").trim());
      var n = 0;
      (function walk(node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (c) {
          if (c.nodeType === 1) { walk(c); return; }
          if (c.nodeType !== 3) return;
          var frag = doc.createDocumentFragment();
          c.nodeValue.split(/(\s+)/).forEach(function (w) {
            if (!w) return;
            if (/^\s+$/.test(w)) { frag.appendChild(doc.createTextNode(" ")); return; }
            var word = doc.createElement("span");
            word.className = "fx-word";
            word.setAttribute("aria-hidden", "true");
            Array.prototype.forEach.call(w, function (ch) {
              var s = doc.createElement("span");
              s.className = "fx-ch";
              s.style.setProperty("--i", Math.min(n++, 40));
              s.textContent = ch;
              word.appendChild(s);
            });
            frag.appendChild(word);
          });
          node.replaceChild(frag, c);
        });
      })(h1);
    }

    /* Wachsende Ranke ueber der Ueberschrift (absolut, keine Layout-Aenderung) */
    var host = h1.parentElement;
    if (host && !host.querySelector(".fx-vine")) {
      if (getComputedStyle(host).position === "static") host.style.position = "relative";
      var v = svgEl("svg", { "class": "fx-vine", viewBox: "0 0 230 30", "aria-hidden": "true" });
      v.appendChild(svgEl("path", { "class": "stem", d: "M2 24 C40 24 48 8 88 14 S150 28 182 12 S216 6 226 4" }));
      [["M46 15 C42 8 48 3 55 4 C56 10 52 15 46 15Z", 0], ["M92 14 C90 20 96 25 103 24 C103 18 98 14 92 14Z", 1],
       ["M138 22 C134 15 140 10 147 11 C148 17 144 22 138 22Z", 2], ["M184 12 C183 18 189 22 196 21 C195 15 190 11 184 12Z", 3],
       ["M214 7 C211 1 217 -2 223 0 C224 5 220 8 214 7Z", 4]].forEach(function (l) {
        var p = svgEl("path", { "class": "leaf", d: l[0] });
        p.style.setProperty("--k", l[1]);
        v.appendChild(p);
      });
      host.insertBefore(v, host.firstChild);
    }

    if (spot) {
      hero.addEventListener("pointermove", function (e) {
        var r = hero.getBoundingClientRect();
        spot.style.setProperty("--sx", e.clientX - r.left + "px");
        spot.style.setProperty("--sy", e.clientY - r.top + "px");
        hero.classList.add("fx-hot");
      }, { passive: true });
      hero.addEventListener("pointerleave", function () { hero.classList.remove("fx-hot"); });
    }
  }

  /* Abschnittsköpfe: Trieb-Linie zeichnet sich */
  var heads = doc.querySelectorAll(".section-head");
  heads.forEach(function (h) {
    if (getComputedStyle(h).textAlign === "center") h.classList.add("fx-c");
  });
  function watch(list, cls, opts, delayStep, noFallback) {
    if (!list.length) return;
    if (!hasIO) { list.forEach(function (el) { el.classList.add(cls); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add(cls); io.unobserve(e.target); }
      });
    }, opts);
    list.forEach(function (el, i) {
      if (delayStep) el.style.setProperty("--d", (i % 4) * delayStep + "ms");
      io.observe(el);
    });
    if (!noFallback) setTimeout(function () { list.forEach(function (el) { el.classList.add(cls); }); }, 4000);
  }
  watch(Array.prototype.slice.call(heads), "is-in", { threshold: 0.3 });

  /* Wachstum: Symbole keimen */
  var sprouts = Array.prototype.slice.call(doc.querySelectorAll(".eco-big, .sustain-emoji"));
  sprouts.forEach(function (s) { s.classList.add("fx-sprout"); });
  watch(sprouts, "is-in", { threshold: 0.5 }, 140);

  /* Mini-Wald im Nachhaltigkeits-Hinweis */
  var eco = doc.querySelector(".eco-highlight");
  if (eco) {
    if (getComputedStyle(eco).position === "static") eco.style.position = "relative";
    var f = svgEl("svg", { "class": "fx-forest", viewBox: "0 0 104 40", "aria-hidden": "true" });
    [[10, 22, 18], [34, 30, 12], [58, 36, 8], [80, 26, 15], [96, 20, 20]].forEach(function (t, i) {
      var p = svgEl("path", { "class": "tree", d: "M" + t[0] + " 40 L" + (t[0] - 6) + " " + (40 - t[1] * 0.55) + " L" + (t[0] - 3) + " " + (40 - t[1] * 0.55) +
        " L" + (t[0] - 8) + " " + (40 - t[1] * 0.2) + " L" + (t[0] + 8) + " " + (40 - t[1] * 0.2) + " L" + (t[0] + 3) + " " + (40 - t[1] * 0.55) +
        " L" + (t[0] + 6) + " " + (40 - t[1] * 0.55) + " Z" });
      p.style.setProperty("--k", i);
      f.appendChild(p);
    });
    eco.appendChild(f);
    watch([f], "is-in", { threshold: 0.4 });
  }

  /* Karten: gestaffelter Einzug (nur was unter dem sichtbaren Bereich liegt, nie bei Deep-Links) */
  if (!deep) {
    var vh = window.innerHeight;
    var cards = Array.prototype.filter.call(doc.querySelectorAll("main .path-card, main .feature-card, main .sustain-card"), function (c) {
      return c.getBoundingClientRect().top > vh;
    });
    cards.forEach(function (c) { c.classList.add("fx-pre"); });
    watch(cards, "fx-in", { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }, 80, true);
    cards.forEach(function (c) {
      c.addEventListener("transitionend", function (ev) {
        if (ev.propertyName === "transform" && c.classList.contains("fx-in")) c.classList.remove("fx-pre", "fx-in");
      });
    });
  }

  if (!fine) return;

  /* 3D-Neigung + Lichtreflex (Delegation, nur Maus/Trackpad) */
  var SEL = ".path-card, .feature-card, .course-card, .sustain-card, .knowledge-card, .eco-highlight";
  var cur = null, pending = false, last = null;
  function leaveCard() { if (cur) { cur.classList.remove("fx-tilt-on"); cur = null; } }
  doc.addEventListener("pointermove", function (e) {
    var t = e.target.closest ? e.target.closest(SEL) : null;
    if (t && t.querySelector("input, select, textarea")) t = null;
    if (t !== cur) {
      leaveCard();
      if (t) {
        if (!t.classList.contains("fx-tilt")) {
          t.classList.add("fx-tilt");
          var g = doc.createElement("span");
          g.className = "fx-glare";
          g.setAttribute("aria-hidden", "true");
          t.appendChild(g);
        }
        cur = t;
      }
    }
    if (!cur) return;
    last = e;
    if (pending) return;
    pending = true;
    raf(function () {
      pending = false;
      if (!cur) return;
      var r = cur.getBoundingClientRect();
      var x = (last.clientX - r.left) / r.width, y = (last.clientY - r.top) / r.height;
      cur.style.setProperty("--ry", ((x - 0.5) * 7).toFixed(2) + "deg");
      cur.style.setProperty("--rx", ((0.5 - y) * 7).toFixed(2) + "deg");
      cur.style.setProperty("--gx", (x * 100).toFixed(1) + "%");
      cur.style.setProperty("--gy", (y * 100).toFixed(1) + "%");
      cur.classList.add("fx-tilt-on");
    });
  }, { passive: true });
  doc.addEventListener("pointerleave", leaveCard);

  /* Primaere Buttons: magnetisch */
  doc.querySelectorAll("main .btn.primary, .hero .btn.primary").forEach(function (b) {
    var pos = getComputedStyle(b).position;
    if (pos !== "static" && pos !== "relative") return;
    b.classList.add("fx-mag");
    b.addEventListener("pointermove", function (e) {
      var r = b.getBoundingClientRect();
      b.style.setProperty("--bx", ((e.clientX - r.left - r.width / 2) * 0.14).toFixed(1) + "px");
      b.style.setProperty("--by", ((e.clientY - r.top - r.height / 2) * 0.2).toFixed(1) + "px");
    }, { passive: true });
    b.addEventListener("pointerleave", function () {
      b.style.setProperty("--bx", "0px");
      b.style.setProperty("--by", "0px");
    });
  });
})();
