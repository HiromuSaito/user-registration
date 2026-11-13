# user-registration

ユーザー登録機能を、Django のフォーム（MPA）、React（SPA）、REST API の 3 つの形で提供するプロジェクト。

## 動作環境

- Python 3.10〜3.14（開発には 3.14 を使用）
- [uv](https://docs.astral.sh/uv/)

## セットアップ

```bash
uv sync
cp .env.example .env
uv run python manage.py migrate
uv run python manage.py runserver
```

http://127.0.0.1:8000/ で起動します。

## 画面

| URL | 内容 |
| --- | --- |
| http://127.0.0.1:8000/signup/ | 登録画面（Django のフォーム） |
| http://127.0.0.1:8000/signup/complete/ | 登録の完了画面（登録した直後だけ表示される） |
| http://127.0.0.1:8000/admin/ | 管理画面（`uv run python manage.py createsuperuser` で作った管理者でログインする） |

## 開発

- リンター: `uv run ruff check .`
- フォーマット: `uv run ruff format .`
- テスト: `uv run pytest`
- CI と同じチェック: `uv run ruff check . && uv run ruff format --check . && uv run pytest`

## ドキュメント

- 設計判断の記録: [docs/adr](docs/adr/README.md)
