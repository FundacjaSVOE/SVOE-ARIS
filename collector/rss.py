"""
ARIS RSS Collector Module
Animal Rescue Intelligence System

Purpose:
- Load RSS sources with proper timeouts and user-agents
- Download and parse news entries
- Clean HTML content from text
- Return structured data
"""

from datetime import datetime
import re
import urllib.request
from bs4 import BeautifulSoup
import feedparser


def clean_html(raw_html: str) -> str:
    """Remove HTML tags and clean whitespace from string."""
    if not raw_html:
        return ""
    # Использование BeautifulSoup для корректной очистки HTML-тегов
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ")
    # Удаление лишних пробелов и переносов строк
    return re.sub(r"\s+", " ", text).strip()


def load_rss(url: str, source_name: str = "Unknown", country: str = "Unknown", timeout: int = 10) -> list[dict]:
    """Read RSS feed and return structured articles with robust error handling."""
    articles = []

    try:
        # Устанавливаем User-Agent, чтобы сайты не блокировали запрос как бота
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ARIS-Bot/1.0"}
        )

        with urllib.request.urlopen(req, timeout=timeout) as response:
            xml_data = response.read()

        feed = feedparser.parse(xml_data)

        for item in feed.entries:
            title = clean_html(item.get("title", ""))
            link = item.get("link", "")

            # Пропускаем пустые или невалидные записи
            if not title or not link:
                continue

            raw_description = item.get("summary", "") or item.get("description", "")
            cleaned_description = clean_html(raw_description)

            article = {
                "title": title,
                "link": link,
                "description": cleaned_description,
                "published": item.get("published", item.get("updated", "")),
                "source": source_name,
                "country": country,
                "collected_at": datetime.now().isoformat(),
            }

            articles.append(article)

    except Exception as error:
        print(f"[ERROR] RSS error ({source_name} - {url}): {error}")

    return articles


def collect_from_sources(sources: list[dict]) -> list[dict]:
    """Collect news from all RSS sources provided in the config."""
    all_articles = []

    for source in sources:
        source_name = source.get("name", "Unknown")
        source_url = source.get("url", "")
        country = source.get("country", "Unknown")

        if not source_url:
            print(f"[WARN] Skipping source '{source_name}': Missing URL")
            continue

        print(f"Checking RSS: {source_name} ({country})...")

        articles = load_rss(
            url=source_url,
            source_name=source_name,
            country=country
        )

        print(f" -> Found valid articles: {len(articles)}")
        all_articles.extend(articles)

    return all_articles


def print_articles(articles: list[dict]) -> None:
    """Display collected articles to stdout."""
    print()
    print("=" * 60)
    print(f"Total articles collected: {len(articles)}")
    print("=" * 60)

    for number, article in enumerate(articles, start=1):
        print(f"\n{number}. {article['title']}")
        print(f"   Source: {article['source']} [{article['country']}]")
        print(f"   Link:   {article['link']}")
        if article["description"]:
            # Обрезаем предпросмотр описания, чтобы не засорять консоль
            short_desc = article["description"][:120] + "..." if len(article["description"]) > 120 else article["description"]
            print(f"   Desc:   {short_desc}")


if __name__ == "__main__":
    # Тестовые рабочие источники новостей о животных / экологии
    test_sources = [
        {
            "name": "World Animal Protection",
            "country": "International",
            "url": "https://www.worldanimalprotection.org/rss.xml"
        }
    ]

    news = collect_from_sources(test_sources)
    print_articles(news)
