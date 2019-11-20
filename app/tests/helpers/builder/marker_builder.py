from app.main.model.marker import Marker
import random
import string


def buildMarker(*overridenValues):
    data = {
        "mapId": randomString(10),
        "text":  randomString(14),
        "cord": [random.random()*360-180, random.random()*360-180]
    }

    if not overridenValues:
        overridenValues = {}

    for (key, value) in overridenValues:
        data[key] = value

    return Marker(data)


def randomString(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
