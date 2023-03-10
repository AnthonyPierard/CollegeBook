from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test

from datetime import datetime

from .models import Evenement, User, Representation, Reservation
from .forms import *


def visu_event(request):
    all_event = Evenement.objects.all()
    return render(request, 'client/visu_event.html', {'all_event' : all_event})

def visu_detail(request, even_id):
    event = get_object_or_404(Evenement, pk = even_id)
    return render(request, 'client/visu_detail.html', {"event" : event})

@user_passes_test(lambda u:u.is_active and u.is_staff)
def crea_compte(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = AdminForm()

    return render(request, 'admin/crea_compte.html', {'form': form})

@login_required
def cre_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = EventForm()

    return render (request, 'admin/crea_event.html',{'form':form})

@login_required
def modif_compte(request,admin_id):
    admin = get_object_or_404(User, pk = admin_id)
    if request.method == 'POST':
        form = UpdateAdminForm(request.POST,instance=admin)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:

        form = UpdateAdminForm(instance=admin)
    return render(request,'admin/modif_compte.html',{'form':form,'admin' : admin})

@user_passes_test(lambda u:u.is_active and u.is_staff)
def admin_display(request):
    all_admins = User.objects.all()
    return render(request, 'admin/afficher_admin.html', {'all_admins': all_admins})

@login_required
def admin_event(request, admin_id):
    admin_events = Evenement.objects.filter(admin=admin_id)
    admin_representations = list()
    for event in admin_events:
        representations = Representation.objects.filter(event=event.id)
        for representation in representations:
            admin_representations.append(representation)
    return render(request, 'admin/event_admin.html', {'admin_representations' :admin_representations})

def admin_login(request):
    if request.method == 'POST':
        form = LoginAdminForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
            if user is not None and user.is_active:
                login(request=request, user=user)
                return HttpResponseRedirect('/')
    else:
        form = LoginAdminForm()
    return render(request, 'admin/connection.html', {'form': form})

@login_required
def admin_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@user_passes_test(lambda u:u.is_active and u.is_staff,login_url='')
def admin_change_super(request, admin_id):
    admin = User.objects.filter(id=admin_id)[0]
    admin.super_admin_update()
    admin.save()
    return HttpResponseRedirect('/afficher_admins')

@user_passes_test(lambda u:u.is_active and u.is_staff,login_url='')
def admin_change_archived(request, admin_id):
    admin = User.objects.filter(id=admin_id)[0]
    admin.archive_admin()
    admin.save()
    return HttpResponseRedirect('/afficher_admins')

@login_required
def admin_representation_change_date(request, representation_id):
    if request.method == 'POST':
        form = UpdateDateEventForm(request.POST)
        print(form)
        if form.is_valid():
            print("yes")
            representation = Representation.objects.filter(pk = representation_id)[0]
            representation.repr_date = datetime.strptime(form.cleaned_data['repr_date'], '%d-%m-%Y/%H:%M')
            representation.save()
            ok_message = "La date à été correctement changée"
        return HttpResponseRedirect(f'/admin_event/{request.user.id}')
            # all_event_for_admin = Evenement.objects.filter(admin=request.user.id)
            # #ajouter ici un envois d'un mail a toutes les personnes qui ont réservé
            # return render(request, 'admin/event_admin.html', {'all_event_admin' : all_event_for_admin, "msg" : ok_message})
    else:
        form = UpdateDateEventForm()
        representation = Representation.objects.filter(pk = representation_id)[0]
        return render(request, 'admin/change_date_representation.html', {"form" : form, "representation": representation})

@login_required
def admin_representation_delete(request, representation_id):
    if request.method=='POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choix']
            if choice=="1":
                Representation.objects.filter(pk = representation_id).delete()
                #avertir les personnes qui ont réserver via un mail.
        return HttpResponseRedirect(f'/admin_event/{request.user.id}')
    else:
        form = ConfirmForm()
        event = Representation.objects.filter(pk = representation_id)[0]
        return render(request, 'admin/confirm_del.html', {"form" : form, "event" : event})
    

def reservation_event(request, even_id):
    if request.method == 'POST':
        
        form = ReservationForm(request.POST)
        if form.is_valid():
            newform = Reservation()
            newform.reserv_email = form.cleaned_data['reserv_email']
            newform.reserv_nom = form.cleaned_data["reserv_nom"]
            newform.reserv_prenom = form.cleaned_data["reserv_prenom"]
            newform.reserv_tel = form.cleaned_data["reserv_tel"]
            newform.reserv_numero = 1
            newform.representation = Representation.objects.filter(pk = even_id)[0]
        #request_copy = request.POST.copy()
        #request_copy['reserv_numero'] = 1
        #form = ReservationForm(request_copy)
            
            newform.save()
            return HttpResponseRedirect('/')
        
    else:
        form = ReservationForm()
    return render(request, 'client/reservation_event.html',{'form':form})
    


