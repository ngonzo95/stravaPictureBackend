import pytest
from app.main.controller.user_auth_controller import api as user_ns
from app.main import dynamo
from flask import current_app
from app.tests.helpers.test_app_builder import buildTestApp
from app.tests.helpers.builder.user_auth_builder import buildUserAuth


def test_example(test_client):
    tableName = current_app.config['TABLE_NAMES']['USER_AUTH_TABLE']
    user = buildUserAuth()

    dynamo.get_table(tableName).put_item(
        Item=user.generateDict())

    response = test_client.get('/user/')
    assert response.status_code == 200
    expected = {'data':
                [{'id': user.id,
                  'strava_athlete_id': user.strava_athlete_id,
                  'strava_expiration_time': user.strava_expiration_time,
                  'strava_username': user.strava_username}]}
    assert response.json == expected

    dynamo.get_table(tableName).delete_item(
        Key={'id': user.id})


@pytest.fixture(scope='module')
def test_client():
    app = buildTestApp([(user_ns, "/user")])

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    yield app.test_client()  # this is where the testing happens!
    ctx.pop()
