from flask_restplus import Api
from app.main import create_app
from app import blueprint


def buildTestApp():
    flask_app = create_app('test')
    flask_app.register_blueprint(blueprint)
    return flask_app
