from app.tests.helpers.builder.run_builder import buildRun
from flask import current_app
import pytest
from app.tests.helpers.test_app_builder import buildTestApp
from app.main import dynamo
import app.main.service.run_service as unit
from botocore.exceptions import ClientError
import app.tests.helpers.util.random_utils as random_utils

runsForDbToDelete = []


def test_get_run_with_id_and_user_gets_correct_map(test_client):
    mapId = random_utils.randomString(10)
    userId = random_utils.randomString(5)

    run = generate_run({'id': mapId, 'userId': userId})
    generate_run({'id': mapId})
    generate_run({'userId': userId})

    assert run == unit.getRunByIdAndUserId(run.id, run.userId)


def generate_run(init_values={}):
    run = buildRun(overridenValues=init_values)
    runsForDbToDelete.append(run)
    unit.createNewRun(run)
    return run


@pytest.fixture(scope='module')
def test_client():
    app = buildTestApp()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    tableName = current_app.config['TABLE_NAMES']['RUN_TABLE']

    yield app.test_client()  # this is where the testing happens!

    # After
    exceptionsToRaise = []
    for runMap in runsForDbToDelete:
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
