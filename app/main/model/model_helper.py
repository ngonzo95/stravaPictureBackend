

def initHelper(object, object_keys, initial_data, kwargs):
    for dictionary in initial_data:
        for key in dictionary:
            if key in object_keys:
                setattr(object, key, dictionary[key])
    for key in kwargs:
        if key in object_keys:
            setattr(object, key, kwargs[key])


def generateDictHelper(object, object_keys):
    d = {}
    for key in object_keys:
        d[key] = getattr(object, key)
    return d


def reprHelper(object, object_keys):
    return str(type(object)) + ":" + str(object.generateDict())


def equalHelper(object, object_keys, other):
    if not type(object) == type(other):
        return False

    for key in object_keys:
        if not (hasattr(object, key)
                and getattr(object, key) == getattr(other, key)):
            return False
    return True
