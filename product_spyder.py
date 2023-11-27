from usp.tree import sitemap_tree_for_homepage
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
import logging

# Load helpers
from helpers.db_connect import db_connect
from helpers.urlchecker import check_old_urls, update_db
from helpers.substring_processor import extract_domain
from helpers.main_error import email_error_report
from helpers.main_email import *
from helpers.price_scraper import price_scraper
from users.user_scrape_products import user_scrape_products
from users.user_manual_input_scrape import manual_input_scraper
from users.scrape_google_for_competitors import scrape_google_for_competitors

# Use to check if user uploads products manually
from manual_product_upload.manual_product_upload import manual_product_upload

load_dotenv()

# Use this to change between "DEV" and "PROD" .env variables
ENV = os.getenv("PROD")

# Check if page exist in the DB
def check_page_exist(page, db_connection):
  
  logging.info(f"Checking - {page}")
  
  # Check DB connection and established connection if not connected
  if db_connection.is_connected():
    pass
  else:
    db_connection = db_connect()

  # Identify if page already exist, if not save to database
  exist_query=f"SELECT EXISTS(SELECT 1 from competitor_pages WHERE page_url LIKE '%{page}%')"

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

  logging.info(f"Flag: {flag}")

  return flag

def save_pages_to_db(url, date, db_connection):

  try:

    # Extract domain
    domain = extract_domain(url)

    # Check DB connection and established connection if not connected
    if db_connection.is_connected():
      pass
    else:
      db_connection = db_connect()

    save_url_query = f"INSERT INTO competitor_pages(page_url, site_url, discovered, flag) VALUES ('{url}', 'https://www.{domain}', '{date}', 'New' )"

    mycursor = db_connection.cursor()

    mycursor.execute(save_url_query)

    db_connection.commit()
    logging.info("%s Record inserted successfully into competitor_pages table", mycursor.rowcount)
    mycursor.close()

  except mysql.connector.Error as error:
    logging.info("Failed to insert record into competitor_pages table %s", error)


# Process Invalid sitemaps
def error_sitemaps(invalid_sitemaps_url, invalid_sitmap_status_list, invalid_sitemap_reason):
  directory = os.path.dirname(os.path.realpath(__file__))
  now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')

  logging.info('Saving to a CSV file...\n')
  logging.info(f'Url: {len(invalid_sitemaps_url)}, Status: {len(invalid_sitmap_status_list)}, Reason: {len(invalid_sitemap_reason)}\n')
  data = {"Url": invalid_sitemaps_url, "Status": invalid_sitmap_status_list, "Reason": invalid_sitemap_reason}
  # df = pd.DataFrame.from_dict(data, orient='index')
  df = pd.DataFrame(data)

  # Drop empty Urls
  df['Url'].replace('', np.nan, inplace=True)
  df.dropna(subset=['Url'], inplace=True)

  # Remove duplicates
  df.drop_duplicates('Url', keep='first', inplace=True)
  # df = df.transpose()

  filename = f"PendingQueue.csv"

  logging.info('%s saved sucessfully.', filename)

  file_path = os.path.join(directory,'pending_queue/', filename)
  df.to_csv(file_path, index=False)

  # Generate an HTML version of the CSV
  a = pd.read_csv(file_path)

  # to save as html file named as "Table"
  a.to_html("Table.htm")

  # assign it to a variable (string)
  msg_head = "<html><head><style> table {border-collapse: collapse; width: 100%;} th, td {text-align: left; padding: 10px; border: 1px solid #ddd;} tr:nth-child(even){background-color: #f2f2f2} th {background-color: #31b821; color: white;} a {background-color: transparent; text-decoration: none;}</style></head><body><p>"
  msg_end = "</p></body></html>"
  html_file = msg_head + a.to_html() + msg_end

  if (invalid_sitemaps_url):
    # Send the generated file to the customer
    send_html_email(os.getenv(f"{ENV}EMAIL"), f'Invalid Sitemaps - {now}', html_file)

