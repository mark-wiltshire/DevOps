"""
frontend_testing.py

Front End testing the web_app.py MUST be running

Hardcoded the Chrome and Chromedriver locations

DEPRECATED - was used for original Local Jenkins run NOT in Docker Version
"""
import sys

from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# TODO would be nice to have these automatically picked up - i.e. not hardcoded
# TODO need to use globals to set browser version ran out of time.
# setup locations
chrome_options = Options()
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chrome_driver_location = "/Users/markwiltshire/Downloads/chromedriver-mac-x64/chromedriver"

driver = webdriver.Chrome(options=chrome_options, service=Service(chrome_driver_location))
driver.implicitly_wait(10)


def output_versions():
    """
    Utility function to output the current versions
    - Python, Selenium, Chrome, Chromedriver
    :return:
    """
    print(f"************************************")
    # output python version
    print(f"Python version: \t\t [{sys.version} {sys.version_info}]")

    # output selenium version
    print(f"Selenium version: \t\t [{webdriver.__version__}]")

    # output browser and chromedriver versions
    # driver has to have been setup
    str1 = driver.capabilities['browserVersion']
    str2 = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    print(f"Chrome version: \t\t [{str1}]")
    print(f"Chromedriver version: \t [{str2}] - https://chromedriver.chromium.org/downloads ")
    print(f"************************************")


# output our versions
output_versions()

print(f"---Test 1--- POST")
# Lookup user_id 1 from web interface - web_app.py has to be running
try:
    driver.get("http://127.0.0.1:5001/users/get_user_data/1")
except WebDriverException as e:
    print(f"ERROR - WebDriverException - ensure web_app.py is running [{e}]")
    raise Exception("Frontend Testing Failed")

try:
    user_name = driver.find_element(By.ID, value="user").text
    print(f"SUCCESS - user_name is [{user_name}] for user_id [1]")
except NoSuchElementException as e:
    # id = user not found - find the error
    error_msg = driver.find_element(By.ID, value="error")
    print(f"ERROR Error message is [{error_msg}] for user_id [1]")
    raise Exception("Frontend Testing Failed")

# close the current tab
driver.close()

# Close the whole
driver.quit()
