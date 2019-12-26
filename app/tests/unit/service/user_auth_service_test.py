from app.tests.helpers.builder.user_auth_builder import buildUserAuth
from flask import current_app
import pytest
from app.tests.helpers.test_app_builder import buildTestApp
from app.main import dynamo
import app.main.service.user_auth_service as unit
from botocore.exceptions import ClientError
import app.tests.helpers.util.random_utils as random_utils
import json
import requests_mock
from decimal import Decimal
import time

userAuthsForDbToDelete = []


def test_get_user_auth_retieves_correct_user_auth(test_client):
    generate_user_auth()
    userAuth = generate_user_auth()

    assert userAuth == unit.getUserAuthById(userAuth.id)


def generate_user_auth(init_value={}):
    userAuth = buildUserAuth(overridenValues=init_value)
    userAuthsForDbToDelete.append(userAuth)
    unit.createUserAuth(userAuth)
    return userAuth


def test_get_updated_user_auth_when_expired_updates(test_client):
    userAuth = generate_user_auth(
        {'strava_expiration_time': int(time.time()) - 1000})

    strava_response = {'token_type': 'Bearer',
                       'access_token': random_utils.randomString(10),
                       'expires_at': random_utils.randint(0, 10000),
                       'expires_in': random_utils.randint(0, 100),
                       'refresh_token': random_utils.randomString(10)}

    with requests_mock.Mocker() as m:
        stravaUrl = 'https://www.strava.com/api/v3/oauth/token'
        m.post(stravaUrl, text=json.dumps(strava_response))
        unit.getUpdatedUserAuth(userAuth.id)
        # ensure that it have been saved to the db.
        updatedUser = unit.getUserAuthById(userAuth.id)
        assert updatedUser.strava_expiration_time == Decimal(
            strava_response['expires_at'])
        assert updatedUser.strava_refresh_token == strava_response['refresh_token']
        assert updatedUser.strava_auth_token == strava_response['access_token']


def test_get_updated_user_auth_when_valid_does_nothing():
    userAuth = generate_user_auth(
        {'strava_expiration_time': int(time.time()) + 1000})
    strava_response = {'token_type': 'Bearer',
                       'access_token': random_utils.randomString(10),
                       'expires_at': random_utils.randint(0, 10000),
                       'expires_in': random_utils.randint(0, 100),
                       'refresh_token': random_utils.randomString(10)}
    with requests_mock.Mocker() as m:
        stravaUrl = 'https://www.strava.com/api/v3/oauth/token'
        adapter = m.post(stravaUrl, text=json.dumps(strava_response))
        newUserAuth = unit.getUpdatedUserAuth(userAuth.id)
        assert userAuth.strava_auth_token == newUserAuth.strava_auth_token
        assert adapter.call_count == 0


@pytest.fixture(scope='module')
def test_client():
    app = buildTestApp()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    tableName = current_app.config['TABLE_NAMES']['USER_AUTH_TABLE']

    yield app.test_client()  # this is where the testing happens!

    # After
    exceptionsToRaise = []
    for user in userAuthsForDbToDelete:
        try:
            dynamo.get_table(tableName).delete_item(
                Key={'id': user.id})
        except ClientError as e:
            exceptionsToRaise.append(e)

    for e in exceptionsToRaise:
        print(e.response['Error']['Message'])

    if not exceptionsToRaise == []:
        raise Exception("Error while trying to delete items from db")

    ctx.pop()
