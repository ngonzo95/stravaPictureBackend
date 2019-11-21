from app.tests.helpers.builder.run_builder import buildRun
from app.main.model.run import Run


def test_user_generation_from_and_to_dict_works():
    run = buildRun()
    expectedRunMapDict = {
        'id': run.id,
        'userId': run.userId,
        'polyline': run.polyline,
        'start': run.start,
        'name': run.name,
        'type': run.type
    }

    assert expectedRunMapDict == run.generateDict()

    builtRun = Run(run.generateDict())
    assert run == builtRun
