from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import EventForm, UpdateDateEventForm, ConfirmForm

from Event.models import Event, Representation


def events_display(request):
    all_event = Event.objects.all()
    return render(request, 'events_display.html', {'all_event': all_event})


def event_details(request, even_id):
    event = Event.objects.get(pk=even_id)
    representations = Representation.objects.filter(event=event.id)
    return render(request, 'event_details.html', {"event": event, "representations": representations})


@login_required
def event_creation(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Event:display')
    else:
        form = EventForm()

    return render(request, 'event_creation.html', {'form': form})


@login_required
def update_representation_date(request, representation_id):
    if request.method == 'POST':
        form = UpdateDateEventForm(request.POST)
        if form.is_valid():
            representation = Representation.objects.get(pk=representation_id)
            representation.date = datetime.strptime(form.cleaned_data['date'], '%d-%m-%Y/%H:%M')
            representation.save()
        return redirect('Account:events', request.user.id)
    else:
        form = UpdateDateEventForm()
        representation = Representation.objects.get(pk=representation_id)
        return render(request, 'update_representation_date.html', {"form": form, "representation": representation})


@login_required
def delete_representation(request, representation_id):
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            if choice == "1":
                Representation.objects.filter(pk=representation_id).delete()
                #TODO avertir les personnes qui ont réserver via un mail.
        return redirect('Account:events', request.user.id)
    else:
        form = ConfirmForm()
        event = Representation.objects.get(pk=representation_id)
        return render(request, 'delete_representation.html', {"form": form, "event": event})
