from behave import *
from nose.tools import assert_equals

from features.pages.basepage import BasePage
from features.pages.homepage import HomePage


@given(u'I navigate to the Google Home page')
def navigate_to_home_page(context):
    # context.browser.get("http://google.com")
    assert_equals(context.browser.current_url, "{}".format(context.home_page.project_url))
    raise NotImplementedError(u'STEP: Given I navigate to the Google Home page')


@when(u'I search for "blabla"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I search for "blabla"')


@then(u'I should see the results')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should see the results')
