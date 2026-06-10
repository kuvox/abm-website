"""Generates the remaining HTML pages for the site from a shared template.
This is a one-shot build helper — you don't need to keep it in your deployed site."""

from pathlib import Path
import textwrap

OUT = Path(__file__).parent / "site"
OUT.mkdir(exist_ok=True)
(OUT / "services").mkdir(exist_ok=True)


def header(active="", depth=0):
    """depth=0 for /, depth=1 for /services/*"""
    p = "../" if depth == 1 else ""
    nav_active = lambda key: "color:var(--brand);" if active == key else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{title}}</title>
<meta name="description" content="{{description}}">
{{extra_head}}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}styles.css">
</head>
<body>
<header class="site-header">
  <div class="container nav">
    <a href="{p}index.html" class="brand-mark"><span class="brand-dot"></span> Austin Becker E-Commerce Marketing</a>
    <button class="menu-toggle" aria-label="Toggle menu" onclick="document.getElementById('navlinks').classList.toggle('open')">☰</button>
    <ul id="navlinks" class="nav-links">
      <li class="has-menu"><a href="{p}index.html#services" style="{nav_active('services')}">Services</a>
        <ul class="submenu">
          <li><a href="{p}services/google-shopping-ads.html">Google Shopping Ads</a></li>
          <li><a href="{p}services/google-search-ads.html">Google Search Ads</a></li>
          <li><a href="{p}services/google-display-network.html">Google Display Network</a></li>
          <li><a href="{p}services/amazon-ads.html">Amazon Ads</a></li>
          <li><a href="{p}services/product-feeds.html">Product Feeds</a></li>
          <li><a href="{p}services/microsoft-ads.html">Microsoft Ads</a></li>
          <li><a href="{p}services/youtube-ads.html">YouTube Ads</a></li>
        </ul>
      </li>
      <li><a href="{p}case-studies.html" style="{nav_active('case')}">Case Studies</a></li>
      <li><a href="{p}about.html" style="{nav_active('about')}">About</a></li>
      <li><a href="{p}resources.html" style="{nav_active('res')}">Free Guides</a></li>
      <li><a href="{p}contact.html" class="nav-cta">Contact Us</a></li>
    </ul>
  </div>
</header>
"""


def footer(depth=0):
    p = "../" if depth == 1 else ""
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h4>Austin Becker E-Commerce Marketing</h4>
        <p style="color:#bcbec1;font-size:0.95rem;">We help $5M to $50M annual revenue businesses grow via pay-per-click ads. Contact us today to learn how we can help.</p>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="{p}services/google-shopping-ads.html">Google Shopping Ads</a></li>
          <li><a href="{p}services/google-search-ads.html">Google Search Ads</a></li>
          <li><a href="{p}services/google-display-network.html">Display Network</a></li>
          <li><a href="{p}services/amazon-ads.html">Amazon Ads</a></li>
          <li><a href="{p}services/product-feeds.html">Product Feeds</a></li>
          <li><a href="{p}services/microsoft-ads.html">Microsoft Ads</a></li>
          <li><a href="{p}services/youtube-ads.html">YouTube Ads</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="{p}about.html">About</a></li>
          <li><a href="{p}case-studies.html">Case Studies</a></li>
          <li><a href="{p}resources.html">Free Guides</a></li>
          <li><a href="{p}contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Legal</h4>
        <ul>
          <li><a href="{p}privacy-policy.html">Privacy Policy</a></li>
          <li><a href="{p}service-agreement.html">Service Agreement</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Austin Becker E-Commerce Marketing. All Rights Reserved.</span>
      <span><a href="mailto:austin@abeckermarketing.com">austin@abeckermarketing.com</a></span>
    </div>
  </div>
</footer>
</body>
</html>"""


def page(filename, title, description, body, active="", depth=0, extra_head=""):
    html = (header(active, depth)
            .replace("{title}", title)
            .replace("{description}", description)
            .replace("{extra_head}", extra_head)
            + body
            + footer(depth))
    out = OUT / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"  wrote {filename}")