# Generate CSV file for inspection
def inspection_sitemap(for_inspection, for_inspection_sitmap_status_list, for_inspection_sitemap_reason):
  directory = os.path.dirname(os.path.realpath(__file__))
  now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')

  logging.info('Saving to a CSV file...\n')
  logging.info(f'Url: {len(for_inspection)}, Status: {len(for_inspection_sitmap_status_list)}, Reason: {len(for_inspection_sitemap_reason)}\n')
  data = {"Url": for_inspection, "Status": for_inspection_sitmap_status_list, "Reason": for_inspection_sitemap_reason}
  # df = pd.DataFrame.from_dict(data, orient='index')
  df = pd.DataFrame(data)

  # Drop empty Urls
  df['Url'].replace('', np.nan, inplace=True)
  df.dropna(subset=['Url'], inplace=True)

  # Remove duplicates
  df.drop_duplicates('Url', keep='first', inplace=True)
  # df = df.transpose()

  filename = f"Inspection_{now}.csv"

  logging.info('%s saved sucessfully.', filename)

  file_path = os.path.join(directory,'inspection/', filename)
  df.to_csv(file_path, index=False)

  # Generate an HTML version of the CSV
  a = pd.read_csv(file_path)

  # to save as html file named as "Table"
  a.to_html("Table.htm")

  # assign it to a variable (string)
  msg_head = "<html><head><style> table {border-collapse: collapse; width: 100%;} th, td {text-align: left; padding: 10px; border: 1px solid #ddd;} tr:nth-child(even){background-color: #f2f2f2} th {background-color: #31b821; color: white;} a {background-color: transparent; text-decoration: none;}</style></head><body><p>"
  msg_end = "</p></body></html>"
  html_file = msg_head + a.to_html() + msg_end

  if (for_inspection):
    # Send the generated file to the customer
    send_html_email(os.getenv(f"{ENV}EMAIL"), f'Sitemaps for Inspection - {now}', html_file)

def pending_queue_on_exception(all_queue_urls):
  directory = os.path.dirname(os.path.realpath(__file__))

  logging.info('Generating a Pending Queue file. Saving to a CSV file.')
  logging.info('Url: %s', len(all_queue_urls))
  data = {"Url": all_queue_urls}
  # df = pd.DataFrame.from_dict(data, orient='index')
  df = pd.DataFrame(data)

  # Drop empty Urls
  df['Url'].replace('', np.nan, inplace=True)
  df.dropna(subset=['Url'], inplace=True)
  
  # Remove duplicates
  df.drop_duplicates('Url', keep='first', inplace=True)
  # df = df.transpose()

  filename = f"PendingQueue.csv"

  logging.info('%s saved sucessfully.', filename)

  file_path = os.path.join(directory,'pending_queue/', filename)
  df.to_csv(file_path, index=False)

