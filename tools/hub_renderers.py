"""Home, category hub, blog hub and 404 page renderers."""

from __future__ import annotations

from seo_config import ARTICLES, BLOG, HOME, HUBS, NOT_FOUND
from site_components import (
    DOMAIN,
    build_graph,
    card_title,
    cluster_badge,
    cluster_style,
    display_date,
    e,
    render_article_card,
    render_document,
    render_fact_cards,
    render_faqs,
    render_source_list,
    render_timeline,
    status_badge,
    visible_breadcrumb,
)

ARTICLE_BY_CLUSTER = {
    cluster: [article for article in ARTICLES if article["cluster"] == cluster]
    for cluster in ("SSC", "HSC", "Admission")
}

HUB_BY_SLUG = {hub["slug"]: hub for hub in HUBS}

HUB_DECKS = {
    "ssc": "Every SSC notice, routine, result and form fill-up update for the nine general boards — with the dates that matter and a link to the full guide.",
    "hsc": "HSC, Alim and equivalent exam dates, practicals, results and form fill-up updates for all 11 education boards.",
    "admission": "Application windows, test dates and eligibility for DU, BUET, medical, GST, RU, RUET, KU and SUST — tracked in one place.",
}

HUB_FACTS = {
    "ssc": [
        {"label": "Boards covered", "value": "9 general boards", "note": "Dhaka, Rajshahi, Cumilla, Jashore, Barishal, Sylhet, Dinajpur, Chattogram and Mymensingh."},
        {"label": "Routine issued", "value": "15 January 2026", "note": "The 2026 routine set a 10:00 AM start for every paper."},
        {"label": "Written exams", "value": "From 11 April 2026", "note": "Bangla 1st paper was the first exam."},
        {"label": "Result published", "value": "10 August 2026", "note": "SSC, Dakhil and Vocational results went live together."},
    ],
    "hsc": [
        {"label": "Boards covered", "value": "11 boards", "note": "Nine general boards, the Madrasah board and the Technical board."},
        {"label": "Written exams", "value": "2 July – 8 August 2026", "note": "Every paper started at 10:00 AM."},
        {"label": "Practical exams", "value": "By 15 August 2026", "note": "Completed after the written papers ended."},
        {"label": "Result scheduled", "value": "29 October 2026", "note": "HSC, Alim and DIBS results are due on the same day."},
    ],
    "admission": [
        {"label": "Tracks covered", "value": "8 admission tracks", "note": "DU, BUET, medical, GST, RU, RUET, KU and SUST."},
        {"label": "DU applications", "value": "11–25 November 2026", "note": "Unit tests are scheduled from 5 to 26 December 2026."},
        {"label": "Medical test", "value": "4 December 2026 (tentative)", "note": "The date depends on the HSC result and DGME circular."},
        {"label": "BUET preliminary", "value": "16 January 2027", "note": "The full application circular is still pending."},
    ],
}

