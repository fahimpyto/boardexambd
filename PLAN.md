# BoardExamBD — Project Plan

Static website for **SSC, HSC & University Admission** notices and routines in Bangladesh.
Stack: plain HTML + Tailwind CSS. Simple, clean, scalable.

---

## 1. Overview

- **Site name:** BoardExamBD
- **Purpose:** One-stop place for board exam notices & routines (SSC/HSC) and university admission updates.
- **Audience:** Bangladeshi SSC/HSC students and admission candidates.
- **Type:** Static multi-page site (no backend, **zero JavaScript**)

## 2. Tech Choices

| Choice | Value | Why |
|---|---|---|
| HTML | HTML5, one file per page | Simplest, easy to host anywhere |
| CSS | Tailwind CSS via **Play CDN** `<script src="https://cdn.tailwindcss.com"></script>` | Zero build step, works by opening files directly. Can migrate to Tailwind CLI later for production |
| **JavaScript** | **None (0 scripts)** — all interactions done with pure HTML+CSS via Tailwind's `peer`/`peer-checked` utilities, checkbox dropdown pattern and `<details>` element | Mobile menu, dropdowns and collapsible panels work with no JS at all |
| Fonts | Google Fonts: `Inter` (Latin) — English-only site | Clean, readable |
| Config | `tailwind.config` inline: custom accent color + Inter font | Consistent branding |

## 3. Branding & Design Language

- **Logo:** Text logo — `Board` (gray-800) + `Exam` (accent) + `BD` badge (accent bg, white text, rounded).
- **Accent color:** Indigo (`indigo-600`) primary; `emerald` for success/updates; `rose` for "Important".
- **Theme:** Light only. White background, `gray-50` section bands, `rounded-xl` cards, subtle `shadow-sm`.
- **Badges color-coded:** SSC → `sky`, HSC → `violet`, Admission → `emerald`, Important → `rose`.
- **Layout rhythm:** Max-width container `max-w-6xl`, consistent section padding `py-12/16`.

## 4. Pages (4 total, shared header/footer)

### `index.html` — Home
- Hero: site intro + search-style CTA buttons linking to the 3 sections.
- 3 category cards (SSC / HSC / Admission) with description + link.
- "Latest Updates" section: 6 newest notices across all categories (card grid).
- Info banner: data-update note + disclaimer.

### `ssc.html` — SSC
- Page intro strip (breadcrumb-lite + title).
- **SSC Notices** list (notice card component, latest first).
- **SSC Routine 2026** table: date, day, subject, time, group/board notes.
- Routine note bar (e.g., "Dates as per Education Board notice — verify before exam").

### `hsc.html` — HSC
- Same structure as SSC: notices list + HSC routine table.

### `admission.html` — Admission
- Admission notices list (universities tagged per-card: DU, BUET, Medical, GST, etc.).
- **Admission Timeline** section: circular/date cards for key phases (application, admit card, exam).
- **Requirements overview** table (GPA minimums, unit info — placeholder to edit).

## 5. Shared Components (100% JS-free)

1. **Header (sticky):** logo left; nav: Home · SSC · HSC · Admission (active link highlighted with accent pill — **hardcoded per page**, no JS detection). Mobile: a hidden `<input type="checkbox">` + label "hamburger" button using Tailwind's `peer`/`peer-checked` utilities toggles the menu with **pure CSS**.
2. **Notice card:** left date block (day + month), title, category badge, one-line summary, "Read more →" link.
3. **Data table:** striped rows, `text-sm`, `md:` padded, horizontally scrollable wrapper on mobile (`overflow-x-auto`).
4. **Page hero strip (subpages):** `bg-indigo-600` band with page title + short subtitle.
5. **Footer:** logo, quick links, disclaimer ("BoardExamBD is an informational site and is not affiliated with any education board or university"), **copyright year hardcoded** (e.g. © 2026) — updated manually, not with a JS date script.

## 6. File Structure

```
E:\ssc-hsc-admission\
├── PLAN.md            ← copy of this plan (created in build phase)
├── index.html
├── ssc.html
├── hsc.html
├── admission.html
└── assets\
    └── css\
        └── custom.css     ← tiny niceties only: thin scrollbar polish (optional)
```
*(no `js/` folder — the site ships with zero JavaScript files)*

## 7. Content Notes (important)

- **Routine & notice dates start as clearly-labeled placeholders** (e.g., sample rows marked "Update with official date"). I will not invent official exam dates — you replace them with real links/data later, structure is ready for it.
- Notice links (`href="#"`) until real sources are provided.
- English-only content per decision.

## 8. Build Steps

1. Write `PLAN.md` into the project root.
2. Build `index.html` with full header/footer + Tailwind config (this becomes the template for all pages), including the CSS-only mobile menu pattern.
3. Build `assets/css/custom.css` (thin scrollbar polish only).
4. Build `ssc.html`, `hsc.html`, `admission.html` reusing the same header/footer markup.
5. Hardcode the active nav state in each page's header (no JS link detection).
6. Final pass: responsive check (tables scroll on mobile, menu spacing), consistent spacing, placeholder badges on sample data.

## 9. Scalability Path (future, not in first build)

- Replace Play CDN with Tailwind CLI build for production (smaller CSS).
- If updates are needed without editing HTML later: add `notices.json` + a tiny optional renderer script — but only if wanted; the default stays zero-JS.
- Sitemap + meta descriptions + Open Graph tags for SEO.
- If the site grows: split header/footer into partials via a build step.