# Main Function - Crawl sitemaps and save urls
def spyder():
  # time_start = datetime.datetime.now().replace(microsecond=0)
  directory = os.path.dirname(os.path.realpath(__file__))
  dicovered_date = ''

  # Instantiate array containers
  url_list = []
  domain_list = []
  discovered_on_list = []
  flag_new_list = []
  all_queue_urls = []
  # negative_pages = ["?attachment", "/blog", "/pages/", "/collections/", "/category/", "/product-tag/", "/post", "/contact", "/testimonials", "/product-category/", "/disclaimer", "/news"]
  negative_pages = ["?attachment"]



  # Variables for error/invalid sitemaps
  invalid_sitemaps_url = []
  invalid_sitmap_status_list = []
  invalid_sitemap_reason = []
  already_processed = [] # Use for checking if sitemap is from other day

  # Variables for for-inspection sitemaps
  for_inspection = [] # Use to generate for Inspection CSV
  for_inspection_sitmap_status_list = []
  for_inspection_sitemap_reason = []

  # Connect to the database
  db_connection = db_connect()

  try:
  
    # Check if a Pending Queue file exist
    pending_queue_file_exist = exists(os.path.join(directory,'pending_queue/', f'PendingQueue.csv'))

    if (pending_queue_file_exist):
      logging.info('Checking for pending queue.')
      # Process PendingQueue from errors and add it to the current queue
      with open(f'{directory}/pending_queue/PendingQueue.csv', encoding='unicode_escape') as p:
        reader = csv.DictReader(p)
        
        for line in reader:

          try:
            # Loop through the csv file and add to the queue
            url = line['Url']
            all_queue_urls.append(url)
            already_processed.append(url)

          except:
            # catch error
            pass

      p.close()

    else:
      logging.info('Pending queue file does not exist.')

    # Process Fresh Current Queue and append it to the PendingQueue
    # Check if a Pending Queue file exist
    current_queue_file_exist = exists(os.path.join(directory, f'input_urls.csv'))
    if (current_queue_file_exist):
      logging.info('Processing todays queue.')
      with open(f'{directory}/input_urls.csv', encoding='unicode_escape') as c:
        reader = csv.DictReader(c)
        
        for line in reader:

          try:

            # Loop through the csv file and add to the queue
            url = line['Url']
            all_queue_urls.append(url)

          except:
            pass

      c.close()

    else:
      logging.info('Current queue file does not exist.')
    
    is_use_sitemap_parser = False #This option will be required User Action. Whether to use Sitemap parser or manual input of Competitor product pages.
    
    # Remove duplicates
    all_queue_urls = list(OrderedDict.fromkeys(all_queue_urls))
    for url in all_queue_urls:
      
      if is_use_sitemap_parser == True: # This will run the Sitemap Parser if user wanted to run the parser
        
        try:
          
          logging.info('Now processing sitemap: %s', url)

          # Instantiate Sitemap Parser
          tree = sitemap_tree_for_homepage(url)

          # Check the sitemap status
          status = type(tree.sub_sitemaps[0]).__name__
          logging.info('Sitemap is %s status.', status)
          
          if (status == 'IndexRobotsTxtSitemap'): # If valid sitemap, extract the pages
            
            # all_pages() returns an Iterator
            for page in tree.all_pages():

              is_negative_page = False

              # Check if page is a negative URL
              for negative_url in negative_pages:

                if negative_url in page.url:
                  is_negative_page = True

              if (is_negative_page != True):
                # Extract domain
                domain = extract_domain(page.url)

                #Function to check if exist in db, if not save it to DB
                url_flag = check_page_exist(page.url, db_connection)
                
                if url_flag == 'New':

                  dicovered_date = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')

                  # Append to array containers for CSV generation
                  url_list.append(page.url)
                  discovered_on_list.append(dicovered_date)
                  flag_new_list.append("New")
                  domain_list.append(f'https://www.{domain}')

          else: # If sitemap is invalid save to a csv
            
            # Skip sitemap if it was from the recent queue
            if (tree.url in already_processed):

              # Add the Url for inspection in the Inspection_{date}.csv if it failed again
              logging.info('Adding sitemap for inspection.')
              for_inspection.append(tree.url)
              for_inspection_sitmap_status_list.append(status)
              for_inspection_sitemap_reason.append(tree.sub_sitemaps[0].reason)

              pass

            else:

              # Add the Url for Pending Queue if failed the first time
              logging.info('Sitemap first time invalid, adding to pending queue.')
              invalid_sitemaps_url.append(tree.url)
              invalid_sitmap_status_list.append(status)
              invalid_sitemap_reason.append(tree.sub_sitemaps[0].reason)

        except:
          pass

      else: # If user opts to manual upload competitor pages
        is_negative_page = False

        # Check if page is a negative URL
        for negative_url in negative_pages:

          if negative_url in url:
            is_negative_page = True

        if (is_negative_page != True):
          # Extract domain
          domain = extract_domain(url)

          #Function to check if exist in db, if not save it to DB
          url_flag = check_page_exist(url, db_connection)
          
          if url_flag == 'New':

            dicovered_date = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')

            # Append to array containers for CSV generation
            url_list.append(url)
            discovered_on_list.append(dicovered_date)
            flag_new_list.append("New")
            domain_list.append(f'https://www.{domain}')


    # Save first time invalid sitemaps to PendingQueue.csv
    if (invalid_sitemaps_url):
      error_sitemaps(invalid_sitemaps_url, invalid_sitmap_status_list, invalid_sitemap_reason)
    else:
      # Generate empty PendingQueue.csv
      error_sitemaps([], [], [])

    # Save 2nd time invalid sitemaps to Inspection_{date}.csv
    if (for_inspection):
      inspection_sitemap(for_inspection, for_inspection_sitmap_status_list, for_inspection_sitemap_reason)

    now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')

    # Cross-check DB to see the Status Code
    # Only cross-check what's in the queue to save resources
    old_url_history = []

    for url in all_queue_urls:
      
      # Extract domain substring
      domain = extract_domain(url)

      url_data = check_old_urls(url, db_connection)

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

    # Save scraped URLs to a CSV file
    if (url_list):
      logging.info('Saving to a CSV file.')
      logging.info('SITE URL: %s, URL: %s', len(domain_list), len(url_list))
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

    else:
      logging.info('No output file generated.')

    # Processed remaining Url in List and save to DB
    # Remove duplicates in case entries from sitemaps appear more than once
    url_list = list(OrderedDict.fromkeys(url_list))
    for url_item in url_list:
      save_pages_to_db(url_item, dicovered_date, db_connection)
  
  # Catch all errors and create a traceback and send to Admin email
  except Exception as err:

    now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    
    logging.error('Cannot continue, an unexpected error occured. A traceback was sent to the Admin email address.')
    trace = traceback.format_exc()          
    email_error_report(subject=f"Product Spyder API Error - {now}",error=err,trace=trace)
    logging.info('%s', err)
    logging.info('%s', trace)

    # Create a PendingQueue.csv on Exception
    pending_queue_on_exception(all_queue_urls)

  try:
    # Check DB connection and established connection if not connected
    if db_connection.is_connected():
      db_connection.close()
      logging.info("MySQL connection is closed.")
    
    # CHECK IF USER WANTED TO CHECK COMPETITOR PRICES
    is_scrape_competitor_prices = False
    with open(f"input_competitor_scrape_price.csv", encoding="unicode_escape") as f:
      reader = csv.DictReader(f)

      for line in reader:
        if (bool(line['Url'])):
          is_scrape_competitor_prices = True
          break;
        
    if is_scrape_competitor_prices == True: # SCRAPE COMPETITOR PRICES USING input_competitor_scrape_price.csv
      price_scraper()

    # THIS WILL SCRAPE USERS PRODUCT INDIVIDUAL PAGE WITH minimum_sale_price, mark_up, price_beat_by, etc.
    is_user_manual_input = False
    with open(f'{directory}/users/user_input_manual_list.csv', encoding='unicode_escape') as p:
      reader = csv.DictReader(p)
      
      for line in reader:
        if (bool(line['Url'])):
          is_user_manual_input = True
          break;
    
    if (is_user_manual_input == True): # THIS WILL SCRAPE USERS PRODUCT INDIVIDUAL PAGE WITH minimum_sale_price, mark_up, price_beat_by, etc.
      logging.info("Now processing user's product list.")
      manual_input_scraper()
    else: # This will scrape prices site-wide using the input_urls.csv
      user_scrape_products()

    # CHECK IF USER WANTS TO UPLOAD PRODUCTS MANUALLY
    is_user_manual_upload_product = False
    with open(f'{directory}/manual_product_upload/input_manual_product_upload.csv', encoding='unicode_escape') as p:
      reader = csv.DictReader(p)
      
      for line in reader:
        if (bool(line['Link'])):
          is_user_manual_upload_product = True
          break;
    
    if (is_user_manual_upload_product == True): # THIS WILL UPLOAD USERS' PRODUCT LIST
      logging.info("Now uploading user's product list.")
      manual_product_upload()

  # Catch all errors and create a traceback and send to Admin email
  except Exception as err:

    now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    
    logging.error('Cannot continue, an unexpected error occured. A traceback was sent to the Admin email address.')
    trace = traceback.format_exc()          
    email_error_report(subject=f"Product Spyder API Error - {now}",error=err,trace=trace)
    logging.info('%s', err)
    logging.info('%s', trace)

  logging.info('The task completed.')