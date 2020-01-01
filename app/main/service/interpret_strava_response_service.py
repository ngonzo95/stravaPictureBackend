from app.main.model.run import Run
from decimal import Decimal

ROUNDING_RESOLUTION = Decimal('.000000001')


def extract_ids_of_interest_from_activity_list(resJson):
    ids = []
    for activity in resJson:
        if activity['type'] == 'Run' and (not activity['commute']) and \
                activity['start_latlng'] is not None:
            ids.append(activity['id'])

    return ids


def create_run_from_detailed_activity(userId, activity):
    start = [Decimal(activity['start_latlng'][0]).quantize(ROUNDING_RESOLUTION),
             Decimal(activity['start_latlng'][1]).quantize(ROUNDING_RESOLUTION)]
    dictOfInterest = {'id': str(activity['id']), 'userId': str(userId),
                      'polyline': activity['map']['polyline'],
                      'start': start,
                      'name': activity['name'],
                      'type': activity['type']
                      }
    return Run(dictOfInterest)
