import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_experimental_option('w3c', False)
    return chrome_options


def test_submit_comment(app, client, selenium):
    selenium.get('http://localhost:5000/blog/post/100')

    comment_form = selenium.find_element(By.ID, 'comment_form')
    name_field = comment_form.find_element_by_name('name')
    text_field = comment_form.find_element_by_name('text')

    name_field.send_keys('tester' + Keys.RETURN)
    text_field.send_keys('Example comment' + Keys.RETURN)

    submit_button = comment_form.find_element_by_id('submit')
    submit_button.click()

    assert 'By: tester on' in selenium.page_source
    assert 'Example comment' in selenium.page_source
