from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import xml.etree.ElementTree as ET
import requests
import random
import string
import json
import pymysql
import datetime
import queue
import os
import time
import pdb

#----------------------------------------------------------------------------------------------------------------------#
#Import pdb allowed to use the debbuger module using the command line pdb.set_trace(), before the code that you want to#
#analise.                                                                                                              #
#   Example:                                                                                                           #
#           def method_x(args, value):                                                                                 #
#               pdb.set_trace()                                                                                        #
#               while True:                                                                                            #
#                    key = args.popitem(value)                                                                         #
#----------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------#
# BasePage is a common class where the developer can write the necessary methods in python and re-use on               #
# entire test, make sure the methods that you will write here are flexible, without constants or hardcode              #
# data.                                                                                                                #
# Verify method names are readable to facilitate future maintenance and make it easier for other                       #
# developers to use the method.                                                                                        #
#----------------------------------------------------------------------------------------------------------------------#

class BasePage(object):

    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url
        self.timeout = 20
        self.implicit_wait = 20

#----------------------------------------------------------------------------------------------------------------------#
#                     Methods that manipulate strings information as described                                         #
#----------------------------------------------------------------------------------------------------------------------#

####-------------------------------------------- Random Strings Methods --------------------------------------------####

    def generate_unique_id(chars_number):
        """Generate N chars random string with Lowercase and Uppercase."""
        unique_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(chars_number)])
        return unique_id

    def generate_unique_lowercase_id(chars_number):
        """Generate N chars random string with Lowercase."""
        unique_id = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(chars_number)])
        return unique_id

    def generate_unique_uppercase_id(chars_number):
        """Generate N chars random string with Uppercase."""
        unique_id = ''.join([random.choice(string.ascii_uppercase + string.digits) for n in range(chars_number)])
        return unique_id

    def generate_unique_email(username, id, domain_list):
         """Generate random email, combine generate_unique_id,  generate_unique_lowercase_id or generate_unique_uppercase_id
         and a list of domains."""
         email = username +'.'+ id + random.choice(domain_list)
         return email
####----------------------------------------- String Manipulation Methods ------------------------------------------####

    def split_string_between(value, a, b):
        """Find and validate before-part and return middle part."""
        pos_a = value.find(a)
        if pos_a == -1: return ""
        #Find and validate after part.
        pos_b = value.rfind(b)
        if pos_b == -1: return ""
        #Return middle part.
        adjusted_pos_a = pos_a + len(a)
        if adjusted_pos_a >= pos_b: return ""
        return value[adjusted_pos_a:pos_b]

    def split_string_before(value, a):
        """Find first part and return slice before it."""
        pos_a = value.find(a)
        if pos_a == -1: return ""
        return value[0:pos_a]

    def split_string_after(value, a):
        """Find and validate first part and returns chars after the found string."""
        pos_a = value.rfind(a)
        if pos_a == -1: return ""
        #Returns chars after the found string.
        adjusted_pos_a = pos_a + len(a)
        if adjusted_pos_a >= len(value): return ""
        return value[adjusted_pos_a:]


#----------------------------------------------------------------------------------------------------------------------#
#                     Methods that connect and manipulate datasource or database information                           #
#----------------------------------------------------------------------------------------------------------------------#

####-------------------------------------------- Database Methods --------------------------------------------------####

    def open_connection_with_database(host, port, username, password, database):
        try:
            db_con = pymysql.connect(host=host, port=port, user=username, passwd=password, db=database, cursorclass=pymysql.cursors.DictCursor, autocommit=True)
        except Exception:
            print("Error in MySQL connection with "+database+" database.")
        else:
            return db_con


    def open_connection_with_database2(host, port, username, password, database):
        try:
            db_con = pymysql.connect(host=host, port=port, user=username, passwd=password, db=database, cursorclass=pymysql.cursors.DictCursor)
        except Exception:
            print("Error in MySQL connection with "+database+" database.")
        else:
            return db_con.cursor(pymysql.cursors.SSCursor)

    def get_columns_from_dict(source, args_key):
        """Convert a dict of arguments into a string to columns separate by comma. Example: 'column_1, column_2, column_3'."""
        str_columns = ""
        data_args = source.get(args_key.replace(' ', '_'))
        if data_args is not None:
            for key, value in enumerate(data_args[0]):
                    str_columns += value + ', '
        else:
                message = "No matching results for parameter data = "+ args_key +" was found in DataPool."
                raise Exception(message)
        return str_columns[:-2]

    def execute_query(db_connection, sql_query):
        connection = db_connection
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        return result

    def execute_query_from_db(host, port, username, password, database, sql_query):
        connection = BasePage.open_connection_with_database(host, port, username, password, database)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        return result


    def select_all_from_table(db_connection, table):
        con = db_connection
        sql_query = "SELECT * FROM " + table
        con.execute(sql_query)
        return con.fetchall()

    def close_connection_database(db_connection):
        con = db_connection
        con.close()