HUB_TIMELINES = {
    "ssc": [
        {"date": "15 Jan 2026", "iso": "2026-01-15", "title": "SSC 2026 routine issued", "text": "The nine general boards published the subject-wise routine with a 10:00 AM start for every paper.", "status": "Published", "href": "/ssc-2026-routine.html", "link_label": "See the full routine"},
        {"date": "11 Apr 2026", "iso": "2026-04-11", "title": "Written exams began", "text": "Bangla 1st paper was the first SSC 2026 exam. Group papers continued through late April into early May.", "status": "Completed", "href": "/ssc-2026-routine.html", "link_label": "Review the schedule"},
        {"date": "10 Aug 2026", "iso": "2026-08-10", "title": "SSC result published", "text": "SSC, Dakhil and Vocational results for all 11 boards went live at 10:00 AM.", "status": "Published", "href": "/ssc-2026-result.html", "link_label": "Check the result guide"},
        {"date": "11–17 Aug 2026", "iso": "2026-08-11", "title": "Board challenge window", "text": "Re-scrutiny applications ran by SMS at Tk 150 per paper. Challenge results were published on 10 September 2026.", "status": "Closed", "href": "/ssc-board-challenge-2026.html", "link_label": "Read the board challenge guide"},
        {"date": "16–23 Nov 2026", "iso": "2026-11-16", "title": "SSC 2027 form fill-up", "text": "The announced online window runs through schools with no late fee. The school submits candidate data to the board.", "status": "Upcoming", "href": "/ssc-form-fillup-2027.html", "link_label": "See the form fill-up process"},
    ],
    "hsc": [
        {"date": "2 Jul 2026", "iso": "2026-07-02", "title": "Written exams began", "text": "The HSC, Alim and equivalent exams started with Bangla 1st paper at 10:00 AM.", "status": "Completed", "href": "/hsc-2026-routine.html", "link_label": "See the full routine"},
        {"date": "8 Aug 2026", "iso": "2026-08-08", "title": "Written exams ended", "text": "The last written paper closed a schedule that ran for around five weeks.", "status": "Completed", "href": "/hsc-2026-routine.html", "link_label": "Review the schedule"},
        {"date": "15 Aug 2026", "iso": "2026-08-15", "title": "Practical exams completed", "text": "Lab-based and oral exams were completed at students' own institutions or assigned centres.", "status": "Completed", "href": "/hsc-practical-2026.html", "link_label": "Read the practical guide"},
        {"date": "29 Oct 2026", "iso": "2026-10-29", "title": "HSC result scheduled", "text": "HSC, Alim and DIBS results are scheduled for Thursday 29 October 2026, according to the latest board notice.", "status": "Scheduled", "href": "/hsc-2026-result.html", "link_label": "Check the result guide"},
        {"date": "Feb–Mar 2027", "title": "HSC 2027 form fill-up expected", "text": "No 2027 circular had been issued as of 23 October 2026. The window is expected around February–March, based on the last cycle.", "status": "Expected", "href": "/hsc-form-fillup-2027.html", "link_label": "See the expected process"},
    ],
}

HUB_OFFICIAL_LINKS = {
    "ssc": [
        ("Education Board Bangladesh", "https://www.educationboard.gov.bd/"),
        ("Dhaka Education Board", "https://dhakaeducationboard.gov.bd/"),
        ("Education Board Results", "https://www.educationboardresults.gov.bd/"),
    ],
    "hsc": [
        ("Education Board Bangladesh", "https://www.educationboard.gov.bd/"),
        ("Dhaka Education Board", "https://dhakaeducationboard.gov.bd/"),
        ("Education Board Results", "https://www.educationboardresults.gov.bd/"),
    ],
    "admission": [
        ("DU Admission Portal", "https://admission.eis.du.ac.bd/"),
        ("BUET Admission", "https://admission.buet.ac.bd/"),
        ("DGME Admission", "https://dgme.teletalk.com.bd/"),
        ("GST Admission", "https://gstadmission.ac.bd/"),
        ("RU Admission Portal", "https://admission.ru.ac.bd/"),
        ("KU", "https://ku.ac.bd/"),
        ("RUET Admission", "https://admission.ruet.ac.bd/"),
        ("SUST Admission", "https://admission.sust.edu.bd/"),
    ],
}

ADMISSION_ROWS = [
    {"name": "DU A Unit", "status": "Upcoming", "date": "11–25 Nov 2026", "detail": "Applications open at 12:00 noon; unit tests are scheduled from 5 to 26 December 2026.", "href": "/du-a-unit-admission-2026-27.html"},
    {"name": "Rajshahi University", "status": "Upcoming", "date": "From 12 Nov 2026", "detail": "Preliminary applications open on admission.ru.ac.bd; the announced tests are on 8, 9 and 16 January 2027.", "href": "/ru-admission-2026-27.html"},
    {"name": "Medical (MBBS/BDS)", "status": "Tentative", "date": "4 Dec 2026", "detail": "Form fill-up is expected in mid-November; the test depends on the HSC result and the DGME circular.", "href": "/medical-admission-2026-27.html"},
    {"name": "BUET", "status": "Scheduled", "date": "16 Jan 2027", "detail": "The preliminary test is set. Online applications are expected from mid-November to early December 2026.", "href": "/buet-admission-2026-27.html"},
    {"name": "GST cluster", "status": "Pending", "date": "Circular pending", "detail": "No 2026-27 circular had been published as of 23 October 2026. Last cycle's A Unit science test was on 10 April 2026.", "href": "/gst-a-unit-admission-2026-27.html"},
    {"name": "Khulna University", "status": "Closed", "date": "Closed 30 Sep 2026", "detail": "The application window has closed. The discipline-wise test schedule is still pending on ku.ac.bd.", "href": "/ku-admission-2026-27.html"},
    {"name": "RUET", "status": "Expected", "date": "Circular late Nov–Dec 2026", "detail": "The test is expected around January 2027, following the previous cycle.", "href": "/ruet-admission-2026-27.html"},
    {"name": "SUST", "status": "Expected", "date": "Circular late Oct–Nov 2026", "detail": "The A and B unit test is expected in December 2026. Last cycle it was held on 7 December 2025.", "href": "/sust-admission-2026-27.html"},
]

