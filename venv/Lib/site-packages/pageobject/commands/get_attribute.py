def get_attribute(self, attribute, log=True):
    """
    Return an attribute value of the page object.

    :param str attribute: attribute name
    :param bool log: whether to log or not (default is True)
    :returns: attribute value
    :rtype: str
    :raises NoSuchElementException: if the element cannot be found
    :raises InvalidSelectorException: if the selector is invalid
        or doesn't select an element
    """
    if log:
        self.logger.info('getting attribute "{}" of page object {}'.format(attribute, self._log_id_short))
    self.logger.debug('getting attribute "{}" of page object; {}'.format(attribute, self._log_id_long))
    return self.webelement.get_attribute(attribute)

