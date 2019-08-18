#!C:\Users\angel_000\Desktop\TestLetucce\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'lettuce-webdriver==0.3.5','console_scripts','lettuce_webdriver'
__requires__ = 'lettuce-webdriver==0.3.5'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('lettuce-webdriver==0.3.5', 'console_scripts', 'lettuce_webdriver')()
    )
