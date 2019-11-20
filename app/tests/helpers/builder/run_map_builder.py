from app.main.model.run_map import RunMap
import app.tests.helpers.util.random_utils as random_utils


def buildRunMap(overridenValues={}):
    data = {
        'id': random_utils.randomString(4),
        'mapName': random_utils.randomString(14),
        'userId': random_utils.randomString(10),
        'center': random_utils.randomCord(),
        'zoom': random_utils.randint(0, 12),
        'runs': []
    }

    for i in range(random_utils.randint(0, 5)):
        data['runs'].append(random_utils.randomString(5))

    for (key, value) in overridenValues.items():
        data[key] = value

    return RunMap(data)
