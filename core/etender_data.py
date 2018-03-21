homePage = {'QA': {'ProzorroQA':'http://52.164.252.138/#/',
                   'RialtoQA': 'http://rialto.qa.e-tender.ua/#/',
                   'RialtoAuctionQA': 'http://rialtoauction.qa.e-tender.ua/#/',
                   'RialtoClosedQA': 'http://rialtoclosed.qa.e-tender.ua/#/'},
            'UAT':{'ProzorroUAT':'http://bid.uat.e-tender.biz/#/',
                   'RialtoUAT':None,
                   'RialtoAuctionUAT':'http://rialtoauction.uat.e-tender.ua/#/',
                   'RialtoClosedUAT': None}}

user_roles = {'owner': 'owner',
              'viewer1': 'viewer1',
              'viewer2': 'viewer2',
              'anonym': 'anonym',}

owner_users = {'username': 'case6',
               'password': 'Qq123456'}

viewer_users = {'username': 'case7',
                'password': 'Qq123456'}

# TODO: make dict inside dict for users

project_titles = {'TitleProzorro': 'Державні закупівлі',
                  'TitleRialto': 'Комерційні торги',
                  'TitleRialtoAuction':'Комерційні торги'}



class BaseProjectData(object):

    def __init__(self, home_page, page_title, owner_username, owner_password, viewer_username, viewer_password):
        self.home = home_page
        self.title = page_title
        self.owner_username = owner_username
        self.owner_password = owner_password
        self.viewer_username = viewer_username
        self.viewer_password = viewer_password


class ProzorroData(BaseProjectData):



    home = homePage.get('UAT', {}).get('ProzorroUAT')
    title = project_titles.get('TitleProzorro')
    owner_username = owner_users.get('username')
    owner_password = owner_users.get('password')
    viewer_username = viewer_users.get('username')
    viewer_password = viewer_users.get('password')


class RialtoData(BaseProjectData):
    def __init__(self):
        pass

    home = homePage.get('QA', {}).get('RialtoQA')
    title = project_titles.get('TitleRialto')
    owner_username = owner_users.get('username')
    owner_password = owner_users.get('password')
    viewer_username = viewer_users.get('username')
    viewer_password = viewer_users.get('password')


class RialtoAuctionData(BaseProjectData):
    home = homePage.get('QA', {}).get('RialtoAuctionQA')
    title = project_titles.get('TitleRialtoAuction')
    owner_username = owner_users.get('username')
    owner_password = owner_users.get('password')
    viewer_username = viewer_users.get('username')
    viewer_password = viewer_users.get('password')