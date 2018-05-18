import pytest


@pytest.fixture()
def create_division(request):
    print('SetUP')
    def delete_division():
        print('teardown')
    request.addfinalizer(delete_division)
