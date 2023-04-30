from Configuration.models import Config, Place
from reportlab.pdfgen import canvas
import qrcode
import cv2
from Reservation.models import *
from Event.models import *

def stripe_id_creation(place_type, event_name):
    stripe_id = place_type.lower() + ''.join([element.capitalize() for element in event_name.split(' ')])
    return stripe_id

def configCreator(config_name, json_url, user_id, seats):
    configuration = Config(name=config_name, url_json=json_url, user=user_id)
    configuration.save()
    for key in seats.keys():
        seat = Place(type=key, price=seats[key], configuration_id=configuration.id)
        seat.save()




def create_ticket_pdf(pdf, type_ticket, code, first_name, last_name, event_name, date):
    #pdf = canvas.Canvas('test.pdf')

    y = 770
    x = 50

    data = 'https://www.youtube.com/%s' % code
    img = qrcode.make(data)
    img.save('t.png')
    imgage = cv2.imread('t.png')
    image_resize =cv2.resize(imgage,(300,300))
    img_reshape = image_resize[30:270,30:270]

    y = 770
    x = 50

    

    pdf.setFillColorRGB(0.85, 0.85, 0.85)
    # Dessiner un rectangle qui couvre toute la page pour définir le fond
    pdf.rect(40, 365, 520, 435, fill=True, stroke=False)
    pdf.setLineWidth(4)
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setLineWidth(4)
    pdf.rect(38, 363, 524, 439)
    pdf.setFillColorRGB(0, 0, 0)
    cv2.imwrite('./t.png',img_reshape)
    pdf.setFont("Helvetica", 16)
    
    if type_ticket ==  "Nourriture" or type_ticket == "Boisson":
        pdf.drawString(165, 707, "Tickets %s" % type_ticket)
    else: 
        pdf.drawString(165, 707, "Ticket place n°%s" % type_ticket)

    pdf.setFont("Helvetica", 17)
    pdf.setLineWidth(0.5)
    pdf.drawString(x, 780, "Evenement: %s" % event_name)
    pdf.drawString(x, 760, "Date: %s" % date) 
    pdf.drawString(x, 740, "Reservation au nom de %s %s" % (first_name, last_name))
    pdf.setFont("Helvetica", 12)
    pdf.drawString(x, 390, "Contact: ladancedescanard@gmail.com")
    pdf.drawString(x, 375, "Adresse: College Saint-Pierre à uccle")

    y = 460
    pdf.setLineWidth(2)
    pdf.rect(163, 458, 244, 244)
    pdf.drawImage('t.png', 165, y, mask='auto')
    pdf.showPage()
    print("ok")
    return(pdf)