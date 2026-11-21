from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_safe


# Django はテンプレートで CSRF のトークンを使ったときだけ Cookie を出す。SPA のテンプレートは
# トークンを使わないため、付けないと Cookie が出ず、SPA の最初の POST が CSRF のチェックで失敗する。
# path は使わない。どの URL でも同じ HTML を返し、画面は React Router が URL から決める
@require_safe
@ensure_csrf_cookie
def spa(request, path=""):
    return render(request, "app.html")
