from rest_framework import serializers

from user_registration.locations.models import Pref


class PrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pref
        fields = ["code", "name"]