HOME_DATES = [
    {"day": "29", "month": "Oct", "title": "HSC Result 2026", "note": "Scheduled — all 11 boards", "href": "/hsc-2026-result.html"},
    {"day": "11", "month": "Nov", "title": "DU A Unit applications", "note": "Open at 12:00 noon", "href": "/du-a-unit-admission-2026-27.html"},
    {"day": "16", "month": "Nov", "title": "SSC 2027 form fill-up", "note": "Window opens through schools", "href": "/ssc-form-fillup-2027.html"},
]

HOME_TIMELINE = [
    {"date": "29 Oct 2026", "iso": "2026-10-29", "title": "HSC result 2026", "text": "HSC, Alim and DIBS results are scheduled for Thursday 29 October 2026, according to the latest board notice.", "status": "Scheduled", "href": "/hsc-2026-result.html", "link_label": "How to check the result"},
    {"date": "11 Nov 2026", "iso": "2026-11-11", "title": "DU A Unit applications open", "text": "Apply from 12:00 noon on 11 November until 11:59 PM on 25 November 2026. All DU unit tests are planned for 5–26 December.", "status": "Upcoming", "href": "/du-a-unit-admission-2026-27.html", "link_label": "See eligibility and steps"},
    {"date": "16 Nov 2026", "iso": "2026-11-16", "title": "SSC 2027 form fill-up opens", "text": "The announced online window runs 16–23 November 2026 with no late fee. Your school submits the candidate data to the board.", "status": "Upcoming", "href": "/ssc-form-fillup-2027.html", "link_label": "Read the form fill-up guide"},
    {"date": "4 Dec 2026", "iso": "2026-12-04", "title": "Medical admission test", "text": "The MBBS/BDS admission test is tentatively set for 4 December 2026. The date depends on the HSC result and the DGME circular.", "status": "Tentative", "href": "/medical-admission-2026-27.html", "link_label": "See the medical guide"},
    {"date": "16 Jan 2027", "iso": "2027-01-16", "title": "BUET preliminary test", "text": "BUET's preliminary admission test is set for 16 January 2027. The full application circular is still pending.", "status": "Scheduled", "href": "/buet-admission-2026-27.html", "link_label": "Read the BUET guide"},
    {"date": "Feb–Mar 2027", "title": "HSC 2027 form fill-up", "text": "No 2027 circular had been issued as of 23 October 2026. The window is expected around February–March, based on the 2026 cycle.", "status": "Expected", "href": "/hsc-form-fillup-2027.html", "link_label": "See the expected process"},
]

FEATURED_SLUGS = [
    "hsc-2026-result",
    "ssc-form-fillup-2027",
    "du-a-unit-admission-2026-27",
    "medical-admission-2026-27",
    "ssc-2026-routine",
    "buet-admission-2026-27",
]


def _hub_articles(hub: dict) -> list[dict]:
    return ARTICLE_BY_CLUSTER[hub["cluster"]]


def _article_grid(articles: list[dict]) -> str:
    return '<div class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">' + "".join(
        render_article_card(article) for article in articles
    ) + "</div>"


def _breadcrumb_for_hub(hub: dict) -> str:
    return visible_breadcrumb([("Home", "/"), (hub["cluster"], None)])


