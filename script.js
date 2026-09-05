/* Everest Heat Treaters — one IIFE, every feature existence-guarded so the
   same file loads safely on every page. */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) {
    return Array.prototype.slice.call((r || document).querySelectorAll(s));
  };

  /* ---------------------------------------------------- sticky header --- */
  var hdr = $("[data-header]");
  if (hdr) {
    var ticking = false;
    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        hdr.classList.toggle("is-stuck", window.scrollY > 60);
        ticking = false;
      });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---------------------------------------------------- mobile drawer --- */
  var drawer = $("[data-drawer]");
  var burger = $("[data-burger]");
  if (drawer && burger) {
    var setDrawer = function (open) {
      drawer.classList.toggle("is-open", open);
      burger.setAttribute("aria-expanded", String(open));
      document.documentElement.style.overflow = open ? "hidden" : "";
      if (open) { var f = $("a", drawer); if (f) f.focus(); }
      else burger.focus();
    };
    burger.addEventListener("click", function () {
      setDrawer(!drawer.classList.contains("is-open"));
    });
    var x = $("[data-drawer-close]", drawer);
    if (x) x.addEventListener("click", function () { setDrawer(false); });
    $$("a", drawer).forEach(function (a) {
      a.addEventListener("click", function () { setDrawer(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drawer.classList.contains("is-open")) setDrawer(false);
    });
  }

  /* --------------------------------------------------------- count up --- */
  function countUp(el) {
    var raw = el.getAttribute("data-count");
    var target = parseFloat(raw);
    // Some figures carry a prefix (±5) and are not animatable. Leave them.
    if (isNaN(target) || String(raw).trim() !== String(target)) return;
    var decimals = (raw.split(".")[1] || "").length;
    if (reduced) { el.textContent = target.toFixed(decimals); return; }
    var start = null, dur = 1300;
    var step = function (now) {
      if (start === null) start = now;
      var p = Math.min((now - start) / dur, 1);
      el.textContent = (target * (1 - Math.pow(1 - p, 3))).toFixed(decimals);
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = target.toFixed(decimals);
    };
    requestAnimationFrame(step);
    // rAF is throttled in a hidden tab; land on the real number regardless.
    setTimeout(function () { el.textContent = target.toFixed(decimals); }, dur + 600);
  }

  /* ---------------------------------------------------------- reveals --- */
  var reveals = $$("[data-reveal]");
  if (reveals.length) {
    var activate = function (el) {
      if (el.classList.contains("is-in")) return;
      el.classList.add("is-in");
      if (el.hasAttribute("data-count")) countUp(el);
      $$("[data-count]", el).forEach(countUp);
    };
    if (reduced || !("IntersectionObserver" in window)) {
      reveals.forEach(activate);
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { activate(en.target); io.unobserve(en.target); }
        });
      }, { threshold: 0.1, rootMargin: "0px 0px -8% 0px" });
      reveals.forEach(function (el) { io.observe(el); });

      /* Safety net. IntersectionObserver does not fire in a hidden or
         non-composited document, and a section stuck at opacity:0 in front of
         a client is the worst failure this page can have. */
      var sweep = function () {
        var h = window.innerHeight || document.documentElement.clientHeight;
        reveals.forEach(function (el) {
          if (el.classList.contains("is-in")) return;
          // Anything at or above the fold, INCLUDING content already scrolled
          // past — an anchor jump or restored scroll position leaves earlier
          // sections behind the viewport and would strand them invisible.
          if (el.getBoundingClientRect().top < h * 0.96) activate(el);
        });
      };
      ["load", "scroll", "resize", "pageshow"].forEach(function (ev) {
        window.addEventListener(ev, sweep, { passive: true });
      });
      setTimeout(sweep, 350);
      sweep();
    }
  }

  /* ================================================ TEMPERATURE SCALE === */
  /* The colour of steel is not decoration here — below roughly 400 C what
     you see is the interference colour of the oxide film, and above it the
     metal is incandescent. Both tables come from content.py. */
  var temp = $("[data-temp]");
  if (temp) {
    var data;
    try { data = JSON.parse(temp.getAttribute("data-scale")); } catch (e) { data = null; }

    if (data) {
      var input = $("[data-temp-input]", temp);
      var bar = $("[data-temp-bar]", temp);
      var reflect = $("[data-temp-reflect]", temp);
      var outC = $("[data-temp-c]", temp);
      var outColour = $("[data-temp-colour]", temp);
      var outBand = $("[data-temp-band]", temp);
      var outDesc = $("[data-temp-desc]", temp);

      var GLOW_START = 400;   // oxide colours give way to visible glow
      var GLOW_FULL = 480;

      function hex2rgb(h) {
        h = h.replace("#", "");
        return [parseInt(h.slice(0, 2), 16),
                parseInt(h.slice(2, 4), 16),
                parseInt(h.slice(4, 6), 16)];
      }
      function mix(a, b, t) {
        return [Math.round(a[0] + (b[0] - a[0]) * t),
                Math.round(a[1] + (b[1] - a[1]) * t),
                Math.round(a[2] + (b[2] - a[2]) * t)];
      }
      function rgbCss(c) { return "rgb(" + c[0] + "," + c[1] + "," + c[2] + ")"; }

      // Walk a [temp, hex, name] table and interpolate between its stops.
      function sample(table, t) {
        if (t <= table[0][0]) return { rgb: hex2rgb(table[0][1]), name: table[0][2] };
        var last = table[table.length - 1];
        if (t >= last[0]) return { rgb: hex2rgb(last[1]), name: last[2] };
        for (var i = 0; i < table.length - 1; i++) {
          var a = table[i], b = table[i + 1];
          if (t >= a[0] && t <= b[0]) {
            var f = (t - a[0]) / (b[0] - a[0]);
            return {
              rgb: mix(hex2rgb(a[1]), hex2rgb(b[1]), f),
              // name snaps to the nearer stop rather than inventing a blend
              name: f < 0.5 ? a[2] : b[2]
            };
          }
        }
        return { rgb: hex2rgb(last[1]), name: last[2] };
      }

      function bandFor(t) {
        for (var i = 0; i < data.bands.length; i++) {
          if (t >= data.bands[i][0] && t < data.bands[i][1]) return data.bands[i];
        }
        return data.bands[data.bands.length - 1];
      }

      function render(t) {
        var ox = sample(data.temper, t);
        var gl = sample(data.glow, t);
        var rgb, name;

        if (t < GLOW_START) {
          rgb = ox.rgb; name = ox.name;
        } else if (t >= GLOW_FULL) {
          rgb = gl.rgb; name = gl.name;
        } else {
          // crossing from oxide film into first visible red
          var f = (t - GLOW_START) / (GLOW_FULL - GLOW_START);
          rgb = mix(ox.rgb, gl.rgb, f);
          name = f < 0.5 ? ox.name : gl.name;
        }

        var css = rgbCss(rgb);
        bar.style.setProperty("--c", css);
        if (reflect) reflect.style.setProperty("--c", css);

        // Glow only once the metal is actually incandescent.
        var heat = Math.max(0, Math.min(1, (t - GLOW_FULL) / (data.max - GLOW_FULL)));
        bar.style.setProperty("--gsize", (heat * heat * 130).toFixed(0) + "px");
        bar.style.setProperty("--gspread", (heat * 12).toFixed(0) + "px");
        if (reflect) reflect.style.opacity = (0.10 + heat * 0.34).toFixed(2);

        var b = bandFor(t);
        if (outC) outC.textContent = t;
        if (outColour) outColour.textContent = name;
        if (outBand) outBand.innerHTML = b[2];
        if (outDesc) outDesc.innerHTML = b[3];
      }

      if (input) {
        input.addEventListener("input", function () { render(+input.value); });
        render(+input.value);

        // Nudge it once on first view so people notice it moves.
        if (!reduced && "IntersectionObserver" in window) {
          var seen = false;
          var tio = new IntersectionObserver(function (es) {
            es.forEach(function (en) {
              if (!en.isIntersecting || seen) return;
              seen = true;
              tio.disconnect();
              var from = +input.value, to = 1180, t0 = null;
              var run = function (now) {
                if (t0 === null) t0 = now;
                var p = Math.min((now - t0) / 1500, 1);
                var e = 1 - Math.pow(1 - p, 3);
                input.value = Math.round(from + (to - from) * e);
                render(+input.value);
                if (p < 1) requestAnimationFrame(run);
              };
              requestAnimationFrame(run);
            });
          }, { threshold: 0.45 });
          tio.observe(temp);
        }
      }
    }
  }

  /* ------------------------------------------------- materials filter --- */
  var matBody = $("[data-mat-body]");
  var matSearch = $("[data-mat-search]");
  if (matBody && matSearch) {
    var rows = $$("tr", matBody);
    var count = $("[data-mat-count]");
    var empty = $("[data-mat-empty]");
    var say = function (n) {
      if (count) count.textContent = n + " of " + rows.length + " grades";
      if (empty) empty.hidden = n !== 0;
    };
    var filter = function () {
      var q = matSearch.value.trim().toLowerCase();
      var n = 0;
      rows.forEach(function (tr) {
        var hit = !q || tr.textContent.toLowerCase().indexOf(q) > -1;
        tr.hidden = !hit;
        if (hit) n++;
      });
      say(n);
    };
    matSearch.addEventListener("input", filter);
    say(rows.length);
  }

  /* ---------------------------------------------- enquiry -> WhatsApp --- */
  /* A static site has no backend. Rather than a form that silently does
     nothing, hand the details to WhatsApp already filled in. */
  var form = $("[data-enquiry]");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var d = new FormData(form);
      var labels = {
        name: "Name", company: "Company", phone: "Phone", email: "Email",
        grade: "Material", process: "Treatment", qty: "Quantity",
        hardness: "Hardness required", message: "Details"
      };
      var lines = ["Heat treatment enquiry", ""];
      Object.keys(labels).forEach(function (k) {
        var v = (d.get(k) || "").toString().trim();
        if (v) lines.push(labels[k] + ": " + v);
      });
      window.open("https://wa.me/" + form.getAttribute("data-wa") +
        "?text=" + encodeURIComponent(lines.join("\n")), "_blank", "noopener");
    });
  }
})();
