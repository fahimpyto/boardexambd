"""Render the individual guide pages without changing their source facts."""

from __future__ import annotations

from content_loader import BODY_END, BODY_START, KF_END, KF_START, load_article_source
from seo_config import SITE
from site_components import (
    AUTHOR,
    DOMAIN,
    build_graph,
    card_title,
    cluster_badge,
    cluster_style,
    display_date,
    e,
    iso_date,
    kicker_for,
    render_article_card,
    render_author_box,
    render_checklist,
    render_document,
    render_faqs,
    render_key_facts,
    render_related,
    render_source_list,
    render_toc,
    visible_breadcrumb,
)


def article_hero(article: dict, source: dict) -> str:
    style = cluster_style(article["cluster"])
    breadcrumb = visible_breadcrumb(
        [
            ("Home", "/"),
            (article["cluster"], f"/{article['category_url']}"),
            (card_title(article), None),
        ]
    )
    return f"""
<section class="border-b border-slate-200 bg-gradient-to-b {style['hero']}">
  <div class="site-container pb-10 pt-8 sm:pb-12 sm:pt-10">
    {breadcrumb}
    <div class="mt-6 flex flex-wrap items-center gap-2">
      {cluster_badge(article['cluster'])}
      <span class="badge bg-white text-slate-600 ring-slate-200">{e(kicker_for(article))}</span>
      <span class="badge bg-white text-slate-600 ring-slate-200">Updated guide</span>
    </div>
    <h1 class="mt-4 max-w-4xl text-3xl font-extrabold leading-tight tracking-tight text-slate-950 sm:text-4xl lg:text-[2.85rem]">{e(article['h1'])}</h1>
    <p class="mt-4 max-w-3xl text-base leading-7 text-slate-600 sm:text-lg" data-deck>{e(source['deck'])}</p>
    <div class="mt-6 flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-slate-500">
      <span>Updated <time datetime="{iso_date(article['modified'])}" class="font-medium text-slate-700">{e(display_date(article['modified']))}</time></span>
      <span class="hidden h-1 w-1 rounded-full bg-slate-300 sm:inline-block" aria-hidden="true"></span>
      <span>Published <time datetime="{iso_date(article['published'])}">{e(display_date(article['published']))}</time></span>
      <span class="hidden h-1 w-1 rounded-full bg-slate-300 sm:inline-block" aria-hidden="true"></span>
      <span>By <a href="#author" class="font-semibold text-indigo-600 hover:text-indigo-800">{e(AUTHOR)}</a></span>
      <span class="hidden h-1 w-1 rounded-full bg-slate-300 sm:inline-block" aria-hidden="true"></span>
      <span>{source['minutes']} min read</span>
    </div>
  </div>
</section>"""


def render_article_page(article: dict) -> str:
    source = load_article_source(article)
    breadcrumb_items = [
        ("Home", f"{DOMAIN}/"),
        (article["cluster"], f"{DOMAIN}/{article['category_url']}"),
        (card_title(article), article["url"]),
    ]
    graph = build_graph(
        article,
        page_type="WebPage",
        article=article,
        breadcrumb_items=breadcrumb_items,
        words=source["words"],
        minutes=source["minutes"],
    )
    toc = render_toc(source["toc"], article)
    article_body = f"""
      <div class="article-body min-w-0" id="guide-content">
{KF_START}
{render_key_facts(source['cards'])}
{KF_END}
{BODY_START}
{source['body_rendered']}
{BODY_END}
{render_checklist(article)}
{render_faqs(article)}
{render_source_list(article)}
      </div>
{render_author_box(article)}
{render_related(article)}"""

    main = f"""{article_hero(article, source)}
  <article>
    <div class="site-container py-10 sm:py-14">
      <div class="grid gap-10 lg:grid-cols-[minmax(0,1fr)_18rem] lg:items-start lg:gap-12">
        {toc}
        <div class="min-w-0 lg:order-1">
          {article_body}
        </div>
      </div>
    </div>
  </article>"""

    return render_document(
        article,
        article["cluster"].lower(),
        main,
        graph,
        og_type="article",
        article=article,
        md_path=f"/md/{article['slug']}.md",
    )
