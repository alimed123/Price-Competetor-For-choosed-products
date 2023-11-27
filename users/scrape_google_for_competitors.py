# USE THIS FILE IF USERS ONLY GAVE URL AND NO SKUs
# SCRAPE USERs COMPETITOR PRODUCTS FROM GOOGLE

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
from w3lib.html import get_base_url
import json
import re
import logging

user_products_list = []
user_sku_list = []
competitor_list = []
competitor_price_list = []
matched_code = []
matched_competitor_filename = ''
competitor_with_issues_filename = ''
consolidated_report_filename = ''
negative_list = ["ebay.com.au", "railblaza.com","amazon.com.au", "catch.com.au", "kogan.com", "mydeal.com.au", "dicksmith.com.au", "kayaks2fish.com", "thebbqstore.com.au"]
special_case_website = ['bcf.com.au']

prices = {}
  
error_user_url_list = []
error_scraped_competitor_url_list = []
error_scraped_competitor_title_list = []
error_scraped_competitor_price_list = []
error_is_proper_competitor_product_list = []
error_competitor_url_response_code = []
error_mpn_list = []
error_upc_list = []

# LIST CONTAINERS FOR ONE OUTPUT FILE
consolidated_sku = []
consolidated_mpn = []
consolidated_upc = []
consolidated_product_url = []
consolidated_product_name = []
consolidated_current_price = []
consolidated_competitor_list_type = []
consolidated_competitor_ranking = []
consolidated_minimum_viable_price = []
consolidated_competitor_product_url = []
consolidated_competitor_product_name = []
consolidated_competitor_price = []
consolidated_tracking_enabled = []
consolidated_match_confidence = []
consolidated_match_type = []
consolidated_match_value = []
consolidated_manual_tracking = []

# VARIABLES USED FOR PRICE ACTION
current_sku_list = []
current_sku = ''
competitor_counter_list = []
mpn_list = []
upc_list = []
user_product_price_list = []
price_action_user_product_name = []
min_sale_price_list = []
competitor_lowest_list = [] # USE TO IDENTIFY THE COMPETITOR WITH HIGHEST PRICE
competitor_highest_list = [] # USE TO IDENTIFY THE COMPETITOR WITH HIGHEST PRICE

# Load helpers
from users.marektplace_logic import *
from helpers.db_connect import db_connect,is_connected
from helpers.zenrows import *
from helpers.substring_processor import *
from helpers.price_db_tasks import price_history
# from helpers.main_error import email_error_report
from helpers.get_price_calculations import *
from helpers.fetch_html_create_json import *
from helpers.zenrows_json_search import *
from helpers.special_case_search import *
from helpers.special_websites import *
from helpers.price_scrape_with_extruct import price_scrape_with_extruct
from users.user_min_sale_price_calculator import calculate_min_sale_price
from users.user_beat_price_by import beat_price_by
from users.user_price_scraper_db_tasks import *
from users.user_price_action_notification import *
from google_merchant.google_content_merchant_center import google_update_products
#from neto.neto_update_price_by_json import *

# Rounding final price
def custom_round(price):
    if price % 1 > 0.5:
        return int(price) + 0.99
    elif price % 1 == 0.5:
        return round(price,2)
    else:
        return int(price)
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

# GENERATE CSV FILE
def generate_sku_competitor_csv(user_products_list, user_sku_list, competitor_list, competitor_price_list, matched_code):
  global matched_competitor_filename

  directory = os.path.dirname(os.path.realpath(__file__))
  now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  logging.info('Saving to a CSV file.')
  logging.info('Url: %s, SKU: %s, Competitors: %s, Competitor Price: %s, Matched Code: %s', len(user_products_list), len(user_sku_list), len(competitor_list), len(competitor_price_list), len(matched_code))
  data = {"Url": user_products_list, "SKU": user_sku_list, "Competitors": competitor_list, "Competitor Price":competitor_price_list, "Matched Code":matched_code}
  # df = pd.DataFrame.from_dict(data, orient='index')
  df = pd.DataFrame(data)

  filename = f"Matched_Competitor_List{ now }.csv"

  logging.info('%s saved sucessfully.', filename)

  file_path = os.path.join(directory,'user_google_competitor/', filename)
  matched_competitor_filename = file_path

  df.to_csv(file_path, index=False)

def get_manually_updater(page_id,db_connection):
  # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    insert_product_query = """SELECT manually_tracking FROM competitor_pages WHERE page_id = %s """


    values = (page_id)

    mycursor = db_connection.cursor()

    mycursor.execute(insert_product_query, values)
    
    manuall=mycursor.fetchall()
    return manuall[0][0]

# SAVE DATA INTO competitor_pages table
def save_to_competitor_pages(url, sku, competitor_product_url, competitor_product_price, manual,db_connection):

  timestamp = datetime.datetime.now()
  site_url = extract_domain(competitor_product_url)
  try:
    price = float(str(competitor_product_price).rstrip("."))
  except:
    price = float(competitor_product_price)
  try:

    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    insert_product_query = """INSERT INTO competitor_pages(
                page_url,
                price,
                site_url,
                discovered,
                user_product,
                user_product_sku,
                manually_tracking) VALUES (%s, %s, %s, %s, %s, %s,%s) 
                ON DUPLICATE KEY UPDATE 
                page_url = VALUES(page_url), 
                price = VALUES(price), 
                site_url = VALUES(site_url),
                discovered = VALUES(discovered), 
                user_product = VALUES(user_product),
                user_product_sku = VALUES(user_product_sku)"""

    values = (
        competitor_product_url,
        price,
        site_url,
        timestamp,
        url,
        sku,
        manual
    )

    mycursor = db_connection.cursor()

    mycursor.execute(insert_product_query, values)

    db_connection.commit()
    logging.info("%s Record saved successfully into competitor_pages table", mycursor.rowcount)

  except mysql.connector.Error as error:
    logging.info("Failed to save record from competitor_pages table {}\n".format(error))

  mycursor.close()

def get_competitor_page_id(competitor_product_url, db_connection):
  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()

    insert_product_query = """SELECT
      page_id
      FROM competitor_pages
      WHERE
      page_url = %s
    """
    
    values = (
        competitor_product_url,
    )

    mycursor = db_connection.cursor()

    mycursor.execute(insert_product_query, values)

    db_connection.commit()
    rows = mycursor.fetchall()
    for row in rows:
      id = row[0]

    return id
  
  except mysql.connector.Error as error:
    logging.info("Failed to fetch record from competitor_pages table {}\n".format(error))

  mycursor.close()

# SAVE DATA INTO competitor_product_prices
def save_to_competitor_product_prices(page_id, prices, db_connection):

  price_json_string = json.dumps(prices)

  try:
    # Check DB connection and established connection if not connected
    if is_connected(db_connection):
      pass
    else:
      db_connection = db_connect()
    
    insert_prices_query = """INSERT INTO competitor_product_prices(
                page_id,
                prices) VALUES (%s, %s) 
                ON DUPLICATE KEY UPDATE 
                page_id = VALUES(page_id), 
                prices = VALUES(prices)"""

    values = (
        page_id,
        price_json_string
    )

    mycursor = db_connection.cursor()

    mycursor.execute(insert_prices_query, values)

    db_connection.commit()
    logging.info("%s Record saved successfully into competitor_product_prices table", mycursor.rowcount)

  except mysql.connector.Error as error:
    logging.info("Failed to save record from competitor_product_prices table {}\n".format(error))

  mycursor.close()

