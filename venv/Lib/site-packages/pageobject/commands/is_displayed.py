def is_displayed(self, log=True):
    """
    Return True if page object is displayed, False otherwise.

    :param bool log: whether to log or not (default is True)
    :returns: whether page object is displayed
    :rtype: bool
    """
    if log:
        self.logger.info('determining whether page object {} is displayed'.format(self._log_id_short))
    self.logger.debug('determining whether page object is displayed; {}'.format(self._log_id_long))
    displayed = self.webelement.is_displayed()
    neg_str = '' if displayed else ' not'
    if log:
        self.logger.info('page object {} is{} displayed'.format(self._log_id_short, neg_str))
    self.logger.debug('page object is{} displayed; {}'.format(neg_str, self._log_id_long))
    return displayed

