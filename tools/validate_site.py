"""Local QA for the generated BoardExamBD site.

Run:
    python tools/validate_site.py

Checks every indexable page, the article furniture, structured data,
internal links, sitemap, robots, Markdown mirrors, and shared assets.
"""

from __future__ import annotations

import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup
from PIL import Image

from seo_config import ALL_INDEXABLE, ALL_PAGES, ARTICLES, HUBS, PAGE_BY_FILE, SITE

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = SITE["domain"]
PLACEHOLDER = re.compile(
    r"PAGE_TITLE|PAGE_DESCRIPTION|Sample content|Lorem ipsum|placeholder|TBD|TODO|FIXME",
    re.IGNORECASE,
)
FAILURES: list[str] = []


def fail(message: str) -> None:
    FAILURES.append(message)


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def attr(soup: BeautifulSoup, name: str) -> str:
    tag = soup.find("meta", attrs={"name": name})
    return (tag.get("content") or "").strip() if tag else ""


def prop(soup: BeautifulSoup, name: str) -> str:
    tag = soup.find("meta", attrs={"property": name})
    return (tag.get("content") or "").strip() if tag else ""


def png_bit_depth(path: Path) -> int | None:
    data = path.read_bytes()[:26]
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        return None
    return data[24]


def check_jsonld(soup: BeautifulSoup, page: dict) -> None:
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    if len(scripts) != 1:
        fail(f"{page['file']}: expected 1 JSON-LD block, found {len(scripts)}")
        return
    try:
        data = json.loads(scripts[0].string or "{}")
    except json.JSONDecodeError as exc:
        fail(f"{page['file']}: invalid JSON-LD: {exc}")
        return
    graph = data.get("@graph")
    if not isinstance(graph, list) or not graph:
        fail(f"{page['file']}: JSON-LD has no @graph")
        return
    types = [node.get("@type") for node in graph if isinstance(node, dict)]
    page_type = "CollectionPage" if page["type"] in ("Category hub", "Blog hub") else "WebPage"
    for required in ("Organization", "WebSite", page_type):
        if required not in types:
            fail(f"{page['file']}: JSON-LD missing {required}")
    if page["type"] == "Article":
        if "Article" not in types:
            fail(f"{page['file']}: JSON-LD missing Article")
        article_node = next((n for n in graph if n.get("@type") == "Article"), {})
        if article_node.get("headline") != page["h1"]:
            fail(f"{page['file']}: Article headline does not match H1")
        if article_node.get("wordCount", 0) < 300:
            fail(f"{page['file']}: Article wordCount is too low")
    if page["type"] in ("Category hub", "Blog hub"):
        if "CollectionPage" not in types or "ItemList" not in types:
            fail(f"{page['file']}: collection schema incomplete")
    if page.get("faqs"):
        faq = next((n for n in graph if n.get("@type") == "FAQPage"), None)
        if faq is None:
            fail(f"{page['file']}: FAQ schema missing")
        elif len(faq.get("mainEntity", [])) != len(page["faqs"]):
            fail(f"{page['file']}: FAQ schema count mismatch")
    if page["type"] not in ("Home", "Utility"):
        if "BreadcrumbList" not in types:
            fail(f"{page['file']}: breadcrumb schema missing")
    ids = [node.get("@id") for node in graph if isinstance(node, dict) and node.get("@id")]
    if len(ids) != len(set(ids)):
        fail(f"{page['file']}: duplicate @id values in JSON-LD")


def check_links(soup: BeautifulSoup, page: dict) -> None:
    checked = 0
    for tag in soup.find_all(["a", "img", "link", "source"]):
        for key in ("href", "src"):
            value = tag.get(key)
            if not value:
                continue
            value = value.strip()
            if value.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
                continue
            parsed = urlparse(value)
            if parsed.scheme in ("http", "https"):
                if not value.startswith(DOMAIN):
                    continue
                path = parsed.path
            else:
                path = parsed.path
            if not path or path == "/":
                target = ROOT / "index.html"
            elif path.startswith("/"):
                target = ROOT / unquote(path.lstrip("/"))
            else:
                target = (ROOT / page["file"]).parent / unquote(path)
            if target.suffix == "" and target.is_dir():
                target = target / "index.html"
            if not target.exists():
                fail(f"{page['file']}: broken internal reference {value!r}")
            checked += 1
    if checked < 10:
        fail(f"{page['file']}: unexpectedly few internal references ({checked})")


