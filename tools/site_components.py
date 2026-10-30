"""Shared HTML components, head tags and structured data for BoardExamBD."""

from __future__ import annotations

import html as html_lib
import json
import math
from datetime import datetime

from seo_config import ARTICLE_BY_SLUG, SITE

DOMAIN = SITE["domain"]
AUTHOR = SITE["author"]
OG_IMAGE = SITE["og_image"]
LOGO = SITE["logo"]
ORG_ID = f"{DOMAIN}/#organization"
WEBSITE_ID = f"{DOMAIN}/#website"

NAV_ITEMS = [
    ("home", "Home", "/"),
    ("ssc", "SSC", "/ssc"),
    ("hsc", "HSC", "/hsc"),
    ("admission", "Admission", "/admission"),
    ("blog", "Blog", "/blog"),
]

CLUSTER_STYLES = {
    "SSC": {
        "badge": "bg-sky-50 text-sky-700 ring-sky-600/20",
        "solid": "bg-sky-500",
        "soft": "bg-sky-50",
        "text": "text-sky-700",
        "hero": "from-sky-50 via-white to-white",
    },
    "HSC": {
        "badge": "bg-violet-50 text-violet-700 ring-violet-600/20",
        "solid": "bg-violet-500",
        "soft": "bg-violet-50",
        "text": "text-violet-700",
        "hero": "from-violet-50 via-white to-white",
    },
    "Admission": {
        "badge": "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
        "solid": "bg-emerald-500",
        "soft": "bg-emerald-50",
        "text": "text-emerald-700",
        "hero": "from-emerald-50 via-white to-white",
    },
    "Blog": {
        "badge": "bg-indigo-50 text-indigo-700 ring-indigo-600/20",
        "solid": "bg-indigo-500",
        "soft": "bg-indigo-50",
        "text": "text-indigo-700",
        "hero": "from-indigo-50 via-white to-white",
    },
}

STATUS_STYLES = {
    "Scheduled": "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
    "Upcoming": "bg-indigo-50 text-indigo-700 ring-indigo-600/20",
    "Tentative": "bg-amber-50 text-amber-800 ring-amber-600/20",
    "Expected": "bg-sky-50 text-sky-700 ring-sky-600/20",
    "Pending": "bg-slate-100 text-slate-600 ring-slate-500/20",
    "Closed": "bg-rose-50 text-rose-700 ring-rose-600/20",
    "Completed": "bg-slate-100 text-slate-600 ring-slate-500/20",
    "Published": "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
    "Open": "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
}

KICKERS = {
    "ssc-2026-routine": "Exam routine",
    "ssc-2026-result": "Result",
    "ssc-form-fillup-2027": "Form fill-up",
    "ssc-board-challenge-2026": "Board challenge",
    "hsc-2026-routine": "Exam routine",
    "hsc-2026-result": "Result",
    "hsc-form-fillup-2027": "Form fill-up",
    "hsc-practical-2026": "Practical exam",
    "buet-admission-2026-27": "BUET admission",
    "du-a-unit-admission-2026-27": "DU A Unit",
    "gst-a-unit-admission-2026-27": "GST admission",
    "ku-admission-2026-27": "KU admission",
    "medical-admission-2026-27": "Medical admission",
    "ru-admission-2026-27": "RU admission",
    "ruet-admission-2026-27": "RUET admission",
    "sust-admission-2026-27": "SUST admission",
}


def e(value: str | None) -> str:
    return html_lib.escape(value or "", quote=True)


def display_date(value: str, short: bool = False) -> str:
    parsed = datetime.fromisoformat(value)
    if short:
        return f"{parsed.day} {parsed.strftime('%b %Y')}"
    return f"{parsed.day} {parsed.strftime('%B %Y')}"


def iso_date(value: str) -> str:
    return datetime.fromisoformat(value).date().isoformat()


def cluster_style(cluster: str) -> dict[str, str]:
    return CLUSTER_STYLES.get(cluster, CLUSTER_STYLES["Blog"])


def kicker_for(article: dict) -> str:
    return KICKERS.get(article["slug"], "Admission guide")


def card_title(article: dict) -> str:
    return article["title"].split(" | ")[0].strip()


def reading_minutes(words: int) -> int:
    return max(3, math.ceil(words / 220))


