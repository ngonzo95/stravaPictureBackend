from app.main.model.basemap import Basemap
from app.tests.helpers.builder.marker_builder import buildMarker
import app.tests.helpers.util.random_utils as random_utils


def buildBasemap(*overridenValues):
    data = {
        "zoom": random_utils.randint(1, 12),
        "center": random_utils.randomCord(),
        "markers": []
    }

    for i in range(random_utils.randint(1, 5)):
        data["markers"].append(buildMarker())

    if not overridenValues:
        overridenValues = {}

    for (key, value) in overridenValues:
        data[key] = value

    return Basemap(data)
