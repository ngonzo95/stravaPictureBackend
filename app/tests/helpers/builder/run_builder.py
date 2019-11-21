from app.main.model.run import Run
import app.tests.helpers.util.random_utils as random_utils


def buildRun(overridenValues={}):
    data = {
        'id': random_utils.randomString(4),
        'userId': random_utils.randomString(10),
        'polyline': random_utils.randomString(14),
        'start': random_utils.randomCord(),
        'name': random_utils.randomString(10),
        'type': random_utils.randomString(6)
    }

    for (key, value) in overridenValues.items():
        data[key] = value

    return Run(data)
