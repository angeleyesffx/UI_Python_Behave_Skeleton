from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import random
import json
import queue
import os
import xml.etree.ElementTree as ET


class BasePage(object):
    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url
        self.timeout = 5
        self.implicit_wait = 5

    def get_payload_from_datapool(source, data):
        dtp = source.get(data.replace(' ', '_'))
        if dtp != None:
            return dtp[0]
        else:
            message = "Nenhum resultado correspondente para os parametros data = "+ data +" foi encontrado no DataPool."
            raise Exception(message)

    def datapool_read(source, data, key):
        dtp = source.get(data.replace(' ', '_'))
        if dtp != None:
            if dtp[0].get(key)!= None:
                return dtp[0].get(key)
            else:
                message = "Nenhum resultado correspondente para os parametros data = "+ data +", key = " + key +" foi encontrado no DataPool."
                raise Exception(message)
        else:
            message = "Nenhum resultado correspondente para os parametros data = "+ data +", key = " + key +" foi encontrado no DataPool."
            raise Exception(message)

    def key_exists(context, key):
        json_key = BasePage.find_key_on_json(context.json, key)
        if json_key == key:
            return True
        else:
            return False

    def value_isCorrect(context, key, value):
        if value == 'null':
            value = None
        if BasePage.key_exists(context, key) == True:
            return True
        if context.value == value:
            return True
        else:
            return False

    def read_xml_file(xml_file):
        xml = open(xml_file, 'r')
        body = xml.read()
        return body

    def find_value_on_xml(response, key):
        responseXml = (response.content).decode("utf-8")
        response_tree = ET.fromstring(responseXml)
        for element in response_tree.iter():
            #print(element.tag) #---------> use to see the tree tags on the XML and use one of the results as key
            if element.tag == key:
                return element.text

    def find_value_json(obj, key):
        if key in obj:
            return obj[key]
        if(type(obj)== dict):
            for k, v in obj.items():
                if isinstance(v, dict):
                    return BasePage.find_value_json(v, key)
        elif(type(obj)== list):
            for k, v in enumerate(obj):
                return BasePage.find_value_json(v, key)

    def find_key_on_json(obj, key):
        if key in obj:
            return key
        for k, v in obj.items():
            if isinstance(v, dict):
                item = BasePage.find_key_on_json(v, key)
                if item is not None:
                    return item

    def find_key_and_replace_valeu_json(obj, key, value):
        if key in obj:
            obj[key]=value
            return obj[key]
        if(type(obj)== dict):
            for k, v in obj.items():
                if isinstance(v,dict):
                    item =  BasePage.find_key_and_replace_valeu_json(v, key, value)
                    if item is not None:
                        return json.dumps(obj, indent=4, sort_keys=True)
        elif(type(obj)== list):
            for k, v in enumerate(obj):
                item = BasePage.find_key_and_replace_valeu_json(v, key, value)
                if item is not None:
                   return json.dumps(obj, indent=4, sort_keys=True)


    def edit_json(json_file_path, args):
        json_file = json_file_path
        with open(json_file, 'r') as file:
            json_data = json.load(file)
            for args_key, args_value in args.items():
                for key, value in json_data.items():
                    v = json_data[key]
                    if(type(v) is dict)or(type(v) is list):
                        item = BasePage.find_key_and_replace_valeu_json(v, args_key, args_value)
                        if(item is not None)or(type(item) is str):
                           new_json = json.dumps(json_data, indent=4, sort_keys=True)
                        for v_key, v_value in v.items():
                            v1 = v[v_key]
                            if(type(v1) is dict)or(type(v1) is list):
                                new_json = BasePage.find_key_and_replace_valeu_json(v1, args_key, args_value)
        new_json = json.dumps(json_data, indent=4, sort_keys=True)
        return new_json





# JSON preparation if more info stored in the config file
# def load_json(json_file):
#     return json_data
#
#
# def load_file(filename):
#     with open(filename, 'r') as f:
#         data = f.read()
#     return data
#
# before all used when bigger project and data is read from JSON file
# def before_all(context):
#     context.env_file = "./myfile.json"
#     context.env = load_json(context.env_file)
#     if "location" in context.env.keys():
#         context.location = context.env["location"]["url"]
#         a = context.location
#         print(a)

# before all scenario allows me to use always fresh browser without cache. Every time a new browser object is created

