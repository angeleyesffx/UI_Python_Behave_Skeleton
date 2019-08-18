def is_interactive(self, log=True):
    """
    Return True if page object is interactive, False otherwise.

    Interactive means both displayed and enabled. This is called
    "clickable" in selenium, which may be misleading,
    as an element can be both displayed and enabled, but not really
    clickable, because another element may cover it and prevent
    it from receiving the click.

    :param bool log: whether to log or not (defualt is True)
    :returns: whether page object is interactive
    :rtype: bool
    """
    if log:
        self.logger.info(('determining whether page object {} is interactive'
            ).format(self._log_id_short))
    self.logger.debug(('determining whether page object is interactive'
        + '; {}').format(self._log_id_long))

    interactive = self.is_displayed(log=False) and self.is_enabled(log=False)

    msg_str = '' if interactive else ' not'
    if log:
        self.logger.info('page object {} is{} interactive'.format(
            msg_str, self._log_id_long))
    self.logger.debug('page object is{} interactive; {}'.format(
        msg_str, self._log_id_long))

    return interactive

