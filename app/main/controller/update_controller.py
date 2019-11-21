from flask_restplus import Resource
import app.main.service.update_user_service as update_user_service
from app.main.controller.rest_plus_api import Api

api = Api.api


@api.route('/<id>/update')
@api.doc(params={'id': 'users id', 'runId': 'the id of the specific run'})
class UpdateController(Resource):
    @api.doc('Forces an update from the user')
    def get(self, id):
        """Updates the user"""
        update_user_service.updateUser(id)
        return {}, 200
