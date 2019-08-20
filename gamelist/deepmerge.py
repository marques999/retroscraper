def merge_dictionary(path, source, destination):

    for key, value in destination.items():

        if key in source:
            source[key] = merge_recursive(path + [key], source[key], value)
        else:
            source[key] = value

    return source

def merge_recursive(path, source, destination):

    if not (isinstance(source, type(destination))
            or isinstance(destination, type(source))):
        return destination
    elif isinstance(destination, dict):
        return merge_dictionary(path, source, destination)
    elif isinstance(destination, list):
        return source + destination
    else:
        return destination

def merge(source, destination):

    return merge_recursive([], source, destination)
