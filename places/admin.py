from django.contrib import admin
from django.utils.html import format_html

from .models import Place, Image

PREVIEW_IMAGE_HEIGHT = "200"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


class ImageInline(admin.TabularInline):
    model = Image
    verbose_name = "Фотография"
    verbose_name_plural = "Фотографии"

    readonly_fields = ('preview',)

    def preview(self, obj):
        return format_html(
            '<img src="{url}" height={height} />',
            url=obj.image.url,
            height=PREVIEW_IMAGE_HEIGHT,
        )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
