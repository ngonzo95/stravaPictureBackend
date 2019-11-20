from app.main.model.basemap import Basemap
import app.main.model.model_helper as model_helper


class User():
    def __init__(self, *initial_data, **kwargs):
        self._availableKeys = ["id", "email", "basemap", "is_admin"]

        self.id = None
        self.email = None
        self.basemap = Basemap()
        self.is_admin = False

        model_helper.initHelper(self, self._availableKeys,
                                initial_data, kwargs)
        # Check to see if the basemap needs to be constructed
        if not type(self.basemap) == Basemap:
            self.basemap = Basemap(self.basemap)

    def generateDict(self):
        d = model_helper.generateDictHelper(self, self._availableKeys)
        d["basemap"] = self.basemap.generateDict()
        return d

    def __repr__(self):
        return model_helper.reprHelper(self, self._availableKeys)

    def __eq__(self, other):
        return model_helper.equalHelper(self, self._availableKeys, other)
