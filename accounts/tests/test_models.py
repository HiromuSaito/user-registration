import pytest

from accounts.models import User


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("email", "expected"),
    [
        pytest.param("Taro@Example.com", True, id="same"),
        pytest.param("taro@example.com", True, id="lowercase"),
        pytest.param("TARO@EXAMPLE.COM", True, id="uppercase"),
        pytest.param("jiro@example.com", False, id="other_email"),
    ],
)
def test_email_is_registered(email, expected):
    User.objects.create_user("taro", "Taro@Example.com", "Abcdefg1", pref_id=13)

    assert User.objects.email_is_registered(email) is expected
