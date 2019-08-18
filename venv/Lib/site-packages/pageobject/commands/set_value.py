from selenium.webdriver.common.keys import Keys


def set_value(self, value, press_enter=False):
    """
    Set value of the page object.

    :param str value: value to set to the page object
    :param bool press_enter: whether to press enter key after
        setting the value (default is False)
    :returns: self
    :rtype: PageObjectBase instance
    :raises NoSuchElementException: if the element cannot be found
    :raises InvalidSelectorException: if the selector is invalid
        or doesn't select an element
    """
    self.clear()
    self.logger.info('setting value of page object {} to "{}"'.format(self._log_id_short, value))
    self.logger.debug('setting value of page object to "{}"; {}'.format(value, self._log_id_long))
    self.webelement.send_keys(value)
    if press_enter:
        self.webelement.send_keys(Keys.ENTER)
    self.logger.info('value of page object {} set to "{}"'.format(self._log_id_short, value))
    self.logger.debug('value of page object set to "{}"; {}'.format(value, self._log_id_long))
    return self