#----------------------------------------------------------------------------------------------------------------------#
# DATAPOOL_READ is a method use to get a collection of information from a source archive Dictionaries, Hashmaps, and   #
# Hash Tables. This method need 3 arguments: the dict's name, the collection's name and the key that you searching for.#
#                                                                                                                      #
#   Example:                                  result = datapool_read(DATA_SOURCE, valid_data, 'key_1')                 #
#       DATA_SOURCE ={                        print("Results is: ", result)                                            #
# 	        "valid_data" :[{                                                                                           #
# 	                 "key_1" : "value1",                                                                               #
#      	             "key_2" : "value2"       output:  Results is: value1                                              #
#      	     }],                                                                                                       #
#           "invalid_data" :[{                                                                                         #
# 	                "key_1" : "value1",                                                                                #
#      	            "key_2" : "value2"                                                                                 #
#      	            }]                                                                                                 #
# }                                                                                                                    #                                                                          #
#----------------------------------------------------------------------------------------------------------------------#

    def datapool_read(source, data, key):
        """Get a list of arguments named as 'data' on the 'source' and search the 'key' on that list."""
        data_args = source.get(data.replace(' ', '_'))
        if data_args is not None:
            #Search the 'key' on that list
            if data_args[0].get(key)is not None:
                return data_args[0].get(key)
            else:
                message = "No matching results for parameter data = "+ data +" on the key = " + key +" was found in DataPool."
                raise Exception(message)
        else:
            message = "No matching results for parameter data = "+ data +" on the key = " + key +" was found in DataPool."
            raise Exception(message)

#----------------------------------------------------------------------------------------------------------------------#
# GET_PAYLOAD_FROM_DATAPOOL is a method use to load a data from a source archive. It's useful to get all information   #
# from a collection. For example, if you need to POST the same .json and the data don't need to be changed, the data   #
# source can emulate the .json.                                                                                        #
# This method need 2 arguments: the dict's name and the collection's name:                                             #
#   Example:                                                                                                           #
#       DATA_SOURCE ={                     payload = get_payload_from_datapool(DATA_SOURCE, 'valid_data')              #
# 	        "valid_data" :[{               print("Payload is: ", payload)                                              #
# 	                 "key_1" : "value1",                                                                               #
#      	             "key_2" : "value2"                                                                                #
#      	     }],                           output:  Payload is:   "valid_data" :[{                                     #
#           "invalid_data" :[{                                           "key_1" : "value1",                           #
# 	                "key_1" : "value1",                                  "key_2" : "value2"                            #
#      	            "key_2" : "value2"                                   }]                                            #
#      	            }]                                                                                                 #
# }                                                                                                                    #                                                                          #
#----------------------------------------------------------------------------------------------------------------------#

    def get_payload_from_datapool(source, data):
        """Get a list of arguments named as 'data' on the 'source'."""
        data_args = source.get(data.replace(' ', '_'))
        if data_args is not None:
            #Return the list if not Empty
            return data_args[0]
        else:
            message = "No matching results for parameter data = "+ data +" was found in DataPool."
            raise Exception(message)

    def get_data_from_dict(dict_args , key):
        """Get a dictionary of arguments named as 'dict_args', search the 'key' on that dict and return the value."""
        if dict_args  is not None:
            #Search the 'key' on that list
            if dict_args.get(key)is not None:
                return dict_args.get(key)
        else:
            message = "No matching results for parameter key = "+ key +" was found in Dictionary."
            raise Exception(message)

