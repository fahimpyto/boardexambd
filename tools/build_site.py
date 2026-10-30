"""Build every page, the sitemap, robots file, AI index and Markdown mirrors."""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

from article_renderer import render_article_page
from content_loader import article_markdown
from hub_renderers import render_404_page, render_blog_page, render_home_page, render_hub_page
from seo_config import ALL_INDEXABLE, ARTICLES, BLOG, HOME, HUBS, NOT_FOUND, SITE

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = SITE["domain"]
DATE = "2026-10-30"


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    if path.endswith(".html"):
        content = "\n".join(line.rstrip() for line in content.splitlines()) + "\n"
    target.write_text(content, encoding="utf-8", newline="\n")
    print(f"  wrote {path}")


def build_sitemap() -> str:
    priority = {
        "Home": "1.0",
        "Category hub": "0.9",
        "Blog hub": "0.8",
        "Article": "0.7",
    }
    changefreq = {
        "Home": "weekly",
        "Category hub": "weekly",
        "Blog hub": "weekly",
        "Article": "monthly",
    }
    items = []
    for page in ALL_INDEXABLE:
        items.append(
            f"""  <url>
    <loc>{escape(page['url'])}</loc>
    <lastmod>{page['modified'][:10]}</lastmod>
    <changefreq>{changefreq.get(page['type'], 'monthly')}</changefreq>
    <priority>{priority.get(page['type'], '0.7')}</priority>
  </url>"""
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(items)
        + "\n</urlset>\n"
    )


def build_robots() -> str:
    ai_agents = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "PerplexityBot", "Google-Extended", "CCBot"]
    ai_rules = "\n\n".join(f"User-agent: {agent}\nAllow: /" for agent in ai_agents)
    return f"""# BoardExamBD robots.txt
# Search engines and AI crawlers are welcome. Verify content with official sources.

User-agent: *
Allow: /
Disallow: /404
Disallow: /SEO_TEMPLATE

{ai_rules}

Sitemap: {DOMAIN}/sitemap.xml
"""


def build_llms() -> str:
    lines = [
        "# BoardExamBD",
        "",
        "> BoardExamBD publishes clear, source-linked guides to SSC, HSC and university admission notices, routines, results, form fill-up dates and admission tests in Bangladesh. Every guide links to the official board or university portal used for its facts.",
        "",
        f"- Canonical site: {DOMAIN}/",
        "- Language: English",
        f"- Site last updated: {DATE}",
        "- Audience: SSC and HSC students, admission candidates, parents and teachers in Bangladesh",
        "- Editorial note: BoardExamBD is independent and is not affiliated with any education board or university. Always verify final dates and instructions with the official source.",
        "",
        "## Core pages",
        "",
        f"- [Home]({DOMAIN}/): Latest SSC, HSC and admission notices, routines, results and form fill-up dates.",
        f"- [SSC hub]({DOMAIN}/ssc): SSC routine, result, form fill-up and board challenge guides.",
        f"- [HSC hub]({DOMAIN}/hsc): HSC routine, result, practical exam and form fill-up guides.",
        f"- [Admission hub]({DOMAIN}/admission): DU, BUET, medical, GST, RU, RUET, KU and SUST admission dates.",
        f"- [All guides]({DOMAIN}/blog): Every BoardExamBD guide in one place.",
        "",
        "## SSC guides",
        "",
    ]
    for article in ARTICLES:
        if article["cluster"] == "SSC":
            lines.append(
                f"- [{article['h1']}]({article['url']}): {article['description']} Markdown: [{article['slug']}.md]({DOMAIN}/md/{article['slug']}.md)"
            )
    lines += ["", "## HSC guides", ""]
    for article in ARTICLES:
        if article["cluster"] == "HSC":
            lines.append(
                f"- [{article['h1']}]({article['url']}): {article['description']} Markdown: [{article['slug']}.md]({DOMAIN}/md/{article['slug']}.md)"
            )
    lines += ["", "## University admission guides", ""]
    for article in ARTICLES:
        if article["cluster"] == "Admission":
            lines.append(
                f"- [{article['h1']}]({article['url']}): {article['description']} Markdown: [{article['slug']}.md]({DOMAIN}/md/{article['slug']}.md)"
            )
    lines += [
        "",
        "## Machine-readable files",
        "",
        f"- [XML sitemap]({DOMAIN}/sitemap.xml)",
        f"- [Robots policy]({DOMAIN}/robots.txt)",
        "",
        "## Optional",
        "",
        "- The HTML pages are canonical. The Markdown files mirror the guide body for AI tools and plain-text readers.",
        "- The shared Open Graph image is `/assets/images/og-default.jpg`.",
        "",
    ]
    return "\n".join(lines)


