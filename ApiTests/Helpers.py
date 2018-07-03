
def update_keys(dictionary, old_key, new_key):
    dictionary[old_key] = dictionary.pop(new_key)
    return dictionary