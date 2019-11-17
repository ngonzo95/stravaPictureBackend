from flask import (request, Flask)
from flask_restplus import (Resource, Namespace)
from app.main.service.user_auth_service import getAllUserAuths
from app.main.response.user_auth_response import UserAuthResponse
api = UserAuthResponse.api
_userResponseType = UserAuthResponse.user


@api.route('/')
class UserList(Resource):
    @api.doc('List of all users')
    @api.marshal_list_with(_userResponseType, envelope='data')
    def get(self):
        """List all registered users"""
        return getAllUserAuths()
