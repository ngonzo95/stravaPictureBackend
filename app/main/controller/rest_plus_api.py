from flask_restplus import Namespace


class Api:
    api = Namespace('user', description='main endpoint for all opperations')
