from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from where_to_go import views
from places import views as places_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("places/<int:place_id>/", places_view.place_read, name="place_detail"),
    path("", views.show_main),
    path("tinymce/", include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
