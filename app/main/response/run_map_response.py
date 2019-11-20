from flask_restplus import fields
from app.main.controller.rest_plus_api import Api


class RunMapResponse:
    api = Api.api
    marker = api.model('marker', {
        'mapId': fields.String(required=True, description='map id'),
        'text': fields.String(required=True, description='text to display to the user'),
        'cord': fields.List(fields.String, description='[lat, lon]')
    })

    runMap = api.model('run_map', {
        "id": fields.String(description='The id of run map, only unique per user'),
        "mapName": fields.String(description='The name of the map'),
        "userId": fields.String(description='The id of the user'),
        "runs": fields.List(fields.String, required=True, description='list of run ids'),
        'center': fields.List(fields.String, required=True, description='center of run map'),
        'zoom': fields.Integer(required=True, description='The zoom level of the base map')
    })
