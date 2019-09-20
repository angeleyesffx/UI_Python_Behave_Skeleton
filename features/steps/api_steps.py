from behave import *
from features.steps.data_source.some_datasource import DATA_REQUEST
from features.steps.data_source.other_datasource import new_information
from features.pages.base_page import BasePage
from requests.auth import HTTPBasicAuth
import os
import requests
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

@when(u'the request sends POST to the Other API')
def send_post_other_request(context):
    context.endpoint = get_other_endpoint(context)
    json_path = os.path.dirname(__file__) + '\\data_source\\other_payloads.json'
    new_information.update({'other_id': context.other_id, 'another_id': context.another_id})
    json_file = BasePage.edit_json(json_path, new_information)
    payload = json.loads(json_file)
    context.response = requests.post(context.endpoint, json=payload)
    context.json = context.response.json()

@then(u'the response form Some API should be equal on API Whatever')
def response_content_key_with_value(context):
    context.some_api = BasePage.find_value_on_xml(context.response_some_api, 'some_tag_key_xml')
    context.whatever_api = BasePage.find_value_on_xml(context.response_whatever, 'some_tag_key_xml')
    assert context.some_api == context.whatever_api
    
    
@then(u'the wrong password message should be received')
def wrong_password_auth_message(context):
    assert context.json['status']['message'].rsplit(' ', 1)[0] == str('Wrong Password for Login ID:')


@then(u'the wrong user message should be received')
def wrong_user_auth_message(context):
    start = context.json['status']['message'].startswith('Login ')
    end = context.json['status']['message'].endswith(' not in system')
    assert start == end == True    
