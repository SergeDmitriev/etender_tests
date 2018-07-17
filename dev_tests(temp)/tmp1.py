import requests
from requests import post

b = [{'id': 38, 'title': 'QA Department'}, {'id': 39, 'title': 'Develop Department'},
     {'id': 40, 'title': 'Support Department'}, {'id': 61, 'title': 'Updated Department Title'}]

base_url = 'http://52.138.214.244/'

def get_cookies():
    request = post(url=base_url + 'Account/Login',
                   data={"UsernameOrEmailAddress": "divisionAdmin@division.com",
                         "Password": "Qq123456",
                         "returnUrl": "#/MyTenders"})
    return request.headers['Set-Cookie']

def get_tenders():
    request_url = 'ApiTests/services/etender/tender/GetTenders'
    content_type = {"Content-Type": "application/json; charset=utf-8",
                    'Cookie': get_cookies()}
    resp = requests.post(url=request_url, headers=content_type, data=json_to_body())
    assert b'{"success":true,"result":{"tender":[{"id":' in resp.content
    return resp.content


if __name__ == '__main__':
    # print(obj_json.get('result').get('id'))
    print(b)
    a = {'id': 61, 'title': 'Updated Department Title'}
    print(a in b)
