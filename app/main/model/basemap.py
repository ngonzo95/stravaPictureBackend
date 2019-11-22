import app.main.model.model_helper as model_helper
from app.main.model.marker import Marker
from decimal import Decimal

ROUNDING_RESOLUTION = Decimal('.000000001')


class Basemap():
    def __init__(self, *initial_data, **kwargs):
        self._availableKeys = ["center", "zoom", "markers"]
        self.center = [Decimal(39.8283).quantize(ROUNDING_RESOLUTION),
                       Decimal(-98.5795).quantize(ROUNDING_RESOLUTION)]
        self.zoom = 3
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
