from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from .models import Image, Place

ADMIN_PREVIEW_IMAGE_MAX_HEIGHT = "200"
ADMIN_PREVIEW_IMAGE_MAX_WIDTH = "300"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    autocomplete_fields = ["place"]

    fields = ["place", "image"]


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    verbose_name = "Фотография"
    verbose_name_plural = "Фотографии"
    extra = 0

    readonly_fields = ("get_preview_image",)

    def get_preview_image(self, obj):
        return format_html(
            '<img src="{url}" style="max-height:{height}px; max-width: {width}px;" />',
            url=obj.image.url,
            height=ADMIN_PREVIEW_IMAGE_MAX_HEIGHT,
            width=ADMIN_PREVIEW_IMAGE_MAX_WIDTH,
        )


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    search_fields = ["title"]

    inlines = [
        ImageInline,
    ]