# ============================================================
# ABOUT
# ============================================================
about_body = """
<section class="hero" style="padding-bottom:48px;">
  <div class="container">
    <div class="eyebrow">About</div>
    <h1>Specialists in e-commerce PPC.</h1>
    <p class="lead">An e-commerce, growth-focused team, equipped to work with $5M&ndash;$50M annual revenue companies. If your product catalog is large, complex or niche, we're the right choice for you.</p>
  </div>
</section>

<section class="section" id="why-choose-us">
  <div class="container split">
    <div>
      <div class="eyebrow">Why choose us?</div>
      <h2>Built specifically for product catalog ad performance.</h2>
      <p>Our services are designed to meet the needs of growing $5M to $50M annual revenue companies. We work with your internal and external teams to ensure that our advertising work matches your brand style and guidelines across all channels.</p>
      <p>We maintain a special emphasis on e-commerce ads and product data feeds. This helps us keep all our clients' ad data clean, understandable and usable.</p>
    </div>
    <div>
      <ul class="checklist">
        <li>Cross-channel: Google, Amazon, Microsoft, YouTube</li>
        <li>Product feed quality is our specialty</li>
        <li>Proven results with $5M&ndash;$50M revenue clients</li>
        <li>Brand-style alignment across every channel</li>
        <li>Clear, transparent reporting</li>
        <li>We work alongside your existing team</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--alt" id="founder">
  <div class="container split">
    <div>
      <div class="eyebrow">About the Founder</div>
      <h2>Austin Becker</h2>
      <p>Austin has worked with Fortune 500 companies as a project manager and in retail sales analytics. He adds to his team's knowledge by studying marketing journals and following current events in the advertising world.</p>
      <p>The result: an agency that combines big-company analytical rigor with the responsiveness and care of a small specialized team.</p>
    </div>
    <div>
      <div class="card" style="background:#fff;">
        <h3>Background</h3>
        <ul style="padding-left:20px;color:var(--ink-soft);">
          <li>10+ years in pay-per-click advertising</li>
          <li>Project management at Fortune 500 companies</li>
          <li>Retail sales analytics experience</li>
          <li>100% UpWork Job Success score</li>
          <li>$3M+ in annual ad spend managed</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section" id="team">
  <div class="container">
    <div class="center" style="max-width:680px;margin:0 auto 32px;">
      <div class="eyebrow">Our Team</div>
      <h2>Specialists working alongside your team</h2>
      <p class="muted">We work with your internal and external teams to ensure that our advertising work matches your brand style and guidelines across all channels.</p>
    </div>
  </div>
</section>

<section class="cta-banner">
  <div class="container">
    <h2>Ready to talk?</h2>
    <p>Let's discuss your business and how we can help you grow.</p>
    <a href="contact.html" class="btn btn-primary">Contact Us</a>
  </div>
</section>
"""
page("about.html",
     "About Us — Austin Becker E-Commerce Marketing",
     "An e-commerce growth-focused team specializing in PPC for $5M-$50M annual revenue stores. Meet the founder and learn why we're the right fit.",
     about_body, active="about")


