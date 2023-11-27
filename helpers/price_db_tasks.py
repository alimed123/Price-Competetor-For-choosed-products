import mysql.connector
from helpers.db_connect import db_connect,is_connected
import datetime
import json
import logging

# Update prices on competitor_pages
def update_product_price(product_url, price, db_connection):
  
  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    update_price_query = f'UPDATE competitor_pages SET price={price} WHERE page_url="{product_url}"'

    mycursor = db_connection.cursor()

    mycursor.execute(update_price_query)

    db_connection.commit()
    logging.info("%s Price record updated successfully into competitor_pages table.", mycursor.rowcount)
    mycursor.close()

  except mysql.connector.Error as error:
    logging.info("Failed to update record into competitor_pages table {}".format(error))

def get_old_price(urls, db_connection):

  product_list = []

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    for url in urls:
      # If you wanted to test URL check, just change the query variable appropriately
      # Example if you just want to test all urls under example.com, you can use '%example.com%'
      get_all_product = f'SELECT page_url FROM competitor_pages WHERE page_url="{url}"'

      mycursor = db_connection.cursor()
      mycursor.execute(get_all_product)
      pages = mycursor.fetchall()

      for page in pages:
        product_list.append(page[0])

    return product_list
  
  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from competitor_pages table {}\n".format(error))

# Update product_prices table if new
def save_product_prices(prices_json_data, page_id_primary_key, db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    insert_product_price_query = f"INSERT INTO competitor_product_prices(prices, page_id) VALUES ('{prices_json_data}', '{page_id_primary_key}' )"

    mycursor = db_connection.cursor()

    mycursor.execute(insert_product_price_query)

    db_connection.commit()
    logging.info("%s Record saved successfully into competitor_product_prices table.", mycursor.rowcount)
    mycursor.close()

  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from competitor_product_prices table {}\n".format(error))


# Update product_prices table
def update_product_prices(prices_json_data, page_id_primary_key, db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    update_product_price_query = f"UPDATE competitor_product_prices SET prices='{prices_json_data}' WHERE page_id='{page_id_primary_key}'"

    mycursor = db_connection.cursor()

    mycursor.execute(update_product_price_query)

    db_connection.commit()
    logging.info("%s Record updated successfully into competitor_product_prices table", mycursor.rowcount)
    mycursor.close()

  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from competitor_product_prices table {}\n".format(error))

# Display price JSON data from DB
def fetch_product_prices(db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    select_product_price_query = f"SELECT page_id, prices FROM competitor_product_prices";

    mycursor = db_connection.cursor()

    mycursor.execute(select_product_price_query)
    row = mycursor.fetchall()

    return row

  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from competitor_product_prices table {}\n".format(error))

# Get the page_id primary key from main table (competitor_pages)
def get_primary_key(url, db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    get_primary_key = f'SELECT page_id FROM competitor_pages WHERE page_url="{url}"';

    mycursor = db_connection.cursor()

    mycursor.execute(get_primary_key)
    rows = mycursor.fetchall()
    
    for row in rows:
      id = row[0]

    return id

  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from competitor_pages table {}\n".format(error))


# Get the page_id primary key from main table (competitor_pages)
def check_key_exist(id, db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    key_exist = f"SELECT * FROM competitor_product_prices WHERE page_id={id}";

    mycursor = db_connection.cursor()

    mycursor.execute(key_exist)
    rows = mycursor.fetchall()
    
    id = 0

    for row in rows:
      id = row[0]

    logging.info(f'id - %s', id)

    if (id):
      return True
    else:
      return False

  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from competitor_product_prices table {}\n".format(error))

# Get the page_id primary key from main table (competitor_pages)
def price_history(id, db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    key_exist = 'SELECT * FROM competitor_product_prices WHERE page_id = %s';

    value = (id, )

    mycursor = db_connection.cursor()

    mycursor.execute(key_exist, value)
    rows = mycursor.fetchall()
    
    id = 0

    for row in rows:
      id = row[0]

    if (id):
      return row[1]
    else:
      return json.dumps({})

  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from competitor_product_prices table {}\n".format(error))