from django.shortcuts import render
from django.http import HttpResponse

from .models import Evenement

from .forms import AdminForm
# Create your views here.


def visu_event(request):
    all_event = Evenement.objects.all()

    return render(request, 'client/visu_event.html', {'all_event' : all_event})

def crea_compte(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<h1>Thanks</h1>')
    else:
        form = AdminForm()

    return render(request, 'admin/crea_compte.html', {'form': form})