from threading import Thread
from time import perf_counter
import traceback
import datetime
import sys
import logging
import concurrent.futures
import os
import csv
import mysql.connector

# Import tasks functions
from users.scrape_google_for_competitors import *
from users.neto_gmc import *

# Import helpers
from helpers.db_connect import db_connect,is_connected
from helpers.main_error import email_error_report

# Logging config
logging.basicConfig(
  encoding='utf-8', 
  level=logging.DEBUG, 
  format='%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] - [%(threadName)s] - %(message)s', 
  datefmt='%m/%d/%Y %I:%M:%S %p',
  handlers=[
    logging.FileHandler('runtimelogs.log'),
    logging.StreamHandler(sys.stdout)
  ]
)

# scrape_google_for_competitors THREAD POOL
def process_scrape_google_for_competitors(scrape_google_for_competitors_filename, num_threads):
    df = pd.read_excel(scrape_google_for_competitors_filename,skiprows=1)
    df = df.fillna("")
    df = df.astype(str)

    # Create a ThreadPoolExecutor with a maximum of num_threads workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
      # Submit tasks for each row
      futures = [executor.submit(scrape_google_for_competitors, row.tolist()) for index, row in df.iterrows()]

      # Wait for all tasks to complete
      concurrent.futures.wait(futures)

if __name__ == "__main__":
  try:
    start_time = perf_counter()
    num_threads = 8  # Adjust as needed
    excel_file = [f for f in os.listdir("Source") if f.endswith('.xlsx')][0]

    scrape_google_for_competitors_filename = os.path.join("Source", excel_file)


    db_connection = db_connect()

    # scrape_google_for_competitors THREAD POOL FUNCTION CALL
    # THIS IS THE FUNCTION FOR TRACKING YOUR PRODUCTS AND DETERMINE IT'S COMPETITORS
    process_scrape_google_for_competitors(scrape_google_for_competitors_filename, num_threads)
    generate_reports_scrape_google_for_competitors(db_connection)
    main_gmc_neto_updater(db_connection) # THIS WILL UPDATE THE ONLINE SHOPS (NETO, GOOGLE MERCHANT CENTER)

    # THIS FUNCTION CALL IS USE TO PERFORM SEVERAL TASK FUNCTIONS FOR THE COMPETITORS AND USERS
    # - SCRAPE COMPETITORS/USER'S WEBSITES USING USP (ULTIMATE SITEMAP PARSER)
    # - UPLOAD USER'S PRODUCTS
    # JUST UNCOMMENT THIS ONE AND SUPPLY THE NECESSARY CSV INPUTS FOR EACH FUNCTION
    # spyder()

    # Check DB connection, closed it at the end of the application run
    if is_connected(db_connection):
      db_connection.close()
      logging.info("MySQL connection is closed.")

    end_time = perf_counter()
    runtime = f'{end_time- start_time :0.2f}'
    logging.info('It took %s second(s) to complete.', runtime)

  except Exception as err:
    logging.error("[!]: ERROR FETCHED")
    logging.info("[+]: SENDING TRACEBACK EMAIL ERROR")
    # SENDING ERROR EMAIL
    now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    email_error_report(subject=f"Product Spyder API Fetch Error - {now}")
    logging.info("[+]: DONE SUCCESSFULLY!")
    trace_err = traceback.format_exc()
    logging.info('%s', err)
    logging.info('%s', trace_err)
  
# Important Notes: https://stackoverflow.com/questions/44950893/processing-huge-csv-file-using-python-and-multithreading