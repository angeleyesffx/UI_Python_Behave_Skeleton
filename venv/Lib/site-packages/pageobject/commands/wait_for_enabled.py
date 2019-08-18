def wait_for_enabled(self, timeout=None):
    """
    DEPRECATED! Use wait_until_enabled command instead.
    """
    self.logger.warning('"wait_for_enabled" command is deprecated, use "wait_until_enabled" instead!')
    self.wait_until_enabled(timeout=timeout)
    return self

