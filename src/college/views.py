from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate

from .models import Evenement
from .models import Admin
from .forms import AdminForm,UpdateAdminForm,LoginAdminForm,EventForm
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

    return render(request, 'admin/crea_compte.html', {'form': form, 'connected':True, 'super_admin':True})

def cre_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<h1>Toast</h1>')
    else:
        form = EventForm()

    return render (request, 'admin/crea_event.html',{'form':form, 'connected':True})


def modif_compte(request,admin_id):
    admin = get_object_or_404(Admin, pk = admin_id)
    if request.method == 'POST':
        form = UpdateAdminForm(request.POST,instance=admin)
        if form.is_valid():
            form.save()
    else:

        form = UpdateAdminForm(instance=admin)
    return render(request,'admin/modif_compte.html',{'form':form,'admin' : admin})

def archiver_compte(request,admin_id):
    admin = Admin.objects.filter(id=admin_id)[0]
    admin.admin_is_archived = True
    admin.save()
    return visu_event(request) # l'url pue la merde en faisant ca

def admin_display(request):
    all_admins = Admin.objects.all()
    return render(request, 'admin/afficher_admin.html', {'all_admins': all_admins})


def login(request):
    if request.method == 'POST':
        form = LoginAdminForm(request.POST)
        if form.is_valid():
            id_form = form.cleaned_data['admin_pseudo']
            password_form = form.cleaned_data['admin_password']
            admin = get_object_or_404(Admin, admin_pseudo = id_form)
            if admin.admin_password == password_form :   
            #user = authenticate(username= id_form, password= password_form)
            #if user is not None:
                #admin = get_object_or_404(Admin, admin_pseudo = id_form)
                if admin.admin_superadmin == True:
                    return render(request, 'client/visu_event.html', {"connected" : True, 'super_admin' : True})
                else:
                    return render(request, 'client/visu_event.html', {"connected" : True, 'super_admin' : False})
    else:
        form = LoginAdminForm()
    return render(request, 'admin/connection.html', {'form': form, 'connected':False})
