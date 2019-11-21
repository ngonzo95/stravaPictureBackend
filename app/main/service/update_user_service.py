import app.main.service.interpret_strava_response_service as interpreter
import app.main.service.strava_backend_service as strava_backend
import app.main.service.user_auth_service as user_auth_service
import app.main.service.run_service as run_service


def updateUser(userId):
    userAuth = user_auth_service.getUserAuthById(userId)
    ids = []

    # Loop through all of the pages until we run out of pages
    pageNum = 1
    activities = strava_backend.list_activities(userAuth, pageNum)

    while len(activities) == strava_backend.ACTIVITIES_PER_PAGE:
        pageNum += 1
        ids += interpreter.extract_ids_of_interest_from_activity_list(activities)
        activities = strava_backend.list_activities(userAuth, pageNum)

    ids += interpreter.extract_ids_of_interest_from_activity_list(activities)

    for id in ids:
        activity = strava_backend.get_activity_by_id(userAuth, id)
        run = interpreter.create_run_from_detailed_activity(userId, activity)
        run_service.createNewRun(run)
