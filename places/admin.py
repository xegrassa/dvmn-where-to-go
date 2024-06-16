from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin

from .models import Place, Image

ADMIN_PREVIEW_IMAGE_HEIGHT = "200"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ["place", "image"]


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    verbose_name = "Фотография"
    verbose_name_plural = "Фотографии"
    extra = 0

    readonly_fields = ('preview',)

    def preview(self, obj):
        return format_html(
            '<img src="{url}" height={height} />',
            url=obj.image.url,
            height=ADMIN_PREVIEW_IMAGE_HEIGHT,
        )


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
