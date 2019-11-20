import app.main.model.model_helper as model_helper
from app.main.model.marker import Marker


class Basemap():
    def __init__(self, *initial_data, **kwargs):
        self._availableKeys = ["center", "cord", "markers"]
        self.center = None
        self.cord = None
        self.markers = []

        model_helper.initHelper(self, self._availableKeys,
                                initial_data, kwargs)
        for i in range(len(self.markers)):
            if not type(self.markers[i]) == Marker:
                self.markers[i] = Marker(self.markers[i])

    def generateDict(self):
        d = model_helper.generateDictHelper(self, self._availableKeys)

        # Generate the dictionary for the marker list
        markers = []
        for marker in self.markers:
            markers.append(marker.generateDict())

        d["markers"] = markers
        return d

    def __repr__(self):
        return model_helper.reprHelper(self, self._availableKeys)

    def __eq__(self, other):
        return model_helper.equalHelper(self, self._availableKeys, other)
