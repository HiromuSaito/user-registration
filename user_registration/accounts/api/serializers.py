from django import forms
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from user_registration.accounts.error_messages import EMAIL_TAKEN, required_message
from user_registration.accounts.models import User
from user_registration.accounts.validators import (
    USERNAME_TOO_SHORT,
    normalize_email,
    normalize_tel,
    validate_tel,
)

INVALID_CHOICE = forms.ModelChoiceField.default_error_messages["invalid_choice"]


class UserCreateSerializer(serializers.ModelSerializer):
    # モデルの EmailField から作ると Django の EmailValidator が validate_email() より先に動き、
    # email-validator のエラー（email_invalid）にたどり着かないため、検証のない CharField にする
    email = serializers.CharField(label="メールアドレス", max_length=254)
    password = serializers.CharField(
        label="パスワード",
        write_only=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "tel", "pref"]
        extra_kwargs = {
            # DRF はモデルの MinLengthValidator を自身の min_length に置き換えて既定の文を出すため、モデルと同じ文にする
            "username": {"error_messages": {"min_length": USERNAME_TOO_SHORT}},
            "pref": {
                "error_messages": {
                    "does_not_exist": INVALID_CHOICE,
                    "incorrect_type": INVALID_CHOICE,
                }
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            message = required_message(field.label)
            field.error_messages.update(required=message, blank=message, null=message)

    def validate_email(self, value):
        email = normalize_email(value)
        if User.objects.email_is_registered(email):
            raise serializers.ValidationError(EMAIL_TAKEN, code="email_taken")
        return email

    def validate_tel(self, value):
        # モデルフォームと違い、DRF は空の入力を None にしないため、ここで None にそろえる
        if not value:
            return None
        tel = normalize_tel(value)
        validate_tel(tel)
        return tel

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
