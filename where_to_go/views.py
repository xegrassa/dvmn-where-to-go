from django.shortcuts import render
from django.urls import reverse

from places.models import Place


def show_main(request):
    points = {"type": "FeatureCollection", "features": []}

    for place in Place.objects.all():
        point = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": reverse("place_detail", args=[place.id])
            },
        }
        points["features"].append(point)

    return render(request, "index.html", context={"points": points})
