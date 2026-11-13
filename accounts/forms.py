from django import forms
from django.core.exceptions import ValidationError

from .models import User
from .validators import (
    normalize_email,
    normalize_tel,
    validate_password_rules,
    validate_tel,
    validate_username,
)


# UserCreationForm は登録時に Django 標準のパスワードの検証（AUTH_PASSWORD_VALIDATORS）を
# 呼ぶため使わない。登録ではフロントとそろえた要件のルール（validate_password_rules）だけを確かめる
class SignupForm(forms.ModelForm):
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        validators=[validate_password_rules],
    )

    class Meta:
        model = User
        fields = ["username", "email", "tel", "pref"]
        # フォームの EmailField は Django の EmailValidator を clean_email() より先に動かし、
        # email-validator のエラー（email_invalid）にたどり着かないため、検証のない CharField にする
        field_classes = {"email": forms.CharField}
        widgets = {"email": forms.EmailInput}

    def clean_username(self):
        username = self.cleaned_data["username"]
        validate_username(username)
        return username

    def clean_email(self):
        email = normalize_email(self.cleaned_data["email"])
        if User.objects.email_is_registered(email):
            raise ValidationError(
                "このメールアドレスは既に登録されています。",
                code="email_taken",
            )
        return email

    def clean_tel(self):
        tel = self.cleaned_data["tel"]
        if tel is None:
            return None
        tel = normalize_tel(tel)
        validate_tel(tel)
        return tel

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
