from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.models import User
from accounts.validators import (
    normalize_email,
    normalize_tel,
    validate_tel,
    validate_username,
)


class UserCreateSerializer(serializers.ModelSerializer):
    # モデルの EmailField から作ると Django の EmailValidator が validate_email() より先に動き、
    # email-validator のエラー（email_invalid）にたどり着かないため、検証のない CharField にする
    email = serializers.CharField(max_length=254)
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "tel", "pref"]

    def validate_username(self, value):
        validate_username(value)
        return value

    def validate_email(self, value):
        email = normalize_email(value)
        if User.objects.email_is_registered(email):
            raise serializers.ValidationError(
                "このメールアドレスは既に登録されています。",
                code="email_taken",
            )
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
