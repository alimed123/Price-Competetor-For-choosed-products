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
import sys
# Load helpers
from helpers.json_parser import parse_json
from helpers.user_agent import user_agent
from users.user_price_scraper_db_tasks import *
from helpers.substring_processor import remove_special_char_except_dot

load_dotenv()

# Use this to change between "DEV" and "PROD" .env variables
ENV = os.getenv("PROD")


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

def price_scrape_with_extruct(url):
  logging.info("Now searching %s for Product price.", url)

   # Get User-Agents for requests header
  user_agents = user_agent()

  # Get random user-agent
  random_user_agents = random.randint(1, len(user_agents) - 1)
  headers = user_agents[random_user_agents]

  price = 0
  try:
    # Make a HTTP Request to the url
    response = requests.get(url)

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
        response = requests.get(url, proxies=proxies)

      # Using extruct package to extract microdata/schema
      pp = pprint.PrettyPrinter(indent=2)
      base_url = get_base_url(response.text, response.url)
      schema_data = extruct.extract(response.text, base_url=base_url)

      # Using Beautifulsoup for non-microdata/schema objects
      # # Step 2: Create a BeautifulSoup object
      soup = BeautifulSoup(content, "html.parser")

      # # Step 3: Find the desired tag
      meta_property_price = soup.find("meta", property="product:price:amount")
      meta_property_og_price = soup.find("meta", property="og:price:amount")
      application_ldjson = soup.find_all("script", type="application/ld+json")
      woocommerce = soup.find(class_="woocommerce-Price-amount amount")
      shopify = soup.find(class_="ProductMeta__Price Price")
      normal_lower_price_class = soup.find(class_="price")
      normal_upper_price_class = soup.find(class_="Price")

      logging.info("Scraping %s", url)
      is_price_found = False

      # Check if price exist in microdata/schema
      if schema_data is not None:
      
        # Find 'price' key
        result = find_key(schema_data, "price")

        if result is not None:
          logging.info('Price: %s', result)
          is_price_found = True
          price = remove_special_char_except_dot(str(result))

        else:
          logging.info("Price not found in microdata/schema.")
          is_price_found = False

      else:
        logging.info('Cannot find microdata/schema element.')

      # Check if price exists in meta property element
      if (is_price_found != True):

        if meta_property_price is not None: 
          
          logging.info('Price: %s', meta_property_price.get("content"))
          is_price_found = True

          price = remove_special_char_except_dot(meta_property_price.get("content"))
          
        else:
          logging.info("No price meta property.")
          is_price_found = False
      
      # Check if price exists in meta property OG element
      if (is_price_found != True):

        if meta_property_og_price is not None: 

          logging.info('%s', meta_property_og_price)
          is_price_found = True

          price = remove_special_char_except_dot(meta_property_og_price)

        else:
          logging.info("No price meta property og:price.")
          is_price_found = False

      # Check if price exists if WooCommerce website
      if (is_price_found != True):
        
        if (woocommerce is not None):
          logging.info('%s', woocommerce.text)
          is_price_found = True
          
          price = remove_special_char_except_dot(woocommerce.text)
          
        else:
          logging.info("No woocommerce price.")
          is_price_found = False

      # Check if price exists if application/ld+json
      if (is_price_found != True):
        
        if (application_ldjson is not None):
          
          for item in application_ldjson:
            # Find 'price' key
            result = find_key(item, "price")

          if result is not None:
            logging.info('%s', result)
            is_price_found = True

            price = remove_special_char_except_dot(application_ldjson.text)

        else:
          logging.info("No application_ldjso price.")
          is_price_found = False
      else:
        logging.info('Cannot find microdata/schema element.')
      
      # Check if price exists if application/ld+json
      if (is_price_found != True):
        
        if (shopify is not None):
          logging.info('%s', shopify.text)
          is_price_found = True

          price = remove_special_char_except_dot(shopify.text)
        else:
          logging.info("No shopify price.")
          is_price_found = False

      # Check if price exists if application/ld+json
      if (is_price_found != True):
        
        if (normal_lower_price_class is not None):
          logging.info('%s', normal_lower_price_class.text)
          is_price_found = True

          price = remove_special_char_except_dot(normal_lower_price_class.text)
        else:
          logging.info("No normal_lower_price_class price.")
          is_price_found = False

      # Check if price exists if application/ld+json
      if (is_price_found != True):
        
        if (normal_upper_price_class is not None):
          logging.info('%s', normal_upper_price_class.text)
          is_price_found = True

          price = remove_special_char_except_dot(normal_upper_price_class.text)
        else:
          logging.info("No normal_upper_price_class price.")
          is_price_found = False

    else: # If requests response code is not 200

      logging.info("Url - %s", url)
      logging.error('Error - Response code: %s', response.status_code)
      price = 0
      pass
  
  except:
    logging.info('An error occured while search for the price of %s', url)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    logging.info(exc_tb.tb_lineno)
    price = 0

  if price is not None :
    return float(price)
  else:
    price = 0