from core import config


def visit(url):
    config.browser.get(url)

def refresh():
    config.browser.refresh()

def get_url():
    config.browser.current_url()