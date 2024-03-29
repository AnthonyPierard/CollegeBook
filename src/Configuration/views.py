from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .forms import ConfigForm
from .models import Config

import json
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
    if request.method=='POST':
        print(request.POST.get('config'))
        form = ConfigForm(request.POST)
        if form.is_valid():
            #l'enregistrement marche bien mais ne marche pas bien en globale car je ne crée pas encore de json
            configName = form.cleaned_data['nom']
            goodConfigName = configName.replace(' ', '_')
            otherConfig = Config.objects.filter(name=goodConfigName)
            if(len(otherConfig)==0):
                newConfig = Config(name=configName, url_json="/static/json/" + goodConfigName + ".json", user= request.user)
                newConfig.save()
            configurations = Config.objects.filter(user=request.user.id)
            return render(request, 'area_configuration.html', {'configurations' : configurations, 'form' : form})
    else :
        if not(Config.objects.filter(user=request.user)) :
            add_default_configuration(request.user)
        configurations = Config.objects.filter(user=request.user.id)
        form = ConfigForm()
        return render(request, 'area_configuration.html', {'configurations' : configurations, 'form' : form})

def create_json(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        goodName = data[0]['nom'].replace(" " , "_")
        path_file = 'Configuration/static/json/' + goodName + '.json'
        print(path_file)
        with open(path_file, 'w') as fi:
            json.dump(data, fi)

        return redirect("Config:Configuration")