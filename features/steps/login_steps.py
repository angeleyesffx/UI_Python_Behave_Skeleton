import time
from behave import *
from nose.tools import assert_equals
from selenium.webdriver.common.by import By
from features.datapool import DATA_ACCESS
from features.object import Singleton
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from features.pages.loginpage import LoginPage



@given(u'I navigate to the Login page')
def navigate_to_login_page(context):
    loginPage = Singleton.getInstance(context, LoginPage)
    time.sleep(5)

@when(u'I fill the credentials from {user}')
def search_for(context, user):
    loginPage = Singleton.getInstance(context, LoginPage)
    element = WebDriverWait(context.browser, 360).until(EC.presence_of_element_located((By.CSS_SELECTOR, loginPage.card_box_layout)))
    email_field = context.browser.find_element_by_id(loginPage.email_field).send_keys(context.user)
    password_field = context.browser.find_element_by_id(loginPage.password_field).send_keys(context.password)
    context.browser.find_element_by_id(loginPage.sign_in_button).click()


@then(u'I should see the my home page')
def get_results(context):
    loginPage = Singleton.getInstance(context, LoginPage)
    assert context.browser.find_element_by_css_selector(loginPage.first_result).text, "Download Python | Python.org"
