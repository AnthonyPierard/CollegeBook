from django.shortcuts import render, redirect

from Event.models import Representation, Event, Price, Place
from .models import Reservation, Ticket, SeatingTicket, StandingTicket
from .forms import ReservationForm

from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
import reportlab
import qrcode

def seat_selection(request, representation_id):
    representation = Representation.objects.get(pk = representation_id)
    return render(request, 'seat_selection.html', {"representation" : representation})

def representation_reservation(request, representation_id):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # reservation = Reservation()
            # reservation.email = form.cleaned_data['email']
            # reservation.last_name = form.cleaned_data["last_name"]
            # reservation.first_name = form.cleaned_data["first_name"]
            # reservation.phone = form.cleaned_data["phone"]
            # reservation.number = 1 #todo rendre l'incrémentation automatique
            # reservation.representation = Representation.objects.get(pk=representation_id)
            form.save(representation_id)

            reservation = Reservation.objects.filter(email= form.cleaned_data['email'], representation_id= representation_id)[0]
            email = EmailMessage(
                'Reservation',
                'Vous avez reserver un Ticket pour la representation de %s pour la date du %s' % (
                reservation.representation.event.name, reservation.representation.date),
                'collegebooktest@gmail.com',
                ['%s' % form.cleaned_data['email']],
                headers={"Reply-To": 'collegebooktest@gmail.com'})

            selected_seats = form.cleaned_data["selectedseat"]
            selected_seats = selected_seats.split(",")
            p = canvas.Canvas('Tickets.pdf')
            for i in range(len(selected_seats)):
                y = 150
                x = 50
                d = i + 1
                data = 'https://www.youtube.com/%d' % d
                img = qrcode.make(data)
                img.save('Tickets n° %d.png' % d)
                p.drawString(x, y, "Tickets place %s" % list[i])
                y = + 200
                p.drawImage('Tickets n° %d.png' % d, 100, y, mask='auto')
                p.showPage()

            for i in range(int(form.cleaned_data["drink_number"])):
                y = 150
                x = 50
                d = i + 1
                data = 'https://www.youtube.com/%d' % d
                img = qrcode.make(data)
                img.save('Tickets Boisson n° %d.png' % d)
                p.drawString(x, y, "Tickets Boisson")
                y = + 200
                p.drawImage('Tickets Boisson n° %d.png' % d, 100, y, mask='auto')
                p.showPage()

            for i in range(int(form.cleaned_data["food_number"])):
                y = 150
                x = 50
                d = i + 1
                data = 'https://www.youtube.com/%d' % d
                img = qrcode.make(data)
                img.save('Tickets Nourriture n° %d.png' % d)
                p.drawString(x, y, "Tickets Nourriture")
                y = + 200
                p.drawImage('Tickets Nourriture n° %d.png' % d, 100, y, mask='auto')
                p.showPage()
            p.save()
            email.attach_file('Tickets.pdf')
            email.send()
            email.attach_file('Tickets Nourriture n° %d.png' %d)
            return redirect('Event:display')

    else:
        form = ReservationForm()
        event_id = Representation.objects.get(pk=representation_id).event
        price_tickets = Price.objects.filter(event=event_id)
        drink_price = price_tickets.get(type="Boisson")
        food_price = price_tickets.get(type="Nourriture")
        place_price = Place.objects.all()
        return render(request, 'representation_reservation.html',
                      {'form': form, 'drink_price': drink_price, 'food_price': food_price, "place_price": place_price})

def makeQrcode():
    data = 'https://www.youtube.com/shorts/SXHMnicI6Pg'
    img = qrcode.make(data)