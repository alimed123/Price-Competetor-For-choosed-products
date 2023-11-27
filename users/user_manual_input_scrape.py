import pandas as pd
import numpy as np
import datetime
import sys
import os
import os.path
import time
import csv
import re
import mysql.connector
from dotenv import load_dotenv
from os.path import exists
from collections import OrderedDict
import traceback

# Load helpers
from helpers.db_connect import db_connect
from helpers.urlchecker import check_old_urls, update_db
from helpers.substring_processor import extract_domain
from helpers.main_error import email_error_report
from helpers.main_email import *
from helpers.price_scraper import price_scraper
from helpers.get_price_calculations import get_lowest_price
from helpers.data_collection_processor import *
# from helpers.auto_update_google_merchant import create_json_google_merchant
from users.user_price_scraper_db_tasks import *
from users.user_price_scraper import scrape_user_price
from users.user_min_sale_price_calculator import calculate_min_sale_price
from users.user_beat_price_by import beat_price_by
from users.user_price_action_notification import price_action_notify_user
from neto.neto_update_price_by_json import *

load_dotenv()

# Use this to change between "DEV" and "PROD" .env variables
ENV = os.getenv("PROD")

def user_result_file(url_list, domain_list):
  directory = os.path.dirname(os.path.realpath(__file__))
  now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  logging.info('Saving to a CSV file.')
  logging.info('SITE URL: %s,URL: %s', len(domain_list), len(url_list))
  data = {"SITE URL": domain_list, "PAGE URL": url_list}
  # df = pd.DataFrame.from_dict(data, orient='index')
  df = pd.DataFrame(data)
  
  # Drop empty Urls
  df['PAGE URL'].replace('', np.nan, inplace=True)
  df.dropna(subset=['PAGE URL'], inplace=True)

  # Remove duplicates
  df.drop_duplicates('PAGE URL', keep='first', inplace=True)
  # df = df.transpose()

  filename = f"Result{ now }.csv"

  logging.info('%s saved sucessfully.', filename)

  file_path = os.path.join(directory,'csvfiles/', filename)
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
  send_html_email(os.getenv(f"{ENV}EMAIL"), f'Newly Discovered Pages - {now}', html_file)


