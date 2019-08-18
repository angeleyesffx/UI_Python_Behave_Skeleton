def click(self):
    """
    Click the page object.

    :returns: self
    :rtype: PageObjectBase instance
    :raises NoSuchElementException: if the element cannot be found
    :raises InvalidSelectorException: if the selector is invalid
        or doesn't select an element
    """
    self.logger.info('clicking on page object {}'.format(self._log_id_short))
    self.logger.debug('clicking on page object; {}'.format(self._log_id_long))
    self.webelement.click()
    self.logger.info('successfully clicked on page object {}'.format(self._log_id_short))
    self.logger.debug('successfully clicked on page object; {}'.format(self._log_id_long))
    return self

