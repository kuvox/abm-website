# Feed demo & shopping ad design preferences

Reference for the interactive demo on `guides/product-data-feeds-as-keywords.html`. Captures layout, typography, colors, and interaction decisions — especially areas we iterated on repeatedly.

**Key files:** `guides/product-data-feeds-as-keywords.html`, `scripts/feed-keyword-matcher.js`, `styles.css` (`.feed-demo-showcase` section)

---

## Overall layout

- **Full-bleed showcase** breaks out of the article column (`width: 100vw` with centering hack).
- **Dark outer shell** with subtle grid (`#0d1b2a` + 32px white grid lines at 4% opacity) — ACP / Google Ads demo aesthetic.
- **Light inner stage** (`#f5f5f5`) holds the interactive canvas; tabs connect visually (active tab shares the stage background).
- **Three columns:** sample searches → product feed data → shopping ads, with dashed arrow connectors between them (hidden below 900px).
- **Header copy on dark background must be white** — see `.cursor/rules/dark-background-text.mdc`. Do not reuse `var(--ink)` or `var(--ink-soft)` on dark panels without a light override.

---

## Colors

| Role | Value | Notes |
|------|-------|-------|
| Brand / match highlight | `var(--brand)` → `#e84f3b` | Active query border, matched feed field left border, matched shopping ad border |
| Showcase background | `#0d1b2a` | Dark grid shell |
| Demo stage | `#f5f5f5` | Light gray canvas |
| Feed panel | `#111` | Dark “merchant center” window |
| Feed field default | `#1a1a1a` bg, `#2a2a2a` border | |
| Feed field matched | `#1f1514` bg, brand left border | Warm red tint |
| Feed field mismatch | `#1f1a10` bg, `#e6a817` accent | Amber warning |
| Feed field labels | Monospace, `#7a7a7a` | Matched: `#f08a7a`; mismatch: `#e6a817` |
| Feed field values | White on dark panel | |
| Shopping ad card | `#fff` bg, `#e5e7eb` border | |
| Shopping ad title/price/brand | `#111827` | |
| Shopping ad subtitle | `#6b7280` | |
| SVG placeholder image area | `#e8eaed` | Google Shopping–style gray |
| Photo image area | `#fff` | Matches PNG white padding |
| AI Overview header (active) | `#5b21b6` | Purple, Google AI Overview nod |
| AI Overview body | `#111827` | |
| Active sample search | `#fff0ee` bg, brand border | |

---

## Typography

### Section labels (column headers, eyebrows)

- Uppercase, `0.72rem`, `font-weight: 700`, `letter-spacing: 0.08em`, `var(--ink-soft)` on light stage.

### Shopping ad card text

**Important:** Shopping tiles live inside `.article-body`, which applies large paragraph styles (`font-size: 1.0625rem`, `line-height: 1.7`, `margin-bottom: 1.1rem`). Always scope tile typography under `.feed-demo-showcase` and reset margins on `.feed-shopping-tile-body p`.

| Element | Size | Weight | Line-height | Color |
|---------|------|--------|-------------|-------|
| Title | **13px** | 600 | **1.3** | `#111827` |
| Subtitle | **12px** | 400 | 1.3 | `#6b7280` |
| Price | **12px** | 500 | 1.3 | `#111827` |
| Brand | **12px** | 500 | 1.3 | `#111827` |
| Footer (arrival / Used) | **12px** | 500 | 1.3 | `#111827` |

**Typography lessons (do not repeat mistakes):**

- Do **not** go below ~12px for detail lines — 8–10px caused overlapping, clipped text.
- Use **`line-height: 1.3`** minimum on small tile text — `1.1` caused lines to sit on top of each other.
- Use **flex column** with `gap: 3px` for the tile body — **not CSS grid** with a `minmax(0, 1fr)` spacer (that caused clipping).
- Title: `-webkit-line-clamp: 2` with `max-height: calc(13px * 1.3 * 2)`.
- Price, brand, subtitle, footer: single line with `text-overflow: ellipsis`.

### AI Overview text

- **12px**, `line-height: 1.5`, `#111827`.
- Full column width with **8px horizontal padding** only — no card/box around it.

---

## Shopping ad cards

### Dimensions & structure

- Card: **175px × 300px**, `border-radius: 12px`.
- Body padding: `8px 9px 9px`.
- Text rows (top to bottom): title → subtitle (optional) → price → brand → footer (`margin-top: auto`).
- Footer: **“Arrives by M/D”** for new items, **“Used”** for used items (`tile.used: true`).
- **Do not show `price` in the center feed field list** — price belongs on the shopping ad only.

### Product images

**This was iterated heavily — follow exactly:**

1. **No zoom, no crop** of product PNGs. The images have built-in white padding around the product; that padding is intentional and must remain visible.
2. Photo tiles (`.png`): use a **square media area** (`175px × 175px`) because source images are square (1600×1600).
3. `object-fit: contain`, `object-position: center`, white background (`#fff`).
4. **Do not** use `transform: scale()` to “fill” the frame — user rejected this.
5. **Do not** use `object-fit: cover` on photo PNGs — it crops the image.
6. SVG placeholders (apparel/industrial): **136px** tall gray area, `object-fit: cover` is fine.

### Stacked deck interaction

Cards are **absolutely positioned** in a stack, not a vertical list with gap.

**Idle (no search):** staggered vertically behind each other:

