"""
Web, REST API and Database testing

BOTH web_app.py AND res_app.py must be running
"""
import pymysql
import requests
from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib3.exceptions import MaxRetryError

import globals

globals.init()

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


# Get TESTING data from user
test_user_id = do_ask_for_int_in_range()
test_user_name = input("Enter your name:")

# 1 - POST new user data REST API
try:
    res = requests.post('http://127.0.0.1:5000/users/' + str(test_user_id), json={"user_name": test_user_name})
    if res.ok:
        print(f"POST user_id[{test_user_id}] {res.json()}")
except (ConnectionError, ConnectionError, MaxRetryError) as e:
    print(f"Exception - ensure rest_app.py is running [{e}]")
    raise Exception("Backend Testing failed")

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

# 3 - Check data in the database
try:
    print(f'Opening DB Connection')
    db_connection = pymysql.connect(host=globals.DB_HOST, port=globals.DB_PORT, user=globals.DB_USER,
                                    passwd=globals.DB_PASSWORD, db=globals.DB_SCHEMA_NAME)
    db_connection.autocommit(True)
    # Getting a cursor from Database
    db_cursor = db_connection.cursor()
    print(f'Getting user_name from user_id [{test_user_id}]')
    row_count = db_cursor.execute(f"Select user_name from {globals.DB_SCHEMA_NAME}.users where user_id = {test_user_id}")
    print(f'row_count is [{row_count}]')
    if row_count != 1:
        print(f'Select - Error row_count !=1 [{row_count}]')
        raise Exception("Test Failed")
    else:
        record = db_cursor.fetchone()
        user_name_read = record[0]
        if user_name_read == test_user_name:
            print(f"USER NAME CORRECT WRITTEN TO DB [{test_user_name}] [{user_name_read}]")
        else:
            print(f"USER NAMES DIFFERENT DB = [{user_name_read}] SENT to REST API = [{test_user_name}]")
            raise Exception("Test Failed")

except pymysql.Error as e:
    print(e)

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
    driver.get("http://127.0.0.1:5001/users/get_user_data/"+str(test_user_id))
except WebDriverException as e:
    print(f"WebDriverException - ensure web_app.py is running [{e}]")
    raise Exception("test failed")

try:
    web_get_user_name = driver.find_element(By.ID, value="user").text
    print(f"user_name is [{web_get_user_name}] for user_id [{test_user_id}]")
    # 6 Check the user_name is correct.
    if web_get_user_name == test_user_name:
        print(f"SUCCESS Web Interface returned correct user_name for [{test_user_id}] [{test_user_name}] [{web_get_user_name}]")
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
# TODO could better control db_cursor to check it was setup correctly before running
try:
    print(f'Cleaning up TEST data - Deleting user_id [{test_user_id}]')
    row_count = db_cursor.execute(
        f"Delete from {globals.DB_SCHEMA_NAME}.users where user_id = {test_user_id}")
    # row_count shows the number of rows effected.
    print(f'row_count is [{row_count}]')
    if row_count != 1:
        print(f"Error when deleting user_id[{test_user_id}]")
    else:
        print(f"Cleaned up - Deleted user_id [{test_user_id}]")

    db_cursor.close()
    db_connection.close()
    print(f"Database connection closed")
except pymysql.Error as e:
    print(e)
    print(f"SQL Error when deleting user_id[{test_user_id}]")
