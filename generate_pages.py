#!/usr/bin/env python3
"""
Generates case study and resource article HTML pages from a data table,
following the templates documented in docs/blog-pages.md and docs/PAGE_PATTERNS.md.

Run from inside the ABM Website folder. Outputs to:
  case-studies/<slug>.html
  resources/<slug>.html
"""
from __future__ import annotations
import os
import sys
import textwrap
from pathlib import Path

SITE_ROOT = Path(__file__).parent
sys.path.insert(0, str(SITE_ROOT))

from case_studies_section import case_study_pager_html
from gated_resources_content import (
    CART_DATA_FAQS,
    CART_DATA_GATED,
    CART_DATA_PREVIEW,
    CONV_TRACKING_GATED,
    CONV_TRACKING_PREVIEW,
    GMC_SETUP_GATED,
    GMC_SETUP_PREVIEW,
    META_CREATIVE_GATED,
    META_CREATIVE_PREVIEW,
    SFTP_GATED,
    SFTP_PREVIEW,
)
from schema.jsonld import article_schema, case_study_schema, guide_schema
from site_nav import blog_newsletter, footer, header

# ---------- case-study closing CTAs ----------

def work_with_us_section(rel: str = "") -> str:
    return f"""<section class="section--black" id="work-with-us">
  <div class="container resources-work-split">
    <div>
      <h2>What it&rsquo;s Like to Work With Us</h2>
      <p>We work closely with our clients to understand their growth plans and growth limits. That allows both your team and ours to aim for ambitious goals that are feasible and within your budget.</p>
      <div class="hero-actions">
        <a href="{rel}about.html" class="btn btn-gradient">Who We Work With</a>
        <a href="{rel}services.html#pricing" class="hero-arrow-link">See Pricing Examples <span aria-hidden="true">&rsaquo;</span></a>
      </div>
    </div>
    <figure class="resources-work-photo">
      <img src="{rel}images/austin-becker-e-commerce-marketing-22.jpg" alt="Austin Becker and team collaborating on e-commerce marketing strategy">
    </figure>
  </div>
</section>"""


def take_the_next_step_section(rel: str = "") -> str:
    return f"""<section class="cta-banner cta-banner--dark grid-trail">
  <canvas class="grid-trail-canvas" aria-hidden="true"></canvas>
  <div class="container">
    <h2>Take the Next Step</h2>
    <p>We're ready to discuss your business and how we can help you grow it. Please fill out a contact form so we can begin the conversation.</p>
    <a href="{rel}contact.html" class="btn btn-primary">Contact Us</a>
  </div>
</section>"""

# ============================================================
# CASE STUDIES
# ============================================================

