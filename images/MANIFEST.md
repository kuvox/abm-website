# Image Manifest

Pulled from your live WordPress site (`abeckermarketing.com/wp-content/uploads/...`) on 2026-04-30. Originals — not the CDN-resized Optimole versions.

---

## In active use (39 images + 5 fonts)

### Branding
| File | Used in |
|------|---------|
| `logo.svg` | Header on every page (`brand-mark`) |
| `Inter-Regular.woff2` / `-Medium` / `-SemiBold` / `-Italic` / `-SemiBoldItalic` | Self-hosted body font (CSS `@font-face`) |

### Service icons (homepage cards)
| File | Service |
|------|---------|
| `google-shopping.svg` | Google Shopping Ads |
| `google.svg` | Google Search Ads / Display Network |
| `amazon.svg` | Amazon Ads |
| `microsoft.svg` | Microsoft Ads |
| `youtube.svg` | YouTube Ads |
| `cart-icon.svg` | Product Feeds |

### Case study photography
| File | Where |
|------|-------|
| `Hose-Warehouse.jpg` | HoseWarehouse case study (homepage + case-studies.html + service pages) |
| `Parker-Baby-Case-Study-Image.png` | Parker Baby case study |
| `iron-fence-shop.jpeg` | Iron Fence Shop case study |
| `datafeedwatch.jpg` | DataFeedWatch feature mention |

### People (headshots)
| File | Person |
|------|--------|
| `Austin-Becker-1.jpg` | Austin (founder) — about page |
| `austin-becker-portrait-3.jpg` | Austin headshot — circular variant |
| `Veronica-Garcia.jpg` | Team |
| `Kodi-Ekenta-scaled.jpg` | Team |

### Blog post / resource hero images
| File | Topic |
|------|-------|
| `2026-Product-Feed-Tutorial-light.png` | 2026 Shopify → Google Merchant Center feed setup |
| `Shopify-Conversion-Tracking-2025.png` | Shopify conversion tracking guide |
| `2_Successful_YouTube_Ad.png` | YouTube ad anatomy |
| `3_Display_Ads.png` | Display creative example |
| `Customer-Match-Lists.png` | Customer Match audiences |
| `Google-Ads-Customer-Match-Example-Statistics.png` | Customer Match stats |
| `1_Customer_Match_Lists.png` | Customer Match (smaller variant) |
| `4_Budgets_for_Paid_Ads.png` | Ad budgeting |
| `Weekly-Guides-on-YouTube.png` | YouTube channel promo |

### Badges
| File | What |
|------|------|
| `80756-2026-Partner-Program-Badge-Updates-LP-C2_Partner.png` | Google Partner Program 2026 badge |
| `Partner-RGB-1.png` | Partner badge (alt) |
| `google-premier-partner-badge.svg` | Google Premier Partner |

### Client logos (available for use)
- `beltsmart-logo.png`
- `hosewarhouse-logo.png`
- `mymusic-folders-logo.png`
- `tallslim-tees-logo.jpg`
- `the-crypto-lawyers-logo.png`
- `Kingsley-North.png`
- `parker-baby.png`

### Misc
- `image-21.png` (case-studies.html)
- `austin-becker-e-commerce-marketing-team-1-1.jpg`, `-team-2.jpg`, `-team-3.jpg` (team group shots)
- `trailheads.jpg` (case study spare)

---

## Spare alternates (not currently used — keep if you might want them)

These are alternate versions of photos already in use. ~1.5 MB total.

- `Parker-Baby-bag.jpeg` — alternate Parker Baby photo
- `austin-becker-e-commerce-marketing-7-1.jpg` — alt Austin/team photo
- `austin-becker-e-commerce-marketing-11.jpg` — alt
- `austin-becker-e-commerce-marketing-15.jpg` — alt
- `austin-becker-e-commerce-marketing-22.jpg` — alt
- `image-22.png` — generic
- `image-23.png` — generic

---

## Safe to delete (WordPress plugin UI cruft, ~1.4 MB)

These came from the WordPress theme/plugin assets and aren't useful in a static site:

- `bad_email.svg`, `good_email.svg` — Gravity Forms email-validation icons
- `checking_email.gif` — Gravity Forms validation spinner (458 KB)
- `gf-creditcards.svg`, `gf-creditcards-check.svg` — Gravity Forms payment UI
- `image.gif` — random 932 KB GIF (likely a theme decorative element)

To delete (in Terminal):
```bash
cd "~/Library/Mobile Documents/com~apple~CloudDocs/Ai/ABM Website/images"
rm bad_email.svg good_email.svg checking_email.gif gf-creditcards.svg gf-creditcards-check.svg image.gif
```

Or just delete them in Finder.

---

## Adding new images later

1. Drop the file into `images/`.
2. In your HTML, reference it as `<img src="images/your-file.jpg" alt="describe it">`.
   - From a service page, use `<img src="../images/your-file.jpg">` (the relative path goes up a directory).
3. Redeploy.

---

*Manifest generated 2026-04-30. 57 files in `images/` totaling ~12 MB.*
