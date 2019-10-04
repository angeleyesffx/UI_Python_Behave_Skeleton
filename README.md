# Python-Behave

**Install Python/behave framework**

**IMPORTANT ---->>>>  This automation needs Python 3.6 or above**

***Step 1:*** Download and Install the latest version of Python on the official site: https://www.python.org/downloads/
        
You can find Installation Guide to your system here:  https://realpython.com/installing-python/


***Step 2:*** Install or Update pip
        
You can find Installation Guide to your system here:  https://pypi.org/project/pip/


***Step 3:*** Install behave and all dependencies listed on requirements.txt inside your project
        Execute the command line:
        
* `pip install -r requirements.txt` 

**IMPORTANT ---->>>>  If you need to install the dependencies in separate execute the command line:**
                  
                  
> **Make sure that your pip installation is updated!** 

        
* `pip install SomeDependencie` 

***Step 4:*** Install Selenium and the apropriate webdrivers
       
You can find a installation Guide here:  https://selenium-python.readthedocs.io/installation.html
Download links for your driver Driver:
        
        
| Browser | Link                                                                  |
| ------  | --------------------------------------------------------------------- |
| Chrome: | https://sites.google.com/a/chromium.org/chromedriver/downloads        |
| Edge:   | https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ | 
| Firefox:| https://github.com/mozilla/geckodriver/releases                       | 
| Safari: | https://webkit.org/blog/6900/webdriver-support-in-safari-10/          | 
       

**User Guide of Behave Framework:**

You can find information about behave framework here:  https://behave.readthedocs.io/en/latest/

For change the environment use -D environment=SOME_ENVIRONMENT like command line below:
        *The default environment is always define by behave.ini*
      
*   `python -m behave -D environment=homolog` 

For change the browser use -D browser=SOME_BROWSER like command line below:
        *The default browser is always define by behave.ini*
       
*  `python -m behave -D browser=headless-chrome` 

For execute a specific feature execute the command line:
        
* `python -m behave features_path/feature_name.feature` 

For execute a specific WIP scenario or a list of WIP scenarios use above scenario @wip and execute the command line:
      
*   `python -m behave -D environment=desenv --tags=@wip` 

By default, behave captures stdout, this captured output is only shown if a failure occurs.
To print output execute the command line:
    
*    ` python -m behave --no-capture `

**IMPORTANT ---->>>>  You can combine the command lines to execute your project**

Example:
      
*  `python -m behave --no-capture -D environment=desenv -D browser=firefox --tags=@wip features_path/feature_name.feature` 