# CHECK IF MPN OR UPC EXIST ON THE COMPETITOR URL
def check_mpn_upc_exist(mpn, upc, competitor_url):
  directory = os.path.dirname(os.path.realpath(__file__))
  global special_case_website
  
  items = []
  found = False
  match_confidence = ''
  match_type = ''
  zenrows_match_counter = 0
  plain_match_counter = 0
  special_case_match_counter = 0
  response = None
  
  items.append(upc)
  items.append(mpn)

  code_to_return = ''

  extracted_domain_name = extract_domain(competitor_url)

  if extracted_domain_name in special_case_website:
    logging.info('Special case search: %s', competitor_url)
    response = special_case_search(competitor_url)
    data = response.text

    # SAVE THE RESPONSE DATA INTO A TEXT FILE FOR DEBUGGING PURPOSES
    logging.info('Now saving response data into a file')
    removed_parameters = remove_query_parameters(competitor_url)
    clean_competitor_url = remove_special_char(removed_parameters)
    competitor_url_filename = f'{clean_competitor_url}-SPECIAL_CASE_SEARCH.txt'
    competitor_url_file_path = os.path.join(directory,'response_data/', competitor_url_filename)
    f = open(competitor_url_file_path, "w+")
    response_data = json.loads(data)
    response_str = json.dumps(response_data)
    f.write(response_str)
    f.close

    for index, item in enumerate(items):

      if item != '':
        logging.info('Now searching for %s', item)
        found_code = search_value(response_data, item)
        logging.info('found_code: %s', found_code)

        if len(found_code):
          if index == 0: # CHECK THE MATCH TYPE
            match_type = 'UPC'
          else:
            match_type = 'MPN'

          found = True
          code_to_return += item
          match_confidence = 'HIGH'
          logging.info("'%s' found on the page %s", found_code, competitor_url)
          special_case_match_counter += 1

  else:
    # Send a GET request to fetch the web page
    response= zenrows_auto_parser_no_proxy(competitor_url)
    if response.status_code != 200:
      response = general_zenrows_autoparser(competitor_url)

    if response:
      # Check if the request was successful (status code 200)
      if response.status_code == 200:

        # SAVE THE RESPONSE DATA INTO A TEXT FILE FOR DEBUGGING PURPOSES
        logging.info('Now saving response data into a file')
        removed_parameters = remove_query_parameters(competitor_url)
        clean_competitor_url = remove_special_char(removed_parameters)
        competitor_url_filename = f'{clean_competitor_url}-ZENROWS.txt'
        competitor_url_file_path = os.path.join(directory,'response_data/', competitor_url_filename)
        f = open(competitor_url_file_path, "w+")
        response_data = json.loads(response.content)
        json_str = json.dumps(response_data)
        f.write(json_str)
        f.close

        # Look for the specified text "02-5004-11" in the page
        for index, item in enumerate(items):
          if item != '':
            logging.info('Now searching for %s', item)
            pattern = r"\b" + item + r"\b"

            json_data = json.loads(response.content)
            # Custom Search using Script Tags and Meta propertiess
            found_text_in_script_meta = search_value(json_data, item)

            logging.info('found_text_in_script_meta: %s', found_text_in_script_meta)

            # Check if the text is found
            if len(found_text_in_script_meta):

              if index == 0: # CHECK THE MATCH TYPE
                match_type = 'UPC'
                code_to_return += item
              else:
                match_type = 'MPN'
                if zenrows_match_counter == 1: # CHECK IF NEEDED TO ADD A COMMA
                  code_to_return += ', ' + item
                else:
                  code_to_return += item

              found = True
              logging.info("'%s' found on the page %s", found_text_in_script_meta, competitor_url)
              zenrows_match_counter += 1

            else:
              logging.info("'%s' not found using ZenRows on the page %s", item, competitor_url)
              
              logging.info("Now trying with PLAIN HTML search.")
              
              try:
                # Use beautifulsoup
                fresponse = fetch_webpage_content(competitor_url)

                if fresponse.status_code == 200:
                  
                  # Parse the HTML content of the page using BeautifulSoup
                  soup = BeautifulSoup(fresponse.content, 'html.parser')

                  # SAVE THE RESPONSE DATA INTO A TEXT FILE FOR DEBUGGING PURPOSES
                  logging.info('Now saving response data into a file')
                  removed_parameters = remove_query_parameters(competitor_url)
                  clean_competitor_url = remove_special_char(removed_parameters)
                  competitor_url_filename = f'{clean_competitor_url}-PLAIN_HTML.txt'
                  competitor_url_file_path = os.path.join(directory,'response_data/', competitor_url_filename)
                  f = open(competitor_url_file_path, "w+")
                  soup_data = soup.prettify()
                  f.write(soup_data)
                  f.close

                  # Search using BeautifulSoup
                  found_text = re.findall(pattern, soup.prettify())

                  logging.info('found_text: %s', found_text)

                  # Check if the text is found
                  if len(found_text):

                    if index == 0: # CHECK THE MATCH TYPE
                      match_type = 'UPC'
                      code_to_return += item
                    else:
                      match_type = 'MPN'
                      if plain_match_counter == 1: # CHECK IF NEEDED TO ADD A COMMA
                        code_to_return += ', ' + item
                      else:
                        code_to_return += item

                    found = True
                    match_confidence = 'LOW'
                    logging.info("'%s' found on the page %s using PLAIN HTML search.", item, competitor_url)
                    response.status_code = fresponse.status_code
                    plain_match_counter += 1

                  else:

                    response.status_code = fresponse.status_code
                    logging.info("'%s' not found on the page %s using PLAIN HTML search.", item, competitor_url)

                else:

                  response.status_code = fresponse.status_code
                  logging.info("Failed to fetch the page. Status Code: %s", response.status_code)
              except:
                pass
      else:
        match_confidence = 'FAIL'
        match_type = 'NONE'
        code_to_return = 'NONE'
        logging.info("Failed to fetch the page. Status Code: %s", response.status_code)
    else:
      match_confidence = 'FAIL'
      match_type = 'NONE'
      code_to_return = 'NONE'
      logging.info("Failed to fetch the page. Status Code: %s", response.status_code)
  if zenrows_match_counter != 0:
    match zenrows_match_counter: # IDENTIFY MATCH CONFIDENCE WHEN USING ZENROWS
      case 2:
        match_confidence = 'HIGH'
        match_type = 'BOTH'
      case 1:
        match_confidence = 'MEDIUM'
  else:
    match plain_match_counter: # IDENTIFY MATCH CONFIDENCE WHEN USING PLAIN HTML
      case 2:
        match_type = 'BOTH'
        match_confidence = 'MEDIUM'
      case 1:
        match_confidence = 'LOW'
  
  if zenrows_match_counter == 1 and plain_match_counter == 1:
    match_type = 'BOTH'

  # SET VALUES TO NONE IF ALL CONDITIONS ARE MET
  if zenrows_match_counter == 0 and plain_match_counter == 0 and response.status_code == 200 and (extracted_domain_name not in special_case_website): 
    match_confidence = 'NONE'
    code_to_return = 'NONE'
    match_type = 'NONE'

  if special_case_match_counter == 0 and (extracted_domain_name in special_case_website): # SET VALUES TO NONE IF SPECIAL CASE SEARCH DID NOT FIND A MATCH
    match_confidence = 'NONE'
    code_to_return = 'NONE'
    match_type = 'NONE'

  if response.status_code != 200 and match_confidence != 'FAIL':
    match_confidence = 'NONE'
    code_to_return = 'NONE'
    match_type = 'NONE'

  return {
    "match_confidence": match_confidence,
    "response_code": response.status_code,
    "exist": found,
    "matched_code": code_to_return,
    "match_type": match_type
  }

