# Client Logo Grid — Site Standard

The **canonical** client logo slider is generated from `client_logos_grid.py` into `snippets/client-logos-grid.html`. Run `python3 scripts/sync_client_logos_grid.py` after edits.

## Where it appears

| Page | Location |
|------|----------|
| `index.html` | “Our Clients” section (`section--clients-dark`) |
| `about.html` | About hero, right column (`about-hero-split`) |

## Markup

Copy the full block from `snippets/client-logos-grid.html` (the `<div class="client-collage-shell">` wrapper and everything inside it).

```html
<div class="client-collage-shell">
  <div class="client-collage-card client-collage-card--home" aria-label="Client logos">
    <div class="logo-item" tabindex="0">
      <img src="images/website-logos/website-client-logos/beltsmart-logo.png" alt="BeltSmart">
      <div class="logo-tooltip" role="tooltip">…</div>
    </div>
    <!-- …remaining logos… -->
  </div>
</div>
```

## Image paths

All client logo PNGs live in **`images/website-logos/website-client-logos/`**.

- **Root-level pages** (`index.html`, `about.html`): `images/website-logos/website-client-logos/beltsmart-logo.png`
- **Nested pages** (if logos are added later): `../images/website-logos/website-client-logos/beltsmart-logo.png`

## Current logos (16)

Regenerate markup from `client_logos_grid.py`:

```bash
python3 scripts/sync_client_logos_grid.py
```

**Featured (hover tooltip + link):** Hose Warehouse, MyMusic Folders, TallSlim Tees, Parker Baby, Kingsley North, Meseroll Shop, Indoor Cycle Pros, Poulsbo RV, Maia Homes, Conservation Mart, BeltSmart — in that order.

**Link only (grayscale → color on hover):** The Crypto Lawyers, Murdock Industrial, Irish Woodworks, Billfodl, Listing Mirror.

**Iron Fence Shop** is intentionally excluded from the logo grid (case study remains elsewhere).

## Adding or updating a client

1. Edit `FEATURED_CLIENTS` or `OTHER_CLIENTS` in `client_logos_grid.py`
2. Run `python3 scripts/sync_client_logos_grid.py`
3. Add the PNG to `images/website-logos/website-client-logos/` if new

## CSS

Styles in `styles.css`:

- `.client-collage-shell` — outer shadow wrapper
- `.client-collage-card` / `.client-collage-card--home` — 2-column scrollable grid
- `.logo-item` — linked logo tile (grayscale until hover)
- `.logo-tooltip-name` / `.logo-tooltip-tenure` / `.logo-tooltip-category` — hover info for featured clients (name + category: black; tenure: brand red — see **Tooltips** below)

## Tooltips

Featured clients show name, tenure, and category on hover. Other logos link out with color-on-hover only.

**Tooltip text colors** (white popup on the logo card — always use these, including on the homepage dark section where `.section--dark p` would otherwise force white text):

| Element | Class | Color |
|---------|-------|-------|
| Client name | `.logo-tooltip-name` | Black (`var(--ink)`, `#343536`) |
| Tenure | `.logo-tooltip-tenure` | Brand red (`var(--brand)`) — e.g. `6+ Year Client` |
| Category | `.logo-tooltip-category` | Muted dark (`var(--ink-soft)`, `#5a5a5a`) |

CSS uses `.logo-tooltip .logo-tooltip-*` selectors so these colors win over section-level dark-theme paragraph styles.
