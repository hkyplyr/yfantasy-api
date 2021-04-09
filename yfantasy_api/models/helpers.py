def flatten_attributes(json):
    attributes = {}
    for d in json:
        if type(d) == list and len(d) == 0:
            continue
        if type(d) == list and len(d) != 0:
            print(d)
            continue
        attributes.update(d)
    return attributes
