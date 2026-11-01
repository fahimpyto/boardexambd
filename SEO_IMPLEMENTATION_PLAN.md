# BoardExamBD SEO Implementation Plan

**Status:** Implemented locally on 26 October 2026. Deployment and live validation are pending.

This document describes the current SEO implementation, not the original site plan. See `PLAN.md` for the archived initial plan.

## 1. Scope

The built site contains **22 HTML pages**:

| Page type | Count | Indexable |
|---|---:|---|
| Home | 1 | Yes |
| Category hubs (`ssc.html`, `hsc.html`, `admission.html`) | 3 | Yes |
| Blog hub (`blog.html`) | 1 | Yes |
| Articles | 16 | Yes |
| 404 utility page | 1 | No |
| **Total** | **22** | **21 indexable URLs** |

`404.html` uses `noindex` and is excluded from `sitemap.xml` and progress totals. `SEO_TEMPLATE.html` is an internal utility page and is also excluded from the sitemap and tracker.

## 2. Canonical domain and identity

- Canonical origin: `https://boardexambd.com`
- Author and publisher: `BoardExamBD Editorial Team`
- Structured-data organisation: `Organization` with the BoardExamBD logo
- Language: English (`en`)
- Theme colour: `#4F46E5`
- Shared OG image: `https://boardexambd.com/assets/images/og-default.jpg` (1200 × 630 JPEG)
- Social card: `summary_large_image`

The domain does not resolve yet. Canonicals, sitemap URLs and structured-data IDs already use the production origin, so they must not be changed to a staging host in committed output.

## 3. On-page metadata

Every indexable page has:

- A unique `<title>` and meta description.
- A self-referencing canonical URL.
- `hreflang="en"` and `x-default` alternates.
- Robots directives with large image and snippet previews.
- Open Graph title, description, type, URL, site name, locale and image.
- Twitter Card title, description, image and image alt text.
- Exactly one H1.
- A visible breadcrumb except on the home page.
- One JSON-LD graph containing `Organization`, `WebSite` and the page schema.

Article pages additionally have:

- `Article` schema with headline, description, dates, author, publisher, image, word count and reading time.
- `BreadcrumbList` and `FAQPage` schema where applicable.
- `article:published_time`, `article:modified_time`, `article:section` and `article:tag` meta tags.
- A Markdown alternate link and Markdown file.

Hub and blog pages use `CollectionPage`, `ItemList` and `BreadcrumbList` schema. Hubs also use `FAQPage`.

## 4. Article content furniture

Each of the 16 guides contains, in this order:

1. Breadcrumb and hero.
2. H1, deck and meta row (updated, published, author, read time).
3. Sticky table of contents generated from H2/H3 headings.
4. Key facts cards from the original guide.
5. Preserved article body with H2/H3 hierarchy.
6. Quick checklist.
7. Three to five FAQs in accessible `<details>` elements.
8. Official source links.
9. Author box.
10. Related guides.

Original article facts and body text are preserved in `svc:*` HTML markers. Rebuilds are idempotent and must not change factual claims, dates or official instructions.

## 5. Navigation and internal linking

- Header navigation: Home, SSC, HSC, Admission, Blog.
- Home page links to all three category hubs and recent guides.
- Category hubs list every guide in their cluster.
- Blog hub lists all 16 guides.
- Each article links to three related guides, its cluster hub via breadcrumb, the author box and the blog hub.
- Footer links to the main hubs, popular guides, sitemap, `llms.txt` and `robots.txt`.
- Mobile navigation uses the existing CSS-only checkbox pattern and has an accessible label.

## 6. Crawler and AI files

- `sitemap.xml`: 21 indexable URLs with `lastmod`, `changefreq` and priority.
- `robots.txt`: allows search and AI crawlers; disallows `/404` and `/SEO_TEMPLATE`; declares the sitemap.
- `llms.txt`: site summary, core pages, all SSC/HSC/admission guides and their Markdown mirrors.
- `md/<slug>.md`: one Markdown mirror per article with YAML front matter, key facts, body, checklist, FAQs, sources and author note.
- `assets/images/site.webmanifest`: app name, icons, colours and shortcuts.

## 7. Performance and assets

- Tailwind 3.4.17 is compiled to `assets/css/tailwind.css`; no Play CDN reference remains.
- The compiled stylesheet and `custom.css` are linked on every page.
- Fonts use `preconnect`, a preload hint and a non-blocking stylesheet load with a `<noscript>` fallback.
- Favicons are generated at 16, 32, 180, 192 and 512 pixels plus a multi-size ICO. All PNGs are 8-bit.
- The shared OG image is a 1200 × 630 JPEG resized from the supplied banner.
- No JavaScript framework or analytics script is loaded.

## 8. Build and QA pipeline

Build order:

```powershell
python tools/build_site.py
npm run build:css
python tools/validate_site.py
```

`tools/validate_site.py` checks all 22 pages and all 21 indexable URLs for:

- Titles, descriptions, robots, canonicals, OG and Twitter tags.
- JSON-LD types, FAQ counts, duplicate IDs and heading hierarchy.
- Exactly one H1 per page.
- Internal links and required article sections.
- TOC targets, related-guide counts, checklist counts and source counts.
- Sitemap URL set and `lastmod` values.
- Markdown alternates and files.
- Favicon dimensions and bit depth, OG image dimensions and compiled CSS.
- `robots.txt`, `llms.txt` and the `noindex` template.
- Duplicate titles and descriptions.

Local browser QA is performed with Playwright and Microsoft Edge at 1440 px and 390 px. It covers horizontal overflow, console errors, failed local requests, one H1 per page and the mobile menu on every page.

## 9. Tracker workflow

`SEO_Tracker.xlsx` tracks each page on the `Pages` sheet. A row is marked Done only after:

1. The page builds successfully.
2. `validate_site.py` passes.
3. The page passes the browser smoke test.
4. Metadata and content requirements have been checked manually.

The tracker dashboard excludes the 404 utility row from progress, and the sitemap coverage counts only indexable pages. Issues 1–6 remain open; issues 7 and 8 are completed.

Running `python tools/make_tracker.py` recreates the workbook and resets all page statuses to “Not started.”

## 10. Pending work

| Item | Status |
|---|---|
| DNS and hosting for `boardexambd.com` | Blocked |
| Live Rich Results, Schema Validator, Lighthouse and social preview checks | Pending deploy |
| Real GA4, Search Console, Bing and Pinterest IDs | Not supplied; analytics omitted |
| Per-page Open Graph images | Pending design |
| HSC 2026 result post-publication update | Done — published 31 October 2026 |
| SSC 2027 form fill-up post-window update | Pending after 23 November 2026 |

No unverified dates, times or claims should be added while completing these items.
