from selenium.webdriver.common.by import By

from features.pages.basepage import BasePage


class HomePage(BasePage):
 
    project_url = "https://www.google.com/?gws_rd=ssl"
    search_bar = "q"
    search_button = "body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > div.A8SBwf.emcav > div.UUbT9 > div.aajZCb > div.lJ9FBc > center > input.gNO89b"
    first_result = "#rso > div:nth-child(1) > div > div > div > div > div > div > div.yuRUbf > a > h3"

    #project_url = "https://www.trivago.ie/"

    local_directories = {

        "slogan": "hero__title",
        "filter_on_search_page": "js_filterlist",
    }