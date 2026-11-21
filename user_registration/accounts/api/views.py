import logging

from django.db import IntegrityError, transaction
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.settings import api_settings

from user_registration.accounts.error_messages import SIGNUP_FAILED

from .serializers import UserCreateSerializer
from .throttles import SignupRateThrottle

logger = logging.getLogger(__name__)


@extend_schema(
    request=UserCreateSerializer,
    responses={
        201: UserCreateSerializer,
        400: OpenApiResponse(
            description="入力の誤り。項目ごとにエラーのメッセージの配列を返す"
        ),
        429: OpenApiResponse(
            description="登録の回数が多すぎる。Retry-After のヘッダーで、次に試せるまでの秒数を返す"
        ),
    },
)
@api_view(["POST"])
@throttle_classes([SignupRateThrottle])
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
        # 例外の内容には入力されたメールアドレスなどが含まれるため、ログには載せない
        logger.warning("ユーザー登録に失敗しました。")
        return Response(
            {api_settings.NON_FIELD_ERRORS_KEY: [SIGNUP_FAILED]},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(serializer.data, status=status.HTTP_201_CREATED)
