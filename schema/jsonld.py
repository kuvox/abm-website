"""Generate JSON-LD knowledge graph snippets for abeckermarketing.com."""

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


def _script_tag(graph: dict) -> str:
    payload = json.dumps(graph, indent=2, ensure_ascii=False)
    return f'<script type="application/ld+json">\n{payload}\n</script>'


def _org_node(*, include_offers: bool = False) -> dict:
    org: dict = {
        "@type": ["Organization", "ProfessionalService"],
        "@id": ORG_ID,
        "name": ORG["name"],
        "url": SITE + "/",
        "logo": ORG["logo"],
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
        "sameAs": ORG["sameAs"],
    }
    if include_offers:
        org["makesOffer"] = [
            {"@id": f"{SITE}/services/{svc['slug']}.html#service"}
            for svc in SERVICES
        ]
    return org


def _website_node() -> dict:
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": SITE + "/",
        "name": ORG["name"],
        "publisher": {"@id": ORG_ID},
        "inLanguage": "en-US",
    }


def _webpage_node(
    *,
    page_url: str,
    name: str,
    description: str,
    page_type: str = "WebPage",
    main_entity_id: str | None = None,
    about_id: str | None = None,
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
    return node


def _person_node() -> dict:
    return {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": PERSON["name"],
        "url": f"{SITE}/about.html#founder",
        "image": PERSON["image"],
        "jobTitle": PERSON["jobTitle"],
        "worksFor": {"@id": ORG_ID},
        "sameAs": PERSON["sameAs"],
    }


def _service_node(slug: str, name: str, description: str) -> dict:
    url = f"{SITE}/services/{slug}.html"
    return {
        "@type": "Service",
        "@id": f"{url}#service",
        "name": name,
        "url": url,
        "description": description,
        "provider": {"@id": ORG_ID},
        "areaServed": {
            "@type": "Country",
            "name": "United States",
        },
    }


def _parse_date(date_str: str) -> str:
    return datetime.strptime(date_str, "%b %d, %Y").strftime("%Y-%m-%d")


def homepage_schema() -> str:
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            _org_node(include_offers=True),
            _website_node(),
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


def service_schema(slug: str, name: str, description: str) -> str:
    page_url = f"{SITE}/services/{slug}.html"
    service_id = f"{page_url}#service"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            _service_node(slug, name, description),
            _webpage_node(
                page_url=page_url,
                name=f"{name} — Austin Becker E-Commerce Marketing",
                description=description,
                main_entity_id=service_id,
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
) -> str:
    page_url = f"{SITE}/resources/{slug}.html"
    article_id = f"{page_url}#article"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
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
            },
            _webpage_node(
                page_url=page_url,
                name=f"{title} — Austin Becker E-Commerce Marketing",
                description=description,
                main_entity_id=article_id,
                about_id=ORG_ID,
            ),
        ],
    }
    return _script_tag(graph)


def case_study_schema(
    *,
    slug: str,
    title: str,
    description: str,
    client: str,
    image_path: str,
) -> str:
    page_url = f"{SITE}/case-studies/{slug}.html"
    article_id = f"{page_url}#article"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": article_id,
                "headline": title,
                "description": description,
                "url": page_url,
                "author": {"@id": PERSON_ID},
                "publisher": {"@id": ORG_ID},
                "image": f"{SITE}/{image_path.lstrip('/')}",
                "articleSection": "Case Study",
                "about": {
                    "@type": "Organization",
                    "name": client,
                },
                "inLanguage": "en-US",
            },
            _webpage_node(
                page_url=page_url,
                name=f"{client} Case Study — Austin Becker E-Commerce Marketing",
                description=description,
                main_entity_id=article_id,
                about_id=ORG_ID,
            ),
        ],
    }
    return _script_tag(graph)


def guide_schema(*, slug: str, title: str, description: str) -> str:
    page_url = f"{SITE}/guides/{slug}.html"
    article_id = f"{page_url}#article"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": article_id,
                "headline": title,
                "description": description,
                "url": page_url,
                "author": {"@id": PERSON_ID},
                "publisher": {"@id": ORG_ID},
                "articleSection": "Guide",
                "inLanguage": "en-US",
            },
            _webpage_node(
                page_url=page_url,
                name=f"{title} — Austin Becker E-Commerce Marketing",
                description=description,
                main_entity_id=article_id,
                about_id=ORG_ID,
            ),
        ],
    }
    return _script_tag(graph)


def collection_page_schema(*, page_url: str, name: str, description: str) -> str:
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            _webpage_node(
                page_url=page_url,
                name=name,
                description=description,
                page_type="CollectionPage",
                about_id=ORG_ID,
            ),
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
        ],
    }
    return _script_tag(graph)
