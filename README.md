# user-registration

ユーザー登録機能を、Django のフォーム（MPA）、React（SPA）、REST API の 3 つの形で提供するプロジェクト。

## 動作環境

- Python 3.10〜3.14（開発には 3.14 を使用）
- [uv](https://docs.astral.sh/uv/)
- Node.js 26（`.nvmrc`）
- [pnpm](https://pnpm.io/) 12（`package.json` の `packageManager`）

## セットアップ

```bash
uv sync
pnpm install
cp .env.example .env
uv run python manage.py migrate
```

## 起動

開発中（`.env` の `DJANGO_DEBUG=true`）は、Django と Vite の開発サーバーを両方起動します。

```bash
uv run python manage.py runserver
pnpm run dev
```

http://127.0.0.1:8000/ で起動します。

`DJANGO_DEBUG=false` で動かすときは、先に `pnpm run build` でフロントをビルドします。

## 開発

### バックエンド

- リンター: `uv run ruff check .`
- フォーマット: `uv run ruff format .`
- テスト: `uv run pytest`
- CI と同じチェック: `uv run ruff check . && uv run ruff format --check . && uv run pytest`

### フロントエンド

- リンター: `pnpm run lint`
- フォーマット: `pnpm run format`
- テスト: `pnpm run test`
- 型チェックとビルド: `pnpm run build`
- CI と同じチェック: `pnpm run lint && pnpm run format:check && pnpm run test && pnpm run build`

## ドキュメント

- 設計判断の記録: [docs/adr](docs/adr/README.md)
- API仕様書: http://127.0.0.1:8000/api/docs/ 
