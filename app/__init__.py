from flask_restplus import Api
from flask import Blueprint

# These imports are needed to render the api todo figure out a way to fix this
import app.main.controller.user_auth_controller
import app.main.controller.user_controller
import app.main.controller.run_map_controller

from app.main.controller.rest_plus_api import Api as UserApi

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(UserApi.api, path='/user')
