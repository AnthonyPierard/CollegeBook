from .models import Representation, Event
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Event, Representation
from Reservation.models import Reservation


def check_event_is_archived():
    print("TASK DONE")
    all_event_not_archived = Event.objects.filter(state='ACT')
    for current in all_event_not_archived:
        if Representation.objects.filter(event=current.id, date__gte=timezone.now()).count() == 0:
            current.state = 'ARC'
            current.save()

def send_remainders_mail():
    print("MAIL DONE")
    now = datetime.now()
    end_date = now + timedelta(days=3)
    representations = Representation.objects.filter(date__year = end_date.year, date__month = end_date.month, date__day = end_date.day)
    for representationIT in representations:
          reservations = Reservation.objects.filter(representation = representationIT)                   
          for reservation in reservations:
                reservation.email 
                mail_content = "N'oubliez pas ! La representation de %s est prévue le %s " %  (reservation.representation.event.name, reservation.representation.date)
                html = render_to_string('email.html', 
                                      { 'name' : "monsieur/madame %s" %reservation.last_name ,
                                      'email': reservation.email,
                                      'content' : mail_content,
                                      })
                send_mail('Reservation Ticket %s' %  reservation.representation.event.name,
                          'Vous avez reserver un Ticket pour la representation de %s' %  reservation.representation.event.name,
                          'collegebooktest@gmail.com',
                          ['%s' % reservation.email ]  ,
                          fail_silently=False,
                          html_message= html
                          )
                
def send_thanks_mail():
    print("MAIL THAKS DONE")
    now = datetime.now()
    end_date = now - timedelta(days = 1)
    representations = Representation.objects.filter(date__year = end_date.year, date__month = end_date.month, date__day = end_date.day)
    for representationIT in representations:
          reservations = Reservation.objects.filter(representation = representationIT)                   
          for reservation in reservations:
                mail_content = "Nous vous remerciont chaleureusement d'avoir été présent à la representation de %s,  le %s " %  (reservation.representation.event.name, reservation.representation.date)
                html = render_to_string('email.html', 
                                      { 'name' : "monsieur/madame %s" %reservation.last_name ,
                                      'email': reservation.email,
                                      'content' : mail_content,
                                      })
                send_mail('Reservation Ticket %s' %  reservation.representation.event.name,
                          'Vous avez reserver un Ticket pour la representation de %s' %  reservation.representation.event.name,
                          'collegebooktest@gmail.com',
                          ['%s' % reservation.email ]  ,
                          fail_silently=False,
                          html_message= html
                          )
     

