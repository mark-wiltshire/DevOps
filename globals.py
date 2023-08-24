"""
Global store of parameters

Stores any Hardcoded values

Uses db_connector.init_config() to populate global_dict of all config parameters stores in the database
"""
from collections import defaultdict

import db_connector

# STATIC DB KEY VALUES
KEY_API_GATEWAY = "API_Gateway"
KEY_TEST_BROWSER = "test_browser"
KEY_TEST_USER_NAME = "test_user_name"
KEY_TEST_USER_ID = "test_user_id"

STRING_FORMAT_TIME = '%Y-%m-%d %H:%M:%S'

# global dictionary of all config parameters
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
        global global_dict
        global_dict = db_connector.init_config()
        initialised = True
        print(f"Initialised Globals from DB")
        return initialised
