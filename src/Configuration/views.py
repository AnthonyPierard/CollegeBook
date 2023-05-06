from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse

from CollegeBook.utils import configCreator
from .forms import ConfigForm
from .models import Config

import json


def add_default_configuration(userId):
    """
    :param userId: the id of the current user log
    :return: create de 4 configurations basic and link them to the user
    """
    basicSeats = {"Debout": 3.00, "Classic": 4.00, "Vip": 5.00}
    configCreator(config_name="only Seat", json_url="/static/json/onlySeat.json", user_id=userId, seats=basicSeats)
    configCreator(config_name="all Seat", json_url="/static/json/allSeat.json", user_id=userId, seats=basicSeats)
    configCreator(config_name="only standing", json_url="/static/json/onlyStanding.json", user_id=userId,
                  seats=basicSeats)
    configCreator(config_name="standing with bleacher", json_url="/static/json/standingWithBleacher.json",
                  user_id=userId, seats=basicSeats)


@login_required
def area_configuration(request):
    """
    :param request:
        POST : the information to create a new configurations
        GET : display the html with the editor of a new configuration
    :return: area_configuration.html
    """
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
        configurations = Config.objects.filter(user=request.user.id)
        return render(request, 'area_configuration.html', {'configurations': configurations, 'form': form})

    else:
        if not (Config.objects.filter(user=request.user)):
            add_default_configuration(request.user)
        configurations = Config.objects.filter(user=request.user.id)
        form = ConfigForm()
        return render(request, 'area_configuration.html', {'configurations': configurations, 'form': form})


def create_json(request):
    """
    :param request:
        POST : the json with the information about a configuration (all the information about seats or standing place)
    :return: area_configuration
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        goodName = data[0]['nom'].replace(" ", "_")
        path_file = 'Configuration/static/json/' + goodName + '.json'
        print(path_file)
        with open(path_file, 'w') as fi:
            json.dump(data, fi)

        return redirect("Config:Configuration")
