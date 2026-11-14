from unittest import mock

import pytest
from django.db import IntegrityError
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User

USER_CREATE_URL = reverse("accounts_api:user_create")

VALID_DATA = {
    "username": "taro",
    "email": "Taro@Example.com",
    "password": "Abcdefg1",
    "tel": "０９０１２３４",
    "pref": 13,
}


@pytest.fixture
def api_client():
    return APIClient()


def post_json(client, data, **extra):
    return client.post(USER_CREATE_URL, data, format="json", **extra)


@pytest.mark.django_db
def test_create_returns_201_with_saved_values(api_client):
    response = post_json(api_client, VALID_DATA)

    assert response.status_code == 201
    assert response.json() == {
        "username": "taro",
        "email": "Taro@example.com",
        "tel": "0901234",
        "pref": 13,
    }
    user = User.objects.get(username="taro")
    assert user.check_password("Abcdefg1")


@pytest.mark.django_db
def test_invalid_input_returns_400_with_errors_per_field(api_client):
    response = post_json(
        api_client, {**VALID_DATA, "username": "ab", "tel": "090-1234"}
    )

    assert response.status_code == 400
    assert response.json() == {
        "username": ["ユーザー名は3文字以上で入力してください。"],
        "tel": ["電話番号は数字のみで入力してください。"],
    }
    assert not User.objects.exists()


@pytest.mark.django_db
def test_integrity_error_returns_400(api_client):
    # 検証のあと保存までの間に同じメールで登録された状況を、保存時の例外で再現する
    with mock.patch(
        "accounts.api.serializers.UserCreateSerializer.save", side_effect=IntegrityError
    ):
        response = post_json(api_client, VALID_DATA)

    assert response.status_code == 400
    assert response.json() == {
        "non_field_errors": [
            "登録できませんでした。入力内容を確かめて、もう一度お試しください。"
        ]
    }


@pytest.mark.django_db
def test_get_is_not_allowed(api_client):
    assert api_client.get(USER_CREATE_URL).status_code == 405


@pytest.mark.django_db
def test_csrf_token_is_required():
    csrf_client = APIClient(enforce_csrf_checks=True)

    response = post_json(csrf_client, VALID_DATA)

    assert response.status_code == 403
    assert not User.objects.exists()


@pytest.mark.django_db
def test_csrf_token_in_header_is_accepted():
    csrf_client = APIClient(enforce_csrf_checks=True)
    # 登録画面を開くと、CSRF のトークンが Cookie に入る
    csrf_client.get(reverse("accounts:signup"))
    token = csrf_client.cookies["csrftoken"].value

    response = post_json(csrf_client, VALID_DATA, HTTP_X_CSRFTOKEN=token)

    assert response.status_code == 201
