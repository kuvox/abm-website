#!/usr/bin/env python3
"""
Generates case study and resource article HTML pages from a data table,
following the templates documented in docs/PAGE_PATTERNS.md.

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

from schema.jsonld import article_schema, case_study_schema

# ---------- shared header / footer (rel-prefix aware) ----------

def header(rel: str) -> str:
    return f"""<header class="site-header">
  <div class="container nav">
    <a href="{rel}index.html" class="brand-mark" aria-label="Austin Becker E-Commerce Marketing"><img src="{rel}images/logo.svg" alt="Austin Becker E-Commerce Marketing" class="brand-logo"></a>
    <button class="menu-toggle" aria-label="Toggle menu" onclick="document.getElementById('navlinks').classList.toggle('open')">☰</button>
    <ul id="navlinks" class="nav-links">
      <li class="has-menu has-megamenu has-megamenu--services"><a href="{rel}index.html#services">Services</a>
        <div class="megamenu megamenu--services">
          <div class="megamenu-col">
            <span class="megamenu-eyebrow">Our Services</span>
            <ul>
              <li><a href="{rel}services/google-shopping-ads.html">Google Shopping Ads</a></li>
              <li><a href="{rel}services/google-search-ads.html">Google Search Ads</a></li>
              <li><a href="{rel}services/google-display-network.html">Google Display Network</a></li>
              <li><a href="{rel}services/amazon-ads.html">Amazon Ads</a></li>
            </ul>
          </div>
          <div class="megamenu-col">
            <ul>
              <li><a href="{rel}services/product-feeds.html">Product Feeds</a></li>
              <li><a href="{rel}services/microsoft-ads.html">Microsoft Ads</a></li>
              <li><a href="{rel}services/youtube-ads.html">YouTube Ads</a></li>
            </ul>
          </div>
          <a href="{rel}contact.html" class="megamenu-cta-card">
            <h4>Contact Us to Get a Proposal</h4>
            <p>Please submit a contact form. We&rsquo;ll reach out to see if our team is a good fit for your business.</p>
            <span class="megamenu-cta-arrow" aria-hidden="true">&rarr;</span>
          </a>
        </div>
      </li>
      <li><a href="{rel}case-studies.html">Case Studies</a></li>
      <li class="has-menu has-megamenu has-megamenu--resources"><a href="{rel}resources.html">Resources</a>
        <div class="megamenu megamenu--resources">
          <div class="megamenu-col">
            <ul>
              <li><a href="{rel}resources.html#featured">Featured Resources</a></li>
              <li><a href="{rel}resources.html#research">Research Articles</a></li>
              <li><a href="{rel}resources.html#video">Video Guides and Training</a></li>
              <li><a href="{rel}resources.html#support">Support Articles</a></li>
            </ul>
          </div>
          <div class="megamenu-col">
            <span class="megamenu-eyebrow">Resources by Topic</span>
            <ul>
              <li><a href="{rel}resources.html#amazon">Amazon</a></li>
              <li><a href="{rel}resources.html#google-ads">Google Ads</a></li>
              <li><a href="{rel}resources.html#google-shopping">Google Shopping</a></li>
              <li><a href="{rel}resources.html#microsoft">Microsoft</a></li>
              <li><a href="{rel}resources.html#product-feeds">Product Feeds</a></li>
              <li><a href="{rel}resources.html#youtube">YouTube</a></li>
            </ul>
          </div>
          <div class="megamenu-card">
            <a href="https://abeckermarketing.com/get-free-guides-here/" target="_blank" rel="noopener">
              <img src="{rel}images/Weekly-Guides-on-YouTube.png" alt="Weekly Guides on YouTube">
              <span class="megamenu-card-cta">Get Free Guides Here &rsaquo;</span>
            </a>
          </div>
        </div>
      </li>
      <li class="has-menu has-megamenu has-megamenu--about"><a href="{rel}about.html">About</a>
        <div class="megamenu megamenu--about">
          <div class="megamenu-col">
            <ul>
              <li><a href="{rel}about.html#why-choose-us">Why choose us?</a></li>
              <li><a href="{rel}about.html#founder">About the Founder</a></li>
              <li><a href="{rel}about.html#team">Our Team</a></li>
            </ul>
          </div>
          <div class="megamenu-col megamenu-col--text">
            <span class="megamenu-eyebrow">About Us</span>
            <p>An e-commerce, growth-focused team, equipped to work with $5M-$50M annual revenue companies. If your product catalog is large, complex or niche, we are the right choice for you.</p>
          </div>
        </div>
      </li>
      <li><a href="{rel}contact.html" class="nav-cta">Contact Us</a></li>
    </ul>
  </div>
