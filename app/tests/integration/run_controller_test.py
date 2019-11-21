import pytest
from app.main import dynamo
from flask import current_app
from app.tests.helpers.test_app_builder import buildTestApp
from app.tests.helpers.builder.run_builder import buildRun
from botocore.exceptions import ClientError


runForDbToDelete = []


def test_retieve_run_with_id_gets_the_desired_run(test_client):
    # arrange
    run = generate_run()

    # act
    response = test_client.get(
        '/user/' + run.userId + '/run/' + run.id)

    # assert
    assert response.status_code == 200
    # asserting indivual things about responses because decimals are a pain
    assert run.id == response.json['id']
    assert run.name == response.json['name']
    assert run.polyline == response.json['polyline']


def generate_run(initValues={}):
    run = buildRun(initValues)
    runForDbToDelete.append(run)

    tableName = current_app.config['TABLE_NAMES']['RUN_TABLE']
    dynamo.get_table(tableName).put_item(
        Item=run.generateDict())
    return run


@pytest.fixture(scope='module')
def test_client():
    app = buildTestApp()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield app.test_client()  # this is where the testing happens!

    # After
    exceptionsToRaise = []
    cleanupRuns(exceptionsToRaise)
    for e in exceptionsToRaise:
        print(e.response['Error']['Message'])

    if not exceptionsToRaise == []:
        raise Exception("Error while trying to delete items from db")

    ctx.pop()


def cleanupRuns(exceptions):
    tableName = current_app.config['TABLE_NAMES']['RUN_TABLE']
    for runMap in runForDbToDelete:
        try:
            dynamo.get_table(tableName).delete_item(
                Key={'id': runMap.id, 'userId': runMap.userId})
        except ClientError as e:
            exceptions.append(e)