#----------------------------------------------------------------------------------------------------------------------#
#                                 Methods exclusive for UI testing tool                                                #
#----------------------------------------------------------------------------------------------------------------------#

    def element_exists(driver, timeout, type, element):
        """"Given a type(id, css, xpath, class name or name), timeout limit and the element, this method will search it
        on the screen and return a boolean (True/False)."""
        try:
            if type == 'id' or type == 'ID':
                WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, element)))
            elif type == 'css' or type == 'CSS':
                WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))
            elif type == 'xpath' or type == 'XPATH':
                WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, element)))
            elif type =='class_name' or type == 'CLASS_NAME':
                WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, element)))
            elif type == 'name' or type == 'NAME':
                WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.NAME, element)))
            else:
                 message = "No matching type "+ type +" to this method for searching element "+ element +"."
                 raise Exception(message)
        except EC.NoSuchElementException:
             return False
        return True


#----------------------------------------------------------------------------------------------------------------------#
#                     Methods manipulate XML files information and responses                                           #
#----------------------------------------------------------------------------------------------------------------------#

####----------------------------------------------- XML Methods ----------------------------------------------------####
#----------------------------------------------------------------------------------------------------------------------#
# READ_XML_FILE is a method use to load a generic .xml archive.                                                        #
# This method need 1 argument: the path of the .xml. It will return the generic.xml allowing to access namespaces      #
# and/or edit them if it's necessary.                                                                                  #
#   Example:                                                                                                           #
#        payload = read_xml_file(os.path.dirname(__file__) + '\\data_source\\generic.xml')                             #	                                                                                               #
#----------------------------------------------------------------------------------------------------------------------#

    def read_xml_file(xml_file):
        """Given a XML file, this method open it and return entire XML body."""
        xml = open(xml_file, 'r')
        body = xml.read()
        return body

