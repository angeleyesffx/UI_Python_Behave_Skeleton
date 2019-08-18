from selenium.webdriver.common.keys import Keys


def clear(self, log=True, press_enter=False):
    """
    Clear the page object.

    :param bool log: whether to log or not (defualt is True)
    :param bool press_enter: whether to press enter key after
        the element is cleared (defualt is False)
    :returns: self
    :rtype: PageObjectBase instance
    :raises NoSuchElementException: if the element cannot be found
    :raises InvalidSelectorException: if the selector is invalid
        or doesn't select an element
    """
    if log:
        self.logger.info('clearing page object {}'.format(self._log_id_short))
    self.logger.debug('clearing page object; {}'.format(self._log_id_long))
    self.webelement.clear()
    if log:
        self.logger.info('page object {} cleared'.format(self._log_id_short))
    self.logger.debug('page object cleared; {}'.format(self._log_id_long))
    if press_enter:
        self.webelement.send_keys(Keys.ENTER)
        if log:
            self.logger.info('"enter" key sent to page object {}'.format(self._log_id_short))
        self.logger.debug('"enter" key sent to page object; {}'.format(self._log_id_long))
    return self

