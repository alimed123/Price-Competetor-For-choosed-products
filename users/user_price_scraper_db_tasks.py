import mysql.connector
from helpers.db_connect import db_connect,is_connected
import datetime
import json
import requests
import os
import random
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from collections import OrderedDict
import logging

# Load helpers
from helpers.substring_processor import *
from helpers.user_agent import user_agent
# from helpers.proxies import get_proxies
from helpers.main_email import send_html_email

load_dotenv()

# Use this to change between "DEV" and "PROD" .env variables
ENV = os.getenv("PROD")

# Check if page exist in the DB
def user_check_page_exist(child_sku, db_connection):
  
  logging.info("Checking User page - %s", child_sku)
  
  # Check DB connection and established connection if not connected
  if is_connected(db_connection):
    pass
  else:
    db_connection = db_connect()

  # Identify if page already exist, if not save to database
  exist_query=f'SELECT EXISTS(SELECT 1 from user_product_pages WHERE sku LIKE "%{child_sku}%")'

  # Update the existing URL to Old status. For later

  mycursor = db_connection.cursor()
  mycursor.execute(exist_query)
  exist_row = mycursor.fetchall()

  flag = ''

  for row in exist_row:
    if (row[0] == 0):
      flag = 'New'
    else:
      flag = 'Old'

  logging.info("The page is: %s", flag)

  return flag

def user_save_pages_to_db(url, date, db_connection):

  try:

    # Extract domain
    domain = extract_domain(url)

    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    save_url_query = f"INSERT INTO user_product_pages(page_url, site_url, discovered, flag) VALUES ('{url}', 'https://www.{domain}', '{date}', 'New' )"

    mycursor = db_connection.cursor()

    mycursor.execute(save_url_query)

    db_connection.commit()
    logging.info("%s Record inserted successfully into user_product_pages table", mycursor.rowcount)
    mycursor.close()

  except mysql.connector.Error as error:
    logging.info("Failed to save record into user_product_pages table {}".format(error))

def user_check_old_urls(query, db_connection):

  directory = os.path.dirname(os.path.realpath(__file__))
  parent_dir = os.path.abspath(os.path.join(directory, os.pardir))
  
  # Instantiate array containers
  url_list = []
  original_url = []
  original_status = []
  destination_url = []
  destination_status = []
  url_data = []

  # Check DB connection and established connection if not connected
  if is_connected(db_connection):
    pass
  else:
    db_connection = db_connect()

  # If you wanted to test URL check, just change the query variable appropriately
  # Example if you just want to test all urls under example.com, you can use '%example.com%'
  get_urls_query = 'SELECT page_url FROM user_product_pages WHERE page_url = %s'

  value = (query,)

  mycursor = db_connection.cursor()
  mycursor.execute(get_urls_query, value)
  pages = mycursor.fetchall()

  url_list = [row[0] for row in pages]

  # Get User-Agents for requests header
  user_agents = user_agent()

  url_list = list(OrderedDict.fromkeys(url_list))

  for url in url_list:

    # Formulate proxy with random proxies. No Proxies for now.
    # proxies = get_proxies() 

    # Formulate header with random user-agents
    # Setup random user-agent
    random_user_agents = random.randint(1, len(user_agents) - 1)
    headers = user_agents[random_user_agents]

    logging.info('Now checking status: %s', url)

    response = requests.get(url, headers=headers)

    # Loop through response history and extract data
    if response.history:
        
        url_to_update = None
        url_status = None
        url_destination = None

        for step in response.history:
          original_url.append(step.url)
          original_status.append(step.status_code)
          
          url_to_update = step.url
          url_status = step.status_code

        destination_url.append(response.url)
        destination_status.append(response.status_code)

        url_destination = response.url

        url_data.append({
          'url': url_to_update,
          'status': url_status,
          'destination': url_destination
        })
        
  # Save scraped URLs to a CSV file
  now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
  if (original_url):
    logging.info('Saving a CSV file.')
    logging.info('original_url: %s, original_status: %s, destination_url: %s, destination_status: %s', len(original_url), len(original_status), len(destination_url), len(destination_status))
    data = {"original_url": original_url, "original_status": original_status, "destination_url": destination_url, "destination_status": destination_status}
    # df = pd.DataFrame.from_dict(data, orient='index')
    df = pd.DataFrame(data)

    # Drop empty Urls
    df['original_url'].replace('', np.nan, inplace=True)
    df.dropna(subset=['original_url'], inplace=True)

    # Remove duplicates
    df.drop_duplicates('original_url', keep='first', inplace=True)
    # df = df.transpose()

    filename = f"checked_url_status{ now }.csv"

    logging.info('%s saved sucessfully.', filename)

    file_path = os.path.join(directory,'check_url_status/', filename)
    df.to_csv(file_path, index=False)

    # Generate an HTML version of the CSV
    a = pd.read_csv(file_path)

    # to save as html file named as "Table"
    a.to_html("Table.htm")

    # assign it to a variable (string)
    msg_head = "<html><head><style> table {border-collapse: collapse; width: 100%;} th, td {text-align: left; padding: 10px; border: 1px solid #ddd;} tr:nth-child(even){background-color: #f2f2f2} th {background-color: #31b821; color: white;} a {background-color: transparent; text-decoration: none;}</style></head><body><p>"
    msg_end = "</p></body></html>"
    html_file = msg_head + a.to_html() + msg_end

    # Send the generated file to the customer
    send_html_email(os.getenv(f"{ENV}EMAIL"), f'Redirected/Removed Pages - {now}', html_file)
  else:
    logging.info('No checked_url_status.csv output file generated.')

  return url_data

