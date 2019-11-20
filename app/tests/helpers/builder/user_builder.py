from app.main.model.user import User
from app.tests.helpers.builder.basemap_builder import buildBasemap
import random
import string


def buildUser(*overridenValues):
    data = {
        "id": random.randint(0, 1000),
        "email": randomString(13),
        "basemap": buildBasemap(),
        "is_admin": False
    }

    if not overridenValues:
        overridenValues = {}

    for (key, value) in overridenValues:
        data[key] = value

    return User(data)


def randomString(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
