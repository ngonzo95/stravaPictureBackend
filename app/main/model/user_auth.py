class UserAuth():
    def __init__(self, *initial_data, **kwargs):
        self._availableKeys = ['id', 'strava_athlete_id', 'strava_username',
                               'strava_auth_token', 'strava_refresh_token',
                               'strava_expiration_time']

        for dictionary in initial_data:
            for key in dictionary:
                if key in self._availableKeys:
                    setattr(self, key, dictionary[key])
        for key in kwargs:
            if key in self._availableKeys:
                setattr(self, key, kwargs[key])

    def generateDict(self):
        d = {}
        for key in self._availableKeys:
            d[key] = getattr(self, key)
        return d

    def __eq__(self, other):
        for key in self._availableKeys:
            if not getattr(self, key) == getattr(other, key):
                return False
        return True