def status_badge(status: str) -> str:
    classes = STATUS_STYLES.get(status, STATUS_STYLES["Pending"])
    return f'<span class="badge {classes}">{e(status)}</span>'


def cluster_badge(cluster: str, label: str | None = None) -> str:
    style = cluster_style(cluster)
    return f'<span class="badge {style["badge"]}">{e(label or cluster)}</span>'


def visible_breadcrumb(items: list[tuple[str, str | None]]) -> str:
    if not items:
        return ""
    parts = []
    for index, (label, href) in enumerate(items):
        if href:
            parts.append(
                f'<li><a href="{e(href)}" class="font-medium text-slate-500 transition hover:text-indigo-700">{e(label)}</a></li>'
            )
        else:
            parts.append(
                f'<li><span aria-current="page" class="font-semibold text-slate-700">{e(label)}</span></li>'
            )
        if index < len(items) - 1:
            parts.append('<li aria-hidden="true" class="text-slate-300">/</li>')
    return (
        '<nav aria-label="Breadcrumb" class="text-sm">'
        '<ol class="flex flex-wrap items-center gap-2">' + "".join(parts) + "</ol></nav>"
    )


def site_header(active: str | None = None) -> str:
    desktop = []
    mobile = []
    for key, label, href in NAV_ITEMS:
        is_active = key == active
        desktop_class = (
            "rounded-lg bg-indigo-600 px-3 py-1.5 text-sm font-semibold text-white shadow-sm"
            if is_active
            else "rounded-lg px-3 py-1.5 text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
        )
        mobile_class = (
            "block rounded-lg bg-indigo-600 px-3 py-2 text-sm font-semibold text-white"
            if is_active
            else "block rounded-lg px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900"
        )
        current = ' aria-current="page"' if is_active else ""
        desktop.append(f'<a href="{href}" class="{desktop_class}"{current}>{label}</a>')
        mobile.append(f'<a href="{href}" class="{mobile_class}"{current}>{label}</a>')

    return f"""
  <header class="sticky top-0 z-50 border-b border-slate-200 bg-white/95 backdrop-blur">
    <div class="site-container">
      <input id="navtoggle" type="checkbox" class="peer sr-only" aria-label="Toggle navigation menu">
      <div class="flex h-16 items-center justify-between gap-4">
        <a href="/" class="inline-flex items-center gap-1.5 text-lg font-extrabold tracking-tight text-slate-900" aria-label="BoardExamBD home">
          <span>Board</span><span class="text-indigo-600">Exam</span><span class="rounded bg-indigo-600 px-1.5 py-0.5 text-xs font-bold text-white">BD</span>
        </a>
        <nav class="hidden items-center gap-1 md:flex" aria-label="Main navigation">
          {''.join(desktop)}
        </nav>
        <label for="navtoggle" class="-mr-2 inline-flex cursor-pointer items-center justify-center rounded-lg p-2 text-slate-600 transition hover:bg-slate-100 peer-focus-visible:ring-2 peer-focus-visible:ring-indigo-500 md:hidden">
          <span class="sr-only">Toggle navigation</span>
          <svg class="h-6 w-6" aria-hidden="true" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
          </svg>
        </label>
      </div>
      <nav class="hidden space-y-1 border-t border-slate-100 py-3 peer-checked:block md:hidden" aria-label="Mobile navigation">
        {''.join(mobile)}
      </nav>
    </div>
  </header>
"""


