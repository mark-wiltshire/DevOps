"""
Web, REST API and Database testing

DEPRECATED - was used for original Local Jenkins run NOT in Docker Version

BOTH web_app.py AND res_app.py must be running

Updated so that if user_id read from user input is already taken
it will use randon user_id for testing.

required arguments
db_host
db_port
db_user
db_pass

Optional arguments
-i --id <test_user_id> to use for testing
-n --name <test_user_name> to use for testing

"""
import argparse
import requests

from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib3.exceptions import MaxRetryError, NewConnectionError

import globals
import db_connector

# parse arguments
parser = argparse.ArgumentParser(description="Run Combined Testing")
parser.add_argument("db_host", type=str, help="the DB host")
parser.add_argument("db_port", type=int, help="the DB port")
parser.add_argument("db_user", type=str, help="the DB username")
parser.add_argument("db_pass", type=str, help="the DB password")
parser.add_argument("-i", "--id", type=int, help="test_user_id to user in testing", default=0)
parser.add_argument("-n", "--name", type=str, help="test_user_name to user in testing", default="")
args = parser.parse_args()

# open and initialise DB Connection
db_connector.get_connection(args.db_host, args.db_port, args.db_user, args.db_pass)
db_connector.init()

# initialise globals
globals.init()

parameters_passed = False


def do_ask_for_int_in_range(range_str="", low=0, high=0):
    """
    Will ask and validate input to check with
    a) have a number
    b) number if in a range (optional)

    :param range_str: String to display on error when number out of range
    :param low: LOW range number must be above
    :param high: HIGHT range number must be below
    :return: int - the number typed in by the user
    """
    while True:
        try:
            my_int = int(input("Enter number " + range_str))
        except ValueError:
            print("Please enter a valid integer " + range_str)
            continue
        if range_str != "":
            if low <= my_int <= high:
                return my_int
            else:
                print('The integer must be in the range ' + range_str)
        else:
            return my_int


# if we don't have test user_id passed ask for one
if args.id == 0:
    args.id = do_ask_for_int_in_range()
# if we don't have test user)name passed ask for one
if args.name == "":
    args.name = input("Enter your name:")

test_user_id = args.id
test_user_name = args.name

print(f"USING TEST DATA test_user_id [{test_user_id}] test_user_name [{test_user_name}]")

print(f"---Test 1--- POST")
# 1 - POST new user data REST API
try:
    res = requests.post('http://127.0.0.1:5000/users/' + str(test_user_id), json={"user_name": test_user_name})
    if res.ok:
        json_response = res.json()
        print(f"SUCCESS POST user_id[{test_user_id}] {json_response}")
        # Check if res.json has user_added_with_new_id - i.e. user_id was changed
        if "user_added_with_new_id" in json_response:
            # if we get this ID for future tests this cycle.
            post_user_id = json_response["user_added_with_new_id"]
            # set following test to use this NEW user_id
            print(f"test_user_id changed to [{post_user_id}] from [{test_user_id}]")
            test_user_id = str(post_user_id)
except (ConnectionRefusedError, NewConnectionError, MaxRetryError, ConnectionError) as e:
    print("***********************************************")
    print(f"Exception - ensure rest_app.py is running [{e}]")
    print("***********************************************")
    raise Exception("Combined Testing failed")

print(f"---Test 2--- GET")
# 2 - GET REST API
res = requests.get('http://127.0.0.1:5000/users/' + str(test_user_id))
if res.ok:
    json_response = res.json()
    read_user_name = json_response["user_name"]
    print(f"GET user_id[{test_user_id}] {json_response}")
    if read_user_name == test_user_name:
        print(f"SUCCESS user_name checked [{test_user_name}] [{read_user_name}]")
    else:
        print(f"ERROR user_names different !!! [{test_user_name}] [{read_user_name}]")
        raise Exception("Test Failed")

print(f"---Test 3--- Check DB")
# 3 - Check data in the database
user_name_read = db_connector.read_user(test_user_id)
if user_name_read == test_user_name:
    print(f"SUCCESS - USER NAME CORRECT WRITTEN TO DB [{test_user_name}] [{user_name_read}]")
else:
    print(f"ERROR - USER NAMES DIFFERENT DB = [{user_name_read}] SENT to REST API = [{test_user_name}]")
    raise Exception("Test Failed")

print(f"---Test 4--- Frontend Testing")
# 4 Start Selenium Webriver
# setup locations
chrome_options = Options()
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chrome_driver_location = "/Users/markwiltshire/Downloads/chromedriver-mac-x64/chromedriver"

driver = webdriver.Chrome(options=chrome_options, service=Service(chrome_driver_location))
driver.implicitly_wait(10)

# 5 Navigate to web interface using the new user id
# Lookup test_user_id from web interface - web_app.py has to be running
try:
    driver.get("http://127.0.0.1:5001/users/get_user_data/" + str(test_user_id))
except WebDriverException as e:
    print(f"WebDriverException - ensure web_app.py is running [{e}]")
    raise Exception("test failed")

try:
    web_get_user_name = driver.find_element(By.ID, value="user").text
    print(f"user_name is [{web_get_user_name}] for user_id [{test_user_id}]")
    # 6 Check the user_name is correct.
    if web_get_user_name == test_user_name:
        print(
            f"SUCCESS Web Interface returned correct user_name for [{test_user_id}] [{test_user_name}] [{web_get_user_name}]")
    else:
        print(
            f"ERROR Web Interface returned incorrect user_name for [{test_user_id}] [{test_user_name}] [{web_get_user_name}]")
        raise Exception("test failed")
except NoSuchElementException as e:
    # id = user not found - find the error
    error_msg = driver.find_element(By.ID, value="error")
    print(f"ERROR Error message is [{error_msg}] for user_id [1]")
    raise Exception("test failed")

# close the current tab
driver.close()

# Close the whole
driver.quit()

# EXTRA - run a delete to clean up after testing
# and close DB cursor and connection
# therefore we can run test again and again
print(f'Cleaning up TEST data - Deleting user_id [{test_user_id}]')
if db_connector.delete_user(test_user_id):
    print(f"Cleaned up - Deleted user_id [{test_user_id}]")
else:
    print(f"Error when deleting user_id[{test_user_id}]")
