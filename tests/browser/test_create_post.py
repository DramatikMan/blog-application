from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def test_login(selenium):
    selenium.get('http://localhost:5000/login')
    assert selenium.title == 'Login'

    # username_field = selenium.find_element(By.NAME, 'username')
    # username_field.send_keys('Random_User' + Keys.RETURN)
    #
    # password_field = selenium.find_element(By.NAME, 'password')
    # password_field.send_keys('no_brute_force_please' + Keys.RETURN)
    #
    # login_button = selenium.find_element(By.CSS_SELECTOR, '[type="Submit"]')