def site_footer() -> str:
    return f"""
  <footer class="mt-16 border-t border-slate-200 bg-slate-50">
    <div class="site-container py-12">
      <div class="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
        <div>
          <a href="/" class="inline-flex items-center gap-1.5 text-lg font-extrabold tracking-tight text-slate-900">
            <span>Board</span><span class="text-indigo-600">Exam</span><span class="rounded bg-indigo-600 px-1.5 py-0.5 text-xs font-bold text-white">BD</span>
          </a>
          <p class="mt-3 max-w-xs text-sm leading-6 text-slate-600">Clear, source-linked guides to SSC, HSC and university admission notices in Bangladesh.</p>
          <p class="mt-4 text-xs leading-5 text-slate-500">Independent publication. Not affiliated with any education board or university.</p>
        </div>
        <div>
          <p class="text-xs font-bold uppercase tracking-[0.16em] text-slate-500">Study</p>
          <ul class="mt-4 space-y-2.5 text-sm">
            <li><a href="/ssc" class="text-slate-600 transition hover:text-indigo-700">SSC notices &amp; routine</a></li>
            <li><a href="/hsc" class="text-slate-600 transition hover:text-indigo-700">HSC notices &amp; routine</a></li>
            <li><a href="/admission" class="text-slate-600 transition hover:text-indigo-700">University admission</a></li>
            <li><a href="/blog" class="text-slate-600 transition hover:text-indigo-700">All guides</a></li>
          </ul>
        </div>
        <div>
          <p class="text-xs font-bold uppercase tracking-[0.16em] text-slate-500">Popular guides</p>
          <ul class="mt-4 space-y-2.5 text-sm">
            <li><a href="/hsc-2026-result" class="text-slate-600 transition hover:text-indigo-700">HSC result 2026</a></li>
            <li><a href="/ssc-form-fillup-2027" class="text-slate-600 transition hover:text-indigo-700">SSC form fill-up 2027</a></li>
            <li><a href="/du-a-unit-admission-2026-27" class="text-slate-600 transition hover:text-indigo-700">DU A Unit admission</a></li>
            <li><a href="/medical-admission-2026-27" class="text-slate-600 transition hover:text-indigo-700">Medical admission</a></li>
          </ul>
        </div>
        <div>
          <p class="text-xs font-bold uppercase tracking-[0.16em] text-slate-500">Site</p>
          <ul class="mt-4 space-y-2.5 text-sm">
            <li><a href="/sitemap.xml" class="text-slate-600 transition hover:text-indigo-700">XML sitemap</a></li>
            <li><a href="/llms.txt" class="text-slate-600 transition hover:text-indigo-700">AI-readable index</a></li>
            <li><a href="/robots.txt" class="text-slate-600 transition hover:text-indigo-700">Robots.txt</a></li>
          </ul>
          <p class="mt-5 text-xs leading-5 text-slate-500">Verify every date and instruction with the official board or university source.</p>
        </div>
      </div>
    </div>
    <div class="border-t border-slate-200">
      <div class="site-container flex flex-col gap-2 py-5 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">
        <p>&copy; 2026 BoardExamBD. All rights reserved.</p>
        <p>Site updated 26 October 2026</p>
      </div>
    </div>
  </footer>
"""


def organization_schema() -> dict:
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": SITE["name"],
        "url": f"{DOMAIN}/",
        "description": SITE["description"],
        "logo": {
            "@type": "ImageObject",
            "url": LOGO,
            "width": 512,
            "height": 512,
        },
    }


def website_schema() -> dict:
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": f"{DOMAIN}/",
        "name": SITE["name"],
        "description": SITE["description"],
        "inLanguage": "en",
        "publisher": {"@id": ORG_ID},
    }


def breadcrumb_schema(items: list[tuple[str, str]]) -> dict:
    if not items:
        return {}
    page_id = items[-1][1]
    return {
        "@type": "BreadcrumbList",
        "@id": f"{page_id}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": label,
                "item": url,
            }
            for index, (label, url) in enumerate(items, start=1)
        ],
    }


def faq_schema(page: dict) -> dict:
    return {
        "@type": "FAQPage",
        "@id": f"{page['url']}#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {"@type": "Answer", "text": faq["a"]},
            }
            for faq in page.get("faqs", [])
        ],
    }


def item_list_schema(articles: list[dict], *, page_url: str, name: str = "BoardExamBD guides") -> dict:
    return {
        "@type": "ItemList",
        "@id": f"{page_url}#guide-list",
        "name": name,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "url": article["url"],
                "name": article["h1"],
            }
            for index, article in enumerate(articles, start=1)
        ],
    }


def article_schema(article: dict, words: int, minutes: int) -> dict:
    return {
        "@type": "Article",
        "@id": f"{article['url']}#article",
        "headline": article["h1"],
        "description": article["description"],
        "url": article["url"],
        "datePublished": article["published"],
        "dateModified": article["modified"],
        "author": {
            "@type": "Organization",
            "name": AUTHOR,
            "parentOrganization": {"@id": ORG_ID},
        },
        "publisher": {"@id": ORG_ID},
        "image": {
            "@type": "ImageObject",
            "url": OG_IMAGE,
            "width": 1200,
            "height": 630,
        },
        "mainEntityOfPage": {"@id": f"{article['url']}#webpage"},
        "isPartOf": {"@id": WEBSITE_ID},
        "articleSection": article["cluster"],
        "keywords": article.get("keywords", ""),
        "wordCount": words,
        "timeRequired": f"PT{minutes}M",
        "inLanguage": "en",
        "isAccessibleForFree": True,
        "copyrightHolder": {"@id": ORG_ID},
        "copyrightYear": 2026,
    }


