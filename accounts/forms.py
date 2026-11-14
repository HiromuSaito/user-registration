from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .error_messages import EMAIL_TAKEN
from .models import User
from .validators import (
    normalize_email,
    normalize_tel,
    validate_tel,
    validate_username,
)


# UserCreationForm はパスワードと確認用の 2 つの欄を前提にしている。確認用の欄を外すと、
# 確認用の欄の値で行うパスワードの検証が飛ばされるため使わず、ModelForm で validate_password() を呼ぶ
class SignupForm(forms.ModelForm):
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        validators=[validate_password],
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
            raise ValidationError(EMAIL_TAKEN, code="email_taken")
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
