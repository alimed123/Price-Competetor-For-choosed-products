# THIS FILE IS USE TO OVERRIDE TRACKING ENABLED

import pandas as pd
import numpy as np
import datetime
import sys
import os
import os.path
import csv
import mysql.connector
import traceback
from bs4 import BeautifulSoup
import requests
import extruct
import pprint
from w3lib.html import get_base_url
import json
import mysql.connector
import re
import logging

sys.path.append('.')  # Add the parent directory to the Python path

# Load helpers
from helpers.db_connect import db_connect
from helpers.zenrows import *
from helpers.substring_processor import *
from helpers.price_db_tasks import price_history
from helpers.main_error import email_error_report
from helpers.get_price_calculations import *
from helpers.fetch_html_create_json import *
from helpers.zenrows_json_search import *
from helpers.special_case_search import *
from helpers.price_scrape_with_extruct import price_scrape_with_extruct
from users.user_min_sale_price_calculator import calculate_min_sale_price
from users.user_beat_price_by import beat_price_by
from users.user_price_scraper_db_tasks import *
from users.user_price_action_notification import *
from users.neto_func import *
from users.neto_gmc import *
from users.user_price_scraper_db_tasks import *
from users.scrape_google_for_competitors import get_competitor_page_id
#from neto.neto_update_price_by_json import *


# update manualtracknig data on database
def manual_tracking_updater(page_url,db_connection):
  if is_connected(db_connection):
      pass
  else:
    db_connection = db_connect()

  logging.info(f"Updating manual tracknig to yes on database for product_url : {page_url}")
  
  insert_product_query = """UPDATE competitor_pages SET manually_tracking = 'YES' WHERE page_url = %s """

  values = (page_url)

  mycursor = db_connection.cursor()

  mycursor.execute(insert_product_query, values)

  db_connection.commit()



# Get neto data from url
def url_to_df():

    # Read the CSV file from the URL
    df = pd.read_csv("https://www.nabf.com.au/dashboard/data/google-feed/k2f-accessories.csv")

    # Now 'df' is a DataFrame containing your data
    return df

# Get product data by sku
def get_product_data(sku):
    df=url_to_df()
    product=df.loc[df["ID"] == sku]
    if not product.empty:
        return product.to_dict(orient='records')[0]
    else:
        logging.info("Product not found")


# Rounding final price
def custom_round(price):
    if price % 1 > 0.5:
        return int(price) + 0.99
    elif price % 1 == 0.5:
        return round(price,2)
    else:
        return int(price)


