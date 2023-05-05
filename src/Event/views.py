from datetime import datetime
import stripe

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from Account.models import User
from Configuration.models import Place
from .forms import EventForm, UpdateDateEventForm, ConfirmForm
from django.utils import timezone
from CollegeBook.utils import stripe_id_creation, get_stripe_product_price
from Event.models import Event, Representation, Config, CodePromo, Price
from Configuration.views import add_default_configuration
from pathlib import Path


def events_display(request):
    all_event = Event.objects.filter(state='ACT')
    return render(request, 'events_display.html', {'all_event': all_event})


def event_details(request, even_id):
    event = Event.objects.get(pk=even_id)
    if event.state != 'ACT':
        return redirect('Event:display')

    representations = Representation.objects.filter(date__gte=datetime.now(), event=event.id)
    return render(request, 'event_details.html', {"event": event, "representations": representations})


@login_required
def event_creation(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('Account:events', request.user.id)
            except ValueError as error:

                return render(request, 'error.html', {'error': error})
        configurations = Config.objects.filter(user=request.user.id)
        return render(request, 'event_creation.html', {'form': form, 'configurations': configurations})

    else:
        form = EventForm()
        if not (Config.objects.filter(user=request.user)):
            add_default_configuration(request.user)
        configurations = Config.objects.filter(user=request.user.id)
        return render(request, 'event_creation.html', {'form': form, 'configurations': configurations})


@login_required
def delete_representation(request, representation_id):
    representation = Representation.objects.get(pk=representation_id)
    if representation.date <= timezone.now():
        return redirect('Account:events', request.user.id)
    if request.method == 'POST':

        form = ConfirmForm(request.POST)

        if form.is_valid():
            choice = form.cleaned_data['choice']
            if choice == "1":
                Representation.objects.filter(pk=representation_id).delete()
                # TODO avertir les personnes qui ont réserver via un mail.
        return redirect('Account:events', request.user.id)
    else:
        form = ConfirmForm()
        event = Representation.objects.get(pk=representation_id)
        return render(request, 'delete_representation.html', {"form": form, "event": event})


@login_required
def event_update(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(pk=event_id)
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event.user.clear()
            Representation.objects.filter(event_id=event.id).delete()
            CodePromo.objects.filter(event_id=event.id).delete()
            Price.objects.filter(event_id=event.id).delete()

            form.save()

        return redirect('Event:display')
    else:
        event = Event.objects.get(pk=event_id)
        representations = Representation.objects.filter(event_id=event.id)
        dates = ""
        for representation in representations:
            dates += representation.date.strftime("%d-%m-%Y/%H:%M, ")
        if dates[-2] == "," and dates[-1] == " ":
            dates = dates[:-2]
        # drink_price = get_stripe_product_price(product_type="boisson", event_name=event.name)
        # food_price = get_stripe_product_price(product_type="nourriture", event_name=event.name)
        drink_price = Price.objects.get(type="Boisson", event_id=event.id).price
        food_price = Price.objects.get(type="Nourriture", event_id=event.id).price
        codes = CodePromo.objects.filter(event_id=event.id)
        promo_codes = ""
        for code in codes:
            promo_codes += str(code) + ","
        if promo_codes:
            if promo_codes[-1] == ",":
                promo_codes = promo_codes[:-1]


        form = EventForm(instance=event, initial={"date": dates, "drink_price": drink_price, "food_price": food_price, "promo_codes":promo_codes})
        return render(request, 'event_modification.html', {"form": form, "event": event})


@login_required()
def publish_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.state = 'ACT'
    event.save()

    # Create stripe products
    drink_price = Price.objects.get(type="Boisson", event_id=event.id).price
    stripe.Product.create(
        name="Ticket boisson" + " [" + event.name + "]",
        default_price_data={
            'unit_amount': int(drink_price * 100),
            'currency': 'eur'
        },
        id=stripe_id_creation("boisson", event.name)
    )

    food_price = Price.objects.get(type="Nourriture", event_id=event.id).price
    stripe.Product.create(
        name="Ticket nourriture" + " [" + event.name + "]",
        default_price_data={
            'unit_amount': int(food_price * 100),
            'currency': 'eur'
        },
        id=stripe_id_creation("nourriture", event.name)
    )

    configuration = Config.objects.get(name=event.configuration)
    places = Place.objects.filter(configuration_id=configuration.id)
    for place in places:
        stripe.Product.create(
            name="Siège " + place.type.capitalize() + " [" + event.name + "]",
            default_price_data={
                'unit_amount': int(float(place.price) * 100),
                'currency': 'eur'
            },
            id=stripe_id_creation(place.type, event.name)
        )

    # Create 1 room per representation
    event_representations = Representation.objects.filter(event_id=event.id)
    path = Path(__file__).resolve().parent
    srcPath = path.parent
    src_file = srcPath.joinpath("Configuration" + configuration.url_json)
    if not path.joinpath("static/json/" + event.name).exists():
        path.joinpath("static/json/" + event.name).mkdir(parents=True, exist_ok=True)
    for represent in event_representations:
        dst_file = path / "static" / "json" / event.name / str(represent.id)
        dst_file = dst_file.with_suffix(".json")
        with open(src_file, "rb") as source_file:
            with open(dst_file, "wb") as destination_file:
                destination_file.write(source_file.read())

    promotions = CodePromo.objects.filter(event_id=event.id)
    applies_to = applies_to = [str(stripe_id_creation(element.type, event.name)) for element in
                  list(Price.objects.filter(event_id=event.id)) + list(
                      Place.objects.filter(configuration_id=event.configuration_id))]

    print(applies_to)

    for promotion in promotions:
        coupon_id = stripe_id_creation(promotion.code, event.name)
        coupon_name = f"Bon {promotion.code} [{event.name}]"
        if promotion.percentage:
            stripe.Coupon.create(
                id=coupon_id,
                name=coupon_name,
                percent_off=promotion.percentage,
                duration="forever",
                applies_to= {"products": applies_to}
            )
        if promotion.amount:
            stripe.Coupon.create(
                id=coupon_id,
                name=coupon_name,
                amount_off=int(promotion.amount * 100),
                currency="eur",
                duration="forever",
                applies_to={"products": applies_to}
            )
        stripe.PromotionCode.create(coupon=coupon_id, code=promotion.code.upper())
    return redirect('Account:events', request.user.id)


@login_required()
def delete_event_draft(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.state == 'DRF':
        Representation.objects.filter(event=event_id).delete()
        event.delete()
    return redirect('Account:events', request.user.id)
