# import json
# import pytest
# from requests import post
#
# from ApiTests.BaseApiTestLogic import set_headers_function
# from ApiTests.Divisions.Division import CreateDivision
# from ApiTests.etender_data_api import base_prozorro_url


# @pytest.yield_fixture()
# def precondition_create_division():
#
#     # request_create = post(url=base_prozorro_url + 'api/services/etender/division/CreateDivision',
#     #                headers= set_headers_function(),
#     #                data=json.dumps({"title": 'Division created in precondition'}))
#     # division_data = json.loads(request_create.content).get('result')
#     division_data = CreateDivision.precondition_create_division()
#     yield division_data
#     print('code after', division_data)
#     request_delete = post(url=base_prozorro_url + 'api/services/etender/division/DeleteDivision',
#                    headers=set_headers_function(),
#                    data=json.dumps({"id": division_data.get('id')}))
#     print('End fixture', request_delete.content)
