# 被災地のつぶやき API

被災地の声（3,610件）をカテゴリ別に検索・ランダム取得できるREST APIです。Cloudflare Workersで動作します。

## データについて

本APIで利用しているデータは、[被災地のつぶやき](http://hisaichi.seesaa.net/)から、著作者の許諾を得て利用しているものです。

## ディレクトリ構成

```
03_build_api/
├── data/                      # データファイル
│   ├── articles.json            # 元データ
│   ├── articles_classified.json # 分類済みデータ
│   └── categories.txt           # カテゴリ定義
├── scripts/                   # 前処理スクリプト
│   └── classify.py
├── src/                       # Worker本体
│   └── index.js
├── public/                    # 静的アセット
│   └── index.html
├── package.json
├── wrangler.jsonc
└── API.md                     # APIリファレンス
```

## セットアップ

### 1. 記事の分類

元データ（`data/articles.json`）を6カテゴリに分類し、`data/articles_classified.json` を生成します。

```bash
python scripts/classify.py
```

### 2. ローカル起動

```bash
npm install
npm run dev
```

http://localhost:8787 でアクセスできます。

### 3. デプロイ

```bash
npm run deploy
```

## カテゴリ

| カテゴリ | 件数 |
|---------|------|
| すまい・そなえ | 1,200 |
| 家族・健康 | 608 |
| 人と人のつながり | 571 |
| その他 | 501 |
| くらしむき | 452 |
| 行政と支援情報 | 278 |

分類はキーワードマッチベースで行っています。詳細は `scripts/classify.py` を参照してください。

## API

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/api/articles` | 記事一覧（page, limit, search, year, month, category） |
| GET | `/api/articles/random` | ランダム1件（?category=カテゴリ名） |
| GET | `/api/articles/:id` | 記事詳細 |
| GET | `/api/categories` | カテゴリ一覧と件数 |
| GET | `/api/stats` | 統計情報 |

詳細は [API.md](API.md) を参照してください。
