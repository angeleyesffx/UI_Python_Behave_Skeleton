# Page commands
from .load import load

# PageObject commands
from .webelement import webelement
from .text import text
from .is_existing import is_existing
from .is_displayed import is_displayed
from .is_visible import is_visible # deprecated
from .is_enabled import is_enabled
from .is_interactive import is_interactive
from .wait_until import wait_until
from .wait_until_existing import wait_until_existing
from .wait_until_displayed import wait_until_displayed
from .wait_until_vanished import wait_until_vanished
from .wait_until_enabled import wait_until_enabled
from .wait_until_interactive import wait_until_interactive
from .wait_for_exist import wait_for_exist # deprecated
from .wait_for_visible import wait_for_visible # deprecated
from .wait_for_vanish import wait_for_vanish # deprecated
from .wait_for_enabled import wait_for_enabled # deprecated
from .wait_for_interactive import wait_for_interactive # deprecated
from .click import click
from .clear import clear
from .get_value import get_value
from .set_value import set_value
from .get_attribute import get_attribute
from .move_to import move_to
from .send_keys import send_keys

# PageObjectList commands
from .text_values import text_values
from .index import index

