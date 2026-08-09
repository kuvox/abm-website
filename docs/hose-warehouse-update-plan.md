# Plan v2: Update + visually reformat the Hose Warehouse / Murdock Industrial case study

**This supersedes v1 of this document entirely.** Same page, same pipeline rules, but v2 adds a visual formatting system (inspired by savvyrevenue.com/cases/rito/) that breaks the page into distinct visual blocks, revises the quote callout layout, and changes one sidebar string.

**Target page:** `case-studies/hose-warehouse-beltsmart.html` (URL unchanged)

**What we're borrowing from the competitor reference (savvyrevenue.com/cases/rito/):** they never show more than ~3 short paragraphs without a visual break. Their tools: small colored kicker labels above every section ("Marathon #1", "Overview", "Key Projects"), each solution phase packaged as a self-contained repeating block, quote cards interleaved between sections, and rounded panels that change the background to signal "new section." We're adapting those ideas to ABM's existing brand (red #e84f3b, white, Inter) — not copying their design.

**The visual rhythm we're building, top to bottom:**

1. Hero (unchanged) → 2. Compact quote callout card (Tony, logo right) → 3. **01 / Challenge** — kicker + short prose → 4. **02 / Solution** — kicker + one intro paragraph → 5. **Three numbered step cards** (the solution subsections, each visually cordoned off in its own bordered card with a numbered chip) → 6. **03 / The result** — a brand-tinted tie-off panel that closes the story → 7. pager/reviews/CTA (unchanged).

---

## Ground rules (unchanged from v1 — read before touching anything)

1. **`generate_pages.py` is the source of truth.** Do NOT hand-edit `case-studies/hose-warehouse-beltsmart.html`. Edit the data + template in `generate_pages.py`, then regenerate. (See `docs/PAGE_PATTERNS.md` §2.)
2. **Reuse existing CSS classes** wherever possible; new classes go in `styles.css` (one file, no new stylesheets).
3. **Python 3.12+ is required** to run `generate_pages.py` (f-string syntax invalid in ≤3.11, ~line 1118). On Austin's Mac `python3` is 3.12. In a cloud sandbox, call `python3.12` explicitly.
4. **Regenerate ONLY this one page** (command in Step 6). Do not run the full `generate_pages.py`.
5. Do not change: the H1, the hero intro paragraph, the hero image, the metric card values (181.92% / 10.65%), the pager, the Google-reviews section, or anything on other pages.

---

## Step 1 — Fix generator drift (REQUIRED before regenerating)

The live case-study HTML files contain two things the generator does not emit. If you regenerate without this fix, they get silently dropped.

In `generate_pages.py`, inside `render_case_study()` (starts ~line 285):

**1a.** In the returned HTML template, after this line:

```html
<meta property="og:image" content="https://abeckermarketing.com/{cs['hero_image'].lstrip('/')}">
```

add:

```html
<meta property="article:modified_time" content="{_TODAY}">
```

**1b.** In the same template, just before `</body>`, after the existing line:

```html
<script src="{rel}scripts/hero-grid-interactive.js" defer></script>
```

add:

```html
<script src="{rel}scripts/site-nav.js" defer></script>
```

---

## Step 2 — Add the featured quote callout component (v2 layout)

Compact card. Quote text left-aligned. Attribution is a single row: Tony's name + title on the left, **Murdock Industrial logo on the right, sized larger** (52px tall) since it now sits beside the name instead of stacking above it.

### 2a. New helper in `generate_pages.py`

Add next to `_case_body_sidebar_metrics_html()` (~line 264):

