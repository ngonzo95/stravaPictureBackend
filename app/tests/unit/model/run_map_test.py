from app.tests.helpers.builder.run_map_builder import buildRunMap
from app.main.model.run_map import RunMap


def test_user_generation_from_and_to_dict_works():
    runMap = buildRunMap()
    expectedRunMapDict = {
        "id": runMap.id,
        "mapName": runMap.mapName,
        "userId": runMap.userId,
        "center": runMap.center,
        "zoom": runMap.zoom,
        "runs": runMap.runs
    }

    assert expectedRunMapDict == runMap.generateDict()

    builtRunMap = RunMap(runMap.generateDict())
    assert runMap == builtRunMap
