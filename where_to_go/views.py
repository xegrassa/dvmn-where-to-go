from django.shortcuts import render
from places.models import Place


def show_main(request):

    points = {
        "type": "FeatureCollection",
        "features": []
    }

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
                "detailsUrl": "./static/empty.json"
            }
        }
        points["features"].append(point)

    return render(request, 'index.html', context={"points": points})
