import os
# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']
basedir = os.path.abspath(os.path.dirname(__file__))


def initTable(tableNames):
    return [
        dict(TableName=tableNames['USER_AUTH_TABLE'],
             KeySchema=[dict(AttributeName='id', KeyType='HASH')],
             AttributeDefinitions=[
                 dict(AttributeName='id', AttributeType='S')],
             ProvisionedThroughput=dict(
                 ReadCapacityUnits=5, WriteCapacityUnits=5)
             )
    ]


def generateTableNames(suffix):
    tableNames = {}
    tableNames['USER_AUTH_TABLE'] = "user_auth_" + suffix
    return tableNames


class Config:
    STRAVA_CLIENT_SECRET_KEY = os.getenv('STRAVA_CLIENT_SECRET_KEY')
    STRAVA_CLIENT_KEY = '21346'
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    TABLE_NAMES = generateTableNames('dev')
    DYNAMO_TABLES = initTable(TABLE_NAMES)
    BASE_URL = "http://localhost:5000/"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    TABLE_NAMES = generateTableNames('test')
    DYNAMO_TABLES = initTable(TABLE_NAMES)
    BASE_URL = "http://testurl/"
    STRAVA_CLIENT_KEY = 'TESTCLIENTID'
    STRAVA_CLIENT_SECRET_KEY = 'TESTSECRET'


class ProductionConfig(Config):
    DEBUG = False
    TABLE_NAMES = generateTableNames('prod')
    DYNAMO_TABLES = initTable(TABLE_NAMES)


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
