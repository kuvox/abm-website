# Page patterns — abeckermarketing.com

This file documents the three distinct page types on the site so that anyone
(or any future AI assistant) can add new pages without re-inventing the layout.
**Always reuse the existing CSS classes in `styles.css` rather than introducing new ones.**

All three page types share the same `<header>` (mega-menu nav) and `<footer>`. The
canonical copy of each lives in `generate_pages.py` — when adding pages at scale,
prefer editing the data table in that script and re-running it.

```
python3 generate_pages.py
```

---

## 1. Main pages (homepage, about, contact)

**Status: keep as-is.** Do not restructure unless explicitly asked.

| Page          | File path           | Notes                                                                  |
| ------------- | ------------------- | ---------------------------------------------------------------------- |
| Home          | `index.html`        | Hero, services grid, testimonials, CTA banner.                         |
| About Us      | `about.html`        | Why-choose-us, founder bio, team grid. Sections anchored via `#`.      |
| Contact Us    | `contact.html`      | Two-column: contact details + lead form (Formspree placeholder today). |

The contact form fields are the canonical version of the lead form. Every case
study page embeds **the same field set** at the bottom so the visitor never has
to leave to talk to us.

---

## 2. Case study pages

**Location:** `case-studies/<client-slug>.html` (one file per client).
**URL shape:** `/case-studies/<client-slug>.html`.
**Generator:** `generate_pages.py`, in the `CASE_STUDIES` list.

### Required sections, in order

1. **`<section class="case-hero">` with `.hero-split`**
   - Left column: `.case-eyebrow` ("Case Study · {client name}"), `<h1>` (the headline result), and `<p class="case-intro">` with the 1–2 sentence client description.
   - Right column: `<img class="case-hero-image">` of the client.

2. **`<section class="case-body">` (prose, narrow container)**
   - `<h2>Challenge</h2>` — what the client was struggling with.
   - `<h2>Solution</h2>` — what we did at a high level.
   - Optional `<h2>What we did</h2>` — additional detail if needed.

3. **`<section class="case-results">` (alt background)**
   - `.results-eyebrow` + `<h2>What changed for {client}</h2>`.
   - `.metric-grid` containing 2 or 3 `.metric` cards. Each `.metric` has a `.metric-value` (the big number) and `.metric-label`.
   - Use `.metric-grid--three` when there are exactly 3 metrics.
   - `.client-quote` block: `<blockquote>` + `<cite>` with name and title.

4. **`<section class="case-contact section--alt">`**
   - Left column: "Want to work with us?" + contact details.
   - Right column: full contact form mirroring `contact.html`. Include a hidden `referrer` input set to the case-study slug so we can attribute leads.

### Required at top of file

```html
<link rel="canonical" href="https://abeckermarketing.com/case-studies/<slug>.html">
<meta name="description" content="...">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
```

Use the client's name in the page `<title>` as `"{Client} Case Study — Austin Becker E-Commerce Marketing"`.

### Adding a new case study

1. Open `generate_pages.py`.
2. Append a dict to the `CASE_STUDIES` list. Required keys: `slug`, `client`, `title`, `intro`, `hero_image`, `hero_alt`, `meta_description`, `challenge`, `solution`, `what_we_did` (list of paragraphs, may be empty), `metrics` (list of `(value, label)` tuples — 2 or 3 entries), `quote`, `quote_author`, `quote_title`.
3. Drop the hero image into `images/`.
4. Run `python3 generate_pages.py`.
5. Add a card on `case-studies.html` pointing at `case-studies/<slug>.html`.
6. Add the new URL to `sitemap.xml`.

---

## 3. Resources pages (articles)

**Location:** `resources/<slug>.html` (one file per article).
**URL shape:** `/resources/<slug>.html`.
**Generator:** `generate_pages.py`, in the `RESOURCES` list.

> **No table of contents** — the WordPress originals had one; on the static site
> we drop it. Anchor links from the side were rarely used and added clutter.

### Required sections, in order

1. **`<section class="article-hero">` (narrow container)**
   - `.article-meta` containing `.article-date`.
   - `.article-categories` containing one or more `<a class="pill-tag" href="../resources.html#<topic>">{topic}</a>` chips. Topic slugs follow the resources index: `amazon`, `google-ads`, `google-shopping`, `microsoft`, `product-feeds`, `youtube`, `research-articles`, `video-guides`.
   - `<h1>` — the article title.
   - `<p class="article-lead">` — one or two sentences describing what you'll get.
   - `.article-author` row with avatar + name + role.

2. **`<section class="article-feature-image">`**
   - One full-width hero image (16:9 aspect ratio enforced by CSS).

3. **`<section class="article-body">` (760px container)**
   - The article prose. Use `<h2>` for main sections and `<h3>` for subsections.
   - Use semantic HTML: `<p>`, `<ul>`, `<ol>`, `<blockquote>`, `<pre><code>`, `<figure>` with `<figcaption>`.
   - Optionally embed one or more **interactive tool blocks** (see section 4 below).
   - End with `.article-categories-footer` line: `Categories: <a>...</a>`.

