from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.db.models.functions import Lower

from locations.models import Pref


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
    email = models.EmailField("メールアドレス", max_length=254)
    # 要件で null=True が指定されているため DJ001 を止める。空は None に統一する
    tel = models.CharField("電話番号", max_length=20, null=True, blank=True)  # noqa: DJ001
    pref = models.ForeignKey(Pref, on_delete=models.PROTECT, verbose_name="都道府県")

    objects = UserManager()

    REQUIRED_FIELDS = ["email", "pref"]

    class Meta(AbstractUser.Meta):
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                name="unique_user_email_ci",
                violation_error_message="このメールアドレスは既に登録されています。",
            ),
        ]

    def __str__(self):
        return self.username
