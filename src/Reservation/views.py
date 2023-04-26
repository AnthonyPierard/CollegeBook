import os.path

from django.shortcuts import render, redirect

from Event.models import Representation, Event, Price, Place
from .models import Reservation, Ticket, SeatingTicket, StandingTicket
from .forms import ReservationForm
from CollegeBook.settings import MEDIA_ROOT

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

            reservation = Reservation.objects.filter(email= form.cleaned_data['email'], representation_id= representation_id).last()
            # email = EmailMessage(
            #     'Reservation',
            #     'Vous avez reserver un Ticket pour la representation de %s pour la date du %s' % (
            #     reservation.representation.event.name, reservation.representation.date),
            #     'collegebooktest@gmail.com',
            #     ['%s' % form.cleaned_data['email']],
            #     headers={"Reply-To": 'collegebooktest@gmail.com'})

            # selected_seats = form.cleaned_data["selectedseat"]
            # selected_seats = selected_seats.split(",")
            # prefix_mail = reservation.email.split("@")[0].replace('.', ' ')
            # date = str(reservation.representation.date).split(' ')[0]
            # qr_path = MEDIA_ROOT / 'QR'
            # ticket_path = MEDIA_ROOT / 'Ticket'
            # pdf_path = os.path.join(ticket_path, f'{date}_{prefix_mail}_Tickets.pdf')
            # if not os.path.exists(ticket_path):
            #     os.mkdir(ticket_path)
            # if not os.path.exists(qr_path):
            #     os.mkdir(qr_path)
            # p = canvas.Canvas(pdf_path)
            #
            # for i in range(len(selected_seats)):
            #     y = 150
            #     x = 50
            #     d = i + 1
            #     data = 'https://www.youtube.com/%d' % d
            #     img = qrcode.make(data)
            #     ticket_name = f'{date}_{prefix_mail}_Ticket_Place_{selected_seats[i]}.png'
            #     img.save(qr_path / ticket_name)
            #     p.drawString(x, y, "Tickets place %s" % selected_seats[i])
            #     y = + 200
            #     p.drawImage(qr_path / ticket_name, 100, y, mask='auto')
            #     p.showPage()
            #
            # drink_number = int(form.cleaned_data["drink_number"])
            # if drink_number > 0:
            #     for i in range(drink_number):
            #         y = 150
            #         x = 50
            #         d = i + 1
            #         data = 'https://www.youtube.com/%d' % d
            #         img = qrcode.make(data)
            #         ticket_name = f'{date}_{prefix_mail}_Ticket_Boisson_n°{d}.png'
            #         img.save(qr_path / ticket_name)
            #         p.drawString(x, y, "Ticket Boisson")
            #         y = + 200
            #         p.drawImage(qr_path / ticket_name, 100, y, mask='auto')
            #         p.showPage()
            #
            # food_number = int(form.cleaned_data["food_number"])
            # if food_number > 0:
            #     for i in range(food_number):
            #         y = 150
            #         x = 50
            #         d = i + 1
            #         data = 'https://www.youtube.com/%d' % d
            #         img = qrcode.make(data)
            #         ticket_name = f'{date}_{prefix_mail}_Ticket_Nourriture_n°{d}.png'
            #         img.save(qr_path / ticket_name)
            #         p.drawString(x, y, "Ticket Nourriture")
            #         y = + 200
            #         p.drawImage(qr_path / ticket_name, 100, y, mask='auto')
            #         p.showPage()
            #
            # p.save()
            # email.attach_file(pdf_path)
            # email.send()
            # # email.attach_file('Tickets Nourriture n° %d.png' %d)
            return redirect('Payment:landing', reservation.id)

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