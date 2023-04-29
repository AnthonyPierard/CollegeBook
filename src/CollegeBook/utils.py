def stripe_id_creation(place_type, event_name):
    stripe_id = place_type.lower() + ''.join([element.capitalize() for element in event_name.split(' ')])
    return stripe_id
