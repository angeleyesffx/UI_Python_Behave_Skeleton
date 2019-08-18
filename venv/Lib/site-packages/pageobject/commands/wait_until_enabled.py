def wait_until_enabled(self, timeout=None):
    """
    Wait until page object is enabled.

    :param int timeout: number of seconds to wait, if not provided
        PageObject.DEFAULT_WAIT_TIMEOUT is used
    """
    if timeout is None:
        timeout = self.DEFAULT_WAIT_TIMEOUT

    self.logger.info(('waiting until page object {} is enabled'
        ).format(self._log_id_short))
    self.logger.debug(('waiting until page object is enabled; {}'
        ).format(self._log_id_long))

    error_msg = ('page object still not enabled after {} seconds; {}'
        ).format(timeout, self._log_id_long)

    self.wait_until(self.is_enabled, func_kwargs=dict(log=False),
        timeout=timeout, error_msg=error_msg)

    self.logger.info(('finished waiting until page object {} is enabled'
        ).format(self._log_id_short))
    self.logger.debug(('finished waiting until page object is enabled; {}'
        ).format(self._log_id_long))

    return self

