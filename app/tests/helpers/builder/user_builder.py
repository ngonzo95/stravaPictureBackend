from app.main.model.user import User
from app.tests.helpers.builder.basemap_builder import buildBasemap
import app.tests.helpers.util.random_utils as random_utils


def buildUser(*overridenValues):
    data = {
        "id": str(random_utils.randint(0, 1000)),
        "email": random_utils.randomString(13),
        "basemap": buildBasemap(),
        "is_admin": False
    }

    if not overridenValues:
        overridenValues = {}

    for (key, value) in overridenValues:
        data[key] = value

    return User(data)
