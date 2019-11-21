import pytest
from app.main import dynamo
from flask import current_app
from app.tests.helpers.test_app_builder import buildTestApp
from app.tests.helpers.builder.run_map_builder import buildRunMap
from botocore.exceptions import ClientError


runMapForDbToDelete = []


def test_retieve_run_map_with_id_gets_the_desired_user(test_client):
    # arrange
    runMap = generate_run_map()

    # act
    response = test_client.get(
        '/user/' + runMap.userId + '/run_map/' + runMap.id)

    # assert
    assert response.status_code == 200
    # asserting indivual things about responses because decimals are a pain
    assert runMap.id == response.json['id']
    assert runMap.mapName == response.json['mapName']


def test_retieve_run_maps_gets_all_run_maps_for_the_user(test_client):
    # arrange
    runMaps = []
    runMaps.append(generate_run_map({'userId': '42'}))
    runMaps.append(generate_run_map({'userId': '42'}))
    generate_run_map({'userId': '85'})

    # act
    response = test_client.get(
        '/user/' + '42' + '/run_map')

    # assert
    assert response.status_code == 200
    # asserting indivual things about responses because decimals are a pain
    res = response.json
    assert len(response.json) == 2
    assert (runMaps[0].id == res[0]['id'] or runMaps[0].id == res[1]['id'])
    assert (runMaps[1].id == res[1]['id'] or runMaps[1].id == res[0]['id'])


def generate_run_map(initValues={}):
    runMap = buildRunMap(initValues)
    runMapForDbToDelete.append(runMap)

    tableName = current_app.config['TABLE_NAMES']['RUN_MAP_TABLE']
    dynamo.get_table(tableName).put_item(
        Item=runMap.generateDict())
    return runMap


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
