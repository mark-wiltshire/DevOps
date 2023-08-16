import pymysql
from datetime import datetime

# Uses freesqldatabase.com for the MySQL Server
# username and password hardcoded here - should be made secure.

SCHEMA_NAME = "sql8640267"
STRING_FORMAT_TIME = '%Y-%m-%d %H:%M:%S'


_connection = None
_cursor = None


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
    global _cursor
    # TODO
    # check if table exists - if not create

    # create table if it doesn't exist
    statementToExecute = "CREATE TABLE `" + SCHEMA_NAME + "`.`users`(`user_id` INT NOT NULL,`user_name` VARCHAR(50) NOT NULL, creation_date VARCHAR(50) NOT NULL, PRIMARY KEY (`user_id`));"
    _cursor.execute(statementToExecute)


def close_connection():
    global _connection
    global _cursor
    if _cursor is not None:
        _cursor.close()
    if _connection is not None:
        _connection.close()


def add_user(user_id, user_name):
    global _cursor

    #  get current date time
    now = datetime.now()
    time_stamp = now.strftime(STRING_FORMAT_TIME)
    #print(f"Current Time [{time_stamp}]")

    # Inserting data into table
    try:
        _cursor.execute(f"INSERT into {SCHEMA_NAME}.users (user_id, user_name, creation_date) VALUES ({user_id}, '{user_name}', '{time_stamp}')")
        return True
    except (pymysql.Error) as e:
        print(e)
        return False


def read_user(user_id):
    # Reading user_name from table
    print(f'in read_user [{user_id}]')
    try:
        row_count = _cursor.execute(f"Select user_name from {SCHEMA_NAME}.users where user_id = {user_id}")
        print(f'row_count is [{row_count}]')
        if (row_count != 1):
            return ""
        else:
            record = _cursor.fetchone()
            user_name = record[0]
            print(f'user_name is [{user_name}]')
            return user_name
    except (pymysql.Error) as e:
        print(e)
        return ""

def update_user():
    pass


def delete_user():
    pass

#used for initial testing
#get_connection()
#init()
#add_user(1,"testing")
#read_user(1)
#close_connection()