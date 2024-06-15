from django.contrib import admin

from .models import Place, Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


class ImageInline(admin.TabularInline):
    model = Image
    verbose_name = "Фотография"
    verbose_name_plural = "Фотографии"


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
