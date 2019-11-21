import app.tests.helpers.util.random_utils as random_utils


def generate_summary_activity(type, commuteFlag):
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
        "id": random_utils.randint(0, 1000000),
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


def generate_detailed_activity():
    return {
        "id": random_utils.randint(0, 10000),
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
