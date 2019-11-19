from app.main import dynamo
from app.main.model.user_auth import UserAuth
from flask import current_app
import requests


def getAllUserAuths():
    results = userAuthTable().scan()['Items']
    users = []
    for res in results:
        user = UserAuth(res)
        users.append(user)

    return users


def setUserAuth(id, args):
    stravaAuthJson = _getStravaAuth(args["code"])
    user = UserAuth(id=id)
    user.strava_athlete_id = stravaAuthJson["athlete"]["id"]
    user.strava_username = stravaAuthJson["athlete"]["username"]
    user.strava_auth_token = stravaAuthJson["access_token"]
    user.strava_refresh_token = stravaAuthJson["refresh_token"]
    user.strava_expiration_time = stravaAuthJson["expires_at"]
    userAuthTable().put_item(Item=user.generateDict())


def generateStravaAuthUrl(id):
    url = "http://www.strava.com/oauth/authorize?client_id=" \
        + current_app.config['STRAVA_CLIENT_KEY'] \
        + "&response_type=code&redirect_uri=" \
        + current_app.config['BASE_URL'] \
        + "user/" + id + "/auth/set_strava_token/"\
        + "exchange_token&approval_prompt=force&scope=read"
    return url

def _getStravaAuth(code):
    url = "https://www.strava.com/oauth/token"
    url += '?client_id=' + current_app.config['STRAVA_CLIENT_KEY']
    url += '&client_secret=' + current_app.config['STRAVA_CLIENT_SECRET_KEY']
    url += '&code=' + code
    url += '&grant_type=authorization_code'
    return requests.post(url).json()

def userAuthTable():
    tableName = current_app.config['TABLE_NAMES']['USER_AUTH_TABLE']
    return dynamo.get_table(tableName)
