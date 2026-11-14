import pytest
from django.urls import reverse
from rest_framework.test import APIClient

PREF_LIST_URL = reverse("locations_api:pref_list")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_pref_list_returns_all_prefs_in_code_order(api_client):
    response = api_client.get(PREF_LIST_URL)

    assert response.status_code == 200
    prefs = response.json()
    assert len(prefs) == 47
    assert [pref["code"] for pref in prefs] == list(range(1, 48))


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("index", "expected"),
    [
        pytest.param(0, {"code": 1, "name": "北海道"}, id="first"),
        pytest.param(12, {"code": 13, "name": "東京都"}, id="tokyo"),
        pytest.param(46, {"code": 47, "name": "沖縄県"}, id="last"),
    ],
)
def test_pref_list_item(api_client, index, expected):
    response = api_client.get(PREF_LIST_URL)

    assert response.json()[index] == expected
