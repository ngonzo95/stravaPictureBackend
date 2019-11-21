from flask_restplus import fields
from app.main.controller.rest_plus_api import Api


class RunResponse:
    api = Api.api

    run = api.model('run', {
        "id": fields.String(description='The id of run map, only unique per user'),
        "name": fields.String(description='The name of the map'),
        "polyline": fields.String(description='The id of the user'),
        'start': fields.List(fields.String, required=True, description='center of run map')
    })
