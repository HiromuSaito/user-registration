import pytest
from django.conf import settings
from django.urls import reverse

pytestmark = pytest.mark.usefixtures("vite_dev_mode")


@pytest.mark.parametrize("path", ["", "signup/", "signup/complete/"])
def test_spa_returns_same_page_for_any_path(client, path):
    response = client.get(f"/app/{path}")

    assert response.status_code == 200
    assert "app.html" in [t.name for t in response.templates]


def test_spa_sets_csrf_cookie(client):
    response = client.get(reverse("spa"))

    assert settings.CSRF_COOKIE_NAME in response.cookies


def test_spa_rejects_post(client):
    response = client.post(reverse("spa"))

    assert response.status_code == 405


def test_root_redirects_to_spa_signup(client):
    response = client.get("/")

    assert response.status_code == 302
    assert response.url == reverse("spa", kwargs={"path": "signup/"})