CASE_STUDIES = [
    {
        "slug": "hose-warehouse-beltsmart",  # already exists; re-generated for consistency
        "client": "Murdock Industrial",
        "title": "181.92% Year-Over-Year Increase in Revenue From Google Ads",
        "intro": "HoseWarehouse.com and BeltSmart.com sell industrial hose, tools and accessories at wholesale prices in the USA. Both are subsidiaries of Murdock Industrial based in Akron, Ohio.",
        "hero_image": "images/Hose-Warehouse.jpg",
        "hero_alt": "Hose Warehouse Google Ads success case study",
        "meta_description": "HoseWarehouse.com and BeltSmart.com — subsidiaries of Murdock Industrial — grew Google Ads revenue 181.92% year-over-year with a rebuilt product feed and shopping ads work.",
        "challenge": "Shopping ad data quality makes a huge difference in a saturated market. Optimizing and cleaning product ad data was a priority for Tony to keep his ads competitive with established competitors. Managing tens of thousands of SKUs was simply too time-consuming and foreign to the internal team, so Tony engaged Austin to begin re-creating a more manageable and organized shopping feed.",
        "solution": "With a more advanced product data feed system, Austin was able to increase the number of products eligible for advertising, more accurately quote shipping rates in Shopping Ads, and add much-needed MPN and SKU data across the entire product catalog.",
        "what_we_did": [
            "Improvements to product feeds led to increased free Google Shopping traffic, but more importantly to substantial paid revenue growth. After completing the product feed overhaul, Tony asked Austin to revamp search and shopping ads for both stores, supporting additional growth already fueled by improved website improvements.",
            "Between 2019 and 2020, sales growth in both stores was nearly 200% year over year, while ads costs increased far less.",
        ],
        "metrics": [
            ("181.92%", "year-over-year increase in revenue from Google Ads"),
            ("10.65%", "increase in paid search conversion rate"),
        ],
        "body_sidebar_intro": "Year-over-year on Google Ads",
        "body_sidebar_foot": "Across Hose Warehouse and BeltSmart.",
        "quote": "Austin collaborates frequently with us to ensure that our online business goals are met. His work has significantly steered our pay per click sales trajectory up over the past years.",
        "quote_author": "Tony Price",
        "quote_title": "Owner &amp; CEO, Murdock Industrial",
    },
    {
        "slug": "iron-fence-shop",
        "client": "Iron Fence Shop",
        "title": "16% Decrease in Google Ad Spend. 221% Increase in Form Leads.",
        "intro": "Iron Fence Shop retails handcrafted and custom-designed perimeter fencing crafted in their own facility — including fencing, driveway gates, and finials constructed of iron and aluminum.",
        "hero_image": "images/iron-fence-shop-homepage.png",
        "hero_alt": "Iron Fence Shop homepage",
        "meta_description": "How we lowered Iron Fence Shop's Google Ads spend 16% while growing form leads 221% through better conversion tracking and refreshed ad copy.",
        "challenge": "Iron Fence Shop's ad accounts performed at a high level already, but business owner Josh wanted a regular watch on ads to ensure the business wasn't overspending or missing opportunities for growth.",
        "solution": "By auditing and improving the conversion tracking of forms on the website, Austin was able to better capture the value of each lead and ultimately lower the cost per lead. Austin's revision of ad copy and extensions increased click-through rates to further increase traffic.",
        "what_we_did": [
            "Iron Fence Shop was able to decrease spend on Google Ads to save money while achieving higher leads volume within three months.",
        ],
        "metrics": [
            ("16%", "decrease in cost"),
            ("221%", "increase in form leads during the same time period"),
        ],
        "body_sidebar_intro": "Within three months",
        "body_sidebar_foot": "While lowering Google Ads spend.",
        "quote": "Throughout the past 2 years, Austin helped us take advantage of large shifts in consumer shopping trends, while keeping costs lean on both our Google and Bing ads campaigns.",
        "quote_author": "Joshua Manley",
        "quote_title": "Owner &amp; President, Iron Fence Shop",
    },
    {
        "slug": "trailheads",
        "client": "TrailHeads",
        "title": "Building on Amazon Sales Success",
        "intro": "Established in 2002, TrailHeads specializes in the manufacturing of quality and comfortable accessories for running and outdoor sports enthusiasts. They design and test their products in-house and offer a variety of hats, headbands, gloves and related accessories that can be worn year round.",
        "hero_image": "images/trailheads.jpg",
        "hero_alt": "Woman wearing Trailheads hat",
        "meta_description": "TrailHeads expanded beyond Amazon by segmenting their product feed by seasonality and styles, driving 172% year-over-year revenue growth on their own site.",
        "challenge": "TrailHeads wanted to supplement their strong position on Amazon.com with their own, newly improved BigCommerce website. In hopes of recreating their success on Amazon, store owner Ed reached out to Austin.",
        "solution": "Austin enhanced TrailHeads' product feed by segmenting products according to seasonality and styles. Having products categorized neatly in seasonal campaigns allowed TrailHeads and Austin to react quickly to holiday sales trends and new product releases with new bids, ad copy, and promotions.",
        "what_we_did": [],
        "metrics": [
            ("172%", "year over year increase in revenue"),
            ("6%", "increase in conversion rate during the same time period"),
        ],
        "body_sidebar_intro": "After feed segmentation and seasonal campaigns",
        "body_sidebar_foot": "Supplementing Amazon with their own site.",
        "quote": "Austin matched our product feed and ad campaigns to our business objectives in a way that allowed us to achieve substantial sales growth with seasonal products and new product launches.",
        "quote_author": "Ed Raftery",
        "quote_title": "Founder &amp; CEO, TrailHeads",
    },
    {
        "slug": "parker-baby",
        "client": "Parker Baby Co.",
        "title": "Increased Return on Ad Spend Within 3 Weeks",
        "intro": "Parker Baby designs and provides exceptional and affordable baby products for the modern parent. Since 2015, they've specialized in diaper backpacks, caddies, bath supplies, and other baby accessories.",
        "hero_image": "images/parker-baby-homepage.png",
        "hero_alt": "Parker Baby Co. homepage",
        "meta_description": "How we scaled Parker Baby's Google Shopping and search ads without scaling acquisition cost — better feeds, optimized GMC data, and a 20.72% conversion rate lift.",
        "challenge": "Google Ads worked well for Parker Baby. However, customer acquisition opportunities were growing thanks to the brand's success on Amazon and increasing demand for the brand's products. The goal was to scale sales on Google shopping and search ads to take advantage of growing demand for Parker Baby's products — but to do so without scaling customer acquisition costs.",
        "solution": "To scale Google Ads, Austin's team re-created Parker Baby's product feed with optimized titles and shipping data to show shoppers the correct product ad with the lowest available shipping price. The team then optimized color, material, size, images and optional data fields in Google Merchant Center. With optimized product data, shopping ads click-through rates and conversion rates increased.",
        "what_we_did": [
            "Within the first 3 weeks, return on ad spend (ROAS) increased and ad spend dropped due to cost savings from improved CTR and a planned reduction in branded search spending. Emphasis on non-branded, higher funnel searches increased pay-per-click sales.",
        ],
        "metrics": [
            ("2.25%", "more revenue from Google Paid/Organic search results"),
            ("20.72%", "increase in conversion rate"),
            ("19.06%", "decrease in cost"),
        ],
        "body_sidebar_intro": "Within the first 3 weeks",
        "body_sidebar_foot": "Without scaling acquisition cost.",
        "quote": "Austin is very responsive and quickly understood our businesses and our goals, and built campaigns to meet those goals.",
        "quote_author": "Sam Huebner",
        "quote_title": "CEO, Parker Baby Co.",
    },
    {
        "slug": "tallslim-tees",
        "client": "TallSlim Tees",
        "title": "6x+ Conv. Value Growth from First to Most Recent Q4",
        "intro": "TallSlim Tees is an apparel brand specifically catered to men 6 ft&ndash;7 ft tall who seek a wardrobe tailored to their natural build. Their specialty is designing slim and tall clothing that focuses on length rather than width for t-shirts, flannels, and activewear that guarantees a perfect fit for the tall and lean figure.",
        "hero_image": "images/tallslim-tees-homepage-3.png",
        "hero_alt": "TallSlim Tees homepage",
        "meta_description": "How we scaled TallSlim Tees Google Shopping ads after acquisition—6x+ attributed conversion value growth from first to most recent Q4 while expanding into new product categories.",
        "challenge": "TallSlim Tees&rsquo; Google Ads account was performing well but the business needed to scale sales after being acquired by a new owner. The new ownership&rsquo;s marketing team needed to increase sales across existing top-selling SKUs, but also introducing new product categories, like jogger pants and hoodies, without losing profits along the way.",
        "solution": "Our team updated TallSlim Tees&rsquo; existing Google Shopping Ads product data with enhanced product attributes, like variant colors, styles and keywords that are frequently searched on Google.com. We optimized all product data per variant, and segmented inventory by sell-through rate (e.g. high, mid, and low sell-through products). We then updated all paid ads assets with additional video and image creative elements in ads, added user-generated content to paid ads, and restructured campaigns to keep spend allocated appropriately between existing inventory and new releases for optimal balance between sales growth and profit.",
        "what_we_did": [],
        "results": [
            "Between our first Q4 working on TallSlim Tees and the most recent Q4, attributed conversion value in Google Ads increased by over 6x, while cost increased by over 2x.",
        ],
        "metrics": [
            ("6x+", "Conv. value growth from 1st to most recent Q4"),
            ("2x+", "Ad budget growth from 1st to most recent Q4"),
            ("3-tier", "segmentation by sell-through rate"),
        ],
        "body_sidebar_intro": "From first to most recent Q4",
        "body_sidebar_foot": "While balancing sales growth and profit.",
        "quote": "Austin is very responsive and quickly understood our businesses and our goals, and built campaigns to meet those goals.",
        "quote_author": "Sam Huebner",
        "quote_title": "CEO, Parker Baby Co.",
    },
    {
        "slug": "kingsley-north",
        "client": "Kingsley North",
        "title": "15.64% Higher Google Ads Conversion Rate on the Same Budget",
        "intro": "Kingsley North is a leader in the lapidary equipment space among rockhounds and lapidary artists.",
        "hero_image": "images/kingsley-north-case-study-thumbnail.jpg",
        "hero_alt": "Kingsley North lapidary equipment",
        "hero_video_webm": "images/kingsley-north-case-study-video.webm",
        "hero_video_mp4": "images/kingsley-north-case-study-video.mp4",
        "hero_caption": "Above: our team created videos to promote the Kingsley North Cabber 6.",
        "meta_description": "How we grew Kingsley North ad impressions with enhanced product feeds and feature-focused video creative, lifting Google Ads conversion rate 15.64% on the same budget.",
        "challenge": "",
        "solution": "",
        "what_we_did": [],

        "body_sidebar_intro": "Since engaging with Kingsley North in 2022",
        "body_sidebar_foot": "All within the same budget.",
        "body_html": """    <h2>Background</h2>
    <p>Lapidary: the craft of cutting, polishing, and engraving stones</p>
    <p>Kingsley North is a leader in the lapidary equipment space among rockhounds and lapidary artists. Kingsley&rsquo;s line of cabbing machines are designed specially for this niche artisan community. Our challenge was to visually demonstrate the superior utility and features of the Kingsley North Cabber 6 - KNC6 Rev 2 to increase sales.</p>

    <h2>Enhanced Data for More Ad Impressions</h2>
    <p>We enhanced product feed data with relevant search queries, i.e., we added keywords into product feed titles and attributes like product_type, product_category, and more. This allowed more and more search queries to match with data in Kingsley North&rsquo;s product feeds across Google Search, and to reach people interested in rock polishing and rockhounding on Facebook and Instagram.</p>

    <h2>Selling the Customer Via Video</h2>
    <p>Because we generated more ad impressions for Kingsley North&rsquo;s products, we needed to take that opportunity to pre-sell people who viewed those ads with video.</p>
    <p>To make this happen, we worked with Kingsley North&rsquo;s team who created a collection of video footage for us to edit into ads. Our video editors assembled video footage into feature-focused videos. These videos highlighted the Cabber 6&rsquo;s trustworthiness and quality by featuring a well-known lapidary artist using the machine. Video viewers also got a chance to preview the quality and appreciated features of the machine.</p>

    <h2>Results</h2>
    <p>By optimizing all of Kingsley North&rsquo;s product data feeds in Google Ads, Facebook, and Instagram, we increased opportunities for their ads to show on relevant searches in search engines, and to appear to interested audiences on social media in video and product-feed ads.</p>""",
        "metrics": [
            ("15.64%", "increase in Google Ads conversion rate"),
            ("6%", "reduction in CPA"),
            ("10%", "ROAS improvement on the same budget"),
        ],
        "quote": "",
        "quote_author": "",
        "quote_title": "",
    },
]

def _case_hero_media(cs: dict, rel: str) -> str:
    alt = cs["hero_alt"]
    poster = cs["hero_image"]
    if cs.get("hero_video_webm") and cs.get("hero_video_mp4"):
        media = f"""      <video class="case-hero-image" autoplay muted loop playsinline poster="{rel}{poster}">
        <source src="{rel}{cs['hero_video_webm']}" type="video/webm">
        <source src="{rel}{cs['hero_video_mp4']}" type="video/mp4">
        <img src="{rel}{poster}" alt="{alt}" class="case-hero-image">
      </video>"""
    else:
        media = f'      <img src="{rel}{poster}" alt="{alt}" class="case-hero-image">'
    caption = cs.get("hero_caption")
    if caption:
        return f"""      <figure class="case-hero-figure">
{media}
        <figcaption class="case-hero-caption">{caption}</figcaption>
      </figure>"""
    return media


