import json


def update_keys(dictionary, old_key, new_key):
    """swap key name in dict, cause .get() may fail (userid != userId)"""
    dictionary[new_key] = dictionary.pop(old_key)
    return dictionary


def body_to_dict(string_query):
    """convert string(contains JSON object) to python dictionary
    string_query - string, which contains JSON object"""
    return json.loads(string_query)


def dict_to_json(body):
    """convert python dictionary to string in JSON format
    body - dict"""
    return json.dumps(body)


def set_ids_for_fixture(input_data):
    """input_data must be list of dict, where key='test_name'"""
    result_list = []
    [result_list.append(input_data[i]['test_name']) for i in range(len(input_data))]
    return result_list


if __name__ == '__main__':
    pass

