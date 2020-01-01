from app.tests.helpers.builder.run_map_builder import buildRunMap
from app.tests.helpers.builder.user_builder import buildUser
from flask import current_app
import pytest
from app.tests.helpers.test_app_builder import buildTestApp
from app.main import dynamo
import app.main.service.run_map_service as unit
from botocore.exceptions import ClientError
import app.tests.helpers.util.random_utils as random_utils
import app.main.service.user_service as user_service
from app.main.model.basemap import Basemap
from app.tests.helpers.builder.marker_builder import buildMarker

runMapForDbToDelete = []
userForDbToDelete = []


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


def test_add_run_maps_adds_runs_to_given_map(test_client):
    runs = []
    for i in range(5):
        runs.append(random_utils.randomString(10))

    runMap = generate_run_map({'runs': runs})

    runsToAdd = []
    for i in range(6):
        runsToAdd.append(random_utils.randomString(10))

    unit.addRunsToRunMap(runMap.id, runMap.userId, runsToAdd)
    assert (runsToAdd + runs) == \
        unit.getRunMapByIdAndUserId(runMap.id, runMap.userId).runs


def test_add_runs_adds_runs_and_removes_runs_more_than_max():
    runs = []
    for i in range(unit.MAX_RUNS - 5):
        runs.append(random_utils.randomString(10))

    runMap = generate_run_map({'runs': runs})

    runsToAdd = []
    for i in range(10):
        runsToAdd.append(random_utils.randomString(10))

    unit.addRunsToRunMap(runMap.id, runMap.userId, runsToAdd)

    expectedRuns = []
    expectedRuns += runsToAdd
    for i in range(unit.MAX_RUNS-10):
        expectedRuns.append(runs[i])

    assert expectedRuns == \
        unit.getRunMapByIdAndUserId(runMap.id, runMap.userId).runs


def test_create_run_map_for_user_creates_run_map_and_adds_to_user(test_client):
    user = generate_user({'basemap': Basemap({'markers': [buildMarker()]})})
    runMap = buildRunMap(overridenValues={'userId': user.id})
    runMapForDbToDelete.append(runMap)

    unit.createRunMapForUser(runMap)

    assert unit.getRunMapByIdAndUserId(runMap.id, runMap.userId) == runMap

    foundUserBasemap = user_service.getUserById(user.id).basemap
    assert foundUserBasemap.markers[0].mapId == user.basemap.markers[0].mapId
    assert foundUserBasemap.markers[1].cord == runMap.center
    assert foundUserBasemap.markers[1].mapId == runMap.id
    assert foundUserBasemap.markers[1].text == runMap.mapName


def generate_run_map(init_values={}):
    runMap = buildRunMap(overridenValues=init_values)
    runMapForDbToDelete.append(runMap)
    unit.createNewRunMap(runMap)
    return runMap


def generate_user(init_values={}):
    user = buildUser(overridenValues=init_values)
    userForDbToDelete.append(user)
    user_service.createNewUser(user)
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
    cleanupRunMaps(exceptionsToRaise)
    cleanupUsers(exceptionsToRaise)

    for e in exceptionsToRaise:
        print(e.response['Error']['Message'])

    if not exceptionsToRaise == []:
        raise Exception("Error while trying to delete items from db")

    ctx.pop()


def cleanupRunMaps(exceptions):
    tableName = current_app.config['TABLE_NAMES']['RUN_MAP_TABLE']
    for runMap in runMapForDbToDelete:
        try:
            dynamo.get_table(tableName).delete_item(
                Key={'id': runMap.id, 'userId': runMap.userId})
        except ClientError as e:
            exceptions.append(e)


def cleanupUsers(exceptions):
    tableName = current_app.config['TABLE_NAMES']['USER_TABLE']
    for user in userForDbToDelete:
        try:
            dynamo.get_table(tableName).delete_item(
                Key={'id': user.id})
        except ClientError as e:
            exceptions.append(e)
