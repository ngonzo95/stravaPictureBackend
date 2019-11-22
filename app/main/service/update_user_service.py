import app.main.service.interpret_strava_response_service as interpreter
import app.main.service.strava_backend_service as strava_backend
import app.main.service.user_auth_service as user_auth_service
import app.main.service.run_service as run_service
import app.main.service.geo_service as geo_service
from app.main.model.run_map import RunMap
import random

MAX_RUNS_TO_COLLECT = 60


def updateUser(userId):
    userAuth = user_auth_service.getUserAuthById(userId)
    runs = collectNewRuns(userAuth)
    for run in runs:
        run_service.createNewRun(runs)


def collectNewRuns(userAuth, last_update=0):
    # Loop through all of the pages until we run out of pages
    pageNum = 1
    activities = strava_backend.list_activities(userAuth, pageNum,
                                                lastUpdate=last_update)
    ids = interpreter.extract_ids_of_interest_from_activity_list(activities)

    while len(activities) == strava_backend.ACTIVITIES_PER_PAGE:
        if len(ids) > MAX_RUNS_TO_COLLECT:
            break

        pageNum += 1
        activities = strava_backend.list_activities(userAuth, pageNum)
        ids += interpreter \
            .extract_ids_of_interest_from_activity_list(activities)

    runs = []
    for id in ids:
        activity = strava_backend.get_activity_by_id(userAuth, id)
        run = interpreter.create_run_from_detailed_activity(userAuth.id,
                                                            activity)
        runs.append(run)

    return runs


def addRunsToRunMaps(runMaps, runs):
    # Map of new runs to add
    newRuns = {}
    for runMap in runMaps:
        newRuns[runMap.id] = []

    newRunMaps = []
    for run in runs:
        runAdded = False
        for runMap in runMaps:
            if geo_service.is_point_in_zone(run.start, runMap.center):
                newRuns[runMap.id].append(run.id)
                runAdded = True
                break
        for runMap in newRunMaps:
            if geo_service.is_point_in_zone(run.start, runMap.center):
                runMap.runs.append(run.id)
                runAdded = True
                break
        if not runAdded:
            map = createRunMapFromRun(run)
            newRunMaps.append(map)

    # append the runs to each run map
    for runMap in runMaps:
        runsToAdd = newRuns[runMap.id]
        if not runsToAdd == []:
            runMap.runs = runsToAdd + runMap.runs

    return runMaps, newRunMaps


def createRunMapFromRun(run):
    city = geo_service.get_city_name(run.start)

    values = {
        'center': run.start,
        'zoom': 7,
        'userId': run.userId,
        'runs': [run.id],
        'id': city + str(random.randint(0, 1000)),
        'mapName': city
    }
    return RunMap(values)
