from .pageobjectbase import PageObjectBase
from . import commands


class PageObjectListBase(PageObjectBase):
    """
    Abstract page object list base class.

    All list-like PageObjectList classes inherit from this one.
    """

    def __bool__(self):
        return bool(len(self))


    def __getitem__(self, slice):
        return self.children[slice]


    def __len__(self):
        """
        Return number of children.

        :returns: number of children
        :rtype: :py:obj:`int`
        """
        return len(self.children)


    def _get_child_name(self, child_po):
        """
        Return indexed name of a child page object.

        :returns: indexed name of a child page object
        :rtype: :py:obj:`str`
        """
        return '{}[{}]'.format(self.name, child_po.index)


    def _get_child_full_name(self, child_po):
        """
        Return indexed full name of a child page object.

        :returns: indexed full name of a child page object
        :rtype: :py:obj:`str`
        """
        return '{}[{}]'.format(self.full_name, child_po.index)


    @property
    def _descendants(self):
        """
        Return descendants of the children_class dummy instance.

        :returns: hierarchical tree of descendants
            of the children_class dummy instance
        :rtype: :py:obj:`dict`
        """
        return self.children_class(None)._descendants


    # commands
    text_values = commands.text_values
    index = commands.index

