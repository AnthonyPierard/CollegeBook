from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models import Q

from Reservation.models import Reservation
from .models import Event, Representation


def check_rep_is_archived():
    print("TASK DONE REP")
    all_rep_active = Representation.objects.filter(state='ACT')
    for rep in all_rep_active:
        if rep.date <= timezone.now():
            rep.state = 'ARC'
            rep.save()



def check_event_is_archived():
    print("TASK DONE EVENT")
    all_event_not_archived = Event.objects.filter(state='ACT')
    for current in all_event_not_archived:
        if Representation.objects.filter(~Q(state='ARC'), event=current.id).count() == 0:
            current.state = 'ARC'
            current.save()


def send_remainders_mail():
    print("MAIL DONE")
    now = datetime.now()
    end_date = now + timedelta(days=3)
    representations = Representation.objects.filter(date__year=end_date.year, date__month=end_date.month,
                                                    date__day=end_date.day)
    for representationIT in representations:
        reservations = Reservation.objects.filter(representation=representationIT)
        for reservation in reservations:
            reservation.email
            date_pdf = reservation.representation.date + timedelta(hours=2)
            date_pdf = date_pdf.strftime("%d/%m/%Y %H:%M")
            mail_content = "N'oubliez pas ! La representation de %s est prévue le %s " % (
            reservation.representation.event.name, date_pdf)
            html = render_to_string('email.html',
                                    {'name': "monsieur/madame %s" % reservation.last_name,
                                     'email': reservation.email,
                                     'content': mail_content,
                                     })
            send_mail('Reservation Ticket %s' % reservation.representation.event.name,
                      'Vous avez reserver un Ticket pour la representation de %s' % reservation.representation.event.name,
                      'collegebooktest@gmail.com',
                      ['%s' % reservation.email],
                      fail_silently=False,
                      html_message=html
                      )


def send_thanks_mail():
    print("MAIL THAKS DONE")
    now = datetime.now()
    end_date = now - timedelta(days=1)
    representations = Representation.objects.filter(date__year=end_date.year, date__month=end_date.month,
                                                    date__day=end_date.day)
    for representationIT in representations:
        reservations = Reservation.objects.filter(representation=representationIT)
        for reservation in reservations:
            date_pdf = reservation.representation.date + timedelta(hours=2)
            date_pdf = date_pdf.strftime("%d/%m/%Y %H:%M")
            mail_content = "Nous vous remerciont chaleureusement d'avoir été présent à la representation de %s,  le %s " % (
            reservation.representation.event.name, date_pdf)
            html = render_to_string('email.html',
                                    {'name': "monsieur/madame %s" % reservation.last_name,
                                     'email': reservation.email,
                                     'content': mail_content,
                                     })
            send_mail('Reservation Ticket %s' % reservation.representation.event.name,
                      'Vous avez reserver un Ticket pour la representation de %s' % reservation.representation.event.name,
                      'collegebooktest@gmail.com',
                      ['%s' % reservation.email],
                      fail_silently=False,
                      html_message=html
                      )