def _case_body_sidebar_metrics_html(cs: dict) -> str:
    if not cs.get("metrics"):
        return ""
    cards = "\n".join(
        f"""      <div class="case-metric-card">
        <div class="case-metric-value">{value}</div>
        <p class="case-metric-label">{label}</p>
      </div>"""
        for value, label in cs["metrics"]
    )
    intro_html = ""
    if cs.get("body_sidebar_intro"):
        intro_html = f'    <p class="case-body-metrics-intro">{cs["body_sidebar_intro"]}</p>\n'
    foot_html = ""
    if cs.get("body_sidebar_foot"):
        foot_html = f'    <p class="case-body-metrics-foot">{cs["body_sidebar_foot"]}</p>\n'
    return f"""    <aside class="case-body-metrics" aria-label="Key results">
{intro_html}{cards}
{foot_html}    </aside>"""


def render_case_study(cs: dict) -> str:
    rel = "../"
    if cs.get("body_html"):
        case_body_html = cs["body_html"]
    else:
        what_we_did_html = ""
        if cs.get("results"):
            what_we_did_html = "\n    <h2>Results</h2>\n" + "\n".join(
                f"    <p>{p}</p>" for p in cs["results"]
            )
        elif cs["what_we_did"]:
            what_we_did_html = "\n    <h2>What we did</h2>\n" + "\n".join(
                f"    <p>{p}</p>" for p in cs["what_we_did"]
            )
        case_body_html = f"""    <h2>Challenge</h2>
    <p>{cs['challenge']}</p>

    <h2>Solution</h2>
    <p>{cs['solution']}</p>{what_we_did_html}"""
    sidebar_html = _case_body_sidebar_metrics_html(cs)
    if sidebar_html:
        case_body_section_html = f"""<section class="case-body">
  <div class="container case-body-split">
{sidebar_html}
    <div class="case-body-content">
{case_body_html}
    </div>
  </div>
</section>"""
    else:
        case_body_section_html = f"""<section class="case-body">
  <div class="container">
{case_body_html}
  </div>
</section>"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{cs['client']} Case Study — Austin Becker E-Commerce Marketing</title>
<meta name="description" content="{cs['meta_description']}">
<meta property="og:title" content="{cs['client']} Case Study">
<meta property="og:description" content="{cs['meta_description']}">
<meta property="og:type" content="article">
<link rel="canonical" href="https://abeckermarketing.com/case-studies/{cs['slug']}.html">
{case_study_schema(slug=cs['slug'], title=cs['title'], description=cs['meta_description'], client=cs['client'], image_path=cs['hero_image'])}
<link rel="stylesheet" href="../styles.css">
</head>
<body>

{header(rel, active="case-studies")}

<section class="case-hero">
  <div class="container hero-split">
    <div>
      <span class="case-eyebrow">Case Study &middot; {cs['client']}</span>
      <h1>{cs['title']}</h1>
      <p class="case-intro">{cs['intro']}</p>
    </div>
    <div>
{_case_hero_media(cs, rel)}
    </div>
  </div>
</section>

{case_body_section_html}

<section class="section client-reviews-section">
  <div class="container">
{case_study_pager_html(cs['slug'], rel)}
    <h3 class="clients-quotes-title clients-quotes-title--light">Client reviews <a href="https://maps.app.goo.gl/MyasdYPg5uZhGE7N7" target="_blank" rel="noopener" class="from-google">from Google</a></h3>
    <div class="grid-3 clients-quotes">
      <div class="quote">
        <p>We&rsquo;ve had a great experience with Austin Becker E-Commerce Marketing. They have managed Google Ads, Google Shopping, and Bing Ads for 2 of our online businesses for over 6 months and we are very impressed so far. Austin is very responsive and quickly understood our businesses and our goals, and built campaigns to meet those goals.</p>
        <cite>Sam Huebner<span><a href="https://www.parkerbaby.com/" target="_blank" rel="noopener">Parkerbaby.com</a></span></cite>
      </div>
      <div class="quote">
        <p>We have been advertising on Google since 2012 and as the chart indicates, we typically have a (Summer) seasonal bump in sales. Since hiring Austin and his team in 2020, the spike tells the story. I highly recommend Austin for your next digital advertising project. You can expect exceptional results and a healthy return on your investment!</p>
        <cite>Rex Bledsoe<span><a href="https://aquadesign.com/" target="_blank" rel="noopener">aquadesign.com</a></span></cite>
      </div>
      <div class="quote">
        <p>I&rsquo;ve had the pleasure of working with Austin, and I must say, he&rsquo;s been an absolute legend! His exceptional expertise, combined with his patient and helpful approach, made navigating complex feed setup, optimisation and scripting a breeze. Austin&rsquo;s attention to detail and thoroughness ensured we covered all bases and his guidance was invaluable.</p>
        <cite>Rich Fraser<span><a href="https://www.boxhill.co.nz/" target="_blank" rel="noopener">boxhill.co.nz</a></span></cite>
      </div>
    </div>
  </div>
</section>

{work_with_us_section(rel)}

{take_the_next_step_section(rel)}

{footer(rel)}
<script src="{rel}scripts/hero-grid-interactive.js" defer></script>
</body>
</html>
"""

# ============================================================
# RESOURCE ARTICLES
# ============================================================

