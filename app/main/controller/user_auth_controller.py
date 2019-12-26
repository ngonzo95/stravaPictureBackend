
from flask_restplus import (Resource, reqparse)
from flask import redirect
import app.main.service.user_auth_service as user_auth_service
import app.main.service.user_service as user_service
from app.main.model.user import User
from werkzeug.exceptions import Unauthorized
from app.main.controller.rest_plus_api import Api

api = Api.api


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
            user_service.createNewUser(User(id=id))
            return {"message": "Successfully set user information please go"
                    + "back to the heatmap"}
        else:
            raise Unauthorized("Please enable the activity read ability, the "
                               + "app wont work without it")


@api.route('/<id>/has_account')
@api.doc(params={'id': 'The users heatmap id'})
class UserList(Resource):
    @api.doc("Returns a single field has_account which is true if the user has"
             + "an account associated with their id.")
    def get(self, id):
        """Returns if the user has an account"""
        return {'has_account': user_auth_service.checkUser(id)}, 200
