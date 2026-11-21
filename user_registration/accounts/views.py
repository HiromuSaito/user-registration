import logging

from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render

from .error_messages import SIGNUP_FAILED
from .forms import SignupForm

logger = logging.getLogger(__name__)

SIGNUP_COMPLETED_SESSION_KEY = "signup_completed"


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # 検証のあと保存までの間に同じメールやユーザー名で登録されると、
            # DB の一意制約で IntegrityError になる
            try:
                with transaction.atomic():
                    form.save()
            except IntegrityError:
                # 例外の内容には入力されたメールアドレスなどが含まれるため、ログには載せない
                logger.warning("ユーザー登録に失敗しました。")
                form.add_error(None, SIGNUP_FAILED)
            else:
                request.session[SIGNUP_COMPLETED_SESSION_KEY] = True
                return redirect("accounts:signup_complete")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


def signup_complete(request):
    if not request.session.pop(SIGNUP_COMPLETED_SESSION_KEY, False):
        return redirect("accounts:signup")
    return render(request, "accounts/signup_complete.html")
