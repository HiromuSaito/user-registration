from django.db import IntegrityError, transaction
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .serializers import UserCreateSerializer


@extend_schema(
    request=UserCreateSerializer,
    responses={
        201: UserCreateSerializer,
        400: OpenApiResponse(
            description="入力の誤り。項目ごとにエラーのメッセージの配列を返す"
        ),
    },
)
@api_view(["POST"])
def user_create(request):
    # DRF はログインしていない人の POST に CSRF のチェックをかけない。
    # @api_view のビューには csrf_exempt の印が付き、外側に csrf_protect を付けても効かないため、
    # DRF が使うのと同じチェックをここで呼ぶ。失敗すると 403 を返す
    SessionAuthentication().enforce_csrf(request)
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # 検証のあと保存までの間に同じメールやユーザー名で登録されると、
    # DB の一意制約で IntegrityError になる
    try:
        with transaction.atomic():
            serializer.save()
    except IntegrityError:
        return Response(
            {
                api_settings.NON_FIELD_ERRORS_KEY: [
                    "登録できませんでした。入力内容を確かめて、もう一度お試しください。"
                ]
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(serializer.data, status=status.HTTP_201_CREATED)
