# user-registration

ユーザー登録機能を、Django のフォーム（MPA）、React（SPA）、REST API の 3 つの形で提供するプロジェクトです。

## 3 つの入口

| 入口 | URL | 中身 |
| --- | --- | --- |
| SPA（普段の入口） | `/app/signup/` | 入力しながら検証する。`/` からここに移る |
| MPA | `/signup/` | JavaScript が使えない人の入口 |
| API | `POST /api/users/`、`GET /api/prefs/` | 登録と、都道府県の一覧 |

どの入口でも、管理画面（`/admin/`）でも、同じ検証のルールで登録します。

## 技術スタック

| レイヤー | 技術 |
| --- | --- |
| バックエンド | Django 5.2 LTS、Django REST Framework、drf-spectacular |
| フロントエンド | Vite、React、React Router、React Hook Form、Zod |
| 連携 | django-vite、OpenAPI のスキーマから生成した型 |
| DB | PostgreSQL 18（ローカルは Docker Compose） |
| テスト | pytest、pytest-django / Vitest、Testing Library、MSW |
| リンター・フォーマッター | Ruff / Oxlint、Prettier、knip |
| パッケージ管理 | uv / pnpm |
| CI・依存の更新 | GitHub Actions、Dependabot、lefthook |

## アーキテクチャ

```
ブラウザ
  │
  ├──────────────▶ Django（127.0.0.1:8000）
  │                  ├── /signup/      MPA（テンプレートとフォーム）
  │                  ├── /app/...      SPA の HTML
  │                  ├── /api/...      API（DRF）
  │                  └── /static/...   CSS とビルドした JS
  │                          │
  │                          ▼
  │                  PostgreSQL（Docker Compose）
  │
  └ ─ ─ ─ ─ ─ ─ ─▶ Vite の開発サーバー（localhost:5173）
     開発中だけ       開発中の JS と HMR
```

`/app/` の配下は、どの URL でも同じ HTML を返し、表示する画面は React Router が決めます。

## プロジェクト構成

```
user-registration/
├── config/                 # Django の設定と URL
├── user_registration/
│   ├── accounts/           # ユーザー（モデル・フォーム・MPA の画面・API）
│   ├── locations/          # 都道府県（モデル・API）
│   ├── templates/          # 共通のテンプレート
│   └── static/css/         # MPA と SPA で共通の CSS
├── frontend/src/
│   ├── app/                # URL と画面の割り当て
│   ├── features/signup/    # 登録の画面・フォーム・API の呼び出し
│   ├── components/         # 全体で使う部品
│   ├── lib/                # API のクライアント
│   └── api/                # OpenAPI のスキーマと、生成した型
├── tests/                  # プロジェクト全体のテスト
├── docs/adr/               # 設計判断の記録
├── .github/workflows/      # CI
└── compose.yaml            # ローカルの PostgreSQL
```

## 環境構築

### 前提条件

- Python 3.10〜3.14
- [uv](https://docs.astral.sh/uv/)
- Node.js 26（`.nvmrc`）
- [pnpm](https://pnpm.io/) 12（`package.json` の `packageManager`）
- [Docker](https://docs.docker.com/) と Docker Compose

### セットアップ手順

```bash
# 1. 依存をインストールする
uv sync
pnpm install

# 2. コミット前のチェックを流す Git のフックを登録する
pnpm exec lefthook install

# 3. 設定の値を用意する
cp .env.example .env

# 4. PostgreSQL を起動して、テーブルと都道府県のデータを作る
docker compose up -d --wait
uv run python manage.py migrate
```

### 起動

開発中（`.env` の `DJANGO_DEBUG=true`）は、Django と Vite の開発サーバーを両方起動します。

```bash
uv run python manage.py runserver
pnpm run dev
```

http://127.0.0.1:8000/ で開きます。

- `DJANGO_DEBUG=false` で動かすときは、先に `pnpm run build` でフロントをビルドします。
- PostgreSQL は `docker compose down` で止めます。データも消して作り直すときは `docker compose down -v` を使います。

## 開発

### バックエンド

- リンター: `uv run ruff check .`
- フォーマット: `uv run ruff format .`
- テスト: `uv run pytest`

### フロントエンド

- リンター: `pnpm run lint`
- 使っていないファイル・export・依存の検出: `pnpm run knip`
- フォーマット: `pnpm run format`
- テスト: `pnpm run test`
- 型チェックとビルド: `pnpm run build`

### コミット前のチェック

lefthook が、ステージしたファイルにリンターと整形のチェックを流し、問題があればコミットを止めます。

### カバレッジ

CI では、PR ごとにジョブの要約（Summary）に表を出します。基準の数字は設けません。

- バックエンド: `uv run pytest --cov`
- フロントエンド: `pnpm run test:coverage`

### API を変えたとき

API のスキーマと、フロントで使う型を作り直します（作り直さないと CI が失敗します）。

```bash
uv run python manage.py spectacular --file frontend/src/api/schema.yaml
pnpm run gen:types
```

## ドキュメント

- 設計判断の記録: [docs/adr](docs/adr/README.md)
- API 仕様書: http://127.0.0.1:8000/api/docs/