def override_tracking():

  manual_file="Manual report"
  excel_file = [f for f in os.listdir(manual_file) if f.endswith('.xlsx')][0]

  db_connection=db_connect()
  # FOR COMPETITORS SHEET
  sku_list = []
  mpn_list = []
  product_url_list = []
  current_price_list = []
  minimum_viable_price_list = []
  competitor_list_type_list = []
  competitor_product_name_list = []
  competitor_price_list = []
  tracking_enabled_list = []
  match_confidence_list = []
  match_type_list = []
  match_value_list = []
  price_beat_results = []

  # FOR PRICEACTION SHEET
  price_action_sku_list = []
  price_action_name_list = []
  price_action_mpn_list = []
  price_action_upc_list = []

  lowest_price_list = []

  current_sku = ''
  competitor_count_list = []
  competitor_count = 0
  action_indexer=0

  file_path = os.path.join(manual_file, excel_file)
  reader=pd.read_excel(file_path,sheet_name="Competitors",index_col=None)
  reader_total_data=pd.read_excel(file_path,sheet_name="PriceAction",index_col=None)

  # Loop through the csv rows
  for index,line in reader.iterrows():
    sku = line['SKU']	
    mpn	= line['MPN']	
    upc	= line['UPC']	
    product_url = line['PRODUCT URL']	
    current_price = line['CURRENT PRICE']	
    minimum_viable_price = line['MINIMUM VIABLE PRICE']	
    competitor_list_type	= line['COMPETITOR LIST TYPE']	
    competitor_product_url	= line['COMPETITOR PRODUCT URL']	
    competitor_product_name	= line['COMPETITOR PRODUCT NAME']	
    competitor_price	= line['COMPETITOR PRICE']	
    tracking_enabled	= line['TRACKING ENABLED']	
    match_confidence	= line['MATCH CONFIDENCE']	
    match_type	= line['MATCH TYPE']	
    match_value = line['MATCH VALUE']
    manual_tracking = line["MANUAL TRACKING"]
    if current_sku == "":
      current_sku = sku

    if current_sku != sku:
      logging.info(current_sku)
      # Rounding final price

      new_price=beat_price_by(lowest_price, "", "5")
      if float(new_price)> float(minimum_viable_price):
          pass
      else:
          new_price=minimum_viable_price
      new_price=custom_round(float(new_price))
      logging.info(f"new price for sku is : {current_sku} {new_price}")
      logging.info(action_indexer)
      reader_total_data.loc[action_indexer, "NEW PRICE"] = new_price
      reader_total_data.loc[action_indexer, "COMPETITOR LOWEST PRICE"]= lowest_price
      reader_total_data.loc[action_indexer, "COMPETITOR AVG PRICE"]= average_price
      reader_total_data.loc[action_indexer, "HIGHEST PRICE COMPETITOR"]= highest_price

      current_sku = sku
      
      logging.info(competitor_count)
      if competitor_count != 0:
        competitor_count_list.append(competitor_count)

      competitor_count = 0
      action_indexer+=1
      
      
      lowest_price_list = []
      if manual_tracking.upper() == 'YES':
        manual_tracking_updater(competitor_product_url,db_connection)
      if tracking_enabled == 'YES' or manual_tracking.upper() == 'YES':
        lowest_price_list.append(competitor_price)
        competitor_count += 1

    else:
      if manual_tracking.upper() == 'YES':
        manual_tracking_updater(competitor_product_url,db_connection)
      if tracking_enabled == 'YES' or manual_tracking.upper() == 'YES' :
        lowest_price_list.append(competitor_price)
        competitor_count += 1
    
    if lowest_price_list:
      lowest_price = float(get_lowest_price(lowest_price_list))
      average_price = float(get_average_price(lowest_price_list))
      highest_price = float(get_highest_price(lowest_price_list))


  new_price=beat_price_by(lowest_price, "", "5")
  if float(new_price)> float(minimum_viable_price):
      pass
  else:
      new_price=minimum_viable_price
  new_price=custom_round(float(new_price))
  logging.info(f"new price for sku is : {current_sku} {new_price}")
  logging.info(action_indexer)
  reader_total_data.loc[action_indexer, "NEW PRICE"] = new_price
  reader_total_data.loc[action_indexer, "COMPETITOR LOWEST PRICE"]= lowest_price
  reader_total_data.loc[action_indexer, "COMPETITOR AVG PRICE"]= average_price
  reader_total_data.loc[action_indexer, "HIGHEST PRICE COMPETITOR"]= highest_price
  
  # Updating database 

  # connecting to database 
  db_connection = db_connect()
  # Check DB connection and established connection if not connected
  if is_connected(db_connection):
    pass
  else:
    db_connection = db_connect()

  # Get parent_sku
  if sku == '':
        product_sku = get_product_sku(sku, db_connection)
        parent_sku, sku = product_sku
  else:
    product_sku = sku
    parent_sku = None
  
  #updating competitor page to yes
  existing_comp_price = get_existing_comp_prices(sku, db_connection)

  # Store product price in the prices json
  if len(existing_comp_price):
    
    # Parse each JSON string into Python dictionaries
    prices_dicts = [json.loads(json_str) for json_str in existing_comp_price]
    
    # Combine the price dictionaries into one
    combined_prices_dict = {}
    for price_dict in prices_dicts:
      combined_prices_dict.update(price_dict)

    prices_json_data = json.dumps(combined_prices_dict)

  else:
    prices = existing_comp_price
    prices_json_data = json.dumps(prices)

  # Time of updating
  timestamp = datetime.datetime.now()
  # Check if price should be updated
  if float(new_price) > float(minimum_viable_price):
      do_update_price = 'yes'
  else:
      do_update_price = 'no'

  update_price_action(
          product_url, 
          parent_sku, 
          sku,
          current_price, 
          prices_json_data, 
          minimum_viable_price, 
          lowest_price,
          average_price,
          highest_price,
          new_price, 
          do_update_price,
          "yes", 
          timestamp, 
          db_connection,
          )
  
#Main function

def main():
  new_price,minimum_viable_price,sku = override_tracking()
  update_neto_gmc(sku,new_price,minimum_viable_price)

if __name__ == "__main__":
  main()
  
      


      