# ============================================================
# CONTACT
# ============================================================
contact_body = """
<section class="hero" style="padding-bottom:48px;">
  <div class="container">
    <div class="eyebrow">Contact</div>
    <h1>Let's talk about your store.</h1>
    <p class="lead">Please submit a contact form. We'll reach out to see if our team is a good fit for your business.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:760px;">
    <div class="form-wrap">
      <!-- ============ HUBSPOT EMBEDDED CONTACT FORM ============ -->
      <!-- Replace the placeholder below with your real HubSpot embed code.
           In HubSpot: Marketing → Forms → choose your form → Share → Embed code.
           It will look something like:

           <script charset="utf-8" type="text/javascript" src="//js-na2.hsforms.net/forms/embed/v2.js"></script>
           <script>
             hbspt.forms.create({
               region: "na2",
               portalId: "YOUR_PORTAL_ID",
               formId: "YOUR_FORM_ID"
             });
           </script>

           Paste that code in place of the placeholder div, and the form will appear here.
      -->

      <div id="hubspot-contact-form" class="hubspot-placeholder">
        <strong>HubSpot contact form mounts here.</strong>
        <p style="margin:8px 0 0;">Paste your HubSpot embed code (from <code>Marketing → Forms → Share → Embed</code>) inside the comment block in <code>contact.html</code>.</p>
      </div>

      <!-- ====== Fallback static form (works without HubSpot) ======
           If you'd rather keep this as a plain HTML form that emails you,
           remove the placeholder above and uncomment the form below.
           Set the action= URL to a service like Formspree, Web3Forms,
           or your Cloudflare Worker.

      <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
        <div class="form-row">
          <label for="name">Your name</label>
          <input id="name" name="name" type="text" required>
        </div>
        <div class="form-row">
          <label for="email">Email</label>
          <input id="email" name="email" type="email" required>
        </div>
        <div class="form-row">
          <label for="company">Company / store URL</label>
          <input id="company" name="company" type="text">
        </div>
        <div class="form-row">
          <label for="revenue">Annual revenue</label>
          <select id="revenue" name="revenue">
            <option>Under $1M</option>
            <option>$1M – $5M</option>
            <option>$5M – $50M</option>
            <option>$50M+</option>
          </select>
        </div>
        <div class="form-row">
          <label for="message">How can we help?</label>
          <textarea id="message" name="message" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Send</button>
      </form>
      -->
    </div>

    <p class="muted" style="margin-top:24px;text-align:center;">Prefer email? Reach out at <a href="mailto:austin@abeckermarketing.com">austin@abeckermarketing.com</a></p>
  </div>
</section>
"""
page("contact.html",
     "Contact Us — Austin Becker E-Commerce Marketing",
     "Talk to our team about scaling your e-commerce business with paid ads.",
     contact_body, active="contact")


# ============================================================
# RESOURCES (gated guides — HubSpot form delivers links)
# ============================================================
guides = [
    ("2026 Shopify to Google Merchant Center Feed Setup",
     "Step-by-step setup for sending Shopify product data into Google Merchant Center, with all the gotchas to watch for in 2026."),
    ("How to Optimize Google Shopping Ads Results",
     "Practical optimization moves that move the needle on Shopping campaigns — bid strategy, segmentation, and feed-level wins."),
    ("2025 Shopify Conversion Tracking Guide",
     "Get clean conversion tracking working on Shopify, including Google Ads, GA4 and server-side considerations."),
    ("Amazon Ads ACOS Playbook",
     "How we set ACOS targets and adjust bids based on margin, lifecycle, and inventory — without burning cash."),
    ("Microsoft Ads for E-commerce: Quick Start",
     "Port your Google Shopping success to Microsoft Ads. Key differences, audience setup, and feed sync."),
]
guides_html = "".join(f"""
      <div class="resource-row">
        <div>
          <span class="tag">Guide</span>
          <h3>{title}</h3>
          <p>{desc}</p>
        </div>
      </div>""" for title, desc in guides)