def render_hub_page(hub: dict) -> str:
    articles = _hub_articles(hub)
    style = cluster_style(hub["cluster"])
    breadcrumb_items = [
        ("Home", f"{DOMAIN}/"),
        (hub["cluster"], hub["url"]),
    ]
    graph = build_graph(
        hub,
        page_type="CollectionPage",
        breadcrumb_items=breadcrumb_items,
        collection_items=articles,
    )
    faq = render_faqs(hub)
    timeline = HUB_TIMELINES.get(hub["slug"])
    table = ""
    if hub["slug"] == "admission":
        rows = "".join(
            f"""
<tr class="border-t border-slate-100 align-top">
  <th scope="row" class="whitespace-nowrap px-4 py-4 text-left text-sm font-bold text-slate-900">{e(row['name'])}</th>
  <td class="whitespace-nowrap px-4 py-4">{status_badge(row['status'])}</td>
  <td class="whitespace-nowrap px-4 py-4 text-sm font-medium text-slate-700">{e(row['date'])}</td>
  <td class="px-4 py-4 text-sm leading-6 text-slate-600">{e(row['detail'])}</td>
  <td class="whitespace-nowrap px-4 py-4 text-sm"><a href="{row['href']}" class="font-semibold text-indigo-600 hover:text-indigo-800">Guide <span aria-hidden="true">&rarr;</span></a></td>
</tr>"""
            for row in ADMISSION_ROWS
        )
        table = f"""
<section id="admission-tracker" class="mt-14 scroll-mt-24">
  <div class="flex flex-wrap items-end justify-between gap-3">
    <div>
      <h2 class="text-2xl font-extrabold tracking-tight text-slate-900">Admission tracker</h2>
      <p class="mt-2 text-sm text-slate-500">Status reflects the notices reviewed on 23 October 2026.</p>
    </div>
    <a href="/blog.html" class="text-sm font-semibold text-indigo-600 hover:text-indigo-800">All guides <span aria-hidden="true">&rarr;</span></a>
  </div>
  <div class="mt-5 overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
    <table class="min-w-full divide-y divide-slate-200 text-left">
      <caption class="sr-only">Admission application and test status for 2026-27</caption>
      <thead class="bg-slate-50 text-xs uppercase tracking-wider text-slate-500">
        <tr>
          <th scope="col" class="px-4 py-3 font-semibold">Track</th>
          <th scope="col" class="px-4 py-3 font-semibold">Status</th>
          <th scope="col" class="px-4 py-3 font-semibold">Key date</th>
          <th scope="col" class="px-4 py-3 font-semibold">What to know</th>
          <th scope="col" class="px-4 py-3 font-semibold">Guide</th>
        </tr>
      </thead>
      <tbody class="bg-white text-slate-700">{rows}</tbody>
    </table>
  </div>
</section>"""
    timeline_html = ""
    if timeline:
        timeline_html = f"""
<section class="mt-14">
  <div class="flex flex-wrap items-end justify-between gap-3">
    <div>
      <h2 class="text-2xl font-extrabold tracking-tight text-slate-900">{"SSC 2026 timeline" if hub["slug"] == "ssc" else "HSC 2026 timeline"}</h2>
      <p class="mt-2 text-sm text-slate-500">What has happened, what is next, and where to verify it.</p>
    </div>
  </div>
  {render_timeline(timeline)}
</section>"""

    sources = HUB_OFFICIAL_LINKS.get(hub["slug"], [])
    sources_html = render_source_list({"sources": sources}) if sources else ""

    main = f"""
<section class="border-b border-slate-200 bg-gradient-to-b {style['hero']}">
  <div class="site-container py-10 sm:py-14">
    {_breadcrumb_for_hub(hub)}
    <div class="mt-6 flex flex-wrap items-center gap-2">
      {cluster_badge(hub['cluster'])}
      <span class="badge bg-white text-slate-600 ring-slate-200">Updated {e(display_date(hub['modified']))}</span>
      <span class="badge bg-white text-slate-600 ring-slate-200">{len(articles)} guides</span>
    </div>
    <h1 class="mt-4 max-w-4xl text-3xl font-extrabold tracking-tight text-slate-950 sm:text-5xl">{e(hub['h1'])}</h1>
    <p class="mt-4 max-w-3xl text-base leading-7 text-slate-600 sm:text-lg">{e(HUB_DECKS[hub['slug']])}</p>
    <div class="mt-6 flex flex-wrap gap-3">
      <a href="#guides" class="btn-primary">Browse the guides <span aria-hidden="true">&darr;</span></a>
      <a href="#faqs" class="btn-secondary">Read the FAQs</a>
    </div>
  </div>
</section>

<div class="site-container py-12">
  <section aria-labelledby="glance-title">
    <h2 id="glance-title" class="text-2xl font-extrabold tracking-tight text-slate-900">At a glance</h2>
    <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-500">The verified dates and coverage for this section, taken from the guides below.</p>
    <div class="mt-6">{render_fact_cards(HUB_FACTS[hub['slug']], cluster=hub['cluster'])}</div>
  </section>

  <section id="guides" class="mt-14 scroll-mt-24">
    <div class="flex flex-wrap items-end justify-between gap-3">
      <div>
        <h2 class="text-2xl font-extrabold tracking-tight text-slate-900">Guides in this section</h2>
        <p class="mt-2 text-sm text-slate-500">Each guide links to the official portal used for its dates and instructions.</p>
      </div>
      <a href="/blog.html" class="text-sm font-semibold text-indigo-600 hover:text-indigo-800">View all guides <span aria-hidden="true">&rarr;</span></a>
    </div>
    {_article_grid(articles)}
  </section>

  {timeline_html}
  {table}
  {faq}
  {sources_html}

  <div class="mt-10 flex gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm leading-6 text-amber-800">
    <svg class="mt-0.5 h-5 w-5 flex-none" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" /></svg>
    <p><strong>Verify before you act:</strong> dates and instructions can change. BoardExamBD is an independent guide and is not affiliated with any board or university.</p>
  </div>
</div>"""

    return render_document(
        hub,
        hub["cluster"].lower(),
        main,
        graph,
        og_type="website",
    )


