def wait_until_vanished(self, timeout=None):
    """
    Wait until page object vanishes from the DOM.

    :param int timeout: number of seconds to wait, if not provided
        PageObject.DEFAULT_WAIT_TIMEOUT is used
    """
    if timeout is None:
        timeout = self.DEFAULT_WAIT_TIMEOUT

    self.logger.info(('waiting until page does not contain page object {}'
        ).format(self._log_id_short))
    self.logger.debug(('waiting until page does not contain page object; {}'
        ).format(self._log_id_long))

    error_msg = ('page object still existing after {} seconds; {}'
        ).format(timeout, self._log_id_long)

    self.wait_until(self.is_existing, func_kwargs=dict(log=False),
        timeout=timeout, error_msg=error_msg, reverse=True)

    self.logger.info(('finished waiting until page does not contain'
        + ' page object {}').format(self._log_id_short))
    self.logger.debug(('finished waiting until page does not contain'
        + ' page object; {}').format(self._log_id_long))

    return self

