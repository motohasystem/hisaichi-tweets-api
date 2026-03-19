# 被災地のつぶやき API

被災地の声（3,610件）を提供するREST APIです。

Base URL: `https://<your-worker>.workers.dev`

全レスポンスは `Content-Type: application/json;charset=UTF-8`、CORS対応済み。

---

## エンドポイント一覧

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/api/articles` | 記事一覧 |
| GET | `/api/articles/random` | ランダム1件取得 |
| GET | `/api/articles/:id` | 記事詳細 |
| GET | `/api/categories` | カテゴリ一覧 |
| GET | `/api/stats` | 統計情報 |

---

## GET /api/articles

記事の一覧を取得します。一覧では `content_html` / `content_text` を除外し軽量化しています。

### クエリパラメータ

| パラメータ | 型 | デフォルト | 説明 |
|-----------|------|-----------|------|
| `page` | number | 1 | ページ番号 |
| `limit` | number | 20 | 1ページあたりの件数（1〜100） |
| `category` | string | - | カテゴリ名で絞り込み |
| `year` | number | - | 年で絞り込み |
| `month` | number | - | 月で絞り込み（1〜12） |
| `search` | string | - | タイトル・本文の全文検索 |

### レスポンス例

```json
{
  "data": [
    {
      "id": 0,
      "url": "http://hisaichi.seesaa.net/article/433652632.html",
      "title": "なんだか寂しいよね。",
      "description": "『震災前に住んでた町に行ってみると...',
      "creator": "ヒサツブ",
      "category": "家族・健康",
      "date": "2016-02-11T07:00:00+09:00"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 3610,
    "totalPages": 181
  }
}
```

### リクエスト例

```
GET /api/articles?category=くらしむき&page=2&limit=10
GET /api/articles?search=津波&year=2016
```

---

## GET /api/articles/random

ランダムに1件取得します。全フィールドを返却します。

### クエリパラメータ

| パラメータ | 型 | デフォルト | 説明 |
|-----------|------|-----------|------|
| `category` | string | - | カテゴリ名で絞り込み |

### レスポンス例

```json
{
  "id": 2947,
  "url": "http://hisaichi.seesaa.net/article/502760237.html",
  "title": "どこで家を再建するか",
  "description": "『津波に家を奪われ...',
  "creator": "ヒサツブ",
  "category": "すまい・そなえ",
  "date": "2020-03-15T07:00:00+09:00",
  "content_html": "...",
  "content_text": "..."
}
```

### リクエスト例

```
GET /api/articles/random
GET /api/articles/random?category=家族・健康
GET /api/articles/random?category=人と人のつながり
```

---

## GET /api/articles/:id

指定IDの記事詳細を取得します。全フィールドを返却します。

### パスパラメータ

| パラメータ | 型 | 説明 |
|-----------|------|------|
| `id` | number | 記事のインデックス番号（0〜3609） |

### レスポンス例

```json
{
  "id": 0,
  "url": "http://hisaichi.seesaa.net/article/433652632.html",
  "title": "なんだか寂しいよね。",
  "description": "『震災前に住んでた町に行ってみると...',
  "creator": "ヒサツブ",
  "category": "家族・健康",
  "date": "2016-02-11T07:00:00+09:00",
  "content_html": "...",
  "content_text": "..."
}
```

### エラー

| ステータス | 条件 |
|-----------|------|
| 400 | IDが数値でない |
| 404 | IDが範囲外 |

---

## GET /api/categories

カテゴリ一覧と各カテゴリの記事件数を取得します。

### レスポンス例

```json
{
  "data": [
    { "name": "家族・健康", "count": 608 },
    { "name": "人と人のつながり", "count": 571 },
    { "name": "くらしむき", "count": 452 },
    { "name": "その他", "count": 501 },
    { "name": "行政と支援情報", "count": 278 },
    { "name": "すまい・そなえ", "count": 1200 }
  ]
}
```

---

## GET /api/stats

統計情報を取得します。

### レスポンス例

```json
{
  "totalArticles": 3610,
  "categories": {
    "家族・健康": 608,
    "人と人のつながり": 571,
    "くらしむき": 452,
    "その他": 501,
    "行政と支援情報": 278,
    "すまい・そなえ": 1200
  },
  "years": [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
}
```

---

## カテゴリ一覧

| カテゴリ | 件数 | 説明 |
|---------|------|------|
| 家族・健康 | 608 | 家族関係、心身の健康、不安やストレス |
| くらしむき | 452 | 仕事、収入、生活再建 |
| 人と人のつながり | 571 | 地域コミュニティ、ボランティア、孤立 |
| 行政と支援情報 | 278 | 行政手続き、支援制度、復興計画 |
| すまい・そなえ | 1,200 | 住宅、避難、防災、移転 |
| その他 | 501 | 上記に該当しないもの |

---

## エラーレスポンス

```json
{
  "error": "エラーメッセージ"
}
```

| ステータス | 説明 |
|-----------|------|
| 400 | 不正なリクエスト |
| 404 | リソースが見つからない |
| 405 | 許可されていないメソッド |
