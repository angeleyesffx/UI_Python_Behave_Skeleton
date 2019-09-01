from selenium.webdriver.common.by import By

from features.pages.basepage import BasePage


class HomePage(BasePage):

    project_url = "https://www.trivago.ie/"

    local_directories = {

        "slogan": "hero__title",
        "filter_on_search_page": "js_filterlist"

    }