</header>"""

SOCIAL_ICONS = """<a href="https://www.linkedin.com/in/austin-becker-marketing/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg></a>
            <a href="https://www.facebook.com/ABeckerMarketing" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.69.24 2.69.24v2.97h-1.52c-1.49 0-1.95.93-1.95 1.89v2.26h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07z"/></svg></a>
            <a href="https://x.com/MktngByABecker" target="_blank" rel="noopener" aria-label="X (Twitter)"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
            <a href="https://www.youtube.com/@ppcforeveryone" target="_blank" rel="noopener" aria-label="YouTube"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23.5 6.2a3 3 0 0 0-2.13-2.13C19.5 3.56 12 3.56 12 3.56s-7.5 0-9.37.51A3 3 0 0 0 .5 6.2 31.4 31.4 0 0 0 0 12a31.4 31.4 0 0 0 .5 5.8 3 3 0 0 0 2.13 2.13c1.87.51 9.37.51 9.37.51s7.5 0 9.37-.51A3 3 0 0 0 23.5 17.8 31.4 31.4 0 0 0 24 12a31.4 31.4 0 0 0-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/></svg></a>"""

def footer(rel: str) -> str:
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <h4>Austin Becker E-Commerce Marketing</h4>
        <p>We help $5M to $50M annual revenue businesses grow via pay per click ads. Contact us today to learn how we can help you grow your business.</p>
        <div class="social-icons">
            {SOCIAL_ICONS}
        </div>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="{rel}services/google-shopping-ads.html">Google Shopping Ads</a></li>
          <li><a href="{rel}services/google-search-ads.html">Google Search Ads</a></li>
          <li><a href="{rel}services/google-display-network.html">Display Network</a></li>
          <li><a href="{rel}services/amazon-ads.html">Amazon Ads</a></li>
          <li><a href="{rel}services/product-feeds.html">Product Feeds</a></li>
          <li><a href="{rel}services/microsoft-ads.html">Microsoft Ads</a></li>
          <li><a href="{rel}services/youtube-ads.html">YouTube Ads</a></li>
        </ul>
      </div>
      <div>
        <h4>About</h4>
        <ul>
          <li><a href="{rel}about.html#why-choose-us">Why Choose Us</a></li>
          <li><a href="{rel}about.html#founder">About the Founder</a></li>
          <li><a href="{rel}about.html#team">Our Team</a></li>
        </ul>
      </div>
      <div>
        <h4>Resources</h4>
        <ul>
          <li><a href="{rel}case-studies.html">Case Studies</a></li>
          <li><a href="{rel}resources.html">Research Articles</a></li>
          <li><a href="{rel}resources.html">Video Guides and Training</a></li>
          <li><a href="{rel}resources.html">Support Articles</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>Copyright &copy; 2026 Austin Becker E-Commerce Marketing. All Rights Reserved.</span>
      <div class="footer-bottom-links">
        <a href="{rel}privacy-policy.html">Privacy Policy</a>
        <a href="{rel}service-agreement.html">Service Agreement</a>
        <span>Website by Kern Co.</span>
      </div>
    </div>
  </div>
</footer>"""

# ---------- case-study contact form (mirrors contact.html) ----------

