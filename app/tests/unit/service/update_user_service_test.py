from flask import current_app
import pytest
from app.tests.helpers.test_app_builder import buildTestApp
from app.main import dynamo
from botocore.exceptions import ClientError
import app.main.service.update_user_service as unit
import app.main.service.user_auth_service as user_auth_service
from app.tests.helpers.builder.user_auth_builder import buildUserAuth
import app.tests.helpers.util.mock_strava_responses as strava_api
from app.tests.helpers.builder.run_builder import buildRun
import app.tests.helpers.util.random_utils as random_utils
import requests_mock
import app.main.service.run_service as run_service
from boto3.dynamodb.conditions import Key

userAuthsForDbToDelete = []
runsForDbToDelete = []


def test_update_user_inserts_runs_into_db(test_client):
    userAuth = generateUserAuth()
    runIds = []
    for i in range(10):
        id = random_utils.randint(0, 10000)
        run = buildRun(overridenValues={'id': str(id), 'userId': userAuth.id})
        runsForDbToDelete.append(run)
        runIds.append(id)

    with requests_mock.Mocker() as m:
        strava_api.generate_mock_strava_api(runIds, 30, m)
        unit.updateUser(userAuth.id)

    dbResponse = run_service.runTable().query(
        KeyConditionExpression=Key('userId').eq(userAuth.id)
    )

    assert len(dbResponse['Items']) == 10

# Test for page stoping but commented out to decrease load on db
# def test_update_user_only_inserts_runs_up_to_max_into_db(test_client):
#     userAuth = generateUserAuth()
#     runIds = []
#     for i in range(40):
#         id = random_utils.randint(0, 10000)
#         run = buildRun(overridenValues={'id': str(id), 'userId': userAuth.id})
#         runsForDbToDelete.append(run)
#         runIds.append(id)
#
#     with requests_mock.Mocker() as m:
#         strava_api.generate_mock_strava_api(runIds, 0, m)
#         unit.MAX_RUNS_TO_COLLECT = 10
#         unit.updateUser(userAuth.id)
#
#     dbResponse = run_service.runTable().query(
#         KeyConditionExpression=Key('userId').eq(userAuth.id)
#     )
#
#     assert len(dbResponse['Items']) == 30


def generateUserAuth():
    userAuth = buildUserAuth()
    userAuthsForDbToDelete.append(userAuth)
    user_auth_service.createUserAuth(userAuth)
    return userAuth


@pytest.fixture(scope='module')
def test_client():
    app = buildTestApp()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    yield app.test_client()  # this is where the testing happens!

    # After
    unit.MAX_RUNS_TO_COLLECT = 30
    exceptionsToRaise = []
    cleanupUserAuth(exceptionsToRaise)
    cleanUpRuns(exceptionsToRaise)

    for e in exceptionsToRaise:
        print(e.response['Error']['Message'])

    if not exceptionsToRaise == []:
        raise Exception("Error while trying to delete items from db")

    ctx.pop()


def cleanupUserAuth(exceptions):
    tableName = current_app.config['TABLE_NAMES']['USER_AUTH_TABLE']
    for userAuth in userAuthsForDbToDelete:
        try:
            dynamo.get_table(tableName).delete_item(
                Key={'id': userAuth.id})
        except ClientError as e:
            exceptions.append(e)


def cleanUpRuns(exceptions):
    tableName = current_app.config['TABLE_NAMES']['RUN_TABLE']
    for run in runsForDbToDelete:
        try:
            dynamo.get_table(tableName).delete_item(
                Key={'id': run.id, 'userId': run.userId})
        except ClientError as e:
            exceptions.append(e)
