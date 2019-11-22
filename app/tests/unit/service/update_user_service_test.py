import app.main.service.update_user_service as unit
from app.tests.helpers.builder.user_auth_builder import buildUserAuth
import app.tests.helpers.util.mock_strava_responses as strava_api
from app.tests.helpers.builder.run_builder import buildRun
import app.tests.helpers.util.random_utils as random_utils
import requests_mock


def test_collect_runs_returns_the_runs_of_interest():
    userAuth = buildUserAuth()
    runIds = []
    for i in range(10):
        id = random_utils.randint(0, 10000)
        run = buildRun(overridenValues={'id': str(id), 'userId': userAuth.id})
        runIds.append(id)

    with requests_mock.Mocker() as m:
        strava_api.generate_mock_strava_api(runIds, 30, m)
        runs = unit.collectNewRuns(userAuth, last_update=5)

    assert len(runs) == 10


def test_update_user_only_inserts_runs_up_to_max_into_db():
    userAuth = buildUserAuth()
    runIds = []
    for i in range(40):
        id = random_utils.randint(0, 10000)
        run = buildRun(overridenValues={'id': str(id), 'userId': userAuth.id})
        runIds.append(id)

    with requests_mock.Mocker() as m:
        strava_api.generate_mock_strava_api(runIds, 0, m)
        unit.MAX_RUNS_TO_COLLECT = 10
        runs = unit.collectNewRuns(userAuth)

    assert len(runs) == 30
