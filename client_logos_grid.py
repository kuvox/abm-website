"""Canonical client logo grid — single source of truth."""
from __future__ import annotations

# Featured clients (tooltip on hover). Order: user list, BeltSmart last among featured.
FEATURED_CLIENTS = [
    {
        "image": "hosewarhouse-logo.png",
        "alt": "Hose Warehouse",
        "href": "https://hosewarehouse.com/",
        "name": "Hose Warehouse",
        "tenure": "6+ Year Client",
        "category": "Industrial Parts",
    },
    {
        "image": "mymusic-folders-logo.png",
        "alt": "My Music Folders",
        "href": "https://www.mymusicfolders.com/",
        "name": "MyMusic Folders",
        "tenure": "3+ Year Client",
        "category": "Musician Supplies",
    },
    {
        "image": "tallslim-tees-logo.png",
        "alt": "TallSlim Tees",
        "href": "https://tallslimtees.com/",
        "name": "TallSlim Tees",
        "tenure": "4+ Year Client",
        "category": "Apparel",
    },
    {
        "image": "parker-baby-logo.png",
        "alt": "Parker Baby",
        "href": "https://parkerbaby.com/",
        "name": "Parker Baby",
        "tenure": "4+ Year Client",
        "category": "Baby Accessories",
    },
    {
        "image": "kingsley-north-logo.png",
        "alt": "Kingsley North",
        "href": "https://kingsleynorth.com/",
        "name": "Kingsley North",
        "tenure": "3+ Year Client",
        "category": "Lapidary Supplies",
    },
    {
        "image": "meseroll-logo.png",
        "alt": "Meseroll Shop",
        "href": "https://meserollshop.com/",
        "name": "Meseroll Shop",
        "tenure": "1 Year Client",
        "category": "Biking Gear",
    },
    {
        "image": "indoor-cycle-pros-logo.png",
        "alt": "Indoor Cycle Pros",
        "href": "https://indoorcyclepros.com/",
        "name": "Indoor Cycle Pros",
        "tenure": "1 Year Client",
        "category": "Biking Gear",
    },
    {
        "image": "poulsbo-rv-logo.png",
        "alt": "Poulsbo RV",
        "href": "https://poulsborv.com/",
        "name": "Poulsbo RV",
        "tenure": "2+ Year Client",
        "category": "RV Dealership",
    },
    {
        "image": "maia-homes-logo.png",
        "alt": "Maia Homes",
        "href": "https://maiahomes.com/",
        "name": "Maia Homes",
        "tenure": "1+ Year Client",
        "category": "Home Decor",
    },
    {
        "image": "conservation-mart-logo.png",
        "alt": "Conservation Mart",
        "href": "https://conservationmart.com/",
        "name": "Conservation Mart",
        "tenure": "1-Year Client",
        "category": "Industrial Parts",
    },
    {
        "image": "beltsmart-logo.png",
        "alt": "BeltSmart",
        "href": "https://murdockindustrial.com/",
        "name": "BeltSmart",
        "tenure": "6+ Year Client",
        "category": "Industrial Parts",
    },
]

# Additional logos — grayscale to color on hover, link only (no tooltip).
OTHER_CLIENTS = [
    {
        "image": "the-crypto-lawyers-logo.png",
        "alt": "The Crypto Lawyers",
        "href": "https://www.thecryptolawyers.com/",
    },
    {
        "image": "murdock-industrial-logo.png",
        "alt": "Murdock Industrial",
        "href": "https://murdockindustrial.com/",
    },
    {
        "image": "irish-woodworks-logo.png",
        "alt": "Irish Woodworks",
        "href": "https://www.irishwoodworks.com/",
    },
    {
        "image": "billfodl-logo.png",
        "alt": "Billfodl",
        "href": "https://billfodl.com/",
    },
    {
        "image": "listing-mirror-logo.png",
        "alt": "Listing Mirror",
        "href": "https://www.listingmirror.com/",
    },
]


def _featured_item(rel: str, client: dict) -> str:
    img = f"{rel}images/website-logos/website-client-logos/{client['image']}"
    return f"""    <a class="logo-item logo-item--has-tooltip" href="{client['href']}" target="_blank" rel="noopener">
      <img src="{img}" alt="{client['alt']}">
      <div class="logo-tooltip" role="tooltip">
        <p class="logo-tooltip-name">{client['name']}</p>
        <p class="logo-tooltip-tenure">{client['tenure']}</p>
        <p class="logo-tooltip-category">{client['category']}</p>
      </div>
    </a>"""


def _other_item(rel: str, client: dict) -> str:
    img = f"{rel}images/website-logos/website-client-logos/{client['image']}"
    return f"""    <a class="logo-item" href="{client['href']}" target="_blank" rel="noopener">
      <img src="{img}" alt="{client['alt']}">
    </a>"""


def client_logos_grid(rel: str = "") -> str:
    featured = "\n".join(_featured_item(rel, c) for c in FEATURED_CLIENTS)
    other = "\n".join(_other_item(rel, c) for c in OTHER_CLIENTS)
    return f"""<div class="client-collage-shell">
  <div class="client-collage-card client-collage-card--home" aria-label="Client logos">
{featured}
{other}
  </div>
</div>"""