```python
def _case_quote_callout_html(cs: dict, rel: str) -> str:
    """Featured client quote banner, rendered under the hero when quote_featured is set."""
    if not (cs.get("quote_featured") and cs.get("quote")):
        return ""
    logo_html = ""
    if cs.get("quote_logo"):
        logo_html = (
            f'        <img src="{rel}{cs["quote_logo"]}" alt="{cs.get("quote_logo_alt", "")}"'
            ' class="case-quote-callout__logo" loading="lazy">\n'
        )
    return f"""<section class="case-quote-callout" aria-label="Client quote">
  <div class="container">
    <figure class="case-quote-callout__card">
      <span class="case-quote-callout__mark" aria-hidden="true">&ldquo;</span>
      <blockquote class="case-quote-callout__text">{cs['quote']}</blockquote>
      <figcaption class="case-quote-callout__attribution">
        <span class="case-quote-callout__who">
          <span class="case-quote-callout__name">{cs['quote_author']}</span>
          <span class="case-quote-callout__role">{cs['quote_title']}</span>
        </span>
{logo_html}      </figcaption>
    </figure>
  </div>
</section>

"""
```

### 2b. Hook it into the page template

In `render_case_study()`'s returned template, the hero section currently ends like this:

```
</section>

{case_body_section_html}
```

Change it to:

```
</section>

{_case_quote_callout_html(cs, rel)}{case_body_section_html}
```

(Pages without `quote_featured` render exactly as before — the helper returns `""`.)

### 2c. Quote callout CSS in `styles.css`

Add directly after the `.case-hero-caption` rules (~line 3082), before the `.case-body` block:

```css
/* Featured client quote callout (case study pages) */
.case-quote-callout { padding: 0 0 1rem; }
.case-quote-callout .container { max-width: 880px; }
.case-quote-callout__card {
  position: relative;
  margin: 0;
  padding: 30px 36px 24px;
  background: linear-gradient(135deg, var(--brand-tint) 0%, #fff 78%);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}
.case-quote-callout__card::before {
  content: "";
  position: absolute;
  inset: 0 0 auto 0;
  height: 4px;
  background: linear-gradient(90deg, var(--brand), #f0907f);
}
.case-quote-callout__mark {
  position: absolute;
  top: 2px;
  left: 16px;
  font-size: 5.5rem;
  line-height: 1;
  font-weight: 800;
  color: var(--brand);
  opacity: 0.12;
  pointer-events: none;
}
.case-quote-callout__text {
  margin: 0 0 18px;
  padding: 0 0 0 34px;
  border: 0;
  font-size: clamp(1.05rem, 1.8vw, 1.25rem);
  line-height: 1.5;
  font-weight: 600;
  color: var(--ink);
}
.case-quote-callout__attribution {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding-left: 34px;
}
.case-quote-callout__who {
  display: flex;
  flex-direction: column;
  gap: 1px;
}
.case-quote-callout__name {
  font-weight: 700;
  color: var(--ink);
  font-size: 0.98rem;
}
.case-quote-callout__role {
  color: var(--ink-soft);
  font-size: 0.9rem;
}
.case-quote-callout__logo {
  height: 52px;
  width: auto;
  border-radius: 8px;
  flex-shrink: 0;
}
@media (max-width: 560px) {
  .case-quote-callout__card { padding: 24px 18px 20px; }
  .case-quote-callout__mark { font-size: 4rem; left: 8px; }
  .case-quote-callout__text { padding-left: 0; }
  .case-quote-callout__attribution { padding-left: 0; }
  .case-quote-callout__logo { height: 40px; }
}
```

---

## Step 3 — Add the section-breaking CSS system

Three new patterns, all page-scoped via classes used only in this case study's `body_html` (other case studies unaffected). Add all of this to `styles.css` right after the existing `.case-body p` rule (~line 3157).

### 3a. Numbered section kickers (01 / 02 / 03 above the H2s)

```css
/* Case study section kickers — numbered eyebrow + short rule above H2s */
.case-sec-kicker {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 2.6rem;
  color: var(--brand);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.14em;
}
.case-sec-kicker::after {
  content: "";
  flex: 0 0 34px;
  height: 2px;
  background: var(--brand);
  opacity: 0.35;
  border-radius: 1px;
}
.case-sec-kicker:first-child { margin-top: 0; }
.case-sec-kicker + h2 { margin-top: 0.35rem; }
```

### 3b. Solution step cards (the three subsections, each cordoned off)