# Each article body uses HTML-as-string. Keep paragraphs short and readable.
RESOURCES = [
    {
        "slug": "fix-cart-data-errors-google-ads",
        "title": "Fix Cart Data Errors in Google Ads",
        "lead": "When Google Ads shows Missing Cart Data, your Merchant Center product IDs and tracking tag IDs don&rsquo;t match. Fix it without losing historic performance data.",
        "meta_description": "Fix Missing Cart Data errors in Google Ads when GMC item IDs don\u2019t match your Shopify tracking tag. Step-by-step gradual ID swap checklist.",
        "date": "Jun 23, 2026",
        "feature_image": "images/3_Display_Ads.png",
        "feature_alt": "Fix Cart Data Errors in Google Ads",
        "categories": [("Google Ads", "google-ads"), ("Google Shopping", "google-shopping"), ("Product Feeds", "product-feeds")],
        "video_embed": "https://www.youtube.com/embed/wSx8Lmtb_L0",
        "video_watch_url": "https://youtu.be/wSx8Lmtb_L0",
        "gated": True,
        "faqs": CART_DATA_FAQS,
        "toc": [
            ("the-problem", "The Problem"),
            ("the-solution", "The Solution"),
            ("cross-sell-reports", "Cross-sell reports"),
            ("sources-cited", "Sources cited"),
        ],
        "preview_html": CART_DATA_PREVIEW,
        "gated_body_html": CART_DATA_GATED,
        "body_html": CART_DATA_PREVIEW + CART_DATA_GATED,
        "hero_cta_href": "#content-gate",
        "hero_cta_label": "Get the Checklist",
    },
    {
        "slug": "google-merchant-center-sftp-upload",
        "title": "Google Merchant Center SFTP File Upload",
        "lead": "Upload pricing and inventory to Google and Microsoft Merchant Center multiple times per day using SFTP and DataFeedWatch.",
        "meta_description": "Step-by-step SFTP file upload setup for Google Merchant Center and Microsoft Merchant Center. Send intraday product feed updates from DataFeedWatch.",
        "date": "Apr 27, 2026",
        "feature_image": "images/2026-Product-Feed-Tutorial-light.png",
        "feature_alt": "Google Merchant Center SFTP file upload guide",
        "categories": [("Google Shopping", "google-shopping"), ("Product Feeds", "product-feeds")],
        "video_embed": "https://www.youtube.com/embed/NjdGmRHEABk",
        "video_watch_url": "https://youtu.be/NjdGmRHEABk",
        "gated": True,
        "toc": [
            ("know-before", "Know before implementing"),
            ("google-merchant-center", "Google Merchant Center"),
            ("microsoft-merchant-center", "Microsoft Merchant Center"),
            ("resources-cited", "Resources cited"),
        ],
        "preview_html": SFTP_PREVIEW,
        "gated_body_html": SFTP_GATED,
        "body_html": SFTP_PREVIEW + SFTP_GATED,
        "hero_cta_href": "#content-gate",
        "hero_cta_label": "Get the Checklist",
    },
    {
        "slug": "google-merchant-center-setup-2026",
        "title": "2026 Google Merchant Center Full Setup",
        "lead": "Complete checklist for sending optimized Shopify product data to Google Merchant Center in 2026 &mdash; without breaking historic sales data tied to existing product IDs.",
        "meta_description": "2026 Google Merchant Center full setup for Shopify: DataFeedWatch, product IDs, feed submission, troubleshooting, and policy fixes.",
        "date": "Feb 17, 2026",
        "feature_image": "images/2026-Product-Feed-Tutorial-light.png",
        "feature_alt": "2026 Google Merchant Center full setup guide",
        "categories": [("Google Shopping", "google-shopping"), ("Product Feeds", "product-feeds")],
        "video_embed": "https://www.youtube.com/embed/-LOxC-yi6SI",
        "video_watch_url": "https://youtu.be/-LOxC-yi6SI",
        "gated": True,
        "toc": [
            ("before-you-begin", "Before you begin"),
            ("shopify-setup", "Shopify setup"),
            ("datafeedwatch-setup", "DataFeedWatch setup"),
            ("submit-feeds", "Submit feeds"),
            ("troubleshooting", "Troubleshooting"),
            ("sources-cited", "Sources cited"),
        ],
        "preview_html": GMC_SETUP_PREVIEW,
        "gated_body_html": GMC_SETUP_GATED,
        "body_html": GMC_SETUP_PREVIEW + GMC_SETUP_GATED,
        "hero_cta_href": "#content-gate",
        "hero_cta_label": "Get the Checklist",
    },
    {
        "slug": "meta-creative-assets-checklist",
        "title": "Meta Creative Assets Checklist",
        "lead": "Prepare image and video assets for Meta ads. Dimensions, safe zones, file specs, and a sales promotion checklist &mdash; deliver 7 days before launch.",
        "meta_description": "Meta ads creative checklist: video and image dimensions, safe zones, file specs, and sales promotion asset requirements for Facebook and Instagram ads.",
        "date": "Apr 14, 2026",
        "feature_image": "images/3_Display_Ads.png",
        "feature_alt": "Meta creative assets checklist",
        "categories": [("Meta", "meta"), ("Research Articles", "research-articles")],
        "gated": True,
        "toc": [
            ("creative-inspiration", "Creative inspiration"),
            ("creative-checklist", "Creative asset checklist"),
            ("sales-promotion", "Sales promotion checklist"),
            ("references", "References"),
        ],
        "preview_html": META_CREATIVE_PREVIEW,
        "gated_body_html": META_CREATIVE_GATED,
        "body_html": META_CREATIVE_PREVIEW + META_CREATIVE_GATED,
        "hero_cta_href": "#content-gate",
        "hero_cta_label": "Get the Checklist",
    },
    {
        "slug": "how-to-optimize-google-shopping-ads-results",
        "title": "How to Optimize Google Shopping Ads Results",
        "lead": "Fixing errors, 150-character titles, optional attributes, and consecutive A/B tests are simple ways to grow shopping ad revenue. No tech magic.",
        "meta_description": "How to optimize Google Shopping ads for more ad revenue. Use 150-character titles, all attributes, and consecutive A/B tests to boost CTR and revenue.",
        "date": "Apr 5, 2025",
        "feature_image": "images/3_Display_Ads.png",
        "feature_alt": "How to optimize Google Shopping Ads",
        "categories": [("Google Shopping", "google-shopping"), ("Product Feeds", "product-feeds")],
        "video_embed": None,
        "toc": [
            ("what-is-optimize", "What do you mean &ldquo;optimize?&rdquo;"),
            ("how-to-run-a-test", "How to run a test"),
            ("summary-and-tips", "Summary and tips"),
            ("resources-cited", "Resources cited"),
        ],
        "body_html": """    <h2 id="what-is-optimize">What do you mean &ldquo;optimize?&rdquo;</h2>
    <p>I mean these four things:</p>
    <ol>
      <li><strong>Fix errors:</strong> missing data, wrong prices, invalid GTINs, etc.</li>
      <li><strong>Write 150-character titles:</strong> about 30 characters are visible when a shopping ad appears. Up to 70 characters are visible on mouse-over. 150 characters is the limit. Use them all.</li>
      <li><strong>Add optional attributes:</strong> add watts to electronics, material to apparel, and MPNs to any product that has a manufacturer-assigned MPN.</li>
      <li><strong>Test changes:</strong> test different keywords and images. I don't see a need to test anything beyond these two product attributes in most cases.
        <ul>
          <li>A <strong>keyword test</strong> could be adding keywords that aren't necessarily part of the product title in your shop, but might be used by Google search users nonetheless. For example, add &ldquo;anniversary&rdquo; to jewelry product titles, even if &ldquo;anniversary&rdquo; is not part of the product title in your shop. Or move the OEM part number from the end to the beginning of the title.</li>
          <li>An <strong>image test</strong> could be between your first and second product image. These tests nearly always lead to substantial changes in CTR, which is the most immediate and telling indicator of whether you've selected the best image for shopping ads. These image formats almost always win: pure white background, apparel items pictured on a human model, product photos (not lifestyle photos).</li>
        </ul>
      </li>
    </ol>
    <p>OEM part numbers are an oft-forgotten title addition to Google shopping ads. Search users sometimes only search the OEM part number, so it's essential to include.</p>

    <h2 id="how-to-run-a-test">How to run a test</h2>
    <p>Testing CTR will yield immediate results, so start with that as your metric.</p>
    <p>Why not test other metrics? You could test number of impressions (more impressions good, less bad) but the problem is that impressions might rise or fall because of factors other than your test variable: increased ad budget, seasonal shopping activity. These would change impressions regardless of your test variable. CTR is a direct indicator of how enticing your shopping ads are, regardless of budget and seasonal changes.</p>

    <h3>Concurrent or consecutive A/B test?</h3>
    <p>You can run A/B tests concurrently (like DataFeedWatch's title A/B test feature, which measures conversion rate changes on your website). However, it's technically hard to test an A/B's impact on CTR because it's not possible to know exactly when version A or B is live when viewing CTR data. A consecutive A/B test is preferable for this reason. The control period is the 30 days before you change a variable. The test period is the 30 days when your variable change is live.</p>

    <h3>Test all or some products?</h3>
    <p>Test changes to all products at once for fast results at the risk of lost ad revenue. Or test a selection of products to allow non-tested products to keep generating sales at the status-quo pace, uninterrupted by your test.</p>

    <h2 id="summary-and-tips">Summary and tips</h2>
    <p>While tests can confirm what you already know (e.g., pure white background images always perform best), they can also help you uncover new ideas (e.g., adding &ldquo;Valentine&rdquo; to a product title during Valentine's Day, or &ldquo;Mother&rdquo; during Mother's Day boosts ad revenue).</p>
    <ul>
      <li>Don't bother testing different background images on your products. A pure white background always wins. I don't know why Google offers AI-generated background changes — they muddle up the product image, which is already small and hard to see.</li>
      <li>Make substantial changes, not minor ones. Moving a word in your title from 1st to 2nd position likely won't change anything. E.g., &ldquo;Nike Men's Running Shoes&rdquo; vs. &ldquo;Men's Nike Running Shoes&rdquo; is a wash. But &ldquo;Nike Men's Road and Track Race Running Shoe&rdquo; vs. &ldquo;Nike Men's Running Shoe&rdquo; will likely yield a difference.</li>
      <li>Automate data collection using software like DataFeedWatch or Supermetrics. Otherwise, gathering reports to compare the outcome of your tests will be so laborious that you never get around to it. Everything should be automated.</li>
    </ul>

    <h2 id="resources-cited">Resources cited</h2>
    <ul>
      <li><a href="https://support.google.com/merchants/answer/7052112?hl=en" target="_blank" rel="noopener">Google Merchant Center Official Attribute Documentation</a></li>
      <li><a href="https://www.datafeedwatch.com/blog/simple-google-shopping-campaign-optimization" target="_blank" rel="noopener">DataFeedWatch's Title A/B Testing Article and Tool</a></li>
    </ul>""",
    },
    {
        "slug": "2025-shopify-conversion-tracking-guide",
        "title": "2025 Shopify Conversion Tracking Guide",
        "lead": "Set up Google Ads and Microsoft Ads conversion tracking on Shopify with enhanced conversions and item_ID hits — without touching theme.liquid.",
        "meta_description": "Set up Shopify conversion tracking for Google Ads and Microsoft Ads with enhanced conversions, all inside Shopify's Customer Events — no theme.liquid edits.",
        "date": "Mar 22, 2025",
        "feature_image": "images/Shopify-Conversion-Tracking-2025.png",
        "feature_alt": "2025 Shopify Conversion Tracking Guide",
        "categories": [("Google Ads", "google-ads"), ("Video Guides and Training", "video-guides")],
        "video_embed": None,
        "toc": [
            ("why-this-approach", "Why this approach"),
            ("what-youll-set-up", "What you'll set up"),
        ],
        "body_html": """    <p>Get the step-by-step <strong>checklist below</strong> the video. The checklist includes code and instructions to quickly set up conversion tracking on Shopify sites.</p>
    <p>With this method I avoid adding code to the <code>theme.liquid</code> file in Shopify (so you don't have to worry about another developer wiping your tracking). Instead, tracking code is all contained within Customer Events, which is what Shopify intended for tracking pixels.</p>

    <h2 id="why-this-approach">Why this approach</h2>
    <ul>
      <li>Tracking lives in <strong>Customer Events</strong>, isolated from theme code.</li>
      <li>Enhanced conversion data (hashed email, phone) flows to Google Ads.</li>
      <li><code>item_ID</code> hits fire so Google Ads can attribute revenue at the product level.</li>
      <li>Same pixel approach works for Microsoft Ads with a parallel snippet.</li>
    </ul>

    <h2 id="what-youll-set-up">What you'll set up</h2>
    <ol>
      <li>A Google Ads Customer Event pixel with <code>conversion</code> and <code>page_view</code> events.</li>
      <li>Enhanced conversions on the purchase event (hashed PII fields).</li>
      <li>A Microsoft Ads UET tag pixel running alongside.</li>
      <li>A test plan: verify each event in Google Ads &ldquo;recent conversions&rdquo; and Microsoft Ads &ldquo;UET tag helper&rdquo;.</li>
    </ol>""",
    },
    {
        "slug": "how-much-to-budget",
        "title": "How to Set Marketing Budgets for Paid Ads",
        "lead": "&ldquo;What should our budget be?&rdquo; A worksheet — and a thirty-minute mental model from Neil H. Borden — to set an appropriate ad budget for your business's size, goals, and margins.",
        "meta_description": "How to set a marketing budget for paid ads using LTV, COGS, and target ROAS. Includes a budget calculator and the &ldquo;marketing mix&rdquo; framework.",
        "date": "May 2, 2023",
        "feature_image": "images/4_Budgets_for_Paid_Ads.png",
        "feature_alt": "How to set budgets for digital advertising",
        "categories": [("Research Articles", "research-articles")],
        "video_embed": None,
        "toc": [
            ("how-much-is-too-much", "How much is too much?"),
            ("marketing-mix", "The &ldquo;marketing mix&rdquo;"),
            ("borden-article", "Full Neil H. Borden article"),
        ],
        "body_html": """    <p>&ldquo;What should our budget be?&rdquo; I get this question often. I used to think &ldquo;as much as you can afford.&rdquo; That's not quite right. Here are methodologies — and a calculator below — to help you set an appropriate budget for your business's size, goals, and margins.</p>

    <h2 id="how-much-is-too-much">How much is too much?</h2>
    <p>It's personally disappointing to me when I see store owners overspending on ads. All the time and effort spent creating products, ultimately wasted on ads that cost more than they netted for the company. Of course, there are reasons to overspend at times to acquire the customer.</p>
    <p>Let's say your average customer is worth $1,000 in lifetime value (LTV). Assume $500 of that goes to cost of goods sold (COGS), 25% to fulfillment, and $150 is reserved for profit. That's $150 left for acquiring a new $1,000-LTV customer. Our cost to acquire a customer (CAC) should be $150 or less.</p>
    <pre><code>$1,000 lifetime customer value (LTV)
- $500   cost of goods sold (COGS)
- $250   miscellaneous costs
- $150   profit taken
= $150   remains to budget for cost to acquire a customer (CAC)</code></pre>
    <p>With that, we know we can spend up to $150 to acquire a new customer while paying bills and taking profit.</p>
    <p>Let's assume that, although the LTV is $1,000, the average order value (AOV) is $250. Therefore a 166% return on ad spend (ROAS) — that's $250 divided by $150 — is acceptable. That's equivalent to a 60% advertising cost of sale (ACoS).</p>
    <pre><code>$1,000 LTV
$250   AOV
$150   available to acquire one new customer

$250 AOV / $150 CAC = 166% ROAS
$150 CAC / $250 AOV = 60% ACoS</code></pre>
    <p>Anything over $150 CAC, 166% ROAS, or 60% ACoS is too high. Anything less is acceptable. So to answer &ldquo;what should my budget be?&rdquo; I ask: how many new customers do you need each month? If you say 1,000, I take your $150 CAC and multiply by 1,000 and set your recommended budget to $150,000 per month.</p>
    <pre><code>1,000  desired new customers
× $150   CAC
= $150,000 monthly ad budget</code></pre>
    <p>Or replace $150 CAC with a desired monthly revenue and a required ROAS target:</p>
    <pre><code>$250,000 desired monthly revenue
÷ 1.66   (166% ROAS)
= $150,602 monthly ad budget</code></pre>

    <section class="interactive-tool" data-tool="budget-calculator" aria-labelledby="budget-calc-title">
      <div class="tool-header">
        <span class="tool-eyebrow">Interactive Tool</span>
        <h3 id="budget-calc-title">Ad Budget Calculator</h3>
        <p class="tool-sub">Enter your desired monthly revenue and your required minimum return on ad spend. We&rsquo;ll tell you what monthly ad budget that implies.</p>
      </div>
      <div class="tool-body">
        <label for="bc-revenue">Desired Monthly Revenue</label>
        <input id="bc-revenue" type="number" min="0" step="100" placeholder="e.g. 250000">
        <label for="bc-roas">Required Minimum Return on Ad Spend (e.g. 1.66 for 166%)</label>
        <input id="bc-roas" type="number" min="0.01" step="0.01" placeholder="e.g. 1.66">
        <button type="button" onclick="(function(){
          var r=parseFloat(document.getElementById('bc-revenue').value);
          var s=parseFloat(document.getElementById('bc-roas').value);
          var out=document.getElementById('bc-out');
          if(!r||!s||s<=0){out.querySelector('.tool-result-value').textContent='—';return;}
          var b=r/s;
          out.querySelector('.tool-result-value').textContent='$'+Math.round(b).toLocaleString();
        })();">Calculate</button>
        <div id="bc-out" class="tool-result">
          <div class="tool-result-value">—</div>
          <p class="tool-result-label">Recommended monthly ad budget</p>
        </div>
      </div>
    </section>

    <h2 id="marketing-mix">The &ldquo;marketing mix&rdquo;</h2>
    <p>The &ldquo;marketing mix&rdquo; is a term coined by Neil H. Borden in the 1950s. He based the concept on James Culliton's work, which surveyed consumer goods companies to understand what percentage of marketing budgets they invested into given functions. He found no consistent pattern of investment — each company followed vastly different allocations.</p>
    <blockquote>The marked differences in the patterns or formulae of the marketing programs not only were evident through facts disclosed in case histories, but also were reflected clearly in the figures of a cost study of food manufacturers made by the Harvard Bureau of Business Research in 1929.<br><cite>&mdash; Neil H. Borden, 1952</cite></blockquote>
    <p>Borden made no recommendation on specific budget allocation percentages. He instead assembled a list of &ldquo;Market Forces Bearing on the Marketing Mix&rdquo; and advised how a company could best react to these forces with marketing activities.</p>
    <p>There is no exact &ldquo;best practice&rdquo; as to what percentage of an ad budget belongs in PPC vs. SEM or influencer vs. snail mail. Instead, the marketing-mix concept gives us a framework with which to work out budgets ourselves.</p>
    <blockquote>When building a marketing program to fit the needs of his firm, the marketing manager has to weigh the behavioral forces and then juggle marketing elements in his mix with a keen eye on the resources with which he has to work.<br><cite>&mdash; Neil H. Borden, 1952</cite></blockquote>

    <h2 id="borden-article">Full Neil H. Borden article</h2>
    <p>Check out &ldquo;The Concept of the Marketing Mix&rdquo; article in its entirety below. This was printed in <em>Science in Marketing</em>, George Schwartz (Ed.), New York: John Wiley, 1964.</p>
    <ul>
      <li><a href="https://www.guillaumenicaise.com/wp-content/uploads/2013/10/Borden-1984_The-concept-of-marketing-mix.pdf" target="_blank" rel="noopener">guillaumenicaise.com — PDF</a></li>
      <li><a href="https://www.academia.edu/27614102/The_Concept_of_the_Marketing_Mix" target="_blank" rel="noopener">academia.edu</a></li>
      <li><a href="https://www.semanticscholar.org/paper/The-Concept-of-the-Marketing-Mix-Borden/2d61882eb93dc912dd50d21c3307edd8c650eefd" target="_blank" rel="noopener">semanticscholar.org</a></li>
    </ul>""",
    },
    {
        "slug": "google-ads-customer-match-lists",
        "title": "Customer Match Lists",
        "lead": "Upload customer data (hashed first name, last name, email, phone, and zip) into Google Ads in minutes — then use those lists to target similar customers across YouTube, Display, and Search.",
        "meta_description": "Learn how to use and create Customer Match lists in Google Ads to target existing and similar customers across YouTube, Display, and Search campaigns.",
        "date": "Apr 7, 2023",
        "feature_image": "images/1_Customer_Match_Lists.png",
        "feature_alt": "Customer match list on Google Ads",
        "categories": [("Google Ads", "google-ads"), ("Video Guides and Training", "video-guides")],
        "video_embed": "https://www.youtube.com/embed/0pcwj39GmW4",
        "video_watch_url": "https://youtu.be/0pcwj39GmW4",
        "toc": [
            ("customer-match", "Customer match?"),
            ("how-is-one-matched", "How is one matched?"),
            ("what-happens-to-matched", "What happens to matched customers?"),
            ("how-do-i-set-this-up", "How do I set this up?"),
            ("strategy", "Strategy"),
            ("considerations", "Considerations"),
        ],
        "body_html": """    <p>Upload your customer data (first name, last name, email, phone number, and zip code) via a secure, hashed process in the Google Ads interface in minutes. I'll speak to ecommerce advertisers — but the principle and guide apply to lead generation advertisers as well.</p>
    <p><em>Not all Google Ads accounts are eligible to use Customer Match lists. Your ad account must meet the requirements listed in </em><a href="https://support.google.com/adspolicy/answer/6299717" target="_blank" rel="noopener">Google's policy</a><em>. As of March 2023, requirements include: &ldquo;90 days of history in Google Ads and more than USD $50,000 lifetime spend.&rdquo;</em></p>

    <h2 id="customer-match">Customer match?</h2>
    <p>A customer match list is a list of &ldquo;matched&rdquo; customers. Specifically, &ldquo;matched&rdquo; means that Google knows who these users are. How does Google know? Take a hypothetical customer named James Jackson. James has just purchased a $100 product from your ecommerce store. Now you want to advertise to more people like James in your Google Ads account, so you create a customer match list and upload some of James's contact information (first name, last name, email, phone number, and zip code). What happens then?</p>

    <h2 id="how-is-one-matched">How is one matched?</h2>
    <p>First, Google &ldquo;matches&rdquo; your contact info from James to a Google-known piece of contact information. For example, if James uses his Gmail email address on your website to make a purchase, Google can &ldquo;match&rdquo; that email address to his YouTube and Gmail accounts for which he uses the same email address. Google now <em>knows</em> who James is.</p>

    <h2 id="what-happens-to-matched">What happens to matched customers?</h2>
    <p>Next, based on James's use of these other Google products (google.com, Gmail, and YouTube), Google can determine who else might be similar to James in purchase behavior. Google can now target those people who are similar to James with your Google Ads.</p>

    <h2 id="how-do-i-set-this-up">How do I set this up?</h2>
    <p>View a video walk-through of this process on <a href="https://youtu.be/0pcwj39GmW4" target="_blank" rel="noopener">YouTube</a> or in the embedded player at the top of this page. To see the audience interface, go to your audience segments manager, then click into a Customer Match list.</p>

    <h2 id="strategy">Strategy</h2>
    <p>Once you've added Customer Match lists, smart bidding will use them by default to inform your campaigns. For example, Performance Max campaigns always use smart bidding and therefore always take your Customer Match lists into account.</p>
    <p>However, if you create a &ldquo;high-value&rdquo; Customer Match list, you can specifically add this to audience signals in Performance Max — or to YouTube, Display, and Search campaigns — to directly tell Google to target these audiences. Alternatively, you can exclude a &ldquo;past purchasers&rdquo; Customer Match list from a campaign that targets new-to-brand audiences with a first-time customer coupon. The options are endless.</p>

    <h2 id="considerations">Considerations</h2>
    <p>Stop and think about what messaging makes sense to which audiences. It's better <em>not</em> to target recent purchasers in your Customer Match list with a 10% discount coupon. Seeing a coupon right after you completed a purchase without said coupon would give any shopper buyer's remorse.</p>
    <ul>
      <li><a href="https://support.google.com/google-ads/answer/6379332?hl=en" target="_blank" rel="noopener">About Customer Match</a></li>
      <li><a href="https://support.google.com/google-ads/answer/10550383" target="_blank" rel="noopener">Your guide to Customer Match</a></li>
    </ul>""",
    },
    {
        "slug": "edit-youtube-ads-for-success",
        "title": "Edit YouTube Ads for Success: What Makes a Successful YouTube Video Ad?",
        "lead": "YouTube is the 2nd-largest search engine after Google. Video ads fall flat if they aren't edited to align with YouTube's short, repetitive ad placements. Here's a starter map.",
        "meta_description": "Practical edit guidance for YouTube Bumper, Non-Skippable, and Skippable video ads — lengths, framing, pacing, and CTA placement.",
        "date": "Aug 31, 2021",
        "feature_image": "images/2_Successful_YouTube_Ad.png",
        "feature_alt": "How to edit YouTube ads for success",
        "categories": [("YouTube", "youtube")],
        "video_embed": None,
        "toc": [
            ("video-lengths", "Video lengths"),
            ("bumper-ads", "Bumper Ads (6 seconds)"),
            ("non-skippable-ads", "Non-Skippable (15 seconds)"),
            ("skippable-ads", "Skippable (15+ seconds)"),
            ("components", "Components of successful video ads"),
            ("summary", "Summary"),
            ("additional-resources", "Additional resources"),
        ],
        "body_html": """    <p><em>This article gives video producers introductory information on creating video ads for YouTube.</em></p>
    <p>Effective YouTube video ads often come in a collection of 6, 15, and 15+ second lengths. This &ldquo;collection&rdquo; is shown to potential customers across YouTube and non-YouTube online placements. Having multiple lengths allows the advertiser to reach customers in multiple scenarios. A potential customer briefly browsing on their phone while waiting in a line can view an entire 6-second ad. Later, at home, that same person might be receptive to a longer 60-second ad.</p>
    <p>Start with video ads that fit YouTube's three most common video ad slots: <strong>Bumper</strong> (6 seconds), <strong>Non-Skippable</strong> (15 seconds), and <strong>Skippable</strong> (15+ seconds).</p>

    <h2 id="video-lengths">Video lengths</h2>
    <ul>
      <li>Bumper Ads (6 seconds)</li>
      <li>Non-Skippable Ads (15 seconds)</li>
      <li>Skippable Ads (15+ seconds)</li>
    </ul>

    <h2 id="bumper-ads">Bumper Ads (6 seconds)</h2>
    <p>Bumper ads are non-skippable — the user must watch the entire ad. Apart from being 6 seconds long and non-skippable, Bumper ads have three things in common:</p>
    <ol>
      <li>Fast pacing; that is, cut from scene to scene quickly.</li>
      <li>Tight framing around faces and products.</li>
      <li>An exceptionally simple message.</li>
    </ol>
    <p>Most importantly, bumper video ads cannot exceed 6 seconds, not even by 1 millisecond. Otherwise Google Ads won't accept them as a &ldquo;bumper ad,&rdquo; meaning a &ldquo;Skip ad&rdquo; button will still appear on your 00:06:01 length video.</p>

    <h2 id="non-skippable-ads">Non-Skippable (15 seconds)</h2>
    <p>Non-Skippable video ads force the user to watch the entirety of the video ad. That's a big ask on YouTube, and that's why 15 seconds is the maximum length of this format. These ads are a great opportunity to restate the same message from 6-second Bumper ads, but with new information or a more detailed call to action.</p>

    <h2 id="skippable-ads">Skippable (15+ seconds)</h2>
    <p>Skippable video ads allow users to click the &ldquo;skip now&rdquo; button after watching the first 5 seconds. A benefit of this format is that advertisers get to deliver their message within those first 5 seconds — and as a bonus, expand on that message should the user choose not to skip. Of all the ad types, this one should be the most front-loaded because the goal is to convince the viewer to continue watching past the &ldquo;skip now&rdquo; button.</p>

    <h2 id="components">Components of successful video ads</h2>
    <ol>
      <li>Use tight framing so that even users on small mobile devices can clearly see the subject.</li>
      <li>Make fast-paced videos to keep attention.</li>
      <li>Use human actors to keep ads interesting (graphic-only ads are uninspiring and not memorable).</li>
      <li>Build your &ldquo;collection&rdquo; of video ads with <strong>one message</strong> in mind (e.g., &ldquo;Lowest Prices&rdquo; or &ldquo;Biggest Selection&rdquo;).</li>
      <li>Drive home the same message across all your ad lengths.</li>
    </ol>
    <p>Potential customers will remember just one message. Avoid highlighting &ldquo;low prices&rdquo; in 6-second ads and &ldquo;best selection&rdquo; in 15-second ads. Stick to one message across all videos, expanding on the message in longer video ads.</p>

    <h2 id="summary">Summary</h2>
    <p>A collection of video ads of various lengths is more effective than a single, long-format video ad. Effective video ads use tight framing, fast pacing, and simple messages. A call to action is essential for 15- and 15+-second video ads. Focus on a single message throughout all video ad lengths.</p>

    <h2 id="additional-resources">Additional resources</h2>
    <ul>
      <li><a href="https://www.youtube.com/intl/en_us/ads/resources/creative-resources/" target="_blank" rel="noopener">Learn &ldquo;How&rdquo; to Make Great Video Ads for YouTube</a></li>
      <li><a href="https://www.youtube.com/intl/en_us/ads/resources/creative-directory/" target="_blank" rel="noopener">A Directory of Google-Approved Video Production Partners</a></li>
    </ul>""",
    },
    {
        "slug": "display-ads-an-introduction-for-graphic-designers",
        "title": "Display Ads: An Introduction for Graphic Designers",
        "lead": "Understand what display ads are, what makes an exceptional display ad, and how the Google Display Network functions.",
        "meta_description": "Display ad specs, dimensions, and creative best practices for graphic designers preparing static and animated image ads for Google Ads.",
        "date": "Aug 20, 2021",
        "feature_image": "images/3_Display_Ads.png",
        "feature_alt": "Display ads guide for Google Ads",
        "categories": [("Research Articles", "research-articles")],
        "video_embed": None,
        "toc": [
            ("ad-specs-dimensions", "Ad specs &amp; dimensions"),
            ("animated-display-ads", "Animated display ads"),
            ("successful-display-ad", "What makes a successful display ad"),
            ("display-summary", "Summary"),
            ("display-resources", "Additional resources"),
        ],
        "body_html": """    <p><em>Graphic designers can use this article in preparation to create static and animated image ads for Google Ads.</em></p>
    <p>The Google Display Network (GDN) broadcasts image ads across the internet. You see GDN ads on blogs, news websites, and some YouTube locations. Think of the last recipe blog you browsed for a cookie recipe — it was probably packed with ads. Those ads are served on the GDN.</p>
    <p>You probably became annoyed with so many GDN ads loading on that recipe blog. Display ads can certainly be intrusive — that's why making a beautiful ad with a great call-to-action is essential. Exceptional display ads use:</p>
    <ul>
      <li>Clean design</li>
      <li>Readable text</li>
      <li>Pleasant imagery</li>
      <li>A call to action (CTA) that offers value</li>
    </ul>
    <p>A professional graphic designer can easily apply their skills to GDN ads after learning a few essentials: <strong>file specifications</strong> (dimensions, size limits — always 150KB), <strong>creative best practices</strong>, and <strong>static</strong> and <strong>animated formats</strong>.</p>

    <h2 id="ad-specs-dimensions">Ad specs &amp; dimensions</h2>
    <h3>Ad specs</h3>
    <p>Short and sweet: all display ads must be 150KB or smaller. Creativity can still thrive under such limitations.</p>
    <ul>
      <li>Make files 150KB or less</li>
      <li>Save static display ads as PNGs</li>
    </ul>

    <h3>14 common dimensions</h3>
    <p>The below dimensions are used in English-speaking countries. <strong>You only need the 14 most common dimensions</strong> in most cases.</p>
    <ul>
      <li><strong>Skyscraper:</strong> 120×600, 160×600, 300×600</li>
      <li><strong>Square and Rectangle:</strong> 200×200, 250×250, 300×250, 336×280</li>
      <li><strong>Leaderboard:</strong> 468×60, 728×90, 970×90, 970×250</li>
      <li><strong>Mobile:</strong> 300×50, 320×50, 320×100</li>
    </ul>
    <p>Other ad dimensions are used in different countries: e.g., if you run ads in Poland, you'll need a unique 750×100 billboard ad. See the full list at <a href="https://support.google.com/google-ads/answer/1722096?hl=en" target="_blank" rel="noopener">Google's documentation</a>.</p>

    <h2 id="animated-display-ads">Animated display ads</h2>
    <p>Animated display ads are exceptional; they increase the available space for your message, capture attention, and provide an opportunity to attract and inspire customers with art. These are called &ldquo;HTML5&rdquo; or &ldquo;AMPHTML&rdquo; ads, made in <a href="https://support.google.com/webdesigner/answer/3184833" target="_blank" rel="noopener">Google Web Designer</a>.</p>
    <p>It's not uncommon for a professional graphic designer to charge anywhere from <strong>$150 USD</strong> to <strong>$1,500 USD</strong> for a set of animated display ads in the 14 common dimensions.</p>

    <h2 id="successful-display-ad">What makes a successful display ad</h2>
    <p>Your display ad call-to-action and ad copy should match the current promotion campaign or offer. CTAs that make an offer are extremely useful on display ads — especially in display ads that are meant to lead directly to a sale. A free trial or 15%+ discount is typically seen as valuable.</p>
    <ul>
      <li>Free 30-Day Trial</li>
      <li>4th of July Sale &mdash; Take 15% Off Till 07/04</li>
      <li>15% Off Your First Order</li>
    </ul>
    <p>Not all ads must include a sale or discount offer. Awareness-generating ads include compelling information about the product offer. Importantly, weave a somewhat subtle CTA, such as &ldquo;free home delivery,&rdquo; into the ad copy.</p>

    <h3>The CTA button</h3>
    <p>Display ads end with CTA buttons. Some ideas for CTA button text: &ldquo;Shop now,&rdquo; &ldquo;Sign Up,&rdquo; or &ldquo;Get Free Trial.&rdquo; Two words is ideal; three words is the maximum.</p>

    <h2 id="display-summary">Summary</h2>
    <p>Google's documentation nearly says it all. If you haven't already, read their materials as your next step.</p>

    <h2 id="display-resources">Additional resources</h2>
    <ul>
      <li><a href="https://support.google.com/google-ads/answer/9823397?hl=en" target="_blank" rel="noopener">Creative Best Practices</a></li>
      <li><a href="https://support.google.com/google-ads/answer/1722134?hl=en" target="_blank" rel="noopener">Tips for Creating Effective Display Ads</a></li>
      <li><a href="https://support.google.com/webdesigner/answer/3184833" target="_blank" rel="noopener">Make animated (HTML5/AMPHTML) Display Ads</a></li>
      <li><a href="http://www.richmediagallery.com/" target="_blank" rel="noopener">Animated Display Ad Example Gallery</a></li>
      <li><a href="https://lineardesign.com/blog/display-ad-examples/" target="_blank" rel="noopener">Static Display Ad Example Gallery</a></li>
    </ul>""",
    },
]


