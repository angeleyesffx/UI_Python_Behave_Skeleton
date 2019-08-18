@property
def webelement(self):
    """
    Return a webelement instance.

    :returns: webelement instance
    :rtype: :py:obj:`selenium.webdriver.remote.webelement.WebElement`
    :raises NoSuchElementException: if the element cannot be found
    :raises InvalidSelectorException: if the selector is invalid
        or doesn't select an element

    .. seealso::
        `selenium WebElement documentation`_ (external link)

        .. _`selenium WebElement documentation`: https://seleniumhq\
            .github.io/selenium/docs/api/py/webdriver_remote/selenium\
            .webdriver.remote.webelement.html
    """
    return self.webdriver.find_element_by_xpath(self._locator_value)

