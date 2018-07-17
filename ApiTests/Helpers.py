
def update_keys(dictionary, old_key, new_key):
    # swap key name in dict, cause .get() may fail (userid != userId)
    dictionary[new_key] = dictionary.pop(old_key)
    return dictionary