```css
/* Solution step cards — each solution subsection in its own bordered card */
.case-steps {
  display: grid;
  gap: 14px;
  margin: 1.6rem 0 0.6rem;
}
.case-step {
  display: grid;
  grid-template-columns: 44px 1fr;
  gap: 16px;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  padding: 22px 26px 18px;
  box-shadow: 0 6px 18px rgba(20, 20, 20, 0.05);
}
.case-step__num {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--brand-tint);
  color: var(--brand);
  font-weight: 800;
  font-size: 1.05rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.case-step__body h3 {
  margin: 0.35rem 0 0.55rem;
  font-size: 1.15rem;
  line-height: 1.3;
}
.case-step__body p {
  font-size: 1rem;
  margin-bottom: 0.9rem;
}
.case-step__body p:last-child { margin-bottom: 0; }
@media (max-width: 560px) {
  .case-step { grid-template-columns: 1fr; padding: 18px 18px 16px; }
  .case-step__num { width: 34px; height: 34px; font-size: 0.95rem; }
}
```

### 3c. Result tie-off panel (brand-tinted closing block)

```css
/* Result tie-off panel — tinted closing block for case studies */
.case-result-panel {
  background: var(--brand-tint);
  border-radius: var(--radius-lg);
  padding: 26px 30px 22px;
  margin-top: 2.6rem;
}
.case-result-panel .case-sec-kicker { margin-top: 0; }
.case-result-panel h2 { margin: 0.35rem 0 0.8rem; }
.case-result-panel p:last-child { margin-bottom: 0; }
```

Note: v1 of this plan had a standalone `.case-body h3` rule — it is no longer needed (the only H3s now live inside `.case-step__body`, which has its own rule). Don't add it.

---

## Step 4 — Replace the case study's content in `generate_pages.py`

Find the `hose-warehouse-beltsmart` dict in `CASE_STUDIES` (~lines 86–109). Replace the **whole dict** with:

