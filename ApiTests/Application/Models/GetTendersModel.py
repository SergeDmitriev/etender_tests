from ApiTests.Helpers import dict_to_json
from ApiTests.app_config import production_mode


class GetTendersModel:

    def __init__(self, tab, is_production_mode=production_mode, is_real_tenders_for_test_mode=False, page_number=1):
        if is_production_mode:
            is_production_mode = True

        if tab == 'competitive':
            procurement_method_value = 'open'
            statuses_values = ['active.enquiries',
                               'active.tendering',
                               'active.pre-qualification',
                               'active.pre-qualification.stand-still',
                               'active.stage2.pending',
                               'active.stage2.waiting',
                               'active.auction',
                               'active.qualification',
                               'active.awarded',
                               'unsuccessful',
                               'complete',
                               'cancelled']
        elif tab == 'noncompetitive':
            procurement_method_value = 'limited'
            statuses_values = ['active',
                               'unsuccessful',
                               'complete',
                               'cancelled']
        else:
            raise KeyError

        if is_real_tenders_for_test_mode:
            is_real_tenders_for_test_mode = True

        self.Page = page_number
        self.PageSize = 10
        self.OrderColumn = ''
        self.OrderDirection = 'desc'
        self.SearchFilter = {'PriceFrom': None,
                             'PriceTo': None,
                             'ProcurementMethod': procurement_method_value,
                             'procurementMethodTypes': [],
                             'regions': [],
                             'Statuses': statuses_values,
                             'IsStasusesDefaulted': False,
                             'Cpvs': [],
                             'Dkpp': None,
                             'isProductionMode': is_production_mode,
                             'parentCodesEDRPOU': [],
                             'codeEDRPOUs': None,
                             'Title': None,
                             'OrganizationName': None,
                             'FunderId': None,
                             'searchTimeType': None,
                             'tenderPeriodEndFrom': None,
                             'tenderPeriodEndTo': None,
                             'tenderCreationTimeFrom': None,
                             'tenderPeriodStartFrom': None,
                             'tenderPeriodStartTo': None,
                             'CustomerRegion': None,
                             'isShowOnlyTendersCreatedOnOurSite': False,
                             'IsRealTendersForTestMode': is_real_tenders_for_test_mode}
        # self.searchIdentifier = None,
        self.includeFavorite = True

    def get_request_body(self):
        return dict_to_json(vars(self))


class GetTendersWithResponsiblesModel(GetTendersModel):
    def __init__(self, **params):
        tab = 'competitive'
        super().__init__(tab, **params)
        self.SearchFilter['IsUseDefaultFilter'] = True
        self.SearchFilter['IsStasusesDefaulted'] = True
        self.SearchFilter['Statuses'] = ['active.enquiries',
                                         'active.tendering',
                                         'active.pre-qualification',
                                         'active.pre-qualification.stand-still',
                                         'active.stage2.pending',
                                         'active.stage2.waiting',
                                         'active.auction',
                                         'active.qualification',
                                         'active.awarded']
        self.SearchFilter['ResponsibleUsersFilter'] = [
            {'AllUsersFromMyOrg': False, 'ToMeAsHead': False, 'ToMeAsManager': False}
        ]

    def set_tenders_in_work_params(self):
        self.SearchFilter['IsUseDefaultFilter'] = None
        self.SearchFilter['ResponsibleUsersFilter'] = \
            {'AllUsersFromMyOrg': None, 'ToMeAsHead': True, 'ToMeAsManager': True}

    def set_tenders_archive_params(self):
        self.set_tenders_in_work_params()
        self.SearchFilter['Statuses'] = ['unsuccessful', 'complete', 'cancelled']


if __name__ == '__main__':
    pass
