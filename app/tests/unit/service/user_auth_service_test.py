from app.tests.helpers.builder.user_auth_builder import buildUserAuth
from flask import current_app
import pytest
from app.tests.helpers.test_app_builder import buildTestApp
from app.main import dynamo
import app.main.service.user_auth_service as unit
from botocore.exceptions import ClientError

userAuthsForDbToDelete = []


def test_get_user_auth_retieves_correct_user_auth(test_client):
    generate_user_auth()
    userAuth = generate_user_auth()

    assert userAuth == unit.getUserAuthById(userAuth.id)


def generate_user_auth():
    userAuth = buildUserAuth()
    userAuthsForDbToDelete.append(userAuth)
    unit.createUserAuth(userAuth)
    return userAuth


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
