from app.main.model.run_map import RunMap
from app.main import dynamo
from flask import current_app
from boto3.dynamodb.conditions import Key
import app.main.service.user_service as user_service
from app.main.model.marker import Marker
MAX_RUNS = 30


def getRunMapByIdAndUserId(id, userId):
    dbResponse = runMapTable().get_item(
        Key={'id': id, 'userId': userId})["Item"]
    return RunMap(dbResponse)


def getRunMapByUser(userId):
    dbResponse = runMapTable().query(
        KeyConditionExpression=Key('userId').eq(userId)
    )
    maps = []
    for res in dbResponse['Items']:
        maps.append(RunMap(res))

    return maps


def addRunsToRunMap(id, userId, runs):
    runMap = getRunMapByIdAndUserId(id, userId)
    newRuns = runs + runMap.runs
    newRuns = newRuns[:MAX_RUNS]

    key = {'id': id, 'userId': userId}
    updateExpression = "set runs = :r"
    attributeValues = {':r': newRuns}
    runMapTable().update_item(Key=key, UpdateExpression=updateExpression,
                              ExpressionAttributeValues=attributeValues)


def createNewRunMap(runMap):
    runMapTable().put_item(Item=runMap.generateDict())


def createRunMapForUser(runMap):
    createNewRunMap(runMap)
    user = user_service.getUserById(runMap.userId)
    initalValues = {"mapId": runMap.id,
                    "text": runMap.mapName, "cord": runMap.center}
    newMarker = Marker(initalValues)
    user.basemap.markers.append(newMarker)
    user_service.update_marker_list(runMap.userId, user.basemap.markers)


def runMapTable():
    tableName = current_app.config['TABLE_NAMES']['RUN_MAP_TABLE']
    return dynamo.get_table(tableName)
