import app.main.service.update_user_service as unit
from app.tests.helpers.builder.user_auth_builder import buildUserAuth
import app.tests.helpers.util.mock_strava_responses as strava_api
from app.tests.helpers.builder.run_builder import buildRun
from app.tests.helpers.builder.run_map_builder import buildRunMap
import app.tests.helpers.util.random_utils as random_utils
import requests_mock
from decimal import Decimal


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


def test_create_run_map_from_run_sets_name_needed_values():
    run = buildRun(overridenValues={
                   'start': [Decimal(44.946636), Decimal(-93.293241)]})
    runMap = unit.createRunMapFromRun(run)

    assert runMap == buildRunMap(overridenValues={'mapName': 'Minneapolis',
                                                  'runs': [run.id],
                                                  'center': run.start,
                                                  'zoom': 7,
                                                  'userId': run.userId,
                                                  'id': runMap.id})


def test_add_runs_to_run_maps():
    #Set up a few run maps with given locations
    startLocations = [[Decimal(75.3425), Decimal(-95.300)],
                      [Decimal(44.946636), Decimal(-93.293241)],
                      [Decimal(54.8675), Decimal(-85.123)],
                      ]
    runMaps = []
    expectedRunList = []
    runs = []

    for start in startLocations:
        runMap = buildRunMap(overridenValues={'center': start})
        expectedRunList.append(runMap.runs.copy())
        runMaps.append(runMap)

    # build a handfull of runs around the start location that must be added to
    # the map
    for i in range(20):
        index = random_utils.randint(0, len(startLocations)-1)
        run = buildRun(overridenValues={'start': startLocations[index]})
        expectedRunList[index] = [run.id] + expectedRunList[index]
        runs.append(run)

    # Now add a few runs that are not apart of any existing run map
    newLocation = [Decimal(40.688237), Decimal(-112.073817)]
    runsFromNewMap = [buildRun(overridenValues={'start': newLocation})]
    runsFromNewMap.append(buildRun(overridenValues={'start': newLocation}))
    runs += runsFromNewMap

    #reverse them so the 'newest ones' are first
    runs = reversed(runs)
    updatedMaps, newMaps = unit.addRunsToRunMaps(runMaps, runs)

    for i in range(len(runMaps)):
        assert updatedMaps[i].runs == expectedRunList[i]

    assert newMaps[0].runs == [runsFromNewMap[1].id, runsFromNewMap[0].id]
    assert newMaps[0].center == newLocation
