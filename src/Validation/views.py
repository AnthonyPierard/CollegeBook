from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from Event.models import Event
from Reservation.models import SeatingTicket, FoodTicket, DrinkTicket, AbstractTicket, Reservation, \
    Representation


# Create your views here.
@login_required()
def scan_ticket(request, code):
    try:
        ticket = AbstractTicket.objects.get(pk=code)
    except AbstractTicket.DoesNotExist:
        error = "Ce ticket n'est pas valide"
        return render(request, 'ticket_error.html', {'error_str': error})
    if ticket.qrcode_is_validated:
        error = "Le ticket à déjà été utilisé"
        return render(request, 'ticket_error.html', {'error_str': error})
    type_ticket = ticket.get_real_concrete_instance_class()
    print(type_ticket)
    if type_ticket == DrinkTicket:
        type_ticket = 'Boisson'
    elif type_ticket == FoodTicket:
        type_ticket = 'Nourriture'
    elif type_ticket == SeatingTicket:
        type_ticket = "Assis"
    else:
        type_ticket = "Debout"
    try:
        seat_number = ticket.seat_number
    except Exception:
        seat_number = None
    reservation = Reservation.objects.get(pk=ticket.reservation.id)
    representation = Representation.objects.get(pk=reservation.representation.id)
    event = Event.objects.get(pk=representation.event.id)
    if representation.date.year <= timezone.now().year \
            and representation.date.month <= timezone.now().month and representation.date.day < timezone.now().day:
        error = f"Ticket expiré. Valable pour le {representation.date.strftime('%d/%m/%Y')}"
        return render(request, 'ticket_error.html', {'error_str': error})
    return render(request, 'scan_tickets.html',
                  {'type_ticket': type_ticket, 'seat_number': seat_number, 'reservation': reservation, 'representation': representation,
                   'code': code, 'event_name':event.name})


@login_required()
def validation_ticket(request, code):
    ticket = AbstractTicket.objects.get(pk=code)
    if ticket is None:
        raise ValueError("Ce ticket n'existe pas")
    ticket.qrcode_is_validated = True
    ticket.save()
    validated = "Ticket Accepté"
    return render(request, 'ticket_validated.html', {'validated_str': validated})
