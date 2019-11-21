from app.main.model.run import Run
from app.main import dynamo
from flask import current_app


def getRunByIdAndUserId(id, userId):
    dbResponse = runTable().get_item(
        Key={'id': id, 'userId': userId})["Item"]
    return Run(dbResponse)


def createNewRun(run):
    runTable().put_item(Item=run.generateDict())


def runTable():
    tableName = current_app.config['TABLE_NAMES']['RUN_TABLE']
    return dynamo.get_table(tableName)
