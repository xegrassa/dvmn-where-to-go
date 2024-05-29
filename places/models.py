from django.db import models

# Create your models here.

class Place(models.Model):
    title = models.CharField(max_length=100)
    description_short = models.CharField(max_length=255)
    description_long = models.TextField()
    longitude = models.FloatField()
    latitude = models.FloatField()