# SAVE ALL COMPETITORS WITH ISSUES/ERRORS TO CSV
def save_errors_csv(user_url, scraped_competitor_url, error_scraped_competitor_title_list, scraped_competitor_price, is_proper_competitor_product, error_mpn_list, error_upc_list, competitor_url_response_code):
  global competitor_with_issues_filename

  directory = os.path.dirname(os.path.realpath(__file__))
  now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  logging.info('Saving to a CSV file.')
  logging.info('Url: %s, Competitors: %s, Competitors Title: %s, Competitors Price: %s, MPN/UPC Exist: %s, MPN: %s, UPC: %s, Response Code: %s', len(user_url), len(scraped_competitor_url), len(error_scraped_competitor_title_list), len(scraped_competitor_price), len(is_proper_competitor_product), len(error_mpn_list), len(error_upc_list), len(competitor_url_response_code))
  data = {"Url": user_url, "Competitors": scraped_competitor_url, "Competitors Title":error_scraped_competitor_title_list, "Competitors Price": scraped_competitor_price, "MPN/UPC Exist":is_proper_competitor_product, "MPN": error_mpn_list, "UPC": error_upc_list, "Response Code":competitor_url_response_code}
  # df = pd.DataFrame.from_dict(data, orient='index')
  df = pd.DataFrame(data)

  filename = f"Competitor_url_with_issues{ now }.csv"

  logging.info('%s saved sucessfully.', filename)

  file_path = os.path.join(directory,'user_google_competitor/', filename)
  competitor_with_issues_filename = file_path

  df.to_csv(file_path, index=False)

# GENERATE CONSOLIDATED REPORT FILE MATCHED/NOT MATCHED
def generate_one_report(sku,
                        mpn,
                        upc,
                        product_url,
                        product_name, 
                        current_price, 
                        competitor_list_type, 
                        consolidated_competitor_ranking,
                        minimum_viable_price, 
                        competitor_product_url, 
                        competitor_product_name, 
                        competitor_price, 
                        tracking_enabled, 
                        match_confidence, 
                        match_type, 
                        match_value,
                        manual_tracking,
                        current_sku_list, # FOR PRICE ACTION SHEET
                        price_action_user_product_name, # FOR PRICE ACTION SHEET
                        mpn_list, # FOR PRICE ACTION SHEET
                        upc_list, # FOR PRICE ACTION SHEET
                        competitor_lowest_list, # FOR PRICE ACTION SHEET
                        competitor_highest_list, # FOR PRICE ACTION SHEET
                        competitor_counter_list, # FOR PRICE ACTION SHEET
                        db_connection):
  
  if is_connected(db_connection):
    pass
  else:
    db_connection = db_connect()
  global consolidated_report_filename
  directory = os.path.dirname(os.path.realpath(__file__))
  now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')

  logging.info('Processing Price Action Summary Reporting file for products: %s', current_sku_list)
  summary_data = price_action_generate_summary(current_sku_list, db_connection)
  
  product_sku_list, product_url_list, product_current_price_list, minimum_sale_price_list, lowest_price_list, average_price_list, highest_price_list, price_beat_by_result_list, timestamp_list = summary_data
  for i,price in enumerate(price_beat_by_result_list):
    price_beat_by_result_list[i]=custom_round(float(price))
  logging.info('%s - %s - %s', competitor_lowest_list, competitor_highest_list, competitor_counter_list)
  logging.info('Saving to a CSV file.')
  logging.info('SKU: %s, NAME: %s, MPN: %s, UPC: %s, CURRENT PRICE: %s, MINIMUM VIABLE PRICE: %s, NEW PRICE: %s, COMPETITOR LOWEST PRICE: %s, COMPETITOR AVG PRICE: %s, COMPETITOR HIGHEST PRICE: %s, LOWEST PRICE COMPETITOR: %s, HIGHEST PRICE COMPETITOR: %s, NUMBER OF COMPETITORS: %s', len(product_sku_list), len(price_action_user_product_name), len(mpn_list), len(upc_list), len(product_current_price_list), len(minimum_sale_price_list), len(price_beat_by_result_list), len(lowest_price_list), len(average_price_list), len(highest_price_list), len(competitor_lowest_list), len(competitor_highest_list), len(competitor_counter_list))
  
  data1 = {"SKU": product_sku_list, 
           "NAME": price_action_user_product_name, 
           "MPN": mpn_list, 
           "UPC": upc_list, 
           "CURRENT PRICE": product_current_price_list, 
           "MINIMUM VIABLE PRICE": minimum_sale_price_list,
           "NEW PRICE": price_beat_by_result_list,
           "COMPETITOR LOWEST PRICE": lowest_price_list,
           "COMPETITOR AVG PRICE": average_price_list,
           "COMPETITOR HIGHEST PRICE": highest_price_list,
           "LOWEST PRICE COMPETITOR": competitor_lowest_list,
           "HIGHEST PRICE COMPETITOR": competitor_highest_list,
           "NUMBER OF COMPETITORS": competitor_counter_list,
           "Manually updated": "no"
           }

  logging.info('Saving to a CSV file.')
  logging.info('SKU: %s, MPN: %s, UPC: %s, PRODUCT URL: %s, PRODUCT NAME: %s, CURRENT PRICE: %s, MINIMUM VIABLE PRICE: %s, COMPETITOR LIST TYPE: %s, COMPETITOR RANKING: %s, COMPETITOR PRODUCT URL: %s, COMPETITOR PRODUCT NAME: %s, COMPETITOR PRICE: %s, TRACKING ENABLED: %s, MATCH CONFIDENT: %s, MATCH TYPE: %s, MATCH VALUE: %s', len(sku), len(mpn), len(upc), len(product_url), len(product_name), len(current_price), len(minimum_viable_price), len(competitor_list_type), len(consolidated_competitor_ranking), len(competitor_product_url), len(competitor_product_name), len(competitor_price), len(tracking_enabled), len(match_confidence), len(match_type), len(match_value))
  
  data2 = {"SKU": sku, 
          "MPN": mpn, 
          "UPC": upc, 
          "PRODUCT URL": product_url, 
          "CURRENT PRICE": current_price, 
          "MINIMUM VIABLE PRICE": minimum_viable_price, 
          "COMPETITOR LIST TYPE": competitor_list_type, 
          "COMPETITOR RANKING": consolidated_competitor_ranking,
          "COMPETITOR PRODUCT URL": competitor_product_url, 
          "COMPETITOR PRODUCT NAME": competitor_product_name, 
          "COMPETITOR PRICE": competitor_price, 
          "TRACKING ENABLED": tracking_enabled, 
          "MATCH CONFIDENCE": match_confidence, 
          "MATCH TYPE": match_type, 
          "MATCH VALUE": match_value,
          "MANUAL TRACKING":manual_tracking}
  
  df2 = pd.DataFrame.from_dict(data2, orient='index')
  df2=df2.transpose()
  df1 = pd.DataFrame(data1)
  #df2 = pd.DataFrame(data2)
  
  filename = f"Daily_Report{ now }.xlsx"

  logging.info('%s saved sucessfully.', filename)


  file_path = os.path.join("Daily report", filename)

  consolidated_report_filename = file_path
  
  # IF FOR SOME REASON SOME DATAS ARE MISSING FILL IT WITH 0
  df1.fillna(0, inplace=True)  # Fill NaN values with 0
  df2.fillna(0, inplace=True)  # Fill NaN values with 0

  df1_sorted = df1.sort_values(by='SKU')
  df2_sorted = df2.sort_values(by='SKU')

  with pd.ExcelWriter(file_path) as writer:
    df1_sorted.to_excel(writer, sheet_name="PriceAction", index=False)
    df2_sorted.to_excel(writer, sheet_name="Competitors", index=False)
  return data1,data2

