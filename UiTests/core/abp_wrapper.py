from UiTests.core.browser_wrapper import s


def toastr():

    s('#toast-container div.toast toast-info') #info Видалено з обраного
    # s('#toast-container div.toast toast-warning div.toast-message')  # success Було створено чернетку пропозиції!
    # s('#toast-container div.toast toast-success')  # success Додано до обраного


    # s('div.toast-message').assure(text, "Додано до обраного")


