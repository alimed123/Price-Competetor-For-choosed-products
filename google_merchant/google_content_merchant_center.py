# google_content_merchant_center.py
import os
import mysql.connector
from helpers.db_connect import db_connect
import logging

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_products_to_update(sku, db_connection):
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

def google_update_products(products_to_update, db_connection):

  directory = os.path.dirname(os.path.realpath(__file__))
  credentials = Credentials.from_authorized_user_file(f'{directory}/service-account.json')
  service = build('content', 'v2.1', credentials=credentials)

  for product_item_sku in products_to_update:

    #Todo get the sku, updated price beat by from DB
    sku_price = get_products_to_update(product_item_sku, db_connection) # USE THIS LINE TO GET THE ACTUAL PRICE ACTION DATA FROM THE DATABASE
    parent_sku, sku, price, do_update_price = sku_price

    if do_update_price == 'yes': # Check if price_beat_by_result > minimum_sale_price

      # Use the product data to make API requests to update products
      # Example: Update price for a product
      # request = service.products().update(
      #     merchantId=113145660,
      #     productId=sku,
      #     body={'price': price}
      # )
      # response = request.execute()
      print('Product updated:', sku)