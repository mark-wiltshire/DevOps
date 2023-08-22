"""
REST API and Database testing

res_app.py must be running

Hardcoded test data
Hardcoded username and password for the database

"""

import pymysql
import requests
from urllib3.exceptions import MaxRetryError, NewConnectionError
import globals

globals.init()

#Set test_user_name from the Globals - taken from config DB
test_user_name = str(globals.global_dict[globals.KEY_TEST_USER_NAME])
#strip off quotes and brackets
test_user_name = test_user_name[2:-2]
print(f"---from Config DB Table--- test_user_name = [{test_user_name}]")

#Set test_user_id from the Globals - taken from the config DB
test_user_id = str(globals.global_dict[globals.KEY_TEST_USER_ID])
#strip off quotes and brackets
test_user_id = test_user_id[2:-2]
print(f"---from Config DB Table--- test_user_id = [{test_user_id}]")


print(f"---Test 1--- POST")
# 1 - POST new user data (USER_ID hardcoded)
try:
    res = requests.post('http://127.0.0.1:5000/users/'+test_user_id, json={"user_name": test_user_name})
    if res.ok:
        json_response = res.json()
        print(f"SUCCESS POST user_id[{test_user_id}] {json_response}")
        # Check if res.json has user_added_with_new_id - i.e. user_id was changed
        if "user_added_with_new_id" in json_response:
            # if we get this ID for future tests this cycle.
            post_user_id = json_response["user_added_with_new_id"]
            #set following test to use this NEW user_id
            print(f"test_user_id changed to [{post_user_id}] from [{test_user_id}]")
            test_user_id = str(post_user_id)
    else:
        print(f"ERROR Result NOT OK {res.json()}")
        raise Exception("Backend Testing failed")
#For some reason this doesn't work - have to use OSError
#except (ConnectionRefusedError, NewConnectionError, MaxRetryError, ConnectionError) as e:
except (OSError) as e:
    print("***********************************************")
    print(f"Exception - ensure rest_app.py is running [{e}]")
    print("***********************************************")
    raise Exception("Backend Testing failed")

print(f"---Test 2--- GET")
# 2 - Use GET to check status code 200 and data equals what was posted in 1
#If we got here server is up
res = requests.get('http://127.0.0.1:5000/users/'+test_user_id)
if res.ok:
    json_response = res.json()
    read_user_name = json_response["user_name"]
    print(f"GET user_id[{test_user_name}] {json_response}")
    if read_user_name==test_user_name:
        print(f"SUCCESS user_name checked [{test_user_name}] [{read_user_name}]")
    else:
        print(f"ERROR user_names different !!! [{test_user_name}] [{read_user_name}]")
        raise Exception("Backend Testing failed")
else:
    print(f"ERROR Result NOT OK {res.json()}")
    raise Exception("Backend Testing failed")

print(f"---Test 3--- Check DB")
# 3 - Check data in the database
try:
    print(f'Opening NEW DB Connection')
    db_connection = pymysql.connect(host='sql8.freesqldatabase.com', port=3306, user='sql8640267',
                                        passwd='FkJQptHWtm', db=globals.DB_SCHEMA_NAME)
    db_connection.autocommit(True)
    # Getting a cursor from Database
    db_cursor = db_connection.cursor()
    print(f'Getting user_name from user_id [{test_user_id}]')
    row_count = db_cursor.execute(f"Select user_name from {globals.DB_SCHEMA_NAME}.users where user_id = {test_user_id}")
    print(f'Results found for [{test_user_id}] is [{row_count}]')
    #we should expect 1 row
    if row_count != 1:
        print(f'Select - Error row_count !=1 [{row_count}]')
        raise Exception("Backend Testing failed")
    else:
        record = db_cursor.fetchone()
        user_name_read = record[0]
        if user_name_read == test_user_name:
            print(f"USER NAME CORRECT WRITTEN TO DB [{test_user_name}] [{user_name_read}]")
        else:
            print(f"USER NAMES DIFFERENT DB = [{user_name_read}] SENT to REST API = [{test_user_name}]")
            raise Exception("Backend Testing failed")
except pymysql.Error as e:
    print(e)
    print(f"SQL Error when checking user in DB user_id[{test_user_id}]")
    raise Exception("Backend Testing failed")

# EXTRA - run a delete to clean up after testing
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

