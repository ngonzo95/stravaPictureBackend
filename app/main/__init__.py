from flask import Flask

from app.main.config import config_by_name
from flask_dynamo import Dynamo

dynamo = Dynamo()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initalize dynamodb
    dynamo.init_app(app)

    return app
