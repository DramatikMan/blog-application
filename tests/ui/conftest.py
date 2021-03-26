import pytest


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_experimental_option('w3c', False)
    return chrome_options
