from flask_restplus import Api
from flask import Blueprint
from app.main import create_app


def buildTestApp(nameSpaces):
    blueprint = Blueprint('api', __name__)
    api = Api(blueprint,
              title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
              version='1.0',
              description='a boilerplate for flask restplus web service'
              )
    for(ns, path) in nameSpaces:
        api.add_namespace(ns, path=path)

    flask_app = create_app('test')
    flask_app.register_blueprint(blueprint)
    return flask_app