```python
    {
        "slug": "hose-warehouse-beltsmart",  # already exists; re-generated for consistency
        "client": "Murdock Industrial",
        "title": "181.92% Year-Over-Year Increase in Revenue From Google Ads",
        "intro": "HoseWarehouse.com and BeltSmart.com sell industrial hose, tools and accessories at wholesale prices in the USA. Both are subsidiaries of Murdock Industrial based in Akron, Ohio.",
        "hero_image": "images/Hose-Warehouse.jpg",
        "hero_alt": "Hose Warehouse Google Ads success case study",
        "meta_description": "A product data feed audit across 100,000+ SKUs plus weekly shopping ad optimization grew Murdock Industrial's Google Ads revenue 181.92% year-over-year.",
        "challenge": "",
        "solution": "",
        "what_we_did": [],
        "body_html": """    <span class="case-sec-kicker" aria-hidden="true">01</span>
    <h2>Challenge</h2>
    <p>Professionals in the hose and accessories market search for replacement parts and materials with all sorts of searches: part numbers, colloquial terminology and nicknames for types of equipment, and brand and manufacturer searches. Being found with any of these disparate types of searches is difficult in Google Shopping Ads, which only display 70 to 150 characters in product ad titles.</p>

    <span class="case-sec-kicker" aria-hidden="true">02</span>
    <h2>Solution</h2>
    <p>Tony at Murdock Industrial requested a product data feed audit and optimization from Austin and his team in 2019. After optimizing product data across Tony&rsquo;s 100,000+ SKU catalog, Austin&rsquo;s team began optimizing shopping ad campaigns to ensure that Murdock Industrial&rsquo;s paid ads appeared on part number, colloquial, brand and other relevant searches across Google and Microsoft Ads (Bing, Yahoo, DuckDuckGo, and more).</p>

    <div class="case-steps">
      <section class="case-step">
        <span class="case-step__num" aria-hidden="true">1</span>
        <div class="case-step__body">
          <h3>Increased inventory approval in Merchant Center</h3>
          <p>With an optimized product data feed, item approval rates in Google and Microsoft Ads increased immediately, meaning more inventory than ever was finally eligible to show ads in Google and Microsoft. A higher percentage of approved items in Merchant Center is the single most predictable indicator of increased sales: more eligible products in ads leads to more clicks, leads to more sales &mdash; all without raising ad budgets. It&rsquo;s a budget-free way to boost sales from shopping ads.</p>
        </div>
      </section>
      <section class="case-step">
        <span class="case-step__num" aria-hidden="true">2</span>
        <div class="case-step__body">
          <h3>Increased specificity in search targeting</h3>
          <p>With a more advanced product data feed setup, Austin and his team increased the number of eligible (and relevant) searches that Murdock Industrial could bid on at auction in Google.</p>
          <p>Increasing the volume of eligible searches has a direct impact on clicks, but not necessarily on sales. So to ensure that more clicks led to more sales (not just more spend), Austin adjusted campaigns weekly until Murdock Industrial&rsquo;s Google Ads campaigns stopped bidding on irrelevant and non-commercial adjacent searches.</p>
        </div>
      </section>
      <section class="case-step">
        <span class="case-step__num" aria-hidden="true">3</span>
        <div class="case-step__body">
          <h3>Accurate shipping timelines and rates</h3>
          <p>Google Shopping displays the total cost of an item to customers, meaning that shipping costs are calculated and displayed in shopping ads. Austin revised all of Murdock Industrial&rsquo;s shipping policies in Google Merchant Center to avoid over-quoting the shipping rate that any USA-based customer viewed in ads. This effectively lowered the prices seen by shoppers in Murdock Industrial&rsquo;s ads.</p>
          <p>Since price is one of the biggest drivers of clicks in Shopping Ads, a lower advertised price leads to more clicks. More clicks lead to more sales, further boosting Murdock Industrial&rsquo;s sales growth from paid ads.</p>
        </div>
      </section>
    </div>

    <div class="case-result-panel">
      <span class="case-sec-kicker" aria-hidden="true">03</span>
      <h2>The result</h2>
      <p>Without sharing actual sales volumes, ROAS, or other proprietary data, we can share that Murdock Industrial&rsquo;s sales were quickly pushed up, while ad costs grew at a far slower pace &mdash; meaning more profit month after month.</p>
      <p>More importantly, Murdock Industrial&rsquo;s trend of high sales growth alongside modest ad budget growth has continued for years, freeing up Tony and his team to invest in additional business objectives, continually growing the entire business&rsquo;s revenue year after year.</p>
    </div>""",
        "metrics": [
            ("181.92%", "year-over-year increase in revenue from Google Ads"),
            ("10.65%", "increase in paid search conversion rate"),
        ],
        "body_sidebar_intro": "Year-over-year on Google Ads",
        "body_sidebar_foot": "Across Hose Warehouse and Murdock Industrial.",
        "quote": "We&rsquo;ve grown every quarter and every year since working with Austin. His weekly campaign optimizations, ongoing data feed work, and ad tracking tech all help us continue growing.",
        "quote_author": "Tony Price",
        "quote_title": "Owner &amp; CEO, Murdock Industrial",
        "quote_featured": True,
        "quote_logo": "images/website-logos/website-client-logos/murdock-industrial-logo.png",
        "quote_logo_alt": "Murdock Industrial logo",
    },
```

Changes vs v1 of this plan: `body_sidebar_foot` now reads "Across Hose Warehouse and Murdock Industrial." (was "…and BeltSmart."), and `body_html` now uses the kicker/step-card/result-panel markup.

The logo file exists at `images/website-logos/website-client-logos/murdock-industrial-logo.png` (2000×1000, light background — fine on the light card at 52px tall).

---

## Step 5 — (No changes) Things that stay as-is

- `case_studies_section.py` — homepage/index card unchanged. Nothing to sync.
- `schema/jsonld.py` — no changes.
- H1, hero image, metric card values, pager order, reviews, footer.

---

## Step 6 — Regenerate the one page

From the site root (`ABM Website/`), with Python **3.12+**:

```bash
python3 - <<'EOF'
from pathlib import Path
from generate_pages import CASE_STUDIES, render_case_study
cs = next(c for c in CASE_STUDIES if c["slug"] == "hose-warehouse-beltsmart")
Path("case-studies/hose-warehouse-beltsmart.html").write_text(render_case_study(cs))
print("regenerated hose-warehouse-beltsmart.html")
EOF
```

