from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class BasePage(object):
    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url
        self.timeout = 5
        self.implicit_wait = 5

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

    def instance_page(page_name, context):
        return page_name(context.browser, context.location)

    def wait_till_specific_element_is_not_displayed(self, element):
        try:
            wait = WebDriverWait(self.browser, self.implicit_wait)
            expected_element = EC.visibility_of_element_located(element)
            wait.until(expected_element)
            return True
        except TimeoutError:
            raise

# JSON preparation if more info stored in the config file
# def load_json(json_file):
#     data = load_file(json_file)
#     json_data = json.loads(data)
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