def manual_input_scraper():
  directory = os.path.dirname(os.path.realpath(__file__))
  dicovered_date = ''

  # Instantiate container list
  url_list = []
  discovered_on_list = []
  flag_new_list = []
  domain_list = []
  lowest_price_list = []
  current_url = ''
  current_url_list = []

  # Connect to the database
  db_connection = db_connect()

  # Open and process input list
  with open(f'{directory}/user_input_manual_list.csv', encoding='unicode_escape') as p:
    reader = csv.DictReader(p)
    
    for line in reader:

      try:
        # Loop through the csv file and add to the queue
        url = line['Url']
        child_sku = line["sku"]
        _competitor_product_page = line['Competitor Product Page']
        min_sale_price_manual = line['Miminum Sale Price Manual']
        cost_price = line['Cost Price']
        markup_perc = line['Mark Up Percentage']
        markup_dollar = line['Mark Up Dollar Value']
        beat_price_by_perc = line['Price Beat By Percentage']
        beat_price_by_dollar = line['Price Beat By Dollar Value']

        min_sale_price = ''

        # START - Save User's product info to user_price_action table 
        # Scrape for the competitor current price
        competitor_price = price_scraper(_competitor_product_page)
        
        # Check current Url, reset lowest_price_list if it user product Url changed
        if (current_url != url):
          logging.info('Product URL changed, resetting lowest price list.')
          lowest_price_list = []
          lowest_price_list.append(competitor_price)
          current_url = url
          current_url_list.append(current_url)
        else:
          lowest_price_list.append(competitor_price)

        # Solve for User's minimum sale price
        if (len(min_sale_price_manual)):
          min_sale_price = min_sale_price_manual
        else:
          min_sale_price = calculate_min_sale_price(cost_price, markup_perc, markup_dollar)

        # Solve for the lowest price
        lowest_price = float(get_lowest_price(lowest_price_list))

        # Calculate the Beat By Price
        beat_price_by_result = beat_price_by(lowest_price, beat_price_by_perc, beat_price_by_dollar)

        # Action to take if beat_price_by_result is higher/lower than min_sale_price
        if beat_price_by_result > min_sale_price:
          do_update_price = 'yes'
        else:
          do_update_price = 'no'

        # Check if product already exist
        exist_price_action = check_product_exist_price_action(child_sku, db_connection)

        timestamp = datetime.datetime.now()
        # timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
        # Get the existing competitor price of the user product
        existing_comp_price = get_existing_comp_prices(child_sku, db_connection)

        # # Get the product SKU
        if child_sku == '':
          product_sku = get_product_sku(child_sku, db_connection)
          parent_sku, sku = product_sku
        else:
          product_sku = child_sku
          parent_sku = None
        
        # Store product price in the prices json
        if len(existing_comp_price):
          
          # Parse each JSON string into Python dictionaries
          prices_dicts = [json.loads(json_str) for json_str in existing_comp_price]
          
          # Combine the price dictionaries into one
          combined_prices_dict = {}
          for price_dict in prices_dicts:
            combined_prices_dict.update(price_dict)

          combined_prices_dict[_competitor_product_page] = competitor_price
          prices_json_data = json.dumps(combined_prices_dict)
        else:
          prices = existing_comp_price
          prices[_competitor_product_page] = competitor_price
          prices_json_data = json.dumps(prices)
          
        if exist_price_action == True:
          logging.info('Updating user price action table.')
          # Update user_price_action table
          update_price_action(url, parent_sku, sku, prices_json_data, min_sale_price, lowest_price, beat_price_by_result, do_update_price, timestamp, db_connection)
        else:
          logging.info('Saving to user price action table.')
          # Insert data if not yet in user_price_action table
          insert_price_action(url, parent_sku, sku, prices_json_data, min_sale_price, lowest_price, beat_price_by_result, do_update_price, timestamp, db_connection)
        # END of task

        # Extract domain
        domain = extract_domain(url)

        #Function to check if exist in db, if not save it to DB
        url_flag = user_check_page_exist(child_sku, db_connection)
        
        if url_flag == 'New':

          dicovered_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

          # Append to array containers for CSV generation
          url_list.append(url)
          discovered_on_list.append(dicovered_date)
          flag_new_list.append("New")
          domain_list.append(f'https://www.{domain}')

        # Cross-check DB to see the Status Code
        # Only cross-check what's in the queue to save resources
        old_url_history = []

        url_data = user_check_old_urls(url, db_connection)

        if (url_data):
          old_url_history.append(url_data)

        # Compare Newly discovered with the Old URL in DB 
        # Update DB if new found Url is a redirect
        if (old_url_history):

          for oldurl_item in old_url_history:

            for item in oldurl_item:

              logging.info("destination - %s", item['destination'])

              if item['destination'] in url_list:

                update_db(item['url'], item['status'], item['destination'], db_connection)
                url_list.remove(item['destination'])

      except:
        logging.info('SOMETHING WENT WRONG...')
        pass
    
    # Save scraped URLs to a CSV file
    if (url_list):
      user_result_file(url_list, domain_list)
    else:
      logging.info('No output file generated.')

    # Processed remaining Url in List and save to DB
    # Remove duplicates in case entries from sitemaps appear more than once
    url_list = list(OrderedDict.fromkeys(url_list))
    for url_item in url_list:
      user_save_pages_to_db(url_item, dicovered_date, db_connection)

    # Notify user for price actions through email
    price_action_notify_user(current_url_list, db_connection)

  # Check DB connection and established connection if not connected
  if db_connection.is_connected():
    db_connection.close()
    logging.info("MySQL connection is closed.")