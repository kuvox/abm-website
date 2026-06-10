# Austin Becker E-Commerce Marketing — Brand Guide

## Color palette

### Primary

| Role | HEX | RGB | CMYK |
|------|-----|-----|------|
| Coral Red (signature accent) | `#E74D3B` | R233 G78 B59 | C3 M85 Y83 K0 |
| Near-Black (text / dark) | `#292E30` | R41 G46 B47 | C74 M64 Y62 K62 |

### Secondary

| Role | HEX | RGB | CMYK |
|------|-----|-----|------|
| Pale Blue (soft background) | `#DCEAEF` | R221 G233 B239 | C12 M3 Y3 K0 |
| Blue-Gray (muted accent) | `#A4BCC5` | R162 G187 B196 | C37 M17 Y18 K0 |
| White (base background) | `#FFFFFF` | R255 G255 B255 | C0 M0 Y0 K0 |

### Usage

- **Coral Red `#E74D3B`** — accent only: calls to action, links, highlights. Make it pop, not dominate.
- **Near-Black `#292E30`** — body text, headings, dark surfaces. Avoid pure black.
- **Secondary tones** — section backgrounds, cards, dividers, supporting graphics.
- **White `#FFFFFF`** — default page background.

## Fonts

- **Gilroy** — headings & display text
- **Astoria** — body & paragraph text

Web/print fallback when unavailable: a clean geometric sans-serif (Montserrat, Poppins) or system sans-serif.

## CSS variables (drop-in)

```css
:root {
  /* Primary */
  --brand:        #E74D3B; /* coral red — signature accent */
  --ink:          #292E30; /* near-black — text / dark */

  /* Secondary */
  --brand-pale:   #DCEAEF; /* pale blue — soft background */
  --brand-muted:  #A4BCC5; /* blue-gray — muted accent */
  --white:        #FFFFFF; /* base background */

  /* Fonts */
  --font-heading: "Gilroy", "Montserrat", -apple-system, "Segoe UI", sans-serif;  /* headings / display */
  --font-body:    "Astoria", "Inter", -apple-system, "Segoe UI", sans-serif;      /* body / paragraph */
}
```