# TO-DO SCRAPE USERS PRODUCT SKUS
def scrape_google_for_competitors(row):

  global competitor_list
  global user_products_list
  global competitor_price_list
  global user_sku_list
  global matched_code
  global marketplace_list
  global negative_list
  global special_case_website

  global prices
  
  global error_user_url_list 
  global error_scraped_competitor_url_list 
  global error_scraped_competitor_title_list 
  global error_scraped_competitor_price_list 
  global error_is_proper_competitor_product_list 
  global error_competitor_url_response_code 
  global error_mpn_list 
  global error_upc_list 

  # LIST CONTAINERS FOR ONE OUTPUT FILE
  global consolidated_sku 
  global consolidated_mpn 
  global consolidated_upc 
  global consolidated_product_url 
  global consolidated_product_name 
  global consolidated_current_price 
  global consolidated_competitor_list_type 
  global consolidated_competitor_ranking
  global consolidated_minimum_viable_price 
  global consolidated_competitor_product_url 
  global consolidated_competitor_product_name 
  global consolidated_competitor_price 
  global consolidated_tracking_enabled 
  global consolidated_match_confidence 
  global consolidated_match_type 
  global consolidated_match_value 
  global consolidated_manual_tracking

  # VARIABLES USED FOR PRICE ACTION
  global current_sku_list 
  global current_sku 
  global competitor_counter_list 
  global mpn_list 
  global upc_list 
  global user_product_price_list 
  global price_action_user_product_name 
  global min_sale_price_list 
  global competitor_lowest_list # USE TO IDENTIFY THE COMPETITOR WITH HIGHEST PRICE
  global competitor_highest_list # USE TO IDENTIFY THE COMPETITOR WITH HIGHEST PRICE
  
  # Connect to the database
  db_connection = db_connect()

  response_data_list = [] # LIST CONTAINER FOR PAID PRODUCTS AND ORGANIC RESULTS

  # Loop through the csv rows
  sku = row[0]
  user_product_name = row[1]
  url = row[2]
  mpn = row[3]
  upc = row[4]
  min_sale_price_manual = row[5]
  cost_price = row[6]
  markup_perc = row[7]
  markup_dollar = row[8]
  beat_price_by_perc = row[9]
  beat_price_by_dollar = row[10]
  special_websites=["www.aquayak.com","www.wynnummarine.com.au","www.bendigomarine.com.au"]
  logging.info('Now processing %s product', sku)
  current_sku_list.append(sku)
  price_action_user_product_name.append(user_product_name)
  mpn_list.append(mpn if mpn != '' else 'NONE')
  upc_list.append(upc if upc != '' else 'NONE')

  user_product_price = 0
  lowest_price_list = []
  competitor_counter = 0
  current_lowest_price = 0 # RESET VARIABLE IF SKU CHANGED
  current_comp_lowest_price = '' # RESET VARIABLE IF SKU CHANGED
  current_highest_price = 0 # RESET VARIABLE IF SKU CHANGED
  current_comp_highest_price = '' # RESET VARIABLE IF SKU CHANGED

  # Solve for User's minimum sale price
  if (len(min_sale_price_manual)):
    min_sale_price = min_sale_price_manual
    logging.info('Minimum Viable Price is %s', min_sale_price)
  else:
    min_sale_price = calculate_min_sale_price(str(cost_price), str(markup_perc), str(markup_dollar))

  try: # THIS WILL PREVENT THE APPLICATION FROM TERMINATING WHEN A REQUEST MODULE ERROR OCCURS

    # Make a HTTP Request to the url
    try:
      response = requests.get(url)
    except:
      response=requests.get(url)
    content = response.text
    
    # -START- IF YOU WANT TO USE BEAUTIFULSOUP
    soup = BeautifulSoup(content, "html.parser")

    if sku == "":

      # Using extruct package to extract microdata/schema
      base_url = get_base_url(content, response.url)
      schema_data = extruct.extract(content, base_url=base_url)

      if user_product_name == '':
        # Step 3: Find the desired tag
        # find_sku = soup.find('div', attrs={'data-firstsku': True})
        # logging.info('soup find - %s', find_sku["data-firstsku"])
        user_product_name = soup.find('h1').text
        logging.info(user_product_name)
        # -END-

      if schema_data is not None:

        sku = find_key(schema_data, "sku")
          
        logging.info('Found sku %s', sku)
        # if type(result) is list: # Check if result is a list
        #   result = result[0]
    
    # Get the current price
    check_user_domain_name = extract_domain(url)
    if check_user_domain_name == 'kayaks2fish.com':
      user_product_price = remove_special_characters_and_letters(soup.find(class_='productpromo').get_text())
    else:
      user_product_price = price_scrape_with_extruct(url)
    
    logging.info('Price found for %s: %s', sku, user_product_price )
    user_product_price_list.append(float(user_product_price))
    
    # Process title for ZenRows search
    user_product_name = user_product_name.replace(" ", "+")

    # TO-DO USE ZENROWS TO SCRAPE GOOGLE FOR COMPETITOR PRODUCTS
    response = zenrows(user_product_name)

    # Process ZenRows result
    parsed_data = json.loads(response)
    
    if parsed_data is not None:

      # CHECK IF ORGANIC RESULT IS PRESENT IN THE ZENROWS RESPONSE AND STORE IT IN THE response_data_list
      if 'organic_results' in parsed_data:
        response_data_list = [
          {
            "type": "ORGANIC",
            "date": entry["date"],
            "description": entry["description"],
            "displayed_link": entry["displayed_link"],
            "domain": entry["domain"],
            "link": entry["link"],
            "title": entry["title"],
            "rank": str(index + 1)
          }
          for index, entry in enumerate(parsed_data['organic_results'])
        ]

      # APPEND THE PAID PRODUCTS TO THE response_data_list
      if 'paid_products' in parsed_data:
        response_data_list += [
          {
            "type": "PAID",
            "advertiser": entry["advertiser"],
            "avg_rating": entry["avg_rating"],
            "full_title": entry["full_title"],
            "link": entry["link"],
            "prev_price": entry["prev_price"],
            "price": entry["price"],
            "review_count": entry["review_count"],
            "title": entry["title"]
          }
          for entry in parsed_data['paid_products'] if entry["title"]
        ]
      
      if len(response_data_list) != 0:
        logging.info('Found %s Products for %s', len(parsed_data['paid_products']), sku)

        for item in response_data_list:
          if "railblaza.com" in item['link']:
            continue

          # CHECK IF THE item IS A PAID PRODUCT OR AN ORGANIC RESULT
          if item['type'] == 'ORGANIC':

            # Check if product is a special webiste
            if item["link"].split("/")[2] in special_websites:
              product_price = sepcial_websites_scraper(item["link"])

            else:
              # GET FOR THE PRODUCT PRICE USING EXTRUCT/BEAUTIFULSOUP
              product_price = str(price_scrape_with_extruct(item['link']))

            index = next((i for i, c in enumerate(product_price) if not c.isdigit() and c != '.'), len(product_price))
            
            product_price_x = product_price[:index].rstrip(".")

            try:
              product_price=remove_special_char(str(product_price))
            except:
              product_price = product_price_x

            if float(product_price) == 0:
              product_price_r = zenrows_auto_parser_no_proxy(item['link'])
              if product_price_r.status_code !=200:
                product_price_r = general_zenrows_autoparser(item['link'])
              if product_price_r:
                if product_price_r.status_code == 200:
                  logging.info("Searching for price using Zenrows")
                  price_re=re.findall("price': '(.*?)',",str(product_price_r.json()))
                  if price_re:
                    logging.info("Price found with Zenrows")
                    product_price = price_re[0]
                  else:
                    logging.info("Price not found with Zenrows")
              else:
                pass
            logging.info('product_price %s', product_price)
            product_link = item['link']
            product_title = item['title']
            product_list_type = item['type']
            product_rank = item['rank']

          else:
            product_price = item['price']
            product_link = item['link']
            product_title = item['title']
            product_list_type = item['type']
            product_rank = 'NONE'

          
          logging.info('Checking if %s is a valid competitor', product_link)

          extracted_domain_name = extract_domain(product_link)

          logging.info('Extracted domain name: %s', extracted_domain_name)
          logging.info('Negative list: %s', negative_list)

          simplified_url = remove_query_parameters(product_link) # CLEAN ANY URL PARAMETERS

          price = remove_special_characters_and_letters(product_price)
          if price == "":
            logging.info("price not found in the page link will be skipped")
            continue
          if extracted_domain_name not in negative_list: # CHECK IF THE DOMAIN IS A MARKETPLACE/OR THE WEBSITE ITSELF
          
            logging.info('%s is not in the Negative list.', extracted_domain_name)

            # DO A CHECK IF THE URL IS A VALID COMPETITOR PRODUCT MATCH
            is_mpn_upc_exist = check_mpn_upc_exist(mpn, upc, product_link)

            logging.info('is_mpn_upc_exist %s', is_mpn_upc_exist)

            if is_mpn_upc_exist['exist'] == True:
              
              if current_lowest_price == 0 and (is_mpn_upc_exist['match_confidence'] != 'LOW' and is_mpn_upc_exist['match_confidence'] !="MEDIUM"):
                current_lowest_price = float(price)

              if current_highest_price == 0 and (is_mpn_upc_exist['match_confidence'] != 'LOW' and is_mpn_upc_exist['match_confidence'] !="MEDIUM") :
                current_highest_price = float(price)
              
              prices[product_link] = price

              # Prepare CSV data - MATCHED-ONLY
              user_products_list.append(url)
              competitor_list.append(product_link)
              competitor_price_list.append(price)
              user_sku_list.append(sku)
              matched_code.append(is_mpn_upc_exist['matched_code'])
              logging.info('Matched code: %s', is_mpn_upc_exist['matched_code'])

              # CSV FILE FOR 1 CONSOLIDATED OUTPUT (MATCHED/NOT MATCHED)
              consolidated_sku.append(sku)
              consolidated_mpn.append(mpn)
              consolidated_upc.append(upc)
              consolidated_product_url.append(url)
              consolidated_product_name.append(user_product_name.replace("+", " "))
              consolidated_current_price.append(float(user_product_price))
              consolidated_competitor_list_type.append(product_list_type)
              consolidated_competitor_ranking.append(product_rank)
              consolidated_minimum_viable_price.append(float(min_sale_price))
              consolidated_competitor_product_url.append(simplified_url)
              consolidated_competitor_product_name.append(product_title)
              consolidated_competitor_price.append(float(price))

              if is_mpn_upc_exist['match_confidence'] == 'LOW' or is_mpn_upc_exist['match_confidence'] == "MEDIUM" :
                consolidated_tracking_enabled.append('PENDING')
                manual = 'WAITING'

              else:
                consolidated_tracking_enabled.append('YES')
                manual = 'AUTO'

              consolidated_match_confidence.append(is_mpn_upc_exist['match_confidence'])
              consolidated_match_type.append(is_mpn_upc_exist['match_type'])
              consolidated_match_value.append(is_mpn_upc_exist['matched_code'])

              save_to_competitor_pages(url, sku, simplified_url, price, manual,db_connection) # FOR INDIVIDUAL COMPETITOR PAGES

              # Get the page's product id from competitor_pages table
              page_id = get_competitor_page_id(simplified_url, db_connection)

              # Get price history if there exist
              prices_data_from_db = price_history(page_id, db_connection)

              # Get manual tracking history if there exist
              consolidated_manual_tracking.append(manual)      

              prices = json.loads(prices_data_from_db)
              timestamp = datetime.datetime.now()
              timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
              prices[timestamp_str] = price

              save_to_competitor_product_prices(page_id, prices, db_connection) # FOR COMPETITOR PRICE HISTORY

              # else:
              if is_mpn_upc_exist['match_confidence'] != 'LOW' and float(price) != 0 : # MAKE SURE THE COMPETITOR PRICE IS NOT 0
                if is_mpn_upc_exist['match_confidence'] != 'MEDIUM':
                  lowest_price_list.append(price)

              if is_mpn_upc_exist['match_confidence'] != 'LOW' or is_mpn_upc_exist['match_confidence'] != 'MEDIUM': # THERE ARE VALID COMPETITORS WITH 0 PRICE BECAUSE THE SCRAPER CANNOT LOCATE IT
                competitor_counter += 1 # Count the number of valid competitors
                logging.info('Competitor counter: %s', competitor_counter)
                logging.info('SKU: %s', sku)

              # DETERMINE WHICH COMPETITOR HAS THE LOWEST/HIGHEST PRICE
              convert_price = float(price.rstrip("."))
              if convert_price != 0 and convert_price <= current_lowest_price and (is_mpn_upc_exist['match_confidence'] != 'LOW') and is_mpn_upc_exist['match_confidence'] != 'MEDIUM': # DETERMINE COMPETITOR WITH THE LOWEST PRICE
                current_lowest_price = convert_price
                current_comp_lowest_price = simplified_url
                logging.info('Lowest Price: %s with %s', current_comp_lowest_price, current_lowest_price)
              
              if convert_price >= current_highest_price and (is_mpn_upc_exist['match_confidence'] != 'LOW') and is_mpn_upc_exist['match_confidence'] != 'MEDIUM': # DETERMINE COMPETITOR WITH THE HIGHEST PRICE
                current_highest_price = convert_price
                current_comp_highest_price = simplified_url
                logging.info('Highest Price: %s with %s', current_comp_highest_price, current_highest_price)
              
              logging.info('Number of Competitors: %s', competitor_counter)

              # Get the existing competitor price of the user product
              existing_comp_price = get_existing_comp_prices(sku, db_connection)
              
              # Store product price in the prices json
              if len(existing_comp_price):
                
                # Parse each JSON string into Python dictionaries
                prices_dicts = [json.loads(json_str) for json_str in existing_comp_price]
                
                # Combine the price dictionaries into one
                combined_prices_dict = {}
                for price_dict in prices_dicts:
                  combined_prices_dict.update(price_dict)

                combined_prices_dict[simplified_url] = price
                prices_json_data = json.dumps(combined_prices_dict)
              else:
                prices = existing_comp_price
                prices[simplified_url] = price
                prices_json_data = json.dumps(prices)

            else: # SAVE THE COMPETITOR URLS THAT DON'T HAVE THE MPN/UPC OR STATUS CODE ERROR TO A CSV FILE

              simplified_url = remove_query_parameters(product_link) # CLEAN ANY URL PARAMETERS
              error_user_url_list.append(url)
              error_scraped_competitor_url_list.append(simplified_url)
              error_scraped_competitor_title_list.append(product_title)
              error_scraped_competitor_price_list.append(float(price.rstrip(".")))
              error_is_proper_competitor_product_list.append(is_mpn_upc_exist['exist'])
              error_competitor_url_response_code.append(is_mpn_upc_exist['response_code'])
              error_mpn_list.append(mpn)
              error_upc_list.append(upc)

              # CSV FILE FOR 1 CONSOLIDATED OUTPUT (MATCHED/NOT MATCHED)
              consolidated_sku.append(sku)
              consolidated_mpn.append(mpn)
              consolidated_upc.append(upc)
              consolidated_product_url.append(url)
              consolidated_product_name.append(user_product_name.replace("+", " "))
              consolidated_current_price.append(float(user_product_price.rstrip(".")))
              consolidated_competitor_list_type.append(product_list_type)
              consolidated_competitor_ranking.append(product_rank)
              consolidated_minimum_viable_price.append(float(min_sale_price))
              consolidated_competitor_product_url.append(simplified_url)
              consolidated_competitor_product_name.append(product_title)
              consolidated_competitor_price.append(float(price.rstrip(".")))
              consolidated_tracking_enabled.append('NO')
              consolidated_match_confidence.append(is_mpn_upc_exist['match_confidence'])
              consolidated_match_type.append(is_mpn_upc_exist['match_type'])
              consolidated_match_value.append(is_mpn_upc_exist['matched_code'])
              manual = "WAITING" 

              #save code to competitor_page
              save_to_competitor_pages(url, sku, simplified_url, price, manual,db_connection) # FOR INDIVIDUAL COMPETITOR PAGES

              # Get the page's product id from competitor_pages table
              page_id = get_competitor_page_id(simplified_url, db_connection)

              # Get price history if there exist
              prices_data_from_db = price_history(page_id, db_connection)

              # Get manual tracking history if there exist
              consolidated_manual_tracking.append(manual)

              prices = json.loads(prices_data_from_db)
              timestamp = datetime.datetime.now()
              timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
              prices[timestamp_str] = price

              save_to_competitor_product_prices(page_id, prices, db_connection) # FOR COMPETITOR PRICE HISTORY

          else:
             if "railblaza.com" in product_link:
               logging.info("seller is the main brand")
               pass
             elif "kayaks2fish" in product_link:
               logging.info("seller is kayaks2fish")
               logging.info("Link will be skipped")
               pass
             else:
              logging.info("Link is a Market place")
              logging.info("checking if seller is not kayks2fish")

              #Get marketplace platform
              matching_marketplaces = [marketplace for marketplace in negative_list if marketplace in extracted_domain_name]   

              seller=market_place(product_link)
              if seller:
                #Seller is us
                logging.info("%s is an ignore link", product_link)


              elif seller == None:

                #Error while fetching
                logging.info("seller not found %s is an ignore link",product_link)
                consolidated_sku.append(sku)
                consolidated_mpn.append(mpn)
                consolidated_upc.append(upc)
                consolidated_product_url.append(url)
                consolidated_product_name.append(user_product_name.replace("+", " "))
                consolidated_current_price.append(float(user_product_price))
                consolidated_competitor_list_type.append(product_list_type)
                consolidated_competitor_ranking.append(product_rank)
                consolidated_minimum_viable_price.append(float(min_sale_price))
                consolidated_competitor_product_url.append(simplified_url)
                consolidated_competitor_product_name.append(product_title)
                consolidated_competitor_price.append(float(price.rstrip('.')))
                consolidated_tracking_enabled.append('NO')
                consolidated_match_confidence.append('IGNORE')
                consolidated_match_type.append('NONE')
                consolidated_match_value.append('NONE')
                manual = "WAITING"

                #save code to competitor_page
                save_to_competitor_pages(url, sku, simplified_url, price, manual,db_connection) # FOR INDIVIDUAL COMPETITOR PAGES

                # Get the page's product id from competitor_pages table
                page_id = get_competitor_page_id(simplified_url, db_connection)

                # Get price history if there exist
                prices_data_from_db = price_history(page_id, db_connection)

                # Get manual tracking history if there exist
                consolidated_manual_tracking.append(manual)

                prices = json.loads(prices_data_from_db)
                timestamp = datetime.datetime.now()
                timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                prices[timestamp_str] = price

                save_to_competitor_product_prices(page_id, prices, db_connection) # FOR COMPETITOR PRICE HISTORY
                

              else:

                #Seller is not us
                logging.info("seller is not Kayks2fish\nlink aprroved")
                # DO A CHECK IF THE URL IS A VALID COMPETITOR PRODUCT MATCH
                is_mpn_upc_exist = check_mpn_upc_exist(mpn, upc, product_link)

                logging.info('is_mpn_upc_exist %s', is_mpn_upc_exist)

                if is_mpn_upc_exist['exist'] == True:
                  
                  if current_lowest_price == 0 and is_mpn_upc_exist['match_confidence'] != 'LOW' and is_mpn_upc_exist['match_confidence'] != 'MEDIUM':
                    current_lowest_price = float(price)

                  if current_highest_price == 0 and is_mpn_upc_exist['match_confidence'] != 'LOW' and is_mpn_upc_exist['match_confidence'] != 'MEDIUM':
                    current_highest_price = float(price)
                  
                  prices[product_link] = price

                  # Prepare CSV data - MATCHED-ONLY
                  user_products_list.append(url)
                  competitor_list.append(product_link)
                  competitor_price_list.append(price)
                  user_sku_list.append(sku)
                  matched_code.append(is_mpn_upc_exist['matched_code'])
                  logging.info('Matched code: %s', is_mpn_upc_exist['matched_code'])

                  # CSV FILE FOR 1 CONSOLIDATED OUTPUT (MATCHED/NOT MATCHED)
                  consolidated_sku.append(sku)
                  consolidated_mpn.append(mpn)
                  consolidated_upc.append(upc)
                  consolidated_product_url.append(url)
                  consolidated_product_name.append(user_product_name.replace("+", " "))
                  consolidated_current_price.append(float(user_product_price))
                  consolidated_competitor_list_type.append(product_list_type)
                  consolidated_competitor_ranking.append(product_rank)
                  consolidated_minimum_viable_price.append(float(min_sale_price))
                  consolidated_competitor_product_url.append(simplified_url)
                  consolidated_competitor_product_name.append(product_title)
                  consolidated_competitor_price.append(float(price))

                  if is_mpn_upc_exist['match_confidence'] == 'LOW' or is_mpn_upc_exist['match_confidence'] == "MEDIUM":
                    consolidated_tracking_enabled.append('PENDING')
                    manual = "WAITING"

                  else:
                    consolidated_tracking_enabled.append('YES')
                    manual = "AUTO"

                  consolidated_match_confidence.append(is_mpn_upc_exist['match_confidence'])
                  consolidated_match_type.append(is_mpn_upc_exist['match_type'])
                  consolidated_match_value.append(is_mpn_upc_exist['matched_code'])

                  save_to_competitor_pages(url, sku, simplified_url, price, manual,db_connection) # FOR INDIVIDUAL COMPETITOR PAGES

                  # Get the page's product id from competitor_pages table
                  page_id = get_competitor_page_id(simplified_url, db_connection)

                  # Get price history if there exist
                  prices_data_from_db = price_history(page_id, db_connection)
                  
                  # Get manual tracking history if there exist
                  consolidated_manual_tracking.append(manual)
                  
                  prices = json.loads(prices_data_from_db)
                  timestamp = datetime.datetime.now()
                  timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                  prices[timestamp_str] = price

                  save_to_competitor_product_prices(page_id, prices, db_connection) # FOR COMPETITOR PRICE HISTORY

                  # else:
                  if is_mpn_upc_exist['match_confidence'] != 'LOW' and float(price) != 0 : # MAKE SURE THE COMPETITOR PRICE IS NOT 0
                    if is_mpn_upc_exist['match_confidence'] != 'MEDIUM':
                        lowest_price_list.append(price)

                  if is_mpn_upc_exist['match_confidence'] != 'LOW' or is_mpn_upc_exist['match_confidence'] != 'MEDIUM': # THERE ARE VALID COMPETITORS WITH 0 PRICE BECAUSE THE SCRAPER CANNOT LOCATE IT
                    competitor_counter += 1 # Count the number of valid competitors
                    logging.info('Competitor counter: %s', competitor_counter)
                    logging.info('SKU: %s', sku)

                  # DETERMINE WHICH COMPETITOR HAS THE LOWEST/HIGHEST PRICE
                  convert_price = float(price)
                  if convert_price != 0 and convert_price <= current_lowest_price and (is_mpn_upc_exist['match_confidence'] != 'LOW') and is_mpn_upc_exist['match_confidence'] != 'MEDIUM': # DETERMINE COMPETITOR WITH THE LOWEST PRICE
                    current_lowest_price = convert_price
                    current_comp_lowest_price = simplified_url
                    logging.info('Lowest Price: %s with %s', current_comp_lowest_price, current_lowest_price)
                  
                  if convert_price >= current_highest_price and (is_mpn_upc_exist['match_confidence'] != 'LOW') and is_mpn_upc_exist['match_confidence'] != 'MEDIUM': # DETERMINE COMPETITOR WITH THE HIGHEST PRICE
                    current_highest_price = convert_price
                    current_comp_highest_price = simplified_url
                    logging.info('Highest Price: %s with %s', current_comp_highest_price, current_highest_price)
                  
                  logging.info('Number of Competitors: %s', competitor_counter)

                  # Get the existing competitor price of the user product
                  existing_comp_price = get_existing_comp_prices(sku, db_connection)
                  
                  # Store product price in the prices json
                  if len(existing_comp_price):
                    
                    # Parse each JSON string into Python dictionaries
                    prices_dicts = [json.loads(json_str) for json_str in existing_comp_price]
                    
                    # Combine the price dictionaries into one
                    combined_prices_dict = {}
                    for price_dict in prices_dicts:
                      combined_prices_dict.update(price_dict)

                    combined_prices_dict[simplified_url] = price
                    prices_json_data = json.dumps(combined_prices_dict)
                  else:
                    prices = existing_comp_price
                    prices[simplified_url] = price
                    prices_json_data = json.dumps(prices)

                else: # SAVE THE COMPETITOR URLS THAT DON'T HAVE THE MPN/UPC OR STATUS CODE ERROR TO A CSV FILE
                  
                  simplified_url = remove_query_parameters(product_link) # CLEAN ANY URL PARAMETERS
                  error_user_url_list.append(url)
                  error_scraped_competitor_url_list.append(simplified_url)
                  error_scraped_competitor_title_list.append(product_title)
                  error_scraped_competitor_price_list.append(float(price))
                  error_is_proper_competitor_product_list.append(is_mpn_upc_exist['exist'])
                  error_competitor_url_response_code.append(is_mpn_upc_exist['response_code'])
                  error_mpn_list.append(mpn)
                  error_upc_list.append(upc)

                  # CSV FILE FOR 1 CONSOLIDATED OUTPUT (MATCHED/NOT MATCHED)
                  consolidated_sku.append(sku)
                  consolidated_mpn.append(mpn)
                  consolidated_upc.append(upc)
                  consolidated_product_url.append(url)
                  consolidated_product_name.append(user_product_name.replace("+", " "))
                  consolidated_current_price.append(float(user_product_price))
                  consolidated_competitor_list_type.append(product_list_type)
                  consolidated_competitor_ranking.append(product_rank)
                  consolidated_minimum_viable_price.append(float(min_sale_price))
                  consolidated_competitor_product_url.append(simplified_url)
                  consolidated_competitor_product_name.append(product_title)
                  consolidated_competitor_price.append(float(price))
                  consolidated_tracking_enabled.append('NO')
                  consolidated_match_confidence.append(is_mpn_upc_exist['match_confidence'])
                  consolidated_match_type.append(is_mpn_upc_exist['match_type'])
                  consolidated_match_value.append(is_mpn_upc_exist['matched_code'])
                  manual = "WAITING" 

                  #save code to competitor_page
                  save_to_competitor_pages(url, sku, simplified_url, price, manual,db_connection) # FOR INDIVIDUAL COMPETITOR PAGES

                  # Get the page's product id from competitor_pages table
                  page_id = get_competitor_page_id(simplified_url, db_connection)

                  # Get price history if there exist
                  prices_data_from_db = price_history(page_id, db_connection)

                  # Get manual tracking history if there exist
                  consolidated_manual_tracking.append(manual)

                  prices = json.loads(prices_data_from_db)
                  timestamp = datetime.datetime.now()
                  timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                  prices[timestamp_str] = price

                  save_to_competitor_product_prices(page_id, prices, db_connection) # FOR COMPETITOR PRICE HISTORY

      else: # IF 0 PRODUCTS
        user_products_list.append(url)
        competitor_list.append('No listed product on Google.')
        competitor_price_list.append('No listed product on Google.')
        user_sku_list.append(sku)
        matched_code.append('Nothing to match')

        # CSV FILE FOR 1 CONSOLIDATED OUTPUT
        consolidated_sku.append(sku)
        consolidated_mpn.append(mpn)
        consolidated_upc.append(upc)
        consolidated_product_url.append(url)
        consolidated_product_name.append(user_product_name.replace("+", " "))
        consolidated_current_price.append(float(user_product_price))
        consolidated_competitor_list_type.append('NONE')
        consolidated_competitor_ranking.append('NONE')
        consolidated_minimum_viable_price.append(float(min_sale_price))
        consolidated_competitor_product_url.append('NONE')
        consolidated_competitor_product_name.append('NONE')
        consolidated_competitor_price.append('NONE')
        consolidated_tracking_enabled.append('NO')
        consolidated_match_confidence.append('NONE')
        consolidated_match_type.append('NONE')
        consolidated_match_value.append('NONE')
        consolidated_manual_tracking.append("WAITING")      

    else: # IF ERROR 4XX/5XX
      user_products_list.append(url)
      competitor_list.append('No listed paid product on Google.')
      competitor_price_list.append('No listed paid product on Google.')
      user_sku_list.append(sku)
      matched_code.append('Nothing to match')

      # CSV FILE FOR 1 CONSOLIDATED OUTPUT (MATCHED/NOT MATCHED)
      consolidated_sku.append(sku)
      consolidated_mpn.append(mpn)
      consolidated_upc.append(upc)
      consolidated_product_url.append(url)
      consolidated_product_name.append(user_product_name.replace("+", " "))
      consolidated_current_price.append(float(user_product_price))
      consolidated_competitor_list_type.append('NONE')
      consolidated_minimum_viable_price.append(float(min_sale_price))
      consolidated_competitor_product_url.append('NONE')
      consolidated_competitor_product_name.append('NONE')
      consolidated_competitor_price.append('NONE')
      consolidated_tracking_enabled.append('NO')
      consolidated_match_confidence.append('FAIL')
      consolidated_match_type.append('NONE')
      consolidated_match_value.append('NONE')
      consolidated_manual_tracking.append("WAITING")  
      

    logging.info('Competitor with Lowest Price: %s', current_comp_lowest_price)
    logging.info('Competitor with Highest Price: %s', current_comp_highest_price)
    logging.info('Number of Competitors: %s', competitor_counter)
    competitor_lowest_list.append(current_comp_lowest_price)
    competitor_highest_list.append(current_comp_highest_price)
    # competitor_counter_list.append(competitor_counter)

    if lowest_price_list:
      # CALCULATE LOWEST PRICE AND PRICE BEAT BY
      # START - Save User's product info to user_price_action table 
      logging.info('Now calculating lowest price and price beat by.')
      # Solve for the lowest price
      lowest_price = float(get_lowest_price(lowest_price_list))

      average_price = float(get_average_price(lowest_price_list))

      highest_price = float(get_highest_price(lowest_price_list))

      # Solve for User's minimum sale price
      if (len(min_sale_price_manual)):
        min_sale_price = min_sale_price_manual
        logging.info('Minimum Sale Price is %s', min_sale_price)
      else:
        min_sale_price = calculate_min_sale_price(str(cost_price), str(markup_perc), str(markup_dollar))

      # Calculate the Beat By Price
      beat_price_by_result = beat_price_by(lowest_price, beat_price_by_perc, beat_price_by_dollar)

      # Action to take if beat_price_by_result is higher/lower than min_sale_price
      if float(beat_price_by_result) > float(min_sale_price):
        do_update_price = 'yes'
      else:
        do_update_price = 'no'
        logging.info("price will not be updated %s,%s",min_sale_price,beat_price_by_result)
      # Check if product already exist
      exist_price_action = check_product_exist_price_action(sku, db_connection)

      timestamp = datetime.datetime.now()
      # timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

      # Get the product SKU
      if sku == '':
        product_sku = get_product_sku(sku, db_connection)
        parent_sku, sku = product_sku
      else:
        product_sku = sku
        parent_sku = None
        
      if exist_price_action == True:
        logging.info('Updating user price action table.')
        # Update user_price_action table
        update_price_action(
          url, 
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
          "NO",
          timestamp, 
          db_connection
        )
      else:
        logging.info('Saving to user price action table.')
        # Insert data if not yet in user_price_action table
        insert_price_action(
          url, 
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
          "NO",
          timestamp, 
          db_connection
        )
    else:
      logging.info('No valid competitors found.')

      lowest_price = 0
      average_price = 0
      highest_price = 0
      price = 0

      # Solve for User's minimum sale price
      if (len(min_sale_price_manual)):
        min_sale_price = min_sale_price_manual
        logging.info('Minimum Sale Price is %s', min_sale_price)
      else:
        min_sale_price = calculate_min_sale_price(str(cost_price), str(markup_perc), str(markup_dollar))

      # Calculate the Beat By Price
      beat_price_by_result = 0

      # Action to take if beat_price_by_result is higher/lower than min_sale_price
      if float(beat_price_by_result) > float(min_sale_price):
        do_update_price = 'yes'
      else:
        do_update_price = 'no'

      # Check if product already exist
      exist_price_action = check_product_exist_price_action(sku, db_connection)

      # Get the existing competitor price of the user product
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

      timestamp = datetime.datetime.now()
      # timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

      # Get the product SKU
      if sku == '':
        product_sku = get_product_sku(sku, db_connection)
        parent_sku, sku = product_sku
      else:
        product_sku = sku
        parent_sku = None
        
      if exist_price_action == True:
        logging.info('Updating user price action table.')
        # Update user_price_action table
        update_price_action(
          url, 
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
          timestamp, 
          db_connection
        )
      else:
        logging.info('Saving to user price action table.')
        # Insert data if not yet in user_price_action table
        insert_price_action(
          url, 
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
          timestamp, 
          db_connection
        )
    competitor_counter_list.append(competitor_counter)
    # END of task
  except Exception as e:

    # STILL PROCESS THE PRICE ACTION FOR THE SKU WITH ERROR
    lowest_price = 0
    average_price = 0
    highest_price = 0
    beat_price_by_result = 0
    do_update_price = 'no'

    # Check if product already exist
    exist_price_action = check_product_exist_price_action(sku, db_connection)

    # Get the existing competitor price of the user product
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

    timestamp = datetime.datetime.now()
    # timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    # Get the product SKU
    if sku == '':
      product_sku = get_product_sku(sku, db_connection)
      parent_sku, sku = product_sku
    else:
      product_sku = sku
      parent_sku = None
      
    if exist_price_action == True:
      logging.info('Updating user price action table.')
      # Update user_price_action table
      update_price_action(
        url, 
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
        timestamp, 
        db_connection
      )
    else:
      logging.info('Saving to user price action table.')
      # Insert data if not yet in user_price_action table
      insert_price_action(
        url, 
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
        timestamp, 
        db_connection
      )

    logging.info('An error occured while processing %s', sku)
    logging.info('Competitor with Lowest Price: %s', 'NONE')
    logging.info('Competitor with Highest Price: %s', 'NONE')
    logging.info('Number of Competitors: %s', 0)
    user_product_price_list.append(0)
    competitor_lowest_list.append('NONE')
    competitor_highest_list.append('NONE')
    competitor_counter_list.append(0)

    # CSV FILE FOR 1 CONSOLIDATED OUTPUT (MATCHED/NOT MATCHED)
    consolidated_sku.append(sku)
    consolidated_mpn.append(mpn)
    consolidated_upc.append(upc)
    consolidated_product_url.append(url)
    consolidated_product_name.append(user_product_name)
    consolidated_current_price.append(float(user_product_price))
    consolidated_competitor_list_type.append('NONE')
    consolidated_competitor_ranking.append('NONE')
    consolidated_minimum_viable_price.append(float(min_sale_price))
    consolidated_competitor_product_url.append('NONE')
    consolidated_competitor_product_name.append('NONE')
    consolidated_competitor_price.append('NONE')
    consolidated_tracking_enabled.append('NO')
    consolidated_match_confidence.append('FAIL')
    consolidated_match_type.append('NONE')
    consolidated_match_value.append('NONE')
    consolidated_manual_tracking.append("WAITING")    
    
    logging.error('%s', e)
    e_type, e_object, e_traceback = sys.exc_info()

    logging.error(e_traceback.tb_lineno)
    pass # CONTINUE THE APPLICATION IF IT ENCOUNTERS A REQUEST MODULE ERROR

  
