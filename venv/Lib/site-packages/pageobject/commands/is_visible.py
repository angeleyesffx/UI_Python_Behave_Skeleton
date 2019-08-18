def is_visible(self, log=True):
    """
    DEPRECATED! Use is_displayed command instead.
    """
    self.logger.warning('"is_visible" command is deprecated, use "is_displayed" instead!')
    return self.is_displayed(log=log)

