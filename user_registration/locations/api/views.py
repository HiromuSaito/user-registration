from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user_registration.locations.models import Pref

from .serializers import PrefSerializer


@extend_schema(responses=PrefSerializer(many=True))
@api_view(["GET"])
def pref_list(request):
    prefs = Pref.objects.all()
    return Response(PrefSerializer(prefs, many=True).data)
