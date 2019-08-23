import os
import yaml
import datetime
from selenium import webdriver
from allure_behave.hooks import allure_report
from Screenshot import Screenshot_Clipping

_file_path = os.path.dirname(__file__)
allure_report(_file_path + "/results")


def browser_config(context, browser_name):

    if not browser_name != "firefox":
        option = webdriver.FirefoxOptions()
        option.add_argument("--start-maximized")
        option.add_argument("--disable-geolocation")
        option.add_argument("--ignore-certificate-errors")
        option.add_argument("--disable-popup-blocking")
        option.add_argument("--disable-translate")
        driver = webdriver.Firefox(firefox_options=option)
        return driver

    if not browser_name != "chrome":
        option = webdriver.ChromeOptions()
        option.add_argument("--start-maximized")
        option.add_argument("--disable-geolocation")
        option.add_argument("--ignore-certificate-errors")
        option.add_argument("--disable-popup-blocking")
        option.add_argument("--disable-translate")
        driver = webdriver.Chrome(chrome_options=option)
        return driver

    if not browser_name != "edge":
        driver = webdriver.Edge()
        return driver


def take_screenshot_on_failure(context, scenario):
    path_screenshots = (_file_path + "/screenshots")
    if not os.path.exists(path_screenshots):
        os.makedirs(path_screenshots)
    date_hour = datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S")
    scenario_name = scenario.feature.name.replace(' ', '_')
    print_file_failed = "BUG-" + scenario_name + "-" + date_hour + ".png"
    Screenshot_Clipping.Screenshot().full_Screenshot(context.browser, save_path=path_screenshots, image_name=print_file_failed)


def before_scenario(context, scenario):
    browser_name = context.config.userdata.get('browser')
    driver = browser_config(context, browser_name)
    context.browser = driver
    context.browser.implicitly_wait(10)
    context.browser.set_page_load_timeout(10)
    context.location = context.config.userdata.get('environment')
    environment = yaml.safe_load(open(os.path.dirname(__file__) + "/config.yml"))
    context.location = environment.get(context.config.userdata['environment']).get('url')
    context.browser.get(context.location)

    #--------------iPhone--------------#
    #driver = webdriver.Remote(browser_name="iphone", command_executor='http://172.24.101.36:3001/hub')
    #-------------Android--------------#
    #driver = webdriver.Remote(browser_name="android", command_executor='http://127.0.0.1:8080/hub')


def after_scenario(context, scenario):
    if scenario.status == 'failed':
        take_screenshot_on_failure(context, scenario)
        context.browser.close()
    else:
        context.browser.close()
