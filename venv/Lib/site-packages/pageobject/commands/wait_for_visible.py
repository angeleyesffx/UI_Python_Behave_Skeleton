def wait_for_visible(self, timeout=None):
    """
    DEPRECATED! Use wait_until_displayed command instead.
    """
    self.logger.warning('"wait_for_visible" command is deprecated, use "wait_until_displayed" instead!')
    self.wait_until_displayed(timeout=timeout)
    return self

