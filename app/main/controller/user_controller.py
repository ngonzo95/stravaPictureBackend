from flask_restplus import Resource
import app.main.service.user_service as user_service
from app.main.response.user_response import UserResponse
from app.main.controller.rest_plus_api import Api

api = Api.api
_userResponseType = UserResponse.user


@api.route('/<id>')
@api.doc(params={'id': 'The users heatmap id'})
class UserList(Resource):
    @api.doc('Returns the base map of the user')
    @api.marshal_with(_userResponseType)
    def get(self, id):
        """Returns the specified user"""
        return user_service.getUserById(id)
