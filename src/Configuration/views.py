from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Config

@login_required
def area_configuration(request):
    configs = Config.objects.filter(user=request.user.id)
    return render(request, 'area_configuration.html', {'configs' : configs})