def build_template() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SEO Template (Noindex) | BoardExamBD</title>
  <meta name="description" content="Internal SEO reference template for BoardExamBD. This page is not part of the public site.">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <link rel="canonical" href="{DOMAIN}/SEO_TEMPLATE">
  <link rel="icon" href="/assets/images/favicon.ico" sizes="any">
  <link rel="stylesheet" href="/assets/css/tailwind.css">
</head>
<body class="bg-white p-8 text-slate-700">
  <main class="mx-auto max-w-2xl">
    <h1 class="text-3xl font-extrabold text-slate-900">SEO template (internal)</h1>
    <p class="mt-4 leading-7">This page is deliberately marked <code class="rounded bg-slate-100 px-1.5 py-0.5">noindex</code>. It is not included in the sitemap or the page tracker.</p>
    <p class="mt-4 leading-7">Production pages are generated by <code class="rounded bg-slate-100 px-1.5 py-0.5">tools/build_site.py</code> using the shared metadata in <code class="rounded bg-slate-100 px-1.5 py-0.5">tools/seo_config.py</code>. Open <a class="font-semibold text-indigo-600 underline" href="/SEO_Tracker.xlsx">SEO_Tracker.xlsx</a> for page-by-page status.</p>
    <p class="mt-4"><a class="font-semibold text-indigo-600 underline" href="/">Back to BoardExamBD</a></p>
  </main>
</body>
</html>
"""


def build_manifest() -> dict:
    return {
        "name": "BoardExamBD — SSC, HSC & Admission Guides",
        "short_name": "BoardExamBD",
        "description": SITE["description"],
        "id": "/",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": SITE["theme_color"],
        "lang": "en",
        "dir": "ltr",
        "categories": ["education", "reference"],
        "icons": [
            {
                "src": "/assets/images/favicon-192x192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": "/assets/images/favicon-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any",
            },
        ],
        "shortcuts": [
            {"name": "SSC guides", "url": "/ssc"},
            {"name": "HSC guides", "url": "/hsc"},
            {"name": "Admission tracker", "url": "/admission"},
            {"name": "All guides", "url": "/blog"},
        ],
    }


def main() -> None:
    print("Building BoardExamBD")
    for article in ARTICLES:
        write(article["file"], render_article_page(article))

    for hub in HUBS:
        write(hub["file"], render_hub_page(hub))

    write(HOME["file"], render_home_page())
    write(BLOG["file"], render_blog_page())
    write(NOT_FOUND["file"], render_404_page())

    write("sitemap.xml", build_sitemap())
    write("robots.txt", build_robots())
    write("llms.txt", build_llms())
    write("SEO_TEMPLATE.html", build_template())
    write("assets/images/site.webmanifest", json.dumps(build_manifest(), ensure_ascii=False, indent=2) + "\n")

    for article in ARTICLES:
        write(f"md/{article['slug']}.md", article_markdown(article))

    print(f"Done. {len(ALL_INDEXABLE)} indexable pages + 404 page.")


if __name__ == "__main__":
    main()