def generate_reports_scrape_google_for_competitors(db_connection):
  # SAVE THE ERROR DATA TO A CSV
  # if error_user_url_list:
  #   save_errors_csv(
  #     error_user_url_list, 
  #     error_scraped_competitor_url_list, 
  #     error_scraped_competitor_title_list, 
  #     error_scraped_competitor_price_list, 
  #     error_is_proper_competitor_product_list, 
  #     error_mpn_list, 
  #     error_upc_list, 
  #     error_competitor_url_response_code
  #   )
    
  # SAVE THE MATCHED COMPEETITORS IN CSV
  # if user_products_list:
  #   generate_sku_competitor_csv(
  #     user_products_list, 
  #     user_sku_list, 
  #     competitor_list, 
  #     competitor_price_list, 
  #     matched_code
  #   )

  # SAVE THE CONSOLIDATED REPORTING IN CSV
  if consolidated_sku:
    data_1,data_2=generate_one_report(
      consolidated_sku,
      consolidated_mpn,
      consolidated_upc,
      consolidated_product_url,
      consolidated_product_name,
      consolidated_current_price,
      consolidated_competitor_list_type,
      consolidated_competitor_ranking,
      consolidated_minimum_viable_price,
      consolidated_competitor_product_url,
      consolidated_competitor_product_name,
      consolidated_competitor_price,
      consolidated_tracking_enabled,
      consolidated_match_confidence,
      consolidated_match_type,
      consolidated_match_value,
      consolidated_manual_tracking,
      current_sku_list, # FOR PRICE ACTION SHEET
      price_action_user_product_name, # FOR PRICE ACTION SHEET
      mpn_list, # FOR PRICE ACTION SHEET
      upc_list, # FOR PRICE ACTION SHEET
      competitor_lowest_list, # FOR PRICE ACTION SHEET
      competitor_highest_list, # FOR PRICE ACTION SHEET
      competitor_counter_list, # FOR PRICE ACTION SHEET
      db_connection
    )
    return data_1,data_2
  # NOTIFY USER FOR PRICE ACTIONS THROUGH EMAIL
  if current_sku_list:
    price_action_notify_user(
      current_sku_list, 
      db_connection,
      matched_code, 
      error_user_url_list, 
      consolidated_report_filename
    )
 
"""def update_products_online_shop(db_connection):

  # SEND PRODUCT URLS TO UPDATE PRICE ON NETO PRODUCT API
  main_neto(current_sku_list, db_connection)
"""
  # SEND PRODUCT URLS TO UPDATE PRICE ON GOOGLE MERCHANT API
  # google_update_products(current_sku_list, db_connection)

# TO-DO CREATE A LOGIC TO IDENTIFY MARKETPLACES
  # - maretplaces: ebay, Amazon, Catch, Kogan, Myers, Bunnings, mydeal, Trademe, graysonline, temple&webster, iconic, asos, dicksmith
    # - EBAY AND AMAZON TO START
  # - IDENTIFY WHO THE SELLER IS, IF IT IS US (KAYAK2FISH)

# TO-DO CHECK WHAT MPN/UPC CODES ARE ON THE PAGE ON THE URLS WITH ISSUES

# TO-DO CREATE BRAND/ORGANIZATION WITH GLOBAL IGNORE LIST

#testing function:
