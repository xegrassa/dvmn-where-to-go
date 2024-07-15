from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField("Название", max_length=255, unique=True)
    short_description = models.TextField("Короткое описание", blank=True)
    long_description = HTMLField("Длинное описание", blank=True)
    longitude = models.FloatField("Долгота")
    latitude = models.FloatField("Широта")

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place, related_name="images", on_delete=models.CASCADE, verbose_name="Место")
    image = models.ImageField("Файл картинки")
    _order = models.PositiveSmallIntegerField("Позиция", default=0, blank=True, db_index=True)

    class Meta(object):
        ordering = ["_order"]

    def __str__(self):
        return f"{self._order} {self.place}"
