"""*pageobject*'s main module"""

__version__ = '0.0.52'

from .page import Page
from .pageobject import PageObject
from .pageobjectlist import PageObjectList
from .select import Select

from . import webdriver_monkey_patches

