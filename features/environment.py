from features.pages.homepage import HomePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# local dir used to wait for an element in main/home page
local_directories = {
    "searching_bar": (By.ID, 'horus-querytext')
}
# tuple used for wait element
find_it = local_directories["searching_bar"]


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

def before_scenario(context, scenario):
    option = webdriver.ChromeOptions()
    option.add_argument("--start-maximized")
    # driver = webdriver.Firefox()
    context.location = "http://www.google.com"
    context.browser = webdriver.Chrome()  # if you have set chromedriver in your PATH
    context.browser.implicitly_wait(5)
    context.browser.set_page_load_timeout(5)
    context.browser.get(context.location)
    context.home_page = HomePage(context.browser, context.location)


# context.search_bar = SearchBar(context.browser, context.location)
# context.searching_page = SearchingPage(context.browser, context.location)


def wait_for_click_element(context, find_it):
    try:
        wait = WebDriverWait(context.browser, 5)
        expected_element = EC.element_to_be_clickable(find_it)
        wait.until(expected_element)
    except TimeoutError:
        raise


def close(self):
    self.driver.close()
