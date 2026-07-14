# Informational Pages — Design Guidelines

Design patterns for **services**, **supported ad platforms**, and other marketing/informational pages on abeckermarketing.com. Reference implementation: `services.html` and `supported-ad-platforms.html`. Styles live in `styles.css`.

---

## Global tokens

| Token | Value | Use |
|-------|-------|-----|
| `--brand` | `#e84f3b` | Primary red, links, accents |
| `--brand-tint` | `#faebe8` | Pale red wash (stat cards, pricing cards) |
| `--bg-black` | `#151619` | Services hero shell |
| `--ink` / `--ink-soft` | `#343536` / `#5a5a5a` | Body text on light backgrounds |
| `--line` | border gray | Card borders |
| `--radius-lg` | large corner radius | Cards, hero photo |
| `--shadow-sm` / `--shadow-lg` | soft shadows | Cards, hover states |

**Gradient text:** wrap accent phrases in `<span class="grad-text">` or use `eyebrow-gradient` on headings for the brand red gradient.

---

## 1. Hero section (offset image)

Savvy Revenue–style band: **black top**, **white below**, photo bridges both at ~50% height.

### Structure

```html
<section class="services-page-hero">
  <div class="services-page-hero__shell">
    <div class="container">
      <div class="services-page-hero__top">
        <div class="services-page-hero__title">
          <h1>Page Title</h1>
          <p class="services-page-hero__tagline">
            <span class="grad-text">Red Gradient Tagline</span>
          </p>
        </div>
      </div>
    </div>
    <div class="container">
      <figure class="services-page-hero__photo">
        <img src="images/austin-becker-e-commerce-marketing-15.jpg" alt="…">
      </figure>
    </div>
  </div>
  <div class="services-page-hero__spacer" aria-hidden="true"></div>
</section>
```

### Design rules

- **Shell:** flat black (`var(--bg-black)`), white `h1`, generous vertical padding.
- **Tagline:** large heading font via `services-page-hero__tagline` + `grad-text` (same treatment as homepage “Increase 10% to 100% a Year”).
- **Photo:** left-aligned, max ~54% width, rounded corners, shadow. Negative bottom margin pulls image into white section; top half reads on black, bottom half on white.
- **Spacer:** white band with negative margin so white background rises to mid-photo without moving content below.
- **No CTA buttons** in hero on informational pages — copy lives in the intro block below.

### CSS variables (`.services-page-hero`)

- `--services-photo-half` — distance white rises / photo overhang (~130–190px desktop)
- `--services-white-rise` — same as photo half
- `--services-photo-overhang` — negative margin on photo bottom

### Page examples

| Page | H1 | Tagline |
|------|-----|---------|
| Services | Services + Pricing | Google Shopping Plus Social & Ai Ads |
| Supported Ad Platforms | Supported Ad Platforms | Search, Social, Marketplaces & AI |

---

## 2. Intro split (right-column copy)

Sits in `services-hub-section`, aligned with photo column on the left.

```html
<div class="services-intro-split">
  <div class="services-intro-split__spacer" aria-hidden="true"></div>
  <div class="services-intro-split__copy">
    <h2 class="eyebrow-gradient">Section Eyebrow</h2>
    <p>First paragraph…</p>
    <p>Second paragraph…</p>
  </div>
</div>
```

- **Grid:** left column empty (aligns with hero photo width); copy on right.
- **Heading:** `h2.eyebrow-gradient` — title case, same size as service card `h2` (`clamp(1.5rem, 2.6vw, 1.85rem)`), gradient color.
- **Body:** `--ink-soft`, max ~52ch, left-aligned.
- **Spacing:** extra margin below last paragraph before logos/cards.

---

## 3. Platform logos block

Partner badges above; channel logos in a white card below.

```html
<div class="services-platform-logos">
  <div class="services-platform-logos__partners badge-row">
    <!-- Google + Microsoft partner badges -->
  </div>
  <div class="services-platform-logos__card">
    <ul class="services-platform-logos__grid" role="list">
      <li><a href="#anchor"><img src="images/website-logos/facebook-icon.png" alt="Facebook"></a></li>
      <!-- … -->
    </ul>
  </div>
</div>
```

- **Partner row:** `badge-row`, left-aligned, ~72–88px badge height, links to partner profiles.
- **Logo card:** white background, border, `border-radius-lg`, light shadow — matches service cards.
- **Logo grid:** single row on desktop (`flex-wrap: nowrap`, `justify-content: space-between`); wraps on mobile.
- **Logo cells:** ~110×140px max, logos scale with `object-fit: contain`.
- **Assets:** use PNG brand files in `images/` (Facebook, Instagram, YouTube, Pinterest, Target, eBay, ChatGPT).

