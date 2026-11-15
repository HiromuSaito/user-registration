from io import StringIO

import pytest
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


# makemigrations は適用済みのマイグレーションとの食い違いも DB に問い合わせて確かめるため、DB を使う
@pytest.mark.django_db
def test_no_pending_migrations():
    out = StringIO()
    try:
        call_command("makemigrations", "--check", stdout=out, stderr=StringIO())
    except SystemExit:
        pytest.fail(f"マイグレーションになっていない変更があります。\n{out.getvalue()}")


def test_api_schema_is_valid_without_warnings():
    call_command("spectacular", "--validate", "--fail-on-warn", stdout=StringIO())
