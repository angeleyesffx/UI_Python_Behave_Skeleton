from selenium.common.exceptions import WebDriverException


def is_existing(self, log=True):
    """
    Return True if page object exists in the DOM, False otherwise.

    :param bool log: whether to log or not (default is True)
    :returns: whether page object exists in the DOM
    :rtype: bool
    """
    if log:
        self.logger.info('determining whether page object {} is existing'.format(self._log_id_short))
        self.logger.debug('determining whether page object is existing; {}'.format(self._log_id_long))
    try:
        self.webelement
    except WebDriverException:
        if log:
            self.logger.info('page object {} is not existing'.format(self._log_id_short))
            self.logger.debug('page object is not existing; {}'.format(self._log_id_long))
        return False
    if log:
        self.logger.info('page object {} is existing'.format(self._log_id_short))
        self.logger.debug('page object is existing; {}'.format(self._log_id_long))
    return True

