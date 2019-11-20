from app.tests.helpers.builder.user_builder import buildUser
from app.main.model.user import User


def test_user_generation_from_and_to_dict_works():
    user = buildUser()
    expectedUserDict = {
        "id": user.id,
        "email": user.email,
        "is_admin": user.is_admin,
        "basemap": {
            "center": user.basemap.center,
            "zoom": user.basemap.zoom,
            "markers": []
        }
    }

    for marker in user.basemap.markers:
        markerDict = {"mapId": marker.mapId,
                      "text": marker.text,
                      "cord": marker.cord}
        expectedUserDict["basemap"]["markers"].append(markerDict)

    assert expectedUserDict == user.generateDict()

    builtUser = User(user.generateDict())
    assert user == builtUser
