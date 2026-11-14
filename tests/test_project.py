from io import StringIO

import pytest
from django.core.management import call_command


def test_system_check_passes():
    call_command("check", fail_level="WARNING")


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
