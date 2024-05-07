def flatten_attributes(json):
    attributes = {}
    for d in json:
        if type(d) == list and len(d) == 0:
            continue
        attributes.update(d)
    return attributes


EMPTY_VALUES = [None, "-", ""]


def as_float(value):
    if value in EMPTY_VALUES:
        return None
    return float(value)


def as_int(value):
    if value in EMPTY_VALUES:
        return None
    return int(value)


def as_bool(value):
    if value in EMPTY_VALUES:
        return False
    return True if as_int(value) else False
