"""Generate JSON-LD knowledge graph snippets for abeckermarketing.com.

Design notes (2026-07 schema architecture update):
- Every entity has ONE stable @id (defined in entities.json) that never varies
  by page. Pages that reference an entity also embed a *slim reference node*
  (same @id + name/url) so page-scoped parsers (Google Rich Results) resolve
  author/publisher/isPartOf without crawling other pages, while
  knowledge-graph consumers merge the nodes by @id.
- Organization.makesOffer wraps each Service in an Offer (schema.org expects
  Offer there), and the full Service nodes live on services.html.
- Articles carry datePublished (when known) + dateModified; case-study
  clients are real entities with their public website URL; hub pages link
  their members via hasPart; breadcrumbs on all article-type pages.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

_ENTITIES = json.loads((Path(__file__).parent / "entities.json").read_text())

SITE: str = _ENTITIES["site"]
ORG_ID: str = _ENTITIES["ids"]["organization"]
WEBSITE_ID: str = _ENTITIES["ids"]["website"]
PERSON_ID: str = _ENTITIES["ids"]["person"]
ORG = _ENTITIES["organization"]
PERSON = _ENTITIES["person"]
SERVICES = _ENTITIES["services"]
CLIENTS = _ENTITIES.get("clients", {})


def _service_url(svc: dict) -> str:
    fragment = svc.get("fragment")
    if fragment:
        return f"{SITE}/services.html#{fragment}"
    return f"{SITE}/services/{svc['slug']}.html"


def _service_id(svc: dict) -> str:
    """Stable @id for a service. If the service lives at a fragment URL the
    fragment IS the id (never append a second '#...' — a URI can only carry
    one fragment)."""
    url = _service_url(svc)
    return url if "#" in url else f"{url}#service"


def _script_tag(graph: dict) -> str:
    payload = json.dumps(graph, indent=2, ensure_ascii=False)
    return f'<script type="application/ld+json">\n{payload}\n</script>'


# ---------------------------------------------------------------------------
# Full entity nodes (emitted on the entity's "home" page)
# ---------------------------------------------------------------------------

def _org_node(*, include_offers: bool = False) -> dict:
    org: dict = {
        "@type": ["Organization", "ProfessionalService"],
        "@id": ORG_ID,
        "name": ORG["name"],
        "url": SITE + "/",
        "logo": ORG["logo"],
        "image": ORG.get("image", ORG["logo"]),
        "description": ORG["description"],
        "email": ORG["email"],
        "founder": {"@id": PERSON_ID},
        "address": {
            "@type": "PostalAddress",
            **ORG["address"],
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "sales",
            "email": ORG["email"],
            "areaServed": "US",
            "availableLanguage": "English",
        },
        "areaServed": {
            "@type": "Country",
            "name": "United States",
        },
        "knowsAbout": ORG.get("knowsAbout", []),
        "sameAs": ORG["sameAs"],
    }
    if include_offers:
        org["makesOffer"] = [
            {
                "@type": "Offer",
                "itemOffered": {"@id": _service_id(svc)},
            }
            for svc in SERVICES
        ]
    return org


def _website_node() -> dict:
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": SITE + "/",
        "name": ORG["name"],
        "alternateName": ORG.get("alternateNames", []),
        "description": ORG["description"],
        "publisher": {"@id": ORG_ID},
        "inLanguage": "en-US",
    }


def _person_node() -> dict:
    return {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": PERSON["name"],
        "url": f"{SITE}/about.html#founder",
        "image": PERSON["image"],
        "jobTitle": PERSON["jobTitle"],
        "worksFor": {"@id": ORG_ID},
        "knowsAbout": ORG.get("knowsAbout", []),
        "sameAs": PERSON["sameAs"],
    }


def _service_node(svc: dict) -> dict:
    return {
        "@type": "Service",
        "@id": _service_id(svc),
        "name": svc["name"],
        "url": _service_url(svc),
        "description": svc["description"],
        "provider": {"@id": ORG_ID},
        "areaServed": {
            "@type": "Country",
            "name": "United States",
        },
    }


# ---------------------------------------------------------------------------
# Slim reference nodes (embedded on every page that references the entity,
# so each page's graph is self-contained for page-scoped parsers)
# ---------------------------------------------------------------------------

def _org_ref() -> dict:
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": ORG["name"],
        "url": SITE + "/",
        "logo": ORG["logo"],
    }


def _person_ref() -> dict:
    return {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": PERSON["name"],
        "jobTitle": PERSON["jobTitle"],
        "url": f"{SITE}/about.html#founder",
    }


def _website_ref() -> dict:
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "name": ORG["name"],
        "url": SITE + "/",
        "publisher": {"@id": ORG_ID},
    }


def _service_ref(svc: dict) -> dict:
    return {
        "@type": "Service",
        "@id": _service_id(svc),
        "name": svc["name"],
        "url": _service_url(svc),
        "provider": {"@id": ORG_ID},
    }


def _service_refs_for(fragments: list[str]) -> list[dict]:
    return [_service_ref(s) for s in SERVICES if s.get("fragment") in fragments]


def _refs(*, person: bool = True) -> list[dict]:
    nodes = [_org_ref(), _website_ref()]
    if person:
        nodes.append(_person_ref())
    return nodes


def _client_node(client: str) -> dict:
    """Case-study client as a real, externally-linked entity when we know
    its public website; otherwise a named entity with a stable local @id."""
    info = CLIENTS.get(client, {})
    url = info.get("url")
    node: dict = {"@type": "Organization", "name": client}
    if url:
        node["@id"] = url.rstrip("/") + "/#organization"
        node["url"] = url
    return node


def _breadcrumb(page_url: str, *, trail: list[tuple[str, str]]) -> dict:
    """trail: list of (name, url) EXCLUDING the current page; current page is
    appended automatically as the last, link-less crumb."""
    items = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "name": name,
            "item": url,
        }
        for i, (name, url) in enumerate(trail)
    ]
    return {
        "@type": "BreadcrumbList",
        "@id": f"{page_url}#breadcrumb",
        "itemListElement": items,
    }


def _webpage_node(
    *,
    page_url: str,
    name: str,
    description: str,
    page_type: str = "WebPage",
    main_entity_id: str | None = None,
    about_id: str | None = None,
    breadcrumb_id: str | None = None,
    has_part_ids: list[str] | None = None,
) -> dict:
    page_id = page_url.rstrip("/") + "#webpage"
    if page_url.endswith("/"):
        page_id = SITE + "/#webpage"
    node: dict = {
        "@type": page_type,
        "@id": page_id,
        "url": page_url,
        "name": name,
        "description": description,
        "isPartOf": {"@id": WEBSITE_ID},
        "inLanguage": "en-US",
    }
    if main_entity_id:
        node["mainEntity"] = {"@id": main_entity_id}
    if about_id:
        node["about"] = {"@id": about_id}
    if breadcrumb_id:
        node["breadcrumb"] = {"@id": breadcrumb_id}
    if has_part_ids:
        node["hasPart"] = [{"@id": pid} for pid in has_part_ids]
    return node


def _parse_date(date_str: str) -> str:
    return datetime.strptime(date_str, "%b %d, %Y").strftime("%Y-%m-%d")


def _youtube_thumbnail(embed_url: str) -> str | None:
    """Derive a thumbnail URL from a YouTube embed URL."""
    for marker in ("/embed/", "youtu.be/"):
        if marker in embed_url:
            vid = embed_url.split(marker)[1].split("?")[0].split("/")[0]
            if vid:
                return f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"
    return None


# ---------------------------------------------------------------------------
# Page schemas
# ---------------------------------------------------------------------------

def homepage_schema() -> str:
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            _org_node(include_offers=True),
            _website_node(),
            _person_ref(),
            *[_service_ref(svc) for svc in SERVICES],
            _webpage_node(
                page_url=SITE + "/",
                name="Austin Becker E-Commerce Marketing — PPC for $5M-$50M Stores",
                description=ORG["description"],
                about_id=ORG_ID,
                main_entity_id=ORG_ID,
            ),
        ],
    }
    return _script_tag(graph)


def about_schema() -> str:
    page_url = f"{SITE}/about.html"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            _person_node(),
            _org_ref(),
            _website_ref(),
            _webpage_node(
                page_url=page_url,
                name="About Us — Austin Becker E-Commerce Marketing",
                description="An e-commerce growth-focused team specializing in PPC for $5M-$50M annual revenue stores.",
                main_entity_id=PERSON_ID,
                about_id=ORG_ID,
            ),
        ],
    }
    return _script_tag(graph)


def services_page_schema() -> str:
    """Full Service nodes live here — the page the offer @ids point at."""
    page_url = f"{SITE}/services.html"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            *[_service_node(svc) for svc in SERVICES],
            _org_ref(),
            _website_ref(),
            _webpage_node(
                page_url=page_url,
                name="Services — Austin Becker E-Commerce Marketing",
                description="Ad management, account setup, product feeds, consulting, and pricing for e-commerce PPC teams.",
                about_id=ORG_ID,
            ),
        ],
    }
    return _script_tag(graph)


def article_schema(
    *,
    slug: str,
    title: str,
    description: str,
    date: str,
    image_path: str,
    section: str = "Resource",
    base_path: str = "resources",
    video_url: str | None = None,
    faqs: list[tuple[str, str]] | None = None,
    date_modified: str | None = None,
) -> str:
    page_url = f"{SITE}/{base_path}/{slug}.html"
    article_id = f"{page_url}#article"
    breadcrumb = _breadcrumb(
        page_url,
        trail=[("Home", SITE + "/"), ("Resources", f"{SITE}/resources.html")],
    )
    article_node: dict = {
        "@type": "Article",
        "@id": article_id,
        "headline": title,
        "description": description,
        "url": page_url,
        "datePublished": _parse_date(date),
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": ORG_ID},
        "image": f"{SITE}/{image_path.lstrip('/')}",
        "articleSection": section,
        "inLanguage": "en-US",
    }
    if date_modified:
        article_node["dateModified"] = date_modified
    graph_nodes: list[dict] = [
        article_node,
        _webpage_node(
            page_url=page_url,
            name=f"{title} — Austin Becker E-Commerce Marketing",
            description=description,
            main_entity_id=article_id,
            about_id=ORG_ID,
            breadcrumb_id=breadcrumb["@id"],
        ),
        breadcrumb,
        *_refs(),
    ]
    if video_url:
        video_node: dict = {
            "@type": "VideoObject",
            "@id": f"{page_url}#video",
            "name": title,
            "description": description,
            "embedUrl": video_url,
            "uploadDate": _parse_date(date),
            "publisher": {"@id": ORG_ID},
        }
        thumb = _youtube_thumbnail(video_url)
        if thumb:
            video_node["thumbnailUrl"] = thumb
        graph_nodes.append(video_node)
    if faqs:
        graph_nodes.append(
            {
                "@type": "FAQPage",
                "@id": f"{page_url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {"@type": "Answer", "text": answer},
                    }
                    for question, answer in faqs
                ],
            }
        )
    graph = {"@context": "https://schema.org", "@graph": graph_nodes}
    return _script_tag(graph)


def case_study_schema(
    *,
    slug: str,
    title: str,
    description: str,
    client: str,
    image_path: str,
    date_modified: str | None = None,
    service_fragments: list[str] | None = None,
) -> str:
    page_url = f"{SITE}/case-studies/{slug}.html"
    article_id = f"{page_url}#article"
    breadcrumb = _breadcrumb(
        page_url,
        trail=[("Home", SITE + "/"), ("Case Studies", f"{SITE}/case-studies.html")],
    )
    article_node: dict = {
        "@type": "Article",
        "@id": article_id,
        "headline": title,
        "description": description,
        "url": page_url,
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": ORG_ID},
        "image": f"{SITE}/{image_path.lstrip('/')}",
        "articleSection": "Case Study",
        "about": _client_node(client),
        "inLanguage": "en-US",
    }
    if date_modified:
        article_node["dateModified"] = date_modified
    service_stub_nodes: list[dict] = []
    if service_fragments:
        article_node["mentions"] = [
            {"@id": f"{SITE}/services.html#{frag}"} for frag in service_fragments
        ]
        service_stub_nodes = _service_refs_for(service_fragments)
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            article_node,
            _webpage_node(
                page_url=page_url,
                name=f"{client} Case Study — Austin Becker E-Commerce Marketing",
                description=description,
                main_entity_id=article_id,
                about_id=ORG_ID,
                breadcrumb_id=breadcrumb["@id"],
            ),
            breadcrumb,
            *service_stub_nodes,
            *_refs(),
        ],
    }
    return _script_tag(graph)


def guide_schema(
    *,
    slug: str,
    title: str,
    description: str,
    date_modified: str | None = None,
    image_path: str | None = None,
) -> str:
    page_url = f"{SITE}/guides/{slug}.html"
    article_id = f"{page_url}#article"
    breadcrumb = _breadcrumb(
        page_url,
        trail=[("Home", SITE + "/"), ("Resources", f"{SITE}/resources.html")],
    )
    article_node: dict = {
        "@type": "Article",
        "@id": article_id,
        "headline": title,
        "description": description,
        "url": page_url,
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": ORG_ID},
        "articleSection": "Guide",
        "inLanguage": "en-US",
    }
    if image_path:
        article_node["image"] = f"{SITE}/{image_path.lstrip('/')}"
    if date_modified:
        article_node["dateModified"] = date_modified
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            article_node,
            _webpage_node(
                page_url=page_url,
                name=f"{title} — Austin Becker E-Commerce Marketing",
                description=description,
                main_entity_id=article_id,
                about_id=ORG_ID,
                breadcrumb_id=breadcrumb["@id"],
            ),
            breadcrumb,
            *_refs(),
        ],
    }
    return _script_tag(graph)


def collection_page_schema(
    *,
    page_url: str,
    name: str,
    description: str,
    has_part: list[dict] | None = None,
) -> str:
    """has_part: list of {"id", "name", "url"} for member articles. Slim stub
    nodes are emitted so the hub's graph is self-contained."""
    stubs = [
        {
            "@type": "Article",
            "@id": part["id"],
            "headline": part["name"],
            "url": part["url"],
            "author": {"@id": PERSON_ID},
            "publisher": {"@id": ORG_ID},
        }
        for part in (has_part or [])
    ]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            _webpage_node(
                page_url=page_url,
                name=name,
                description=description,
                page_type="CollectionPage",
                about_id=ORG_ID,
                has_part_ids=[p["id"] for p in has_part] if has_part else None,
            ),
            *stubs,
            *_refs(),
        ],
    }
    return _script_tag(graph)


