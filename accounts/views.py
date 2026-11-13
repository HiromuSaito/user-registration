from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render

from .forms import SignupForm

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
                form.add_error(
                    None,
                    "登録できませんでした。入力内容を確かめて、もう一度お試しください。",
                )
            else:
                request.session[SIGNUP_COMPLETED_SESSION_KEY] = True
                return redirect("accounts:signup_complete")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


def signup_complete(request):
    # 完了画面に直接来た人や再読み込みした人は、登録画面に戻す
    if not request.session.pop(SIGNUP_COMPLETED_SESSION_KEY, False):
        return redirect("accounts:signup")
    return render(request, "accounts/signup_complete.html")
