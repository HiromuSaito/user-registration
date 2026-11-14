"""AUTH_PASSWORD_VALIDATORS に登録するパスワードのルール。

Django に同じルールがないものだけを置く。8 文字以上は Django の MinimumLengthValidator を使う。
"""

import re

from django.core.exceptions import ValidationError


class _RequiredCharacterValidator:
    # 全角の文字は数えない。フロントで同じ判定（/[A-Z]/ など）ができるよう、半角の英数字だけを見る
    pattern = ""
    message = ""
    code = ""

    def validate(self, password, user=None):
        if not re.search(self.pattern, password):
            raise ValidationError(self.message, code=self.code)

    def get_help_text(self):
        return self.message


class UppercaseValidator(_RequiredCharacterValidator):
    pattern = r"[A-Z]"
    message = "パスワードには大文字を1文字以上含めてください。"
    code = "password_no_upper"


class LowercaseValidator(_RequiredCharacterValidator):
    pattern = r"[a-z]"
    message = "パスワードには小文字を1文字以上含めてください。"
    code = "password_no_lower"


class DigitValidator(_RequiredCharacterValidator):
    pattern = r"[0-9]"
    message = "パスワードには数字を1文字以上含めてください。"
    code = "password_no_digit"
