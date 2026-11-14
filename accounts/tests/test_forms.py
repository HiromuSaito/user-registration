import pytest

from accounts.forms import SignupForm
from accounts.models import User


def form_data(**overrides):
    data = {
        "username": "taro",
        "email": "taro@example.com",
        "password": "Abcdefg1",
        "tel": "",
        "pref": "13",
    }
    data.update(overrides)
    return data


def error_codes(form, field):
    return [error.code for error in form.errors.as_data().get(field, [])]


@pytest.mark.django_db
def test_save_creates_user():
    form = SignupForm(data=form_data(email="Taro@Example.com"))

    assert form.is_valid()
    user = form.save()

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
        pytest.param("0901234", "0901234", id="halfwidth"),
        pytest.param("０９０１２３４", "0901234", id="fullwidth"),
        pytest.param(" 0901234 ", "0901234", id="surrounding_spaces"),
    ],
)
def test_tel_is_normalized(tel, expected):
    form = SignupForm(data=form_data(tel=tel))

    assert form.is_valid()
    assert form.cleaned_data["tel"] == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        pytest.param("username", "", ["required"], id="username_required"),
        pytest.param("username", "ab", ["min_length"], id="username_too_short"),
        pytest.param("username", "ta ro", ["invalid"], id="username_invalid_chars"),
        pytest.param("email", "", ["required"], id="email_required"),
        pytest.param("email", "taro", ["email_invalid"], id="email_invalid"),
        pytest.param("password", "", ["required"], id="password_required"),
        pytest.param(
            "password",
            "abc",
            ["password_too_short", "password_no_upper", "password_no_digit"],
            id="password_rules",
        ),
        pytest.param("tel", "090-1234", ["tel_not_digits"], id="tel_not_digits"),
        pytest.param("pref", "", ["required"], id="pref_required"),
        pytest.param("pref", "48", ["invalid_choice"], id="pref_not_exists"),
    ],
)
def test_invalid_input(field, value, expected):
    form = SignupForm(data=form_data(**{field: value}))

    assert not form.is_valid()
    assert error_codes(form, field) == expected


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
    form = SignupForm(data=form_data(**{field: value}))

    assert not form.is_valid()
    assert error_codes(form, field) == expected


@pytest.mark.django_db
def test_username_allows_non_ascii_letters():
    form = SignupForm(data=form_data(username="山田太郎"))

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_username_invalid_chars_message_matches_behavior():
    form = SignupForm(data=form_data(username="ta ro"))

    assert not form.is_valid()
    assert form.errors["username"] == [
        "ユーザー名には、文字、数字、@/./+/-/_ だけを使えます。"
    ]
