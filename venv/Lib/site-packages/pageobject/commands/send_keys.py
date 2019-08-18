from selenium.webdriver.common.utils import keys_to_typing


def send_keys(self, keys, log=True):
    """
    Send keys to the page object.

    :param keys: keys to send to the page object
    :param bool log: whether to log or not (default is True)
    :type keys: iterable of string type
    :returns: self
    :rtype: PageObjectBase instance
    :raises NoSuchElementException: if the element cannot be found
    :raises InvalidSelectorException: if the selector is invalid
        or doesn't select an element
    """
    single_keys = keys_to_typing(keys)
    if log:
        self.logger.info('sending keys {} to page object {}'.format(single_keys, self._log_id_short))
    self.logger.debug('sending keys {} to page object; {}'.format(single_keys, self._log_id_long))
    self.webelement.send_keys(keys)
    if log:
        self.logger.info('sent keys {} to page object {}'.format(single_keys, self._log_id_short))
    self.logger.debug('sent keys {} to page object; {}'.format(single_keys, self._log_id_long))
    return self

