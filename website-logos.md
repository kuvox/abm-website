# Website Logos — Ad Platforms & Brand Assets

Ad platform and site brand icons live in **`images/website-logos/`**. Client company logos live in **`images/website-logos/website-client-logos/`** (see `client-logos.md`).

## Ad platform icons (`images/website-logos/`)

Used on the services page, supported ad platforms page, homepage “What You Get” sync graphic, and service detail pages.

| Platform | File |
|----------|------|
| Google Ads | `google-logo.svg` |
| Google Merchant Center | `google-merchant-center-icon.png` |
| Microsoft Ads | `microsoft-ads-icon.png` |
| Facebook | `facebook-icon.png` |
| Instagram | `instagram-icon.png` |
| YouTube | `youtube-icon.png` |
| Pinterest | `pinterest-red-icon.png` (light backgrounds) / `pinterest-white-icon.png` (dark) |
| ChatGPT | `chatgpt-black-icon.png` (light) / `chatgpt-white-icon.png` (dark) |
| Target | `target-icon.png` |
| eBay | `ebay-icon.png` |
| Shopify | `shopify-icon.png` |
| Amazon | `amazon-logo-icon.png` |
| Meta | `meta-icon.png` |
| TikTok | `tiktok-icon.png` |
| X (Twitter) | `x-black-icon.png` / `x-white-icon.png` |
| Reddit | `reddit-icon.png` |

Partner badges (Google Premier, Microsoft Partner) remain in `images/` root (`Partner-RGB-1.png`, etc.) — not in `website-logos/`.

**Homepage sync tile (not in `website-logos/`):** `images/austin-becker-logo-icon-white.png`

## Path conventions

- **Root-level pages:** `images/website-logos/facebook-icon.png`
- **Nested pages:** `../images/website-logos/facebook-icon.png`

## Homepage “What You Get” sync graphic

Sources column (`sync-logo--platforms`):

- Google Ads → `google-logo.svg`
- Microsoft Ads → `microsoft-ads-icon.png`
- Google Merchant Center → `google-merchant-center-icon.png`
- Facebook → `facebook-icon.png`
- Instagram → `instagram-icon.png`
- ChatGPT → `chatgpt-black-icon.png`
- Reddit → `reddit-icon.png`
- Pinterest → `pinterest-red-icon.png`

Middle tile (ABM): `images/austin-becker-logo-icon-white.png` in `.sync-tile-icon`

Destination column: Shopify → `shopify-icon.png`

**Captions (sources):** Managed Channels / Focused on Google Ads  
**Captions (dest):** Overall Sales Growth / More efficient + line break + ad spend

## Footer logo

`ABHorizontalWhiteDigital.png` → `images/website-logos/ABHorizontalWhiteDigital.png`

## Adding a new ad platform icon

1. Add PNG/SVG to `images/website-logos/`
2. Update `services.html`, `supported-ad-platforms.html`, and any other pages that list platforms
3. Update this file
