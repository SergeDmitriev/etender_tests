# -*- coding: utf-8 -*-
from requests import post

from ApiTests.Application.Catalogs.Address import Address
from ApiTests.Helpers import body_to_dict, dict_to_json
from db_layer.db_application import send_query
from db_layer.sql_queries import select_code_of_organization
from tools.data_generator import generate_code_of_organization, generate_organization_name, generate_phone_number


class Organization:

    def __init__(self, user):
        self.user_obj = user  # user = User()

    def get_organization(self, tenant_id):
        request = post(url=self.user_obj.base_url + 'api/services/etender/organization/GetOrganization',
                       headers=self.user_obj.headers,
                       data=dict_to_json({'tenantId': tenant_id}))
        return body_to_dict(request.content)

    def is_organization_registered(self, tenant_name):
        request = post(url=self.user_obj.base_url + 'api/services/etender/organization/IsOrganizationRegistered',
                       headers=self.user_obj.headers,
                       data=dict_to_json({"tenantName": str(tenant_name)}))
        assert True is body_to_dict(request.content)['success']
        return body_to_dict(request.content)['result']

    def update_or_create_organization(self, organization_data):
        data = {"addressId": organization_data['address_id'],
                "codeOfOrganization": organization_data['code_of_organization'],
                "organizationKindId": organization_data['organization_kind_id'],
                "name": organization_data['name'],
                "nameEN": organization_data['name_en'],
                "isCustomer": organization_data['is_customer'],
                "shortName": organization_data['short_name'],
                "typeOfOrganization": organization_data['type_of_organization'],
                "userName": organization_data['user_name'],
                "phone": organization_data['phone'],
                "fax": organization_data['fax'],
                "url": organization_data['url'],
                "contactEmail": organization_data['contact_email'],
                "userId": organization_data['user_id'],
                "isVatPayer": organization_data['is_vat_payer'],
                "vatNumber": organization_data['vat_number'],
                "schemeId": organization_data['scheme_id'],
                "kinds": organization_data['kinds'],
                "sKind": organization_data['s_kind'],
                "parentCodeEDRPOU": organization_data['parent_code_EDRPOU'],
                "parentId": organization_data['parent_id'],
                "directorFirstName": organization_data['director_first_name'],
                "directorLastName": organization_data['director_last_name'],
                "directorPatronymic": organization_data['director_patronymic'],
                "documentWayType": organization_data['document_way_type'],
                "confirmOrg": organization_data['confirm_org'],
                "directorId": organization_data['director_id'],
                "contactPointId": organization_data['contact_point_id']}

        request = post(url=self.user_obj.base_url + 'Account/UpdateOrCreateOrganization',
                       headers=self.user_obj.headers,
                       data=dict_to_json(data))
        assert True is body_to_dict(request.content)['success']
        return body_to_dict(request.content)['result']

    def create_or_update_contact_point(self, user_obj):
        request = post(url=self.user_obj.base_url + 'api/services/etender/organization/CreateOrUpdateContactPoint',
                       headers=self.user_obj.headers,
                       data=dict_to_json({"fio": {"firstName": user_obj.data['Name'],
                                                  "lastName": user_obj.data['Surname']},
                                          "email": user_obj.data['EmailAddress'],
                                          "telephone": user_obj.data['Phone'],
                                          "name": user_obj.data['Name'] + ' ' + user_obj.data['Surname']}))
        print(body_to_dict(request.content)['result'])
        return body_to_dict(request.content)['result']['id']

    def generate_random_data(self, org_type, is_customer=True, selected_kind=1):
        """
        :param org_type: 'Фізична особа' or 'Юридична особа' or 'Нерезидент'
        :param is_customer: default value = True for legal_entity as Customer
        :param selected_kind:
        kinds = [{"title": "Замовник (загальний)", "code": 1},
             {"title": "Замовник, що здійснює діяльність в окремих сферах господарювання", "code": 3},
             {"title": "Замовник, що здійснює закупівлі для потреб оборони", "code": 2},
             {"title": "Державні та комунальні підприємства, які не є замовниками в розумінні Закону", "code": 4}]
        """

        o = OrganizationDataForRegistration(self.user_obj)

        if org_type == 'Фізична особа':
            a = o.generate_fop_data()
            try:
                b = send_query(select_code_of_organization(a['code_of_organization']))[0][0]
            except:
                b = []
            while a['code_of_organization'] == b:
                a = o.generate_fop_data()
            return a

        elif org_type == 'Юридична особа':
            a = o.generate_legal_data(is_customer=is_customer, s_kind=selected_kind)
            try:
                b = send_query(select_code_of_organization(a['code_of_organization']))[0][0]
            except:
                b = []
            while a['code_of_organization'] == b:
                a = o.generate_legal_data(is_customer=is_customer, s_kind=selected_kind)
            return a

        elif org_type == 'Нерезидент':
            return o.generate_non_resident_data()
        else:
            print('Некорректный тип организации')
            raise TypeError


