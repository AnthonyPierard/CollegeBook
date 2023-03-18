from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def area_configuration(request):
    return render(request, 'area_configuration.html')
