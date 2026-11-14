import pytest
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def error_codes(password):
    try:
        validate_password(password)
    except ValidationError as e:
        return [error.code for error in e.error_list]
    return []


@pytest.mark.parametrize(
    ("password", "expected"),
    [
        pytest.param("Abcdefg1", [], id="all_rules_met"),
        pytest.param("Abcdef1", ["password_too_short"], id="7_chars"),
        pytest.param("abcdefg1", ["password_no_upper"], id="no_upper"),
        pytest.param("ABCDEFG1", ["password_no_lower"], id="no_lower"),
        pytest.param("Abcdefgh", ["password_no_digit"], id="no_digit"),
        pytest.param(
            "ＡＢＣdefgh1", ["password_no_upper"], id="fullwidth_upper_not_counted"
        ),
        pytest.param(
            "",
            [
                "password_too_short",
                "password_no_upper",
                "password_no_lower",
                "password_no_digit",
            ],
            id="empty",
        ),
        # よくあるパスワードの判定は、フロントで再現できないため入れていない
        pytest.param("Password1", [], id="common_password_allowed"),
    ],
)
def test_validate_password(password, expected):
    assert error_codes(password) == expected