def webpage_schema(
    page: dict,
    *,
    page_type: str = "WebPage",
    breadcrumb: dict | None = None,
    collection: dict | None = None,
    article: dict | None = None,
) -> dict:
    node = {
        "@type": page_type,
        "@id": f"{page['url']}#webpage",
        "url": page["url"],
        "name": page["title"],
        "description": page["description"],
        "isPartOf": {"@id": WEBSITE_ID},
        "inLanguage": "en",
        "datePublished": page.get("published"),
        "dateModified": page.get("modified"),
    }
    if page["file"] != "404.html":
        node["primaryImageOfPage"] = {
            "@type": "ImageObject",
            "url": OG_IMAGE,
            "width": 1200,
            "height": 630,
        }
    if article:
        node["mainEntity"] = {"@id": f"{page['url']}#article"}
    if collection:
        node["mainEntity"] = {"@id": collection["@id"]}
    if breadcrumb:
        node["breadcrumb"] = {"@id": breadcrumb["@id"]}
    return node


def build_graph(
    page: dict,
    *,
    page_type: str = "WebPage",
    article: dict | None = None,
    breadcrumb_items: list[tuple[str, str]] | None = None,
    collection_items: list[dict] | None = None,
    words: int = 0,
    minutes: int = 0,
) -> list[dict]:
    breadcrumb = breadcrumb_schema(breadcrumb_items or [])
    collection = (
        item_list_schema(collection_items, page_url=page["url"], name=page["title"])
        if collection_items
        else None
    )
    webpage = webpage_schema(
        page,
        page_type=page_type,
        breadcrumb=breadcrumb or None,
        collection=collection,
        article=article,
    )
    graph: list[dict] = [organization_schema(), website_schema(), webpage]
    if article:
        graph.append(article_schema(article, words, minutes))
    if collection:
        graph.append(collection)
    if page.get("faqs"):
        graph.append(faq_schema(page))
    if breadcrumb:
        graph.append(breadcrumb)
    return graph


def render_head(
    page: dict,
    graph: list[dict],
    *,
    og_type: str = "website",
    article: dict | None = None,
    md_path: str | None = None,
) -> str:
    title = e(page["title"])
    description = e(page["description"])
    url = e(page["url"])
    image = e(OG_IMAGE)
    image_alt = e(page["title"])
    robots = (
        "noindex, follow, noarchive"
        if page.get("noindex")
        else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    )
    keywords = page.get("keywords", "")
    article_meta = ""
    twitter_meta = ""
    if article:
        published = iso_date(article["published"])
        modified = iso_date(article["modified"])
        article_meta = f"""
  <meta property="article:published_time" content="{published}">
  <meta property="article:modified_time" content="{modified}">
  <meta property="article:section" content="{e(article['cluster'])}">
  <meta property="article:tag" content="{e(kicker_for(article))}">"""
        twitter_meta = f"""
  <meta name="twitter:label1" content="Updated">
  <meta name="twitter:data1" content="{e(display_date(article['modified']))}">"""
    md_link = ""
    if md_path:
        md_link = f'\n  <link rel="alternate" type="text/markdown" href="{e(md_path)}" title="Markdown version">'
    jsonld = json.dumps(
        {"@context": "https://schema.org", "@graph": graph},
        ensure_ascii=False,
        indent=2,
    ).replace("</", "<\\/")
    keyword_tag = f'\n  <meta name="keywords" content="{e(keywords)}">' if keywords else ""
    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="author" content="{e(AUTHOR)}">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="{SITE['theme_color']}">
  <meta name="color-scheme" content="light">
  <meta name="application-name" content="BoardExamBD">{keyword_tag}
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="en" href="{url}">
  <link rel="alternate" hreflang="x-default" href="{url}">{md_link}
  <link rel="sitemap" type="application/xml" title="Sitemap" href="/sitemap.xml">

  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="BoardExamBD">
  <meta property="og:locale" content="en_US">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}">
  <meta property="og:image:secure_url" content="{image}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{image_alt}">{article_meta}

  <meta name="twitter:card" content="{SITE['twitter_card']}">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{image}">
  <meta name="twitter:image:alt" content="{image_alt}">{twitter_meta}

  <link rel="icon" href="/assets/images/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="/assets/images/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/images/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png">
  <link rel="manifest" href="/assets/images/site.webmanifest">
  <meta name="format-detection" content="telephone=no">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap"></noscript>
  <link rel="stylesheet" href="/assets/css/tailwind.css">
  <link rel="stylesheet" href="/assets/css/custom.css">

  <!-- No analytics are loaded until a real GA4 measurement ID is configured. -->
  <script type="application/ld+json">
{jsonld}
  </script>
