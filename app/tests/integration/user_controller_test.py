import pytest
from app.main import dynamo
from flask import current_app
from app.tests.helpers.test_app_builder import buildTestApp
from app.tests.helpers.builder.user_builder import buildUser
from botocore.exceptions import ClientError


usersForDbToDelete = []


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
    cleanupUsers(exceptionsToRaise)
    for e in exceptionsToRaise:
        print(e.response['Error']['Message'])

    if not exceptionsToRaise == []:
        raise Exception("Error while trying to delete items from db")

    ctx.pop()


def cleanupUsers(exceptions):
    tableName = current_app.config['TABLE_NAMES']['USER_TABLE']
    for user in usersForDbToDelete:
        try:
            dynamo.get_table(tableName).delete_item(
                Key={'id': user.id})
        except ClientError as e:
            exceptions.append(e)