(If `python3 --version` reports < 3.12, use `python3.12`. Do NOT run the full `python3 generate_pages.py`.)

---

## Step 7 — Bump sitemap lastmod

In `sitemap.xml`, find the `<url>` entry for `https://abeckermarketing.com/case-studies/hose-warehouse-beltsmart.html` and set its `<lastmod>` to today's date (currently `2026-07-15`).

---

## Step 8 — Optional (nice-to-have, skip if unsure)

1. `llms.txt` line ~26: update the case-study blurb, e.g. `181.92% year-over-year Google Ads revenue growth from a product data feed audit across a 100,000+ SKU catalog and weekly shopping ad optimization on Google and Microsoft Ads.`
2. `docs/PAGE_PATTERNS.md` §2: document the new reusable patterns — generator keys `quote_featured`, `quote_logo`, `quote_logo_alt`, and CSS classes `.case-quote-callout`, `.case-sec-kicker`, `.case-steps` / `.case-step`, `.case-result-panel` — so future case studies can use the same visual system.
3. **Fact chips under the hero eyebrow** (borrowed from the competitor's hero): a small row of pill badges like `Client since 2019 · 100,000+ SKUs · Google + Microsoft Ads`. Only do this if Austin asks — it needs a new component and template hook.

---

## Step 9 — Verification checklist (do all of these)

1. `git diff case-studies/hose-warehouse-beltsmart.html` — expected changes ONLY:
   - new `article:modified_time` meta (today) and `dateModified` in JSON-LD (today)
   - new `meta name="description"` / `og:description` / schema description text
   - new `.case-quote-callout` section between the hero and `.case-body`
   - new body content with kickers, `.case-steps` cards, and `.case-result-panel`
   - sidebar footnote now "Across Hose Warehouse and Murdock Industrial."
   - `<script src="../scripts/site-nav.js" defer></script>` still present at the bottom
   - Everything else (header/megamenu, hero, metric card values, pager, reviews, footer) byte-identical.
2. `git status` — confirm NO other case-study or resource HTML files changed.
3. Open the page in a browser (`python3 -m http.server` from site root):
   - Quote callout under the hero: compact card, quote text, then one row with "Tony Price / Owner & CEO, Murdock Industrial" on the left and the Murdock logo (~52px tall) on the right.
   - "01 —" kicker above Challenge, "02 —" above Solution, "03 —" above The result.
   - Three white bordered step cards with numbered circles 1/2/3, visually distinct from surrounding prose.
   - The result section sits in a pale-red tinted panel.
   - Sidebar metric cards unchanged (181.92%, 10.65%); footnote reads "Across Hose Warehouse and Murdock Industrial."
   - Check at ~375px wide: cards stack cleanly, number chips shrink, quote logo drops to 40px, nothing overflows.
4. Check the Kingsley North case study page renders unchanged (it shares `.case-body` CSS; none of the new classes should affect it).
5. Paste the page's JSON-LD into validator.schema.org — zero errors.
6. Do NOT commit/deploy — leave changes for Austin to review.

---

## Copy edits applied to Austin's draft (flag to Austin if any look wrong)

- "With optimized product data feed" → "With **an** optimized product data feed"
- "Austin and his team **to increased**" → "Austin and his team **increased**"
- "more clicks led to more **sales sales**" → "more sales"
- "And so to ensure" → "So to ensure"
- "Google Shopping **display** the total cost" → "**displays**"
- "More clicks **leads** to more sales" (shipping section) → "**lead**"
- "trends of 1) high sales growth alongside 2) modest ad budget growth, has continued" → "trend of high sales growth alongside modest ad budget growth has continued"
- Em dashes and curly apostrophes converted to house-style HTML entities (`&mdash;`, `&rsquo;`)
- Quote attributed to "Tony Price, Owner & CEO, Murdock Industrial" (name/title already in the repo's data; the draft just said "Tony")
- Per Austin: sidebar footnote says "Hose Warehouse and Murdock Industrial" (BeltSmart removed), even though the page intro still describes both stores.
