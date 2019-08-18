import time
from selenium.common.exceptions import TimeoutException


def wait_until(self, func, func_args=[], func_kwargs={},
        timeout=None, error_msg=None, reverse=False):
    """
    Wait until a condition is met.

    Condition is an arbitrary function with optional args and kwargs
    that returns bool. If reverse=True, wait until the function
    returns False, otherwise wait until the function returns True
    (default).

    :param func: function returning :py:obj:`bool` that is repeatedly
        invoked until it returns correct value
    :param list func_args: list of args to be passed to func
    :param dict func_kwargs: dict of kwargs to be passed to func
    :param int timeout: number of seconds to try to call func,
        if not provided, PageObject.DEFAULT_WAIT_TIMEOUT is used
    :param str error_msg: error message to attach to the exception
        raised when the condition is not met in time
    :param bool reverse: flag indicating whether to wait until
        the condition is True or False
    :type func: function
    :raises TimeoutException: if the condition is not met in time
    """
    if timeout is None:
        timeout = self.DEFAULT_WAIT_TIMEOUT
    deadline = time.time() + timeout
    while time.time() < deadline:
        if bool(func(*func_args, **func_kwargs)) is not reverse:
            return self
        time.sleep(self.DEFAULT_POLL_INTERVAL)
    if error_msg is None:
        error_msg = ('function {} called with args {} and kwargs '
                    + '{} still returns {} after {} seconds').format(
                func, func_args, func_kwargs, reverse, timeout)
    raise TimeoutException(error_msg)

