from requests import post


class BaseApiTestLogic(object):
    base_url = 'http://52.138.214.244/'

    @classmethod
    def get_cookies(cls):
        request = post(url=cls.base_url +'Account/Login',
                       data={"UsernameOrEmailAddress": "divisionAdmin@division.com",
                             "Password": "Qq123456",
                             "returnUrl": "#/MyTenders"})
        return request.headers['Set-Cookie']

    @classmethod
    def set_headers(cls):
        """:return dict"""
        headers = {"Content-Type": "application/json; charset=utf-8", 'Cookie': cls.get_cookies()}
        return headers
