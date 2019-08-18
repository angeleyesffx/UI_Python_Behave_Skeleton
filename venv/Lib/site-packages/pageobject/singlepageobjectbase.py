from .pageobjectbase import PageObjectBase
from . import commands


class SinglePageObjectBase(PageObjectBase):

    def __bool__(self):
        """
        Delegate to is_existing command.

        .. seealso::
            :py:func:`commands.is_existing`
        """
        return self.is_existing(log=False)


    def __getitem__(self, key):
        return self.children[key]


    def __len__(self):
        return len(self.children)


    def __setattr__(self, attr_name, attr_value):
        """
        Register self as parent if attribute value is a page object.
        """
        object.__setattr__(self, attr_name, attr_value)
        if attr_name is not '_parent' and isinstance(attr_value, PageObjectBase):
            child = attr_value
            child.__dict__['_parent'] = self


    def init_children(self): # pragma: no cover
        """
        Initialize children of the page object.

        Intended to be overridden by page objects
        containing other page objects.

        :rtype: :py:obj:`None`
        """
        pass


    @property
    def children(self):
        """
        Return dict of page object children.

        :returns: children of the page object
        :rtype: :py:obj:`dict`
        """
        return {attr_name: attr_value for attr_name, attr_value in self.__dict__.items()
                if isinstance(attr_value, PageObjectBase)
                and attr_value is not self.parent}


    def _get_child_name(self, child_po):
        """
        Return name of a child page object.

        :returns: name of a child page object
        :rtype: :py:obj:`str`
        """
        for child_name in self.children:
            if self.__dict__[child_name] == child_po:
                return child_name


    def _get_child_full_name(self, child_po):
        """
        Return full name of a child page object.

        :returns: full name of a child page object
        :rtype: :py:obj:`str`
        """
        return '{}{}{}'.format(self.full_name, self.__class__.NAME_SEPARATOR,
                child_po.name)


    @property
    def _descendants(self):
        """
        Return descendants of the page object.

        :returns: hierarchical tree of descendants of the page object
        :rtype: :py:obj:`dict`
        """
        descendants = dict()
        for child_name, child in self.children.items():
            if not isinstance(child, SinglePageObjectBase):
                child_name = '{}[i]'.format(child_name)
            descendants[child_name] = child._descendants
        return descendants


    # commands
    webelement = commands.webelement
    text = commands.text
    get_attribute = commands.get_attribute
    is_existing = commands.is_existing
    wait_until = commands.wait_until
    wait_until_existing = commands.wait_until_existing
    wait_until_vanished = commands.wait_until_vanished
    wait_for_exist = commands.wait_for_exist # deprecated
    wait_for_vanish = commands.wait_for_vanish

