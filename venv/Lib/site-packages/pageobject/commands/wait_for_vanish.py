def wait_for_vanish(self, timeout=None):
    """
    DEPRECATED! Use wait_until_vanished command instead.
    """
    self.logger.warning('"wait_for_vanish" command is deprecated, use "wait_until_vanished" instead!')
    self.wait_until_vanished(timeout=timeout)
    return self