---

## 4. Service / content cards (Ad Management block)

Stacked full-width white cards for each topic. Used for **Ad Management**, **Product Feeds**, **Consulting**, and each **ad platform** on `supported-ad-platforms.html`.

```html
<div class="services-hub-list">
  <article class="service-card" id="ad-management-pricing">
    <h2>Ad Management</h2>
    <p>Body copy…</p>
  </article>
</div>
```

### Design rules

- **Container:** `services-hub-section` with negative top margin so cards overlap hero photo zone; white page background.
- **Card:** white bg, 1px border, large radius, soft shadow; hover lifts slightly (`translateY(-2px)`, stronger shadow).
- **Heading:** `h2` at `clamp(1.5rem, 2.6vw, 1.85rem)`, bold, dark ink.
- **Body:** `--ink-soft`, 1.0625rem, line-height ~1.7. Multiple paragraphs use default `p + p` spacing.
- **Anchors:** meaningful `id` on each card for megamenu deep links (e.g. `#ad-management-pricing`, `#google-youtube`).
- **Links in copy:** `font-weight: 600`, brand color on hover.

---

## 5. Pricing block

Lifted panel on soft gray band; carousel left, explanatory copy right.

```html
<section class="section pricing-section" id="pricing">
  <div class="container">
    <div class="pricing-panel">
      <div class="pricing-split">
        <div class="pricing-carousel-wrap">
          <div class="pricing-carousel" id="pricing-carousel" role="region" …>
            <article class="pricing-card">
              <p class="pricing-card__detail">
                <strong class="pricing-card__tier">Large Shop:</strong> …
              </p>
              <p class="pricing-card__fee eyebrow-gradient">$6,500 to $8,500 per month fee…</p>
            </article>
          </div>
          <div class="pricing-carousel-dots" role="tablist">…</div>
        </div>
        <div class="pricing-copy">
          <h2>Pricing Examples</h2>
          <p>…</p>
        </div>
      </div>
    </div>
  </div>
</section>
<script src="scripts/pricing-carousel.js"></script>
```

### Design rules

