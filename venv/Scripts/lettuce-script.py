#!C:\Users\angel_000\Desktop\TestLetucce\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'lettuce==0.2.23','console_scripts','lettuce'
__requires__ = 'lettuce==0.2.23'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('lettuce==0.2.23', 'console_scripts', 'lettuce')()
    )
