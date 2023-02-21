from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Evenement
from .models import Admin
from .forms import AdminForm
# Create your views here.


def visu_event(request):
    all_event = Evenement.objects.all()

    return render(request, 'client/visu_event.html', {'all_event' : all_event})

def visu_detail(request, even_id):
    event = get_object_or_404(Evenement, pk = even_id)
    return render(request, 'client/visu_detail.html', {"event" : event})

def crea_compte(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<h1>Thanks</h1>')
    else:
        form = AdminForm()

    return render(request, 'admin/crea_compte.html', {'form': form})
    
def supprimer_compte(admin_id):
    Admin.objects.filter(id=admin_id).delete()

def modif_compte(request,admin_id):
    admin = get_object_or_404(Admin, pk = admin_id)
    return render(request,'admin/modif_compte.html',{'admin' : admin})