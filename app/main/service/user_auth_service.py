from app.main import dynamo
from app.main.model.user_auth import UserAuth
import app.main.service.strava_backend_service as api
from flask import current_app
import requests
import time


def getAllUserAuths():
    results = userAuthTable().scan()['Items']
    users = []
    for res in results:
        user = UserAuth(res)
        users.append(user)

    return users


def getUserAuthById(id):
    dbResponse = userAuthTable().get_item(Key={'id': id})["Item"]
    return UserAuth(dbResponse)


def createUserAuth(userAuth):
    userAuthTable().put_item(Item=userAuth.generateDict())


def setUserAuth(id, args):
    stravaAuthJson = _getStravaAuth(args["code"])
    userAuth = UserAuth(id=id)
    _updateUserAuthWithStravaJson(userAuth, stravaAuthJson)
    userAuthTable().put_item(Item=userAuth.generateDict())


def checkUser(id):
    dbResponse = userAuthTable().get_item(Key={'id': id})
    return 'Item' in dbResponse

def generateStravaAuthUrl(id):
    url = "http://www.strava.com/oauth/authorize?client_id=" \
        + current_app.config['STRAVA_CLIENT_KEY'] \
        + "&response_type=code&redirect_uri=" \
        + current_app.config['BASE_URL'] \
        + "user/" + id + "/auth/"\
        + "exchange_token&approval_prompt=force&scope=read,activity:read"
    return url


def _getStravaAuth(code):
    url = "https://www.strava.com/oauth/token"
    url += '?client_id=' + current_app.config['STRAVA_CLIENT_KEY']
    url += '&client_secret=' + current_app.config['STRAVA_CLIENT_SECRET_KEY']
    url += '&code=' + code
    url += '&grant_type=authorization_code'
    return requests.post(url).json()


def _updateUserAuthWithStravaJson(userAuth, stravaAuthJson):
    userAuth.strava_athlete_id = stravaAuthJson["athlete"]["id"]
    userAuth.strava_username = stravaAuthJson["athlete"]["username"]
    userAuth.strava_auth_token = stravaAuthJson["access_token"]
    userAuth.strava_refresh_token = stravaAuthJson["refresh_token"]
    userAuth.strava_expiration_time = stravaAuthJson["expires_at"]
    return userAuth


def userAuthTable():
    tableName = current_app.config['TABLE_NAMES']['USER_AUTH_TABLE']
    return dynamo.get_table(tableName)


def getUpdatedUserAuth(id):
    userAuth = getUserAuthById(id)
    if int(time.time()) > userAuth.strava_expiration_time:
        _refreshAndSaveToken(userAuth)

    return userAuth


def _refreshAndSaveToken(userAuth):
    updated_token = api.refresh_auth_token(userAuth)
    userAuth.strava_refresh_token = updated_token['refresh_token']
    userAuth.strava_auth_token = updated_token['access_token']
    userAuth.strava_expiration_time = updated_token['expires_at']
    _saveToken(userAuth)


def _saveToken(userAuth):
    key = {'id': userAuth.id}
    updateExpression = "set strava_auth_token = :a, " \
        + "strava_expiration_time = :e, strava_refresh_token = :r"
    attributeValues = {':a': userAuth.strava_auth_token,
                       ':e': userAuth.strava_expiration_time,
                       ':r': userAuth.strava_refresh_token}

    userAuthTable().update_item(Key=key, UpdateExpression=updateExpression,
                                ExpressionAttributeValues=attributeValues)
