"""Create and update the BoardExamBD SEO tracker workbook."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.formatting.rule import CellIsRule, DataBarRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from seo_config import ALL_PAGES, SITE

TRACKER = Path("SEO_Tracker.xlsx")

HEADERS = [
    "Page", "Type", "Cluster", "URL", "Title", "Title length",
    "Description", "Description length", "H1", "H1 count", "Canonical",
    "Robots", "OG", "Twitter", "JSON-LD", "Breadcrumb", "FAQ",
    "Internal links", "Sitemap", "Markdown", "Local QA", "Live QA",
    "Status", "Done date", "Next review", "Notes",
]

WIDTHS = {
    "A": 34, "B": 14, "C": 12, "D": 48, "E": 54, "F": 12,
    "G": 64, "H": 14, "I": 52, "J": 10, "K": 42, "L": 16,
    "M": 10, "N": 10, "O": 42, "P": 12, "Q": 10, "R": 14,
    "S": 11, "T": 11, "U": 12, "V": 14, "W": 12, "X": 12,
    "Y": 14, "Z": 54,
}

HEADER_FILL = PatternFill("solid", fgColor="4F46E5")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=10)
SECTION_FILL = PatternFill("solid", fgColor="EEF2FF")
TITLE_FONT = Font(size=18, bold=True, color="1E1B4B")
SUBTITLE_FONT = Font(size=10, color="475569")
BOLD = Font(bold=True)
THIN_BORDER = Border(bottom=Side(style="thin", color="E2E8F0"))

STATUS_COLORS = {
    "Done": ("DCFCE7", "166534"),
    "In progress": ("FEF3C7", "92400E"),
    "Not started": ("F1F5F9", "475569"),
    "Blocked": ("FEE2E2", "991B1B"),
}


def _style_header(ws, row=1):
    for col in range(1, len(HEADERS) + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 32


def _setup_pages(ws):
    ws.append(HEADERS)
    _style_header(ws)
    for idx, page in enumerate(ALL_PAGES, start=2):
        indexable = page.get("indexable", True)
        faqs = page.get("faqs", [])
        is_article = page["type"] == "Article"
        row = [
            page["file"],
            page["type"],
            page["cluster"],
            page["url"],
            page["title"],
            f"=LEN(E{idx})",
            page["description"],
            f"=LEN(G{idx})",
            page["h1"],
            1,
            "Pending",
            "noindex, follow" if page.get("noindex") else "index, follow",
            "Pending",
            "Pending",
            page.get("schema", ""),
            "N/A" if page["file"] in ("index.html", "404.html") else "Pending",
            "Yes" if faqs else "N/A",
            "Pending",
            "Excluded" if not indexable else "Pending",
            "Pending" if is_article else "N/A",
            "Pending",
            "Pending deploy",
            "Not started",
            "",
            page.get("next_review", ""),
            page.get("notes", ""),
        ]
        ws.append(row)
        ws.cell(row=idx, column=1).hyperlink = page["file"]
        ws.cell(row=idx, column=1).font = Font(color="1D4ED8", underline="single")
        ws.cell(row=idx, column=26).alignment = Alignment(wrap_text=True, vertical="top")
        for col in (1, 2, 3, 5, 7, 9, 15, 26):
            ws.cell(row=idx, column=col).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=idx, column=4).alignment = Alignment(wrap_text=True, vertical="top")

    for col, width in WIDTHS.items():
        ws.column_dimensions[col].width = width
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = f"A1:Z{len(ALL_PAGES) + 1}"
    ws.sheet_view.showGridLines = False

    dv = DataValidation(
        type="list",
        formula1='"Not started,In progress,Done,Blocked"',
        allow_blank=False,
        showDropDown=False,
    )
    dv.error = "Choose a valid status."
    dv.errorTitle = "Invalid status"
    dv.prompt = "Select the current status for this page."
    dv.promptTitle = "Status"
    ws.add_data_validation(dv)
    dv.add(f"W2:W{len(ALL_PAGES) + 1}")

    for status, (fill, font) in STATUS_COLORS.items():
        ws.conditional_formatting.add(
            f"W2:W{len(ALL_PAGES) + 1}",
            CellIsRule(
                operator="equal",
                formula=[f'"{status}"'],
                fill=PatternFill("solid", fgColor=fill),
                font=Font(color=font, bold=True),
            ),
        )

    # Highlight missing checks in amber, completed checks in green.
    for col in ("K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U"):
        rng = f"{col}2:{col}{len(ALL_PAGES) + 1}"
        ws.conditional_formatting.add(
            rng, CellIsRule(operator="equal", formula=['"Pending"'], fill=PatternFill("solid", fgColor="FEF3C7"))
        )
        ws.conditional_formatting.add(
            rng, CellIsRule(operator="equal", formula=['"Yes"'], fill=PatternFill("solid", fgColor="DCFCE7"))
        )
        ws.conditional_formatting.add(
            rng, CellIsRule(operator="equal", formula=['"Pass"'], fill=PatternFill("solid", fgColor="DCFCE7"))
        )


def _setup_dashboard(ws):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 36
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 16
    ws.column_dimensions["E"].width = 16
    ws.column_dimensions["F"].width = 20
    ws.column_dimensions["G"].width = 24

    ws["B2"] = "BoardExamBD — SEO Implementation Tracker"
    ws["B2"].font = TITLE_FONT
    ws["B3"] = f"Domain: {SITE['domain']}   ·   Author: {SITE['author']}   ·   Last updated: 26 October 2026"
    ws["B3"].font = SUBTITLE_FONT

    ws["B5"] = "Progress"
    ws["B5"].font = Font(size=13, bold=True, color="1E1B4B")
    ws["B6"] = "Total indexable pages"
    ws["C6"] = '=COUNTA(Pages!A2:A100)-COUNTIF(Pages!B2:B100,"Utility")'
    ws["B7"] = "Done"
    ws["C7"] = '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!W2:W100,"Done")'
    ws["B8"] = "In progress"
    ws["C8"] = '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!W2:W100,"In progress")'
    ws["B9"] = "Not started"
    ws["C9"] = '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!W2:W100,"Not started")'
    ws["B10"] = "Blocked"
    ws["C10"] = '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!W2:W100,"Blocked")'
    ws["B11"] = "% complete"
    ws["C11"] = "=IFERROR(C7/C6,0)"
    ws["C11"].number_format = "0%"

    for cell in ("B6", "B7", "B8", "B9", "B10", "B11"):
        ws[cell].font = BOLD
    for cell in ("C6", "C7", "C8", "C9", "C10", "C11"):
        ws[cell].alignment = Alignment(horizontal="center")

    ws.conditional_formatting.add(
        "C11",
        DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="4F46E5"),
    )

    ws["B13"] = "Coverage by check"
    ws["B13"].font = Font(size=13, bold=True, color="1E1B4B")
    checks = [
        ("Title + description set", '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!E2:E100,"<>",Pages!G2:G100,"<>")'),
        ("Canonical set", '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!K2:K100,"Yes")'),
        ("Robots set", '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!L2:L100,"Yes")'),
        ("Open Graph set", '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!M2:M100,"Yes")'),
        ("Twitter Card set", '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!N2:N100,"Yes")'),
        ("JSON-LD set", '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!O2:O100,"Yes")'),
        ("Breadcrumb set", '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!P2:P100,"Yes")'),
        ("FAQ where relevant", '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!Q2:Q100,"Yes")'),
        ("Internal links checked", '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!R2:R100,"Yes")'),
        ("Sitemap included", '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!S2:S100,"Yes")'),
        ("Markdown alternate", '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!T2:T100,"Yes")'),
        ("Local QA passed", '=COUNTIFS(Pages!B2:B100,"<>Utility",Pages!U2:U100,"Pass")'),
    ]
    row = 14
    for label, formula in checks:
        ws[f"B{row}"] = label
        ws[f"C{row}"] = formula
        ws[f"C{row}"].alignment = Alignment(horizontal="center")
        row += 1

    ws["B27"] = "Progress by cluster"
    ws["B27"].font = Font(size=13, bold=True, color="1E1B4B")
    ws["B28"] = "Cluster"
    ws["C28"] = "Total"
    ws["D28"] = "Done"
    ws["E28"] = "Remaining"
    for cell in ("B28", "C28", "D28", "E28"):
        ws[cell].fill = SECTION_FILL
        ws[cell].font = BOLD
        ws[cell].alignment = Alignment(horizontal="center")
    clusters = ["Home", "SSC", "HSC", "Admission", "Blog"]
    for i, cluster in enumerate(clusters, start=29):
        ws[f"B{i}"] = cluster
        ws[f"C{i}"] = f'=COUNTIF(Pages!C2:C100,"{cluster}")'
        ws[f"D{i}"] = f'=COUNTIFS(Pages!C2:C100,"{cluster}",Pages!W2:W100,"Done")'
        ws[f"E{i}"] = f"=C{i}-D{i}"
        for col in "BCDE":
            ws[f"{col}{i}"].alignment = Alignment(horizontal="center")

    ws["B36"] = "Reminder"
    ws["B36"].font = Font(size=13, bold=True, color="1E1B4B")
    ws["B37"] = (
        "Update the status column on the Pages sheet after each page passes local QA. "
        "Live QA stays \"Pending deploy\" until boardexambd.com is live. "
        "The 404.html utility page is tracked on Pages but excluded from progress totals and the sitemap."
    )
    ws["B37"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("B37:G39")
    ws["B37"].fill = PatternFill("solid", fgColor="F8FAFC")


def _setup_issues(ws):
    headers = ["ID", "Page", "Issue", "Severity", "Status", "Fix / next action", "Date logged"]
    ws.append(headers)
    _style_header(ws)
    width_map = {"A": 8, "B": 30, "C": 58, "D": 12, "E": 14, "F": 58, "G": 14}
    for col, width in width_map.items():
        ws.column_dimensions[col].width = width
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:G100"

    issues = [
        ("1", "Site-wide", "Canonical domain boardexambd.com does not resolve yet.", "High", "Open",
         "Point DNS/hosting at the production domain before launch; canonicals and sitemap already use it.", "2026-10-26"),
        ("2", "Site-wide", "No GA4 property, Search Console, Bing or Pinterest verification IDs supplied.", "Medium", "Open",
         "Add real IDs to the Config sheet and the head comment block before launch.", "2026-10-26"),
        ("3", "Site-wide", "Per-page OG images not designed yet; one supplied banner is used for all pages.", "Low", "Open",
         "Replace the shared og-default.jpg with per-page images when available.", "2026-10-26"),
        ("4", "Site-wide", "Live validation cannot run until the site is deployed.", "Medium", "Open",
         "Run Rich Results Test, Schema Markup Validator, Lighthouse and social previews after deploy.", "2026-10-26"),
        ("5", "hsc-2026-result.html", "HSC result was published on 31 October 2026 (revised from 29 Oct); page updated with pass rate, GPA-5 and SMS number.", "High", "Done",
         "Re-check the page after the 1-7 Nov 2026 re-scrutiny window closes.", "2026-10-31"),
        ("6", "ssc-form-fillup-2027.html", "SSC 2027 form fill-up window is 16–23 November 2026.", "High", "Open",
         "Update the status and fee details after the window opens and closes.", "2026-10-26"),
        ("7", "Category hubs", "Old sample-data routine and requirements tables were placeholders.", "High", "Done",
         "Replaced with verified summaries, timelines and admission tracker rows from the published guides.", "2026-10-26"),
        ("8", "Site-wide", "Empty accidental folders with mangled names exist in the root.", "Low", "Done",
         "Confirmed empty and removed the three folders.", "2026-10-26"),
    ]
    for issue in issues:
        ws.append(issue)
        for col in range(1, len(headers) + 1):
            ws.cell(row=ws.max_row, column=col).alignment = Alignment(wrap_text=True, vertical="top")


def _setup_config(ws):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 80
    ws.column_dimensions["C"].width = 26
    ws["A1"] = "Site configuration"
    ws["A1"].font = TITLE_FONT
    ws.append([])
    ws.append(["Property", "Value", "Source / note"])
    _style_header(ws, row=3)
    config = [
        ("Site name", SITE["name"], "Brand"),
        ("Canonical domain", SITE["domain"], "Confirmed by site owner"),
        ("Author", SITE["author"], "Organization schema author"),
        ("Default OG image", SITE["og_image"], "Generated from supplied banner"),
        ("OG source asset", "BoardExamBD Educational Notices Banner.png", "Original file kept in project root"),
        ("Default OG size", "1200 × 630 px", "Resized from 1730 × 909"),
        ("Language", "en", "English-only site"),
        ("Theme color", SITE["theme_color"], "Indigo brand"),
        ("Google Analytics 4", "Not set", "Add measurement ID before launch"),
        ("Google Search Console", "Not set", "Add verification meta before launch"),
        ("Bing Webmaster", "Not set", "Add verification meta before launch"),
        ("Pinterest", "Not set", "Add verification meta before launch"),
        ("Tailwind", "Compiled static CSS", "assets/css/tailwind.css"),
        ("Markdown alternates", "md/ folder", "One .md file per article"),
        ("AI index", "llms.txt", "Site-level AI crawler summary"),
        ("Sitemap", "sitemap.xml", "21 indexable URLs"),
        ("Robots", "robots.txt", "Allows search and AI crawlers"),
        ("Last updated", "2026-10-31", "HSC result published 31 October 2026; site-wide date refresh"),
    ]
    for row in config:
        ws.append(row)
        ws.cell(row=ws.max_row, column=1).font = BOLD
        ws.cell(row=ws.max_row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=ws.max_row, column=3).alignment = Alignment(wrap_text=True, vertical="top")


def build_tracker(path: Path = TRACKER):
    wb = Workbook()
    dashboard = wb.active
    dashboard.title = "Dashboard"
    pages = wb.create_sheet("Pages")
    issues = wb.create_sheet("Issues")
    config = wb.create_sheet("Config")

    _setup_dashboard(dashboard)
    _setup_pages(pages)
    _setup_issues(issues)
    _setup_config(config)

    dashboard.sheet_properties.tabColor = "4F46E5"
    pages.sheet_properties.tabColor = "0EA5E9"
    issues.sheet_properties.tabColor = "F59E0B"
    config.sheet_properties.tabColor = "10B981"
    wb.calculation.fullCalcOnLoad = True
    wb.save(path)
    print(f"Created {path}")
    return path


def _find_row(ws, page_file: str) -> int | None:
    for row in range(2, ws.max_row + 1):
        if ws.cell(row=row, column=1).value == page_file:
            return row
    return None


def update_page(page_file: str, **values):
    """Update arbitrary columns for a page.

    keys: canonical, robots, og, twitter, jsonld, breadcrumb, faq,
          internal_links, sitemap, markdown, local_qa, live_qa, status,
          done_date, notes, h1_count
    """
    wb = load_workbook(TRACKER)
    ws = wb["Pages"]
    row = _find_row(ws, page_file)
    if row is None:
        raise KeyError(f"{page_file} not found in tracker")
    mapping = {
        "canonical": 11, "robots": 12, "og": 13, "twitter": 14,
        "jsonld": 15, "breadcrumb": 16, "faq": 17, "internal_links": 18,
        "sitemap": 19, "markdown": 20, "local_qa": 21, "live_qa": 22,
        "status": 23, "done_date": 24, "next_review": 25, "notes": 26,
        "h1_count": 10,
    }
    for key, value in values.items():
        col = mapping.get(key)
        if col is None:
            raise KeyError(f"Unknown tracker key: {key}")
        ws.cell(row=row, column=col).value = value
        if key == "status" and value in STATUS_COLORS:
            fill, font = STATUS_COLORS[value]
            ws.cell(row=row, column=col).fill = PatternFill("solid", fgColor=fill)
            ws.cell(row=row, column=col).font = Font(color=font, bold=True)
        if key == "done_date" and value:
            ws.cell(row=row, column=col).number_format = "yyyy-mm-dd"
    wb.save(TRACKER)


def mark_page_done(page_file: str, *, faq: bool = False, markdown: bool = False):
    update_page(
        page_file,
        canonical="Yes",
        robots="Yes",
        og="Yes",
        twitter="Yes",
        jsonld="Yes",
        breadcrumb="N/A" if page_file in ("index.html", "404.html") else "Yes",
        faq="Yes" if faq else "N/A",
        internal_links="Yes",
        sitemap="Excluded" if page_file == "404.html" else "Yes",
        markdown="Yes" if markdown else "N/A",
        local_qa="Pass",
        status="Done",
        done_date=date.today().isoformat(),
    )


if __name__ == "__main__":
    build_tracker()
