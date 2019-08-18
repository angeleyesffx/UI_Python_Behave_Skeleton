from .singlepageobjectbase import SinglePageObjectBase
from .locator import Locator
from . import commands


class Page(SinglePageObjectBase):
    """Web page class."""

    DEFAULT_ROOT_NAME = 'page'
    """Default name for a root page object."""


    def __init__(self, url=None, locator='', chain=True, webdriver=None, name=None):
        """
        Create a page and its children page objects.

        :param str url: Url of the page. Must start with a valid
            protocol (like http)
        :param str locator: Xpath describing location of the page
            object in the DOM.
        :param bool chain: Determines whether to chain locator
            to its parent.
        :param webdriver: Only needs to be provided if the page
            is also a root page object.
        :param str name: Name used when the page is a root.
        :type webdriver: :py:obj:`selenium.webdriver.Remote` instance
            or :py:obj:`None`

        :Example usage:

        .. code-block:: python

            from pageobject import Page
            from selenium import webdriver
            wd = webdriver.Chrome()
            python_org_page = Page(url="http://www.python.org", webdriver=wd)

        """
        self._initialized_url = url
        self._initialized_locator = locator
        self._chain = chain
        self._webdriver = webdriver
        self._name = name
        self._parent = None

        self.init_children()


    @property
    def requested_url(self):
        """
        Return requested url, None by default.

        May be overridden to take precedence over the url
        provided to constructor.

        :returns: requested url of the page
        :rtype: str
        """
        return None


    @property
    def _provided_url(self):
        """
        :returns: url string provided either as an overridden
            requested_url attribute or passed to the constructor
        :rtype: str
        """
        if self.requested_url:
            return self.requested_url
        else:
            return self._initialized_url


    # commands
    load = commands.load

