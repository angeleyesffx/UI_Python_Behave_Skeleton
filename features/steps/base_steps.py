from behave import *
from features.object import Singleton
from features.pages.basepage import BasePage
import requests
import xml.etree.ElementTree


@given(u'a request to the API')
def _endpoint(context):
    return context.api_url


@then(u'the response status is {code_status}')
def response_status(context, code_status):
    assert context.response.status_code == int(code_status)


@then(u'the response should content the key {key}')
def response_content_key(context, key):
    context.key = BasePage.key_exists(context, key)
    assert context.key is True


@then(u'the response should content a key {key} with the value {value}')
def response_content_key_with_value(context, key, value):
    value = BasePage.value_isCorrect(context, key, value)
    assert value is True


@then(u'the response should content a key {key} with some value different the null')
def response_content_key_different_null(context, key):
    context.value = context.json[key]
    assert context.value is not None
