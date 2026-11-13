from django.db import models


class Pref(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=4, unique=True)

    class Meta:
        ordering = ["code"]
        verbose_name = "都道府県"
        verbose_name_plural = "都道府県"

    def __str__(self):
        return self.name
