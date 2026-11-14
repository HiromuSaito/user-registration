from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # 詳細の画面: 標準の項目に、追加した tel と pref を足す
    fieldsets = (
        *DjangoUserAdmin.fieldsets,
        ("連絡先と地域", {"fields": ("tel", "pref")}),
    )
    # 追加の画面: email と pref は必須なので、標準のユーザー名とパスワードに足す
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "pref",
                    "tel",
                    "usable_password",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = ("username", "email", "pref", "tel", "is_staff")
