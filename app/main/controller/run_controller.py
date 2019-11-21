from flask_restplus import Resource
import app.main.service.run_service as run_service
from app.main.response.run_response import RunResponse
from app.main.controller.rest_plus_api import Api

api = Api.api
_runResponseType = RunResponse.run


@api.route('/<id>/run/<runId>')
@api.doc(params={'id': 'users id', 'runId': 'the id of the specific run'})
class RunMapController(Resource):
    @api.doc('Returns the specified run')
    @api.marshal_with(_runResponseType)
    def get(self, id, runId):
        """Returns the specified user"""
        return run_service.getRunByIdAndUserId(runId, id)
