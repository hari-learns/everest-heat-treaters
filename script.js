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
    var lastY = window.scrollY;
    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.scrollY;
        hdr.classList.toggle("is-stuck", y > 60);
        // Reading down the page, the page links fold away into the Contact
        // button; any move back up unfolds them. The bar itself stays.
        var dr = $("[data-drawer]");
        var open = dr && dr.classList.contains("is-open");
        if (y < 120 || open) hdr.classList.remove("is-tucked");
        else if (y > lastY + 6) hdr.classList.add("is-tucked");
        else if (y < lastY - 6) hdr.classList.remove("is-tucked");
        if (Math.abs(y - lastY) > 6 || y < 120) lastY = y;
        ticking = false;
      });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    hdr.addEventListener("focusin", function () { hdr.classList.remove("is-tucked"); });
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
  /* ------------------------------------------- text that runs on heat --- */
  /* Two things paint themselves from the incandescent scale: the word in the
     headline, and the company name in the header. They run half a cycle
     apart, so when one is at red heat the other is at orange and the pair
     never sit on the same colour. */
  (function () {
    var targets = [];
    var word = $("[data-heat-word]");
    var heroSrc = $(".hero__title[data-heat-scale]");
    if (word && heroSrc) {
      targets.push({ el: word, src: heroSrc, phase: 0,
                     label: $("[data-heat-temp]", word) });
    }
    $$("[data-heat-brand]").forEach(function (el) {
      targets.push({ el: el, src: el, phase: 0.5, label: null });
    });
    if (!targets.length) return;

    var hexToRgb = function (h) {
      h = h.replace("#", "");
      return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16),
              parseInt(h.slice(4, 6), 16)];
    };
    var sampleStops = function (stops, t) {
      if (t <= stops[0][0]) return hexToRgb(stops[0][1]);
      var last = stops[stops.length - 1];
      if (t >= last[0]) return hexToRgb(last[1]);
      for (var i = 0; i < stops.length - 1; i++) {
        var a = stops[i], b = stops[i + 1];
        if (t >= a[0] && t <= b[0]) {
          var f = (t - a[0]) / (b[0] - a[0]);
          var ca = hexToRgb(a[1]), cb = hexToRgb(b[1]);
          return [Math.round(ca[0] + (cb[0] - ca[0]) * f),
                  Math.round(ca[1] + (cb[1] - ca[1]) * f),
                  Math.round(ca[2] + (cb[2] - ca[2]) * f)];
        }
      }
      return hexToRgb(last[1]);
    };

    var live = [];
    targets.forEach(function (t) {
      var stops = null;
      try { stops = JSON.parse(t.src.getAttribute("data-heat-scale")); }
      catch (e) { return; }
      if (!stops || stops.length < 2) return;
      t.stops = stops;
      t.lo = +t.src.getAttribute("data-heat-lo");
      t.hi = +t.src.getAttribute("data-heat-hi");
      t.paint = function (temp) {
        var c = sampleStops(t.stops, temp);
        t.el.style.color = "rgb(" + c[0] + "," + c[1] + "," + c[2] + ")";
        if (t.label) t.label.textContent = Math.round(temp) + "\u00B0C";
      };
      live.push(t);
    });
    if (!live.length) return;

    if (reduced) {
      live.forEach(function (t) { t.paint((t.lo + t.hi) / 2); });
      return;
    }

    var CYCLE = 9000;                 // one climb and fall
    var origin = 0, raf = 0;
    var tick = function (now) {
      if (!origin) origin = now;
      live.forEach(function (t) {
        var p = ((now - origin) / CYCLE + t.phase) % 1;
        var e = (1 - Math.cos(p * 2 * Math.PI)) / 2;
        t.paint(t.lo + (t.hi - t.lo) * e);
      });
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) {
        if (raf) { cancelAnimationFrame(raf); raf = 0; }
      } else if (!raf) { origin = 0; raf = requestAnimationFrame(tick); }
    });
  })();

  /* -------------------------------------------------------- validation --- */
  /* Phone numbers and emails are checked before anything is sent. Indian
     numbers may be written as 10 digits, +91 and 10 digits, or 0 and 10
     digits for a landline with its STD code; anything starting + is taken
     as international and needs 8 to 15 digits. Only digits, spaces, + and -
     can be typed into a phone field at all. */
  var phoneOk = function (v) {
    v = v.trim();
    if (!/^\+?[\d\s-]+$/.test(v)) return false;
    var d = v.replace(/\D/g, "");
    if (v.charAt(0) === "+" && d.slice(0, 2) !== "91") return d.length >= 8 && d.length <= 15;
    if (d.length === 12 && d.slice(0, 2) === "91") d = d.slice(2);
    else if (d.length === 11 && d.charAt(0) === "0") d = d.slice(1);
    return d.length === 10 && /^[2-9]/.test(d) && !/^(\d)\1{9}$/.test(d);
  };
  var emailOk = function (v) {
    return /^[^\s@]+@[^\s@.]+(\.[^\s@.]+)+$/.test(v.trim()) && !/\.\./.test(v);
  };
  var nameOk = function (v) { return (v.match(/[A-Za-z\u0B80-\u0BFF]/g) || []).length >= 2; };
  var RULES = {
    phone: [phoneOk, "Enter a valid phone number, e.g. 98400 12345 or +91 98400 12345."],
    email: [emailOk, "Enter a valid email address, e.g. name@company.com."],
    name: [nameOk, "Enter your name."]
  };
  var errFor = function (input) {
    var host = input.closest("label") || input.parentNode;
    var e = host.querySelector(".field__err");
    if (!e) {
      e = document.createElement("span");
      e.className = "field__err";
      e.id = "err-" + Math.random().toString(36).slice(2);
      e.setAttribute("role", "alert");
      host.appendChild(e);
      input.setAttribute("aria-describedby", e.id);
    }
    return e;
  };
  // true when the field is fine; shows or clears the message either way
  var check = function (input, loud) {
    var rule = RULES[input.name];
    var v = input.value;
    var bad = "";
    if (!v.trim()) { if (input.required) bad = rule ? rule[1] : "This field is required."; }
    else if (rule && !rule[0](v)) bad = rule[1];
    input.setCustomValidity(bad);
    input.classList.toggle("is-bad", !!bad && loud);
    input.setAttribute("aria-invalid", bad && loud ? "true" : "false");
    var e = errFor(input);
    e.textContent = loud ? bad : "";
    e.hidden = !(bad && loud);
    return !bad;
  };
  var guard = function (root) {
    $$('input[name="phone"],input[name="email"],input[name="name"]', root).forEach(function (input) {
      if (input.name === "phone") {
        input.addEventListener("input", function () {
          var c = input.value.replace(/[^\d\s+-]/g, "").replace(/(?!^)\+/g, "");
          if (c !== input.value) input.value = c;
        });
      }
      input.addEventListener("blur", function () { if (input.value) check(input, true); });
      input.addEventListener("input", function () {
        if (input.classList.contains("is-bad")) check(input, true);
      });
    });
  };
  // checks every rule-bound field; focuses the first that fails
  var validate = function (root) {
    var first = null;
    $$('input[name="phone"],input[name="email"],input[name="name"]', root).forEach(function (input) {
      if (!check(input, true) && !first) first = input;
    });
    if (first) first.focus();
    return !first;
  };

  /* --------------------------------------------------------- delivery --- */
  /* One place that knows how an enquiry leaves the site: an email through
     FormSubmit to the company inbox, copied to the metallurgist. Resolves
     true when FormSubmit confirms it, false otherwise, so the page can say
     which. */
  var LABELS = {
    name: "Name", company: "Company", phone: "Phone", email: "Email",
    grade: "Material grade", process: "Treatment", weight: "Weight",
    size: "Size", hardness: "Hardness required", message: "Details",
    page: "Sent from"
  };
  function deliver(payload, opts) {
    opts = opts || {};
    if (!opts.endpoint) return Promise.resolve(false);
    var fd = new FormData();
    var who = payload.name || payload.phone || "website visitor";
    fd.append("_subject", (payload.grade ? payload.grade + " enquiry" :
      "Heat treatment enquiry") + " from " + who);
    fd.append("_template", "table");
    fd.append("_captcha", "false");
    if (opts.cc) fd.append("_cc", opts.cc);
    if (payload.email) fd.append("_replyto", payload.email);
    Object.keys(LABELS).forEach(function (k) {
      var v = (payload[k] || "").toString().trim();
      if (v) fd.append(LABELS[k], v);
    });
    if (opts.file) fd.append("attachment", opts.file, opts.file.name);
    return fetch(opts.endpoint, {
      method: "POST", headers: { "Accept": "application/json" }, body: fd
    }).then(function (r) { return r.json(); })
      .then(function (j) { return j && (j.success === true || j.success === "true"); })
      .catch(function () { return false; });
  }

  /* ------------------------------------------------ reviews, one up --- */
  (function () {
    var box = $("[data-quotes]");
    if (!box) return;
    var slides = $$(".quote", box);
    var dots = $$("[data-quote-dot]", box);
    if (slides.length < 2) { box.setAttribute("data-single", ""); return; }

    var at = 0, timer = 0;
    var show = function (i) {
      at = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) {
        s.classList.toggle("is-on", n === at);
        s.setAttribute("aria-hidden", n === at ? "false" : "true");
      });
      dots.forEach(function (d, n) {
        d.classList.toggle("is-on", n === at);
        d.setAttribute("aria-selected", n === at ? "true" : "false");
      });
    };
    var stop = function () { if (timer) { clearInterval(timer); timer = 0; } };
    var play = function () {
      if (reduced || timer) return;
      timer = setInterval(function () { show(at + 1); }, 5000);
    };

    dots.forEach(function (d, n) {
      d.addEventListener("click", function () { stop(); show(n); play(); });
    });
    // hold still while someone is reading or tabbing through
    box.addEventListener("mouseenter", stop);
    box.addEventListener("mouseleave", play);
    box.addEventListener("focusin", stop);
    box.addEventListener("focusout", play);
    document.addEventListener("visibilitychange", function () {
      document.hidden ? stop() : play();
    });

    show(0);
    play();
  })();

  /* --------------------------------------------- pick a grade, enquire --- */
  /* The enquiry opens in the table, directly under the grade that was
     clicked. A button at the foot of a 26-row table is a button nobody sees.
     One tap asks for a number and nothing else, because a phone number given
     in two seconds beats a nine-field form nobody fills in. */
  (function () {
    var body = $("[data-mat-body]");
    if (!body) return;
    var table = body.closest("table");
    // read at send time, not at load, so the endpoint can be swapped in
    // without caring when the script happened to run
    var endpoint = function () { return table.getAttribute("data-endpoint") || ""; };
    var cc = function () { return table.getAttribute("data-cc") || ""; };
    var COLS = $$("thead th", table).length || 5;
    var open = null;

    var close = function () {
      if (open) { open.remove(); open = null; }
      $$("tr", body).forEach(function (r) { r.classList.remove("is-picked"); });
      table.classList.remove("is-picking");
    };

    var rowFor = function (grade) {
      var tr = document.createElement("tr");
      tr.className = "mat__ask";
      tr.innerHTML =
        '<td colspan="' + COLS + '">' +
          '<div class="ask">' +
            '<p class="ask__lead">Enquire about <b></b></p>' +
            '<form class="ask__form" data-ask-form novalidate>' +
              '<input type="tel" name="phone" required autocomplete="tel" ' +
                'inputmode="tel" maxlength="20" placeholder="Your phone number" ' +
                'aria-label="Your phone number">' +
              '<button class="btn btn--sm" type="submit">Enquire</button>' +
              '<button class="btn btn--ghost btn--sm" type="button" data-ask-cancel>Cancel</button>' +
            '</form>' +
            '<div class="thanks thanks--mini ask__done" data-ask-done hidden tabindex="-1">' +
              '<svg class="thanks__tick" viewBox="0 0 96 96" aria-hidden="true">' +
                '<circle class="thanks__glow" cx="48" cy="48" r="40"/>' +
                '<circle class="thanks__ring" cx="48" cy="48" r="40" pathLength="1"/>' +
                '<path class="thanks__check" d="M30 49 L43 62 L67 36" pathLength="1"/>' +
              '</svg>' +
              '<div><p class="thanks__h">Thanks for reaching out</p>' +
              '<p class="thanks__p">We have your number and will call you about <b></b> soon.</p></div>' +
            '</div>' +
          '</div>' +
        '</td>';
      $("b", $(".ask__lead", tr)).textContent = grade;
      $("b", $(".thanks__p", tr)).textContent = grade;
      return tr;
    };

    var pick = function (row) {
      var grade = row.getAttribute("data-grade") || "";
      var wasOpen = open && open.previousElementSibling === row;
      close();
      if (wasOpen) return;
      row.classList.add("is-picked");
      table.classList.add("is-picking");
      open = rowFor(grade);
      row.after(open);

      var form = $("[data-ask-form]", open);
      var done = $("[data-ask-done]", open);
      // one step: the phone field and Enquire are there as soon as the row
      // opens. Focus only with a mouse, so a phone keyboard does not jump up.
      guard(form);
      if (window.matchMedia("(hover:hover)").matches) $("input", form).focus();
      $("[data-ask-cancel]", form).addEventListener("click", close);
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (!validate(form)) return;
        var btn = $('button[type="submit"]', form);
        btn.disabled = true;
        btn.textContent = "Sending\u2026";
        deliver({
          grade: grade,
          phone: $("input", form).value.trim(),
          page: location.href
        }, { endpoint: endpoint(), cc: cc() }).then(function (ok) {
          if (!ok) {
            // keep the form, say what to do instead
            btn.disabled = false;
            btn.textContent = "Enquire";
            var e = errFor($("input", form));
            e.textContent = table.getAttribute("data-fail") || "";
            e.hidden = false;
            return;
          }
          form.hidden = true;
          $(".ask__lead", open).hidden = true;
          done.hidden = false;
          void done.offsetWidth;
          done.classList.add("is-on");
          done.focus({ preventScroll: true });
        });
      });
    };

    body.addEventListener("click", function (e) {
      var row = e.target.closest("tr[data-grade]");
      if (row) pick(row);
    });
    body.addEventListener("keydown", function (e) {
      if (e.key !== "Enter" && e.key !== " ") return;
      var row = e.target.closest("tr[data-grade]");
      if (!row) return;
      e.preventDefault();
      pick(row);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  })();

  /* ----------------------------------------------------------- lightbox --- */
  /* Gallery photos open full size over the page. Arrow keys and swipes move
     through the photos on the page; videos play in place and are skipped. */
  (function () {
    var links = $$("[data-lightbox]");
    if (!links.length) return;
    var box = document.createElement("div");
    box.className = "lb";
    box.hidden = true;
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "Photo viewer");
    box.innerHTML =
      '<figure class="lb__fig"><img class="lb__img" alt=""><figcaption class="lb__cap"></figcaption></figure>' +
      '<button class="lb__btn lb__x" type="button" aria-label="Close">&times;</button>' +
      '<button class="lb__btn lb__prev" type="button" aria-label="Previous photo">&lsaquo;</button>' +
      '<button class="lb__btn lb__next" type="button" aria-label="Next photo">&rsaquo;</button>' +
      '<p class="lb__n" aria-live="polite"></p>';
    document.body.appendChild(box);
    var im = $(".lb__img", box), cap = $(".lb__cap", box), num = $(".lb__n", box);
    var at = 0, back = null;
    var show = function (i) {
      at = (i + links.length) % links.length;
      var a = links[at], pic = $("img", a);
      im.src = a.getAttribute("href");
      im.alt = pic ? pic.alt : "";
      var fc = a.parentNode.querySelector("figcaption");
      cap.textContent = fc ? fc.textContent : (pic ? pic.alt : "");
      num.textContent = (at + 1) + " / " + links.length;
    };
    var open = function (i) {
      back = document.activeElement;
      show(i);
      box.hidden = false;
      document.documentElement.classList.add("lb-open");
      $(".lb__x", box).focus();
    };
    var close = function () {
      box.hidden = true;
      document.documentElement.classList.remove("lb-open");
      im.removeAttribute("src");
      if (back) back.focus();
    };
    links.forEach(function (a, i) {
      a.addEventListener("click", function (e) { e.preventDefault(); open(i); });
    });
    $(".lb__x", box).addEventListener("click", close);
    $(".lb__prev", box).addEventListener("click", function () { show(at - 1); });
    $(".lb__next", box).addEventListener("click", function () { show(at + 1); });
    box.addEventListener("click", function (e) {
      if (e.target === box || e.target.classList.contains("lb__fig")) close();
    });
    document.addEventListener("keydown", function (e) {
      if (box.hidden) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowLeft") show(at - 1);
      else if (e.key === "ArrowRight") show(at + 1);
    });
    var x0 = null;
    box.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    box.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) show(at + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  })();

  /* ------------------------------------------- one video plays at a time --- */
  document.addEventListener("play", function (e) {
    $$("video").forEach(function (v) { if (v !== e.target) v.pause(); });
  }, true);

  /* ------------------------------- arrive at the form with a grade set --- */
  (function () {
    var field = $('[data-enquiry] input[name="grade"]');
    if (!field) return;
    var grade = new URLSearchParams(location.search).get("grade");
    if (!grade) return;
    field.value = grade;
    field.classList.add("is-prefilled");
    // land on the form with the first empty field ready, not the filled one
    var name = $('[data-enquiry] input[name="name"]');
    if (name) setTimeout(function () { name.focus({ preventScroll: true }); }, 260);
  })();

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

  /* ------------------------------------------------ enquiry -> email --- */
  var form = $("[data-enquiry]");
  if (form) {
    var send = $("[data-send]", form), status = $("[data-status]", form);
    guard(form);
    var thanks = $("[data-thanks]");
    $("[data-again]", thanks).addEventListener("click", function () {
      thanks.hidden = true;
      thanks.classList.remove("is-on");
      status.hidden = true;
      form.hidden = false;
      var n = $('input[name="name"]', form);
      if (n) n.focus();
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validate(form)) return;
      var d = new FormData(form);
      var payload = { page: location.href };
      ["name", "company", "phone", "email", "grade", "process", "weight",
       "size", "hardness", "message"].forEach(function (k) {
        payload[k] = (d.get(k) || "").toString().trim();
      });
      var file = d.get("drawing");
      if (!(file && file.size)) file = null;
      send.disabled = true;
      send.textContent = "Sending\u2026";
      status.hidden = true;
      deliver(payload, {
        endpoint: form.getAttribute("data-endpoint") || "",
        cc: form.getAttribute("data-cc") || "",
        file: file
      }).then(function (ok) {
        send.disabled = false;
        send.textContent = "Send enquiry";
        if (ok) {
          // close the form and show the thank-you with its drawn tick
          form.reset();
          form.hidden = true;
          thanks.hidden = false;
          thanks.classList.remove("is-on");
          void thanks.offsetWidth;
          thanks.classList.add("is-on");
          thanks.focus({ preventScroll: true });
          var top = thanks.getBoundingClientRect().top;
          if (top < 80 || top > window.innerHeight - 200) {
            thanks.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" });
          }
          return;
        }
        status.textContent = form.getAttribute("data-fail");
        status.classList.add("is-fail");
        status.hidden = false;
      });
    });
  }
})();
