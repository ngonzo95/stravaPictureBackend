from app.tests.helpers.builder.run_map_builder import buildRunMap
from flask import current_app
import pytest
from app.tests.helpers.test_app_builder import buildTestApp
from app.main import dynamo
import app.main.service.run_map_service as unit
from botocore.exceptions import ClientError
import app.tests.helpers.util.random_utils as random_utils

runMapForDbToDelete = []


def test_get_run_map_with_id_and_user_gets_correct_map(test_client):
    mapId = random_utils.randomString(10)
    userId = random_utils.randomString(5)

    runMap = generate_run_map({'id': mapId, 'userId': userId})
    generate_run_map({'id': mapId})
    generate_run_map({'userId': userId})

    assert runMap == unit.getRunMapByIdAndUserId(runMap.id, runMap.userId)


def test_get_run_map_by_user_returns_all_run_maps_for_user(test_client):
    userId = random_utils.randomString(5)

    runMaps = []
    runMaps.append(generate_run_map({'userId': userId}))
    runMaps.append(generate_run_map({'userId': userId}))
    generate_run_map()

    assert sorted(runMaps) == sorted(unit.getRunMapByUser(userId))


def generate_run_map(init_values={}):
    runMap = buildRunMap(overridenValues=init_values)
    runMapForDbToDelete.append(runMap)
    unit.createNewRunMap(runMap)
    return runMap


@pytest.fixture(scope='module')
def test_client():
    app = buildTestApp()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    tableName = current_app.config['TABLE_NAMES']['RUN_MAP_TABLE']

    yield app.test_client()  # this is where the testing happens!

    # After
    exceptionsToRaise = []
    for runMap in runMapForDbToDelete:
        try:
            dynamo.get_table(tableName).delete_item(
                Key={'id': runMap.id, 'userId': runMap.userId})
        except ClientError as e:
            exceptionsToRaise.append(e)

    for e in exceptionsToRaise:
        print(e.response['Error']['Message'])

    if not exceptionsToRaise == []:
        raise Exception("Error while trying to delete items from db")

    ctx.pop()
