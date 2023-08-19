"""
Global store of parameters

Makes it easier to use parameters in multiple locations
initialised in db_connector.init()

Will open its own DB connection and set globals then close DB connection

#TODO - currently init in db_connector will create tables if they don't exist - this should be removed
You have to run db_connector - get_connection() then init() to re-initialise database
"""
from collections import defaultdict

import pymysql
import pymysql.cursors

# STATIC DB KEY VALUES
KEY_API_GATEWAY = "API_Gateway"
KEY_TEST_BROWSER = "test_browser"
KEY_TEST_USER_NAME = "user_name"

# STATIC VALUES
DB_HOST = "sql8.freesqldatabase.com"
DB_USER = "sql8640267"
DB_PORT = 3306
DB_PASSWORD = "FkJQptHWtm"
DB_SCHEMA_NAME = "sql8640267"

STRING_FORMAT_TIME = '%Y-%m-%d %H:%M:%S'

# global dictionary
global_dict = defaultdict()
initialised = False


def init():
    """
    init()
    Initialised the global variables read from the config database on startup

    :return:
    TODO add error handling when config table not there.
    """
    global initialised

    if not initialised:
        # Open DB connection using dictionary
        connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER,
                                 passwd=DB_PASSWORD, db=DB_SCHEMA_NAME)
        cursor = connection.cursor()
        # setup globals from reading data from config
        # COULD READ THIS USING A DICTIONARY CURSOR
        row_count = cursor.execute(f"Select * from {DB_SCHEMA_NAME}.config")
        print(f'CONFIG row_count is [{row_count}]')
        if row_count == 0:
            return False
        else:
            data = cursor.fetchall()
            for row in data:
                #print(f"Adding to global_dict [{row[0]}][{row[1]}]")
                global_dict[row[0]]=[row[1]]
            initialised = True
        print(f"Initialised Globals from DB")
        return initialised