def render_blog_page() -> str:
    all_articles = ARTICLES
    breadcrumb_items = [("Home", f"{DOMAIN}/"), ("Blog", BLOG["url"])]
    graph = build_graph(
        BLOG,
        page_type="CollectionPage",
        breadcrumb_items=breadcrumb_items,
        collection_items=all_articles,
    )
    groups = []
    for cluster in ("SSC", "HSC", "Admission"):
        items = ARTICLE_BY_CLUSTER[cluster]
        anchor = f"{cluster.lower()}-guides"
        groups.append(
            f"""
<section id="{anchor}" class="mt-14 scroll-mt-24">
  <div class="flex flex-wrap items-end justify-between gap-3">
    <div class="flex items-center gap-2.5">
      {cluster_badge(cluster)}
      <h2 class="text-2xl font-extrabold tracking-tight text-slate-900">{cluster} guides</h2>
    </div>
    <span class="text-sm text-slate-500">{len(items)} guides</span>
  </div>
  {_article_grid(items)}
</section>"""
        )

    main = f"""
<section class="border-b border-slate-200 bg-gradient-to-b from-indigo-50 via-white to-white">
  <div class="site-container py-10 sm:py-14">
    {visible_breadcrumb([('Home', '/'), ('Blog', None)])}
    <div class="mt-6 flex flex-wrap items-center gap-2">
      {cluster_badge('Blog', 'All guides')}
      <span class="badge bg-white text-slate-600 ring-slate-200">Updated {e(display_date(BLOG['modified']))}</span>
      <span class="badge bg-white text-slate-600 ring-slate-200">{len(all_articles)} guides</span>
    </div>
    <h1 class="mt-4 max-w-4xl text-3xl font-extrabold tracking-tight text-slate-950 sm:text-5xl">{e(BLOG['h1'])}</h1>
    <p class="mt-4 max-w-3xl text-base leading-7 text-slate-600 sm:text-lg">All BoardExamBD guides, grouped by SSC, HSC and university admission. Every guide links to the official source used for its dates and instructions.</p>
    <div class="mt-6 flex flex-wrap gap-2">
      <a href="#ssc-guides" class="btn-secondary">SSC</a>
      <a href="#hsc-guides" class="btn-secondary">HSC</a>
      <a href="#admission-guides" class="btn-secondary">Admission</a>
    </div>
  </div>
</section>

<div class="site-container py-12">
  <section aria-labelledby="how-to-use-title" class="rounded-2xl border border-slate-200 bg-slate-50 p-6">
    <h2 id="how-to-use-title" class="text-lg font-bold text-slate-900">How to use this hub</h2>
    <div class="mt-4 grid gap-4 text-sm leading-6 text-slate-600 sm:grid-cols-3">
      <p><strong class="font-semibold text-slate-900">Pick your exam.</strong> SSC and HSC sections cover routines, results, practicals and form fill-up.</p>
      <p><strong class="font-semibold text-slate-900">Check the date.</strong> Scheduled, tentative and expected dates are labelled inside each guide.</p>
      <p><strong class="font-semibold text-slate-900">Verify at the source.</strong> Every guide ends with the official portal links used for its facts.</p>
    </div>
  </section>
  {''.join(groups)}
  <div class="mt-12 rounded-2xl border border-indigo-200 bg-indigo-50 p-6">
    <p class="text-sm leading-6 text-indigo-900"><strong class="font-semibold">For AI tools and researchers:</strong> every guide has a plain-text Markdown version. Start with the <a href="/llms.txt" class="font-semibold underline decoration-indigo-300 underline-offset-2 hover:text-indigo-700">AI-readable index</a> or the <a href="/sitemap.xml" class="font-semibold underline decoration-indigo-300 underline-offset-2 hover:text-indigo-700">XML sitemap</a>.</p>
  </div>
</div>"""

    return render_document(BLOG, "blog", main, graph, og_type="website")


