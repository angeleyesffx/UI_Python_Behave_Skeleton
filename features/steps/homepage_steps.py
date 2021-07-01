import time
from behave import *
from nose.tools import assert_equals
from selenium.webdriver.common.by import By
from features.datapool import DATA_ACCESS
from features.object import Singleton

from features.pages.homepage import HomePage


@given(u'I navigate to the Google Home page')
def navigate_to_home_page(context):
    home = Singleton.getInstance(context, HomePage)
    time.sleep(5)
    assert_equals(context.browser.current_url, "{}".format(home.project_url))


@when(u'I search for {search_data}')
def search_for(context, search_data):
    home = Singleton.getInstance(context, HomePage)
    search_bar = context.browser.find_element_by_name(home.search_bar)
    search_bar.clear()
    search_bar.send_keys(search_data)
    context.browser.find_element_by_css_selector(home.search_button).click()

@then(u'I should see the results')
def get_results(context):
    home = Singleton.getInstance(context, HomePage)
    assert_equals(context.browser.find_element_by_css_selector(home.first_result).text, "Welcome to Python.org")

