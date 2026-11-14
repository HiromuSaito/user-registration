from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.functions import Lower

from user_registration.locations.models import Pref

from .error_messages import EMAIL_TAKEN


class UserManager(DjangoUserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        # createsuperuser は REQUIRED_FIELDS の外部キーに主キーの値（都道府県コード）を渡すため、
        # pref ではなく pref_id として渡す
        if "pref" in extra_fields and not isinstance(extra_fields["pref"], Pref):
            extra_fields["pref_id"] = extra_fields.pop("pref")
        return super().create_superuser(username, email, password, **extra_fields)

    def email_is_registered(self, email):
        return self.filter(email__iexact=email).exists()


class User(AbstractUser):
    # Django の日本語の訳は「半角英数、@/./+/-/_ を使用できます」だが、UnicodeUsernameValidator は
    # 日本語などの文字も通すため、実際の動きに合わせてエラーメッセージと説明を書き直す。
    # バリデーターは AbstractUser がフィールドを作るときに組み込まれ、username_validator を
    # 上書きするだけでは変わらないため、フィールドごと定義し直す。メッセージと説明以外は AbstractUser と同じ
    username = models.CharField(
        "ユーザー名",
        max_length=150,
        unique=True,
        help_text="必須。150文字以下で、文字、数字、@/./+/-/_ だけを使えます。",
        validators=[
            UnicodeUsernameValidator(
                message="ユーザー名には、文字、数字、@/./+/-/_ だけを使えます。"
            )
        ],
        error_messages={"unique": "同じユーザー名が既に登録済みです。"},
    )
    email = models.EmailField("メールアドレス")
    # 要件で null=True が指定されているため DJ001 を止める。空は None に統一する
    tel = models.CharField("電話番号", max_length=20, null=True, blank=True)  # noqa: DJ001
    pref = models.ForeignKey(Pref, on_delete=models.PROTECT, verbose_name="都道府県")

    objects = UserManager()

    REQUIRED_FIELDS = ["email", "pref"]

    class Meta(AbstractUser.Meta):
        constraints = [
            # RFC ではローカル部（@ の前）の大文字・小文字を区別してよいが、実際に区別するメールサービスはほぼなく、
            # 区別すると同じ人が大文字・小文字を変えただけで何度も登録できるため、区別せずに一意にする。
            # 入力されたとおりの値を残すため、小文字にして保存するのではなく Lower() の一意制約にする
            models.UniqueConstraint(
                Lower("email"),
                name="unique_user_email_ci",
                violation_error_message=EMAIL_TAKEN,
            ),
        ]
