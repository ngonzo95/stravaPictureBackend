import app.main.service.strava_backend_service as unit
import app.tests.helpers.util.random_utils as random_utils
from app.tests.helpers.builder.user_auth_builder import buildUserAuth
import requests_mock
import json
from app.tests.helpers.test_app_builder import buildTestApp
import pytest


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


def test_refresh_token(test_client):
    userAuth = buildUserAuth()
    strava_client_id = 'TESTCLIENTID'
    strava_client_secret = 'TESTSECRET'

    strava_response = {'token_type': 'Bearer',
                       'access_token': random_utils.randomString(10),
                       'expires_at': random_utils.randint(0, 10000),
                       'expires_in': random_utils.randint(0, 100),
                       'refresh_token': random_utils.randomString(10)}
    expectedPostBody = {'client_id': strava_client_id,
                        'client_secret': strava_client_secret,
                        'grant_type': 'refresh_token',
                        'refresh_token': userAuth.strava_refresh_token}

    with requests_mock.Mocker() as m:
        stravaUrl = 'https://www.strava.com/api/v3/oauth/token'
        adapter = m.post(stravaUrl, text=json.dumps(strava_response))

        assert unit.refresh_auth_token(userAuth) == strava_response
        adapter.call_count == 1
        assert "client_id=" + expectedPostBody['client_id'] in adapter.last_request.text
        assert "client_secret=" + expectedPostBody['client_secret'] in adapter.last_request.text
        assert "grant_type=" + expectedPostBody['grant_type'] in adapter.last_request.text
        assert "refresh_token=" + expectedPostBody['refresh_token'] in adapter.last_request.text


@pytest.fixture(scope='module')
def test_client():
    app = buildTestApp()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield app.test_client()  # this is where the testing happens!

    # After
    ctx.pop()