resources_body = f"""
<section class="hero" style="padding-bottom:48px;">
  <div class="container">
    <div class="eyebrow">Free Guides</div>
    <h1>Sign up to unlock our free guide library.</h1>
    <p class="lead">We send our subscribers private links to in-depth guides on Google Shopping, Amazon Ads, product feeds, and more. Drop your email below and we'll send you links to everything.</p>
  </div>
</section>

<section class="section">
  <div class="container split" style="grid-template-columns:1.1fr 1fr;align-items:start;">
    <div>
      <h2>What you'll get</h2>
      <p class="muted">After you sign up, HubSpot will email you private links to every guide below — and to any new guides we publish in the future. Links are unlisted and not indexed by search engines, so they're for subscribers only.</p>
      <div style="margin-top:24px;">{guides_html}
      </div>
    </div>
    <div>
      <div class="form-wrap">
        <h3 style="margin-top:0;">Get all guides — free</h3>
        <p class="muted">One email. We'll send you links to every guide.</p>

        <!-- ============ HUBSPOT EMBEDDED NEWSLETTER FORM ============ -->
        <!-- Use your "Newsletter / Free Guides" HubSpot form here.
             In HubSpot: Marketing → Forms → choose your newsletter form → Share → Embed code.

             Then in HubSpot:
               1. Build a workflow triggered by this form's submission
               2. Action: Send marketing email containing the Notion guide URLs
               3. Optional: tag contact with "Newsletter Subscriber"

             Paste your embed code in place of the placeholder.
        -->

        <div id="hubspot-newsletter-form" class="hubspot-placeholder">
          <strong>HubSpot signup form mounts here.</strong>
          <p style="margin:8px 0 0;">Paste your newsletter form embed code (from <code>Marketing → Forms → Share → Embed</code>) into <code>resources.html</code>.</p>
        </div>
      </div>
      <p class="muted" style="margin-top:16px;font-size:0.85rem;text-align:center;">By signing up you agree to receive emails from Austin Becker E-Commerce Marketing. Unsubscribe anytime.</p>
    </div>
  </div>
</section>
"""
page("resources.html",
     "Free E-commerce PPC Guides — Austin Becker E-Commerce Marketing",
     "Sign up to get private links to free guides on Google Shopping, Amazon Ads, product feeds and more.",
     resources_body, active="res")


# ============================================================
# CASE STUDIES
# ============================================================
case_body = """
<section class="hero" style="padding-bottom:48px;">
  <div class="container">
    <div class="eyebrow">Case Studies</div>
    <h1>Real results for real e-commerce stores.</h1>
    <p class="lead">A few of the businesses we've helped grow.</p>
  </div>
</section>

<section class="section">
  <div class="container grid-2">
    <div class="case-card">
      <div class="result">181.92% Increase in Revenue</div>
      <h3>HoseWarehouse &amp; BeltSmart</h3>
      <p>HoseWarehouse.com and BeltSmart.com sell industrial hose, tools and accessories at wholesale prices in the USA. Both are subsidiaries of Murdock Industrial based in Akron, Ohio.</p>
      <p>We worked across Google Shopping, Search and Microsoft Ads to scale revenue while keeping ad spend efficient — focusing on product feed quality and segmentation.</p>
    </div>
    <div class="case-card">
      <div class="result">Increased ROAS in 3 Weeks</div>
      <h3>Parker Baby</h3>
      <p>Parker Baby designs and provides exceptional and affordable baby products for the modern parent. Since 2015, they've specialized in diaper backpacks, caddies, bath supplies, and other baby accessories.</p>
      <p>By restructuring their Shopping campaigns and tightening their product feed, we drove a meaningful ROAS lift in just three weeks.</p>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="center" style="max-width:680px;margin:0 auto 32px;">
      <div class="eyebrow">Clients</div>
      <h2>A few of the brands we've worked with</h2>
      <p class="muted">Beltsmart · Hose Warehouse · My Music Folders · Parker Baby · TallSlim Tees · The Crypto Lawyers · Kingsley North · Your Car Buying Advocate</p>
    </div>
  </div>
</section>

<section class="cta-banner">
  <div class="container">
    <h2>Want to be our next case study?</h2>
    <p>Let's discuss your store and how we'd approach it.</p>
    <a href="contact.html" class="btn btn-primary">Contact Us</a>
  </div>
</section>
"""
page("case-studies.html",
     "Case Studies — Austin Becker E-Commerce Marketing",
     "Real results for real e-commerce stores. See how we helped HoseWarehouse, Parker Baby and more grow with PPC.",
     case_body, active="case")


