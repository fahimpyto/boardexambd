"""Load the existing article bodies and convert them into the new article format."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify

from seo_config import ARTICLE_BY_SLUG, SITE

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = SITE["domain"]

BODY_START = "<!-- svc:body:start -->"
BODY_END = "<!-- svc:body:end -->"
KF_START = "<!-- svc:key-facts:start -->"
KF_END = "<!-- svc:key-facts:end -->"

CACHE: dict[str, dict] = {}


def _between(text: str, start: str, end: str) -> str:
    pattern = re.escape(start) + r"(.*?)" + re.escape(end)
    match = re.search(pattern, text, re.S)
    return match.group(1).strip() if match else ""


def _is_cta(section) -> bool:
    if section.find(["h2", "h3", "h4", "p", "ul", "ol", "div", "table", "figure"]):
        return False
    return len(section.find_all("a")) >= 2


def parse_key_facts(section) -> list[dict]:
    cards: list[dict] = []
    if section is None:
        return cards
    grid = section.select_one("div.grid")
    if grid:
        for card in grid.find_all("div", recursive=False):
            paragraphs = card.find_all("p", recursive=False)
            if len(paragraphs) >= 2:
                cards.append(
                    {
                        "label": paragraphs[0].get_text(" ", strip=True),
                        "value": paragraphs[1].get_text(" ", strip=True),
                        "note": paragraphs[2].get_text(" ", strip=True) if len(paragraphs) > 2 else "",
                    }
                )
    if not cards:
        texts = [p.get_text(" ", strip=True) for p in section.find_all("p")]
        for index in range(0, len(texts) - 1, 3):
            chunk = texts[index : index + 3]
            if len(chunk) >= 2:
                cards.append(
                    {
                        "label": chunk[0],
                        "value": chunk[1],
                        "note": chunk[2] if len(chunk) > 2 else "",
                    }
                )
    if not cards:
        raise RuntimeError("Could not parse key facts cards")
    return cards


def slugify(value: str) -> str:
    value = value.replace("&", " and ")
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "section"


def decorate_body(body_html: str) -> tuple[str, list[tuple[int, str, str]]]:
    soup = BeautifulSoup(body_html, "html.parser")
    for link in soup.select(".anchor-link"):
        link.decompose()
    used = {"key-facts", "checklist", "faqs", "sources", "author", "related", "main-content"}
    entries: list[tuple[int, str, str]] = []
    for heading in soup.find_all(["h2", "h3"]):
        text = heading.get_text(" ", strip=True)
        if not text:
            continue
        base = heading.get("id") or slugify(text)
        anchor = base
        counter = 2
        while anchor in used:
            anchor = f"{base}-{counter}"
            counter += 1
        used.add(anchor)
        heading["id"] = anchor
        link = soup.new_tag("a", href=f"#{anchor}")
        link["class"] = "anchor-link"
        link["aria-label"] = f"Link to {text}"
        link.string = "#"
        heading.append(link)
        entries.append((int(heading.name[1]), text, anchor))
    rendered = "".join(str(node) for node in soup.contents).strip()
    return rendered, entries


def _extract_first_run(soup: BeautifulSoup) -> tuple[str, list[dict], str]:
    article_tag = soup.find("article")
    if article_tag is None:
        raise RuntimeError("Article element not found")
    h1 = soup.find("h1")
    if h1 is None:
        raise RuntimeError("H1 not found on page")

    deck = ""
    hero = h1.find_parent("section")
    if hero:
        for paragraph in hero.find_all("p"):
            classes = paragraph.get("class") or []
            if "text-indigo-100" in classes:
                deck = paragraph.get_text(" ", strip=True)
                break

    key_facts_section = article_tag.find("section", attrs={"aria-label": "Key facts"})
    if key_facts_section is None:
        key_facts_section = article_tag.find("section", id="key-facts")
    if key_facts_section is None:
        raise RuntimeError("Key facts section not found")
    cards = parse_key_facts(key_facts_section)

    body_parts = []
    for section in article_tag.find_all("section", recursive=False):
        if section is key_facts_section:
            continue
        if _is_cta(section):
            continue
        body_parts.append(str(section))
    if not body_parts:
        raise RuntimeError("Article body is empty")
    return deck, cards, "\n".join(body_parts)


def load_article_source(article: dict) -> dict:
    slug = article["slug"]
    if slug in CACHE:
        return CACHE[slug]

    path = ROOT / article["file"]
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")

    if BODY_START in text:
        deck_tag = soup.select_one("[data-deck]")
        deck = deck_tag.get_text(" ", strip=True) if deck_tag else article["description"]
        key_facts_html = _between(text, KF_START, KF_END)
        body_html = _between(text, BODY_START, BODY_END)
        if not body_html:
            raise RuntimeError(f"Could not read stored body for {article['file']}")
        key_facts_soup = BeautifulSoup(key_facts_html, "html.parser")
        cards = parse_key_facts(key_facts_soup.find("section"))
    else:
        deck, cards, body_html = _extract_first_run(soup)

    raw_soup = BeautifulSoup(body_html, "html.parser")
    for link in raw_soup.select(".anchor-link"):
        link.decompose()
    body_html = "".join(str(node) for node in raw_soup.contents).strip()

    rendered_body, body_toc = decorate_body(body_html)
    body_text = BeautifulSoup(body_html, "html.parser").get_text(" ", strip=True)
    words = len(re.findall(r"\w+", body_text, re.UNICODE))
    words += len(re.findall(r"\w+", deck, re.UNICODE))
    words += sum(len(re.findall(r"\w+", card["value"] + " " + card["note"], re.UNICODE)) for card in cards)
    words += sum(len(re.findall(r"\w+", item, re.UNICODE)) for item in article.get("checklist", []))
    words += sum(
        len(re.findall(r"\w+", faq["q"] + " " + faq["a"], re.UNICODE))
        for faq in article.get("faqs", [])
    )
    minutes = max(3, -(-words // 220))
    toc = [(2, "Key facts", "key-facts"), *body_toc]
    if article.get("checklist"):
        toc.append((2, "Quick checklist", "checklist"))
    if article.get("faqs"):
        toc.append((2, "Frequently asked questions", "faqs"))
    if article.get("sources"):
        toc.append((2, "Official sources", "sources"))

    source = {
        "deck": deck or article["description"],
        "cards": cards,
        "body_html": body_html,
        "body_rendered": rendered_body,
        "body_text": body_text,
        "toc": toc,
        "words": words,
        "minutes": minutes,
    }
    CACHE[slug] = source
    return source


def _absolutize(fragment) -> None:
    for tag in fragment.find_all(["a", "img", "source"]):
        for attr in ("href", "src"):
            value = tag.get(attr)
            if not value or value.startswith(("http://", "https://", "mailto:", "tel:", "#", "//", "data:")):
                continue
            if value.startswith("/"):
                tag[attr] = f"{DOMAIN}{value}"
            else:
                tag[attr] = f"{DOMAIN}/{value.lstrip('./')}"


def _clean_markdown(value: str) -> str:
    value = value.replace("\r\n", "\n")
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def article_markdown(article: dict) -> str:
    source = load_article_source(article)
    body = BeautifulSoup(source["body_html"], "html.parser")
    _absolutize(body)
    body_md = _clean_markdown(
        markdownify(
            str(body),
            heading_style="ATX",
            bullets="-",
            strip=["script", "style"],
        )
    )

    frontmatter = [
        "---",
        f"title: {json.dumps(article['h1'], ensure_ascii=False)}",
        f"description: {json.dumps(article['description'], ensure_ascii=False)}",
        f"url: {json.dumps(article['url'], ensure_ascii=False)}",
        f"date_published: {json.dumps(article['published'], ensure_ascii=False)}",
        f"date_modified: {json.dumps(article['modified'], ensure_ascii=False)}",
        f"author: {json.dumps(SITE['author'], ensure_ascii=False)}",
        f"publisher: {json.dumps(SITE['name'], ensure_ascii=False)}",
        f"category: {json.dumps(article['cluster'], ensure_ascii=False)}",
        "language: en",
        "robots: index, follow",
        f"canonical: {json.dumps(article['url'], ensure_ascii=False)}",
        "---",
        "",
    ]

    key_facts = []
    for card in source["cards"]:
        note = f" — {card['note']}" if card.get("note") else ""
        key_facts.append(f"- **{card['label']}:** {card['value']}{note}")

    checklist = "\n".join(f"- {item}" for item in article.get("checklist", []))
    faqs = "\n\n".join(
        f"### {faq['q']}\n\n{faq['a']}" for faq in article.get("faqs", [])
    )
    sources = "\n".join(f"- [{name}]({href})" for name, href in article.get("sources", []))

    body_sections = [
        f"# {article['h1']}",
        "",
        f"> {source['deck']}",
        "",
        f"**Updated:** {article['modified'][:10]} · **Published:** {article['published'][:10]} · **Author:** {SITE['author']} · **Read time:** {source['minutes']} min",
        "",
        f"[Read the formatted guide]({article['url']})",
        "",
        "## Key facts",
        "",
        "\n".join(key_facts),
        "",
        body_md,
    ]
    if checklist:
        body_sections += ["", "## Quick checklist", "", checklist]
    if faqs:
        body_sections += ["", "## Frequently asked questions", "", faqs]
    if sources:
        body_sections += ["", "## Official sources", "", sources]
    body_sections += [
        "",
        "## About the author",
        "",
        f"The {SITE['author']} prepares plain-language guides to SSC, HSC and university admission notices. Each guide links to the official board or university source used for its dates and instructions.",
        "",
        "BoardExamBD is an independent publication and is not affiliated with any education board or university. Always verify dates and instructions with the official source.",
        "",
    ]
    return "\n".join(frontmatter + body_sections).strip() + "\n"
