from django.http import JsonResponse
from django.shortcuts import render, get_list_or_404
from django.urls import reverse

from places.models import Place, Image


def read_place(request, place_id: int):
    images = get_list_or_404(Image.objects.select_related("place").filter(place_id=place_id))
    place = images[0].place
    payload = {
        "title": place.title,
        "imgs": [img.image.url for img in images],
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {"lat": place.latitude, "lng": place.longitude},
    }
    return JsonResponse(payload, json_dumps_params={"indent": 4, "ensure_ascii": False}, safe=False)


def show_main(request):
    features = [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [place.longitude, place.latitude]},
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": reverse("place_detail", args=[place.id]),
            },
        }
        for place in Place.objects.all()
    ]
    points = {"type": "FeatureCollection", "features": features}

    return render(request, "index.html", context={"points": points})
