from .pageobject import PageObject
from selenium.webdriver.support.ui import Select as Python2IncompatibleSelect


class WebDriverSelect(Python2IncompatibleSelect, object):
    """
    Temporary abstract class.

    This is a workaround for selenium.webdriver.support.ui.Select class
    not inheriting from object.

    TODO: Get rid of this class when the below PR is merged:
    https://github.com/SeleniumHQ/selenium/pull/3067
    """
    pass


class Select(PageObject):
    """
    Select page object class.

    Extends PageObject class and attempts to delegate unrecognized
    attributes to selenium Select class.

    .. seealso::
        `selenium Select class documentation`_ (external link)

        .. _`selenium select class documentation`: http://seleniumhq\
            .github.io/selenium/docs/api/py/webdriver_support/selenium\
            .webdriver.support.select.html
    """

    @property
    def _select_class(self):
        """
        Return the selenium Select class.

        :returns: selenium Select class
        :rtype: :py:obj:`selenium.webdriver.support.ui.Select` class
        """
        return WebDriverSelect


    @property
    def elem(self):
        """
        Return select element to which to delegate webdriver methods.

        :returns: select webelement
        :rtype: :py:obj:`selenium.webdriver.support.ui.Select` instance
        """
        return self._select_class(self.webelement)


    def __getattr__(self, attribute_name):
        """
        Delegate unrecognized attributes to selenium Select class.
        """
        return self.elem.__getattribute__(attribute_name)

