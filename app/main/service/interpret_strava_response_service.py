def extract_ids_of_interest_from_activity_list(resJson):
    ids = []
    for activity in resJson:
        if activity['type'] == 'Run' and (not activity['commute']):
            ids.append(activity['id'])

    return ids
