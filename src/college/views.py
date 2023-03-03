from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Evenement, User
from .forms import AdminForm,UpdateAdminForm,LoginAdminForm,EventForm, UpdateDateEventForm, ConfirmForm


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
            return HttpResponseRedirect('/')
    else:
        form = AdminForm()

    return render(request, 'admin/crea_compte.html', {'form': form})

def cre_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = EventForm()

    return render (request, 'admin/crea_event.html',{'form':form})


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

# def archiver_compte(request,admin_id):
#     admin = Admin.objects.filter(id=admin_id)[0]
#     admin.admin_is_archived = True
#     admin.save()
#     return visu_event(request) # l'url pue la merde en faisant ca

@login_required
def admin_display(request):
    all_admins = User.objects.all()
    return render(request, 'admin/afficher_admin.html', {'all_admins': all_admins})

@login_required
def admin_event(request, admin_id):
    all_event_for_admin = Evenement.objects.filter(admin=admin_id)
    return render(request, 'admin/event_admin.html', {'all_event_admin' : all_event_for_admin, "admin" : request.user, "connected" : request.user.is_authenticated})

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

def admin_change_super(request, admin_id):
    admin = User.objects.filter(id=admin_id)[0]
    admin.super_admin_update()
    admin.save()
    return HttpResponseRedirect('/afficher_admins')

def admin_change_archived(request, admin_id):
    admin = User.objects.filter(id=admin_id)[0]
    admin.archive_admin()
    admin.save()
    return HttpResponseRedirect('/afficher_admins')

def admin_event_change_date(request, event_id):
    if request.method== 'POST':
        form = UpdateDateEventForm(request.POST)
        if form.is_valid():
            event = Evenement.objects.filter(pk = event_id)[0]
            event.even_date = form.cleaned_data['even_date']
            event.save()
            ok_message = "La date à été correctement changée"
            all_event_for_admin = Evenement.objects.filter(admin=request.user.id)
            #ajouter ici un envois d'un mail a toutes les personnes qui ont réservé
            return render(request, 'admin/event_admin.html', {'all_event_admin' : all_event_for_admin, "admin" : request.user, "msg" : ok_message, "connected" : request.user.is_authenticated})
    else:
        form = UpdateDateEventForm()
        event = Evenement.objects.filter(pk = event_id)[0]
        return render(request, 'admin/change_date_event.html', {"admin" : request.user, "form" : form, "connected" : request.user.is_authenticated, "event": event})

def admin_event_delete(request, event_id):
    if request.method=='POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choix']
            if choice=="1":
                Evenement.objects.filter(pk = event_id).delete()
                #avertir les personnes qui ont réserver via un mail.
        all_event_for_admin = Evenement.objects.filter(admin=request.user.id)
        return render(request,'admin/event_admin.html', {'all_event_admin' : all_event_for_admin})
    else:
        form = ConfirmForm()
        event = Evenement.objects.filter(pk = event_id)[0]
        return render(request, 'admin/confirm_del.html', {"form" : form, "event" : event})