@property
def text(self):
    """
    Return text of the page object.

    :returns: text of the page object
    :rtype: str
    :raises NoSuchElementException: if the element cannot be found
    :raises InvalidSelectorException: if the selector is invalid
        or doesn't select an element
    """
    return self.webelement.text

