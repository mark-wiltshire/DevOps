# REST API and Database testing
# res_app.py must be running
import pymysql
import requests
from urllib3.exceptions import MaxRetryError

SCHEMA_NAME = "sql8640267"
# Set our Test Data - user_id and user_name so we can test it later.
TEST_USER_NAME = "mark"
TEST_USER_ID = "22"

# 1 - POST new user data (USER_ID hardcoded)
try:
    res = requests.post('http://127.0.0.1:5000/users/'+TEST_USER_ID, json={"user_name": TEST_USER_NAME})
    if res.ok:
        print(f"POST user_id[{TEST_USER_NAME}] {res.json()}")
except (ConnectionError, ConnectionError, MaxRetryError) as e:
    print(f"Exception - ensure rest_app.py is running [{e}]")
    raise Exception("Backend Testing failed")

# 2 - Use GET to check status code 200 and data equals what was posted in 1
res = requests.get('http://127.0.0.1:5000/users/'+TEST_USER_ID)
if res.ok:
    json_response = res.json()
    read_user_name = json_response["user_name"]
    print(f"GET user_id[{TEST_USER_NAME}] {json_response}")
    if read_user_name==TEST_USER_NAME:
        print(f"SUCCESS user_name checked [{TEST_USER_NAME}] [{read_user_name}]")
    else:
        print(f"ERROR user_names different !!! [{TEST_USER_NAME}] [{read_user_name}]")

# 3 - Check data in the database
try:
    print(f'Opening DB Connection')
    db_connection = pymysql.connect(host='sql8.freesqldatabase.com', port=3306, user='sql8640267',
                                        passwd='FkJQptHWtm', db=SCHEMA_NAME)
    db_connection.autocommit(True)
    # Getting a cursor from Database
    db_cursor = db_connection.cursor()
    print(f'Getting user_name from user_id [{TEST_USER_ID}]')
    row_count = db_cursor.execute(f"Select user_name from {SCHEMA_NAME}.users where user_id = {TEST_USER_ID}")
    print(f'row_count is [{row_count}]')
    if row_count != 1:
        print(f'Error row_count !=1 [{row_count}]')
    else:
        record = db_cursor.fetchone()
        user_name_read = record[0]
        if user_name_read == TEST_USER_NAME:
            print(f"USER NAME CORRECT WRITTEN TO DB [{TEST_USER_NAME}] [{user_name_read}]")
        else:
            print(f"USER NAMES DIFFERENT DB = [{user_name_read}] SENT to REST API = [{TEST_USER_NAME}]")

except pymysql.Error as e:
    print(e)

# EXTRA - run a delete to clean up after testing
# therefore we can run test again and again
# TODO could better control db_cursor to check it was setup correctly before running
try:
    print(f'Cleaning up TEST data - Deleting user_id [{TEST_USER_ID}]')
    row_count = db_cursor.execute(
        f"Delete from {SCHEMA_NAME}.users where user_id = {TEST_USER_ID}")
    # row_count shows the number of rows effected.
    print(f'row_count is [{row_count}]')
    if row_count != 1:
        print(f"Error when deleting user_id[{TEST_USER_ID}]")
    else:
        print(f"Cleaned up - Deleted user_id [{TEST_USER_ID}]")
except pymysql.Error as e:
    print(e)
    print(f"SQL Error when deleting user_id[{TEST_USER_ID}]")

