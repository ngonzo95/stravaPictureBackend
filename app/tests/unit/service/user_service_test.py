from app.tests.helpers.builder.user_builder import buildUser
from flask import current_app
import pytest
from app.tests.helpers.test_app_builder import buildTestApp
from app.main import dynamo
import app.main.service.user_service as unit
from botocore.exceptions import ClientError
from app.tests.helpers.builder.marker_builder import buildMarker

usersForDbToDelete = []


def test_get_user_retieves_correct_user(test_client):
    generate_user()
    user = generate_user()

    assert user == unit.getUserById(user.id)


def test_update_marker_list_works_correctly(test_client):
    user = generate_user()
    markerlist = [buildMarker(), buildMarker(), buildMarker()]
    unit.update_marker_list(user.id, markerlist)
    user.basemap.markers = markerlist

    assert user == unit.getUserById(user.id)


def generate_user():
    user = buildUser()
    usersForDbToDelete.append(user)
    unit.createNewUser(user)
    return user


@pytest.fixture(scope='module')
def test_client():
    app = buildTestApp()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    tableName = current_app.config['TABLE_NAMES']['USER_TABLE']

    yield app.test_client()  # this is where the testing happens!

    # After
    exceptionsToRaise = []
    for user in usersForDbToDelete:
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
