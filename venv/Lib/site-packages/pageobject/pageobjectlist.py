from .pageobjectlistbase import PageObjectListBase
from .pageobject import PageObject
from .locator import Locator


class PageObjectList(PageObjectListBase):

    def __init__(self, locator, chain=True, children_class=None,
            children_locator=None, count_locator=None):
        """
        Create page object list of children of the same type.

        :param str locator: Xpath locator of children page objects
            for simple indexing of children in a one-level of nesting.
        :param bool chain: Determines whether to chain locator
            to its parent.
        :param children_class: Class to use for instantiation
            of children page objects.
        :param str children_locator: Locator of children page objects
            offering more control over what will be indexed, necessary
            for more deeply nested children.
        :param str count_locator: Xpath determining the number of
            children, necessary for more deeply nested children.
        :type children_class: PageObjectBase
        """
        self._initialized_locator = locator
        self._chain = chain
        self._children_class = children_class
        self._initialized_children_locator = children_locator
        self._initialized_count_locator = count_locator
        self._parent = None


    @property
    def _children_count(self):
        return len(self.webdriver.find_elements_by_xpath(self._count_locator_value))


    @property
    def children(self):
        """
        Return list of children page objects.

        :returns: list of children page objects
        :rtype: :py:obj:`list` of PageObjectBase instances
        """
        children = []
        ChildrenClass = self.children_class
        for i in range(self._children_count):
            locator = self._children_locator_value.format(i+1)
            child = ChildrenClass(locator, chain=False)
            child.index = i
            child._parent = self
            children.append(child)
        return children


    @property
    def children_class(self):
        """
        Return class to use for children instantiation.

        :returns: Class for children instantiation.
        :rtype: PageObjectBase subclass
        """
        if self._children_class:
            return self._children_class
        else:
            return PageObject


    @property
    def default_children_locator(self):
        """
        Return defualt children locator, None by default.

        May be overridden to take precedence over the children_locator
        provided to constructor.

        :returns: default children locator
        :rtype: :py:obj:`None` (default) or :py:obj:`str`
            (if overridden)
        """
        return None


    @property
    def _provided_children_locator(self):
        """
        :returns: children locator string provided either as an overridden
            default_children_locator or passed to the constructor
        :rtype: str
        """
        if self.default_children_locator:
            return self.default_children_locator
        elif self._initialized_children_locator:
            return self._initialized_children_locator
        else:
            return '({})[{}]'.format(self._locator_value, '{}')


    @property
    def _children_locator_value(self):
        """
        :returns: processed children locator value ready to be passed
            to a webdriver find method
        :rtype: str
        """
        return self._provided_children_locator


    @property
    def default_count_locator(self):
        """
        Return default count locator, None by default.

        May be overridden to take precedence over the count_locator
        provided to constructor

        :returns: defualt count locator
        :rtype: :py:obj:`None` (default) or :py:obj:`str`
            (if overridden)
        """
        return None


    @property
    def _provided_count_locator(self):
        """
        :returns: count locator string provided either as an overridden
            default_count_locator or passed to the constructor
        :rtype: str
        """
        if self.default_count_locator:
            return self.default_count_locator
        elif self._initialized_count_locator:
            return self._initialized_count_locator
        else:
            return self._locator_value


    @property
    def _count_locator_value(self):
        """
        :returns: processed count locator value ready to be passed
            to a webdriver find method
        :rtype: str
        """
        return self._provided_count_locator