# ============================================================
# PRIVACY POLICY
# ============================================================
privacy_body = """
<section class="hero" style="padding-bottom:32px;">
  <div class="container">
    <div class="eyebrow">Legal</div>
    <h1>Privacy Policy</h1>
    <p class="lead">How we collect, use and protect your information.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:780px;">
    <p><strong>Last updated:</strong> 2026</p>

    <h2>What we collect</h2>
    <p>When you submit a contact form or sign up for our newsletter, we collect your name, email address, and any other information you choose to provide (such as company name and store URL).</p>
    <p>Like most websites, we collect anonymous usage data through analytics tools (such as page views and referring sources). This data does not identify you personally.</p>

    <h2>How we use it</h2>
    <p>We use your information only to respond to your inquiries, deliver the resources you requested, and send marketing communications you've opted into. We do not sell your personal information to third parties.</p>

    <h2>Your choices</h2>
    <p>You can unsubscribe from our marketing emails at any time using the unsubscribe link in any email. To request deletion of your data, email <a href="mailto:austin@abeckermarketing.com">austin@abeckermarketing.com</a>.</p>

    <h2>Data storage</h2>
    <p>Form submissions are stored in our CRM (HubSpot). HubSpot's privacy practices are described at <a href="https://legal.hubspot.com/privacy-policy" target="_blank" rel="noopener">hubspot.com/privacy-policy</a>.</p>

    <h2>Cookies</h2>
    <p>We use cookies for analytics and to remember basic preferences. You can disable cookies in your browser settings.</p>

    <h2>Contact</h2>
    <p>Questions about this policy? Email <a href="mailto:austin@abeckermarketing.com">austin@abeckermarketing.com</a>.</p>

    <p class="muted" style="margin-top:32px;font-size:0.9rem;"><em>This is a starting template. Review with a lawyer before publishing if your business has specific compliance requirements (GDPR, CCPA, etc.).</em></p>
  </div>
</section>
"""
page("privacy-policy.html",
     "Privacy Policy — Austin Becker E-Commerce Marketing",
     "Privacy policy for abeckermarketing.com.",
     privacy_body)


# ============================================================
# SERVICE AGREEMENT
# ============================================================
agreement_body = """
<section class="hero" style="padding-bottom:32px;">
  <div class="container">
    <div class="eyebrow">Legal</div>
    <h1>Service Agreement</h1>
    <p class="lead">The terms that govern our client engagements.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:780px;">
    <p class="muted"><em>This page is a placeholder. Replace this content with your actual service agreement, or link to a hosted version (PDF or e-sign system) of your full agreement.</em></p>

    <h2>Engagement</h2>
    <p>By engaging Austin Becker E-Commerce Marketing for paid advertising services, you agree to the terms outlined in your signed Statement of Work.</p>

    <h2>Scope of services</h2>
    <p>Services covered include account setup, campaign management, optimization, reporting, and strategic guidance for the channels listed in your agreement (Google Ads, Amazon Ads, Microsoft Ads, etc.).</p>

    <h2>Fees and billing</h2>
    <p>Fees and billing terms are specified in your Statement of Work. Invoices are due upon receipt unless otherwise stated.</p>

    <h2>Termination</h2>
    <p>Either party may terminate the engagement with 30 days written notice. Account access will be returned to the client in a usable state.</p>

    <h2>Confidentiality</h2>
    <p>Both parties agree to keep confidential information shared during the engagement private and to use it only for purposes of the agreement.</p>

    <h2>Contact</h2>
    <p>Questions about your agreement? Email <a href="mailto:austin@abeckermarketing.com">austin@abeckermarketing.com</a>.</p>
  </div>
</section>
"""
page("service-agreement.html",
     "Service Agreement — Austin Becker E-Commerce Marketing",
     "Service agreement and engagement terms.",
     agreement_body)


