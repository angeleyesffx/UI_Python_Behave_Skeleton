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
def step_impl(context):
    raise NotImplementedError(u'STEP: When I search for "blabla"')


@then(u'I should see the results')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should see the results')