def _home_category_card(hub: dict) -> str:
    articles = ARTICLE_BY_CLUSTER[hub["cluster"]]
    style = cluster_style(hub["cluster"])
    descriptions = {
        "SSC": "Routine, result, form fill-up and board challenge — across the nine general boards.",
        "HSC": "Exam dates, practicals, result and the next form fill-up cycle for all 11 boards.",
        "Admission": "DU, BUET, medical, GST, RU, RUET, KU and SUST dates in one place.",
    }
    links = "".join(
        f'<li><a href="/{article["file"]}" class="text-sm font-medium text-slate-600 hover:text-indigo-700">{e(card_title(article))}</a></li>'
        for article in articles[:2]
    )
    return f"""
<div class="group flex h-full flex-col rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-0.5 hover:border-indigo-200 hover:shadow-soft">
  <div class="flex items-center justify-between gap-3">
    {cluster_badge(hub['cluster'])}
    <span class="text-xs font-semibold text-slate-500">{len(articles)} guides</span>
  </div>
  <h3 class="mt-4 text-xl font-extrabold text-slate-900">
    <a href="/{hub['file']}" class="transition group-hover:text-indigo-700">{e(hub['h1'])}</a>
  </h3>
  <p class="mt-2 text-sm leading-6 text-slate-600">{descriptions[hub['cluster']]}</p>
  <ul class="mt-4 space-y-2 border-t border-slate-100 pt-4">{links}</ul>
  <a href="/{hub['file']}" class="mt-auto inline-flex items-center gap-1 pt-4 text-sm font-semibold {style['text']}">Browse {hub['cluster']} <span aria-hidden="true">&rarr;</span></a>
</div>"""


