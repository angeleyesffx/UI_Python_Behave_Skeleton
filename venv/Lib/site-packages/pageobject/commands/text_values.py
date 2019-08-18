@property
def text_values(self):
    """
    Return list of text values of PageObjectList children.

    :returns: index of the first child containing the specified value
    :returns: list of text values (innerHTML)
    :rtype: list of str
    """
    self.logger.info('getting children text values of page object list {}'.format(self._log_id_short))
    self.logger.debug('getting children text values of page object list; {}'.format(self._log_id_long))
    values = [child.text for child in self.children]
    self.logger.info('children text values of page object list {} are: {}'.format(values, self._log_id_short))
    self.logger.debug('children text values of page object list are: {}; {}'.format(values, self._log_id_long))
    return values