</head>"""


def render_document(
    page: dict,
    active: str | None,
    main_inner: str,
    graph: list[dict],
    *,
    og_type: str = "website",
    article: dict | None = None,
    md_path: str | None = None,
) -> str:
    return f"""{render_head(page, graph, og_type=og_type, article=article, md_path=md_path)}
<body class="flex min-h-screen flex-col bg-white text-slate-700 antialiased">
  <a href="#main-content" class="sr-only focus:not-sr-only focus:fixed focus:left-3 focus:top-3 focus:z-[200] focus:rounded-lg focus:bg-white focus:px-4 focus:py-3 focus:text-sm focus:font-bold focus:text-indigo-700 focus:shadow-xl">Skip to main content</a>
{site_header(active)}
  <main id="main-content" tabindex="-1" class="flex-1">
{main_inner}
  </main>
{site_footer()}
</body>
</html>
"""


def render_article_card(article: dict, *, show_cluster: bool = True, compact: bool = False) -> str:
    style = cluster_style(article["cluster"])
    badge = cluster_badge(article["cluster"]) if show_cluster else ""
    title_size = "text-base" if compact else "text-lg"
    padding = "p-4" if compact else "p-5"
    description = "" if compact else f'<p class="mt-2 text-sm leading-6 text-slate-600">{e(article["description"])}</p>'
    return f"""
<article class="group flex h-full flex-col rounded-2xl border border-slate-200 bg-white {padding} shadow-sm transition hover:-translate-y-0.5 hover:border-indigo-200 hover:shadow-soft">
  <div class="flex flex-wrap items-center gap-2">
    {badge}
    <span class="text-xs text-slate-500">Updated {e(display_date(article['modified'], short=True))}</span>
  </div>
  <h3 class="mt-3 {title_size} font-bold leading-6 text-slate-900">
    <a href="{e(article['path'])}" class="transition group-hover:text-indigo-700">{e(card_title(article))}</a>
  </h3>
  {description}
  <span class="mt-auto inline-flex items-center gap-1 pt-4 text-sm font-semibold {style['text']}">Read guide <span aria-hidden="true">&rarr;</span></span>
</article>"""


def render_faqs(page: dict) -> str:
    if not page.get("faqs"):
        return ""
    items = []
    for index, faq in enumerate(page["faqs"]):
        open_attr = " open" if index == 0 else ""
        items.append(
            f"""
<details class="faq-item group rounded-xl border border-slate-200 bg-white shadow-sm"{open_attr}>
  <summary class="flex cursor-pointer list-none items-center justify-between gap-4 px-4 py-4 font-semibold text-slate-900 marker:content-none">
    <span>{e(faq['q'])}</span>
    <span class="faq-icon flex h-6 w-6 flex-none items-center justify-center rounded-full bg-indigo-50 text-lg leading-none text-indigo-700 transition-transform" aria-hidden="true">+</span>
  </summary>
  <div class="px-4 pb-4 text-sm leading-6 text-slate-600"><p>{e(faq['a'])}</p></div>
</details>"""
        )
    return f"""
<section id="faqs" aria-labelledby="faqs-title" class="mt-12 scroll-mt-24">
  <h2 id="faqs-title" class="text-2xl font-extrabold tracking-tight text-slate-900">Frequently asked questions</h2>
  <p class="mt-2 text-sm text-slate-500">Short answers based on the dates and instructions in this guide.</p>
  <div class="mt-5 space-y-3">{''.join(items)}</div>
</section>"""


def render_checklist(article: dict) -> str:
    if not article.get("checklist"):
        return ""
    items = "".join(
        f"""
