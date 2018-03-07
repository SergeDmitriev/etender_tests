from core import config


def visit(url):
    config.browser.get(url)


def refresh():
    config.browser.refresh()


def get_curl():
    return config.browser.current_url


def close():
    config.browser.close()
