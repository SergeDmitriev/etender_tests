import pytest


@pytest.mark.usefixtures("setup")
class BaseTest(object):
    pass


class BaseOwnerTest(BaseTest):
    pass


class BaseViewerTest(BaseTest):
    pass