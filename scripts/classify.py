import json
from collections import Counter

CATEGORIES = {
    "家族・健康": [
        "家族", "子ども", "子供", "親", "母", "父", "病院", "健康", "体調", "病気",
        "介護", "入院", "命", "亡くな", "遺族", "心身", "ストレス", "不安", "眠れ",
        "PTSD", "心のケア"
    ],
    "くらしむき": [
        "仕事", "収入", "生活", "お金", "経済", "商売", "店", "営業", "給料",
        "ローン", "借金", "雇用", "失業", "就職", "賠償", "補助金"
    ],
    "人と人のつながり": [
        "近所", "地域", "コミュニティ", "ボランティア", "仲間", "絆", "支え合",
        "つながり", "助け合", "交流", "集まり", "孤立", "孤独", "寂しい"
    ],
    "行政と支援情報": [
        "行政", "市役所", "支援", "制度", "申請", "手続き", "補助", "自治体",
        "国", "県", "復興", "計画", "工事", "区画整理", "政策"
    ],
    "すまい・そなえ": [
        "家", "住宅", "仮設", "復興住宅", "引越", "建て替え", "修理", "避難",
        "防災", "備え", "耐震", "津波", "避難所", "高台", "移転"
    ],
}

# Priority order (lower index = higher priority for tie-breaking)
PRIORITY = list(CATEGORIES.keys())


def classify(article):
    text = " ".join([
        article.get("content_text", ""),
        article.get("title", ""),
        article.get("description", ""),
    ])

    scores = {}
    for cat, keywords in CATEGORIES.items():
        score = sum(1 for kw in keywords if kw in text)
        scores[cat] = score

    max_score = max(scores.values())
    if max_score == 0:
        return "その他"

    # Among categories with max score, pick by priority
    for cat in PRIORITY:
        if scores[cat] == max_score:
            return cat

    return "その他"


def main():
    with open("data/articles.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"Total articles: {len(articles)}")

    category_counts = Counter()
    for article in articles:
        cat = classify(article)
        article["category"] = cat
        category_counts[cat] += 1

    print("\nCategory distribution:")
    for cat in PRIORITY + ["その他"]:
        count = category_counts.get(cat, 0)
        print(f"  {cat}: {count}")

    with open("data/articles_classified.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"\nSaved to data/articles_classified.json")


if __name__ == "__main__":
    main()
