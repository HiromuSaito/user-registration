import pytest
from django.contrib import admin
from django.forms.models import model_to_dict

from user_registration.accounts.forms import UserAdminChangeForm, UserAdminCreationForm
from user_registration.accounts.models import User


def creation_data(**overrides):
    data = {
        "username": "taro",
        "email": "taro@example.com",
        "pref": "13",
        "tel": "",
        "usable_password": "true",
        "password1": "Abcdefg1",
        "password2": "Abcdefg1",
    }
    data.update(overrides)
    return data


def test_user_admin_uses_forms_with_signup_rules():
    model_admin = admin.site.get_model_admin(User)

    assert model_admin.add_form is UserAdminCreationForm
    assert model_admin.form is UserAdminChangeForm


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        pytest.param("username", "ab", "min_length", id="username_too_short"),
        pytest.param("email", "taro", "email_invalid", id="email_invalid"),
        pytest.param("tel", "090-1234", "tel_not_digits", id="tel_not_digits"),
    ],
)
def test_creation_form_applies_signup_rules(field, value, code):
    form = UserAdminCreationForm(data=creation_data(**{field: value}))

    assert not form.is_valid()
    assert [error.code for error in form.errors.as_data()[field]] == [code]


@pytest.mark.django_db
def test_creation_form_normalizes_like_signup():
    form = UserAdminCreationForm(
        data=creation_data(email="Taro@Example.COM", tel="０９０１２３４")
    )

    assert form.is_valid(), form.errors
    user = form.save()
    assert user.email == "Taro@example.com"
    assert user.tel == "0901234"


def change_data(user, **overrides):
    data = {
        key: value
        for key, value in model_to_dict(user).items()
        if value is not None and key != "password"
    }
    data.update(overrides)
    return data


@pytest.mark.django_db
def test_change_form_accepts_own_email():
    user = User.objects.create_user("taro", "taro@example.com", "Abcdefg1", pref_id=13)

    form = UserAdminChangeForm(instance=user, data=change_data(user))

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_change_form_rejects_email_of_another_user():
    User.objects.create_user("jiro", "jiro@example.com", "Abcdefg1", pref_id=13)
    user = User.objects.create_user("taro", "taro@example.com", "Abcdefg1", pref_id=13)

    form = UserAdminChangeForm(
        instance=user, data=change_data(user, email="JIRO@example.com")
    )

    assert not form.is_valid()
    assert "このメールアドレスは既に登録されています。" in form.non_field_errors()
