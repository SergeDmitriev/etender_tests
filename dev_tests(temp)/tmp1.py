
b = [{'id': 38, 'title': 'QA Department'}, {'id': 39, 'title': 'Develop Department'},
     {'id': 40, 'title': 'Support Department'}, {'id': 61, 'title': 'Updated Department Title'}]



if __name__ == '__main__':
    # print(obj_json.get('result').get('id'))
    print(b)
    a = {'id': 61, 'title': 'Updated Department Title'}
    print(a in b)
