from django.shortcuts import render

from Event.models import Representation


def reservation(request, representation_id):
    representation = Representation.objects.get(pk=representation_id)
    return render(request, '', {"representation": representation})
