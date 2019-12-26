from app.main.model.user_auth import UserAuth
import random
import string


def buildUserAuth(overridenValues={}):
    data = {'id': randomString(10),
            'strava_athlete_id': randomString(12),
            'strava_username': randomString(6),
            'strava_auth_token': randomString(12),
            'strava_refresh_token': randomString(12),
            'strava_expiration_time': 10}

    if not overridenValues:
        overridenValues = {}

    for (key, value) in overridenValues.items():
        data[key] = value

    return UserAuth(data)


def randomString(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
