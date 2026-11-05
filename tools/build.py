"""Assemble the static site.

Each file in src/pages/ starts with a meta block:

    <!--meta
    title: Page title
    description: Meta description
    nav: home
    -->

The build wraps every page in the shared header and footer, swaps [[i:name]]
for inline SVG icons, and writes the result to the site root (one level up
from tools/). Run:  python tools/build.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "pages"

SITE = {
    "name": "JIT Mining & General Contractors Limited",
    "short": "JIT Mining",
    "email": "info@jitmining.com",
    "phone_display": "+260 961 481 874",
    "phone": "+260961481874",
    "wa": "260961481874",
    "address": "Plot No. 1345, Industrial Area",
    "city": "Kitwe",
    "zip": "50100",
    "country": "Zambia",
    "url": "https://jitmining.com",
}

ICONS = {
    "mail": '<path d="M4 6h16v12H4z"/><path d="m4 7 8 6 8-6"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "shield": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    "flask": '<path d="M9 3h6M10 3v6L4 19a1.5 1.5 0 0 0 1.3 2h13.4a1.5 1.5 0 0 0 1.3-2L14 9V3"/><path d="M7 15h10"/>',
    "truck": '<path d="M3 6h11v10H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
    "ship": '<path d="M3 17c2 2 4 2 6 0 2 2 4 2 6 0 2 2 4 2 6 0"/><path d="M5 14 4 10h16l-1 4M8 10V6h8v4M12 3v3"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
    "scale": '<path d="M12 4v16M6 20h12M5 8h14M5 8l-3 6a3 3 0 0 0 6 0zM19 8l-3 6a3 3 0 0 0 6 0z"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
    "chart": '<path d="M4 20V4M4 20h16"/><path d="m7 15 4-4 3 3 5-6"/>',
    "users": '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2A5 5 0 0 1 21 19"/>',
    "handshake": '<path d="m11 17 2 2a1.4 1.4 0 0 0 2-2"/><path d="m14 14 2.5 2.5a1.4 1.4 0 0 0 2-2L15 11l-3 1-2-2 3-3h3l4 4"/><path d="M3 11 7 7l5 5"/><path d="m7 15 2 2"/>',
    "pick": '<path d="M14 6c3-2 6-1 7 1-3-1-5-1-7 1"/><path d="M10 6C7 4 4 5 3 7c3-1 5-1 7 1"/><path d="m12 6-8 15M12 6l1.5 2"/>',
    "hammer": '<path d="m14 4 6 6-3 3-6-6z"/><path d="m11 7-8 8 3 3 8-8"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "warehouse": '<path d="M3 21V9l9-5 9 5v12"/><path d="M7 21v-8h10v8M7 17h10"/>',
    "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="1"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    "map": '<path d="m9 4-6 2v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
    "cog": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9 7 7M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>',
    "heart": '<path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"/>',
    "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.3 1 2.1h5c0-.8.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
}
WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-1 1.2-.4.2-.7.1a8.2 8.2 0 0 1-4-3.5c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.7 3.7 0 0 0-1.1 2.8 6.5 6.5 0 0 0 1.4 3.4 14.6 14.6 0 0 0 5.6 5c2.1.9 2.9 1 4 .8a3.4 3.4 0 0 0 2.2-1.6 2.8 2.8 0 0 0 .2-1.6c-.1-.1-.3-.2-.6-.3zM12 21.8a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zm8.4-18.2A11.8 11.8 0 0 0 1.8 17.9L.1 24l6.3-1.6A11.8 11.8 0 0 0 12 23.8 11.9 11.9 0 0 0 20.4 3.6z"/></svg>'


def icon(name):
    if name == "wa":
        return WA_SVG
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[name] + "</svg>")


def wa_link(text):
    from urllib.parse import quote
    return f"https://wa.me/{SITE['wa']}?text={quote(text)}"


NAV = [
    ("home", "Home", "index.html", None),
    ("products", "Products", "products.html", [
        ("All products", "Commodities, grades & terms", "products.html"),
        ("Copper cathodes", "99.99% Cu, LME Grade A", "products.html#copper-cathode"),
        ("Copper concentrate", "Cu 35%, DMT basis", "products.html#copper-concentrate"),
        ("Copper ore", "Cu 20–25%", "products.html#copper-ore"),
        ("Manganese ore", "Mn 52–67% min", "products.html#manganese"),
        ("Iron ore", "Fe 62%", "products.html#iron-ore"),
        ("Gold (Au)", "96–99.99%", "products.html#gold"),
    ]),
    ("logistics", "Logistics", "logistics.html", [
        ("Export logistics & transport", "Rail and road to the ports", "logistics.html"),
        ("Shipping routes & transit", "Dar es Salaam & Durban", "logistics.html#routes"),
        ("Bonded warehousing", "Lusaka, Ndola & Kitwe", "logistics.html#warehousing"),
    ]),
    ("due-diligence", "Due Diligence", "due-diligence.html", [
        ("The JIT Verification Standard", "What we check before you commit", "due-diligence.html"),
        ("Transaction procedure", "LOI to loading in 7 steps", "due-diligence.html#procedure"),
        ("Inspection & quality assurance", "SGS / Bureau Veritas at loading", "due-diligence.html#inspection"),
    ]),
    ("services", "Mining Services", "services.html", None),

    ("about", "About", "about.html", None),
    ("contact", "Contact", "contact.html", None),
]


def header(current):
    items = []
    for key, label, href, sub in NAV:
        cur = ' aria-current="page"' if key == current else ""
        if sub:
            links = "".join(f'<a href="{h}"><b>{t}</b><small>{s}</small></a>' for t, s, h in sub)
            items.append(
                f'<div class="dd{" current" if key == current else ""}"><button type="button" aria-expanded="false">{label}{icon("chev")}</button>'
                f'<div class="dd-menu">{links}</div></div>')
        else:
            items.append(f'<a href="{href}"{cur}>{label}</a>')
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <div class="tb-left"><a href="mailto:{SITE['email']}">{SITE['email']}</a><a href="tel:{SITE['phone']}">{SITE['phone_display']}</a></div>
  <div class="tb-right hide-sm"><span><i class="dot"></i>Kitwe · Copperbelt · Zambia</span></div>
</div></div>
<header class="site-header"><div class="wrap">
  <a class="brand" href="index.html" aria-label="JIT Mining home">
    <img src="assets/img/logo.png" alt="JMGC logo" width="60" height="60">
    <span class="brand-text"><b>JIT<span>.</span>MINING</b><small>Mining &amp; General Contractors</small></span>
  </a>
  <nav class="nav" aria-label="Main">
    {''.join(items)}
    <div class="nav-cta"><a class="btn orange" href="rfq.html">Request a quote</a></div>
  </nav>
  <a class="btn orange header-cta" href="rfq.html">Request Quote</a>
  <button class="menu-toggle" type="button" aria-label="Open menu" aria-expanded="false">{icon('menu')}</button>
</div></header>"""


