def wait_for_exist(self, timeout=None):
    """
    DEPRECATED! Use wait_until_existing command instead.
    """
    self.logger.warning('"wait_for_exist" command is deprecated, use "wait_until_existing" instead!')
    self.wait_until_existing(timeout=timeout)
    return self

