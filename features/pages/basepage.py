import json
import random
import string
import time
import xml.dom.minidom as DOM
import xml.etree.ElementTree as ET
import pymysql
import os
import sys
import yaml
import datetime
import argparse
import requests
import json
import csv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# ----------------------------------------------------------------------------------------------------------------------#
# BasePage is a common class where the developer can write the necessary functions in python and re-use on              #
# entire test, make sure the functions which you will write here are flexible, without constants or hardcode            #
# data.                                                                                                                 #
# Verify function names are readable to facilitate future maintenance and make it easier for other                      #
# developers to use the function.                                                                                       #
# ----------------------------------------------------------------------------------------------------------------------#

# ----------------------------------------------------------------------------------------------------------------------#
# Import pdb allowed to use the debbuger module using the command line pdb.set_trace(), before the code that you want to#
# analise.                                                                                                              #
#   Example:                                                                                                            #
#           def function_x(args, value):                                                                                #
#               pdb.set_trace()                                                                                         #
#               while True:                                                                                             #
#                    key = args.popitem(value)                                                                          #
# ----------------------------------------------------------------------------------------------------------------------#


class Actions(ActionChains):
    def wait(self, time_s: float):
        self._actions.append(lambda: time.sleep(time_s))
        return self


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.base_url = base_url
        self.timeout = 20
        self.implicit_wait = 20

    # -----------------------------------------------------------------------------------------------------------------#
    #                     Functions to manipulate strings information as described                                     #
    # -----------------------------------------------------------------------------------------------------------------#

    ####---------------------------------------- Random String Functions -------------------------------------------####

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
        """Generate random email, combine generate_unique_id,  generate_unique_lowercase_id or
        generate_unique_uppercase_id and a list of domains. """
        email = username + '.' + id + random.choice(domain_list)
        return email

    ####--------------------------------------- String Manipulation Functions --------------------------------------####

    def split_string_between(string_value, slice_a, slice_b):
        """Find and validate before-part and return middle part."""
        pos_a = string_value.find(slice_a)
        if pos_a == -1: return ""
        # Find and validate after part.
        pos_b = string_value.rfind(slice_b)
        if pos_b == -1: return ""
        # Return middle part.
        adjusted_pos_a = pos_a + len(slice_a)
        if adjusted_pos_a >= pos_b: return ""
        return string_value[adjusted_pos_a:pos_b]

    def split_string_before(string_value, slice_a):
        """Find first part and return slice before it."""
        pos_a = string_value.find(slice_a)
        if pos_a == -1: return ""
        return string_value[0:pos_a]

    def split_string_after(string_value, slice_a):
        """Find and validate first part and returns chars after the found string."""
        pos_a = string_value.rfind(slice_a)
        if pos_a == -1: return ""
        # Returns chars after the found string.
        adjusted_pos_a = pos_a + len(slice_a)
        if adjusted_pos_a >= len(string_value): return ""
        return string_value[adjusted_pos_a:]

    def remove_chars_from_string(string_value, char_list):
        """Remove all characters in list from string."""
        new_string = string_value
        for char in char_list:
            # Remove the char in list from the string value.
            new_string = new_string.replace(char, "")
        return new_string

    def replace_string_with(string_value, old_string, new_string):
        # Replace the string for another value.
        result_string = string_value.replace(old_string, new_string)
        return result_string

    def empty_string_to_none_string(string_value):
        # Replace the string "" or '' for None.
        if string_value == '' or "":
            return None
        else:
            return string_value

    # -----------------------------------------------------------------------------------------------------------------#
    #                     Functions to connect and manipulate datasource or database information                       #
    # -----------------------------------------------------------------------------------------------------------------#

    ####---------------------------------------- Database Functions ------------------------------------------------####

    def open_connection_with_database(host, port, username, password, database):
        try:
            db_con = pymysql.connect(host=host, port=port, user=username, passwd=password, db=database,
                                     cursorclass=pymysql.cursors.DictCursor, autocommit=True)
        except Exception:
            print("Error in MySQL connection with " + database + " database.")
        else:
            return db_con

    def get_columns_from_dict(source, args_key):
        """Convert a dict of arguments into a string to columns separate by comma. Example: 'column_1, column_2,
        column_3'. """
        str_columns = ""
        data_args = source.get(args_key.replace(' ', '_'))
        if data_args is not None:
            for key, value in enumerate(data_args[0]):
                str_columns += value + ', '
        else:
            message = "No matching results for parameter data = " + args_key + " was found in DataPool."
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

    def get_entire_result_from_executed_query(host, port, username, password, database, sql_query):
        connection = BasePage.open_connection_with_database(host, port, username, password, database)
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

    # -----------------------------------------------------------------------------------------------------------------#
    # DATAPOOL_READ is a function use to get a collection of information from a source archive Dictionaries, Hashmaps, #
    # and Hash Tables.                                                                                                 #
    # This function needs 3 arguments: the dict's name, the collection's name and the key that you searching for.      #
    #                                                                                                                  #
    #   Example:                                  result = datapool_read(DATA_SOURCE, valid_data, 'key_1')             #
    #       DATA_SOURCE ={                        print("Results is: ", result)                                        #
    # 	        "valid_data" :[{                                                                                       #
    # 	                 "key_1" : "value1",                                                                           #
    #      	             "key_2" : "value2"       output:  Results is: value1                                          #
    #      	     }],                                                                                                   #
    #           "invalid_data" :[{                                                                                     #
    # 	                "key_1" : "value1",                                                                            #
    #      	            "key_2" : "value2"                                                                             #
    #      	            }]                                                                                             #
    # }                                                                                                                #                                                                          #
    # -----------------------------------------------------------------------------------------------------------------#

    def datapool_read(source, data, key):
        """Get a list of arguments named as 'data' on the 'source' and search the 'key' on that list."""
        data_args = source.get(data.replace(' ', '_'))
        dt_key = key.replace(' ', '_')
        if data_args is not None:
            # Search the 'key' on that list ------> for "python data_args[0].get(dt_key)"
            if data_args.get(dt_key) is not None:
                return data_args.get(dt_key)
            else:
                message = "No matching results for parameter data = " + data + " on the key = " + key + "was found in " \
                                                                                                        "DataPool. "
                raise Exception(message)
        else:
            message = "No matching results for parameter data = " + data + " on the key = " + key + "was found in " \
                                                                                                    "DataPool. "
            raise Exception(message)

    def read_yml_file(yml_path):
        with open(yml_path) as file:
            data = yaml.full_load(file)
            return data

    def select_the_keys_from_yml(yml_path, parent_reference):
        environments = read_yml_file(yml_path)
        params = set()
        if parent_reference == "environment":
            for key in environments.keys():
                params.update(environments)
                return sorted(params)
        else:
            for key in environments.keys():
                params.update(environments[key])
                return sorted(params)

    # -----------------------------------------------------------------------------------------------------------------#
    # GET_LIST_FROM_SOURCE is a function use to load a data from a source archive. It's useful to get all information  #
    # from a collection. For example, if you need to POST the same .json and the data don't need to be changed, the    #
    # data source can emulate the .json.                                                                               #
    # This function needs 2 arguments: the dict's name and the collection's name:                                      #
    #   Example:                                                                                                       #
    #       DATA_SOURCE ={                     payload = get_list_from_source(DATA_SOURCE, 'valid_data')               #
    # 	        "valid_data" :[{               print("Payload is: ", payload)                                          #
    # 	                 "key_1" : "value1",                                                                           #
    #      	             "key_2" : "value2"                                                                            #
    #      	     }],                           output:  Payload is:   "valid_data" :[{                                 #
    #           "invalid_data" :[{                                           "key_1" : "value1",                       #
    # 	                "key_1" : "value1",                                  "key_2" : "value2"                        #
    #      	            "key_2" : "value2"                                   }]                                        #
    #      	            }]                                                                                             #
    # }                                                                                                                #                                                                          #
    # -----------------------------------------------------------------------------------------------------------------#

    # -----------------------------------------------------------------------------------------------------------------#
    #                                            Functions to manipulate lists                                         #
    # -----------------------------------------------------------------------------------------------------------------#

    ####-------------------------------------------- List Functions ------------------------------------------------####

    def union_list_without_duplicate_item(list_a, list_b):
        result_list = list(list_a)
        result_list.extend(x for x in list_b if x not in result_list)

    def intersection_list(list_a, list_b):
        result_list = [list(filter(lambda x: x in list_a, sublist)) for sublist in list_b]
        return result_list

    def remove_item_from_list(list, item):
        result_list = list.remove(item)
        return result_list

    def get_random_item_from_list(list, item):
        selected_item = random.choice(list)
        return selected_item

    def get_different_random_item_from_list(list, item):
        result_list = list.remove(item)
        selected_item = random.choice(result_list)
        return selected_item

    def get_list_from_source(source, data):
        """Get a list of arguments named as 'data' on the 'source'."""
        data_args = source.get(data.replace(' ', '_'))
        if data_args is not None:
            # Return the list if not Empty
            return data_args[0]
        else:
            message = "No matching results for parameter data = " + data + " was found in DataPool."
            raise Exception(message)

    def get_data_from_dict(dict_args, key):
        """Get a dictionary of arguments named as 'dict_args', search the 'key' on that dict and return the value."""
        data_args = dict_args
        if data_args is not None:
            # Search the 'key' on that list
            if data_args.get(key) is not None:
                return data_args.get(key)
        else:
            message = "No matching results for parameter key = " + key + " was found in Dictionary."
            raise Exception(message)

    # -----------------------------------------------------------------------------------------------------------------#
    #                                 Functions exclusive for UI testing tool                                          #
    # -----------------------------------------------------------------------------------------------------------------#

    # -----------------------------------------------------------------------------------------------------------------#
    # Function that use "selector_type" as (str)argument is implementing selenium.webdriver.common.by                  #
    #                                                                                                                  #
    # class selenium.webdriver.common.by.By[source]                                                                    #
    # Set of supported locator strategies.                                                                             #
    #    CLASS_NAME = 'class name'                                                                                     #
    #    CSS_SELECTOR = 'css selector'                                                                                 #
    #    ID = 'id'                                                                                                     #
    #    LINK_TEXT = 'link text'                                                                                       #
    #    NAME = 'name'                                                                                                 #
    #    PARTIAL_LINK_TEXT = 'partial link text'                                                                       #
    #    TAG_NAME = 'tag name'                                                                                         #
    #    XPATH = 'xpath'                                                                                               #
    # -----------------------------------------------------------------------------------------------------------------#
    def page_has_loaded(driver):
        page_state = driver.execute_script('return document.readyState;')
        if page_state == 'complete':
            pass
        else:
            message = "The page isn't load, or take to long to load!"
            raise Exception(message)

    def element_exists(driver, timeout, selector_type, element):
        """Given a selector type(id, css selector, xpath, class name, tag name or name), timeout limit and the
        element, this function will search it on the screen and return a boolean (True/False). """
        try:
            # wait for the element to appear
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((selector_type, element)))
        except TimeoutException or EC.NoSuchElementException:
            # if the element appear return True, else return False
            return False
        return True

    def fast_element_exists(driver, selector_type, element):
        """Given a selector type(id, css selector, xpath, class name, tag name or name), timeout limit and the
        element, this function will search it on the screen and return a boolean (True/False). """
        try:
            # wait for the element to appear
            driver.find_element(selector_type, element)
        except EC.NoSuchElementException:
            # if the element appear return True, else return False
            return False
        return True

    def locate_element(driver, timeout, selector_type, element):
        """Given a selector type(id, css selector, xpath, class name, tag name or name), timeout limit and the
        element, this function will search it on the screen and return it. """
        try:
            # wait for the element to appear, if so return it
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((selector_type, element)))
        except TimeoutException:
            message = "The element " + element + " or the type " + selector_type + "can't be found or it doesn't " \
                                                                                   "exist in the screen. "
            raise Exception(message)

    def get_the_ancestor_element(element, parent_xpath):
        try:
            # return the ancestor element from the child element
            return element.find_element(By.XPATH, "ancestor::" + str(parent_xpath))
        except TimeoutException:
            message = "The element xpath can't be found or it doesn't exist in the screen."
            raise Exception(message)

    def wait_until_disappears(driver, timeout_to_be_visible, timeout_to_be_invisible, selector_type, element):
        """Given a selector type(id, css selector, xpath, class name, tag name or name), the timeout limit to the
        element to be visible and the timeout limit to the element to be disappear, this function will wait until the
        element isn't displayed on screen. """
        try:
            # wait for loading element to appear
            # -required to prevent prematurely checking if element has disappeared, before it has had a chance to appear
            if BasePage.element_exists(driver, timeout_to_be_visible, selector_type, element):
                # then wait for the element to disappear
                WebDriverWait(driver, timeout_to_be_invisible).until_not(
                    EC.presence_of_element_located((selector_type, element)))
            else:
                message = "The element " + element + " or the type " + selector_type + "can't be found or it doesn't " \
                                                                                       "exist in the screen. "
                raise Exception(message)
        except TimeoutException:
            # if the element disappear return True, else return False
            return False
        return True
    
    def wait_for_element (driver, timeout_to_be_visible, selector_type, element):
        """Given a selector type(id, css selector, xpath, class name, tag name or name), the timeout limit to the
        element to be visible, this function will wait until the
        element isn't displayed on screen. """
        try:
            WebDriverWait(driver, timeout_to_be_visible).until(EC.visibility_of_element_located((selector_type, element)))
        except TimeoutException:
            return False
        return True

    def wait_for_element (driver, timeout_to_be_visible, selector_type, element):
        """Given a selector type(id, css selector, xpath, class name, tag name or name), the timeout limit to the
        element to be visible, this function will wait until the
        element isn't displayed on screen. """
        try:
            WebDriverWait(driver, timeout_to_be_visible).until(EC.visibility_of_element_located((selector_type, element)))
        except TimeoutException:
            return False
        return True

    def verify_element_list(driver, timeout, element_list):
        """Given list of element like: LAYOUT_LIST = [{element, selector_type, text_expected}, {element,
        selector_type, text_expected}], this function will verify if the elements on the list is on the screen or if
        the expected data text is on the screen. If it fails a report is return. """
        fail_results = []
        for key in element_list:
            element = BasePage.get_data_from_dict(key, "element")
            selector_type = BasePage.get_data_from_dict(key, "type")
            text_expected = BasePage.get_data_from_dict(key, "text_expected")
            if text_expected == "":
                if BasePage.element_exists(driver, timeout, selector_type, element) is False:
                    message = "The element " + element + " can't be found or it doesn't exist in the screen."
                    fail_results.append(message)
                else:
                    pass
            else:
                if BasePage.element_exists(driver, timeout, selector_type, element) is False:
                    message = "The element " + element + " can't be found or it doesn't exist in the screen."
                    fail_results.append(message)
                else:
                    text_obtained = BasePage.locate_element(driver, timeout, selector_type, element).text
                    if text_obtained == text_expected:
                        pass
                    else:
                        message = "The text shown by the " + str(
                            element) + " on the screen is different that was expected. It was expected: '" + str(
                            text_expected) + "' and was obtained: '" + str(text_obtained) + "'."
                        fail_results.append(message)
        if fail_results is not None:
            raise Exception(fail_results)

    def get_element_from_list(driver, selector_type, element_list, attribute, expected_attribute_content):
        element_list = driver.find_elements(selector_type, element_list)
        for element in element_list:
            if element.get_attribute(attribute) == expected_attribute_content:
                return element

    def get_list_without_an_element(driver, selector_type, element_list, attribute, expected_attribute_content):
        result_list = []
        element_list = driver.find_elements(selector_type, element_list)
        for element in element_list:
            if element.get_attribute(attribute) != expected_attribute_content:
                result_list.append(element)
        if result_list is None:
            message = "The provied list is empty or the function can't find any results."
            raise Exception(message)
        else:
            return result_list

    def select_option_from_dropdown_list(driver, selector_type, dropdown_element, attribute,
                                         expected_attribute_content):
        element_found = BasePage.locate_element(driver, 10, selector_type, dropdown_element)
        options_list = element_found.find_elements_by_tag_name('option')
        for option in options_list:
            attribute_content = option.get_attribute(attribute)
            if attribute_content == expected_attribute_content:
                option.click()

    # -----------------------------------------------------------------------------------------------------------------#
    #                 Functions to manipulate XML files information and responses                                      #
    # -----------------------------------------------------------------------------------------------------------------#

    ####----------------------------------------------- XML Functions ----------------------------------------------####
    # -----------------------------------------------------------------------------------------------------------------#
    # READ_XML_FILE is a function use to load a generic .xml archive.                                                  #
    # This function need 1 argument: the path of the .xml. It will return the generic.xml allowing to access namespaces#
    # and/or edit them if it's necessary.                                                                              #
    #   Example:                                                                                                       #
    #        payload = read_xml_file(os.path.dirname(__file__) + '\\data_source\\generic.xml')                         #	                                                                                               #
    # -----------------------------------------------------------------------------------------------------------------#

    def read_xml_file(xml_file):
        """Given a XML file, this function open it and return entire XML body."""
        xml = open(xml_file, 'r', encoding='utf8')
        body = xml.read()
        return body

    # ----------------------------------------------------------------------------------------------------------------------#
    # GET_XML_ROOT is a function use to get the root from a .xml response tree.                                             #
    # This function need 1 argument: the response .xml from an API. It will get the content of the response and return the  #
    # root.                                                                                                                #
    #   Example:                                                                                                           #
    #        root_tree = get_xml_root(xml_response)                                                                        #	                                                                                               #
    # ----------------------------------------------------------------------------------------------------------------------#

    def beautify_xml(element):
        """Return a pretty-printed XML string for the Element."""
        element_content = element
        if type(element_content) != bytes and type(element_content) != str:
            element_content = element.content.decode("utf-8")
        reparsed = DOM.parseString(element_content)
        return '\n'.join([line for line in reparsed.toprettyxml(indent=' ' * 2).split('\n') if line.strip()])

    def verify_responses_status(response, request):
        if str(response) != '<Response [500]>':
            return True
        else:
            message = "The status is " + str(
                response) + ". The system is disable, suspended or the request is badly formatted."
            print("Resquest used: \n", request)
            print("Obtained Response: \n", BasePage.beautify_xml(response.content))
            raise Exception(message)

    def get_xml_root(response, endpoint):
        """Given a XML File or XML response from an API, this function open it and return the root(iterable)."""
        response_content = response
        if type(response_content) != bytes and type(response_content) != str:
            response_content = response.content.decode("utf-8")
        # Transform the content into tree(iterable)
        try:
            tree = ET.fromstring(response_content)
        except ET.ParseError as err:
            error = BasePage.split_string_before(err.msg, ": line ")
            if error == 'not well-formed (invalid token)':
                message = "Also check the endpoint: " + endpoint
            raise Exception(message)
        response_tree = ET.ElementTree(tree)
        response_root = response_tree.getroot()
        return response_root

    def count_blocks_by_id_tag_on_xml(response, tag, endpoint):
        """Given a XML response from API and specific unique id tag, this function count the number of blocks in the
        XML response. """
        # Get the root from the XML File or XML response from an API
        count_blocks = 0
        response_root = BasePage.get_xml_root(response, endpoint)
        # Search the element where the tag name is
        for data_block in response_root.findall('.//' + tag):
            count_blocks = count_blocks + 1
        return count_blocks

    def find_value_on_xml(response, tag, endpoint):
        """Given a XML response from API and specific tag name, this function search that tag name and return the
        value. """
        # Get the root from the XML File or XML response from an API
        response_root = BasePage.get_xml_root(response, endpoint)
        # for element in response_root.iter():
        # print(element.getchildren())
        # print(element.tag)
        # Search the element where the tag name is
        for element in response_root.iterfind('.//' + tag):
            # Return the value
            return element.text

    def find_values_inside_blocks_on_xml(response, tag, endpoint):
        """Given a XML response from API and specific block and tag name, this function search that tag name and return
        the value. """
        # Get the root from the XML File or XML response from an API
        values_list = []
        position = 1
        response_root = BasePage.get_xml_root(response, endpoint)
        for data_block in response_root.findall('.//' + tag):
            for element in data_block.iter():
                # Return the list of values in blocks
                values_list.append([position, element.tag, element.text])
            position = position + 1
        # print(*values_list, sep="\n")
        return values_list

    def get_data_from_tag_parent_list(tag_parent_list, tag_name, tag_value):
        """This function search the specific tag name and tag value inside the return of the function
        find_values_inside_blocks_on_xml, then return the specific data block. """
        index = 1
        values_list = []
        for elem in tag_parent_list:
            if tag_name == elem[1] and tag_value == elem[2]:
                index = elem[0]
                for elem1 in tag_parent_list:
                    if elem1[0] == index:
                        values_list.append([elem1[1], elem1[2]])
        # print(values_list)
        return values_list

    def remove_tag_from_xml_response(response, parent_tag, child_tag, endpoint):
        response_root = BasePage.get_xml_root(response, endpoint)
        for child in response_root.findall(parent_tag):
            for element in child.findall(child_tag):
                child.remove(element)
        new_response = response_root
        return new_response

    def remove_closed_tag_from_xml_response(response, closed_tag, closed_child_tag, parent_tag, endpoint):
        response_root = BasePage.get_xml_root(response, endpoint)
        for child in response_root.findall(closed_tag):
            for element in child.findall(closed_child_tag):
                return response_root
        new_response = BasePage.remove_tag_from_xml_response(response, parent_tag, closed_tag, endpoint)
        return new_response

    def tag_exists_on_xml(response, tag, endpoint):
        """Given a XML response from API and specific tag name, this function search if that tag name exists on the XML
        response and return a boolean. """
        # Get the root from the XML File or XML response from an API
        response_root = BasePage.get_xml_root(response, endpoint)
        # Search the element where the tag name is
        for element in response_root.iterfind('.//' + tag):
            return True
        return False

    def tag_list_exists_on_xml(response, tag_list, endpoint):
        """Given a XML response from API and specific list of tags, this function verify if all tags exists in the
        response and return a boolean. """
        args = tag_list
        # Search the list of elements
        for args_key, args_value in args.items():
            item = BasePage.tag_exists_on_xml(response, args_value, endpoint)
            # Validate if tag exists
            if item is True:
                pass
            else:
                return False
        return True

    def tag_list_is_on_xml(response, tag_list, namespace, endpoint):
        """Given a XML response from API and specific list of tags, this function verify if all tags are in the
        response. """
        args = tag_list
        # Search the list of elements
        for key in args.items():
            item = BasePage.tag_exists_on_xml(response, key, endpoint)
            # Validate the tag name when it is found
            if item is True:
                # print("The tag <"+ key[1].replace(namespace, "")+"> on the tag list was in the XML response.")
                pass
            else:
                message = "The tag <" + key.replace(namespace, "") + "> on the tag list wasn't in the XML response."
                raise Exception(message)

    def verify_hit(response, tag_list, endpoint):
        """Given a XML response from API and specific list of tags, this function verify if all tags are in the
        response. """
        args = tag_list
        # Search the list of elements
        for key in args.items():
            item = BasePage.tag_exists_on_xml(response, key, endpoint)
            # Validate the value when it is found
            if item:
                return True
            else:
                return False

    def confirm_persistence_of_response_in_different_sources(source_a, source_b, args, namespace_a, namespace_b,
                                                             source_name_a, source_name_b, endpoint_a, endpoint_b):
        """Given an XML File or XML response in different sources, this function search in the both sources the tag names
        and validate the values."""
        fail_list = []
        for key in args.items():
            # Get tag name from both arguments list
            # Search them in their respective XML File or XML response
            item_a = BasePage.find_value_on_xml(source_a, key[1], endpoint_a)
            item_b = BasePage.find_value_on_xml(source_b, key[1], endpoint_b)
            # Validate the value when it is found
            if item_a == item_b:
                # print("The values on the "+ key[1] +" = "+ str(item_a) +" and "+ key[1] + " = "+ str(item_b)+" match.")
                pass
            else:
                message = "The values on the " + source_name_a + " " + key[1].replace(namespace_a, "") + " = " + str(
                    item_a) + " and " + source_name_b + " " + key[1].replace(namespace_b, "") + " = " + str(
                    item_b) + " didn't match."
                fail_list.append(message)
        if not fail_list:
            pass
        else:
            message = "End of Fail List"
            print(*fail_list, sep="\n")
            raise Exception(message)

    def compare_values_from_two_xml(xml_a, xml_b, args_a, args_b, namespace_a, namespace_b, source_name_a,
                                    source_name_b, endpoint_a, endpoint_b):
        """Given two XML Files, this function search in the both files the tag name arguments and validate the values."""
        fail_list = []
        while True:  # It simulate a DO/WHILE
            # Pop the first tag name from both arguments list
            key_a = args_a.popitem()
            key_b = args_b.popitem()
            # Search them in their respective XML File or XML response
            item_a = BasePage.find_value_on_xml(xml_a, key_a[1], endpoint_a)
            item_b = BasePage.find_value_on_xml(xml_b, key_b[1], endpoint_b)
            # Validate the value when it is found
            if item_a == item_b:
                # print("Match on the "+ key_a[1].replace(namespace_a, "") +" = "+ str(item_a) +" and "+ key_b[1].replace(namespace_b, "") + " = "+ str(item_b)+" match.")
                pass
            else:
                message = "The values on the " + source_name_a + " " + key_a[1].replace(namespace_a, "") + " = " + str(
                    item_a) + " and " + source_name_b + " " + key_b[1].replace(namespace_b, "") + " = " + str(
                    item_b) + " didn't match."
                # Stored the path list
                fail_list.append(message)
            count_args_a = len(args_a)
            count_args_b = len(args_b)
            # Stop the loop when one of the arguments list end
            if count_args_a <= 0 or count_args_b <= 0:
                break
        if not fail_list:
            pass
        else:
            message = "End of Fail List"
            print(*fail_list, sep="\n")
            raise Exception(message)

    def list_all_paths_on_xml_starting_from_node(path_list, response_root, start_path, namespace, node_name):
        """Given a XML File or XML response from an API, it will list all path starting it from a specific node. It
        will return the entire path for example 'Body > Parent > Child1' if it start from Body the path will be
        'Parent/Child1' """
        # Start from the root of XML File or XML response from an API
        for element in response_root:
            element_name = ET.QName(element.tag)
            # Get the parent tag name without namespace
            parent = element_name.text.strip().lstrip(namespace)
            # Test if it is a parent or child and concatenate to the new path
            if not element.getchildren() and element.text:
                new_path = start_path + "/" + parent
            else:
                new_path = start_path + "/" + parent
                BasePage.list_all_paths_on_xml_starting_from_node(path_list, element, new_path, namespace, node_name)
            # Once the entire path is stored, manipulate the string to get the path that starts only from the desired node.
            path = BasePage.split_string_after(new_path, node_name)
            # Clean the Empty path
            if path != "":
                # Stored the path list
                path_list.append(path)
        return path_list

    def list_all_full_paths_on_xml(path_list, response_root, start_path, namespace):
        """Given a XML File or XML response from an API, it will list all full path from it'"""
        # Start from the root of XML File or XML response from an API
        for element in response_root:
            element_name = ET.QName(element.tag)
            # Get the parent tag name without namespace
            parent = element_name.text.strip().lstrip(namespace)
            # Test if it is a parent or child and concatenate to the new path
            if not element.getchildren() and element.text:
                new_path = start_path + "/" + parent
            else:
                new_path = start_path + "/" + parent
                BasePage.list_all_full_paths_on_xml(path_list, element, new_path, namespace)
            # Stored the path list
            path_list.append(new_path)
        return path_list

    def compare_pathlist_from_two_xml_responses(context, system_name_a, system_name_b, response_a, response_b,
                                                namespace_a, namespace_b, node_name_a, node_name_b, endpoint_a,
                                                endpoint_b):
        """Given two XML Files or two XML responses, this function search in the both responses or both files divergent
        paths starting from a specific node and validate it. If any divergent path is found an report of divergences
        will be provide. """
        # Get both root
        xml_root_a = BasePage.get_xml_root(response_a, endpoint_a)
        xml_root_b = BasePage.get_xml_root(response_b, endpoint_b)
        # Define the path lists and result lists before call the function
        list_a = []
        list_b = []
        result_a = []
        result_b = []
        # Get the path list
        path_list_a = BasePage.list_all_paths_on_xml_starting_from_node(list_a, xml_root_a, "", namespace_a,
                                                                        node_name_a)
        path_list_b = BasePage.list_all_paths_on_xml_starting_from_node(list_b, xml_root_b, "", namespace_b,
                                                                        node_name_b)
        print("\nResponse Count Path " + system_name_a + ":", len(list(path_list_a)),
              "Response Count Path " + system_name_b + ":", len(list(path_list_b)))
        # Get the intersection of both path lists, sort it alphabetically and count the result
        divergent_paths = sorted(set(path_list_a).symmetric_difference(set(path_list_b)))
        divergent_count = len(list(divergent_paths))
        # If any divergence is found the report will be shown
        if divergent_count == 0:
            pass
        else:
            print("Total Divergent Paths: ", divergent_count, "Divergent Paths List: ", *divergent_paths, sep="\n")
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
            print("\nTotal Divergent Paths " + system_name_a + ":", count_result_a, system_name_a + ":", *result_a,
                  sep="\n")
            print("\nTotal Divergent Paths " + system_name_b + ":", count_result_b, system_name_b + ":", *result_b,
                  sep="\n")
            message = "End of Divergent Paths Report"
            raise Exception(message)

    def get_string_around(string_value, slice_a, slice_b):
        string_a = BasePage.split_string_before(string_value, slice_a)
        string_b = BasePage.split_string_after(string_value, slice_b)
        return (string_a.rstrip() + string_b.rstrip())

    # ----------------------------------------------------------------------------------------------------------------------#
    #                    Functions to manipulate JSON files information and responses                                       #
    # ----------------------------------------------------------------------------------------------------------------------#

    ####----------------------------------------------- JSON Functions --------------------------------------------------####

    def load_json(json_file_path):
        json_file = json_file_path
        with open(json_file, 'r') as file:
            json_data = json.load(file)
            return json_data

    def load_json_as_string(json_file_path):
        json_file = json_file_path
        with open(json_file, 'r') as file:
            json_data = json.loads(file)
            return json_data

    def load_json_as_dict(json_file_path):
        json_file = json_file_path
        with open(json_file, 'r') as file:
            json_data = json.load(file)
            return json_data

    def get_json_keys(json_file_path):
        json_file = load_json_as_dict(json_file_path)
        return json_file.keys()

    def get_json_values(json_file_path):
        json_file = load_json_as_dict(json_file_path)
        return json_file.values()

    def write_json_as_string(json_string):
        new_json = json.dumps(json_string, sort_keys=True)
        # open("new_json.json", "w").write(new_json) --> in a new file
        return new_json

    def write_json_as_dict(json_file_path):
        new_json = json.dump(json_string, sort_keys=True)
        # open("new_json.json", "w").write(new_json) --> in a new file
        return new_json

    def print_new_json(json_file_path, data):
        args = load_csv("datamass_creation/price.csv")
        json1 = edit_json(json_file_path, args)
        print("Editado.....", json1)

    def key_exists(context, key):
        json_key = find_key_on_json(context.json, key)
        if json_key == key:
            return True
        else:
            return False

    def value_is_correct(context, key, value):
        if value == 'null':
            value = None
        if key_exists(context, key) is True:
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
                    return find_value_json(v, key)
        elif type(obj) is list:
            for k, v in enumerate(obj):
                return find_value_json(v, key)

    def find_key_on_json(obj, key):
        if key in obj:
            return key
        for k, v in obj.items():
            if isinstance(v, dict):
                item = find_key_on_json(v, key)
                if item is not None:
                    return item

    def find_key_and_replace_value_json(obj, key, value):
        if key in obj:
            obj[key] = value
            return obj[key]
        if type(obj) is str:
            json.dumps(obj, indent=2, sort_keys=True)
        if type(obj) is dict:
            for k, v in obj.items():
                if isinstance(v, dict):
                    item = find_key_and_replace_value_json(v, key, value)
                    if item is not None:
                        return json.dumps(obj, indent=2, sort_keys=True)
        elif type(obj) is list:
            for k, v in enumerate(obj):
                item = find_key_and_replace_value_json(v, key, value)
                if item is not None:
                    return json.dumps(obj, indent=2, sort_keys=True)

    def simple_edit_json(json_file_path, args_data):
        json_file = json_file_path
        if type(args_data) is list:
            for index, item in enumerate(args_data):
                args = dict(args_data[index])
        else:
            args = args_data
        with open(json_file, 'r') as file:
            data = json.load(file)
            if type(data) is list:
                for index, item in enumerate(data):
                    json_data = dict(data[index])
            else:
                json_data = data
            for args_key, args_value in args.items():
                for key, value in json_data.items():
                    if args_key == key and args_value != value:
                        json_data[key] = args_value
                        v = json_data[key]
                    else:
                        v = json_data[key]
                        if (type(v) is dict) or (type(v) is list):
                            item = find_key_and_replace_value_json(v, args_key, args_value)
                            if (item is not None) or (type(item) is str):
                                json.dumps(json_data, indent=2, sort_keys=True)
                            for v_key, v_value in v.items():
                                v1 = v[v_key]
                                if (type(v1) is dict) or (type(v1) is list):
                                    find_key_and_replace_value_json(v1, args_key, args_value)
        new_json = json.dumps(json_data, indent=2, sort_keys=True)
        return new_json

    def edit_json(json_file_path, args_data):
        new_json = []
        json_file = json_file_path
        if type(args_data) is list:
            for index, item in enumerate(args_data):
                args = eval(args_data[index])
                with open(json_file, 'r') as file:
                    data = json.load(file)
                    if type(data) is list:
                        for index, item in enumerate(data):
                            json_data = dict(data[index])
                    else:
                        json_data = data
                    for args_key, args_value in args.items():
                        for key, value in json_data.items():
                            if args_key == key and args_value != value:
                                json_data[key] = args_value
                                v = json_data[key]
                            else:
                                v = json_data[key]
                                if (type(v) is dict) or (type(v) is list):
                                    item = find_key_and_replace_value_json(v, args_key, args_value)
                                    if (item is not None) or (type(item) is str):
                                        json.dumps(json_data, indent=2, sort_keys=True)
                                    for v_key, v_value in v.items():
                                        v1 = v[v_key]
                                        if (type(v1) is dict) or (type(v1) is list):
                                            find_key_and_replace_value_json(v1, args_key, args_value)
                new_json.append(json.dumps(json_data, sort_keys=True))
        if type(args_data) is dict:
            args = args_data
            with open(json_file, 'r') as file:
                data = json.load(file)
                if type(data) is list:
                    for index, item in enumerate(data):
                        json_data = eval(data[index])
                else:
                    json_data = data
                for args_key, args_value in args.items():
                    for key, value in json_data.items():
                        if args_key == key and args_value != value:
                            json_data[key] = args_value
                            v = json_data[key]
                        else:
                            v = json_data[key]
                            if (type(v) is dict) or (type(v) is list):
                                item = find_key_and_replace_value_json(v, args_key, args_value)
                                if (item is not None) or (type(item) is str):
                                    json.dumps(json_data, indent=2, sort_keys=True)
                                for v_key, v_value in v.items():
                                    v1 = v[v_key]
                                    if (type(v1) is dict) or (type(v1) is list):
                                        find_key_and_replace_value_json(v1, args_key, args_value)
            new_json.append(json.dumps(json_data, sort_keys=True))
        return new_json

    def load_csv(csv_file_path):
        new_json = []
        with open(csv_file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                new_json.append(json.dumps(row, sort_keys=True))
        print(type(new_json))
        return new_json
    
    def old_edit_json(json_file_path, args):
        json_file = json_file_path
        with open(json_file, 'r') as file:
            json_data = json.load(file)
            for args_key, args_value in args.items():
                for key, value in json_data.items():
                    v = json_data[key]
                    if (type(v) is dict) or (type(v) is list):
                        item = BasePage.find_key_and_replace_value_json(v, args_key, args_value)
                        if (item is not None) or (type(item) is str):
                            json.dumps(json_data, indent=2, sort_keys=True)
                        for v_key, v_value in v.items():
                            v1 = v[v_key]
                            if (type(v1) is dict) or (type(v1) is list):
                                BasePage.find_key_and_replace_value_json(v1, args_key, args_value)
        new_json = json.dumps(json_data, indent=2, sort_keys=True)
        return new_json