def check_page(page: dict) -> None:
    path = ROOT / page["file"]
    if not path.exists():
        fail(f"{page['file']}: file missing")
        return
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    if soup.html.get("lang") != "en":
        fail(f"{page['file']}: html lang is not en")
    if soup.find("meta", attrs={"name": "viewport"}) is None:
        fail(f"{page['file']}: viewport meta missing")

    title = norm(soup.title.get_text()) if soup.title else ""
    description = attr(soup, "description")
    if title != page["title"]:
        fail(f"{page['file']}: title differs from config")
    min_title = 20 if page["type"] == "Utility" else 30
    if len(title) < min_title or len(title) > 60:
        fail(f"{page['file']}: title length {len(title)} outside {min_title}-60")
    if description != page["description"]:
        fail(f"{page['file']}: description differs from config")
    if len(description) < 70 or len(description) > 160:
        fail(f"{page['file']}: description length {len(description)} outside 70-160")

    expected_robots = "noindex" if page.get("noindex") else "index, follow"
    robots = attr(soup, "robots")
    if expected_robots not in robots:
        fail(f"{page['file']}: robots {robots!r} does not contain {expected_robots!r}")

    canonical = soup.find("link", rel="canonical")
    if not canonical or canonical.get("href") != page["url"]:
        fail(f"{page['file']}: canonical missing or incorrect")

    for date_key in ("published", "modified"):
        value = page.get(date_key, "")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            fail(f"{page['file']}: {date_key} must be a date-only value, got {value!r}")

    og_type = "article" if page["type"] == "Article" else "website"
    og_checks = {
        "og:title": page["title"],
        "og:description": page["description"],
        "og:type": og_type,
        "og:site_name": "BoardExamBD",
        "og:url": page["url"],
        "og:image": SITE["og_image"],
        "og:image:width": "1200",
        "og:image:height": "630",
    }
    for key, expected in og_checks.items():
        if prop(soup, key) != expected:
            fail(f"{page['file']}: {key} missing or incorrect")
    for key in ("og:image:alt", "og:image:secure_url", "og:image:type"):
        if not prop(soup, key):
            fail(f"{page['file']}: {key} missing")

    twitter = {
        "twitter:card": SITE["twitter_card"],
        "twitter:title": page["title"],
        "twitter:description": page["description"],
        "twitter:image": SITE["og_image"],
    }
    for key, expected in twitter.items():
        if attr(soup, key) != expected:
            fail(f"{page['file']}: {key} missing or incorrect")
    if not attr(soup, "twitter:image:alt"):
        fail(f"{page['file']}: twitter:image:alt missing")

    h1s = soup.find_all("h1")
    if len(h1s) != 1:
        fail(f"{page['file']}: expected exactly 1 H1, found {len(h1s)}")
    elif norm(h1s[0].get_text(" ", strip=True)) != norm(page["h1"]):
        fail(f"{page['file']}: H1 does not match config")

    if page["type"] not in ("Home", "Utility"):
        breadcrumb = soup.find("nav", attrs={"aria-label": "Breadcrumb"})
        if breadcrumb is None:
            fail(f"{page['file']}: visible breadcrumb missing")

    if soup.find("script", src="https://cdn.tailwindcss.com") or "cdn.tailwindcss.com" in html:
        fail(f"{page['file']}: Tailwind Play CDN is still referenced")
    if not soup.find("link", href="/assets/css/tailwind.css"):
        fail(f"{page['file']}: compiled Tailwind stylesheet not linked")

    if PLACEHOLDER.search(html):
        fail(f"{page['file']}: placeholder copy still present")

    check_jsonld(soup, page)
    check_links(soup, page)

    ids = [tag["id"] for tag in soup.find_all(id=True)]
    if len(ids) != len(set(ids)):
        fail(f"{page['file']}: duplicate element ids")

    for anchor in soup.find_all("a"):
        if anchor.find("a"):
            fail(f"{page['file']}: nested anchor elements are invalid")

    for image in soup.find_all("img"):
        if not (image.get("alt") or "").strip():
            fail(f"{page['file']}: image without alt text ({image.get('src')})")

    levels = [int(tag.name[1]) for tag in soup.find_all(re.compile(r"^h[1-6]$"))]
    for previous, current in zip(levels, levels[1:]):
        if current > previous + 1:
            fail(f"{page['file']}: heading jump h{previous} -> h{current}")

    if page["type"] == "Article":
        md_link = soup.find("link", attrs={"type": "text/markdown"})
        expected_md = f"/md/{page['slug']}.md"
        if not md_link or md_link.get("href") != expected_md:
            fail(f"{page['file']}: Markdown alternate missing")
        md_path = ROOT / expected_md.lstrip("/")
        if not md_path.exists() or md_path.stat().st_size < 1000:
            fail(f"{page['file']}: Markdown file missing or too small")
        else:
            md_text = md_path.read_text(encoding="utf-8")
            for date_key, field in (("published", "date_published"), ("modified", "date_modified")):
                expected = f'{field}: "{page[date_key]}"'
                if expected not in md_text:
                    fail(f"{page['file']}: Markdown {field} does not match page date")
            for meta_key in ("article:published_time", "article:modified_time"):
                if prop(soup, meta_key) != page["published" if meta_key.endswith("published_time") else "modified"]:
                    fail(f"{page['file']}: {meta_key} does not match page date")
        if soup.find("aside", attrs={"aria-labelledby": "toc-title"}) is None:
            fail(f"{page['file']}: table of contents missing")
        if soup.find(id="key-facts") is None:
            fail(f"{page['file']}: key facts section missing")
        if soup.find(id="checklist") is None:
            fail(f"{page['file']}: checklist missing")
        if soup.find(id="faqs") is None:
            fail(f"{page['file']}: FAQ section missing")
        if soup.find(id="sources") is None:
            fail(f"{page['file']}: official sources missing")
        if soup.find(id="author") is None:
            fail(f"{page['file']}: author box missing")
        related = soup.find("section", attrs={"aria-labelledby": "related-title"})
        if related is None or len(related.select("article")) != len(page.get("related", [])):
            fail(f"{page['file']}: related guides incomplete")
        if len(soup.select("#faqs details")) != len(page["faqs"]):
            fail(f"{page['file']}: visible FAQ count mismatch")
        if len(soup.select("#checklist li")) != len(page["checklist"]):
            fail(f"{page['file']}: checklist count mismatch")
        if len(soup.select("#sources a")) != len(page["sources"]):
            fail(f"{page['file']}: source count mismatch")
        toc_ids = {a["href"][1:] for a in soup.select("aside[aria-labelledby='toc-title'] a[href^='#']")}
        missing = sorted(toc_ids - {tag["id"] for tag in soup.find_all(id=True)})
        if missing:
            fail(f"{page['file']}: TOC targets missing: {missing}")

    if page["type"] == "Blog hub":
        if len(soup.select("article")) != len(ARTICLES):
            fail(f"{page['file']}: blog does not list all {len(ARTICLES)} articles")
    if page["type"] == "Category hub":
        cluster = page["cluster"]
        expected = len([a for a in ARTICLES if a["cluster"] == cluster])
        if len(soup.select("#guides article")) != expected:
            fail(f"{page['file']}: hub card count is not {expected}")


