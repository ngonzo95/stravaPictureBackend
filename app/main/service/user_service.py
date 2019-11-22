from app.main.model.user import User
from app.main import dynamo
from flask import current_app


def getUserById(id):
    dbResponse = userTable().get_item(Key={'id': id})["Item"]
    return User(dbResponse)


def createNewUser(user):
    userTable().put_item(Item=user.generateDict())


def update_marker_list(id, markerlist):
    key = {'id': id}
    updateExpression = "set basemap.markers = :m"

    serialMarkerList = []
    for marker in markerlist:
        serialMarkerList.append(marker.generateDict())

    attributeValues = {':m': serialMarkerList}
    userTable().update_item(Key=key, UpdateExpression=updateExpression,
                            ExpressionAttributeValues=attributeValues)


def update_last_update(id, lastUpdate):
    key = {'id': id}
    updateExpression = "set last_update = :l"

    attributeValues = {':l': lastUpdate}
    userTable().update_item(Key=key, UpdateExpression=updateExpression,
                            ExpressionAttributeValues=attributeValues)


def userTable():
    tableName = current_app.config['TABLE_NAMES']['USER_TABLE']
    return dynamo.get_table(tableName)