def footer():
    return f"""<footer class="site-footer">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <div class="logo-disc"><img src="assets/img/logo.png" alt="JMGC logo" width="80" height="80"></div>
      <p>We supply high-grade minerals from Zambia to the international market and help investors and mining companies get work done on the Copperbelt — from geology and valuation to contracts, inspection and loading.</p>
      <div class="socials">
        <a href="{wa_link('Hello JIT Mining, I would like to make an enquiry.')}" aria-label="WhatsApp" target="_blank" rel="noopener">{WA_SVG}</a>
        <a href="mailto:{SITE['email']}" aria-label="Email">{icon('mail')}</a>
        <a href="tel:{SITE['phone']}" aria-label="Call">{icon('phone')}</a>
      </div>
    </div>
    <div>
      <h4>Minerals</h4>
      <ul>
        <li><a href="products.html#copper-cathode">Copper cathodes</a></li>
        <li><a href="products.html#copper-concentrate">Copper concentrate</a></li>
        <li><a href="products.html#copper-ore">Copper ore</a></li>
        <li><a href="products.html#manganese">Manganese ore</a></li>
        <li><a href="products.html#iron-ore">Iron ore</a></li>
        <li><a href="products.html#gold">Gold (Au)</a></li>
        <li><a href="products.html">All products</a></li>
      </ul>
    </div>
    <div>
      <h4>Services</h4>
      <ul>
        <li><a href="logistics.html">Export logistics &amp; transport</a></li>
        <li><a href="logistics.html#warehousing">Bonded warehousing</a></li>
        <li><a href="due-diligence.html">Due diligence &amp; inspection</a></li>
        <li><a href="services.html#geology">Geological services</a></li>
        <li><a href="services.html#valuation">Asset valuation</a></li>
        <li><a href="services.html#investor">Investor readiness</a></li>
        <li><a href="services.html#contracts">Contract facilitation</a></li>
        <li><a href="services.html#contracting">General contracting</a></li>
      </ul>
    </div>
    <div>
      <h4>Head office</h4>
      <address>
        {SITE['name']}<br>
        {SITE['address']}<br>
        {SITE['city']} {SITE['zip']}, {SITE['country']}<br>
        <a href="tel:{SITE['phone']}">{SITE['phone_display']}</a><br>
        <a href="mailto:{SITE['email']}">{SITE['email']}</a>
      </address>
      <ul class="mt-2">
        <li><a href="rfq.html">Request a quote</a></li>
        <li><a href="about.html">About us</a></li>
        <li><a href="contact.html">Contact us</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap foot-bottom">
    <span>© <span data-year>2026</span> JIT Mining &amp; General Contractors Limited · Kitwe, Zambia</span>
    <span><a href="privacy.html">Privacy</a> · <a href="contact.html">Contact</a></span>
  </div>
</footer>
<a class="wa-float" href="{wa_link('Hello JIT Mining. Please share current availability, specifications and terms.')}" target="_blank" rel="noopener" aria-label="Chat with JIT Mining on WhatsApp">{WA_SVG}</a>"""


