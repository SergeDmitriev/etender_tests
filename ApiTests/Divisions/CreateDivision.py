import json

import requests
from requests import post


def get_cookie():
    request = post(url='http://52.138.214.244/Account/Login',
                   data={"UsernameOrEmailAddress": "divisionAdmin@division.com",
                         "Password": "Qq123456",
                         "returnUrl": "#/MyTenders"})
    return request.headers['Set-Cookie']


def set_headers():
    return {"Content-Type": "application/json; charset=utf-8", 'Cookie': get_cookie()}


def create_division():
    request = post(url='http://52.138.214.244/api/services/etender/division/CreateDivision',
                   headers=set_headers(),
                   data="""{"Title": "TestDivisionCreationNew"}""")
    assert b'success":true' in request.content
    # d = dict(toks)
    return request.content


def update_division():
    pass


if __name__ == '__main__':
    print(create_division())