- **Section bg:** `var(--bg-soft)` (#f7f7f8).
- **Panel:** white card, border, radius, padding — “lifted” over gray.
- **Carousel cards:** `--brand-tint` background (pale red), horizontal scroll, snap; tier name in **title case** (`Large Shop`, `Medium Shop`, etc.).
- **Fee line:** `eyebrow-gradient` for dollar amounts.
- **Dots:** below carousel; active dot filled brand red.
- **Copy column:** plain `h2` + muted paragraphs; stacks below carousel on mobile.
- **JS:** `scripts/pricing-carousel.js` syncs scroll position with dot navigation.

---

## 6. CTA banner

Standard closing block on informational pages.

```html
<section class="cta-banner">
  <div class="container">
    <h2>Ready to talk?</h2>
    <p>…</p>
    <a href="contact.html" class="btn btn-primary">Contact Us</a>
  </div>
</section>
```

---

## 7. “What It’s Like to Work With Us” block

Dark band above the footer on **services**, **supported ad platforms**, **resources**, and **all case study** pages (replaces the old embedded case-study contact form).

```html
<section class="section--black" id="work-with-us">
  <div class="container resources-work-split">
    <div>
      <h2>What it&rsquo;s Like to Work With Us</h2>
      <p>We work closely with our clients to understand their growth plans and growth limits. That allows both your team and ours to aim for ambitious goals that are feasible and within your budget.</p>
      <div class="hero-actions">
        <a href="about.html" class="btn btn-gradient">Who We Work With</a>
        <a href="services.html#pricing" class="hero-arrow-link">See Pricing Examples <span aria-hidden="true">&rsaquo;</span></a>
      </div>
    </div>
    <figure class="resources-work-photo">
      <img src="images/austin-becker-e-commerce-marketing-22.jpg" alt="Austin Becker and team collaborating on e-commerce marketing strategy">
    </figure>
  </div>
</section>
```

### Design rules

- **Layout:** 2-column grid — copy + actions left, office photo right (`resources-work-split`). Stacks to one column below 900px.
- **Background:** black (`section--black`), white heading and body text.
- **CTAs:** always **side by side** in `.hero-actions` — `flex-wrap: nowrap` on `.resources-work-split .hero-actions` so “Who We Work With” and “See Pricing Examples ›” stay on one row at all breakpoints.
- **Primary button:** `btn btn-gradient` → `about.html`.
- **Secondary link:** `hero-arrow-link` → `services.html#pricing` (scrolls to the pricing examples carousel). Use `../` prefixes on nested pages (case studies, guides, etc.).
- **Photo:** rounded corners, shadow; same asset sitewide.

---

## Homepage blocks (reference for future informational pages)

These patterns live on `index.html` but are documented here for reuse.

### 8. “Our approach to marketing” metric callout blocks

**Location:** `#services` section, `pov-intro-grid`.

```html
<div class="pov-intro-grid">
  <div class="pov-intro-text">
    <p class="eyebrow-gradient">Our approach to marketing</p>
    <h2>Where is Your Business's Opportunity Right Now?</h2>
    <p class="muted">…</p>
    <hr class="pov-divider">
    <p class="pov-featured-label">Follow us in</p>
    <div class="pov-featured-logos">…</div>
  </div>
  <div class="stat-card-grid">
    <article class="stat-card">…</article>
  </div>
</div>
```

- **Layout:** 2-column grid — narrative left, 2×2 stat card grid right.
- **Stat cards:** `--brand-tint` background, topic label, large figure (`stat-card-figure`), heading, body, arrow link.
- **Current cards (top-left → bottom-right):**
  1. **Data Feeds** — 10% → `guides/product-data-feeds-as-keywords.html`
  2. **Case Study** — 15.64% (Kingsley North) → `case-studies/kingsley-north.html`
  3. **Guides** — 2026 vehicle ads → `guides/google-vehicle-listing-ads.html`
  4. **Case Study** — 182% (Hose Warehouse / BeltSmart) → `case-studies/hose-warehouse-beltsmart.html`
- **Featured logos:** DataFeedWatch dropdown + PPC for Everyone YouTube link below divider.

---

### 9. Scrolling client logo grid

**Canonical source:** `client_logos_grid.py` → `snippets/client-logos-grid.html`. Run `python3 scripts/sync_client_logos_grid.py` after edits. Full rules in **`client-logos.md`**.

**Location:** `section--dark section--clients-dark` (home) or `about-hero-split` (about hero, right column).

```html
<div class="client-collage-shell">
  <div class="client-collage-card client-collage-card--home" aria-label="Client logos">
    <a class="logo-item logo-item--has-tooltip" href="…" target="_blank" rel="noopener">
      <img src="images/website-logos/website-client-logos/hosewarhouse-logo.png" alt="Hose Warehouse">
      <div class="logo-tooltip" role="tooltip">
        <p class="logo-tooltip-name">Hose Warehouse</p>
        <p class="logo-tooltip-tenure">6+ Year Client</p>
        <p class="logo-tooltip-category">Industrial Parts</p>
      </div>
    </a>
  </div>
</div>
```

- **Section:** dark background on home; about hero uses the same grid in the right column.
- **Logo grid:** 2-column card, fixed **420px** height, scrollable (manual + slow auto-scroll on home/about — see `client-logos.md`).
- **Featured logos:** linked tiles with name / tenure / category tooltips (black + red text on white popup).
- **Other logos:** link only, grayscale → color on hover, no tooltip.
- **Do not** maintain separate logo lists per page — edit `client_logos_grid.py`, then sync.

---

### 10. Client success stories (case studies carousel)

**Canonical source:** `case_studies_section.py` — run `python3 scripts/sync_case_studies_section.py` to sync `index.html`, `about.html`, `case-studies.html`, etc.

**Location:** `client-case-studies-section`.

```html
<section class="section section--alt client-case-studies-section">
  <div class="container">
    <div class="case-studies-carousel-header center">
      <h2>Customer Success Stories</h2>
    </div>
  </div>
  <div class="case-studies-carousel-track" tabindex="0" aria-label="Client case studies">
    <div class="case-studies-carousel">
      <a class="case-card" href="case-studies/kingsley-north.html">
        <video class="case-image" …></video><!-- or img -->
        <div class="case-body">
          <h3>Kingsley North</h3>
          <div class="result">15.64% Higher Conversion Rate</div>
          <p>Summary…</p>
          <span class="more">Read the case study &rarr;</span>
        </div>
      </a>
    </div>
  </div>
</section>
```

- **Layout:** full-bleed horizontal scroll track below centered heading.
- **Cards:** image or video top, client name, bold `.result` line, excerpt, “Read the case study →”.
- **Order:** Hose Warehouse → Kingsley North → Parker Baby → TallSlim Tees → Iron Fence Shop → TrailHeads → DataFeedWatch (external).

---

### 11. “What You Get” block

**Location:** `services-cta` section (brand-red gradient background).

```html
<section class="section services-cta">
  <div class="container">
    <div class="services-cta-intro">
      <p class="eyebrow services-cta-eyebrow">When You Work With Us</p>
      <h2>What You Get</h2>
      <div class="sync-graphic" aria-label="Optimized data and campaigns across platforms">
        <!-- platform logos → dots → ABM tile → dots → Shopify -->
      </div>
    </div>
    <div class="services-cta-copy">
      <p class="services-cta-body">Our team takes over responsibility for all of the paid ads duties below…</p>
      <ul class="services-cta-dashlist" aria-label="Included services">
        <li>Create and optimize ad campaigns</li>
        <!-- …8 items, em-dash separators via CSS between items … -->
      </ul>
    </div>
  </div>
</section>
```

- **Background:** brand gradient (`services-cta`), white text.
- **Order (top → bottom):** white eyebrow “When You Work With Us” → centered `h2` → **sync graphic** → body paragraph → dash-separated service list (centered, wraps horizontally).
- **Sync graphic:** sources column (8 platform logos + “Managed Channels / Focused on Google Ads”) → animated dots → ABM tile (`austin-becker-logo-icon-white.png`) → dots → Shopify dest (“Overall Sales Growth / More efficient / ad spend” on three lines).
- **Platform logos:** see **`website-logos.md`** (Reddit → `reddit-icon.png`).
- **No** intro subhead, pill bubbles, or side-by-side copy/graphic split (retired layout).

---

### 12. About Us block

**Location:** homepage `section--alt` with `split` grid.

```html
<section class="section section--alt">
  <div class="container split">
    <div>
      <h2>About Us</h2>
      <p>…</p>
      <div class="stats stats-inline">…</div>
      <div class="badge-row badge-row--about">…</div>
    </div>
    <div>
      <img class="about-photo" …>
    </div>
  </div>
</section>
```

- **Layout:** 50/50 split — copy + inline stats + partner badges left; team photo right.
- **Stats:** three inline metrics (UpWork, years, dollars managed).
- **Badges:** Google + Microsoft partner badges, left-aligned, link to partner profiles.
- **Photo:** full-width in column, rounded.

---

### 13. Case studies listing block

Used on `case-studies.html` and related hubs — card grid similar to carousel cards but static grid layout. Same `case-card` component: image, pill, title, result metric, excerpt, read-more link.

---

## Page assembly checklist

For a new informational page (services-style):

1. Standard `site-header` + megamenu
2. `services-page-hero` (title, grad tagline, offset photo)
3. `services-hub-section`:
   - `services-intro-split` (eyebrow + 1–2 paragraphs)
   - `services-platform-logos` (optional)
   - `services-hub-list` → `service-card` articles with anchor IDs
4. `pricing-section` (if pricing applies)
5. `cta-banner`
6. `#work-with-us` section (services, platforms, case studies, resources)
7. `site-footer`
8. Page-specific scripts (e.g. `pricing-carousel.js`)

---

## Files

| File | Purpose |
|------|---------|
| `services.html` | Primary reference — services + pricing |
| `supported-ad-platforms.html` | Platform hub — same shell, platform cards |
| `styles.css` | All component styles (~`.services-page-hero*`, `.service-card`, `.pricing-*`, etc.) |
| `scripts/pricing-carousel.js` | Pricing card dot navigation |
| `scripts/client-logos-autoscroll.js` | Slow auto-scroll for client logo box (home + about) |
| `scripts/sync_client_logos_grid.py` | Sync logo grid snippet → pages |
| `scripts/sync_case_studies_section.py` | Sync case study carousel → pages |
| `case_studies_section.py` | Case study carousel data + markup |
| `client_logos_grid.py` | Client logo grid data + markup |
| `site_nav.py` | Shared header, footer, megamenu |
| `resources.html` | Work With Us block reference |
| `client-logos.md` | Client logo grid standard + logo list |
| `website-logos.md` | Ad platform icon paths and usage |
| `snippets/client-logos-grid.html` | Canonical client logo slider markup |
| `index.html` | Homepage blocks (stat cards, client collage, What You Get, About) |

---

*Last updated: June 2026 — homepage What You Get, stat cards, client logo autoscroll, case study carousel sync, case study page layout.*
