# - Script to update Google Shopping Fields such as Name, Decscription for items that are IsGoogleShopping == Yes
# - If the GSProductCategory needs to be different than default then update into Neto directly. This script won't overwrite it.
# - Updates neto automatically
# - Cron job set up to run at midnight everyday

import csv
import json
import requests
import sys
import re
import html
import os
import os.path

from main_neto_api import NETO_API_URL
from main_neto_api import NETO_API_HEADERS_JSON_GETITEM
from main_neto_api import NETO_API_HEADERS_JSON_UPDATEITEM
# from main_file import write_file
from pprint import pprint
# from common import *
from urllib.parse import unquote
import unicodedata
import traceback
from bs4 import BeautifulSoup
from string import Template
from dotenv import load_dotenv

from helpers.db_connect import db_connect
from helpers.main_email import send_email
from neto.neto_db_tasks import *

load_dotenv()

# Use this to change between "DEV" and "PROD" .env variables
ENV = os.getenv("PROD")

json_get_all_acc = {
  "Filter": {
    "CategoryID":"98",    
    "Page":"0",
    "Limit":"100000",
    "Approved":"True",
    "IsActive":"True",
    "OrderBy":"Enumeration",
    "ParentSKU":"",
    "OutputSelector":["ItemURL", "InventoryID", "SKU", "PromotionPrice", "ParentSKU", "Name", "Brand", "DefaultPrice", "PriceGroups", "Misc41"]
    }
}

parent_only_list = []
products_list = []
product_to_update_list = []
website_domain = "https://www.kayaks2fish.com/"

def fetch_api_prepare_data(products_to_update, db_connection):

  global parent_only_list
  global products_list
  global product_to_update_list

  # DUMMY PRODUCT URL FOR TESTING
  # products_to_update = ["https://www.kayaks2fish.com/railblaza-illuminate-i360"]

  # Check DB connection and established connection if not connected
  if db_connection.is_connected():
    pass
  else:
    db_connection = db_connect()

  for product_item_sku in products_to_update:
    
    logging.info('Processing %s for product update.', product_item_sku)
    # DUMMY PRICE ACTION FOR TESTING
    # sku_price = ("RB-ILLUMINATE-i360-V", None, 74.00, "yes")

    #Todo get the sku, updated price beat by from DB
    sku_price = get_sku_price(product_item_sku, db_connection) # USE THIS LINE TO GET THE ACTUAL PRICE ACTION DATA FROM THE DATABASE
    parent_sku, sku, price, do_update_price = sku_price

    if do_update_price == 'yes': # Check if price_beat_by_result > minimum_sale_price
      
      if sku: # CHECK IF PRODUCT TO BE UPDATED IS ALREADY A CHILD PRODUCT SKU
        updated_item = {
          "Item": {
            "SKU": sku,
            "PriceGroups": {
              "PriceGroup": [
                {
                  "Group": "A",
                  "Price": price
                }
              ]
            }
          }
        }
        product_to_update_list.append(updated_item)

      else:
        # USE PARENT SKU TO GET CHILD SKU ON NETO IF USER DID NOT SUPPLY CHILD SKU MANUALLY
        json_get_all_acc["Filter"]["ParentSKU"] = parent_sku
        json_string = json.dumps(json_get_all_acc)

        try:
          logging.info('Fetching %s Child SKUs in NETO API.', parent_sku)
          all_prod_dict = (requests.post(url = NETO_API_URL, data = json_string, headers = NETO_API_HEADERS_JSON_GETITEM)).json() 
          products_list = all_prod_dict['Item'] #main data is under "item" key
          
          # Create an updated price Item from the products_list
          for item in products_list:

            updated_item = {
              "Item": {
                "SKU": item["SKU"],
                "PriceGroups": {
                  "PriceGroup": [
                    {
                      "Group": "A",
                      "Price": price
                    }
                  ]
                }
              }
            }

            product_to_update_list.append(updated_item)

        except Exception as err:        
          send_email(os.getenv(f"{ENV}EMAIL"),'Error: K2F Google Shopping Field - Failed Neto API Fetch', err)
          traceback.print_exc()

def upload_to_neto():
  global product_to_update_list

  logging.info('Products to update: %s', product_to_update_list)
  #API post
  for item in product_to_update_list:
    logging.info('%s', type(item))
    logging.info('%s', item)
    json_string = json.dumps(item)
    try:
      update_crossell_json_response = requests.post(url = NETO_API_URL, data = json_string, headers = NETO_API_HEADERS_JSON_UPDATEITEM)
      logging.info('%s', update_crossell_json_response.text)
        
    except Exception as err:
      send_email(os.getenv(f"{ENV}EMAIL"),'Error: K2F Google Shopping Field - Neto API Post Failed', update_crossell_json_response.text)
 

def main_neto(products_to_update, db_connection):
  try:
    fetch_api_prepare_data(products_to_update, db_connection)
    # create_shopping_feed()#? Dont need it since we are now updating neto API
    upload_to_neto()
  except Exception as err:        
    send_email(os.getenv(f"{ENV}EMAIL"),'Error: K2F Google Shopping Field - Something Went Wrong', traceback.format_exc())
    traceback.print_exc()
    logging.error('%s', err)
# if __name__ == "__main__":
#   main_neto()