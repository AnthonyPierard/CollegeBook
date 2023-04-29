from Configuration.models import Config, Place


def stripe_id_creation(place_type, event_name):
    stripe_id = place_type.lower() + ''.join([element.capitalize() for element in event_name.split(' ')])
    return stripe_id

def configCreator(config_name, json_url, user_id, seats):
    configuration = Config(name=config_name, url_json=json_url, user=user_id)
    configuration.save()
    for key in seats.keys():
        seat = Place(type=key, price=seats[key], configuration_id=configuration.id)
        seat.save()