# ============================================================
# 404
# ============================================================
notfound_body = """
<section class="hero" style="padding:120px 0;text-align:center;">
  <div class="container">
    <div class="eyebrow">404</div>
    <h1>Page not found.</h1>
    <p class="lead" style="margin-left:auto;margin-right:auto;">The page you're looking for doesn't exist or has been moved.</p>
    <a href="/" class="btn btn-primary">Back to home</a>
  </div>
</section>
"""
page("404.html",
     "Page Not Found — Austin Becker E-Commerce Marketing",
     "404 — page not found.",
     notfound_body)


# ============================================================
# SERVICE PAGES (7)
# ============================================================
services = [
    {
        "slug": "google-shopping-ads",
        "name": "Google Shopping Ads",
        "tagline": "Product listing ads, done right.",
        "lead": "Optimized product data helps customers select your offer and convert. We place special emphasis on creating complete product data so your ads stand out.",
        "body": """
            <p>Google Shopping ads are the most important ad surface for most e-commerce stores — and they're entirely driven by the quality of your product feed. We treat the feed as a first-class asset and tune it continuously.</p>
            <p>What we focus on:</p>
            <ul class="checklist">
              <li>Product feed quality, completeness and segmentation</li>
              <li>Bid strategy aligned to margin and inventory</li>
              <li>Custom labels for promotions, seasonality and lifecycle</li>
              <li>Negative keywords and search query review</li>
              <li>Inventory prioritization for profitable SKUs</li>
              <li>Performance Max strategy when it fits the account</li>
            </ul>
        """
    },
    {
        "slug": "amazon-ads",
        "name": "Amazon Ads",
        "tagline": "Optimize ACOS without burning cash.",
        "lead": "Amazon ads can be your sales lifeline or a bottomless pit for cash. We understand how to optimize ad spend and ACOS based on your business's unique goals.",
        "body": """
            <p>Amazon's ad platform rewards specialists who understand both the marketplace mechanics and the broader retail context. We bring both.</p>
            <ul class="checklist">
              <li>Sponsored Products, Brands, and Display campaigns</li>
              <li>ACOS targets aligned to margin and product lifecycle</li>
              <li>Brand defense and competitor conquest strategies</li>
              <li>Search term harvesting and negative keyword management</li>
              <li>DSP for advanced retargeting (when account size justifies)</li>
            </ul>
        """
    },
    {
        "slug": "product-feeds",
        "name": "Product Feeds",
        "tagline": "Clean, complete, optimized product data.",
        "lead": "Optimized product data helps customers select your offer and convert. We place special emphasis on creating complete product data so your ads stand out.",
        "body": """
            <p>Product feeds are the unsexy work that drives most of the wins in e-commerce PPC. We do this work seriously, with feed transformation tooling and a process for keeping data clean as your catalog evolves.</p>
            <ul class="checklist">
              <li>Shopify, WooCommerce, BigCommerce, custom carts</li>
              <li>Title and description optimization at scale</li>
              <li>Custom labels for segmentation</li>
              <li>Image, GTIN and category compliance</li>
              <li>Multi-channel feed management (Google, Microsoft, Meta, Amazon)</li>
            </ul>
        """
    },
    {
        "slug": "google-search-ads",
        "name": "Google Search Ads",
        "tagline": "Capture intent across all of Google.",
        "lead": "Your ads perform best when they appear across all Google ad inventory. Search (text) ads give incremental gains to e-commerce businesses.",
        "body": """
            <p>Search ads complement Shopping by capturing branded queries, high-intent product searches, and category-level demand. We structure search accounts for long-term performance, not short-term flash.</p>
            <ul class="checklist">
              <li>Brand and competitor strategy</li>
              <li>Category and product-level keyword expansion</li>
              <li>Smart bidding configuration</li>
              <li>Ad copy testing and asset rotation</li>
              <li>Match type and negative keyword discipline</li>
            </ul>
        """
    },
    {
        "slug": "google-display-network",
        "name": "Google Display Network",
        "tagline": "Stay top-of-mind through the buyer journey.",
        "lead": "We optimize and deploy your ad data across display ads to ensure customers see and remember your store before making a final purchase decision. The end result is more sales.",
        "body": """
            <p>Display done well drives incremental sales. Display done poorly burns cash. We focus on the audiences and placements that move the needle.</p>
            <ul class="checklist">
              <li>Dynamic remarketing tied to your product feed</li>
              <li>Custom audiences and lookalikes</li>
              <li>Placement and topic exclusions to protect spend</li>
              <li>Creative asset development and testing</li>
            </ul>
        """
    },
    {
        "slug": "microsoft-ads",
        "name": "Microsoft Ads",
        "tagline": "Reach customers on Bing, AOL, Yahoo and DuckDuckGo.",
        "lead": "Carry your success on Google and Amazon over to Microsoft Ads, where you can reach customers on Bing, AOL, Yahoo and DuckDuckGo.",
        "body": """
            <p>Microsoft Ads often delivers cheaper clicks and a higher-spending audience for the right verticals. Importing from Google is the easy part — making the account actually perform takes specialization.</p>
            <ul class="checklist">
              <li>Account import and structure cleanup</li>
              <li>Microsoft Shopping with optimized feeds</li>
              <li>LinkedIn audience targeting (a Microsoft-only advantage)</li>
              <li>Search and audience network management</li>
            </ul>
        """
    },
    {
        "slug": "youtube-ads",
        "name": "YouTube Ads",
        "tagline": "Reach buyers on the second-most-visited site in the US.",
        "lead": "YouTube is the second most visited website in the USA. We expand your ads into YouTube to help more potential customers consider and purchase from you.",
        "body": """
            <p>YouTube isn't just a brand awareness channel — for the right products, it's a direct response engine. We focus on the formats, audiences, and creative briefs that drive measurable results.</p>
            <ul class="checklist">
              <li>Performance-focused video ad strategy</li>
              <li>Audience targeting tuned to your customer profile</li>
              <li>Creative briefs and testing frameworks</li>
              <li>Integration with your Google Ads conversion tracking</li>
            </ul>
        """
    },
]

