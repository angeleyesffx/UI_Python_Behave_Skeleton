def wait_for_interactive(self, timeout=None):
    """
    DEPRECATED! Use wait_until_interactive command instead.
    """
    self.logger.warning('"wait_for_interactive" command is deprecated, use "wait_until_interactive" instead!')
    self.wait_until_interactive(timeout=timeout)
    return self

