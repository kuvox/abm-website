"""Canonical site header navigation — single source of truth for all pages."""
from __future__ import annotations

from pathlib import Path

NESTED_SECTIONS = frozenset({"services", "case-studies", "resources", "guides"})

SERVICES_NAV_ITEMS = (
    ("Ad Management", "services.html", "#ad-management-pricing"),
    ("Product Feeds", "services.html", "#product-feeds"),
    ("Consulting", "services.html", "#consulting"),
    ("Pricing", "services.html", "#pricing"),
)

SOCIAL_ICONS = """<a href="https://www.youtube.com/@ppcforeveryone" target="_blank" rel="noopener" aria-label="YouTube"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23.5 6.2a3 3 0 0 0-2.13-2.13C19.5 3.56 12 3.56 12 3.56s-7.5 0-9.37.51A3 3 0 0 0 .5 6.2 31.4 31.4 0 0 0 0 12a31.4 31.4 0 0 0 .5 5.8 3 3 0 0 0 2.13 2.13c1.87.51 9.37.51 9.37.51s7.5 0 9.37-.51A3 3 0 0 0 23.5 17.8 31.4 31.4 0 0 0 24 12a31.4 31.4 0 0 0-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/></svg></a>
            <a href="https://www.instagram.com/austinbeckerecommarketing/" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.71 3.71 0 0 1-1.38-.9 3.71 3.71 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41 1.27-.06 1.65-.07 4.85-.07M12 0C8.74 0 8.33.01 7.05.07 5.78.13 4.9.33 4.14.63a5.87 5.87 0 0 0-2.13 1.38A5.87 5.87 0 0 0 .63 4.14C.33 4.9.13 5.78.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91.31.79.73 1.46 1.38 2.13a5.87 5.87 0 0 0 2.13 1.38c.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27-.06 2.15-.26 2.91-.56a5.87 5.87 0 0 0 2.13-1.38 5.87 5.87 0 0 0 1.38-2.13c.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91a5.87 5.87 0 0 0-1.38-2.13A5.87 5.87 0 0 0 19.86.63c-.76-.3-1.64-.5-2.91-.56C15.67.01 15.26 0 12 0zm0 5.84a6.16 6.16 0 1 0 0 12.32 6.16 6.16 0 0 0 0-12.32zm0 10.16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.41-11.85a1.44 1.44 0 1 0 0 2.88 1.44 1.44 0 0 0 0-2.88z"/></svg></a>
            <a href="https://www.linkedin.com/in/austin-becker-marketing/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg></a>
            <a href="https://x.com/MktngByABecker" target="_blank" rel="noopener" aria-label="X (Twitter)"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
            <a href="https://www.facebook.com/ABeckerMarketing" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.69.24 2.69.24v2.97h-1.52c-1.49 0-1.95.93-1.95 1.89v2.26h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07z"/></svg></a>"""


def _services_nav_links(rel: str, *, use_anchors: bool = False, indent: str = "              ") -> str:
    lines = []
    for label, page, anchor in SERVICES_NAV_ITEMS:
        href = f"{rel}{page}{anchor}" if use_anchors else f"{rel}{page}"
        lines.append(f'{indent}<li><a href="{href}">{label}</a></li>')
    return "\n".join(lines)


def rel_prefix(path: Path, site_root: Path) -> str:
    parts = path.relative_to(site_root).parts
    return "../" if parts and parts[0] in NESTED_SECTIONS else ""


def detect_active(path: Path, site_root: Path) -> str | None:
    rel = path.relative_to(site_root)
    parts = rel.parts
    name = rel.name

    if parts and parts[0] == "services":
        return "services"
    if name in ("services.html", "supported-ad-platforms.html"):
        return "services"
    if parts and parts[0] == "guides":
        return "learn"
    if parts and parts[0] == "resources":
        return "learn"
    if name == "resources.html":
        return "learn"
    if parts and parts[0] == "case-studies":
        return "case-studies"
    if name == "case-studies.html":
        return "case-studies"
    if name == "about.html":
        return "about"
    if name == "contact.html":
        return "contact"
    return None


def _nav_class(active: str | None, item: str, extra: str = "") -> str:
    classes = [c for c in (extra, "active" if active == item else "") if c]
    return f' class="{" ".join(classes)}"' if classes else ""


