from behave import *
from features.steps.data_source.some_datasource import DATA_REQUEST
from features.pages.base_page import BasePage
import requests
from requests.auth import HTTPBasicAuth
import os
import xml.etree.ElementTree as ET

@given(u'a request to the Some API')
def get_some_endpoint(context):
    context.endpoint = "{0}{1}".format(context.api_url, "/Some_path")
    return context.endpoint


@when(u'the request sends POST to the ESP Quod Report API with a')
def send_post_some_request(context):
    context.endpoint = get_some_endpoint(context)
    payload = BasePage.read_xml_file(os.path.dirname(__file__) + '\\data_source\\some.xml')
    context.response = requests.post(context.endpoint, auth=HTTPBasicAuth(context.username, context.password), data=payload.format(), headers={'Content-Type': 'text/xml'}, verify=False)
    return context.response_some_api

@then(u'the response form Some API should be equal on API Whatever')
def response_content_key_with_value(context):
    context.some_api = BasePage.find_value_on_xml(context.response_some_api, 'some_tag_key_xml')
    context.whatever_api = BasePage.find_value_on_xml(context.response_whatever, 'some_tag_key_xml')
    assert context.some_api == context.whatever_api
