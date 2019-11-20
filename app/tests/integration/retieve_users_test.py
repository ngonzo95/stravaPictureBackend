import pytest
from app.main import dynamo
from flask import current_app
from app.tests.helpers.test_app_builder import buildTestApp
from app.tests.helpers.builder.user_auth_builder import buildUserAuth
from app.tests.helpers.builder.user_builder import buildUser
from app.main.model.user_auth import UserAuth
from app.main.model.user import User
import requests_mock
import json
from botocore.exceptions import ClientError
from decimal import Decimal

usersAuthForDbToDelete = []
usersForDbToDelete = []


def test_when_user_signs_in_redirects_to_strava_auth(test_client):
    userId = "35324d"
    response = test_client.get(
        'user/' + userId + '/auth/get_strava_token', follow_redirects=False)
    url = "http://www.strava.com/oauth/authorize?client_id=" \
        + current_app.config['STRAVA_CLIENT_KEY'] \
        + "&response_type=code&redirect_uri=" \
        + "http://testurl/user/" + userId + "/auth/"\
        + "exchange_token&approval_prompt=force&scope=read,activity:read"

    # check that the path changed
    assert response.status_code == 302
    assert response.location == url

    # assert request.path == url_for(url)


def test_exchange_token_calls_strava_api_and_sets_token(test_client):
    userAuth = buildUserAuth()
    usersAuthForDbToDelete.append(userAuth)

    strava_response = {"token_type": "Bearer",
                       "expires_at": userAuth.strava_expiration_time,
                       "expires_in": 21600,
                       "refresh_token": userAuth.strava_refresh_token,
                       "access_token": userAuth.strava_auth_token,
                       "athlete": {"id": userAuth.strava_athlete_id,
                                   "username": userAuth.strava_username,
                                   "resource_state": 2}}

    with requests_mock.Mocker() as m:
        athleteCode = "asdfasdfds"
        stravaUrl = 'https://www.strava.com/oauth/token'
        stravaUrlParmas = '?client_id=TESTCLIENTID&client_secret=TESTSECRET' \
            + '&code=' + athleteCode + '&grant_type=authorization_code'
        m.post(stravaUrl + stravaUrlParmas, text=json.dumps(strava_response))

        reqUrl = 'user/' + userAuth.id + '/auth/exchange_token?state=&code=' \
            + athleteCode + '&scope=read,activity:read'

        response = test_client.get(reqUrl)
        assert response.status_code == 200

        tableName = current_app.config['TABLE_NAMES']['USER_AUTH_TABLE']
        dbRes = dynamo.get_table(tableName).get_item(Key={'id': userAuth.id})
        userAuth = UserAuth(dbRes['Item'])
        assert userAuth == UserAuth(dbRes['Item'])


def test_exchange_token_with_bad_scope_returns_error(test_client):
    userAuth = buildUserAuth()
    usersAuthForDbToDelete.append(userAuth)

    with requests_mock.Mocker() as m:
        athleteCode = "asdfasdfds"
        stravaUrl = 'https://www.strava.com/oauth/token'
        stravaUrlParmas = '?client_id=TESTCLIENTID&client_secret=TESTSECRET' \
            + '&code=' + athleteCode + '&grant_type=authorization_code'
        m.post(stravaUrl + stravaUrlParmas, text="{}")

        reqUrl = 'user/' + userAuth.id + '/auth/exchange_token?state=&code=' \
            + athleteCode + '&scope=read'

        response = test_client.get(reqUrl)
        assert response.status_code == 401

        tableName = current_app.config['TABLE_NAMES']['USER_AUTH_TABLE']
        dbRes = dynamo.get_table(tableName).get_item(Key={'id': userAuth.id})
        assert 'Item' not in dbRes


def test_retieve_user_gets_the_desired_user(test_client):
    # arrange
    user = generate_user()

    # act
    response = test_client.get('/user/' + user.id)

    # assert
    assert response.status_code == 200
    # asserting indivual things about responses because decimals are a pain
    assert response.json['email'] == user.email
    assert response.json['id'] == user.id
    assert response.json['basemap']['zoom'] == user.basemap.zoom
    assert response.json['basemap']['markers'][0]['mapId'] \
        == user.basemap.markers[0].mapId


def generate_auth_user():
    user = buildUserAuth()
    usersAuthForDbToDelete.append(user)

    tableName = current_app.config['TABLE_NAMES']['USER_AUTH_TABLE']
    dynamo.get_table(tableName).put_item(
        Item=user.generateDict())
    return user


def generate_user():
    user = buildUser()
    usersForDbToDelete.append(user)

    tableName = current_app.config['TABLE_NAMES']['USER_TABLE']
    dynamo.get_table(tableName).put_item(
        Item=user.generateDict())
    return user


@pytest.fixture(scope='module')
def test_client():
    app = buildTestApp()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield app.test_client()  # this is where the testing happens!

    # After
    exceptionsToRaise = []
    cleanupUserAuths(exceptionsToRaise)
    cleanupUsers(exceptionsToRaise)
    for e in exceptionsToRaise:
        print(e.response['Error']['Message'])

    if not exceptionsToRaise == []:
        raise Exception("Error while trying to delete items from db")

    ctx.pop()


def cleanupUserAuths(exceptions):
    tableName = current_app.config['TABLE_NAMES']['USER_AUTH_TABLE']
    for user in usersAuthForDbToDelete:
        try:
            dynamo.get_table(tableName).delete_item(
                Key={'id': user.id})
        except ClientError as e:
            exceptions.append(e)


def cleanupUsers(exceptions):
    tableName = current_app.config['TABLE_NAMES']['USER_TABLE']
    for user in usersForDbToDelete:
        try:
            dynamo.get_table(tableName).delete_item(
                Key={'id': user.id})
        except ClientError as e:
            exceptions.append(e)
