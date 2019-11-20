from app.main.model.run_map import RunMap
from app.main import dynamo
from flask import current_app
from boto3.dynamodb.conditions import Key


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


def createNewRunMap(runMap):
    runMapTable().put_item(Item=runMap.generateDict())


def runMapTable():
    tableName = current_app.config['TABLE_NAMES']['RUN_MAP_TABLE']
    return dynamo.get_table(tableName)
