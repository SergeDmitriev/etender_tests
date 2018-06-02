from requests import post



### Functional block for fixtures ###
# TODO: guess its a bad way
from core.etender_data import homePage

def get_prozorro_home_page_function():
    """cut /# from url"""
    return homePage.get('QA', {}).get('ProzorroQA')[:-2]

def get_cookies_function():
    request = post(url=get_prozorro_home_page_function() + 'Account/Login',
                   data={"UsernameOrEmailAddress": "divisionAdmin@division.com",
                         "Password": "Qq123456"})
    return request.headers['Set-Cookie']

def set_headers_function():
    """:return dict"""
    headers = {"Content-Type": "application/json; charset=utf-8", 'Cookie': get_cookies_function()}
    return headers


### OOP block for test ###
class BaseApiTestLogic(object):
    base_url = get_prozorro_home_page_function()

    def get_cookies(self):
        return get_cookies_function()

    def set_headers(self):
        return set_headers_function()


if __name__ == "__main__":
    pass
