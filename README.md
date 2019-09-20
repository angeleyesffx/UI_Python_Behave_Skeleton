# Python-Behave

For change the environment use -D environment=SOME_ENVIRONMENT like command line below:
#The default environment is always define by behave.ini
python -m behave -D environment=homolog

For change the browser use -D browser=SOME_BROWSER like command line below:
#The default browser is always define by behave.ini
python -m behave -D browser=headless-chrome

For WIP scenario use above scenario @wip and execute the command line:
python -m behave -D environment=desenv --tags=@wip

By default, behave captures stdout, this captured output is only shown if a failure occurs
To print output execute the command line:
python -m behave --no-capture