<li class="flex gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
  <span class="mt-0.5 flex h-5 w-5 flex-none items-center justify-center rounded-full bg-emerald-50 text-xs font-bold text-emerald-700 ring-1 ring-inset ring-emerald-600/20" aria-hidden="true">&#10003;</span>
  <span class="text-sm leading-6 text-slate-600">{e(item)}</span>
</li>"""
        for item in article["checklist"]
    )
    return f"""
<section id="checklist" aria-labelledby="checklist-title" class="mt-12 scroll-mt-24">
  <h2 id="checklist-title" class="text-2xl font-extrabold tracking-tight text-slate-900">Quick checklist</h2>
  <p class="mt-2 text-sm text-slate-500">What to confirm before you act on this guide.</p>
  <ul class="mt-5 grid gap-3 sm:grid-cols-2">{items}</ul>
</section>"""


def render_source_list(article: dict) -> str:
    if not article.get("sources"):
        return ""
    items = "".join(
        f'<li><a href="{e(href)}" target="_blank" rel="noopener noreferrer" class="font-semibold text-indigo-600 underline decoration-indigo-200 decoration-2 underline-offset-2 hover:text-indigo-800">{e(name)} <span aria-hidden="true">&#8599;</span></a></li>'
        for name, href in article["sources"]
    )
    return f"""
<section id="sources" aria-labelledby="sources-title" class="mt-12 scroll-mt-24">
  <h2 id="sources-title" class="text-2xl font-extrabold tracking-tight text-slate-900">Official sources</h2>
  <p class="mt-2 text-sm text-slate-500">Verify dates and instructions on the original board or university portal.</p>
  <ul class="mt-4 space-y-2 text-sm">{items}</ul>
</section>"""


def render_author_box(article: dict) -> str:
    return f"""
<section id="author" aria-labelledby="author-title" class="mt-12 scroll-mt-24 rounded-2xl border border-slate-200 bg-slate-50 p-6">
  <div class="flex flex-col gap-4 sm:flex-row sm:items-start">
    <div class="flex h-12 w-12 flex-none items-center justify-center rounded-xl bg-indigo-600 text-sm font-extrabold text-white" aria-hidden="true">BE</div>
    <div>
      <h2 id="author-title" class="text-lg font-bold text-slate-900">About the author</h2>
      <p class="mt-2 text-sm leading-6 text-slate-600">The <strong class="font-semibold text-slate-900">BoardExamBD Editorial Team</strong> prepares plain-language guides to SSC, HSC and university admission notices. Each guide links to the official board or university source used for its dates and instructions.</p>
      <p class="mt-3 text-xs text-slate-500">Guide updated <time datetime="{iso_date(article['modified'])}">{e(display_date(article['modified']))}</time>. BoardExamBD is independent and is not affiliated with any education board or university.</p>
      <a href="/blog" class="mt-3 inline-flex text-sm font-semibold text-indigo-600 hover:text-indigo-800">Browse all guides <span aria-hidden="true">&rarr;</span></a>
    </div>
  </div>
</section>"""


def render_related(article: dict) -> str:
    related = [ARTICLE_BY_SLUG[slug] for slug in article.get("related", []) if slug in ARTICLE_BY_SLUG]
    if not related:
        return ""
    cards = "".join(render_article_card(item, show_cluster=True, compact=True) for item in related)
    return f"""
<section aria-labelledby="related-title" class="mt-12">
  <div class="flex flex-wrap items-end justify-between gap-3">
    <h2 id="related-title" class="text-2xl font-extrabold tracking-tight text-slate-900">Related guides</h2>
    <a href="/blog" class="text-sm font-semibold text-indigo-600 hover:text-indigo-800">All guides <span aria-hidden="true">&rarr;</span></a>
  </div>
  <div class="mt-5 grid gap-4 sm:grid-cols-3">{cards}</div>
</section>"""


def render_key_facts(cards: list[dict]) -> str:
    rendered = []
    for card in cards:
        note = (
            f'<p class="mt-1 text-xs leading-5 text-slate-500">{e(card.get("note", ""))}</p>'
            if card.get("note")
            else ""
        )
        rendered.append(
            f"""
<div class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
  <p class="text-[11px] font-bold uppercase tracking-[0.14em] text-slate-500">{e(card['label'])}</p>
  <p class="mt-1.5 text-lg font-extrabold leading-6 text-slate-900">{e(card['value'])}</p>
  {note}
