from requests import post
from ApiTests.etender_data_api import base_prozorro_url


### Functional block for fixtures ###
# TODO: guess its a bad way
def get_cookies_function():
    request = post(url=base_prozorro_url + 'Account/Login',
                   data={"UsernameOrEmailAddress": "divisionAdmin@division.com",
                         "Password": "Qq123456",
                         "returnUrl": "#/MyTenders"})
    return request.headers['Set-Cookie']

def set_headers_function():
    """:return dict"""
    headers = {"Content-Type": "application/json; charset=utf-8", 'Cookie': get_cookies_function()}
    return headers


### OOP block for test ###
class BaseApiTestLogic(object):
    base_url = base_prozorro_url

    @classmethod
    def get_cookies(cls):
        return get_cookies_function()

    @classmethod
    def set_headers(cls):
        return set_headers_function()

    def set_headers1(self):
        BaseApiTestLogic.get_cookies()
