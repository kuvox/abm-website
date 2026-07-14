# Austin Becker E-Commerce Marketing — Static Site

A plain HTML/CSS replacement for the WordPress version of abeckermarketing.com. No build step, no database, no plugins — just files you can edit in any text editor.

## What's in here

```
├── index.html              ← homepage
├── about.html
├── contact.html            ← contact form (HubSpot embed placeholder)
├── resources.html          ← gated guides (HubSpot signup placeholder)
├── case-studies.html
├── services.html           ← services + pricing hub
├── supported-ad-platforms.html
├── guides/                 ← long-form guides (feed demo, vehicle ads, etc.)
├── privacy-policy.html
├── 404.html
├── _archive/               ← archived pages (not deployed)
│   └── services/
│       └── amazon-ads.html
├── case-studies/           ← one HTML file per client (generated)
├── styles.css              ← all styling (one file)
├── site_nav.py             ← shared header/footer/megamenu
├── client_logos_grid.py    ← client logo grid source
├── case_studies_section.py ← case study carousel source
├── scripts/                ← sync scripts, autoscroll, pricing carousel, etc.
├── snippets/               ← canonical HTML fragments (logos, reviews)
├── robots.txt
└── sitemap.xml
```

**Docs:** `informational-pages.md`, `client-logos.md`, `website-logos.md`, `docs/PAGE_PATTERNS.md`.

`generate_pages.py` regenerates case study and resource article pages from data tables. Sync scripts (`scripts/sync_*.py`) push shared snippets into `index.html`, `about.html`, etc.

---

## 1. Deploy to Cloudflare Pages

Cloudflare Pages is free and the perfect host for a site like this.

**Easiest path (drag-and-drop):**

