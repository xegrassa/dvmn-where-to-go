from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place


def read_place(request, place_id: int):
    place = get_object_or_404(Place, id=place_id)

    payload = {
        "title": place.title,
        "imgs": [img.image.url for img in place.image_set.all()],
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {"lat": place.latitude, "lng": place.longitude},
    }
    return JsonResponse(payload, json_dumps_params={"indent": 4, "ensure_ascii": False}, safe=False)


def show_main(request):
    points = {"type": "FeatureCollection", "features": []}

    for place in Place.objects.all():
        point = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [place.longitude, place.latitude]},
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": reverse("place_detail", args=[place.id]),
            },
        }
        points["features"].append(point)

    return render(request, "index.html", context={"points": points})
