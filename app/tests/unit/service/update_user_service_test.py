import app.tests.helpers.util.random_utils as random_utils
import app.main.service.interpret_strava_response_service as unit


def test_collect_ids_of_interest():
    resJson = [generate_summary_activity("Run", True),
               generate_summary_activity("Run", False),
               generate_summary_activity("Bike", True),
               generate_summary_activity("Bike", False),
               generate_summary_activity("Run", False)]

    idsOfInterest = unit.extract_ids_of_interest_from_activity_list(resJson)
    assert sorted([resJson[1]['id'], resJson[4]['id']]) \
        == sorted(idsOfInterest)


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