def render_home_page() -> str:
    graph = build_graph(HOME, page_type="WebPage")
    by_slug = {article["slug"]: article for article in ARTICLES}
    featured = [by_slug[slug] for slug in FEATURED_SLUGS if slug in by_slug]
    category_cards = "".join(_home_category_card(hub) for hub in HUBS)
    featured_cards = "".join(render_article_card(article) for article in featured)
    dates = "".join(
        f"""
<li>
  <a href="{item['href']}" class="flex items-center gap-4 rounded-xl border border-slate-200 bg-white p-3 transition hover:border-indigo-200 hover:bg-indigo-50/40">
    <span class="flex h-14 w-14 flex-none flex-col items-center justify-center rounded-xl bg-indigo-50 text-indigo-700">
      <span class="text-lg font-extrabold leading-none">{item['day']}</span>
      <span class="mt-1 text-[11px] font-bold uppercase tracking-wide">{item['month']}</span>
    </span>
    <span class="min-w-0">
      <span class="block text-sm font-bold text-slate-900">{e(item['title'])}</span>
      <span class="mt-0.5 block text-xs text-slate-500">{e(item['note'])}</span>
    </span>
  </a>
</li>"""
        for item in HOME_DATES
    )
    main = f"""
<section class="border-b border-slate-200 bg-gradient-to-b from-indigo-50 via-white to-white">
  <div class="site-container py-14 sm:py-20">
    <div class="grid items-start gap-10 lg:grid-cols-[1.15fr_0.85fr]">
      <div>
        <span class="badge bg-indigo-50 text-indigo-700 ring-indigo-600/20">SSC &middot; HSC &middot; Admission</span>
        <h1 class="mt-5 max-w-3xl text-4xl font-extrabold leading-[1.08] tracking-tight text-slate-950 sm:text-5xl lg:text-6xl">{e(HOME['h1'])}</h1>
        <p class="mt-5 max-w-2xl text-base leading-7 text-slate-600 sm:text-lg">Clear, source-linked guides to exam routines, results, form fill-up and university admission dates — built for students and parents in Bangladesh.</p>
        <div class="mt-7 flex flex-wrap gap-3">
          <a href="/blog.html" class="btn-primary">Browse all guides <span aria-hidden="true">&rarr;</span></a>
          <a href="#dates" class="btn-secondary">See upcoming dates</a>
        </div>
        <div class="mt-8 flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-500">
          <span><strong class="font-semibold text-slate-800">16</strong> in-depth guides</span>
          <span><strong class="font-semibold text-slate-800">11</strong> education boards</span>
          <span><strong class="font-semibold text-slate-800">8</strong> admission tracks</span>
        </div>
        <p class="mt-3 text-xs text-slate-500">Last updated {e(display_date(HOME['modified']))}</p>
      </div>
      <aside class="rounded-2xl border border-slate-200 bg-white p-5 shadow-soft" aria-labelledby="dates-card-title">
        <div class="flex items-center justify-between gap-3">
          <h2 id="dates-card-title" class="text-sm font-bold text-slate-900">Dates to watch</h2>
          <a href="#dates" class="text-xs font-semibold text-indigo-600 hover:text-indigo-800">All dates <span aria-hidden="true">&rarr;</span></a>
        </div>
        <ul class="mt-4 space-y-2">{dates}</ul>
        <p class="mt-4 border-t border-slate-100 pt-3 text-xs leading-5 text-slate-500">Scheduled and tentative dates from the guides. Always confirm with the official source.</p>
      </aside>
    </div>
  </div>
</section>

<section class="site-container py-14">
  <div class="flex flex-wrap items-end justify-between gap-3">
    <div>
      <p class="eyebrow">Start here</p>
      <h2 class="mt-2 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">Browse by exam</h2>
    </div>
    <a href="/blog.html" class="text-sm font-semibold text-indigo-600 hover:text-indigo-800">All 16 guides <span aria-hidden="true">&rarr;</span></a>
  </div>
  <div class="mt-6 grid gap-5 lg:grid-cols-3">{category_cards}</div>
</section>

<section id="dates" class="scroll-mt-24 border-y border-slate-200 bg-slate-50">
  <div class="site-container py-14">
    <div class="max-w-3xl">
      <p class="eyebrow">Plan ahead</p>
      <h2 class="mt-2 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">Upcoming dates for students</h2>
      <p class="mt-3 text-sm leading-6 text-slate-600">The next result, application and form fill-up dates across SSC, HSC and university admission. Tentative and expected dates are labelled.</p>
    </div>
    {render_timeline(HOME_TIMELINE)}
  </div>
</section>

<section class="site-container py-14">
  <div class="flex flex-wrap items-end justify-between gap-3">
    <div>
      <p class="eyebrow">Featured</p>
      <h2 class="mt-2 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">Guides students need now</h2>
    </div>
    <a href="/blog.html" class="text-sm font-semibold text-indigo-600 hover:text-indigo-800">See every guide <span aria-hidden="true">&rarr;</span></a>
  </div>
  <div class="mt-6 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">{featured_cards}</div>
</section>

<section class="border-y border-slate-200 bg-slate-50">
  <div class="site-container py-14">
    <div class="max-w-3xl">
      <p class="eyebrow">How we work</p>
      <h2 class="mt-2 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">Built around the official notice</h2>
    </div>
    <div class="mt-6 grid gap-4 sm:grid-cols-3">
      <div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <p class="text-sm font-bold text-slate-900">Source first</p>
        <p class="mt-2 text-sm leading-6 text-slate-600">Each guide links back to the board or university portal used for its dates and instructions.</p>
      </div>
      <div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <p class="text-sm font-bold text-slate-900">Plain language</p>
        <p class="mt-2 text-sm leading-6 text-slate-600">Dates, fees and steps are written in a readable order, without burying the answer.</p>
      </div>
      <div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <p class="text-sm font-bold text-slate-900">Visible updates</p>
        <p class="mt-2 text-sm leading-6 text-slate-600">Every article shows when it was last updated so you can judge whether a date still applies.</p>
      </div>
    </div>
  </div>
</section>

<section class="site-container py-14">
  <div class="rounded-3xl bg-indigo-600 p-8 text-white sm:p-10">
    <div class="max-w-2xl">
      <p class="text-xs font-bold uppercase tracking-[0.16em] text-indigo-200">One place, every guide</p>
      <h2 class="mt-3 text-2xl font-extrabold tracking-tight sm:text-3xl">Find the next date before it passes</h2>
      <p class="mt-3 text-sm leading-6 text-indigo-100">Browse SSC, HSC and admission guides by exam, with official links on every page.</p>
    </div>
    <div class="mt-6 flex flex-wrap gap-3">
      <a href="/blog.html" class="inline-flex items-center justify-center gap-2 rounded-lg bg-white px-4 py-2.5 text-sm font-semibold text-indigo-700 shadow-sm transition hover:bg-indigo-50">Open the guide hub <span aria-hidden="true">&rarr;</span></a>
      <a href="/admission.html" class="inline-flex items-center justify-center gap-2 rounded-lg border border-white/30 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-white/10">Admission tracker</a>
    </div>
  </div>
</section>"""

    return render_document(HOME, "home", main, graph, og_type="website")


