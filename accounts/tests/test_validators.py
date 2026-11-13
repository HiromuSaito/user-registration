import pytest
from django.core.exceptions import ValidationError

from accounts.validators import (
    normalize_email,
    normalize_tel,
    validate_password_rules,
    validate_tel,
    validate_username,
)


def error_codes(validator, value):
    try:
        validator(value)
    except ValidationError as e:
        return [error.code for error in e.error_list]
    return []


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("abc", [], id="3_chars"),
        pytest.param("ab", ["username_too_short"], id="2_chars"),
        pytest.param("山田太郎", [], id="japanese_4_chars"),
        pytest.param("山田", ["username_too_short"], id="japanese_2_chars"),
    ],
)
def test_validate_username(value, expected):
    assert error_codes(validate_username, value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("user@example.com", "user@example.com", id="valid"),
        pytest.param(
            "Taro@Example.COM", "Taro@example.com", id="lowercases_domain_only"
        ),
        pytest.param("user+tag@example.com", "user+tag@example.com", id="plus_sign"),
    ],
)
def test_normalize_email_ok(value, expected):
    assert normalize_email(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("", id="empty"),
        pytest.param("user", id="no_at_sign"),
        pytest.param("user@", id="no_domain"),
        pytest.param("@example.com", id="no_local_part"),
        pytest.param("us er@example.com", id="space"),
        pytest.param("a..b@example.com", id="consecutive_dots"),
        pytest.param('"john doe"@example.com', id="quoted"),
        pytest.param("user@[192.168.0.1]", id="ip_domain"),
        pytest.param("ユーザー@example.com", id="non_ascii_local_part"),
    ],
)
def test_normalize_email_invalid(value):
    assert error_codes(normalize_email, value) == ["email_invalid"]


@pytest.mark.parametrize(
    ("value", "expected"),
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
    ],
)
def test_validate_password_rules(value, expected):
    assert error_codes(validate_password_rules, value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("0901234", "0901234", id="halfwidth"),
        pytest.param("０９０１２３４", "0901234", id="fullwidth"),
        pytest.param("090－1234", "090-1234", id="fullwidth_hyphen"),
    ],
)
def test_normalize_tel(value, expected):
    assert normalize_tel(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("0901234", [], id="halfwidth_digits"),
        pytest.param("090-1234", ["tel_not_digits"], id="hyphen"),
        pytest.param("090 1234", ["tel_not_digits"], id="space"),
        pytest.param("0901234\n", ["tel_not_digits"], id="trailing_newline"),
        pytest.param("０９０", ["tel_not_digits"], id="fullwidth_before_normalize"),
        pytest.param("abc", ["tel_not_digits"], id="letters"),
    ],
)
def test_validate_tel(value, expected):
    assert error_codes(validate_tel, value) == expected
