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


def page_switch_times(count_all_records):
    """Method helps to define, how many times we should switch between pages
     {"Page": 1, "PageSize": 10}"""
    def cycle_times(items_count):
        i = 0
        j = 0
        if items_count > 10:
            if items_count % 10 > 0:
                i = items_count // 10 + 1
            else:
                i = items_count // 10
                print(i)
        elif 0 < items_count <= 10:
            i = 1
        elif items_count == 0:
            pass

        for j in range(i):
            j += 1
        return j

    for x in range(1, cycle_times(count_all_records)+1):
        yield x


if __name__ == '__main__':
    pass

