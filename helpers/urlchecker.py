import pandas as pd
import numpy as np
import random
import datetime
import sys
import os
import os.path
import time
import csv
import re
import mysql.connector
from dotenv import load_dotenv
import requests
from collections import OrderedDict
import logging

# Load helpers
from helpers.db_connect import db_connect
from helpers.user_agent import user_agent
# from helpers.proxies import get_proxies
from helpers.main_email import send_html_email

load_dotenv()

# Use this to change between "DEV" and "PROD" .env variables
ENV = os.getenv("PROD")

def update_db(url, status, destination, db_connection):
  
  try:
    # Check DB connection and established connection if not connected
    if db_connection.is_connected():
      pass
    else:
      db_connection = db_connect()

    update_row_query = ''
    
    # Check the http status and perform the necessary task
    match status:
      case 301:
        now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
        update_row_query = f'UPDATE competitor_pages SET page_url="{destination}", discovered="{now}", status={status}, flag="Redirect" WHERE page_url="{url}"'
      case 302:
        now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
        update_row_query = f'UPDATE competitor_pages SET page_url="{destination}", discovered="{now}", status={status}, flag="Redirect" WHERE page_url="{url}"'
      case _:
        now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
        update_row_query = f'UPDATE competitor_pages SET discovered="{now}", status={status}, flag="Removed" WHERE page_url="{url}"'
    
    mycursor = db_connection.cursor()
    mycursor.execute(update_row_query)
    db_connection.commit()
    logging.info("%s Record updated successfully into competitor_pages table", mycursor.rowcount)
    mycursor.close()

  except mysql.connector.Error as error:
    logging.info("Failed to update record into competitor_pages table {}".format(error))

def check_old_urls(query, db_connection):

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
  if db_connection.is_connected():
    pass
  else:
    db_connection = db_connect()

  # If you wanted to test URL check, just change the query variable appropriately
  # Example if you just want to test all urls under example.com, you can use '%example.com%'
  get_urls_query = f"SELECT page_url FROM competitor_pages WHERE page_url LIKE '%{query}%'"

  mycursor = db_connection.cursor()
  mycursor.execute(get_urls_query)
  pages = mycursor.fetchall()

  for row in pages:
    url_list.append(row[0])

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
    logging.info('Saving to a CSV file.')
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

    file_path = os.path.join(parent_dir,'check_url_status/', filename)
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