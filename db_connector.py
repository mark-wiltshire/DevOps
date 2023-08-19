"""
db_connector.py

This handles the Database connection to freesqldatabase.com
Username and password are currently hardcoded in the code.

Used by rest_app.py and web_app.py

Methods
- get_connection() - will initialise connection and cursor to the Database
- init() - will create the DB table if they do not exist
- close_connection() - will close connection and cursor to the Database
- add_user() - will add user to DB
- read_user() - will read user from DB
- update_user() - will update user in DB
- delete_user() - will delete user

"""
from datetime import datetime

import pymysql

import globals

# check globals initialised
globals.init()

# pymuysql reference - https://pymysql.readthedocs.io/en/latest/modules/index.html
# Uses freesqldatabase.com for the MySQL Server
# username and password hardcoded here - should be made secure.

_connection = None
_cursor = None


# TODO - should really store the password securely
def get_connection():
    """
    Will create or return a connection to the Database
    user and password currently hardcoded.

    :return: pymysql.connections.Connection
    """
    global _connection
    global _cursor
    if not _connection:
        _connection = pymysql.connect(host=globals.DB_HOST, port=globals.DB_PORT, user=globals.DB_USER,
                                      passwd=globals.DB_PASSWORD, db=globals.DB_SCHEMA_NAME)
        _connection.autocommit(True)
        # Getting a cursor from Database
        # for prepared statements (using mysql)
        #   - https://pynative.com/python-mysql-execute-parameterized-query-using-prepared-statement/
        # use line below.
        # _cursor = _connection.cursor(prepared=True)
        _cursor = _connection.cursor()
    return _connection


def init():
    """
    initialises the database - by creating the table users AND config - if they don't exist

    Also calls globals.init() to initialise globals from config DB

    :return: False - on error or table exists - True - when table created
    """
    created_user_table = False
    created_config_table = False
    try:
        # check if users table exists - if not create it
        check_table_exists = "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME LIKE 'users'"
        row_count = _cursor.execute(check_table_exists)
        print(f'User Table Check [{row_count}]')
        if row_count != 1:
            # create table if it doesn't exist
            print(f'Creating USERS Table')
            create_table = "CREATE TABLE `" + globals.DB_SCHEMA_NAME + (
                "`.`users`(`user_id` INT NOT NULL,`user_name` VARCHAR(50) "
                "NOT NULL, creation_date DATETIME NOT NULL, "
                "PRIMARY KEY (`user_id`));")
            _cursor.execute(create_table)
            created_user_table = True
        else:
            print(f'USER Table exists')

        # check if config table exists - if not create it
        check_table_exists = "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME LIKE 'config'"
        row_count = _cursor.execute(check_table_exists)
        print(f'Config table check [{row_count}]')
        if row_count != 1:
            # create table if it doesn't exist
            print(f'Creating CONFIG Table')
            create_table = "CREATE TABLE `" + globals.DB_SCHEMA_NAME + (
                "`.`config`(`key` VARCHAR(50) NOT NULL,`value` VARCHAR(50) NOT NULL, PRIMARY KEY (`key`));")
            _cursor.execute(create_table)
            created_config_table = True

            print(f'Inserting CONFIG Table')
            prepared_config_sql = """INSERT into """ + globals.DB_SCHEMA_NAME + """.config (`key`, `value`) VALUES (%s, %s)"""
            _cursor.execute(prepared_config_sql, (globals.KEY_API_GATEWAY, '127.0.0.1:5000/users'))
            _cursor.execute(prepared_config_sql, (globals.KEY_TEST_BROWSER, 'chrome'))
            _cursor.execute(prepared_config_sql, (globals.KEY_TEST_USER_NAME, 'Bob'))
            print(f'Completed CONFIG Table')
        else:
            print(f'CONFIG Table exists')

    except pymysql.Error as e:
        print(e)
        return False

    # calculate return
    if created_config_table or created_user_table:
        return True
    else:
        return False


def close_connection():
    """
    used to close the database cursor and connection when needed
    From the rest_app.py and web_app.py modules

    :return: none
    """
    if _cursor is not None:
        _cursor.close()
    if _connection is not None:
        _connection.close()


def add_user(user_id, user_name):
    """
    Adds the user to the database with a creation_date

    Updated to use prepared statement

    :param user_id: - the unique user_id
    :param user_name: - the text user_name
    :return: True - user added - False - Error occured
    """
    print(f'in add_user [{user_id}][{user_name}]')
    #  get current date time
    now = datetime.now()
    time_stamp = now.strftime(globals.STRING_FORMAT_TIME)
    print(f"Current Time [{time_stamp}]")

    # Inserting data into table
    try:
        insert_query = """INSERT into """ + globals.DB_SCHEMA_NAME + """.users (user_id, user_name, creation_date) VALUES (%s, %s, %s)"""
        print(f"Insert Query [{insert_query}]")
        tuple_data = (user_id, user_name, time_stamp)
        for a in tuple_data:
            print(f"In Tuple [{a}]")
        _cursor.execute(insert_query, tuple_data)
        return True
    except pymysql.Error as e:
        print(e)
        return False


def read_user(user_id):
    """
    Reads the user_name for the user_id passed in the database

    :param user_id:
    :return: "" - blank string on error or no user found
            "<user_name>" - from the Databse when user_id found.
    """
    # Reading user_name from table
    print(f'in read_user [{user_id}]')
    try:
        row_count = _cursor.execute(f"Select user_name from {globals.DB_SCHEMA_NAME}.users where user_id = {user_id}")
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


def update_user(user_id, user_name):
    """
    Update the current user_name for the passed user_id

    :param user_id: user_id to update
    :param user_name: NEW user_name to store in the database
    :return: False - on error - True - if update works
    """
    # Updating user_name in table
    print(f'in update_user [{user_id}][{user_name}]')
    try:
        row_count = _cursor.execute(
            f"Update {globals.DB_SCHEMA_NAME}.users set user_name = '{user_name}'  where user_id = {user_id}")
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
    """
    Delete the user from the database
    :param user_id: - id of user to delete
    :return: False - on error - True if delete works
    """
    # Deleting user_id in table
    print(f'in update_user [{user_id}]')
    try:
        row_count = _cursor.execute(
            f"Delete from {globals.DB_SCHEMA_NAME}.users where user_id = {user_id}")
        # row_count shows the number of rows effected.
        print(f'row_count is [{row_count}]')
        if row_count != 1:
            return False
        else:
            return True
    except pymysql.Error as e:
        print(e)
        return False
