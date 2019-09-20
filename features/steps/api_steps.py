from behave import *
from features.steps.data_source.some_datasource import DATA_REQUEST
from features.pages.base_page import BasePage
import requests
from requests.auth import HTTPBasicAuth
import os
import xml.etree.ElementTree as ET

@given(u'a request to the Some API')
def get_some_endpoint(context):
    context.endpoint_some_api = "{0}{1}".format(context.some_api_url, "/Some_path")
    return context.endpoint_some_api


@given(u'a request to the Whatever API')
def get_whatever_endpoint(context):
    context.endpoint_whatever = "{0}{1}".format(context.whatever_url, "/Whatever_path")
    return context.endpoint_whatever


@when(u'the request sends POST to the Whatever API with a <body>')
def send_post_whatever_request(context, body):
    context.endpoint_whatever = get_whatever_endpoint(context)
    payload_whatever = BasePage.read_xml_file(os.path.dirname(__file__) + '\\data_source\\whatever.xml')
    context.response_whatever = requests.post(context.endpoint_whatever, auth=HTTPBasicAuth(context.username_whatever, context.password_whatever), data=payload_whatever.format(), headers={'Content-Type': 'text/xml'}, verify=False)
    return context.response_whatever


@when(u'the request sends POST to the Some API with a <body>')
def send_post_some_request(context, body):
    context.endpoint_some_api = get_some_endpoint(context)
    payload_some = BasePage.read_xml_file(os.path.dirname(__file__) + '\\data_source\\some.xml')
    context.response = requests.post(context.endpoint_some_api, auth=HTTPBasicAuth(context.username, context.password), data=payload_some.format(), headers={'Content-Type': 'text/xml'}, verify=False)
    return context.response_some_api


@then(u'the response form Some API should be equal on API Whatever')
def response_content_key_with_value(context):
    context.some_api = BasePage.find_value_on_xml(context.response_some_api, 'some_tag_key_xml')
    context.whatever_api = BasePage.find_value_on_xml(context.response_whatever, 'some_tag_key_xml')
    assert context.some_api == context.whatever_api