def _blog_eyebrow(art: dict) -> str:
    if art.get("eyebrow"):
        return art["eyebrow"]
    cat = art["categories"][0][0] if art.get("categories") else "Resource"
    return f"Free Guide &middot; {cat}"


def _blog_hero_media(art: dict, rel: str) -> str:
    if art.get("video_embed"):
        return f"""    <div class="hero-video">
      <div class="video-frame">
        <iframe src="{art['video_embed']}" title="{art['title']}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
      </div>
    </div>"""
    return f"""    <div class="hero-video">
      <img src="{rel}{art['feature_image']}" alt="{art['feature_alt']}" class="guide-hero-image">
    </div>"""


def _blog_hero_actions(art: dict) -> str:
    toc = art.get("toc")
    cta_href = art.get("hero_cta_href")
    if not cta_href:
        cta_href = f"#{toc[0][0]}" if toc else "#article-body"
    default_label = "Get Started" if toc else "Read the Guide"
    cta_label = art.get("hero_cta_label", default_label)
    actions = [f'        <a href="{cta_href}" class="btn btn-dark">{cta_label}</a>']
    watch = art.get("video_watch_url")
    if watch:
        actions.append(
            f'        <a href="{watch}" target="_blank" rel="noopener" class="hero-arrow-link">Watch on YouTube <span aria-hidden="true">&rsaquo;</span></a>'
        )
    return "\n".join(actions)