def render_404_page() -> str:
    graph = build_graph(NOT_FOUND, page_type="WebPage")
    main = f"""
<section class="border-b border-slate-200 bg-gradient-to-b from-indigo-50 via-white to-white">
  <div class="site-container py-16 text-center sm:py-24">
    <p class="eyebrow">404</p>
    <h1 class="mt-3 text-4xl font-extrabold tracking-tight text-slate-950 sm:text-5xl">{e(NOT_FOUND['h1'])}</h1>
    <p class="mx-auto mt-4 max-w-xl text-base leading-7 text-slate-600">The page you requested could not be found. It may have moved, or the link may be out of date.</p>
    <div class="mt-7 flex flex-wrap justify-center gap-3">
      <a href="/" class="btn-primary">Go to the homepage</a>
      <a href="/blog.html" class="btn-secondary">Browse all guides</a>
    </div>
  </div>
</section>
<div class="site-container py-12">
  <h2 class="text-lg font-bold text-slate-900">Popular sections</h2>
  <div class="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
    <a href="/ssc.html" class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-indigo-200 hover:shadow-soft"><span class="badge bg-sky-50 text-sky-700 ring-sky-600/20">SSC</span><p class="mt-3 font-semibold text-slate-900">SSC notices &amp; routine</p><p class="mt-1 text-sm text-slate-500">Routine, result and form fill-up.</p></a>
    <a href="/hsc.html" class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-indigo-200 hover:shadow-soft"><span class="badge bg-violet-50 text-violet-700 ring-violet-600/20">HSC</span><p class="mt-3 font-semibold text-slate-900">HSC notices &amp; routine</p><p class="mt-1 text-sm text-slate-500">Exam dates, practicals and result.</p></a>
    <a href="/admission.html" class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-indigo-200 hover:shadow-soft"><span class="badge bg-emerald-50 text-emerald-700 ring-emerald-600/20">Admission</span><p class="mt-3 font-semibold text-slate-900">University admission</p><p class="mt-1 text-sm text-slate-500">DU, BUET, medical and more.</p></a>
    <a href="/blog.html" class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-indigo-200 hover:shadow-soft"><span class="badge bg-indigo-50 text-indigo-700 ring-indigo-600/20">Blog</span><p class="mt-3 font-semibold text-slate-900">All guides</p><p class="mt-1 text-sm text-slate-500">Every BoardExamBD guide in one place.</p></a>
  </div>
</div>"""
    return render_document(NOT_FOUND, None, main, graph, og_type="website")
