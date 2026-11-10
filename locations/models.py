from django.db import models


class Pref(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=4, unique=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.name
