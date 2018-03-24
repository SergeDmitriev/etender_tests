from core.browser_wrapper import visit, get_curl, s
from core.conditions import clickable

#unnecessary implementationS
# def print_to_console_username(login):
#         ("Current user is: ", login)
#
# def create_owner(username, password):
#     from core.managers import OwnerManager
#     owner = OwnerManager("owner", username, password)
#     print_to_console_username(owner.username)
#     return owner
#
# def create_viewer(username, password):
#     from core.managers import ViewerManager
#     viewer = ViewerManager("owner", username, password)
#     print_to_console_username(viewer.username)
#     return viewer

def check_bidButton_for_anonym(home):
    visit(home)
    s('a .bidButton-fixed cp ng-scope').assure(clickable).click()
    assert get_curl() == home + 'register'
