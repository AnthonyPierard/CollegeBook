from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.utils import timezone

from Account.forms import UserForm, LoginUserForm, UpdateUserForm
from Account.models import User
from Event.models import Representation, Event


@user_passes_test(lambda u: u.is_active and u.is_staff)
def account_creation(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Account:display')
    else:
        form = UserForm()

    return render(request, 'account_creation.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
            if user is not None and user.is_active:
                login(request=request, user=user)
                return redirect('Event:display')
    else:
        form = LoginUserForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('Event:display')


@login_required
def update_account(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('Event:display')
    else:

        form = UpdateUserForm(instance=user)
    return render(request, 'update_account.html', {'form': form})


@user_passes_test(lambda u: u.is_active and u.is_staff)
def users_display(request):
    all_users = User.objects.all()
    return render(request, 'users_display.html', {'all_users': all_users})


@user_passes_test(lambda u: u.is_active and u.is_staff, login_url='')
def user_update_admin(request, user_id):
    user = User.objects.get(id=user_id)
    user.update_is_staff_superuser()
    user.save()
    return redirect('Account:display')


@user_passes_test(lambda u: u.is_active and u.is_staff, login_url='')
def user_update_archive(request, user_id):
    user = User.objects.get(id=user_id)
    user.update_is_active()
    user.save()
    return redirect('Account:display')


@login_required
def user_events_display(request, user_id):
    user_events = Event.objects.filter(user=user_id)
    user_representations = list()
    for event in user_events:
        representations = Representation.objects.filter(event=event.id)
        for representation in representations:
            user_representations.append(representation)
    return render(request, 'user_events_display.html', {'user_representations': user_representations, 'now' : timezone.now()})