def _blog_toc_html(toc: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f'          <li><a href="#{anchor}">{label}</a></li>' for anchor, label in toc
    )
    return f"""    <aside class="guide-toc-sidebar">
      <nav class="guide-toc" aria-label="Table of contents">
        <h2>Table of contents</h2>
        <ol>
{items}
        </ol>
      </nav>
    </aside>"""


def _content_gate_html() -> str:
    return """    <div class="content-gate" id="content-gate">
      <div class="content-gate-form-wrap">
        <div id="content-gate-form" class="content-gate-form"></div>
      </div>
    </div>"""


def _gated_body_html(art: dict) -> str:
    preview = art.get("preview_html", "")
    gated = art.get("gated_body_html", "")
    toc = art.get("toc")
    gate = _content_gate_html()
    preview_block = f"""    <div class="content-gate-preview content-gate-preview--faded">
{preview}
    </div>
{gate}
    <div class="gated-content" id="gated-content" hidden>
{gated}
      <div class="content-gate-success" id="content-gate-success" hidden></div>
    </div>"""
    if not toc:
        return f"""<section class="article-body" id="article-body">
  <div class="container">
{preview_block}
  </div>
</section>"""
    toc_sidebar = _blog_toc_html(toc)
    return f"""<section class="article-body article-body--with-toc" id="article-body">
  <div class="container guide-body-split">
{toc_sidebar}
    <div class="guide-body-content">
{preview_block}
    </div>
  </div>
</section>"""


