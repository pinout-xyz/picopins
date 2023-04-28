def test_setup(test):
    assert test is None


def test_version():
    import PROJECT_NAME
    assert PROJECT_NAME.__version__ == '0.0.1'
