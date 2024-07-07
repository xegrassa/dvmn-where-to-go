from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from places.models import Place


def place_read(request, place_id: int):
    place = get_object_or_404(Place, id=place_id)

    payload = {
        "title": place.title,
        "imgs": [img.image.url for img in place.image_set.all()],
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {"lat": place.latitude, "lng": place.longitude},
    }
    return JsonResponse(payload, json_dumps_params={"indent": 4, "ensure_ascii": False}, safe=False)
