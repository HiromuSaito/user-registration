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
uv run python manage.py runserver
```

http://127.0.0.1:8000/ で起動します。

## 開発

### バックエンド

- リンター: `uv run ruff check .`
- フォーマット: `uv run ruff format .`
- テスト: `uv run pytest`
- CI と同じチェック: `uv run ruff check . && uv run ruff format --check . && uv run pytest`

### フロントエンド

- リンター: `pnpm lint`
- フォーマット: `pnpm format`
- テスト: `pnpm test`
- 型チェックとビルド: `pnpm build`
- CI と同じチェック: `pnpm lint && pnpm format:check && pnpm test && pnpm build`

## ドキュメント

- 設計判断の記録: [docs/adr](docs/adr/README.md)
- API仕様書: http://127.0.0.1:8000/api/docs/ 
