import json
from jsondiff import diff
from behave import *
#from features.steps.data_source.some_datasource import DATA_REQUEST
from features.steps.data_source.other_datasource import new_information
from features.pages.basepage import BasePage
from requests.auth import HTTPBasicAuth
import os
import requests
import xml.etree.ElementTree as ET

@given(u'I get the endpoint from TokenAPI')
def get_token_endpoint(context):
    context.endpoint_token_api = "{0}{1}".format(context.base_url, "/authentication")
    return context.endpoint_token_api


@given(u'I get the endpoint from HomeAPI')
@when(u'I get the endpoint from HomeAPI')
def get_home_endpoint(context):
    context.endpoint_home_api = "{0}{1}".format(context.base_url, "/home")
    return context.endpoint_home_api


@when(u'the request sends POST to the TokenAPI')
def send_post_tokenAPI_request(context):
    url = context.endpoint_token_api
    headers = {
        'x-os': 'android',
        'Content-Type': 'application/json',
    }
    payload = '{ "user": "angeleyes@mail.com", "password": "test@1234$" }'
    context.response = requests.post(url, data=payload, headers=headers)
    context.data = context.response.json()
    return context.data

@when(u'the request sends GET to the HomeAPI')
def send_get_home_request(context):
    url = context.endpoint_home_api
    token = BasePage.find_value_json(context.data, "token")
    headers = {
        'x-token': f"{{{token}}}",
        'x-token-type': 'jwt',
        'x-os': 'android',
        'x-poc-id': '0000100002',
    }
    payload = '{ "user": "angeleyes@mail.com", "password": "test@1234$" }'
    context.response = requests.get(url, data=payload, headers=headers)
    context.page = context.response.json()
    return context.page


@then(u'I should see the response')
def send_post_tokenAPI_request(context):
    # Opening JSON file
    f = open('features/pages/api_example.json')
    # returns JSON object as
    # a dictionary
    datasource_json = json.load(f)
    # Iterating through the
    print(diff(context.page, datasource_json))
    print(diff( datasource_json,context.page))
    if test == 1:
     pass
    else:
      print(context.res)

