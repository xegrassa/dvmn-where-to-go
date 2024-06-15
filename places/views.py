from places.models import Place
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


# Create your views here.


def place_read(request, place_id: int):

    obj = get_object_or_404(Place, id=place_id)
    return HttpResponse(obj.title)
