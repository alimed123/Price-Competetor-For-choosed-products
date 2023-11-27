

# Connect database

import pymysql
from dotenv import load_dotenv
import os
import os.path
import logging
import sys

logging.basicConfig(
  encoding='utf-8', 
  level=logging.DEBUG, 
  format='%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] - [%(threadName)s] - %(message)s', 
  datefmt='%m/%d/%Y %I:%M:%S %p',
  handlers=[
    logging.FileHandler('runtimelogs.log'),
    logging.StreamHandler(sys.stdout)
  ]
)

load_dotenv()


def db_connect():

    #connect to data base
    db_connection = pymysql.connect(
        host='127.0.0.1',
        user="spyder",
        password="password1011",
        db="product_spyder"
    )
   
    return db_connection



def is_connected(connection):

    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        return True
    except pymysql.Error:
        return False
