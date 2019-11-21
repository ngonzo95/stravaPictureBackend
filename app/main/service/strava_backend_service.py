import requests


def list_activities(userAuth, pageNumber, lastUpdate=None):
    url = "https://www.strava.com/api/v3/athlete/activities"
    urlParams = "?page=" + str(pageNumber) + "&per_page=30"
    headers = {'Authorization': 'Bearer ' + userAuth.strava_auth_token}
    if lastUpdate:
        urlParams += "&after=" + str(lastUpdate)

    return requests.get(url+urlParams, headers=headers).json()


def get_activity_by_id(userAuth, id):
    url = "https://www.strava.com/api/v3/activities/" + str(id)
    headers = {'Authorization': 'Bearer ' + userAuth.strava_auth_token}
    return requests.get(url, headers=headers).json()
