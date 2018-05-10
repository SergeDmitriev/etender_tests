import json
import pytest
import requests
from requests import post


def get_cookie():
    """:return string value"""
    request = post(url='http://52.138.214.244/Account/Login',
                   data={"UsernameOrEmailAddress": "divisionAdmin@division.com",
                         "Password": "Qq123456",
                         "returnUrl": "#/MyTenders"})
    return request.headers['Set-Cookie']


def set_headers():
    return {"Content-Type": "application/json; charset=utf-8", 'Cookie': get_cookie()}


def create_division(division_name):
    """:return id of created obj"""
    request = post(url='http://52.138.214.244/api/services/etender/division/CreateDivision',
                   headers=set_headers(),
                   data=json.dumps({"title": division_name}))
    assert b'success":true' in request.content
    return json.loads(request.content).get('result').get('id')


def update_division(id, new_division_title):
    """:return list: id, title of updated object
        if error: return server answer
    example: [62, 'Updated Department Title']"""
    request = post(url='http://52.138.214.244/api/services/etender/division/UpdateDivision',
                            headers=set_headers())
                            # data=json.dumps({"id":id, "title":new_division_title}))

    try:
        assert b'success":true' in request.content
        return [json.loads(request.content).get('result').get('id'),
                json.loads(request.content).get('result').get('title')]
    except AssertionError:
        assert json.loads(request.content).get('error').get('message') == 'Division is not in your organization'
        return json.loads(request.content)

def get_division(params=None):

    if params is None:
        body = json.dumps({"": ''})
        case = 1
    elif params == 'paging':
        body = json.dumps({"Page":1,"PageSize":10})
        case = 2
    else:
        body = ''
        case = 3

    request = post(url='http://52.138.214.244/api/services/etender/division/GetDivisions',
                            headers=set_headers(),
                            data=body)
    if case == 1:
        assert json.loads(request.content).get('result').get('totalCount') >= 1
    elif case == 2:
        assert len(json.loads(request.content).get('result').get('items')) == 10
    return json.loads(request.content)



# def delete_division():
#     request = post(url='')


if __name__ == '__main__':
    # print(create_division('QA Department'))
    # print(create_division('Develop Department'))
    # print(create_division('Support Department'))
    # print(create_division('Sales Department'))
    # print(create_division('Test Department'))
    # division_id = create_division('Test Department')

    # division_id = 61
    # division_id_not_existed = 62
    # division_id_not_in_my_organization = 1
    # print(update_division(division_id, 'Updated Department Title'))
    # print(update_division(division_id_not_existed, "Division title not updated"))
    # print(update_division(division_id_not_in_my_organization, "Division title not updated"))
    print(get_division())
    print(get_division('paging'))

    # print(get_cookie())

