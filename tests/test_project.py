from io import StringIO
from pathlib import Path

import pytest
from django.conf import settings
from django.core import checks
from django.core.management import call_command

# Python の CI ではフロントをビルドしないため、ビルドの出力（frontend/dist と manifest.json）が
# ないことによる警告だけを除く。本番でビルドを忘れたときには警告として出てほしいので、設定では止めない
MISSING_FRONTEND_BUILD = {"staticfiles.W004", "django_vite.W001"}


def test_system_check_passes():
    issues = [
        issue
        for issue in checks.run_checks()
        if issue.level >= checks.WARNING and issue.id not in MISSING_FRONTEND_BUILD
    ]

    assert issues == []


# makemigrations は適用済みのマイグレーションとの食い違いも DB に問い合わせてチェックするため、DB を使う
@pytest.mark.django_db
def test_no_pending_migrations():
    out = StringIO()
    try:
        call_command("makemigrations", "--check", stdout=out, stderr=StringIO())
    except SystemExit:
        pytest.fail(f"マイグレーションになっていない変更があります。\n{out.getvalue()}")


def test_api_schema_is_valid_without_warnings():
    call_command("spectacular", "--validate", "--fail-on-warn", stdout=StringIO())


def test_api_schema_file_is_up_to_date():
    schema_file = Path(settings.BASE_DIR) / "frontend" / "src" / "api" / "schema.yaml"
    out = StringIO()
    call_command("spectacular", stdout=out)

    assert out.getvalue() == schema_file.read_text(encoding="utf-8"), (
        "API のスキーマのファイルが古くなっています。次のコマンドで作り直してください。\n"
        "uv run python manage.py spectacular --file frontend/src/api/schema.yaml"
        " && pnpm run gen:types"
    )
