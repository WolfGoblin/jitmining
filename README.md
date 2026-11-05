# JIT Mining website

A static website for JIT Mining & General Contractors Limited. It has no build server or database, so it can be hosted anywhere (cPanel, Netlify, GitHub Pages, Cloudflare Pages).

## Pages

| File | Page |
|---|---|
| `index.html` | Home |
| `products.html` | Minerals & products (copper cathode, concentrate, ore, manganese, iron ore, gold) |
| `logistics.html` | Export logistics, routes and bonded warehousing |
| `due-diligence.html` | Verification standard, 7-step procedure, inspection |
| `services.html` | Geology, valuation, investor readiness, contract facilitation, general contracting |
| `about.html` | Who we are, mission, values |
| `contact.html` | Contact details, message form and map |
| `rfq.html` | Request a quote |
| `privacy.html`, `404.html` | Privacy notice, not-found page |

## Editing

Don't edit the root `.html` files directly. They are generated.

1. Edit the page content in `src/pages/*.html`. To change the header, footer or contact details (email, phone, address), edit `tools/build.py`.
2. Rebuild:

   ```bash
   python tools/build.py
   ```

3. Upload everything except `src/`, `tools/` and `.claude/` to the web host.

Styles are in `assets/css/style.css` and behaviour is in `assets/js/main.js`.

## Forms

The RFQ and contact forms open the visitor's email app, with the message addressed to info@jitmining.com and filled in. They can also send the same details by WhatsApp to +260 961 481 874. To receive form submissions without the visitor's email app, connect a form service such as Formspree or Netlify Forms and change the `submit` handler in `assets/js/main.js`.
