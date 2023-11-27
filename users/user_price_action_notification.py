import mysql.connector
from helpers.db_connect import db_connect,is_connected
import datetime
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import logging

# Load helpers
from helpers.main_email import send_html_email

load_dotenv()

# Use this to change between "DEV" and "PROD" .env variables
ENV = os.getenv("PROD")

# Function to apply style based on "Price Action" value
def highlight_price_action(val):
  if val == "▼ Lower than Min Sale Price":
    return "color: red; font-weight: bold"
  return ""

def price_action_notify_user(current_sku_list, db_connection, matched_code = [], did_not_matched = [], consolidated_report_filename = ''):

  directory = os.path.dirname(os.path.realpath(__file__))
  parent_dir = os.path.abspath(os.path.join(directory, os.pardir))

  additional_info = ''

  product_url_list = []
  product_sku_list = []
  minimum_sale_price_list = []
  lowest_price_list = []
  price_beat_by_result_list = []
  timestamp_list = []
  price_action_list_email = []
  price_action_list_csv = []

  for sku in current_sku_list:

    try:

      logging.info('Fetching price action data for %s', sku)

      # Check DB connection and established connection if not connected
      if is_connected(db_connection):
        pass
      else:
        db_connection = db_connect()

      save_url_query = 'SELECT product_url, sku, minimum_sale_price, lowest_price, price_beat_by_result, timestamp FROM user_price_action WHERE sku = %s'

      values = (sku,)

      mycursor = db_connection.cursor()
      mycursor.execute(save_url_query, values)
      rows = mycursor.fetchall()

      for row in rows:
        product_url, sku, minimum_sale_price, lowest_price, price_beat_by_result, timestamp = row

        # Determine of price_beat_by_result is higher/lower than the minimum_sale_price
        if (price_beat_by_result > minimum_sale_price):
          price_action_list_email.append('<span style="color:green;">▲</span> Higher than Min Sale Price')
          price_action_list_csv.append('Higher than Min Sale Price')
        else:
          price_action_list_email.append('<span style="color:red;">▼</span> Lower than Min Sale Price')
          price_action_list_csv.append('Lower than Min Sale Price')
                        
        product_url_list.append(product_url)
        product_sku_list.append(sku)
        minimum_sale_price_list.append(minimum_sale_price)
        lowest_price_list.append(lowest_price)
        price_beat_by_result_list.append(price_beat_by_result)
        timestamp_list.append(timestamp)

    except mysql.connector.Error as error:
      logging.info("Failed to retrieve record into user_price_action table {}".format(error))

  now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  if (product_url_list):
    logging.info('Saving a CSV file.')
    logging.info('sku: %s, product_url: %s, minimum_sale_price_list: %s, lowest_price_list: %s, price_beat_by_result_list: %s, price_action_list: %s, timestamp_list: %s', len(product_sku_list), len(product_url_list), len(minimum_sale_price_list), len(lowest_price_list), len(price_beat_by_result_list), len(price_action_list_email), len(timestamp_list))
    data = {"SKU": product_sku_list, "Product Url": product_url_list, "Minimum Sale Price": minimum_sale_price_list, "Lowest Price": lowest_price_list, "Price Beat By": price_beat_by_result_list, "Price Action": price_action_list_email, "Timestamp": timestamp_list}
    datacsv = {"SKU": product_sku_list, "Product Url": product_url_list, "Minimum Sale Price": minimum_sale_price_list, "Lowest Price": lowest_price_list, "Price Beat By": price_beat_by_result_list, "Price Action": price_action_list_csv, "Timestamp": timestamp_list}
    # df = pd.DataFrame.from_dict(data, orient='index')
    df = pd.DataFrame(data)
    dfcsv = pd.DataFrame(datacsv)

    # Drop empty Urls
    df['Product Url'].replace('', np.nan, inplace=True)
    df.dropna(subset=['Product Url'], inplace=True)
    dfcsv['Product Url'].replace('', np.nan, inplace=True)
    dfcsv.dropna(subset=['Product Url'], inplace=True)

    # Remove duplicates
    df.drop_duplicates('Product Url', keep='first', inplace=True)
    dfcsv.drop_duplicates('Product Url', keep='first', inplace=True)
    # df = df.transpose()

    filename = f"price_action{ now }.csv"

    logging.info('%s saved sucessfully.', filename)

    file_path = os.path.join(directory,'price_action/', filename)
    
    dfcsv.to_csv(file_path, index=False)

    # Generate an HTML version of the DF
    # a = pd.read_csv(file_path)
    df_to_html = df.to_html(escape=False, index=False)

    # to save as html file named as "Table"
    # a.to_html("Table.htm")

    # assign it to a variable (string)
    msg_head = "<html><head><style> table {border-collapse: collapse; width: 100%;} th, td {text-align: left; padding: 10px; border: 1px solid #ddd;} tr:nth-child(even){background-color: #f2f2f2} th {background-color: #31b821; color: white;} a {background-color: transparent; text-decoration: none;}</style></head><body><p>"
    msg_end = "</p></body></html>"

    # PREPARE ADDITIONAL INFO IF EXIST
    if matched_code:
      additional_info = f"""
        <p>
          Additional Information:<br>
          Competitor Matched:{len(matched_code)}<br>
          Did not Matched:{len(did_not_matched)}<br>
          Attached file for additional references.<br>
        </p>
      """

    # PREPARE ATTACHMENT IF THEY EXIST
    if consolidated_report_filename:
      files = [os.path.join(parent_dir, consolidated_report_filename)]
      logging.info('Filepaths: %s', files)

    if additional_info:
      html_file = msg_head + df_to_html + additional_info + msg_end
    else:
      html_file = msg_head + df_to_html + msg_end

    # Send the generated file to the customer
    send_html_email(os.getenv(f"{ENV}EMAIL"), f'Price Action Notification - {now}', html_file, files)
  else:
    logging.info('No price_action.csv output file generated.')

