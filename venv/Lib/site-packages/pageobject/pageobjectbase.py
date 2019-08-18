import logging
from selenium.webdriver import Remote as WebDriver
from .locator import Locator


class PageObjectBase(object):
    """
    Abstract page object base class.

    All the other classes inherit from this one.
    """

    DEFAULT_ROOT_NAME = 'root'
    """Default name for a root page object."""

    NAME_SEPARATOR = '.'
    """Separator character for long (chained) page object names."""

    DEFAULT_WAIT_TIMEOUT = 60
    """Default timeout (in seconds) for wait commands."""

    DEFAULT_POLL_INTERVAL = 0.25
    """Poll interval (in seconds) for wait commands."""


    def __nonzero__(self):      # pragma: no cover
        return self.__bool__()  # Python 2 throwback


    def __repr__(self):
        my_class = self.__class__.__name__
        base_class = self.__class__.__bases__[0].__name__
        return '<{}({}) (full_name="{}")>'.format(my_class,
            base_class, self.full_name)


    @property
    def parent(self):
        """
        Return the parent of the page object.

        :returns: Parent page object.
        :rtype: :class:`pageobject.pageobjectbase.PageObjectBase` or `None` (default)
        """
        return self._parent


    @property
    def default_locator(self):
        """
        Return default locator, None by default.

        May be overridden to take precedence over the locator
        provided to constructor.

        :returns: default locator
        :rtype: `None` (default) or `str` (if overridden)
        """
        return None


    @property
    def _parent_locator(self):
        """
        Return the locator of the parent page object.

        :returns: Locator of parent or None if parent does not exist
        :rtype: Locator or None
        """
        try:
            return self.parent._locator
        except AttributeError:
            return None


    @property
    def _parent_locator_value(self):
        """
        :returns: value of the parent locator
        :rtype: str
        """
        try:
            return self._parent_locator.value
        except AttributeError:
            return None


    @property
    def _provided_locator(self):
        """
        :returns: locator string provided either to the constructor
            or as an overridden default_locator property
        :rtype: str
        """
        if self.default_locator:
            return self.default_locator
        else:
            return self._initialized_locator


    @property
    def _locator_class(self):
        """
        :returns: locator class
        :rtype: Locator
        """
        return Locator


    @property
    def _locator(self):
        """
        :returns: Locator of the page object
        :rtype: Locator instance
        """
        LocatorClass = self._locator_class
        return LocatorClass(self._provided_locator, page_object=self)


    @property
    def _locator_value(self):
        """
        :returns: processed locator value ready to be passed
            to a webdriver find method
        :rtype: str
        """
        return self._locator.value


    @property
    def locator(self):
        """
        Publicly exposed locator value.

        :returns: locator value
        :rtype: str
        """
        return self._locator_value


    @property
    def webdriver(self):
        """
        Return the instance of WebDriver.

        If parent exists, use the webdriver property of the parent.
        Otherwise use the value provided to constructor.

        :returns: reference to the webdriver instance
        :rtype: `selenium.webdriver.Remote`
        :raises AssertionError: if the webdriver is not a valid WebDriver
        """
        try:
            if isinstance(self.parent, WebDriver):
                return self.parent
            else:
                return self.parent.webdriver
        except AttributeError:
            error_msg = ('webdriver should be an instance of selenium'
                        + ' WebDriver, instead is "{}"').format(self._webdriver)
            assert isinstance(self._webdriver, WebDriver), error_msg
            return self._webdriver


    @property
    def logger(self):
        """
        Return the logger object.

        :returns: standard logging module
        :rtype: :py:obj:`logging`
        """
        return logging


    @property
    def name(self):
        """
        Return name of the page object instance.

        If parent exists, ask for its child name, otherwise use the name
        provided to constructor. If that doesn't exist either,
        use `DEFAULT_ROOT_NAME`.

        :returns: Name of the page object.
        :rtype: `str`
        """
        try:
            return self.parent._get_child_name(self)
        except AttributeError:
            if self._name:
                return self._name
            else:
                return self.__class__.DEFAULT_ROOT_NAME


    @property
    def full_name(self):
        """
        Return full name of the page object instance.

        If parent exists, ask for its child full name, otherwiser use
        normal short name.

        :returns: Full name of the pge object.
        :rtype: `str`

        .. seealso::
            :py:func:`_get_child_full_name`

        """
        try:
            return self.parent._get_child_full_name(self)
        except AttributeError:
            return self.name


    @property
    def tree(self):
        """
        :returns: Hierarchical tree of page object and its descendants.
        :rtype: `dict`
        """
        return {self.name: self._descendants}


    @property
    def _log_id_short(self): # pragma: no cover
        """
        :returns: String identifying the page object by its full name.
        :rtype: str
        """
        return '"{}"'.format(self.full_name)


    @property
    def _log_id_long(self): # pragma: no cover
        """
        :returns: String identifying the page object
            by its full name and locator.
        :rtype: str
        """
        return 'full name: "{}", locatort: "{}"'.format(
                self.full_name, self._locator_value)