def check_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    try:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"sitemap.xml: invalid XML ({exc})")
        return
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [node.text or "" for node in root.findall("sm:url/sm:loc", ns)]
    expected = [page["url"] for page in ALL_INDEXABLE]
    if len(locs) != 21:
        fail(f"sitemap.xml: expected 21 URLs, found {len(locs)}")
    if len(locs) != len(set(locs)):
        fail("sitemap.xml: duplicate URLs")
    if set(locs) != set(expected):
        missing = sorted(set(expected) - set(locs))
        extra = sorted(set(locs) - set(expected))
        fail(f"sitemap.xml: URL set mismatch; missing={missing}, extra={extra}")
    for node in root.findall("sm:url", ns):
        loc = (node.findtext("sm:loc", default="", namespaces=ns) or "").strip()
        lastmod = (node.findtext("sm:lastmod", default="", namespaces=ns) or "").strip()
        page = next((p for p in ALL_INDEXABLE if p["url"] == loc), None)
        if page and lastmod != page["modified"][:10]:
            fail(f"sitemap.xml: lastmod mismatch for {loc}")


def check_assets() -> None:
    og = ROOT / "assets/images/og-default.jpg"
    try:
        with Image.open(og) as image:
            if image.size != (1200, 630) or image.format != "JPEG":
                fail("og-default.jpg is not a 1200x630 JPEG")
    except Exception as exc:  # noqa: BLE001
        fail(f"og-default.jpg cannot be opened: {exc}")

    png_sizes = {
        "favicon-16x16.png": (16, 16),
        "favicon-32x32.png": (32, 32),
        "apple-touch-icon.png": (180, 180),
        "favicon-192x192.png": (192, 192),
        "favicon-512x512.png": (512, 512),
    }
    for name, size in png_sizes.items():
        icon_path = ROOT / "assets/images" / name
        try:
            with Image.open(icon_path) as image:
                if image.size != size:
                    fail(f"{name} has wrong dimensions {image.size}")
            if png_bit_depth(icon_path) != 8:
                fail(f"{name} is not an 8-bit PNG")
        except Exception as exc:  # noqa: BLE001
            fail(f"{name} cannot be opened: {exc}")

    ico = ROOT / "assets/images/favicon.ico"
    try:
        with Image.open(ico) as image:
            sizes = set(image.info.get("sizes", {image.size}))
            if not {(16, 16), (32, 32), (48, 48)}.issubset(sizes):
                fail(f"favicon.ico is missing expected sizes: {sorted(sizes)}")
    except Exception as exc:  # noqa: BLE001
        fail(f"favicon.ico cannot be opened: {exc}")

    manifest = json.loads((ROOT / "assets/images/site.webmanifest").read_text(encoding="utf-8"))
    if manifest.get("name") != "BoardExamBD — SSC, HSC & Admission Guides":
        fail("site.webmanifest name is not set")

    css = ROOT / "assets/css/tailwind.css"
    if not css.exists() or css.stat().st_size < 20000:
        fail("compiled Tailwind CSS is missing or too small")
    else:
        text = css.read_text(encoding="utf-8")
        if "@tailwind" in text or "cdn.tailwindcss.com" in text:
            fail("tailwind.css still contains source directives or CDN references")
        for token in (".site-container", ".btn-primary", ".article-body", "details"):
            if token not in text:
                fail(f"tailwind.css is missing expected rule {token}")