1. Go to [dash.cloudflare.com](https://dash.cloudflare.com) → **Workers & Pages** → **Create** → **Pages** → **Upload assets**.
2. Drag the entire `site/` folder into the upload area.
3. Give it a project name (e.g., `abm`) and click **Deploy**.
4. You'll get a `*.pages.dev` URL. Test it in a browser.
5. To use your real domain, go to **Custom domains** → add `abeckermarketing.com`. Cloudflare will walk you through pointing your DNS records.

**Better path (Git-connected, auto-deploys when you edit):**

1. Push the `site/` folder to a GitHub or GitLab repo.
2. In Cloudflare Pages: **Create a project** → **Connect to Git** → pick your repo.
3. **Build command:** leave blank. **Build output directory:** `site` (or whatever folder you used). **Framework preset:** None.
4. Click **Save and Deploy**. Future commits to the main branch redeploy automatically.

**Cutting over from WordPress:**

When you're ready to switch:

1. Verify the new site looks right on its `*.pages.dev` URL.
2. Add `abeckermarketing.com` as a custom domain in Cloudflare Pages.
3. Update your DNS (in whatever registrar holds your domain) to point at Cloudflare's nameservers, OR add the `CNAME` record Cloudflare gives you.
4. Once DNS propagates, your domain serves the new static site instead of WordPress. You can shut down the WordPress hosting after a few days of confirming everything works.

---

## 2. Wire up HubSpot forms

Both the contact form (`contact.html`) and the newsletter signup (`resources.html`) currently show a placeholder where the HubSpot form should mount. To wire them up:

### Step A — Build the forms in HubSpot

1. In HubSpot: **Marketing → Forms → Create form**.
2. Build two forms:
   - **Contact us** — name, email, company URL, annual revenue, message.
   - **Free guides signup** — first name, email. (Keep it short. Lower friction = more signups.)
3. Save each form.

### Step B — Get the embed code

1. Open each form → **Share → Embed code**. You'll see a snippet that looks like this:

   ```html
   <script charset="utf-8" type="text/javascript" src="//js-na2.hsforms.net/forms/embed/v2.js"></script>
   <script>
     hbspt.forms.create({
       region: "na2",
       portalId: "12345678",
       formId: "abcdef12-3456-7890-abcd-ef1234567890"
     });
   </script>
   ```

2. Copy that code.

### Step C — Paste it into the HTML

**Contact form** — open `site/contact.html`, find this block:

```html
<div id="hubspot-contact-form" class="hubspot-placeholder">
  <strong>HubSpot contact form mounts here.</strong>
  ...
</div>
```

Replace the entire `<div id="hubspot-contact-form" ...>...</div>` with your HubSpot embed snippet from Step B.

**Newsletter signup** — open `site/resources.html`, find:

```html
<div id="hubspot-newsletter-form" class="hubspot-placeholder">
  <strong>HubSpot signup form mounts here.</strong>
  ...
</div>
```

Replace it with your newsletter form's embed snippet.

Save, redeploy. The forms now submit straight into HubSpot.

---

## 3. Set up the HubSpot workflow that emails guide links

This is the magic that delivers the gated guides automatically.

1. In HubSpot: **Automation → Workflows → Create workflow → Contact-based**.
2. **Enrollment trigger:** "Form submission" → select your *Free Guides Signup* form.
3. **Action 1:** Send marketing email.
   - Create a new marketing email titled "Your free PPC guides 📚" (or similar).
   - In the body, paste the Notion URLs to your guides (more on Notion in section 4).
4. **Action 2 (optional):** Add the contact to a list called "Newsletter Subscribers" so you can email them with future guides.
5. **Action 3 (optional):** After 3 days, send a follow-up checking in.

Turn the workflow on. Now every signup automatically gets the guide links.

---

## 4. Hosting your guides on Notion (non-indexable)

Notion is great for this — you can publish pages publicly, but Google won't index them.

### Per-guide setup

1. In Notion, open the guide page you want to share.
2. Click **Share** (top right) → **Publish** → toggle **Publish to web ON**.
3. Click **Settings** under the publish toggle. Turn:
   - **Allow editing** → OFF
   - **Allow comments** → your call
   - **Allow duplicate as template** → OFF (otherwise people can lift your work)
   - **Search engine indexing** → **OFF** ← **this is the key setting**
4. Copy the public URL. It looks like `https://your-workspace.notion.site/Your-Guide-Title-abc123def456`.
5. Paste that URL into your HubSpot welcome email.

That's it. The page is publicly accessible to anyone who has the link, but it won't appear in Google search results, and the URL is long enough to be impractical to guess.

### Adding a new guide later

1. Write the guide in Notion → publish it with indexing off (steps above).
2. In `site/resources.html`, add a new entry to the guides list. Look for the `<div class="resource-row">` blocks and copy one. Update the title and description.
3. In HubSpot, edit the welcome email and add the new guide's link.
4. Redeploy the site (drag-and-drop, or a Git push if connected).

---

## 5. Editing copy on the site

Every page is plain HTML. To change a headline, paragraph, or service description:

1. Open the relevant `.html` file in any text editor (VS Code, Sublime, even TextEdit).
2. Find the text and change it. Don't worry about HTML tags — just don't delete them.
3. Save the file.
4. Redeploy (drag-and-drop folder, or `git commit && git push` if connected).

**Common edits:**

- **Hero headline / subhead** → top of `index.html`, inside `<section class="hero">`.
- **Stats numbers** → `index.html`, inside `<section class="section section--alt">` after the hero.
- **Testimonials** → `index.html`, inside the `<!-- TESTIMONIALS -->` section.
- **Service descriptions** → either the homepage cards (`index.html`) or the individual service page (`services/*.html`).
- **Brand color** → change `--brand: #e84f3b;` at the top of `styles.css` to retheme the whole site.

---

## 6. Updating the service pages in bulk

If you want to edit all 7 service pages at once (e.g., adding a new section to all of them), it's easiest to edit `build_pages.py` (in the parent folder), update the `services` list and the service-page template inside the loop, then re-run:

```bash
python3 build_pages.py
```

That regenerates all 7 service pages from the template. Then redeploy.

---

## 7. SEO checklist

Already done for you:

- [x] `<title>` and `<meta name="description">` on every page
- [x] Open Graph tags on the homepage (you can copy the pattern to other pages if you want richer social shares)
- [x] `robots.txt` — allows search engines, points at the sitemap
- [x] `sitemap.xml` — lists all the public pages
- [x] Canonical URLs on the homepage

Still to do (manual):

- [ ] Submit `https://abeckermarketing.com/sitemap.xml` to Google Search Console after launch
- [ ] Add Google Analytics or your preferred analytics tag (paste the snippet just before `</head>` in each HTML file, or in a shared include)
- [ ] Set up 301 redirects from old WordPress URLs to new URLs if any URL paths changed (Cloudflare Pages supports a `_redirects` file or you can do it at the DNS level)

---

## 8. What this does NOT include

- **A blog/CMS.** WordPress's strength was easy content publishing. If you want to keep posting articles, two options:
  1. Write blog posts in Notion (publish with indexing **on** for blog posts you want Google to find), and link to them from a `/blog` index page on this site.
  2. Add a static-site generator like Eleventy or Astro later if you want fancier blog tooling.
- **Logged-in user areas.** Static sites can't authenticate users. The Notion + HubSpot workflow approach replaces that need for guide gating.
- **E-commerce or members-only payments.** Out of scope — let me know if you ever need this and we'll layer it in.

---

## Questions?

When you hit something, ping me. The most common gotchas are:
- HubSpot embed code pasted in the wrong spot — make sure you replace the entire placeholder `<div>`, not just the text inside it.
- Custom domain not resolving — DNS propagation can take 30 min to a few hours.
- Forms working but not triggering the workflow — check the workflow's enrollment trigger is set to the *exact* form you embedded.
