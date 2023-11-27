from bs4 import BeautifulSoup
import requests
import os
import os.path
import csv
import random
import json
import extruct
import pprint
from w3lib.html import get_base_url
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# Load helpers
from helpers.json_parser import parse_json
from helpers.user_agent import user_agent
from helpers.price_db_tasks import *
from helpers.substring_processor import remove_special_char_except_dot

# Find 'price' key if it exist
def find_key(json_obj, target_key):
  if isinstance(json_obj, dict):
    if target_key in json_obj:
      return json_obj[target_key]
    else:
      for key, value in json_obj.items():
        result = find_key(value, target_key)
        if result is not None:
          return result
  elif isinstance(json_obj, list):
    for item in json_obj:
      result = find_key(item, target_key)
      if result is not None:
        return result
      
  return None

def price_scraper(arg_url=''):
  logging.info("Now scraping for Competitor Product Prices.")

  directory = os.path.dirname(os.path.realpath(__file__))
  parent_dir = os.path.abspath(os.path.join(directory, os.pardir))

  # Connect to the database
  db_connection = db_connect()

  # Get User-Agents for requests header
  user_agents = user_agent()

  # Create a list of websites you dont want to scrape ATM.
  negative_sites = os.path.join(parent_dir, "input_negative_sites.csv")
  
  website_list =[]
  price = None

  if (arg_url == ''):
    # Get the list of websites you want to scrape prices
    with open(f"input_competitor_scrape_price.csv", encoding="unicode_escape") as f:
      reader = csv.DictReader(f)
    
      # Loop through the csv rows
      for line in reader:
        url = line["Url"]
        website_list.append(url)
  else:
    website_list.append(arg_url)

  # Get old prices
  product_list = get_old_price(website_list, db_connection)

  logging.info('product_list - %s', product_list)

  timestamp = datetime.datetime.now()
  timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

  if len(product_list) == 0:
    logging.info('Product URLs not found in the database.')
  else:
    logging.info('Found %s active products on your scrape list.', len(product_list))

  # Loop through the csv rows
  for p in product_list:

    # Get random user-agent
    random_user_agents = random.randint(1, len(user_agents) - 1)
    headers = user_agents[random_user_agents]

    # Make a HTTP Request to the url
    response = requests.get(p)
    
    # Check the HTTP response code
    logging.info('Status: %s', response.status_code)
    if response.status_code == 200:

      is_blocked_cloudflare = False

      content = response.text
      url = response.url

      # Do a check here if we are getting blocked by Cloudflare
      if "Cloudflare Ray ID" in content:
      # if "cf-ray" in response.headers: # ONLY USE THIS TO SIMULATE CLOUDFLARE BLOCKED REQUEST
        logging.info("Request blocked by Cloudflare.")
        is_blocked_cloudflare = True

        # Use proxy
        proxies = {
          "http": f'https://{os.getenv("PROXY_USERNAME")}:{os.getenv("PROXY_PASSWORD")}@{os.getenv("PROXY_HOST")}:{os.getenv("PROXY_PORT")}'
        }
        # Todo if blocked flag the url as blocked
        response = requests.get(p, proxies=proxies)
        content = response.text
        url = response.url

      # Using extruct package to extract microdata/schema
      # pp = pprint.PrettyPrinter(indent=2)
      base_url = get_base_url(content, response.url)
      schema_data = extruct.extract(content, base_url=base_url)

      # Using Beautifulsoup for non-microdata/schema objects
      # # Step 2: Create a BeautifulSoup object
      soup = BeautifulSoup(content, "html.parser")

      # # Step 3: Find the desired tag
      meta_property_price = soup.find("meta", property="product:price:amount")
      meta_property_og_price = soup.find("meta", property="og:price:amount")
      application_ldjson = soup.find("script", type="application/ld+json")
      woocommerce = soup.find(class_="woocommerce-Price-amount amount")

      try:
        logging.info("Scraping %s", url)
        is_price_found = False
        
        # Get the page_id primary key from main table (competitor_pages)
        page_id_primary_key = get_primary_key(url, db_connection)
        logging.info('Product ID: %s', page_id_primary_key)

        #Check if page_id already exist in product_prices table
        key_exist = check_key_exist(page_id_primary_key, db_connection)
        logging.info('Product in table: %s', key_exist)

        # Get price history from JSON
        prices_data_from_db = price_history(page_id_primary_key, db_connection)

        # Check if price exist in microdata/schema
        if schema_data is not None:
        
          # Find 'price' key
          result = find_key(schema_data, "price")
          if type(result) is list: # Check if result is a list
            result = result[0]

          if result is not None:
            logging.info('Price: %s', result)
            is_price_found = True

            price = remove_special_char_except_dot(result)
            logging.info('Timestamp: %s', timestamp_str)

            # Store product price in the prices json
            if bool(prices_data_from_db):
              prices = json.loads(prices_data_from_db)
              prices[timestamp_str] = price
              # logging.info('%s', prices)
              prices_json_data = json.dumps(prices)
            else:
              prices = prices_data_from_db
              prices[timestamp_str] = price
              # logging.info('%s', prices)
              prices_json_data = json.dumps(prices)

            # Save or Update product_prices table
            if key_exist == True:
              price_float = float(price)
              update_product_prices(prices_json_data, page_id_primary_key, db_connection)
              update_product_price(url, price_float, db_connection)
            else:
              price_float = float(price)
              save_product_prices(prices_json_data, page_id_primary_key, db_connection)
              update_product_price(url, price_float, db_connection)
            
          else:
            logging.info("Price not found in microdata/schema.")
            is_price_found = False

        else:
          logging.info('Cannot find microdata/schema element.')

        # Check if price exists in meta property element
        if (is_price_found != True):

          if meta_property_price is not None: 

            logging.info('Price: %s', meta_property_price)
            is_price_found = True

            price = remove_special_char_except_dot(meta_property_price)
            logging.info('Timestamp: %s', timestamp_str)

            # Store product price in the prices json
            if bool(prices_data_from_db):
              prices = json.loads(prices_data_from_db)
              prices[timestamp_str] = price
              # logging.info('%s', prices)
              prices_json_data = json.dumps(prices)
            else:
              prices = prices_data_from_db
              prices[timestamp_str] = price
              # logging.info('%s', prices)
              prices_json_data = json.dumps(prices)

            # Save or Update product_prices table
            if key_exist == True:
              price_float = float(price)
              update_product_prices(prices_json_data, page_id_primary_key, db_connection)
              update_product_price(url, price, db_connection)
            else:
              price_float = float(price)
              save_product_prices(prices_json_data, page_id_primary_key, db_connection)
              update_product_price(url, price, db_connection)

          else:
            logging.info("No price meta property.")
            is_price_found = False
        
        # Check if price exists in meta property OG element
        if (is_price_found != True):

          if meta_property_og_price is not None: 

            logging.info('%s', meta_property_og_price)
            is_price_found = True

            price = remove_special_char_except_dot(meta_property_og_price)
            logging.info('Timestamp: %s', timestamp_str)

            # Store product price in the prices json
            if bool(prices_data_from_db):
              prices = json.loads(prices_data_from_db)
              prices[timestamp_str] = price
              # logging.info('%s', prices)
              prices_json_data = json.dumps(prices)
            else:
              prices = prices_data_from_db
              prices[timestamp_str] = price
              # logging.info('%s', prices)
              prices_json_data = json.dumps(prices)

            # Save or Update product_prices table
            if key_exist == True:
              price_float = float(price)
              update_product_prices(prices_json_data, page_id_primary_key, db_connection)
              update_product_price(url, price, db_connection)
            else:
              price_float = float(price)
              save_product_prices(prices_json_data, page_id_primary_key, db_connection)
              update_product_price(url, price, db_connection)

          else:
            logging.info("No price meta property.")
            is_price_found = False

        # Check if price exists if WooCommerce website
        if (is_price_found != True):
          
          if (woocommerce is not None):
            logging.info('%s', woocommerce.text)

            price = remove_special_char_except_dot(woocommerce.text)
            logging.info('Timestamp: %s', timestamp_str)

            # Store product price in the prices json
            if bool(prices_data_from_db):
              prices = json.loads(prices_data_from_db)
              prices[timestamp_str] = price
              # logging.info('%s', prices)
              prices_json_data = json.dumps(prices)
            else:
              prices = prices_data_from_db
              prices[timestamp_str] = price
              # logging.info('%s', prices)
              prices_json_data = json.dumps(prices)

            # Save or Update product_prices table
            if key_exist == True:
              price_float = float(price)
              update_product_prices(prices_json_data, page_id_primary_key, db_connection)
              update_product_price(url, price, db_connection)
            else:
              price_float = float(price)
              save_product_prices(prices_json_data, page_id_primary_key, db_connection)
              update_product_price(url, price, db_connection)

      except:
        logging.warning('SOMETHING WENT WRONG.')
        pass

    else: # If requests response code is not 200
      logging.error("Cannot access %s", url)
      logging.error('Error - Response code: %s', response.status_code)
      pass
  
  # Check DB connection
  if db_connection.is_connected():
    db_connection.close()
    logging.info("MySQL connection is closed")

  return price
