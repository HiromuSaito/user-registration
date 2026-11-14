import pytest

from accounts.api.serializers import UserCreateSerializer
from accounts.models import User


def request_data(**overrides):
    data = {
        "username": "taro",
        "email": "taro@example.com",
        "password": "Abcdefg1",
        "tel": "",
        "pref": 13,
    }
    data.update(overrides)
    return data


def error_codes(serializer, field):
    return [detail.code for detail in serializer.errors.get(field, [])]


@pytest.mark.django_db
def test_save_creates_user():
    serializer = UserCreateSerializer(data=request_data(email="Taro@Example.com"))

    assert serializer.is_valid(), serializer.errors
    user = serializer.save()

    user.refresh_from_db()
    assert user.username == "taro"
    assert user.email == "Taro@example.com"
    assert user.check_password("Abcdefg1")
    assert user.tel is None
    assert user.pref.name == "東京都"


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("tel", "expected"),
    [
        pytest.param("", None, id="empty_is_none"),
        pytest.param(None, None, id="null_is_none"),
        pytest.param("0901234", "0901234", id="halfwidth"),
        pytest.param("０９０１２３４", "0901234", id="fullwidth"),
        pytest.param(" 0901234 ", "0901234", id="surrounding_spaces"),
    ],
)
def test_tel_is_normalized(tel, expected):
    serializer = UserCreateSerializer(data=request_data(tel=tel))

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["tel"] == expected


@pytest.mark.django_db
def test_tel_can_be_omitted():
    data = request_data()
    del data["tel"]
    serializer = UserCreateSerializer(data=data)

    assert serializer.is_valid(), serializer.errors
    assert serializer.save().tel is None


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        pytest.param("username", "", ["blank"], id="username_blank"),
        pytest.param("username", "ab", ["username_too_short"], id="username_too_short"),
        pytest.param("username", "ta ro", ["invalid"], id="username_invalid_chars"),
        pytest.param("email", "", ["blank"], id="email_blank"),
        pytest.param("email", "taro", ["email_invalid"], id="email_invalid"),
        pytest.param("password", "", ["blank"], id="password_blank"),
        pytest.param(
            "password",
            "abc",
            ["password_too_short", "password_no_upper", "password_no_digit"],
            id="password_rules",
        ),
        pytest.param("tel", "090-1234", ["tel_not_digits"], id="tel_not_digits"),
        pytest.param("pref", None, ["null"], id="pref_null"),
        pytest.param("pref", 48, ["does_not_exist"], id="pref_not_exists"),
    ],
)
def test_invalid_input(field, value, expected):
    serializer = UserCreateSerializer(data=request_data(**{field: value}))

    assert not serializer.is_valid()
    assert error_codes(serializer, field) == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field",
    ["username", "email", "password", "pref"],
)
def test_required_fields(field):
    data = request_data()
    del data[field]
    serializer = UserCreateSerializer(data=data)

    assert not serializer.is_valid()
    assert error_codes(serializer, field) == ["required"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("field", "registered", "value", "expected"),
    [
        pytest.param(
            "email",
            "Taro@Example.com",
            "taro@example.com",
            ["email_taken"],
            id="email_case_insensitive",
        ),
        pytest.param("username", "taro", "taro", ["unique"], id="username"),
    ],
)
def test_duplicate(field, registered, value, expected):
    User.objects.create_user(
        **{"username": "someone", "email": "someone@example.com", field: registered},
        password="Abcdefg1",
        pref_id=1,
    )
    serializer = UserCreateSerializer(data=request_data(**{field: value}))

    assert not serializer.is_valid()
    assert error_codes(serializer, field) == expected


@pytest.mark.django_db
def test_password_is_not_in_output():
    serializer = UserCreateSerializer(data=request_data())
    serializer.is_valid()
    serializer.save()

    assert serializer.data == {
        "username": "taro",
        "email": "taro@example.com",
        "tel": None,
        "pref": 13,
    }