for s in services:
    body = f"""
<section class="hero" style="padding-bottom:32px;">
  <div class="container">
    <div class="eyebrow">Service</div>
    <h1>{s['name']}</h1>
    <p class="lead">{s['lead']}</p>
    <a href="../contact.html" class="btn btn-primary">Talk to us about {s['name']}</a>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:780px;">
    <h2>{s['tagline']}</h2>
    {s['body']}
    <hr class="rule">
    <h3>Want to see if we're a fit?</h3>
    <p>Tell us about your store and your current ad performance. We'll let you know whether we can help — honestly.</p>
    <a href="../contact.html" class="btn btn-ghost">Contact us</a>
  </div>
</section>

<section class="cta-banner">
  <div class="container">
    <h2>Ready to grow {s['name']} performance?</h2>
    <p>We work with $5M&ndash;$50M annual revenue e-commerce companies. Let's talk.</p>
    <a href="../contact.html" class="btn btn-primary">Contact Us</a>
  </div>
</section>
"""
    page(f"services/{s['slug']}.html",
         f"{s['name']} — Austin Becker E-Commerce Marketing",
         s['lead'][:160],
         body, active="services", depth=1)


# ============================================================
# robots.txt
# ============================================================
(OUT / "robots.txt").write_text("""User-agent: *
Allow: /
Sitemap: https://abeckermarketing.com/sitemap.xml
""")
print("  wrote robots.txt")


# ============================================================
# sitemap.xml
# ============================================================
urls = [
    "/", "/about.html", "/contact.html", "/case-studies.html", "/resources.html",
    "/privacy-policy.html", "/service-agreement.html",
] + [f"/services/{s['slug']}.html" for s in services]

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    sitemap += f"  <url><loc>https://abeckermarketing.com{u}</loc></url>\n"
sitemap += "</urlset>\n"
(OUT / "sitemap.xml").write_text(sitemap)
print("  wrote sitemap.xml")

print("\n✅ Site generation complete.")