def header(rel: str, *, active: str | None = None) -> str:
  brand_href = "/" if not rel else f"{rel}index.html"
  return f"""<header class="site-header">
  <div class="container nav">
    <a href="{brand_href}" class="brand-mark" aria-label="Austin Becker E-Commerce Marketing"><img src="{rel}images/logo.svg" alt="Austin Becker E-Commerce Marketing" class="brand-logo"></a>
    <button class="menu-toggle" aria-label="Toggle menu" onclick="document.getElementById('navlinks').classList.toggle('open')">☰</button>
    <ul id="navlinks" class="nav-links">
      <li class="has-menu has-megamenu has-megamenu--services"><a href="{rel}services.html"{_nav_class(active, "services")}>Services</a>
        <div class="megamenu megamenu--services">
          <div class="megamenu-col megamenu-col--with-cta">
            <span class="megamenu-eyebrow">Services</span>
            <ul>
{_services_nav_links(rel)}
            </ul>
            <div class="megamenu-cta-card">
              <p class="megamenu-cta-quote">I&rsquo;ve had the pleasure of working with Austin, and I must say, he&rsquo;s been an absolute legend!</p>
              <div class="megamenu-cta-attribution">
                <img src="{rel}images/boxhill-instagram-logo-circle.jpg" alt="" class="megamenu-cta-avatar" width="52" height="52">
                <div class="megamenu-cta-attribution-text">
                  <strong class="megamenu-cta-name">Rich Fraser</strong>
                  <span class="megamenu-cta-title">Owner at <a href="https://www.boxhill.co.nz/" target="_blank" rel="noopener">boxhill.co.nz</a></span>
                </div>
              </div>
            </div>
          </div>
          <div class="megamenu-col">
            <span class="megamenu-eyebrow">Ad Platforms</span>
            <ul>
              <li><a href="{rel}supported-ad-platforms.html">Google &amp; YouTube</a></li>
              <li><a href="{rel}supported-ad-platforms.html">Microsoft</a></li>
              <li><a href="{rel}supported-ad-platforms.html">ChatGPT</a></li>
              <li><a href="{rel}supported-ad-platforms.html">Meta</a></li>
              <li><a href="{rel}supported-ad-platforms.html">Pinterest</a></li>
              <li><a href="{rel}supported-ad-platforms.html">Target</a></li>
              <li><a href="{rel}supported-ad-platforms.html">Walmart</a></li>
              <li><a href="{rel}supported-ad-platforms.html">Reddit</a></li>
            </ul>
          </div>
        </div>
      </li>
      <li><a href="{rel}case-studies.html"{_nav_class(active, "case-studies")}>Case Studies</a></li>
      <li class="has-menu has-megamenu has-megamenu--learn"><a href="{rel}resources.html"{_nav_class(active, "learn")}>Learn</a>
        <div class="megamenu megamenu--learn">
          <div class="megamenu-col">
            <ul>
              <li><a href="{rel}resources.html"><span class="megamenu-learn-label">Blog</span><span class="megamenu-learn-desc">Optimize Campaigns &amp; Data Feeds</span></a></li>
              <li><a href="https://www.youtube.com/@ppcforeveryone" target="_blank" rel="noopener"><span class="megamenu-learn-label">YouTube Channel</span><span class="megamenu-learn-desc">PPC for Everyone</span></a></li>
              <li><a href="{rel}resources.html#newsletter"><span class="megamenu-learn-label">Newsletter</span><span class="megamenu-learn-desc">Up-to-Date on Digital Ads</span></a></li>
            </ul>
          </div>
        </div>
      </li>
      <li class="has-menu has-megamenu has-megamenu--about"><a href="{rel}about.html"{_nav_class(active, "about")}>About</a>
        <div class="megamenu megamenu--about">
          <div class="megamenu-col">
            <ul>
              <li><a href="{rel}about.html">Who We Work With</a></li>
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
      <li><a href="{rel}contact.html"{_nav_class(active, "contact", "nav-cta")}>Contact Us</a></li>
    </ul>
  </div>
</header>"""


def services_hub_nav(rel: str = "") -> str:
    return f"""    <nav class="services-hub-nav megamenu-col" aria-label="Services">
      <span class="megamenu-eyebrow">Services</span>
      <ul>
{_services_nav_links(rel, use_anchors=True, indent="        ")}
      </ul>
    </nav>"""


def footer(rel: str) -> str:
    services_links = "\n".join(
        f'          <li><a href="{rel}{page}">{label}</a></li>'
        for label, page, _anchor in SERVICES_NAV_ITEMS
    )
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{rel}images/website-logos/ABHorizontalWhiteDigital.png" alt="Austin Becker E-Commerce Marketing" class="footer-logo">
        <p>We help $5M to $50M annual revenue businesses grow via pay per click ads. Contact us today to learn how we can help you grow your business.</p>
        <div class="social-icons">
            {SOCIAL_ICONS}
        </div>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
{services_links}
        </ul>
      </div>
      <div>
        <h4>About</h4>
        <ul>
          <li><a href="{rel}about.html#why-choose-us">Are We a Fit?</a></li>
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
      </div>
    </div>
  </div>
</footer>"""


def blog_newsletter(rel: str) -> str:
    return f"""<section class="newsletter-cta" id="newsletter">
  <div class="container">
    <div class="newsletter-grid">
      <div class="newsletter-text">
        <span class="eyebrow">Newsletter</span>
        <h2>Up-to-Date on Digital Ads</h2>
        <p>Sign up for practical PPC and product feed updates. We&rsquo;ll email you when new guides and resources are published.</p>
      </div>
      <div class="newsletter-form-wrap">
        <form class="abm-newsletter-form" novalidate>
          <label class="visually-hidden" for="abm-newsletter-email">Email</label>
          <input id="abm-newsletter-email" name="email" type="email" autocomplete="email" required placeholder="Email address">
          <button type="submit" class="btn btn-primary">Subscribe</button>
          <p class="abm-newsletter-status" hidden></p>
        </form>
      </div>
    </div>
  </div>
</section>"""
