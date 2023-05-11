import cv2
import qrcode
import stripe
from django import forms
from unidecode import unidecode

from CollegeBook.settings import MEDIA_ROOT
from Event.models import *
from Reservation.models import *
import os
import shutil

def check_password(form):
    password = form.cleaned_data.get('password')
    confirm_password = form.cleaned_data.get('confirm_password')
    if password != confirm_password:
        raise forms.ValidationError('La confirmation du mot de passe n\'est pas correcte')
def stripe_id_creation(product_type, event_name):
    stripe_id = product_type.lower() + ''.join([element.capitalize() for element in event_name.split(' ')])
    return stripe_id


def get_stripe_product_price(product_type, event_name):
    product = stripe.Product.retrieve(stripe_id_creation(product_type=product_type, event_name=event_name))
    return stripe.Price.retrieve(product["default_price"])["unit_amount"] / 100


def configCreator(config_name, json_url, user_id, seats):
    configuration = Config(name=config_name, url_json=json_url, user=user_id)
    configuration.save()
    for key in seats.keys():
        seat = Place(type=key, price=seats[key], configuration_id=configuration.id)
        seat.save()

def clean_tagify_string(data):
    tempList = data.replace("{", "").replace("}", "").replace("[", "").replace("]", "")
    tempList = tempList.replace('"value":', "").replace('"value":', "")
    tempList = tempList.split(",")
    for index, element in enumerate(tempList):
        if element[0] == " ":
            tempList[index] = element[1:]
        tempList[index] = tempList[index].replace('"', "")
    return tempList


def empty_folder(folder_path):
   
    # Vérifier si le dossier existe
    if os.path.exists(folder_path):
        # Parcourir tous les éléments dans le dossier
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Si l'élément est un dossier, appeler la fonction récursivement pour le vider
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            # Si l'élément est un fichier, le supprimer
            else:
                os.remove(file_path)
    else:
        print(f"Le dossier {folder_path} n'existe pas.")

def create_ticket_pdf(pdf, type_ticket, code, first_name, last_name, event_name, date):
    # pdf = canvas.Canvas('test.pdf')

    first_name = unidecode(first_name)
    last_name = unidecode(last_name)
    event_name = unidecode(event_name)

    qr_path = MEDIA_ROOT / 'QR'
    date_pdf = date + timedelta(hours=2)

    date_pdf = date_pdf.strftime("%d/%m/%Y %H:%M")
    date = str(date).split(' ')[0]

    y = 770
    x = 50

    data = 'http://localhost:8000/validation/scan_ticket/%s' % code
    img = qrcode.make(data)
    if type_ticket == "Nourriture" or type_ticket == "Boisson" or type_ticket == "Boisson":
        ticket_name = f'{date}_{first_name}_{last_name}_Ticket_{type_ticket}.png'
    else:
        ticket_name = f'{date}_{first_name}_{last_name}_Ticket_{type_ticket}.png'
    img.save(qr_path / ticket_name)
    print(f"{qr_path}/{ticket_name}")
    image = cv2.imread(f"{qr_path}/{ticket_name}")
    image_resize = cv2.resize(image, (300, 300))
    img_reshape = image_resize[30:270, 30:270]

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
    cv2.imwrite(f"{qr_path}/{ticket_name}", img_reshape)
    pdf.setFont("Helvetica", 16)

    if type_ticket == "Nourriture" or type_ticket == "Boisson" or type_ticket == "debout":
        pdf.drawString(165, 707, "Tickets %s" % type_ticket)
    else:
        pdf.drawString(165, 707, "Ticket place n°%s" % type_ticket)

    pdf.setFont("Helvetica", 17)
    pdf.setLineWidth(0.5)
    pdf.drawString(x, 780, "Evenement: %s" % event_name)
    pdf.drawString(x, 760, "Date: %s" % date_pdf)
    pdf.drawString(x, 740, "Reservation au nom de %s %s" % (first_name, last_name))
    pdf.setFont("Helvetica", 12)
    pdf.drawString(x, 390, "Contact: reservations@cspu.be")
    pdf.drawString(x, 375, "Adresse:  Avenue Coghen 205, 1180 Uccle")

    y = 460
    pdf.setLineWidth(2)
    pdf.rect(162, 457, 245, 245)
    pdf.drawImage(f"{qr_path}/{ticket_name}", 165, y, mask='auto')
    pdf.showPage()
    return (pdf)
def findRowId(char):
    alphabet = {'A': 0,'B': 1,'C': 2,'D': 3,'E': 4,
                'F': 5,'G': 6,'H': 7,'I': 8,'J': 9,
                'K': 10,'L': 11,'M': 12,'N': 13,'O': 14,
                'P': 15,'Q': 16,'R': 17,'S': 18,'T': 19,
                'U': 20,'V': 21,'W': 22,'X': 23,'Y': 24,
                'Z': 25
    }

    return alphabet[char]

def findJsonID(seatList,column):
    seatCounter = 0
    print("\n\n\n",seatList)
    for i in range(len(seatList)):
        if "seat" in seatList[i]:
            seatCounter += 1
            if seatCounter == column:
                return i