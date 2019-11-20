from flask_restplus import Resource
import app.main.service.run_map_service as run_map_service
from app.main.response.run_map_response import RunMapResponse
from app.main.controller.rest_plus_api import Api

api = Api.api
_runMapResponseType = RunMapResponse.runMap


@api.route('/<id>/run_map/<mapId>')
@api.doc(params={'id': 'users id', 'mapId': 'the id of the specific run map'})
class RunMapController(Resource):
    @api.doc('Returns the specified run map for the user')
    @api.marshal_with(_runMapResponseType)
    def get(self, id, mapId):
        """Returns the specified user"""
        return run_map_service.getRunMapByIdAndUserId(mapId, id)


@api.route('/<id>/run_map')
@api.doc(params={'id': 'Retieves the specified run map'})
class RunMapsController(Resource):
    @api.doc('Returns all the run maps for the user')
    @api.marshal_list_with(_runMapResponseType)
    def get(self, id):
        """Returns the specified user"""
        return run_map_service.getRunMapByUser(id)
