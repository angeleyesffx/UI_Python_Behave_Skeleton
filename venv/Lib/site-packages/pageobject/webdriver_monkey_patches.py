from selenium.webdriver import Remote as WebDriver
from .pageobjectbase import PageObjectBase


def __setattr__(self, attr_name, attr_value):
    """
    Register self as parent if attribute value is a page object.
    """
    object.__setattr__(self, attr_name, attr_value)
    if isinstance(attr_value, PageObjectBase):
        child = attr_value
        child.__dict__['_parent'] = self

WebDriver.__setattr__ = __setattr__

