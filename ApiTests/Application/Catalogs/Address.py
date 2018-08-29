import random
from requests import post

from ApiTests.Helpers import dict_to_json, body_to_dict
from tools.data_generator import generate_street_name, generate_post_index


class Address:

    def __init__(self, user_obj):
        self.user = user_obj

    def get_regions_by_country_id(self, country_id=1):
        """on default = 1 (Ukraine), returns list of regions in country"""
        request = post(url=self.user.base_url + 'api/services/etender/reference/GetRegionsByCountryId',
                       headers=self.user.headers,
                       data=dict_to_json({"countryId": country_id}))
        return body_to_dict(request.content)['result']['regions']

    def get_countries_reg_code_exists(self):
        """list_index=0 = Ukraine default, returns list of countries"""
        request = post(url=self.user.base_url + 'api/services/etender/reference/GetCountriesRegCodeExists',
                       headers=self.user.headers,
                       data=dict_to_json(self.user.empty_body_request))
        return body_to_dict(request.content)['result']['countries']

    def get_cities_by_region_id(self, region_id):
        request = post(url=self.user.base_url + 'api/services/etender/reference/GetCitiesByRegionId',
                       headers=self.user.headers,
                       data=dict_to_json({'regionId': region_id}))
        return body_to_dict(request.content)['result']['cities']

    def get_reg_codes_by_country_id(self, country_code):
        request = post(url=self.user.base_url + 'api/services/etender/reference/GetRegCodesByCountryId',
                       headers=self.user.headers,
                       data=dict_to_json({'countryCode': country_code}))
        return body_to_dict(request.content)['result']['regCodes']

    def get_or_create_address(self, is_random=True, is_new_city=False, address_params=None):
        """address_params: {'country_name': 1, }"""
        data = self.generate_address(is_random, is_new_city, address_params)
        request = post(url=self.user.base_url + 'api/services/etender/address/GetOrCreateAddress',
                       headers=self.user.headers,
                       data=dict_to_json(data))
        return body_to_dict(request.content)['result']['address']['id']

    def generate_address(self, is_random, is_new_city, address_params):
        """custom data: {'country_name': 1, 'region_title': 'Одеська область', 'city_name': 'Болград'}"""
        # TODO: add logic, when user add own city address (is_new_city parameter)
        # list of countries and list of regions(Ukraine default)
        selected_city = None
        country_list = self.get_countries_reg_code_exists()  # get Ukraine
        region_list = self.get_regions_by_country_id()

        if is_new_city:
            pass
        else:
            pass

        if is_random:
            # Set country:
            country_obj = search_by_country_name(country_list, 'Україна')

            # Set region from country list
            region_id = random.choice(region_ids_to_list(region_list))  # select random region id from Ukraine
            selected_region = select_region_by_id(region_list, region_id)  # choose region from list by id

            # Set city from region list
            cities_list = self.get_cities_by_region_id(region_id)

            # костыль, на 2 города, в запросе id берется не ясно от куда
            if not cities_list:
                if selected_region['id'] == 76:
                    selected_city = {"title": "Київ", "regionId": None, "id": 167}
                elif selected_region['id'] == 77:
                    selected_city = {"title": "Севастополь", "regionId": None, "id": 340}
            else:
                city_id = random.choice(cities_ids_to_list(cities_list))
                selected_city = select_city_by_id(cities_list, city_id)

        else:
            country_obj = search_by_country_name(country_list, address_params['country_name'])
            is_ukraine = True if address_params['country_name'] == 'Україна' else False

            if not is_ukraine:
                # region_list = self.get_reg_codes_by_country_id(country_obj.get('code', []))  # Схема не отпр. в БД
                selected_region = {'title': address_params['region_title'], 'id': None}
                selected_city = {'title': address_params['city_name'], 'id': None}
            else:
                selected_region = search_by_region_name(region_list, address_params['region_title'])
                cities_list = self.get_cities_by_region_id(selected_region['id'])
                selected_city = search_by_city_name(cities_list, address_params['city_name'])

        address_str = generate_street_name()
        post_index = generate_post_index()

        output = {
            "country": country_obj,
            "region": selected_region,
            "city": selected_city, "newCity": None,  # {"title": "New City Title"}
            "addressStr": address_str,
            "postIndex": post_index
        }
        return output


def region_ids_to_list(l):
    x = []
    for i in l:
        x.append(i['id'])
    return x


def select_region_by_id(l, region_id):
    region = None
    for i in l:
        if i['id'] == region_id:
            region = i
    return region


def cities_ids_to_list(l):
    x = []
    for i in l:
        x.append(i['id'])
    return x


def select_city_by_id(l, city_id):
    city = None
    for i in l:
        if i['id'] == city_id:
            city = i
    return city


def search_by_country_name(country_list, title):
    obj = None
    for i in country_list:
        if i['title'] == title:
            obj = i
    return obj


def search_by_region_name(region_list, title):
    obj = None
    for i in region_list:
        if i['title'] == title:
            obj = i
    return obj


def search_by_city_name(cities_list, title):
    obj = None
    for i in cities_list:
        if i['title'] == title:
            obj = i
    return obj


if __name__ == '__main__':
    pass

    # data = {'country_name': 'Австралія', 'region_title': 'own_region0', 'city_name': 'CITY0'}
    # data1 = {'country_name': 'Австрія', 'region_title': 'own_region1', 'city_name': 'CITY1'}
    # data2 = {'country_name': 'Україна', 'region_title': 'м. ', 'city_name': 'Болград'}

    # r = a.get_or_create_address(is_random=False, is_new_city=False, address_params=data)
    # print(r)
    #
    # rc = a.get_or_create_address(is_random=False, is_new_city=False, address_params=data1)
    # print(rc)
    #
    # rcu = a.get_or_create_address(is_random=False, is_new_city=False, address_params=data2)
    # print(rcu)