def contact_form_section(referrer_slug: str) -> str:
    return f"""<section class="case-contact section--alt">
  <div class="container">
    <div>
      <span class="eyebrow">Talk to us</span>
      <h2>Want to work with us?</h2>
      <p class="lead">We&rsquo;re ready to discuss your business and how we can help you grow it. Fill out the form and we&rsquo;ll book a call to learn more about your business.</p>
      <div class="contact-info-block">
        <p class="info-label-inline">Email</p>
        <p><a href="mailto:austin@abeckermarketing.com">austin@abeckermarketing.com</a></p>
        <p class="info-label-inline">Address</p>
        <p>510 S Main St Suite 120, South Bend, IN 46601</p>
      </div>
    </div>
    <div class="form-wrap">
      <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
        <div class="form-row form-row-split">
          <div>
            <label for="first">First Name <span class="req">*</span></label>
            <input id="first" name="first" type="text" required>
          </div>
          <div>
            <label for="last">Last Name <span class="req">*</span></label>
            <input id="last" name="last" type="text" required>
          </div>
        </div>
        <div class="form-row">
          <label for="email">Email <span class="req">*</span></label>
          <input id="email" name="email" type="email" required>
        </div>
        <div class="form-row">
          <label for="phone">Phone</label>
          <input id="phone" name="phone" type="tel">
        </div>
        <div class="form-row">
          <label for="company">Company Name <span class="req">*</span></label>
          <input id="company" name="company" type="text" required>
        </div>
        <div class="form-row">
          <label for="revenue">Annual Revenue</label>
          <select id="revenue" name="revenue">
            <option>1 to 5 million</option>
            <option>5 to 25 million</option>
            <option>25 to 50 million</option>
            <option>50 million +</option>
          </select>
        </div>
        <div class="form-row">
          <label for="budget">Advertising Budget <span class="req">*</span></label>
          <select id="budget" name="budget" required>
            <option>We haven&rsquo;t started yet</option>
            <option>Less than $5,000 / month</option>
            <option>$5,000 - $25,000 / month</option>
            <option>$25,000+ / month</option>
          </select>
        </div>
        <div class="form-row">
          <label for="website">Company Website <span class="req">*</span></label>
          <input id="website" name="website" type="url" placeholder="https://" required>
        </div>
        <div class="form-row">
          <label for="message">Message</label>
          <textarea id="message" name="message"></textarea>
        </div>
        <input type="hidden" name="referrer" value="{referrer_slug}">
        <button type="submit" class="btn btn-primary" style="width:100%;">Submit</button>
      </form>
    </div>
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
        "quote": "Austin collaborates frequently with us to ensure that our online business goals are met. His work has significantly steered our pay per click sales trajectory up over the past years.",
        "quote_author": "Tony Price",
        "quote_title": "Owner &amp; CEO, Murdock Industrial",
    },
    {
        "slug": "iron-fence-shop",
        "client": "Iron Fence Shop",
        "title": "16% Decrease in Google Ad Spend. 221% Increase in Form Leads.",
        "intro": "Iron Fence Shop retails handcrafted and custom-designed perimeter fencing crafted in their own facility — including fencing, driveway gates, and finials constructed of iron and aluminum.",
        "hero_image": "images/iron-fence-shop.jpeg",
        "hero_alt": "Iron Fence Shop case study",
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
        "quote": "Austin matched our product feed and ad campaigns to our business objectives in a way that allowed us to achieve substantial sales growth with seasonal products and new product launches.",
        "quote_author": "Ed Raftery",
        "quote_title": "Founder &amp; CEO, TrailHeads",
    },
    {
        "slug": "parker-baby",
        "client": "Parker Baby Co.",
        "title": "Increased Return on Ad Spend Within 3 Weeks",
        "intro": "Parker Baby designs and provides exceptional and affordable baby products for the modern parent. Since 2015, they've specialized in diaper backpacks, caddies, bath supplies, and other baby accessories.",
        "hero_image": "images/Parker-Baby-bag.jpeg",
        "hero_alt": "Parker Baby diaper bag",
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
        "quote": "Austin is very responsive and quickly understood our businesses and our goals, and built campaigns to meet those goals.",
        "quote_author": "Sam Huebner",
        "quote_title": "CEO, Parker Baby Co.",
    },
]

def render_case_study(cs: dict) -> str:
    rel = "../"
    what_we_did_html = ""
    if cs["what_we_did"]:
        what_we_did_html = "\n    <h2>What we did</h2>\n" + "\n".join(
            f"    <p>{p}</p>" for p in cs["what_we_did"]
        )
    metric_count = len(cs["metrics"])
    grid_cls = "metric-grid"
    if metric_count == 3:
        grid_cls = "metric-grid metric-grid--three"
    metrics_html = "\n".join(
        f"""      <div class="metric">
        <div class="metric-value">{value}</div>
        <p class="metric-label">{label}</p>
      </div>"""
        for value, label in cs["metrics"]
    )
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

{header(rel)}

<section class="case-hero">
  <div class="container hero-split">
    <div>
      <span class="case-eyebrow">Case Study &middot; {cs['client']}</span>
      <h1>{cs['title']}</h1>
      <p class="case-intro">{cs['intro']}</p>
    </div>
    <div>
      <img src="{rel}{cs['hero_image']}" alt="{cs['hero_alt']}" class="case-hero-image">
    </div>
  </div>
</section>

<section class="case-body">
  <div class="container">
    <h2>Challenge</h2>
    <p>{cs['challenge']}</p>

    <h2>Solution</h2>
    <p>{cs['solution']}</p>{what_we_did_html}
  </div>
</section>

<section class="case-results">
  <div class="container">
    <span class="results-eyebrow">Results</span>
    <h2>What changed for {cs['client']}</h2>
    <div class="{grid_cls}">
{metrics_html}
    </div>
    <div class="client-quote">
      <blockquote>&ldquo;{cs['quote']}&rdquo;</blockquote>
      <cite>{cs['quote_author']}<span class="quote-title">{cs['quote_title']}</span></cite>
    </div>
  </div>
</section>

{contact_form_section(cs['slug'])}

{footer(rel)}
</body>
</html>
"""

