from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Config

def add_default_configuration(userId):
    onlySeat = Config(name="only Seat", url_json="/static/json/onlySeat.json", user=userId)
    onlySeat.save()
    allSeat = Config(name="all Seat", url_json="/static/json/allSeat.json", user=userId)
    allSeat.save()
    onlyStanding = Config(name="only standing", url_json="/static/json/onlyStanding.json", user=userId)
    onlyStanding.save()
    standingBleacher = Config(name="standing with bleacher", url_json="/static/json/standingWithBleacher.json", user=userId)
    standingBleacher.save()

@login_required
def area_configuration(request):
    if not(Config.objects.all()) :
        add_default_configuration(request.user)

    configurations = Config.objects.filter(user=request.user.id)
    return render(request, 'area_configuration.html', {'configurations' : configurations})
