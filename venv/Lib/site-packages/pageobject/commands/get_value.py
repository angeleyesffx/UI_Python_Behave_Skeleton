def get_value(self):
    """
    Return value of the page object.

    :returns: value of the page object
    :rtype: str
    :raises NoSuchElementException: if the element cannot be found
    :raises InvalidSelectorException: if the selector is invalid
        or doesn't select an element
    """
    self.logger.info('getting value of page object {}'.format(self._log_id_short))
    self.logger.debug('getting value of page object; {}'.format(self._log_id_long))
    value = self.webelement.get_attribute('value')
    self.logger.info('value of page object {} is "{}"'.format(self._log_id_short, value))
    self.logger.debug('value of page object is "{}"; {}'.format(value, self._log_id_long))
    return value