#----------------------------------------------------------------------------------------------------------------------#
# GET_XML_ROOT is a method use to get the root from a .xml response tree.                                              #
# This method need 1 argument: the response .xml from an API. It will get the content of the response and return the   #
# root.                                                                                                                #
#   Example:                                                                                                           #
#        root_tree = get_xml_root(xml_response)                                                                        #	                                                                                               #
#----------------------------------------------------------------------------------------------------------------------#

    def verify_responses_status(response):
        if str(response) != '<Response [500]>':
            return True
        else:
            message = "The status is "+str(response)+". The system is disable, suspended or the request is badly formatted."
            print(response.content)
            raise Exception(message)

    def get_xml_root(response):
        """Given a XML File or XML response from an API, this method open it and return the root(iterable)."""
        response_content = response
        if type(response_content)!= bytes and type(response_content)!= str:
            response_content = response.content.decode("utf-8")
        #Transform the content into tree(iterable)
        response_tree = ET.ElementTree(ET.fromstring(response_content))
        response_root = response_tree.getroot()
        return response_root

    def find_value_on_xml(response, tag):
        """Given a XML response from API and specific tag name, this method search that tag name and return the value."""
        #Get the root from the XML File or XML response from an API
        response_root = BasePage.get_xml_root(response)
        #Search the element where the tag name is
        for element in response_root.iterfind('.//'+ tag):
            #Return the value
            return element.text

    def tag_exists_on_xml(response, tag):
        """Given a XML response from API and specific tag name, this method search if that tag name exists on the XML response and return a boolean."""
        #Get the root from the XML File or XML response from an API
        response_root = BasePage.get_xml_root(response)
        #Search the element where the tag name is
        for element in response_root.iterfind('.//'+ tag):
            return True
        return False

    def tag_list_exists_on_xml(response, tag_list):
        """Given a XML response from API and specific list of tags, this method verify if all tags exists in the response and return a boolean."""
        args = tag_list
        #Search the list of elements
        for args_key, args_value in args.items():
            item = BasePage.tag_exists_on_xml(response, args_value)
            #Validate if tag exists
            if item is True:
                pass
            else:
                return False
        return True

    def tag_list_is_on_xml(response, tag_list, namespace):
        """Given a XML response from API and specific list of tags, this method verify if all tags are in the response."""
        args = tag_list
        #Search the list of elements
        for key in args.items():
                item = BasePage.tag_exists_on_xml(response, key)
                #Validate the tag name when it is found
                if item is True:
                    #print("The tag <"+ key[1].replace(namespace, "")+"> on the tag list was in the XML response.")
                    pass
                else:
                    message = "The tag <"+ key.replace(namespace, "") +"> on the tag list wasn't in the XML response."
                    raise Exception(message)


    def verify_hit(response, tag_list):
        """Given a XML response from API and specific list of tags, this method verify if all tags are in the response."""
        args = tag_list
        #Search the list of elements
        for key in args.items():
            item = BasePage.tag_exists_on_xml(response, key)
            #Validate the value when it is found
            if item:
                return True
            else:
                return False

    def confirm_persistence_of_response_in_different_sources(source_a, source_b, args, namespace_a, namespace_b, source_name_a, source_name_b):
        """Given an XML File or XML response in different sources, this method search in the both sources the tag names
        and validate the values."""
        for key in args.items():
            #Get tag name from both arguments list
            #Search them in their respective XML File or XML response
            item_a = BasePage.find_value_on_xml(source_a, key[1])
            item_b = BasePage.find_value_on_xml(source_b, key[1])
            #Validate the value when it is found
            if item_a == item_b:
                #print("The values on the "+ key[1].replace(namespace_a, "") +" = "+ str(item_a) +" and "+ key[1].replace(namespace_b, "") + " = "+ str(item_b)+" match.")
                pass
            else:
                message = "The values on the "+source_name_a+" "+ key[1].replace(namespace_a, "") +" = "+ str(item_a) +" and "+source_name_b+" "+ key[1].replace(namespace_b, "") + " = "+ str(item_b)+" didn't match."
                raise Exception(message)


    def compare_values_from_two_xml(xml_a, xml_b, args_a, args_b, namespace_a, namespace_b):
        """Given two XML Files, this method search in the both files the tag name arguments and validate the values."""
        while True:#It simulate a DO/WHILE
            #Pop the first tag name from both arguments list
            key_a = args_a.popitem()
            key_b = args_b.popitem()
            #Search them in their respective XML File or XML response
            item_a = BasePage.find_value_on_xml(xml_a, key_a[1])
            item_b = BasePage.find_value_on_xml(xml_b, key_b[1])
            #Validate the value when it is found
            if item_a == item_b:
                #print("The values on the "+ key_a[1].replace(namespace_a, "") +" = "+ str(item_a) +" and "+ key_b[1].replace(namespace_b, "") + " = "+ str(item_b)+" match.")
                pass
            else:
                message = "The values on the "+ key_a[1].replace(namespace_a, "") +" = "+ str(item_a) +" and "+ key_b[1].replace(namespace_b, "") + " = "+ str(item_b)+" didn't match."
                raise Exception(message)
            count_args_a = len(args_a)
            count_args_b = len(args_b)
            #Stop the loop when one of the arguments list end
            if count_args_a <= 0 or count_args_b <= 0:
                break

    def list_all_paths_on_xml_starting_from_node(path_list, response_root, start_path,namespace, node_name):
        """Given a XML File or XML response from an API, it will list all path starting it from a specific node. It will
        return the entire path for example 'Body > Parent > Child1' if it start from Body the path will be 'Parent/Child1'"""
        #Start from the root of XML File or XML response from an API
        for element in response_root:
            element_name = ET.QName(element.tag)
            #Get the parent tag name without namespace
            parent = element_name.text.strip().lstrip(namespace)
            #Test if it is a parent or child and concatenate to the new path
            if not element.getchildren() and element.text:
                new_path = start_path + "/" + parent
            else:
                new_path = start_path + "/" + parent
                BasePage.list_all_paths_on_xml_starting_from_node(path_list, element, new_path, namespace, node_name)
            #Once the entire path is stored, manipulate the string to get the path that starts only from the desired node.
            path = BasePage.split_string_after(new_path, node_name)
            #Clean the Empty path
            if path != "":
                #Stored the path list
                path_list.append(path)
        return path_list

    def list_all_full_paths_on_xml(path_list, response_root, start_path, namespace):
        """Given a XML File or XML response from an API, it will list all full path from it'"""
        #Start from the root of XML File or XML response from an API
        for element in response_root:
            element_name = ET.QName(element.tag)
             #Get the parent tag name without namespace
            parent = element_name.text.strip().lstrip(namespace)
             #Test if it is a parent or child and concatenate to the new path
            if not element.getchildren() and element.text:
                new_path = start_path + "/" + parent
            else:
                new_path = start_path + "/" + parent
                BasePage.list_all_full_paths_on_xml(path_list, element, new_path, namespace)
            #Stored the path list
            path_list.append(new_path)
        return path_list

    def compare_pathlist_from_two_xml_responses(context, system_name_a, system_name_b, response_a, response_b, namespace_a, namespace_b, node_name_a, node_name_b):
        """Given two XML Files or two XML responses, this method search in the both responses or both files divergent
        paths starting from a specific node and validate it. If any divergent path is found an report of divergences will be provide."""
        #Get both root
        xml_root_a = BasePage.get_xml_root(response_a)
        xml_root_b = BasePage.get_xml_root(response_b)
        #Define the path lists and result lists before call the method
        list_a = []
        list_b = []
        result_a = []
        result_b = []
        #Get the path list
        path_list_a = BasePage.list_all_paths_on_xml_starting_from_node(list_a, xml_root_a,"",namespace_a, node_name_a)
        path_list_b = BasePage.list_all_paths_on_xml_starting_from_node(list_b, xml_root_b,"",namespace_b, node_name_b)
        print("\nResponse Count Path "+system_name_a+":",len(list(path_list_a)),"Response Count Path "+system_name_b+":",len(list(path_list_b)))
        #Get the intersection of both path lists, sort it alphabetically and count the result
        divergent_paths = sorted(set(path_list_a).symmetric_difference(set(path_list_b)))
        divergent_count = len(list(divergent_paths))
        #If any divergence is found the report will be shown
        if divergent_count == 0:
           pass
        else:
            print("Total Divergent Paths: ",divergent_count,"Divergent Paths List: ",*divergent_paths, sep="\n")
            for path_a in path_list_a:
                if path_a in path_list_b:
                    pass
                else:
                    result_a.append(path_a)
            count_result_a = len(list(result_a))
            for path_b in path_list_b:
                if path_b in path_list_a:
                    pass
                else:
                    result_b.append(path_b)
            count_result_b = len(list(result_b))
            print("\nTotal Divergent Paths "+system_name_a+":",count_result_a, system_name_a+":", *result_a, sep="\n")
            print("\nTotal Divergent Paths "+system_name_b+":",count_result_b, system_name_b+":", *result_b, sep="\n")
            message =  "End of Divergent Paths Report"
            raise Exception(message)


