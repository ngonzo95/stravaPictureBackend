import app.main.service.strava_backend_service as unit
import app.tests.helpers.util.random_utils as random_utils
from app.tests.helpers.builder.user_auth_builder import buildUserAuth
import requests_mock
import json


def test_list_activities_passes_in_required_header_and_reqest():

    userAuth = buildUserAuth()
    strava_response = []
    for i in range(5):
        strava_response.append({'fakedata': random_utils.randomString(6)})

    with requests_mock.Mocker() as m:
        stravaUrl = 'https://www.strava.com/api/v3/athlete/activities'
        stravaUrlParmas = '?page=1&per_page=30'
        headers = {'Authorization': 'Bearer ' + userAuth.strava_auth_token}
        m.get(stravaUrl + stravaUrlParmas,
              text=json.dumps(strava_response), request_headers=headers)

        assert unit.list_activities(userAuth, 1) == strava_response


def test_list_activities_from_specific_page():

    userAuth = buildUserAuth()
    strava_response = []
    for i in range(5):
        strava_response.append({'fakedata': random_utils.randomString(6)})

    with requests_mock.Mocker() as m:
        stravaUrl = 'https://www.strava.com/api/v3/athlete/activities'
        stravaUrlParmas = '?page=3&per_page=30'
        headers = {'Authorization': 'Bearer ' + userAuth.strava_auth_token}
        m.get(stravaUrl + stravaUrlParmas,
              text=json.dumps(strava_response), request_headers=headers)

        assert unit.list_activities(userAuth, 3) == strava_response


def test_list_activities_with_after_time():

    userAuth = buildUserAuth()
    strava_response = []
    for i in range(5):
        strava_response.append({'fakedata': random_utils.randomString(6)})

    with requests_mock.Mocker() as m:
        stravaUrl = 'https://www.strava.com/api/v3/athlete/activities'
        stravaUrlParmas = '?page=3&per_page=30&after=2314'
        headers = {'Authorization': 'Bearer ' + userAuth.strava_auth_token}
        m.get(stravaUrl + stravaUrlParmas,
              text=json.dumps(strava_response), request_headers=headers)

        assert unit.list_activities(
            userAuth, 3, lastUpdate=2314) == strava_response


def test_get_activity_by_id():
    userAuth = buildUserAuth()
    activityId = random_utils.randint(0, 100)
    strava_response = {'fakedata': random_utils.randomString(6)}

    with requests_mock.Mocker() as m:
        stravaUrl = 'https://www.strava.com/api/v3/activities/' \
                    + str(activityId)
        headers = {'Authorization': 'Bearer ' + userAuth.strava_auth_token}
        print(stravaUrl)
        m.get(stravaUrl,
              text=json.dumps(strava_response), request_headers=headers)

        assert unit.get_activity_by_id(userAuth, activityId) == strava_response