# Update prices on competitor_pages
def user_update_product_price(product_url, price, db_connection):
  
  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    update_price_query = f"UPDATE user_product_pages SET price='{price}' WHERE page_url='{product_url}'"

    mycursor = db_connection.cursor()

    mycursor.execute(update_price_query)

    db_connection.commit()
    logging.info("%s Record updated successfully into user_product_pages table.", mycursor.rowcount)
    mycursor.close()

  except mysql.connector.Error as error:
    logging.info("Failed to update record into user_product_pages table {}".format(error))

def user_get_old_price(urls, db_connection):

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
      get_all_product = f"SELECT page_url FROM user_product_pages WHERE page_url LIKE '%{url}%'"

      mycursor = db_connection.cursor()
      mycursor.execute(get_all_product)
      pages = mycursor.fetchall()

      for page in pages:
        product_list.append(page[0])

    return product_list
  
  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from user_product_pages table {}\n".format(error))

# Update product_prices table if new
def user_save_product_prices(prices_json_data, page_id_primary_key, db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    insert_product_price_query = f"INSERT INTO user_product_prices(prices, page_id) VALUES ('{prices_json_data}', '{page_id_primary_key}' )"

    mycursor = db_connection.cursor()

    mycursor.execute(insert_product_price_query)

    db_connection.commit()
    logging.info("%s Record saved successfully into user_product_prices table.", mycursor.rowcount)
    mycursor.close()

  except mysql.connector.Error as error:
    logging.info("Failed to save record from user_product_prices table {}\n".format(error))


# Update product_prices table
def user_update_product_prices(prices_json_data, page_id_primary_key, db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    update_product_price_query = f"UPDATE user_product_prices SET prices='{prices_json_data}' WHERE page_id='{page_id_primary_key}'"

    mycursor = db_connection.cursor()

    mycursor.execute(update_product_price_query)

    db_connection.commit()
    logging.info("%s Record updated successfully into user_product_prices table.", mycursor.rowcount)
    mycursor.close()

  except mysql.connector.Error as error:
    logging.info("Failed to update record from user_product_prices table {}\n".format(error))

# Display price JSON data from DB
def user_fetch_product_prices(db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    select_product_price_query = f"SELECT page_id, prices FROM user_product_prices";

    mycursor = db_connection.cursor()

    mycursor.execute(select_product_price_query)
    row = mycursor.fetchall()

    return row

  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from user_product_prices table {}\n".format(error))

# Get the page_id primary key from main table (competitor_pages)
def user_get_primary_key(url, db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    get_primary_key = f"SELECT page_id FROM user_product_pages WHERE page_url LIKE '%{url}%'";

    mycursor = db_connection.cursor()

    mycursor.execute(get_primary_key)
    rows = mycursor.fetchall()
    
    for row in rows:
      id = row[0]

    return id

  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from user_product_pages table {}\n".format(error))

# Get the page_id primary key from main table (competitor_pages)
def user_check_key_exist(id, db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    key_exist = f"SELECT * FROM user_product_prices WHERE page_id={id}";

    mycursor = db_connection.cursor()

    mycursor.execute(key_exist)
    rows = mycursor.fetchall()
    
    id = 0

    for row in rows:
      id = row[0]

    if (id):
      return True
    else:
      return False

  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from user_product_prices table {}\n".format(error))

# Get the page_id primary key from main table (competitor_pages)
def user_price_history(id, db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    key_exist = f"SELECT * FROM user_product_prices WHERE page_id={id}";

    mycursor = db_connection.cursor()

    mycursor.execute(key_exist)
    rows = mycursor.fetchall()
    
    id = 0

    for row in rows:
      id = row[0]

    if (id):
      return row[1]
    else:
      return json.dumps({})

  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from user_product_prices table {}\n".format(error))

def check_product_exist_price_action(sku, db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    key_exist = f'SELECT product_url FROM user_price_action WHERE sku="{sku}"';

    mycursor = db_connection.cursor()

    mycursor.execute(key_exist)
    rows = mycursor.fetchall()
    
    id = 0

    for row in rows:
      id = row[0]

    if (id):
      return True
    else:
      logging.info('Product not yet in the user_price_action table.')
      return False

  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from user_product_prices table {}\n".format(error))



def update_price_action(url, 
                        parent_sku, 
                        sku,
                        user_product_price, 
                        prices_json_data, 
                        min_sale_price, 
                        lowest_price, 
                        average_price,
                        highest_price, 
                        beat_price_by_result, 
                        do_update_price,
                        manually_updated, 
                        timestamp_str, 
                        db_connection):
  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    update_product_price_query = "UPDATE user_price_action SET parent_sku = %s, sku = %s, current_price = %s, competitor_prices = %s, minimum_sale_price = %s, lowest_price = %s, average_price = %s, highest_price = %s, price_beat_by_result = %s, do_update_price = %s, manually_updated = %s,timestamp = %s WHERE product_url = %s"

    values = (parent_sku, sku, user_product_price, prices_json_data, min_sale_price, lowest_price, average_price, highest_price, beat_price_by_result, do_update_price,manually_updated, timestamp_str, url)

    mycursor = db_connection.cursor()

    mycursor.execute(update_product_price_query, values)

    db_connection.commit()
    logging.info("%s Record update successfully into user_price_action table.", mycursor.rowcount)
    mycursor.close()

  except mysql.connector.Error as error:
    logging.info("Failed to update record from user_price_action table {}\n".format(error))

def insert_price_action(url, 
                        parent_sku, 
                        sku,
                        user_product_price,
                        prices_json_data, 
                        min_sale_price, 
                        lowest_price,
                        average_price, 
                        highest_price,
                        beat_price_by_result, 
                        do_update_price, 
                        manual_update,
                        timestamp, 
                        db_connection):

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    insert_product_price_query = "INSERT INTO user_price_action(product_url, parent_sku, sku, current_price, competitor_prices, minimum_sale_price, lowest_price, average_price, highest_price, price_beat_by_result, do_update_price, manually_updated ,timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)"

    values = (url, 
              parent_sku, 
              sku,
              user_product_price, 
              prices_json_data, 
              min_sale_price, 
              lowest_price, 
              average_price, 
              highest_price, 
              beat_price_by_result, 
              do_update_price, 
              "no",
              timestamp)

    mycursor = db_connection.cursor()

    mycursor.execute(insert_product_price_query, values)

    db_connection.commit()
    logging.info("%s Record saved successfully into user_price_action table.", mycursor.rowcount)
    mycursor.close()

  except mysql.connector.Error as error:
    logging.info("Failed to save record from user_price_action table {}\n".format(error))

def get_existing_comp_prices(sku, db_connection):
  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    get_existing_comp_prices_data = 'SELECT competitor_prices FROM user_price_action WHERE sku = %s';

    value = (sku, )

    mycursor = db_connection.cursor()

    mycursor.execute(get_existing_comp_prices_data, value)
    row = mycursor.fetchall()

    if (row):
      return row[0]
    else:
      return {}

  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from user_product_prices table {}\n".format(error))

def get_product_sku(sku, db_connection):
  
  logging.info('Now fetching parent_sku, sku for page %s', sku)
  # Clean url of trailing slash
  # clean_url = remove_trailing_slash(url)

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    get_product_sku = f'SELECT parent_sku, sku FROM user_product_pages WHERE sku LIKE "{sku}"';

    mycursor = db_connection.cursor()

    mycursor.execute(get_product_sku)
    row = mycursor.fetchall()

    if (row):
      return row[0]
    else:
      return ''

  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from user_product_prices table {}\n".format(error))

def get_price_action_data(db_connection):
    try:
      # Check DB connection and established connection if not connected
      if is_connected(db_connection):
        pass
      else:
        db_connection = db_connect()

      get_product_sku = f"SELECT sku,minimum_sale_price,price_beat_by_result FROM user_price_action  WHERE 1;";

      mycursor = db_connection.cursor()

      mycursor.execute(get_product_sku)
      row = mycursor.fetchall()

      return row

    except mysql.connector.Error as error:
      logging.info("Failed to fetch record from user_product_prices table {}\n".format(error))