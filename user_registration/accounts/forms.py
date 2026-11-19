from django import forms
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .error_messages import EMAIL_TAKEN, required_message
from .models import User
from .validators import normalize_email, normalize_tel, validate_tel


# 全角の数字を半角に直してから確かめることと、email-validator での確かめと正規化は、モデルのフィールドの
# 検証ではできないため、登録画面と管理画面のフォームでこのクラスを共有して、同じルールにする
class UserInputCleanMixin:
    def clean_email(self):
        return normalize_email(self.cleaned_data["email"])

    def clean_tel(self):
        tel = self.cleaned_data["tel"]
        if tel is None:
            return None
        tel = normalize_tel(tel)
        validate_tel(tel)
        return tel


# UserCreationForm はパスワードと確認用の 2 つの欄を前提にしている。確認用の欄を外すと、
# 確認用の欄の値で行うパスワードの検証が飛ばされるため使わず、ModelForm で validate_password() を呼ぶ
class SignupForm(UserInputCleanMixin, forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages["required"] = required_message(field.label)

    def clean_email(self):
        email = super().clean_email()
        if User.objects.email_is_registered(email):
            raise ValidationError(EMAIL_TAKEN, code="email_taken")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# 管理画面では、Django が一意制約を自分自身を除いて確かめるので、メールの重複はここでは確かめない
class UserAdminCreationForm(UserInputCleanMixin, AdminUserCreationForm):
    class Meta(AdminUserCreationForm.Meta):
        model = User
        fields = ["username", "email", "pref", "tel"]
        field_classes = {
            **AdminUserCreationForm.Meta.field_classes,
            "email": forms.CharField,
        }


class UserAdminChangeForm(UserInputCleanMixin, UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        field_classes = {**UserChangeForm.Meta.field_classes, "email": forms.CharField}
