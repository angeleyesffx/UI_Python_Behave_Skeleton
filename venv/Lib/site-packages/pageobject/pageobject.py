from .singlepageobjectbase import SinglePageObjectBase
from .locator import Locator
from . import commands


class PageObject(SinglePageObjectBase):
    """Main general-purpose page object class."""

    DEFAULT_ROOT_NAME = 'page_object'
    """Default name for a root page object."""


    def __init__(self, locator, chain=True, webdriver=None, name=None):
        """
        Create a page object and its children.

        :param str locator: Xpath describing location of the page
            object in the DOM.
        :param bool chain: Determines whether to chain locator
            to its parent.
        :param webdriver: Only needs to be provided for root page object.
        :param str name: Name used when the page object is a root.
        :type webdriver: :class:`selenium.webdriver.Remote` instance or None

        :Example usage:

        .. code-block:: python

            from pageobject import PageObject
            top_panel = PageObject("//*[@class='topPanel']")

        """
        self._initialized_locator = locator
        self._chain = chain
        self._webdriver = webdriver
        self._name = name
        self._parent = None

        self.init_children()


    # commands
    is_enabled = commands.is_enabled
    is_displayed = commands.is_displayed
    is_visible = commands.is_visible # deprecated
    is_interactive = commands.is_interactive
    wait_until_displayed = commands.wait_until_displayed
    wait_for_visible = commands.wait_for_visible # deprecated
    wait_until_enabled = commands.wait_until_enabled
    wait_for_enabled = commands.wait_for_enabled # deprecated
    wait_until_interactive = commands.wait_until_interactive
    wait_for_interactive = commands.wait_for_interactive # deprecated
    click = commands.click
    clear = commands.clear
    get_value = commands.get_value
    set_value = commands.set_value
    move_to = commands.move_to
    send_keys = commands.send_keys