def ver():
    """Cache-busting stamp from the CSS/JS contents."""
    import hashlib
    h = hashlib.md5()
    for f in ("assets/css/style.css", "assets/js/main.js"):
        h.update((ROOT / f).read_bytes())
    return h.hexdigest()[:8]


def page(meta, body):
    title = meta["title"]
    desc = meta.get("description", "")
    canonical = SITE["url"] + "/" + (meta["file"] if meta["file"] != "index.html" else "")
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE['url']}/assets/img/hero-underground.jpg">
<meta name="theme-color" content="#0d0c0a">
<link rel="icon" href="favicon.ico?v=2" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png?v=2">
<link rel="icon" type="image/png" sizes="192x192" href="assets/img/favicon.png?v=2">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800;900&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v={ver()}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"{SITE['name']}","url":"{SITE['url']}","logo":"{SITE['url']}/assets/img/logo.png","email":"{SITE['email']}","telephone":"{SITE['phone']}","address":{{"@type":"PostalAddress","streetAddress":"{SITE['address']}","addressLocality":"{SITE['city']}","postalCode":"{SITE['zip']}","addressCountry":"ZM"}}}}</script>
</head>
<body>
{header(meta.get('nav', ''))}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/js/main.js?v={ver()}"></script>
</body>
</html>
"""


def build():
    count = 0
    for src in sorted(SRC.glob("*.html")):
        text = src.read_text(encoding="utf-8")
        m = re.match(r"<!--meta\n(.*?)\n-->\n", text, re.S)
        meta = dict(line.split(": ", 1) for line in m.group(1).splitlines())
        meta["file"] = src.name
        body = text[m.end():]
        body = re.sub(r"\[\[i:(\w+)\]\]", lambda mm: icon(mm.group(1)), body)
        body = re.sub(r"\[\[wa:(.*?)\]\]", lambda mm: wa_link(mm.group(1)), body)
        for k, v in SITE.items():
            body = body.replace("{{" + k + "}}", v)
        (ROOT / src.name).write_text(page(meta, body), encoding="utf-8")
        count += 1
    print(f"built {count} pages into {ROOT}")


if __name__ == "__main__":
    build()
