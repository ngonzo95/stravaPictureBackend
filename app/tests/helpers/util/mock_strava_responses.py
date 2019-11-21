import app.tests.helpers.util.random_utils as random_utils
import json
import random
import decimal


def generate_mock_strava_api(runIds, numberOfNoiseActivities, mock):
    # Save the last Item for the end
    runIdsCopy = runIds.copy()
    lastId = runIdsCopy[-1]
    del runIdsCopy[-1]

    activityList = []
    activityListPage = 1
    for i in reversed(range(len(runIdsCopy) + numberOfNoiseActivities)):
        noiseThreshold = 1.0 * (i - len(runIdsCopy)) / (len(runIdsCopy) + 1)
        isNoise = False

        idOfActivity = None
        if len(runIdsCopy) == 0 or (random.random() < noiseThreshold):
            idOfActivity = random_utils.randint(0, 1000000)
            isNoise = True
        else:
            idOfActivity = runIdsCopy[0]
            del runIdsCopy[0]

        generate_endpoint_for_activity(mock, idOfActivity)
        activityList.append(
            generate_summary_activity('Run', isNoise, id=idOfActivity))
        if len(activityList) == 30:
            generate_endpoint_for_activity_list_page(mock, activityListPage, activityList)
            activityList = []
            activityListPage += 1

    # Generate the api for the last item
    generate_endpoint_for_activity(mock, lastId)
    activityList.append(generate_summary_activity('Run', False, lastId))
    generate_endpoint_for_activity_list_page(
        mock, activityListPage, activityList)


def generate_endpoint_for_activity_list_page(mock, pageNumber, activities):
    stravaUrl = 'https://www.strava.com/api/v3/athlete/activities'
    stravaUrl += '?page=' + str(pageNumber) + '&per_page=30'
    mock.get(stravaUrl, text=json.dumps(activities, cls=DecimalEncoder))


def generate_endpoint_for_activity(mock, id):
    stravaUrl = 'https://www.strava.com/api/v3/activities/' + str(id)
    mock.get(stravaUrl,
             text=json.dumps(generate_detailed_activity(id=id), cls=DecimalEncoder)
             )


def generate_summary_activity(type, commuteFlag, id=random_utils.randint(0, 1000000)):
    return {
        "resource_state": random_utils.randint(0, 5),
        "athlete": {
            "id": random_utils.randint(0, 10000),
            "resource_state": random_utils.randint(0, 100)
        },
        "name": random_utils.randomString(5),
        "distance": random_utils.randomDecimal(0, 100, 3),
        "type": type,
        "workout_type": random_utils.randomString(15),
        "id": id,
        "commute": commuteFlag,
        "external_id": random_utils.randomString(5),
        "utc_offset": random_utils.randint(-10000, 10000),
        "start_latlng": random_utils.randomCord(),
        "end_latlng": random_utils.randomCord(),
        "location_city": random_utils.randomString(6),
        "location_state": random_utils.randomString(6),
        "location_country": random_utils.randomString(4),
        "start_latitude": [random_utils.randomCord()[0]],
        "start_longitude": [random_utils.randomCord()[1]],
        "achievement_count": random_utils.randint(0, 10)
    }


def generate_detailed_activity(id=random_utils.randint(0, 1000000)):
    return {
        "id": id,
        "resource_state": random_utils.randint(0, 10000),
        "athlete": {
            "id": random_utils.randint(0, 10000),
            "resource_state": random_utils.randint(0, 10000)
        },
        "name": random_utils.randomString(6),
        "distance": random_utils.randint(0, 10000),
        "moving_time": random_utils.randint(0, 10000),
        "elapsed_time": random_utils.randint(0, 10000),
        "type": "Ride",
        "start_latlng": random_utils.randomCord(),
        "end_latlng": random_utils.randomCord(),
        "start_latitude": random_utils.randomCord()[0],
        "start_longitude": random_utils.randomCord()[1],
        "achievement_count": random_utils.randint(0, 10000),
        "kudos_count": random_utils.randint(0, 10000),
        "comment_count": random_utils.randint(0, 10000),
        "map": {
            "id": random_utils.randomString(6),
            "polyline": random_utils.randomString(20),
            "resource_state": random_utils.randint(0, 10000),
            "summary_polyline": random_utils.randomString(6)
        },
        "trainer": False,
        "commute": False,
        "manual": False,
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