# ============================================================
# RESOURCE ARTICLES
# ============================================================

# Each article body uses HTML-as-string. Keep paragraphs short and readable.
RESOURCES = [
    {
        "slug": "shopify-google-merchant-center-setup-2026",
        "title": "2026 Shopify to Google Merchant Center Feed Setup",
        "lead": "Step-by-step checklist for sending Shopify product data into Google Merchant Center in 2026 — without breaking historic sales data tied to your existing product IDs.",
        "meta_description": "Learn how to send a Shopify product feed to Google Merchant Center in 2026, keeping historic sales data and syncing shipping settings automatically.",
        "date": "Feb 11, 2026",
        "feature_image": "images/2026-Product-Feed-Tutorial-light.png",
        "feature_alt": "2026 Product Feed Tutorial for Shopify and Google Merchant Center",
        "categories": [("Google Ads", "google-ads"), ("Google Shopping", "google-shopping"), ("Product Feeds", "product-feeds")],
        "video_embed": None,
        "body_html": """    <p>Get the step-by-step <strong>checklist below</strong>. The checklist includes all necessary steps and instructions to quickly send a product data feed from Shopify to Google Merchant Center.</p>
    <p>With this method you will:</p>
    <ol>
      <li>Avoid losing historic sales data associated with your old product feed's product IDs,</li>
      <li>Send a product data feed for free, or with our recommended 3rd-party product data feed tool DataFeedWatch,</li>
      <li>Sync all your Shopify shipping settings to Google Merchant Center automatically, and</li>
      <li>Have a foundation to start from when optimizing product data for Google Shopping Ads.</li>
    </ol>

    <h2>What you'll need before starting</h2>
    <ul>
      <li>Admin access to your Shopify store</li>
      <li>An active Google Merchant Center account linked to your domain</li>
      <li>Optional: a DataFeedWatch (or comparable feed-management) trial if you want to manage many SKUs in one place</li>
    </ul>

    <h2>The checklist</h2>
    <p>The checklist itself lives alongside the full video walkthrough on YouTube. The high-level moves:</p>
    <ol>
      <li>Decide on your <strong>product ID</strong> strategy. If you've already advertised, preserving the existing IDs (SKU or variant ID) keeps historic learning intact.</li>
      <li>Map Shopify product fields to Google's required attributes: <code>id</code>, <code>title</code>, <code>description</code>, <code>link</code>, <code>image_link</code>, <code>availability</code>, <code>price</code>, <code>brand</code>, and <code>gtin</code> or <code>mpn</code>.</li>
      <li>Connect Shopify shipping to GMC so the price the user sees in the ad reflects real-time shipping rates from your store.</li>
      <li>Validate the feed in GMC and resolve all warnings before launching campaigns.</li>
    </ol>""",
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
        "body_html": """    <h2>What do you mean &ldquo;optimize?&rdquo;</h2>
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

    <h2>How to run a test</h2>
    <p>Testing CTR will yield immediate results, so start with that as your metric.</p>
    <p>Why not test other metrics? You could test number of impressions (more impressions good, less bad) but the problem is that impressions might rise or fall because of factors other than your test variable: increased ad budget, seasonal shopping activity. These would change impressions regardless of your test variable. CTR is a direct indicator of how enticing your shopping ads are, regardless of budget and seasonal changes.</p>

    <h3>Concurrent or consecutive A/B test?</h3>
    <p>You can run A/B tests concurrently (like DataFeedWatch's title A/B test feature, which measures conversion rate changes on your website). However, it's technically hard to test an A/B's impact on CTR because it's not possible to know exactly when version A or B is live when viewing CTR data. A consecutive A/B test is preferable for this reason. The control period is the 30 days before you change a variable. The test period is the 30 days when your variable change is live.</p>

    <h3>Test all or some products?</h3>
    <p>Test changes to all products at once for fast results at the risk of lost ad revenue. Or test a selection of products to allow non-tested products to keep generating sales at the status-quo pace, uninterrupted by your test.</p>

    <h2>Summary and tips</h2>
    <p>While tests can confirm what you already know (e.g., pure white background images always perform best), they can also help you uncover new ideas (e.g., adding &ldquo;Valentine&rdquo; to a product title during Valentine's Day, or &ldquo;Mother&rdquo; during Mother's Day boosts ad revenue).</p>
    <ul>
      <li>Don't bother testing different background images on your products. A pure white background always wins. I don't know why Google offers AI-generated background changes — they muddle up the product image, which is already small and hard to see.</li>
      <li>Make substantial changes, not minor ones. Moving a word in your title from 1st to 2nd position likely won't change anything. E.g., &ldquo;Nike Men's Running Shoes&rdquo; vs. &ldquo;Men's Nike Running Shoes&rdquo; is a wash. But &ldquo;Nike Men's Road and Track Race Running Shoe&rdquo; vs. &ldquo;Nike Men's Running Shoe&rdquo; will likely yield a difference.</li>
      <li>Automate data collection using software like DataFeedWatch or Supermetrics. Otherwise, gathering reports to compare the outcome of your tests will be so laborious that you never get around to it. Everything should be automated.</li>
    </ul>

    <h2>Resources cited</h2>
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
        "body_html": """    <p>Get the step-by-step <strong>checklist below</strong> the video. The checklist includes code and instructions to quickly set up conversion tracking on Shopify sites.</p>
    <p>With this method I avoid adding code to the <code>theme.liquid</code> file in Shopify (so you don't have to worry about another developer wiping your tracking). Instead, tracking code is all contained within Customer Events, which is what Shopify intended for tracking pixels.</p>

    <h2>Why this approach</h2>
    <ul>
      <li>Tracking lives in <strong>Customer Events</strong>, isolated from theme code.</li>
      <li>Enhanced conversion data (hashed email, phone) flows to Google Ads.</li>
      <li><code>item_ID</code> hits fire so Google Ads can attribute revenue at the product level.</li>
      <li>Same pixel approach works for Microsoft Ads with a parallel snippet.</li>
    </ul>

    <h2>What you'll set up</h2>
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
        "body_html": """    <p>&ldquo;What should our budget be?&rdquo; I get this question often. I used to think &ldquo;as much as you can afford.&rdquo; That's not quite right. Here are methodologies — and a calculator below — to help you set an appropriate budget for your business's size, goals, and margins.</p>

    <h2>How much is too much?</h2>
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

    <h2>The &ldquo;marketing mix&rdquo;</h2>
    <p>The &ldquo;marketing mix&rdquo; is a term coined by Neil H. Borden in the 1950s. He based the concept on James Culliton's work, which surveyed consumer goods companies to understand what percentage of marketing budgets they invested into given functions. He found no consistent pattern of investment — each company followed vastly different allocations.</p>
    <blockquote>The marked differences in the patterns or formulae of the marketing programs not only were evident through facts disclosed in case histories, but also were reflected clearly in the figures of a cost study of food manufacturers made by the Harvard Bureau of Business Research in 1929.<br><cite>&mdash; Neil H. Borden, 1952</cite></blockquote>
    <p>Borden made no recommendation on specific budget allocation percentages. He instead assembled a list of &ldquo;Market Forces Bearing on the Marketing Mix&rdquo; and advised how a company could best react to these forces with marketing activities.</p>
    <p>There is no exact &ldquo;best practice&rdquo; as to what percentage of an ad budget belongs in PPC vs. SEM or influencer vs. snail mail. Instead, the marketing-mix concept gives us a framework with which to work out budgets ourselves.</p>
    <blockquote>When building a marketing program to fit the needs of his firm, the marketing manager has to weigh the behavioral forces and then juggle marketing elements in his mix with a keen eye on the resources with which he has to work.<br><cite>&mdash; Neil H. Borden, 1952</cite></blockquote>

    <h2>Full Neil H. Borden article</h2>
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
        "video_embed": None,
        "body_html": """    <p>Upload your customer data (first name, last name, email, phone number, and zip code) via a secure, hashed process in the Google Ads interface in minutes. I'll speak to ecommerce advertisers — but the principle and guide apply to lead generation advertisers as well.</p>
    <p><em>Not all Google Ads accounts are eligible to use Customer Match lists. Your ad account must meet the requirements listed in </em><a href="https://support.google.com/adspolicy/answer/6299717" target="_blank" rel="noopener">Google's policy</a><em>. As of March 2023, requirements include: &ldquo;90 days of history in Google Ads and more than USD $50,000 lifetime spend.&rdquo;</em></p>

    <h2>Customer match?</h2>
    <p>A customer match list is a list of &ldquo;matched&rdquo; customers. Specifically, &ldquo;matched&rdquo; means that Google knows who these users are. How does Google know? Take a hypothetical customer named James Jackson. James has just purchased a $100 product from your ecommerce store. Now you want to advertise to more people like James in your Google Ads account, so you create a customer match list and upload some of James's contact information (first name, last name, email, phone number, and zip code). What happens then?</p>

    <h2>How is one matched?</h2>
    <p>First, Google &ldquo;matches&rdquo; your contact info from James to a Google-known piece of contact information. For example, if James uses his Gmail email address on your website to make a purchase, Google can &ldquo;match&rdquo; that email address to his YouTube and Gmail accounts for which he uses the same email address. Google now <em>knows</em> who James is.</p>

    <h2>What happens to matched customers?</h2>
    <p>Next, based on James's use of these other Google products (google.com, Gmail, and YouTube), Google can determine who else might be similar to James in purchase behavior. Google can now target those people who are similar to James with your Google Ads.</p>

    <h2>How do I set this up?</h2>
    <p>View a video walk-through of this process on <a href="https://youtu.be/0pcwj39GmW4" target="_blank" rel="noopener">YouTube</a>. To see the audience interface, go to your audience segments manager, then click into a Customer Match list.</p>

    <h2>Strategy</h2>
    <p>Once you've added Customer Match lists, smart bidding will use them by default to inform your campaigns. For example, Performance Max campaigns always use smart bidding and therefore always take your Customer Match lists into account.</p>
    <p>However, if you create a &ldquo;high-value&rdquo; Customer Match list, you can specifically add this to audience signals in Performance Max — or to YouTube, Display, and Search campaigns — to directly tell Google to target these audiences. Alternatively, you can exclude a &ldquo;past purchasers&rdquo; Customer Match list from a campaign that targets new-to-brand audiences with a first-time customer coupon. The options are endless.</p>

    <h2>Considerations</h2>
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
        "body_html": """    <p><em>This article gives video producers introductory information on creating video ads for YouTube.</em></p>
    <p>Effective YouTube video ads often come in a collection of 6, 15, and 15+ second lengths. This &ldquo;collection&rdquo; is shown to potential customers across YouTube and non-YouTube online placements. Having multiple lengths allows the advertiser to reach customers in multiple scenarios. A potential customer briefly browsing on their phone while waiting in a line can view an entire 6-second ad. Later, at home, that same person might be receptive to a longer 60-second ad.</p>
    <p>Start with video ads that fit YouTube's three most common video ad slots: <strong>Bumper</strong> (6 seconds), <strong>Non-Skippable</strong> (15 seconds), and <strong>Skippable</strong> (15+ seconds).</p>

    <h2>Video lengths</h2>
    <ul>
      <li>Bumper Ads (6 seconds)</li>
      <li>Non-Skippable Ads (15 seconds)</li>
      <li>Skippable Ads (15+ seconds)</li>
    </ul>

    <h2>Bumper Ads (6 seconds)</h2>
    <p>Bumper ads are non-skippable — the user must watch the entire ad. Apart from being 6 seconds long and non-skippable, Bumper ads have three things in common:</p>
    <ol>
      <li>Fast pacing; that is, cut from scene to scene quickly.</li>
      <li>Tight framing around faces and products.</li>
      <li>An exceptionally simple message.</li>
    </ol>
    <p>Most importantly, bumper video ads cannot exceed 6 seconds, not even by 1 millisecond. Otherwise Google Ads won't accept them as a &ldquo;bumper ad,&rdquo; meaning a &ldquo;Skip ad&rdquo; button will still appear on your 00:06:01 length video.</p>

    <h2>Non-Skippable (15 seconds)</h2>
    <p>Non-Skippable video ads force the user to watch the entirety of the video ad. That's a big ask on YouTube, and that's why 15 seconds is the maximum length of this format. These ads are a great opportunity to restate the same message from 6-second Bumper ads, but with new information or a more detailed call to action.</p>

    <h2>Skippable (15+ seconds)</h2>
    <p>Skippable video ads allow users to click the &ldquo;skip now&rdquo; button after watching the first 5 seconds. A benefit of this format is that advertisers get to deliver their message within those first 5 seconds — and as a bonus, expand on that message should the user choose not to skip. Of all the ad types, this one should be the most front-loaded because the goal is to convince the viewer to continue watching past the &ldquo;skip now&rdquo; button.</p>

    <h2>Components of successful video ads</h2>
    <ol>
      <li>Use tight framing so that even users on small mobile devices can clearly see the subject.</li>
      <li>Make fast-paced videos to keep attention.</li>
      <li>Use human actors to keep ads interesting (graphic-only ads are uninspiring and not memorable).</li>
      <li>Build your &ldquo;collection&rdquo; of video ads with <strong>one message</strong> in mind (e.g., &ldquo;Lowest Prices&rdquo; or &ldquo;Biggest Selection&rdquo;).</li>
      <li>Drive home the same message across all your ad lengths.</li>
    </ol>
    <p>Potential customers will remember just one message. Avoid highlighting &ldquo;low prices&rdquo; in 6-second ads and &ldquo;best selection&rdquo; in 15-second ads. Stick to one message across all videos, expanding on the message in longer video ads.</p>

    <h2>Summary</h2>
    <p>A collection of video ads of various lengths is more effective than a single, long-format video ad. Effective video ads use tight framing, fast pacing, and simple messages. A call to action is essential for 15- and 15+-second video ads. Focus on a single message throughout all video ad lengths.</p>

    <h2>Additional resources</h2>
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

    <h2>Ad specs &amp; dimensions</h2>
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

    <h2>Animated display ads</h2>
    <p>Animated display ads are exceptional; they increase the available space for your message, capture attention, and provide an opportunity to attract and inspire customers with art. These are called &ldquo;HTML5&rdquo; or &ldquo;AMPHTML&rdquo; ads, made in <a href="https://support.google.com/webdesigner/answer/3184833" target="_blank" rel="noopener">Google Web Designer</a>.</p>
    <p>It's not uncommon for a professional graphic designer to charge anywhere from <strong>$150 USD</strong> to <strong>$1,500 USD</strong> for a set of animated display ads in the 14 common dimensions.</p>

    <h2>What makes a successful display ad</h2>
    <p>Your display ad call-to-action and ad copy should match the current promotion campaign or offer. CTAs that make an offer are extremely useful on display ads — especially in display ads that are meant to lead directly to a sale. A free trial or 15%+ discount is typically seen as valuable.</p>
    <ul>
      <li>Free 30-Day Trial</li>
      <li>4th of July Sale &mdash; Take 15% Off Till 07/04</li>
      <li>15% Off Your First Order</li>
    </ul>
    <p>Not all ads must include a sale or discount offer. Awareness-generating ads include compelling information about the product offer. Importantly, weave a somewhat subtle CTA, such as &ldquo;free home delivery,&rdquo; into the ad copy.</p>

    <h3>The CTA button</h3>
    <p>Display ads end with CTA buttons. Some ideas for CTA button text: &ldquo;Shop now,&rdquo; &ldquo;Sign Up,&rdquo; or &ldquo;Get Free Trial.&rdquo; Two words is ideal; three words is the maximum.</p>

    <h2>Summary</h2>
    <p>Google's documentation nearly says it all. If you haven't already, read their materials as your next step.</p>

    <h2>Additional resources</h2>
    <ul>
      <li><a href="https://support.google.com/google-ads/answer/9823397?hl=en" target="_blank" rel="noopener">Creative Best Practices</a></li>
      <li><a href="https://support.google.com/google-ads/answer/1722134?hl=en" target="_blank" rel="noopener">Tips for Creating Effective Display Ads</a></li>
      <li><a href="https://support.google.com/webdesigner/answer/3184833" target="_blank" rel="noopener">Make animated (HTML5/AMPHTML) Display Ads</a></li>
      <li><a href="http://www.richmediagallery.com/" target="_blank" rel="noopener">Animated Display Ad Example Gallery</a></li>
      <li><a href="https://lineardesign.com/blog/display-ad-examples/" target="_blank" rel="noopener">Static Display Ad Example Gallery</a></li>
    </ul>""",
    },
]


def render_article(art: dict, all_articles: list) -> str:
    rel = "../"
    # Categories
    cats_html = "\n".join(
        f'      <a class="pill-tag" href="{rel}resources.html#{slug}">{name}</a>'
        for (name, slug) in art["categories"]
    )
    cats_footer_html = ", ".join(
        f'<a href="{rel}resources.html#{slug}">{name}</a>'
        for (name, slug) in art["categories"]
    )
    # Related: pick up to 3 others sharing a category, else fall back to most-recent
    related = []
    art_cat_slugs = {c[1] for c in art["categories"]}
    for other in all_articles:
        if other["slug"] == art["slug"]:
            continue
        other_cats = {c[1] for c in other["categories"]}
        if art_cat_slugs & other_cats:
            related.append(other)
        if len(related) >= 3:
            break
    if len(related) < 3:
        for other in all_articles:
            if other["slug"] == art["slug"] or other in related:
                continue
            related.append(other)
            if len(related) >= 3:
                break
    related_html = "\n".join(
        f"""        <a class="related-card" href="{rel}resources/{r['slug']}.html">
          <img src="{rel}{r['feature_image']}" alt="{r['feature_alt']}">
          <div class="related-body">
            <div class="related-tags">
              {' '.join(f'<span class="pill-tag">{n}</span>' for (n, _s) in r['categories'])}
            </div>
            <h3>{r['title']}</h3>
            <div class="related-meta">{r['date']} &middot; Austin Becker</div>
          </div>
        </a>"""
        for r in related
    )

    video_block = ""
    if art.get("video_embed"):
        video_block = f"""    <div class="video-frame" style="margin-bottom:2rem;">
      <iframe src="{art['video_embed']}" title="{art['title']}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
    </div>"""

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
{article_schema(slug=art['slug'], title=art['title'], description=art['meta_description'], date=art['date'], image_path=art['feature_image'])}
<link rel="stylesheet" href="../styles.css">
</head>
<body>

{header(rel)}

<section class="article-hero">
  <div class="container">
    <div class="article-meta">
      <span class="article-date">{art['date']}</span>
    </div>
    <div class="article-categories">
{cats_html}
    </div>
    <h1>{art['title']}</h1>
    <p class="article-lead">{art['lead']}</p>
    <div class="article-author">
      <img src="{rel}images/Austin-Becker-1.jpg" alt="Austin Becker">
      <div>
        <div class="author-name">Austin Becker</div>
        <div class="author-role">Founder &amp; Google Ads Manager</div>
      </div>
    </div>
  </div>
</section>

<section class="article-feature-image">
  <div class="container">
    <img src="{rel}{art['feature_image']}" alt="{art['feature_alt']}">
  </div>
</section>

<section class="article-body">
  <div class="container">
{video_block}
{art['body_html']}

    <div class="article-categories-footer">
      Categories: {cats_footer_html}
    </div>
  </div>
</section>

<section class="article-related">
  <div class="container">
    <h2>Related Resources</h2>
    <div class="related-grid">
{related_html}
    </div>
  </div>
</section>

{footer(rel)}
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


if __name__ == "__main__":
    main()
