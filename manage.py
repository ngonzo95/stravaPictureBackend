import os
from app import blueprint
from flask_script import Manager
from app.main import create_app

app = create_app(os.getenv('STRAVA_BACKEND_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


manager = Manager(app)


@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()
