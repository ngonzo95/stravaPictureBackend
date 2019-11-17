from app.main import dynamo
from app.main.model.user_auth import UserAuth
from flask import current_app


def getAllUserAuths():
    results = userAuthTable().scan()['Items']
    users = []
    for res in results:
        user = UserAuth(res)
        users.append(user)

    return users


def userAuthTable():
    tableName = current_app.config['TABLE_NAMES']['USER_AUTH_TABLE']
    return dynamo.get_table(tableName)