4. **`<section class="article-related">` (alt background)**
   - `<h2>Related Resources</h2>` + a `.related-grid` of up to 3 `.related-card` links. The generator auto-picks related cards by overlapping category slugs.

### Adding a new resource

1. Open `generate_pages.py`.
2. Append a dict to the `RESOURCES` list. Required keys: `slug`, `title`, `lead`, `meta_description`, `date` (e.g. `"Feb 11, 2026"`), `feature_image`, `feature_alt`, `categories` (list of `(name, slug)` tuples), `body_html` (a string of HTML — keep it ≤ ~80% of the content; long pieces should link to Notion or YouTube), and optionally `video_embed` (a YouTube embed URL).
3. Drop the feature image into `images/`.
4. Run `python3 generate_pages.py`.
5. Add a card on `resources.html` pointing at `resources/<slug>.html`.
6. Add the new URL to `sitemap.xml`.

---

## 4. Embedding interactive tools inside resource pages

Resource articles support drop-in interactive widgets — budget estimators, ad
copy preview tools, ACoS / ROAS calculators, etc. Two patterns are supported.

### Pattern A — Inline self-contained block (preferred)

For small tools (calculators, picker UIs), drop a `<section class="interactive-tool">` into the article body. The CSS in `styles.css` handles the visual treatment. Example:

```html
<section class="interactive-tool" data-tool="budget-calculator" aria-labelledby="bc-title">
  <div class="tool-header">
    <span class="tool-eyebrow">Interactive Tool</span>
    <h3 id="bc-title">Ad Budget Calculator</h3>
    <p class="tool-sub">Enter desired revenue and required ROAS. We'll calculate the implied monthly ad budget.</p>
  </div>
  <div class="tool-body">
    <label for="bc-revenue">Desired Monthly Revenue</label>
    <input id="bc-revenue" type="number" min="0">
    <label for="bc-roas">Required ROAS (1.66 = 166%)</label>
    <input id="bc-roas" type="number" step="0.01">
    <button type="button" onclick="/* inline calc */">Calculate</button>
    <div id="bc-out" class="tool-result">
      <div class="tool-result-value">—</div>
      <p class="tool-result-label">Recommended monthly ad budget</p>
    </div>
  </div>
</section>
```

A working example is live in `resources/how-much-to-budget.html`. Vanilla JS only —
no frameworks, no external dependencies. Keeps the article page load light.

### Pattern B — Iframe-embedded tool (for bigger tools)

For tools that need their own routing, state, or larger code surface (e.g. an
ad copy preview tool that talks to an API), build the tool as a standalone HTML
file under `tools/<tool-name>.html` and embed it via:

```html
<section class="interactive-tool" data-tool="ad-copy-preview">
  <div class="tool-header">
    <span class="tool-eyebrow">Interactive Tool</span>
    <h3>Ad Copy Preview</h3>
  </div>
  <iframe src="../tools/ad-copy-preview.html" title="Ad copy preview" loading="lazy"></iframe>
</section>
```

Iframes are sandboxed by default — keep them on the same origin so resizing
and message-passing work. Sized via `min-height` in CSS (default 420px).

### Authoring new tools — checklist

- One file per tool: `tools/<tool-name>.html` (or inline if simple).
- Mobile-friendly: tools render inside an article column ~720px wide.
- Plain HTML/CSS/JS only — match the static-site philosophy.
- Avoid network calls. If a tool needs data, fetch from same-origin JSON.
- Add the tool name to the catalog at the bottom of this document.

### Tool catalog

| Tool                | Pattern | Lives in                                                | Used on                                            |
| ------------------- | ------- | ------------------------------------------------------- | -------------------------------------------------- |
| Ad Budget Calculator| Inline  | `resources/how-much-to-budget.html`                     | `resources/how-much-to-budget.html`                |
| Ad Copy Preview     | Future  | `tools/ad-copy-preview.html` _(not yet built)_         | TBD                                                |
| ACoS / ROAS toggler | Future  | TBD                                                     | TBD                                                |

---

## CSS classes used across these patterns

Defined in `styles.css`. Don't redefine; reuse.

**Layout helpers:** `.container`, `.section`, `.section--alt`, `.hero-split`, `.split`, `.center`, `.muted`, `.eyebrow`, `.lead`, `.btn`, `.btn-primary`.

**Case study pattern:** `.case-hero`, `.case-eyebrow`, `.case-intro`, `.case-hero-image`, `.case-body`, `.case-results`, `.results-eyebrow`, `.metric-grid`, `.metric-grid--three`, `.metric`, `.metric-value`, `.metric-label`, `.client-quote`, `.case-contact`, `.contact-info-block`, `.form-wrap`.

**Resource article pattern:** `.article-hero`, `.article-meta`, `.article-date`, `.article-categories`, `.article-lead`, `.article-author`, `.article-feature-image`, `.article-body`, `.article-categories-footer`, `.article-related`, `.related-grid`, `.related-card`, `.pill-tag`.

**Interactive tool pattern:** `.interactive-tool`, `.tool-header`, `.tool-eyebrow`, `.tool-sub`, `.tool-body`, `.tool-result`, `.tool-result-value`, `.tool-result-label`.
