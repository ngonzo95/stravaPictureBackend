
from flask_restplus import (Resource, reqparse)
from flask import redirect
from app.main.service.user_auth_service import (generateStravaAuthUrl,
                                                setUserAuth)

from app.main.response.user_response import UserAuthResponse
from werkzeug.exceptions import Unauthorized

api = UserAuthResponse.api
_userResponseType = UserAuthResponse.user


@api.route('/<id>')
@api.doc(params={'id': 'The users heatmap id'})
class UserList(Resource):
    @api.doc('Returns the base map of the user')
    @api.marshal_with(_userResponseType)
    def get(self):
        """Returns the specified user"""
        pass


@api.route('/<id>/auth/get_strava_token')
@api.doc(params={'id': 'The users heatmap id'})
class GetStravaToken(Resource):
    @api.doc('Redirects user to strava so that users can approve the heatmap')
    def get(self, id):
        """Redirects user to strava so that the user can approve the app"""

        return redirect(generateStravaAuthUrl(id), code=302)


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
            setUserAuth(id, args)
            return {"message": "Successfully set user information please go"
                    + "back to the heatmap"}
        else:
            raise Unauthorized("Please enable the activity read ability, the "
                               + "app wont work without it")
