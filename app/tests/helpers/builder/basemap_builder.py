from app.main.model.basemap import Basemap
from app.tests.helpers.builder.marker_builder import buildMarker
import random
import string


def buildBasemap(*overridenValues):
    data = {
        "center": 3,
        "cord": [39.8333, -98.58333],
        "markers": []
    }

    for i in range(random.randint(1, 5)):
        data["markers"].append(buildMarker())

    if not overridenValues:
        overridenValues = {}

    for (key, value) in overridenValues:
        data[key] = value

    return Basemap(data)


def randomString(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
