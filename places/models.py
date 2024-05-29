from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=100)
    description_short = models.CharField(max_length=255)
    description_long = models.TextField()
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place, null=True, on_delete=models.SET_NULL)
    image = models.ImageField()
    _order = models.PositiveSmallIntegerField(verbose_name="order", default=0)

    class Meta(object):
        ordering = ("place", "_order",)

    def __str__(self):
        return f"{self._order} {self.place}"