</div>"""
        )
    return f"""
<section id="key-facts" aria-labelledby="key-facts-title" class="scroll-mt-24">
  <div class="flex flex-wrap items-center justify-between gap-2">
    <h2 id="key-facts-title" class="text-2xl font-extrabold tracking-tight text-slate-900">Key facts</h2>
    <span class="badge bg-indigo-50 text-indigo-700 ring-indigo-600/20">At a glance</span>
  </div>
  <div class="mt-4 grid gap-3 sm:grid-cols-2">{''.join(rendered)}</div>
</section>"""


def render_toc(entries: list[tuple[int, str, str]], article: dict) -> str:
    items = []
    for level, label, anchor in entries:
        indent = "pl-3 text-[13px]" if level == 3 else "text-sm"
        items.append(
            f'<li><a href="#{e(anchor)}" class="block rounded-md py-1.5 pr-2 leading-5 text-slate-600 transition hover:text-indigo-700 {indent}">{e(label)}</a></li>'
        )
    return f"""
<aside class="lg:sticky lg:top-24 lg:order-2" aria-labelledby="toc-title">
  <div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
    <h2 id="toc-title" class="text-xs font-bold uppercase tracking-[0.16em] text-slate-500">In this guide</h2>
    <nav aria-labelledby="toc-title" class="mt-3">
      <ul class="max-h-[55vh] space-y-0.5 overflow-y-auto pr-1 lg:max-h-[calc(100vh-10rem)]">
        {''.join(items)}
      </ul>
    </nav>
    <div class="mt-4 border-t border-slate-100 pt-4 text-xs leading-5 text-slate-500">
      <p>Updated <time datetime="{iso_date(article['modified'])}">{e(display_date(article['modified']))}</time></p>
      <a href="#main-content" class="mt-2 inline-flex font-semibold text-indigo-600 hover:text-indigo-800">Back to top <span aria-hidden="true">&uarr;</span></a>
    </div>
  </div>
</aside>"""


def render_fact_cards(facts: list[dict], *, cluster: str = "Blog") -> str:
    style = cluster_style(cluster)
    cards = "".join(
        f"""
<div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
  <div class="flex items-center gap-2">
    <span class="h-2 w-2 rounded-full {style['solid']}" aria-hidden="true"></span>
    <p class="text-[11px] font-bold uppercase tracking-[0.14em] text-slate-500">{e(fact['label'])}</p>
  </div>
  <p class="mt-2 text-xl font-extrabold leading-7 text-slate-900">{e(fact['value'])}</p>
  <p class="mt-1 text-xs leading-5 text-slate-500">{e(fact.get('note', ''))}</p>
</div>"""
        for fact in facts
    )
    return f'<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">{cards}</div>'


def render_timeline(items: list[dict], *, compact: bool = False) -> str:
    rendered = []
    for item in items:
        date_tag = (
            f'<time datetime="{e(item["iso"])}" class="text-xs font-bold uppercase tracking-[0.12em] text-slate-500">{e(item["date"])}</time>'
            if item.get("iso")
            else f'<span class="text-xs font-bold uppercase tracking-[0.12em] text-slate-500">{e(item["date"])}</span>'
        )
        link = (
            f'<a href="{e(item["href"])}" class="mt-3 inline-flex items-center gap-1 text-sm font-semibold text-indigo-600 hover:text-indigo-800">{e(item.get("link_label", "Read the guide"))} <span aria-hidden="true">&rarr;</span></a>'
            if item.get("href")
            else ""
        )
        card_pad = "p-4" if compact else "p-5"
        rendered.append(
            f"""
<li class="relative pl-7">
  <span class="absolute left-0 top-5 h-3.5 w-3.5 -translate-x-[7px] rounded-full border-2 border-white bg-indigo-600" aria-hidden="true"></span>
  <article class="rounded-xl border border-slate-200 bg-white {card_pad} shadow-sm">
    <div class="flex flex-wrap items-center gap-2">{status_badge(item['status'])}{date_tag}</div>
    <h3 class="mt-2 font-bold text-slate-900">{e(item['title'])}</h3>
    <p class="mt-1 text-sm leading-6 text-slate-600">{e(item['text'])}</p>
    {link}
  </article>
</li>"""
        )
    return f'<ol class="relative ml-3 mt-6 space-y-5 border-l border-slate-200">{"".join(rendered)}</ol>'
