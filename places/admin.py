from django.contrib import admin

# Register your models here.
from .models import Place, Image

admin.site.register(Place)
admin.site.register(Image)
