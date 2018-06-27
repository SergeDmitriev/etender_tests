import json
from requests import post



### Functional block for fixtures ###
# TODO: guess its a bad way
from core.etender_data import homePage

def get_prozorro_home_page_function():
    """cut /# from url"""
    return homePage.get('QA', {}).get('ProzorroQA')[:-2]

def get_cookies_function(login, password):
    request = post(url=get_prozorro_home_page_function() + 'Account/Login',
                   data={"UsernameOrEmailAddress": login,
                         "Password": password})
    return request.headers['Set-Cookie']

def set_headers_function(login, password):
    """:return dict"""
    headers = {"Content-Type": "application/json; charset=utf-8", 'Cookie': get_cookies_function(login, password)}
    return headers


### OOP block for test ###
class BaseApiTestLogic(object):
    base_url = get_prozorro_home_page_function()

    empty_body_request = json.dumps({"": ''})

    def get_cookies(self, login, password):
        return get_cookies_function(login, password)

    @staticmethod
    def set_headers(login, password):
        headers = set_headers_function(login, password)
        return headers

    def check_success_status(self, request):
        """Check json.loads(request.content) status"""

        if isinstance(request, bytes):
            request = request.decode("utf-8")
        elif isinstance(request, dict):
            request = json.dumps(request)
        else:
            raise TypeError

        if '"success": true' in request or '"success":true' in request:
            return True
        elif '"success": false' in request or '"success":false' in request:
            return False
        else:
            raise TypeError


if __name__ == "__main__":
    pass
