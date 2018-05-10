from collections import namedtuple
import json
a = b'{"success":true,"result":{"id":49,"title":"Support Department"},"error":null,"unAuthorizedRequest":false}'

obj_json = json.loads(a)




b = {'success': True, 'result': {'totalCount': 11, 'items': [{'id': 38, 'title': 'QA Department'},
                                {'id': 39, 'title': 'Develop Department'}, {'id': 40, 'title': 'Support Department'},
                                {'id': 61, 'title': 'Updated Department Title'},
                                {'id': 63, 'title': 'Sales Department'}, {'id': 64, 'title': 'Sales Department'},
                                {'id': 65, 'title': 'Sales Department'}, {'id': 66, 'title': 'Sales Department'},
                                {'id': 67, 'title': 'Sales Department'}, {'id': 68, 'title': 'Sales Department'}]},
                                'error': None, 'unAuthorizedRequest': False}




if __name__ == '__main__':
    # print(obj_json.get('result').get('id'))
    print(len(b.get('result').get('items')))
