from app.main.model.marker import Marker
import app.tests.helpers.util.random_utils as random_utils


def buildMarker(*overridenValues):
    data = {
        "mapId": random_utils.randomString(10),
        "text":  random_utils.randomString(14),
        "cord": random_utils.randomCord()
    }

    if not overridenValues:
        overridenValues = {}

    for (key, value) in overridenValues:
        data[key] = value

    return Marker(data)
