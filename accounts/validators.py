"""フォームとシリアライザで共通の入力ルール。

フロントの検証も同じルールにそろえているので、変えるときはフロントも直す。
DB を見るもの（メールの重複）はここに置かない。
"""

import unicodedata

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from email_validator import EmailNotValidError
from email_validator import validate_email as validate_email_format

# 使える文字は AbstractUser の UnicodeUsernameValidator が確かめる
validate_username = MinLengthValidator(
    3,
    message="ユーザー名は%(limit_value)d文字以上で入力してください。",
)

# \d や str.isdigit() は全角数字なども通すので、半角の 0〜9 だけを [0-9] で確かめる
validate_tel = RegexValidator(
    r"^[0-9]+\Z",
    message="電話番号は数字のみで入力してください。",
    code="tel_not_digits",
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


def normalize_tel(value):
    return unicodedata.normalize("NFKC", value)
