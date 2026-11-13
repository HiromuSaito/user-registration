"""フォームとシリアライザで共通の入力ルール。DB を見るもの（メールの重複）はここに置かない。"""

import re
import unicodedata

from django.core.exceptions import ValidationError
from email_validator import EmailNotValidError
from email_validator import validate_email as validate_email_format

USERNAME_MIN_LENGTH = 3
PASSWORD_MIN_LENGTH = 8


def validate_username(value):
    # 使える文字は AbstractUser の UnicodeUsernameValidator が確かめる
    if len(value) < USERNAME_MIN_LENGTH:
        raise ValidationError(
            "ユーザー名は3文字以上で入力してください。",
            code="username_too_short",
        )


def normalize_email(value):
    try:
        # モデルの EmailField の EmailValidator は @ の前に英数字と一部の記号しか許さないため、
        # それに合わせて @ の前の英数字以外（国際化メールアドレス）を許さない
        result = validate_email_format(
            value, check_deliverability=False, allow_smtputf8=False
        )
    except EmailNotValidError as e:
        raise ValidationError(
            "メールアドレスの形式が正しくありません。",
            code="email_invalid",
        ) from e
    return result.normalized


def validate_password_rules(value):
    errors = []
    if len(value) < PASSWORD_MIN_LENGTH:
        errors.append(
            ValidationError(
                "パスワードは8文字以上で入力してください。",
                code="password_too_short",
            )
        )
    if not re.search(r"[A-Z]", value):
        errors.append(
            ValidationError(
                "パスワードには大文字を1文字以上含めてください。",
                code="password_no_upper",
            )
        )
    if not re.search(r"[a-z]", value):
        errors.append(
            ValidationError(
                "パスワードには小文字を1文字以上含めてください。",
                code="password_no_lower",
            )
        )
    if not re.search(r"[0-9]", value):
        errors.append(
            ValidationError(
                "パスワードには数字を1文字以上含めてください。",
                code="password_no_digit",
            )
        )
    if errors:
        raise ValidationError(errors)


def normalize_tel(value):
    return unicodedata.normalize("NFKC", value)


def validate_tel(value):
    # \d や str.isdigit() は全角数字なども通すので、半角の 0〜9 だけを [0-9] で確かめる
    if not re.fullmatch(r"[0-9]+", value):
        raise ValidationError(
            "電話番号は数字のみで入力してください。",
            code="tel_not_digits",
        )
