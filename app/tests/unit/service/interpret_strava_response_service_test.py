import app.tests.helpers.util.random_utils as random_utils
from app.tests.helpers.util.mock_strava_responses import (
    generate_summary_activity, generate_detailed_activity)
import app.main.service.interpret_strava_response_service as unit
from app.main.model.run import Run
from decimal import Decimal


def test_collect_ids_of_interest():
    resJson = [generate_summary_activity("Run", True),
               generate_summary_activity("Run", False),
               generate_summary_activity("Bike", True),
               generate_summary_activity("Bike", False),
               generate_summary_activity("Run", False)]

    idsOfInterest = unit.extract_ids_of_interest_from_activity_list(resJson)
    assert sorted([resJson[1]['id'], resJson[4]['id']]) \
        == sorted(idsOfInterest)


def test_create_run_from_detailed_activity():
    userId = random_utils.randomString(5)
    activity = generate_detailed_activity()

    run = unit.create_run_from_detailed_activity(userId, activity)

    start = [Decimal(activity['start_latlng'][0]).quantize(unit.ROUNDING_RESOLUTION),
             Decimal(activity['start_latlng'][1]).quantize(unit.ROUNDING_RESOLUTION)]
    dictOfInterest = {'id': activity['id'], 'userId': userId,
                      'polyline': activity['map']['polyline'],
                      'start': start,
                      'name': activity['name'],
                      'type': activity['type']
                      }
    expectedRun = Run(dictOfInterest)

    #TODO deal with the problem of decimal equality
    assert str(expectedRun.id) == run.id
    assert expectedRun.polyline == run.polyline