def check_robots_and_ai() -> None:
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    for needle in ("Sitemap: https://boardexambd.com/sitemap.xml", "Disallow: /404.html", "Disallow: /SEO_TEMPLATE.html"):
        if needle not in robots:
            fail(f"robots.txt missing {needle!r}")
    if re.search(r"User-agent: \*\s*\nDisallow: /\s*$", robots, re.MULTILINE):
        fail("robots.txt blocks the whole site")

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    for page in ALL_INDEXABLE:
        if page["url"] not in llms:
            fail(f"llms.txt missing {page['url']}")
    for article in ARTICLES:
        if f"https://boardexambd.com/md/{article['slug']}.md" not in llms:
            fail(f"llms.txt missing Markdown link for {article['slug']}")
    for bad in ("404.html", "SEO_TEMPLATE.html"):
        if bad in llms:
            fail(f"llms.txt references {bad}")

    template = (ROOT / "SEO_TEMPLATE.html").read_text(encoding="utf-8")
    if "noindex, nofollow" not in template:
        fail("SEO_TEMPLATE.html is not fully noindex")


def check_duplicates() -> None:
    for key in ("title", "description"):
        values = [page[key] for page in ALL_PAGES]
        duplicates = {value for value in values if values.count(value) > 1}
        if duplicates:
            fail(f"duplicate {key}s: {sorted(duplicates)}")


def main() -> int:
    print("BoardExamBD local QA")
    print("-" * 60)
    for page in ALL_PAGES:
        before = len(FAILURES)
        check_page(page)
        status = "PASS" if len(FAILURES) == before else f"FAIL ({len(FAILURES) - before})"
        print(f"{page['file']:<38} {status}")

    print("-" * 60)
    for label, func in (
        ("sitemap.xml", check_sitemap),
        ("shared assets", check_assets),
        ("robots.txt / llms.txt", check_robots_and_ai),
        ("duplicate metadata", check_duplicates),
    ):
        before = len(FAILURES)
        func()
        print(f"{label:<38} {'PASS' if len(FAILURES) == before else 'FAIL'}")

    print("-" * 60)
    if FAILURES:
        print(f"{len(FAILURES)} issue(s) found:")
        for item in FAILURES:
            print(f"  - {item}")
        return 1
    print(f"All checks passed for {len(ALL_PAGES)} pages, {len(ALL_INDEXABLE)} indexable URLs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
