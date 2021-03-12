import configparser
from contextlib import contextmanager
import os

import mysql.connector

from . import config

@contextmanager
def ctx_db_cursor():
    connection = mysql.connector.connect(**config.get_db_config())
    cursor = connection.cursor()
    try:
        yield cursor
    except:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        cursor.close()
        connection.close()

@contextmanager
def ctx_db_dict_cursor():
    connection = mysql.connector.connect(**config.get_db_config())
    cursor = connection.cursor(dictionary=True)
    try:
        yield cursor
    except:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        cursor.close()
        connection.close()
        
