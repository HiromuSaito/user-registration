from django.forms.renderers import TemplatesSetting


# 欄のテンプレートを差し替えるには TemplatesSetting が要る（既定の DjangoTemplates は
# TEMPLATES の設定を見ないため、プロジェクトのテンプレートを読めない）
class FormRenderer(TemplatesSetting):
    field_template_name = "forms/field.html"
