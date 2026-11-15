import pytest
from django_vite.core.asset_loader import DjangoViteAssetLoader


def _reload_django_vite():
    # django-vite は設定を起動時に 1 回だけ読んで使い回すため、settings を書き換えたら
    # 作り直させる。django-vite 自身のテスト（tests/conftest.py）と同じやり方
    DjangoViteAssetLoader._instance = None
    DjangoViteAssetLoader.instance()


# テストではフロントをビルドしないため、ビルドでできる manifest を読まずに描ける開発用の形にする
@pytest.fixture
def vite_dev_mode(settings):
    original = settings.DJANGO_VITE
    settings.DJANGO_VITE = {"default": {**original["default"], "dev_mode": True}}
    _reload_django_vite()
    yield
    # settings fixture が設定を戻すのはこの後片付けより後なので、ここで戻してから作り直す
    settings.DJANGO_VITE = original
    _reload_django_vite()
