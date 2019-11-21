from app.main.model.run import Run


def extract_ids_of_interest_from_activity_list(resJson):
    ids = []
    for activity in resJson:
        if activity['type'] == 'Run' and (not activity['commute']):
            ids.append(activity['id'])

    return ids


def create_run_from_detailed_activity(userId, activity):
    dictOfInterest = {'id': activity['id'], 'userId': userId,
                      'polyline': activity['map']['polyline'],
                      'start': activity['start_latlng'],
                      'name': activity['name'],
                      'type': activity['type']
                      }
    return Run(dictOfInterest)