| Position | Transform | z-index | Opacity |
|----------|-----------|---------|---------|
| 1st card | `translate(0, 0) scale(1)` | 3 | 1 |
| 2nd card | `translate(0, 16px) scale(0.985)` | 2 | 0.9 |
| 3rd card | `translate(0, 32px) scale(0.97)` | 1 | 0.82 |

**On match:** winning card animates to front (`translate(0, 0) scale(1.03)`, brand border, full opacity, `z-index: 10`). Non-winners sit **directly below** (`translate(0, 28px)`, opacity 0.45) — vertical offset only, not diagonal.

- Container `min-height` must account for stack offset (~348px for 3 cards).
- Transition: `transform 0.4s cubic-bezier(0.34, 1.15, 0.64, 1)` (light spring).
- Respect `prefers-reduced-motion` — shorten/disable transform animation.

---

## AI Overview block

- Placed **above** the shopping ad cards (under the “Shopping ads” header) — not below.
- **No white box**, border, or shadow. Sits on the light stage background.
- **Inactive by default:** container `opacity: 0.4`, answer text hidden.
- **Active only** when the fitment query is selected (see automotive scenario below).
- Header always visible; answer paragraph appears only when active.

---

## Feed data panel (automotive)

### Fields shown

Include only keys present in the scenario `feed` object (do not render empty rows).

Automotive feed attributes:

- `product_type`
- `title`
- `mpn`
- `condition` ← **keep**
- `question_and_answer`
- ~~`availability`~~ ← **removed** to reduce panel height
- ~~`price`~~ ← never in feed panel

### Empty state

Placeholder: *“To preview relevant product data, click a keyword or shopping ad.”* — white text on dark panel.

### Removed UI

- **No black match-note box** in the bottom-left query panel. Explanations like *“DKV10R in product_type…”* were removed — the feed highlighting and shopping ad animation carry the demo.

---

## Automotive sample data

### Center feed (featured SKU)

- **product_type:** `automotive > replacement parts > subaru > impreza > DKV10R`
- **title:** `A/C Compressor - 2015-2019 Subaru WRX STI 2.5L H4`
- **mpn:** `129872-03724743`
- **condition:** `new`
- **question_and_answer:** 2014 Impreza fit question (feeds AI Overview / fitment story)

### Shopping ad tiles (3 cards)

| ID | Title | Price | Brand | Image | Footer |
|----|-------|-------|-------|-------|--------|
| `compressor-new` | A/C Compressor - 2015-2019 Subaru WRX STI 2.5L H4 | $168.95 | Premium Autoparts | `subaru-compressor-new.png` | Arrives by 5/4 |
| `compressor-used` | Used Compressor - 2015 Subaru WRX STI | $75.00 | Autoparts Resale | `subaru-compressor-used.png` | Used |
| `compressor-2002` | 2002 Subaru WRX A/C Compressor | $122.50 | Classic Parts | `subaru-compressor-2002.png` | Arrives by 5/25 |

### Sample searches (automotive)

| Query text | Purpose |
|------------|---------|
| `dkv10r compressor` | Basic product_type + title match → new compressor ad |
| `used dkv10r subaru ac` | “used” steers to resale listing |
| `subaru air compressor` | Generic Subaru + compressor match |
| `129872-03724743` | MPN exact match |
| `compressor with clutch 2014 impreza` | title + product_type + question_and_answer |
| `does a DKV10R compressor fit subaru 2002 wrx` | **AI Overview query** — activates AI block; highlights feed fields; **2002 WRX ad wins** in shopping stack |

### AI Overview copy (fitment query only)

> No, the DKV10R compressor will not fit a 2002 Subaru WRX. The DKV10R (often associated with Zexel/Valeo) is primarily designed for later-generation Subaru models (typically 2007–2014 Impreza, WRX, and Forester models equipped with 2.5L engines).

**Demo narrative:** Feed panel shows the DKV10R SKU data, AI Overview explains it doesn’t fit a 2002 WRX, but the **2002 WRX compressor shopping ad** comes to the front — illustrating how feed attributes power different surfaces (AI answers vs. ad eligibility).

### Removed / rejected

- ~~`used subaru air conditioning compressor`~~ as a sample search with condition-mismatch note — removed with the match-note box.
- ~~Condition mismatch callout~~ (“search says used while condition is new”) — removed.

---

## Interaction patterns

- **Reset** clears search, feed placeholder, tile highlights, and AI Overview.
- **Tab scenarios:** Automotive (default), Apparel, Industrial Parts — each with own feed, queries, and tiles.
- **Click sample search** → highlights feed fields, animates shopping ad winner, optionally activates AI Overview.
- **Click shopping ad** → runs first qualifying sample search for that tile (`previewSearch` fallback when no query wins).
- **Type in search box** → token inference or exact query match.
- Reverse-click on used tile uses `previewSearch: 'used subaru air conditioning compressor'`.
- Reverse-click on 2002 tile uses `previewSearch: 'does a DKV10R compressor fit subaru 2002 wrx'`.

---

## Quick checklist before changing the demo

- [ ] Tile text readable at 12–13px with `line-height: 1.3`?
- [ ] `.feed-demo-showcase` scoping overrides `.article-body p` styles?
- [ ] Product PNGs shown in full with `object-fit: contain` (no zoom)?
- [ ] White text on all dark backgrounds?
- [ ] AI Overview only activates on the fitment query?
- [ ] No match-note explanation box in the query panel?
- [ ] Automotive feed has `condition` but not `availability`?
- [ ] Stacked cards animate to front/back positions without diagonal offset on match?