def _blog_body_section(art: dict) -> str:
    if art.get("gated"):
        return _gated_body_html(art)
    body = art["body_html"]
    toc = art.get("toc")
    if not toc:
        return f"""<section class="article-body" id="article-body">
  <div class="container">
{body}
  </div>
</section>"""
    toc_sidebar = _blog_toc_html(toc)
    return f"""<section class="article-body article-body--with-toc" id="article-body">
  <div class="container guide-body-split">
{toc_sidebar}
    <div class="guide-body-content">
{body}
    </div>
  </div>
</section>"""


def _article_schema_html(art: dict) -> str:
    video_url = art.get("video_embed")
    return article_schema(
        slug=art["slug"],
        title=art["title"],
        description=art["meta_description"],
        date=art["date"],
        image_path=art["feature_image"],
        video_url=video_url,
        faqs=art.get("faqs"),
    )


GATED_GUIDES = [
    {
        "slug": "conversion-tracking-shopify-2026",
        "title": "Streamlined Conversion Tracking for Shopify 2026",
        "lead": "Set up Google Ads and Microsoft Ads conversion tracking on Shopify using Customer Events &mdash; without editing theme.liquid. Watch the video, then unlock the full written checklist.",
        "meta_description": "2026 Shopify conversion tracking guide: Google & YouTube Sales Channel, Microsoft Sales Channel, primary conversion setup, and optional GTM steps.",
        "date": "May 7, 2026",
        "feature_image": "images/Shopify-Conversion-Tracking-2025.png",
        "feature_alt": "Streamlined Conversion Tracking for Shopify 2026",
        "video_embed": "https://www.youtube.com/embed/dL_jtZz8uQQ",
        "video_watch_url": "https://www.youtube.com/watch?v=dL_jtZz8uQQ",
        "toc": [
            ("installation", "Installation"),
            ("microsoft-ads", "Microsoft Ads"),
            ("last-steps", "Last steps"),
            ("optional-steps", "Optional custom events"),
            ("resources-cited", "Resources cited"),
        ],
        "preview_html": CONV_TRACKING_PREVIEW,
        "gated_body_html": CONV_TRACKING_GATED,
    },
]


