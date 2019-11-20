import app.main.model.model_helper as model_helper


class Marker():
    def __init__(self, *initial_data, **kwargs):
        self._availableKeys = ["mapId", "text", "cord"]
        self.mapId = None
        self.text = None
        self.cord = None

        model_helper.initHelper(self, self._availableKeys,
                                initial_data, kwargs)

    def generateDict(self):
        return model_helper.generateDictHelper(self, self._availableKeys)

    def __repr__(self):
        return model_helper.reprHelper(self, self._availableKeys)

    def __eq__(self, other):
        return model_helper.equalHelper(self, self._availableKeys, other)
