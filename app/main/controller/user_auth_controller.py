
from flask_restplus import (Resource, reqparse)
from flask import redirect
from app.main.service.user_auth_service import (getAllUserAuths,
                                                generateStravaAuthUrl,
                                                setUserAuth)

from app.main.response.user_auth_response import UserAuthResponse

api = UserAuthResponse.api
_userResponseType = UserAuthResponse.user


@api.route('')
class UserList(Resource):
    @api.doc('List of all users')
    @api.marshal_list_with(_userResponseType, envelope='data')
    def get(self):
        """List all registered users"""
        return getAllUserAuths()


@api.route('/<id>/auth/get_strava_token')
@api.doc(params={'id': 'The users heatmap id'})
class GetStravaToken(Resource):
    @api.doc('Redirects user to strava so that users can approve the heatmap')
    def get(self, id):
        """Redirects user to strava so that the user can approve the app"""

        return redirect(generateStravaAuthUrl(id), code=302)


@api.route('/<id>/auth/set_strava_token')
@api.doc(params={'id': 'The users heatmap id'})
class SetStravaToken(Resource):
    @api.doc('A url used for updating users auth information')
    def get(self, id):
        """puts user auth information into dynamo"""
        parser = reqparse.RequestParser()
        parser.add_argument('code')
        args = parser.parse_args()
        setUserAuth(id, args)
        return {"message": "Successfully set user information please go"
                + "back to the heatmap"}
