from behave import *
from nose.tools import assert_equals
from selenium.webdriver.common.by import By
from features.datapool import DATA_ACCESS

from features.pages.basepage import BasePage
from features.pages.homepage import HomePage


@given(u'I navigate to the Google Home page')
def navigate_to_home_page(context):
    context.home_page = BasePage.instance_page(HomePage,context)
    assert_equals(context.browser.current_url, "{}".format(context.home_page.project_url))


@when(u'I search for {search_data}')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I search for "blabla"')


@then(u'I should see the results')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should see the results')