def contact_page_schema() -> str:
    page_url = f"{SITE}/contact.html"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            _webpage_node(
                page_url=page_url,
                name="Contact Us — Austin Becker E-Commerce Marketing",
                description="Talk to our team about scaling your e-commerce business with paid ads.",
                page_type="ContactPage",
                about_id=ORG_ID,
            ),
            _org_ref(),
            _website_ref(),
        ],
    }
    return _script_tag(graph)


def platforms_page_schema(platforms: list[dict]) -> str:
    """supported-ad-platforms.html — ItemList of platforms.
    Each platform dict: {"name": ..., "sameAs": optional external URI}."""
    page_url = f"{SITE}/supported-ad-platforms.html"
    items = []
    for i, p in enumerate(platforms):
        thing: dict = {"@type": "Thing", "name": p["name"]}
        if p.get("sameAs"):
            thing["sameAs"] = p["sameAs"]
        items.append({"@type": "ListItem", "position": i + 1, "item": thing})
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            _webpage_node(
                page_url=page_url,
                name="Supported Ad Platforms — Austin Becker E-Commerce Marketing",
                description="Google, YouTube, Microsoft, Meta, Pinterest, Target, Walmart, Reddit, and ChatGPT catalog advertising for e-commerce.",
                about_id=ORG_ID,
            ),
            {
                "@type": "ItemList",
                "@id": f"{page_url}#platforms",
                "name": "Supported Ad Platforms",
                "itemListElement": items,
            },
            _org_ref(),
            _website_ref(),
        ],
    }
    return _script_tag(graph)