#----------------------------------------------------------------------------------------------------------------------#
#                     Methods manipulate JSON files information and responses                                          #
#----------------------------------------------------------------------------------------------------------------------#

####----------------------------------------------- JSON Methods ---------------------------------------------------####

    def key_exists(context, key):
        json_key = BasePage.find_key_on_json(context.json, key)
        if json_key == key:
            return True
        else:
            return False

    def value_is_correct(context, key, value):
        if value == 'null':
            value = None
        if BasePage.key_exists(context, key) is True:
            return True
        if context.value == value:
            return True
        else:
            return False

    def find_value_json(obj, key):
        if key in obj:
            return obj[key]
        if type(obj) is dict:
            for k, v in obj.items():
                if isinstance(v, dict):
                    return BasePage.find_value_json(v, key)
        elif type(obj) is list:
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

    def find_key_and_replace_value_json(obj, key, value):
        if key in obj:
            obj[key]=value
            return obj[key]
        if type(obj) is dict:
            for k, v in obj.items():
                if isinstance(v,dict):
                    item = BasePage.find_key_and_replace_value_json(v, key, value)
                    if item is not None:
                        return json.dumps(obj, indent=4, sort_keys=True)
        elif type(obj) is list:
            for k, v in enumerate(obj):
                item = BasePage.find_key_and_replace_value_json(v, key, value)
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
                        item = BasePage.find_key_and_replace_value_json(v, args_key, args_value)
                        if(item is not None)or(type(item) is str):
                           json.dumps(json_data, indent=4, sort_keys=True)
                        for v_key, v_value in v.items():
                            v1 = v[v_key]
                            if(type(v1) is dict)or(type(v1) is list):
                                BasePage.find_key_and_replace_value_json(v1, args_key, args_value)
        new_json = json.dumps(json_data, indent=4, sort_keys=True)
        return new_json


