from unittest import mock

import pytest
from django.db import IntegrityError
from django.urls import reverse

from user_registration.accounts.models import User

SIGNUP_URL = reverse("accounts:signup")
COMPLETE_URL = reverse("accounts:signup_complete")

VALID_DATA = {
    "username": "taro",
    "email": "taro@example.com",
    "password": "Abcdefg1",
    "tel": "0901234",
    "pref": "13",
}


@pytest.mark.django_db
def test_signup_page_is_shown(client):
    response = client.get(SIGNUP_URL)

    assert response.status_code == 200
    assert "accounts/signup.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_signup_redirects_to_complete_and_saves_user(client):
    response = client.post(SIGNUP_URL, VALID_DATA)

    assert response.status_code == 302
    assert response.url == COMPLETE_URL
    assert User.objects.filter(username="taro").exists()


@pytest.mark.django_db
def test_invalid_input_shows_errors_without_saving(client):
    response = client.post(SIGNUP_URL, {**VALID_DATA, "username": "ab"})

    assert response.status_code == 200
    assert "ユーザー名は3文字以上で入力してください。" in response.content.decode()
    assert not User.objects.exists()


@pytest.mark.django_db
def test_integrity_error_is_shown_as_form_error(client):
    # 検証のあと保存までの間に同じメールで登録された状況を、保存時の例外で再現する
    with mock.patch(
        "user_registration.accounts.forms.SignupForm.save", side_effect=IntegrityError
    ) as save:
        response = client.post(SIGNUP_URL, VALID_DATA)

    save.assert_called_once()
    assert response.status_code == 200
    assert "登録できませんでした。" in response.content.decode()


@pytest.mark.django_db
def test_complete_page_is_shown_once_after_signup(client):
    client.post(SIGNUP_URL, VALID_DATA)

    first = client.get(COMPLETE_URL)
    second = client.get(COMPLETE_URL)

    assert first.status_code == 200
    assert "登録が完了しました。" in first.content.decode()
    assert second.status_code == 302
    assert second.url == SIGNUP_URL


def test_root_redirects_to_signup(client):
    response = client.get("/")

    assert response.status_code == 302
    assert response.url == SIGNUP_URL


def test_complete_page_redirects_without_signup(client):
    response = client.get(COMPLETE_URL)

    assert response.status_code == 302
    assert response.url == SIGNUP_URL
