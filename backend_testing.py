# REST API and Database testing
import requests

import db_connector

# initialise DB Connection
db_connector.get_connection()
print("DB Connection Opened")

db_connector.init()
print("DB initialised")

#Set our user_name so we can test it later.
USER_NAME = "mark"

# 1 - POST new user data (USER_ID hardcoded)
res = requests.post('http://127.0.0.1:5000/users/22', json={"user_name":USER_NAME})
if res.ok:
    print(f"POST {res.json()}")

# 2 - Use GET to check status code 200 and data equals what was posted in 1
res = requests.get('http://127.0.0.1:5000/users/22')
if res.ok:
    print(f"POST {res.json()}")

# 3 - Check data in the database
# option 1 - using stored procedure - could also use new connector and SQL
user_name_read = db_connector.read_user(22)
if user_name_read == USER_NAME:
    print(f"USER NAME CORRECT WRITTEN TO DB")
else:
    print(f"USER NAMES DIFFERENT DB = [{user_name_read}] SENT to REST API = [{USER_NAME}]")

# EXTRA - run a delete to clean up after testing
# therefore can run again.
res = db_connector.delete_user(22)
print(f"Cleaned up - Deleted user_id 22 [{res}]")
