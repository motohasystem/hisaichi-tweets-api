"""
RSSフィードから新着記事を取得し、articles.jsonに追加する。
既存URLと重複する記事はスキップする。
"""

import json
import os
import re
import xml.etree.ElementTree as ET
import urllib.request

RSS_URL = "http://hisaichi.seesaa.net/index.rdf"

NS = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rss": "http://purl.org/rss/1.0/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "content": "http://purl.org/rss/1.0/modules/content/",
}


def fetch_rss():
    req = urllib.request.Request(RSS_URL, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    })
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def clean_html(raw):
    """content:encodedからCDATAの中身を取り出し、整形する"""
    if not raw:
        return "", ""
    # CDATA内の余分な部分を除去
    html = raw.strip()
    # <a name="more"></a> 以降を除去
    html = re.split(r'<a\s+name="more"', html)[0].strip()
    # テキスト版を生成
    text = re.sub(r"<br\s*/?>", "\n", html)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip()
    return html, text


def parse_rss(xml_bytes):
    root = ET.fromstring(xml_bytes)
    articles = []
    for item in root.findall("rss:item", NS):
        url = item.find("rss:link", NS)
        title = item.find("rss:title", NS)
        description = item.find("rss:description", NS)
        creator = item.find("dc:creator", NS)
        category = item.find("dc:subject", NS)
        date = item.find("dc:date", NS)
        content_encoded = item.find("content:encoded", NS)

        content_html, content_text = clean_html(
            content_encoded.text if content_encoded is not None else ""
        )

        articles.append({
            "url": url.text if url is not None else "",
            "title": title.text if title is not None else "",
            "description": description.text if description is not None else "",
            "creator": creator.text if creator is not None else "",
            "category": category.text if category is not None else "日記",
            "date": date.text if date is not None else "",
            "content_html": content_html,
            "content_text": content_text,
        })
    return articles


def main():
    # 既存データを読み込み
    with open("data/articles.json", "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_urls = {a["url"] for a in existing}
    print(f"Existing articles: {len(existing)}")

    # RSS取得・パース
    xml_bytes = fetch_rss()
    new_articles = parse_rss(xml_bytes)
    print(f"RSS items: {len(new_articles)}")

    # 重複除外して追加
    added = []
    for article in new_articles:
        if article["url"] not in existing_urls:
            added.append(article)

    # GitHub Actions output に結果を書き出す
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"added={len(added)}\n")
            f.write(f"total={len(existing) + len(added)}\n")
            titles = ", ".join(a["title"] for a in added[:5])
            f.write(f"titles={titles}\n")

    if not added:
        print("No new articles found.")
        return

    # 新しい記事を先頭に追加（日付降順）
    added.sort(key=lambda a: a["date"], reverse=True)
    existing = added + existing

    with open("data/articles.json", "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"Added {len(added)} new articles:")
    for a in added:
        print(f"  - {a['title']} ({a['date']})")
    print(f"Total: {len(existing)}")


if __name__ == "__main__":
    main()
