from datetime import datetime

import pymysql

# pymuysql reference - https://pymysql.readthedocs.io/en/latest/modules/index.html
# Uses freesqldatabase.com for the MySQL Server
# username and password hardcoded here - should be made secure.

SCHEMA_NAME = "sql8640267"
STRING_FORMAT_TIME = '%Y-%m-%d %H:%M:%S'

_connection = None
_cursor = None

# TODO - should really store the password securely
def get_connection():
    global _connection
    global _cursor
    if not _connection:
        _connection = pymysql.connect(host='sql8.freesqldatabase.com', port=3306, user='sql8640267',
                                      passwd='FkJQptHWtm', db=SCHEMA_NAME)
        _connection.autocommit(True)
        # Getting a cursor from Database
        _cursor = _connection.cursor()
    return _connection


def init():
    # check if table exists - if not create it
    try:
        check_table_exists = "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME LIKE 'users'"
        row_count = _cursor.execute(check_table_exists)
        print(f'row_count is [{row_count}]')
        if row_count != 1:
            # create table if it doesn't exist
            print(f'Creating Table')
            create_table = "CREATE TABLE `" + SCHEMA_NAME + ("`.`users`(`user_id` INT NOT NULL,`user_name` VARCHAR(50) "
                                                             "NOT NULL, creation_date VARCHAR(50) NOT NULL, "
                                                             "PRIMARY KEY (`user_id`));")
            _cursor.execute(create_table)
            return True
        else:
            print(f'Table exists')
            return False

    except pymysql.Error as e:
        print(e)
        return False


def close_connection():
    if _cursor is not None:
        _cursor.close()
    if _connection is not None:
        _connection.close()


def add_user(user_id, user_name):
    print(f'in add_user [{user_id}][{user_name}]')
    #  get current date time
    now = datetime.now()
    time_stamp = now.strftime(STRING_FORMAT_TIME)
    print(f"Current Time [{time_stamp}]")

    # Inserting data into table
    try:
        _cursor.execute(
            f"INSERT into {SCHEMA_NAME}.users (user_id, user_name, creation_date) VALUES ({user_id}, '{user_name}', '{time_stamp}')")
        return True
    except pymysql.Error as e:
        print(e)
        return False


def read_user(user_id):
    # Reading user_name from table
    print(f'in read_user [{user_id}]')
    try:
        row_count = _cursor.execute(f"Select user_name from {SCHEMA_NAME}.users where user_id = {user_id}")
        print(f'row_count is [{row_count}]')
        if row_count != 1:
            return ""
        else:
            record = _cursor.fetchone()
            user_name = record[0]
            print(f'user_name is [{user_name}]')
            return user_name
    except pymysql.Error as e:
        print(e)
        return ""


# TODO
#  - if update doesn't change the name
#  - it returns error
#  - possibly should have another return error case - user_name not different
#  - but this wasn't in specification
def update_user(user_id, user_name):
    # Updating user_name in table
    print(f'in update_user [{user_id}][{user_name}]')
    try:
        row_count = _cursor.execute(
            f"Update {SCHEMA_NAME}.users set user_name = '{user_name}'  where user_id = {user_id}")
        # row_count shows the number of rows effected.
        print(f'row_count is [{row_count}]')
        if row_count != 1:
            return False
        else:
            return True
    except pymysql.Error as e:
        print(e)
        return False


def delete_user(user_id):
    # Deleting user_id in table
    print(f'in update_user [{user_id}]')
    try:
        row_count = _cursor.execute(
            f"Delete from {SCHEMA_NAME}.users where user_id = {user_id}")
        # row_count shows the number of rows effected.
        print(f'row_count is [{row_count}]')
        if row_count != 1:
            return False
        else:
            return True
    except pymysql.Error as e:
        print(e)
        return False