class OrganizationDataForRegistration:
    kinds = [{"title": "Замовник (загальний)", "code": 1},
             {"title": "Замовник, що здійснює діяльність в окремих сферах господарювання", "code": 3},
             {"title": "Замовник, що здійснює закупівлі для потреб оборони", "code": 2},
             {"title": "Державні та комунальні підприємства, які не є замовниками в розумінні Закону", "code": 4}]

    def __init__(self, user_obj):
        self._user = user_obj
        self._address_obj = Address(self._user)
        self.address_id = None
        self.code_of_organization = None
        self.organization_kind_id = None
        self.name = None
        self.name_en = None
        self.is_customer = None
        self.short_name = None
        self.type_of_organization = None
        self.user_name = None
        self.phone = None
        self.fax = None
        self.url = None
        self.contact_email = None
        self.user_id = None
        self.is_vat_payer = None
        self.vat_number = None
        self.scheme_id = None
        self.kinds = self.kinds
        self.s_kind = None  # {"title":"Замовник (загальний)","code":1}
        self.parent_code_EDRPOU = None
        self.parent_id = None
        self.document_way_type = None
        self.confirm_org = None
        self.director_id = None
        self.director_first_name = None
        self.director_last_name = None
        self.director_patronymic = None
        self.contact_point_id = None

    def get_obj(self):
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    def generate_base_data(self):
        self.address_id = self._address_obj.get_or_create_address()
        self.name = generate_organization_name()
        self.name_en = None
        self.confirm_org = True
        self.document_way_type = "paper"
        self.short_name = None
        self.is_vat_payer = False  # Also could be True + vat_number
        self.vat_number = None
        self.phone = generate_phone_number()
        self.fax = None
        self.url = None
        self.parent_code_EDRPOU = None
        self.parent_id = 0
        self.user_name = self._user.email_address
        self.user_id = self._user.data['id']
        self.contact_point_id = Organization(self._user).create_or_update_contact_point(self._user)

    def generate_fop_data(self):
        self.generate_base_data()
        self.type_of_organization = 1
        self.code_of_organization = generate_code_of_organization(2)
        self.organization_kind_id = 1
        self.s_kind = self.kinds[0]
        self.is_customer = False
        self.scheme_id = 36
        self.contact_email = None
        self.director_id = None
        self.director_first_name = None
        self.director_last_name = None
        self.director_patronymic = None
        return self.get_obj()

    def generate_legal_data(self, is_customer, s_kind):
        self.generate_base_data()
        self.is_customer = is_customer

        if s_kind == 1:
            self.s_kind = self.kinds[0]
        elif s_kind == 2:
            self.s_kind = self.kinds[2]
        elif s_kind == 3:
            self.s_kind = self.kinds[1]
        elif s_kind == 4:
            self.s_kind = self.kinds[3]

        self.is_customer = is_customer
        self.type_of_organization = 2
        self.code_of_organization = generate_code_of_organization(1)
        self.organization_kind_id = self.s_kind['code']
        self.scheme_id = 36
        return self.get_obj()

    def generate_non_resident_data(self):
        self.generate_base_data()
        self.type_of_organization = self.type_of_organization['Нерезидент']
        self.code_of_organization = generate_code_of_organization(self.type_of_organization['Нерезидент'])
        self.organization_kind_id = 1
        self.is_customer = False
        return self.get_obj()


if __name__ == '__main__':
    pass
