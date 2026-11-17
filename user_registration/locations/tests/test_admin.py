import pytest
from django.contrib import admin

from user_registration.locations.models import Pref


@pytest.mark.parametrize(
    "permission",
    ["has_add_permission", "has_change_permission", "has_delete_permission"],
)
def test_prefs_are_read_only_in_admin(rf, permission):
    model_admin = admin.site.get_model_admin(Pref)

    assert getattr(model_admin, permission)(rf.get("/")) is False
