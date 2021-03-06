import requests
from flask import current_app

ACTIVITIES_PER_PAGE = 30


def list_activities(userAuth, pageNumber, lastUpdate=None):
    url = "https://www.strava.com/api/v3/athlete/activities"
    urlParams = "?page=" + str(pageNumber) + "&per_page=" \
        + str(ACTIVITIES_PER_PAGE)
    headers = {'Authorization': 'Bearer ' + userAuth.strava_auth_token}
    if lastUpdate:
        urlParams += "&after=" + str(lastUpdate)

    print("Activity List called with page number: " + str(pageNumber))
    return requests.get(url + urlParams, headers=headers).json()


def get_activity_by_id(userAuth, id):
    url = "https://www.strava.com/api/v3/activities/" + str(id)
    headers = {'Authorization': 'Bearer ' + userAuth.strava_auth_token}
    print("Run lookup called with: " + str(id))
    return requests.get(url, headers=headers).json()


def refresh_auth_token(userAuth):
    url = 'https://www.strava.com/api/v3/oauth/token'
    data = {'client_id': current_app.config['STRAVA_CLIENT_KEY'],
            'client_secret': current_app.config['STRAVA_CLIENT_SECRET_KEY'],
            'grant_type': 'refresh_token',
            'refresh_token': userAuth.strava_refresh_token}
    return requests.post(url, data=data).json()
