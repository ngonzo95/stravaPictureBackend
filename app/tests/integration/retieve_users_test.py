import pytest
from app.main import create_app
from flask_restplus import Api
from flask import Blueprint
from app.main.controller.user_auth_controller import api as user_ns
from app.main import dynamo
from flask import current_app
from app.main.model.user_auth import UserAuth

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns, path='/user')


def test_example(test_client):
    tableName = current_app.config['TABLE_NAMES']['USER_AUTH_TABLE']
    user = UserAuth({'id': "test1", 'strava_athlete_id': "dfd",
                     'strava_username': 'asdfd',
                     'strava_auth_token': 'dfdfd',
                     'strava_refresh_token': 'fd',
                     'strava_expiration_time': 10})

    dynamo.get_table(tableName).put_item(
        Item=user.generateDict())

    response = test_client.get('/user/')
    assert response.status_code == 200
    assert response.json == {'data': [{'id': 'test1',
                                       'strava_athlete_id': 'dfd',
                                       'strava_expiration_time': 10,
                                       'strava_username': 'asdfd'}]}

    dynamo.get_table(tableName).delete_item(
        Key={'id': user.id})


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('test')
    testing_client = flask_app.test_client()

    flask_app.register_blueprint(blueprint)
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()
