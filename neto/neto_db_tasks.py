import mysql.connector
from helpers.db_connect import db_connect
import logging

def get_sku_price(sku, db_connection):

  try:
    # Check DB connection and established connection if not connected
    if db_connection.is_connected():
      pass
    else:
      db_connection = db_connect()

    get_sku_price = 'SELECT parent_sku, sku, price_beat_by_result, do_update_price FROM user_price_action WHERE sku= %s'

    value = (sku, )

    mycursor = db_connection.cursor()

    mycursor.execute(get_sku_price, value)
    row = mycursor.fetchall()

    return row[0]

  except mysql.connector.Error as error:
    logging.error("Failed to retrieve record into user_price_action table {}".format(error))