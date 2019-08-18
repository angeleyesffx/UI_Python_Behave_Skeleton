from selenium.webdriver.common.action_chains import ActionChains


def move_to(self):
    """
    Move mouse over the page object.

    :returns: self
    :rtype: PageObjectBase instance
    :raises NoSuchElementException: if the element cannot be found
    :raises InvalidSelectorException: if the selector is invalid
        or doesn't select an element
    """
    self.logger.info('moving to page object {}'.format(self._log_id_short))
    self.logger.debug('moving to page object; {}'.format(self._log_id_long))
    action = ActionChains(self.webdriver).move_to_element(self.webelement)
    action.perform()
    self.logger.info('moved to page object {}'.format(self._log_id_short))
    self.logger.debug('moved to page object; {}'.format(self._log_id_long))
    return self

