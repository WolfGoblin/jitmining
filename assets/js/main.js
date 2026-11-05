/* JIT Mining — site behaviour (no dependencies) */
(function () {
  document.documentElement.classList.remove("no-js");

  var CONTACT = { email: "info@jitmining.com", wa: "260961481874" };

  // Mobile menu
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var hdr = document.querySelector(".site-header");
      nav.style.top = hdr.getBoundingClientRect().bottom + "px";
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open);
      document.body.style.overflow = open ? "hidden" : "";
    });
  }

  // Dropdowns (click for touch/keyboard, hover handled by CSS on desktop)
  document.querySelectorAll(".nav .dd > button").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var dd = btn.parentElement;
      var open = !dd.classList.contains("open");
      document.querySelectorAll(".nav .dd.open").forEach(function (o) { if (o !== dd) { o.classList.remove("open"); o.firstElementChild.setAttribute("aria-expanded", "false"); } });
      dd.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open);
    });
  });
  document.addEventListener("click", function () {
    if (window.innerWidth > 1180) document.querySelectorAll(".nav .dd.open").forEach(function (o) { o.classList.remove("open"); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") document.querySelectorAll(".nav .dd.open").forEach(function (o) { o.classList.remove("open"); });
  });

  // Ticker: duplicate content for a seamless loop
  document.querySelectorAll(".ticker-track").forEach(function (t) {
    t.innerHTML += t.innerHTML;
    Array.prototype.slice.call(t.children, t.children.length / 2).forEach(function (c) { c.setAttribute("aria-hidden", "true"); c.tabIndex = -1; });
  });

  // Scroll reveal
  var els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    els.forEach(function (el, i) {
      el.style.transitionDelay = (el.dataset.delay || 0) + "ms";
      io.observe(el);
    });
  } else {
    els.forEach(function (el) { el.classList.add("in"); });
  }

  // Year
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Forms: no server yet — compose an email (or WhatsApp message) from the fields.
  function collect(form) {
    var lines = [];
    Array.prototype.forEach.call(form.elements, function (f) {
      if (!f.name || f.type === "submit" || f.type === "button" || f.type === "file") return;
      if (!f.value) return;
      var label = f.dataset.label || f.name;
      lines.push(label + ": " + f.value);
    });
    return lines;
  }

  document.querySelectorAll("form[data-mailto]").forEach(function (form) {
    var status = form.querySelector(".form-status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var subject = form.dataset.mailto;
      var body = collect(form).join("\n");
      window.location.href = "mailto:" + CONTACT.email + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      if (status) {
        status.textContent = "Your email app should now open with the details filled in — press send to reach our desk. If nothing opens, email " + CONTACT.email + " or use WhatsApp.";
        status.classList.add("show");
      }
    });
    var waBtn = form.querySelector("[data-wa-send]");
    if (waBtn) {
      waBtn.addEventListener("click", function () {
        var text = form.dataset.mailto + "\n" + collect(form).join("\n");
        window.open("https://wa.me/" + CONTACT.wa + "?text=" + encodeURIComponent(text), "_blank", "noopener");
      });
    }
  });
})();
