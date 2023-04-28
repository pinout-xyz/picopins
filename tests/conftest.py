import pytest


@pytest.fixture(scope='function', autouse=False)
def test():
    yield None
