from flask_restplus import Namespace, fields


class UserAuthResponse:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'id': fields.String(required=True, description='user id'),
        'strava_athlete_id': fields.String(required=True, description='strava athlete id'),
        'strava_username': fields.String(required=True, description='strava user name'),
        'strava_expiration_time': fields.Integer(required=True, description='The time in epoch when the auth will expire')
    })
