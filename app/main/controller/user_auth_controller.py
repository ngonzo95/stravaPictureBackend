
from flask_restplus import (Resource, reqparse)
from flask import redirect
import app.main.service.user_auth_service as user_auth_service
import app.main.service.user_service as user_service

from app.main.response.user_response import UserResponse
from werkzeug.exceptions import Unauthorized

api = UserResponse.api
_userResponseType = UserResponse.user


@api.route('/<id>')
@api.doc(params={'id': 'The users heatmap id'})
class UserList(Resource):
    @api.doc('Returns the base map of the user')
    @api.marshal_with(_userResponseType)
    def get(self, id):
        """Returns the specified user"""
        return user_service.getUserById(id)


@api.route('/<id>/auth/get_strava_token')
@api.doc(params={'id': 'The users heatmap id'})
class GetStravaToken(Resource):
    @api.doc('Redirects user to strava so that users can approve the heatmap')
    def get(self, id):
        """Redirects user to strava so that the user can approve the app"""

        return redirect(user_auth_service.generateStravaAuthUrl(id), code=302)


@api.route('/<id>/auth/exchange_token')
@api.doc(params={'id': 'The users heatmap id'})
class SetStravaToken(Resource):
    @api.doc('A url used for updating users auth information')
    def get(self, id):
        """puts user auth information into dynamo"""
        parser = reqparse.RequestParser()
        parser.add_argument('code')
        parser.add_argument('scope')
        args = parser.parse_args()

        if "activity:read" in args["scope"]:
            user_auth_service.setUserAuth(id, args)
            return {"message": "Successfully set user information please go"
                    + "back to the heatmap"}
        else:
            raise Unauthorized("Please enable the activity read ability, the "
                               + "app wont work without it")
