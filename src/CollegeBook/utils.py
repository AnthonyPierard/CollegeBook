from Configuration.models import Config, Place
import stripe


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