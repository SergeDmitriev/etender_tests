import requests
from requests import post


def login_and_get_cookie():
    request_url = 'http://52.138.214.244/Account/Login'
    resp = post(request_url, data={"UsernameOrEmailAddress":"divisionAdmin@division.com",
                                   "Password":"Qq123456",
                                   "returnUrl":"#/MyTenders"})
    a = str(requests.utils.dict_from_cookiejar(resp.cookies))
    return 'Cookie: ' + a[2:-2]


def json_to_body():
    body_request = """{"page":1,"pageSize":10,"orderColumn":"","orderDirection":"desc","searchFilter":
    {"statuses":["active.enquiries","active.tendering","active.pre-qualification",
    "active.pre-qualification.stand-still","active.stage2.pending","active.stage2.waiting","active.auction",
    "active.qualification","active.awarded"],"userName":"case7","priceFrom":null,"priceTo":null,"tendersKind":"",
    "procurementMethod":"open","procurementMethodTypes":[],"isStasusesDefaulted":true,"cpvs":[],"dkpp":null,
    "title":null,"organizationName":null,"tenderPeriodEndFrom":"","tenderPeriodEndTo":"","tenderCreationTimeFrom":"",
    "tenderCreationTimeTo":"","tenderPeriodStartFrom":"","tenderPeriodStartTo":"","customerRegion":"",
    "parentCodesEDRPOU":null,"funderId":null},"searchIdentifier":null,"fieldsForCustomer":true}"""
    return body_request


def get_tenders():
    request_url = 'http://52.138.214.244/api/services/etender/tender/GetTenders'
    content_type = {"Content-Type": "application/json; charset=utf-8",
                    'Cookie': login_and_get_cookie()}
    resp = requests.post(url=request_url, headers=content_type, data=json_to_body())
    assert b'{"success":true,"result":{"tender":[{"id":' in resp.content
    return resp.content



if __name__ == '__main__':
    print(get_tenders())















