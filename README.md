# user-registration

ユーザー登録機能を、Django のフォーム（MPA）、React（SPA）、REST API の 3 つの形で提供するプロジェクト。

## 画面

| URL | 実装 | 説明 |
| --- | --- | --- |
| `/app/signup/` | SPA(React) | 通常のアプリの入り口。`/`のリダイレクト先 |
| `/signup/` |MPA(Django)  | セキュリティ要件などにより、JavaScriptが使えない環境向け |

## 技術スタック

| レイヤー | 技術 |
| --- | --- |
| バックエンド | Django 5.2、Django REST Framework、drf-spectacular |
| フロントエンド | Vite、React、React Router、React Hook Form、Zod |
| 連携 | django-vite、OpenAPI のスキーマから生成した型 |
| DB | PostgreSQL 18 |
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
  │                      PostgreSQL
  │
  └ ─ ─ ─ ─ ─ ─ ─▶ Vite の開発サーバー（localhost:5173）
     開発中だけ       開発中の JS と HMR
```

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

# 2. 環境変数の用意
cp .env.example .env

# 3. ローカルDBを起動
docker compose up -d --wait

# 4. migrationの実行
uv run python manage.py migrate

# 5. 開発サーバーを起動
uv run python manage.py runserver
pnpm run dev

# http://127.0.0.1:8000/ でアクセスできるようになる
```

- `DJANGO_DEBUG=false` で動かすときは、先に `pnpm run build` でフロントをビルドする必要がある。

## ドキュメント

- 設計判断の記録は[docs/adr](docs/adr/README.md)に記載

### API ドキュメント
開発サーバー起動後、以下のURLでAPIドキュメントを確認できる。
- http://127.0.0.1:8000/api/docs/

## 開発

### リント・フォーマット
```bash
# バックエンド
uv run ruff check .
uv run ruff format .

# フロント
pnpm run lint         # oxLint
pnpm run format       # Prettier(修正)
pnpm run format:check # Prettier(チェックのみ)
pnpm run knip         # 使っていないファイル・export・依存の検出:
pnpm run typecheck    # 型チェック
```

#### コミット前のチェック

下記を実行後はlefthook が、ステージしたファイルにリンターと整形のチェックを流し、問題があればコミットが止まる。

```bash
pnpm exec lefthook install
```

### テスト

```bash
# バックエンド
uv run pytest
uv run pytest --cov #カバレッジ付

#　フロントエンド
pnpm run test
pnpm run test:coverage #カバレッジ付
```

### API の型定義
本プロジェクトでは、フロントエンド（React）で使うAPIの型定義をPythonのコードから自動生成する。APIのインタフェースが変わる場合は型定義を作り直すこと。

```bash
uv run python manage.py spectacular --file frontend/src/api/schema.yaml         # Python のコードからスキーマを生成
pnpm run gen:types  # スキーマから型定義を生成
```