def render_gated_guide(guide: dict) -> str:
    rel = "../"
    art = {
        **guide,
        "gated": True,
        "body_html": guide["preview_html"] + guide["gated_body_html"],
        "hero_cta_href": "#content-gate",
        "hero_cta_label": "Get the Guide",
        "categories": [("Google Ads", "google-ads")],
    }
    eyebrow = _blog_eyebrow(art)
    hero_media = _blog_hero_media(art, rel)
    hero_actions = _blog_hero_actions(art)
    schema = guide_schema(
        slug=guide["slug"],
        title=guide["title"],
        description=guide["meta_description"],
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{guide['title']} — Austin Becker E-Commerce Marketing</title>
<meta name="description" content="{guide['meta_description']}">
<meta property="og:title" content="{guide['title']}">
<meta property="og:description" content="{guide['meta_description']}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://abeckermarketing.com/{guide['feature_image']}">
<link rel="canonical" href="https://abeckermarketing.com/guides/{guide['slug']}.html">
{schema}
<link rel="stylesheet" href="../styles.css">
</head>
<body>

{header(rel, active="learn")}

<section class="hero">
  <div class="container hero-split">
    <div class="hero-text">
      <span class="eyebrow">{eyebrow}</span>
      <h1>{guide['title']}</h1>
      <p class="lead">{guide['lead']}</p>
      <div class="hero-actions">
{hero_actions}
      </div>
    </div>
{hero_media}
  </div>
</section>

{_gated_body_html(art)}

{blog_newsletter(rel)}

{footer(rel)}
<script src="../scripts/guide-image-lightbox.js" defer></script>
<script src="../scripts/newsletter-form.js" defer></script>
<script src="../scripts/content-gate.js" defer></script>
</body>
</html>
"""


def render_article(art: dict, all_articles: list) -> str:
    del all_articles  # related resources removed from blog template
    rel = "../"
    eyebrow = _blog_eyebrow(art)
    hero_media = _blog_hero_media(art, rel)
    hero_actions = _blog_hero_actions(art)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{art['title']} — Austin Becker E-Commerce Marketing</title>
<meta name="description" content="{art['meta_description']}">
<meta property="og:title" content="{art['title']}">
<meta property="og:description" content="{art['meta_description']}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://abeckermarketing.com/{art['feature_image']}">
<link rel="canonical" href="https://abeckermarketing.com/resources/{art['slug']}.html">
{_article_schema_html(art)}
<link rel="stylesheet" href="../styles.css">
</head>
<body>

{header(rel, active="learn")}

<section class="hero">
  <div class="container hero-split">
    <div class="hero-text">
      <span class="eyebrow">{eyebrow}</span>
      <h1>{art['title']}</h1>
      <p class="lead">{art['lead']}</p>
      <div class="hero-actions">
{hero_actions}
      </div>
    </div>
{hero_media}
  </div>
</section>

{_blog_body_section(art)}

{blog_newsletter(rel)}

{footer(rel)}
<script src="../scripts/guide-image-lightbox.js" defer></script>
<script src="../scripts/newsletter-form.js" defer></script>
{"<script src=\"../scripts/content-gate.js\" defer></script>" if art.get("gated") else ""}
</body>
</html>
"""

# ============================================================
# WRITE FILES
# ============================================================

def main():
    case_dir = SITE_ROOT / "case-studies"
    case_dir.mkdir(exist_ok=True)
    for cs in CASE_STUDIES:
        (case_dir / f"{cs['slug']}.html").write_text(render_case_study(cs))
        print(f"wrote case-studies/{cs['slug']}.html")

    res_dir = SITE_ROOT / "resources"
    res_dir.mkdir(exist_ok=True)
    for art in RESOURCES:
        (res_dir / f"{art['slug']}.html").write_text(render_article(art, RESOURCES))
        print(f"wrote resources/{art['slug']}.html")

    guide_dir = SITE_ROOT / "guides"
    guide_dir.mkdir(exist_ok=True)
    for guide in GATED_GUIDES:
        (guide_dir / f"{guide['slug']}.html").write_text(render_gated_guide(guide))
        print(f"wrote guides/{guide['slug']}.html")


if __name__ == "__main__":
    main()
