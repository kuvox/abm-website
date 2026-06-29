"""Canonical Client Case Studies carousel — single source of truth."""
from __future__ import annotations

CASE_STUDY_CARDS = [
    {
        "href": "case-studies/hose-warehouse-beltsmart.html",
        "image": "images/Hose-Warehouse.jpg",
        "alt": "HoseWarehouse",
        "name": "HoseWarehouse",
        "result": "181.92% Increase in Revenue",
        "excerpt": "HoseWarehouse.com and BeltSmart.com sell industrial hose, tools and accessories at wholesale prices in the USA. Both are subsidiaries of Murdock Industrial based in Akron, Ohio.",
    },
    {
        "href": "case-studies/kingsley-north.html",
        "image": "images/kingsley-north-case-study-thumbnail.jpg",
        "video_webm": "images/kingsley-north-case-study-video.webm",
        "video_mp4": "images/kingsley-north-case-study-video.mp4",
        "alt": "Kingsley North",
        "name": "Kingsley North",
        "result": "15.64% Higher Conversion Rate",
        "excerpt": "Kingsley North leads the lapidary equipment space. We enhanced product feeds and built feature-focused video ads to grow conversions on the same budget.",
    },
    {
        "href": "case-studies/parker-baby.html",
        "image": "images/parker-baby-homepage.png",
        "alt": "Parker Baby",
        "name": "Parker Baby",
        "result": "Increased ROAS Within 3 Weeks",
        "excerpt": "Parker Baby designs and provides exceptional and affordable baby products for the modern parent. Since 2015, they've specialized in diaper backpacks, caddies, bath supplies, and other baby accessories.",
    },
    {
        "href": "case-studies/tallslim-tees.html",
        "image": "images/tallslim-tees-homepage-3.png",
        "alt": "TallSlim Tees",
        "name": "TallSlim Tees",
        "result": "74.70% YoY Growth in Google Ads Revenue",
        "excerpt": "TallSlim Tees is an apparel brand for men 6 ft&ndash;7 ft tall, designing slim and tall clothing focused on length rather than width for t-shirts, flannels, and activewear.",
    },
    {
        "href": "case-studies/iron-fence-shop.html",
        "image": "images/iron-fence-shop-homepage.png",
        "alt": "Iron Fence Shop",
        "name": "Iron Fence Shop",
        "result": "221% Increase in Form Leads",
        "excerpt": "Iron Fence Shop retails handcrafted and custom designed perimeter fencing crafted in their own facility including fencing, driveway gates and finials constructed of iron and aluminum.",
    },
    {
        "href": "case-studies/trailheads.html",
        "image": "images/trailheads.jpg",
        "alt": "Trailheads",
        "name": "TrailHeads",
        "result": "172% Year-Over-Year Revenue Growth",
        "excerpt": "Established in 2002, TrailHeads specializes in the manufacturing of quality and comfortable accessories for running and outdoor sports enthusiasts. They design and test their products in-house and offer a variety of hats, headbands, gloves and related accessories that can be worn year round.",
    },
    {
        "href": "https://www.datafeedwatch.com/blog/increase-revenue-manging-multiple-feeds",
        "external": True,
        "image": "images/datafeedwatch.jpg",
        "alt": "DataFeedWatch feature",
        "name": "DataFeedWatch",
        "result": "136% Average Revenue Increase",
        "excerpt": "Discover how we use DataFeedWatch to manage multiple product feeds for over 50 clients while increasing their revenue by 136% and ROAS by 32% on average.",
    },
]


def case_study_nav_slugs() -> list[str]:
    """Ordered internal case study slugs (matches homepage carousel, excludes external links)."""
    slugs: list[str] = []
    for card in CASE_STUDY_CARDS:
        if card.get("external"):
            continue
        href = card["href"]
        slugs.append(href.removeprefix("case-studies/").removesuffix(".html"))
    return slugs


def case_study_pager_html(current_slug: str, rel: str = "../") -> str:
    slugs = case_study_nav_slugs()
    if current_slug not in slugs:
        return ""
    idx = slugs.index(current_slug)
    prev_slug = slugs[(idx - 1) % len(slugs)]
    next_slug = slugs[(idx + 1) % len(slugs)]
    base = f"{rel}case-studies/"
    return f"""    <nav class="case-study-pager" aria-label="Browse case studies">
      <a href="{base}{prev_slug}.html" class="case-study-pager__arrow" aria-label="Previous case study"><span aria-hidden="true">&lsaquo;</span></a>
      <span class="case-study-pager__label">Next case study</span>
      <a href="{base}{next_slug}.html" class="case-study-pager__arrow" aria-label="Next case study"><span aria-hidden="true">&rsaquo;</span></a>
    </nav>
"""
    if card.get("video_webm") or card.get("video_mp4"):
        poster = f"{rel}{card['image']}"
        sources = []
        if card.get("video_webm"):
            sources.append(
                f'<source src="{rel}{card["video_webm"]}" type="video/webm">'
            )
        if card.get("video_mp4"):
            sources.append(
                f'<source src="{rel}{card["video_mp4"]}" type="video/mp4">'
            )
        source_markup = "\n        ".join(sources)
        return f"""        <video class="case-image" autoplay muted loop playsinline poster="{poster}" aria-label="{card['alt']}">
        {source_markup}
        </video>"""
    return f"""        <img src="{rel}{card['image']}" alt="{card['alt']}" class="case-image">"""


def _card_html(rel: str, card: dict) -> str:
    href = card["href"] if card.get("external") else f"{rel}{card['href']}"
    target = ' target="_blank" rel="noopener"' if card.get("external") else ""
    return f"""      <a class="case-card" href="{href}"{target} style="text-decoration:none;color:inherit;">
{_media_html(rel, card)}
        <div class="case-body">
          <h3>{card['name']}</h3>
          <div class="result">{card['result']}</div>
          <p>{card['excerpt']}</p>
          <span class="more">Read the case study &rarr;</span>
        </div>
      </a>"""


def case_studies_section(rel: str = "", *, heading: str | None = "Customer Success Stories") -> str:
    cards = "\n".join(_card_html(rel, card) for card in CASE_STUDY_CARDS)
    heading_html = ""
    if heading:
        heading_html = f"""  <div class="container">
    <div class="case-studies-carousel-header center">
      <h2>{heading}</h2>
    </div>
  </div>
"""
    return f"""<section class="section section--alt client-case-studies-section">
{heading_html}  <div class="case-studies-carousel-track" tabindex="0" aria-label="Client case studies">
    <div class="case-studies-carousel">
{cards}
    </div>
  </div>
</section>"""
