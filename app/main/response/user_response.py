from flask_restplus import fields
from app.main.controller.rest_plus_api import Api

class UserResponse:
    api = Api.api
    marker = api.model('marker', {
        'mapId': fields.String(required=True, description='map id'),
        'text': fields.String(required=True, description='text to display to the user'),
        'cord': fields.List(fields.String, description='[lat, lon]')
    })

    basemap = api.model('basemap', {
        'center': fields.List(fields.String, required=True, description='center lat lon of the basemap'),
        'zoom': fields.Integer(required=True, description='The zoom level of the base map'),
        'markers': fields.Nested(marker, description="markers to represent each runmap")
    })

    user = api.model('user', {
        'id': fields.String(required=True, description='user id'),
        'email': fields.String(description='email of user'),
        'basemap': fields.Nested(basemap, description='The representation for the main page'),
    })