def price_action_generate_summary(current_sku_list, db_connection):

  directory = os.path.dirname(os.path.realpath(__file__))
  parent_dir = os.path.abspath(os.path.join(directory, os.pardir))

  product_url_list = []
  product_sku_list = []
  product_current_price_list = []
  minimum_sale_price_list = []
  lowest_price_list = []
  average_price_list = []
  highest_price_list = []
  price_beat_by_result_list = []
  timestamp_list = []

  for sku in current_sku_list:

    try:

      logging.info('Fetching price action data for %s', sku)

      # Check DB connection and established connection if not connected
      if is_connected(db_connection):
        pass
      else:
        db_connection = db_connect()

      save_url_query = 'SELECT product_url, sku, current_price, minimum_sale_price, lowest_price, average_price, highest_price, price_beat_by_result, timestamp FROM user_price_action WHERE sku = %s'

      values = (sku,)

      mycursor = db_connection.cursor()
      mycursor.execute(save_url_query, values)
      rows = mycursor.fetchall()

      for row in rows:
        product_url, sku, current_price, minimum_sale_price, lowest_price, average_price, highest_price, price_beat_by_result, timestamp = row
                        
        product_url_list.append(product_url)
        product_sku_list.append(sku)
        product_current_price_list.append(current_price)
        minimum_sale_price_list.append(minimum_sale_price)
        lowest_price_list.append(lowest_price)
        average_price_list.append(average_price)
        highest_price_list.append(highest_price)
        price_beat_by_result_list.append(price_beat_by_result)
        timestamp_list.append(timestamp)

    except mysql.connector.Error as error:
      logging.info("Failed to retrieve record into user_price_action table {}".format(error))

  return (
    product_sku_list, 
    product_url_list,
    product_current_price_list,
    minimum_sale_price_list, 
    lowest_price_list,
    average_price_list,
    highest_price_list,
    price_beat_by_result_list, 
    timestamp_list
    )