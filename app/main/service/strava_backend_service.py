import requests


def list_activities(userAuth, pageNumber, lastUpdate=None):
    url = "https://www.strava.com/api/v3/athlete/activities"
    urlParams = "?page=" + str(pageNumber) + "&per_page=30"
    headers = {'Authorization': userAuth.strava_auth_token}
    if lastUpdate:
        urlParams += "&after=" + str(lastUpdate)

    return requests.post(url+urlParams, headers=headers).json()
