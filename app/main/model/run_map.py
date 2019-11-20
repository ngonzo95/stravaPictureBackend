import app.main.model.model_helper as model_helper
from decimal import Decimal


class RunMap():
    def __init__(self, *initial_data, **kwargs):
        self._availableKeys = ["id", "mapName",
                               "userId", "center", "zoom", "runs"]

        self.id = ""
        self.mapName = ""
        self.userId = ""
        self.center = [Decimal(0), Decimal(0)]
        self.zoom = 1
        self.runs = []

        model_helper.initHelper(self, self._availableKeys,
                                initial_data, kwargs)
        # Check to see if the basemap needs to be constructed

    def generateDict(self):
        return model_helper.generateDictHelper(self, self._availableKeys)

    def __repr__(self):
        return model_helper.reprHelper(self, self._availableKeys)

    def __eq__(self, other):
        return model_helper.equalHelper(self, self._availableKeys, other)

    def __lt__(self, other):
        if not self.userId == other.userId:
            return self.userId < other.userId
        else:
            return self.id < other.id
