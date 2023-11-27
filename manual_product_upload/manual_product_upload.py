import pandas as pd
import numpy as np
import datetime
import sys
import os
import os.path
import csv
import mysql.connector
from dotenv import load_dotenv
import requests
import json
import logging

# Load helpers
from helpers.db_connect import db_connect
from helpers.substring_processor import *
#from main_neto_api import NETO_API_URL
#from main_neto_api import NETO_API_HEADERS_JSON_GETITEM

load_dotenv()

# Use this to change between "DEV" and "PROD" .env variables
ENV = os.getenv("PROD")

def manual_product_upload():
  directory = os.path.dirname(os.path.realpath(__file__))
  now = datetime.datetime.now().strftime("%Y%m%d-%Hh%M")

  # Established DB Connection
  db_connection = db_connect()

  with open(
    f"{directory}/input_manual_product_upload.csv",
    encoding="unicode_escape",
  ) as p:
    reader = csv.DictReader(p)

    for line in reader:
      brand = line["Brand"]
      mpn = line["MPN"]
      upc = line["UPC"]
      parent_sku = line["Parent_sku"]
      sku = line["sku"]
      condition = line["Condition"]
      availability = line["Availability"]
      identifier_exists = line["Identifier_exists"]
      quantity = line["Quantity"]
      sale_price = line["Sale_Price"]
      price = line["Price"]
      product_id = line["ID"]
      link = line["Link"]
      title = line["Title"]
      image_link = line["Image_Link"]
      description = line["Description"]
      product_type = line["Product_Type"]
      google_product_category = line["Google_Product_Category"]
      shipping_label = line["Shipping_Label"]
      shipping_weight = line["Shipping_Weight"]
      gtin = line["GTIN"]
      promotion_id = line["Promotion_ID"]

      # Process strings to remove letters/special characters and convert
      if sale_price:
        sale_price = float(remove_special_characters_and_letters(sale_price))
      else:
        sale_price = None
      
      if price:
        price = float(remove_special_characters_and_letters(price))
      else:
        price = None
      
      if shipping_weight:
        shipping_weight = float(remove_special_characters_and_letters(shipping_weight))
      else:
        shipping_weight = None

      # FETCH NETO FOR ID IF USER DID NOT SUPPLY ID
      if product_id == '':
        logging.info('Did not supply product ID for %s, now fetching ID from NETO', link)
        json_get_all_acc = {
          "Filter": {
            "SKU":[sku],
            "Page":"0",
            "Limit":"100000",
            "Approved":"True",
            "IsActive":"True",
            "OrderBy":"Enumeration",
            "OutputSelector":["ItemURL", "SKU", "ParentSKU", "Name", "ID"]
            }
        }
        json_string = json.dumps(json_get_all_acc)
        response = (requests.post(url = NETO_API_URL, data = json_string, headers = NETO_API_HEADERS_JSON_GETITEM)).json()
        fetched_id_list = response['Item']

        for item in fetched_id_list:
          if item["ID"]:
            product_id = int(item["ID"])
            
        logging.info('ID found: %s of type %s', product_id, type(product_id))

      site_url = extract_domain(link)

      try:
        if (sku == ''): # If row is a Parent Product SKU
          insert_product_query = """INSERT INTO user_product_pages(
            brand, 
            mpn,
            upc,
            parent_sku,
            product_condition, 
            availability, 
            identifier_exists, 
            quantity, 
            sale_price, 
            price,
            site_url,
            id, 
            page_url, 
            title, 
            image_link, 
            description, 
            product_type, 
            google_product_category, 
            shipping_label, 
            shipping_weight, 
            gtin, 
            promotion_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE 
            brand = VALUES(brand), 
            mpn = VALUES(mpn),
            upc = VALUES(upc),
            parent_sku = VALUES(parent_sku),
            product_condition = VALUES(product_condition), 
            availability = VALUES(availability), 
            identifier_exists = VALUES(identifier_exists), 
            quantity = VALUES(quantity), 
            sale_price = VALUES(sale_price), 
            price = VALUES(price),
            site_url = VALUES(site_url),
            id = VALUES(id), 
            page_url = VALUES(page_url), 
            title = VALUES(title), 
            image_link = VALUES(image_link), 
            description = VALUES(description), 
            product_type = VALUES(product_type), 
            google_product_category = VALUES(google_product_category), 
            shipping_label = VALUES(shipping_label), 
            shipping_weight = VALUES(shipping_weight), 
            gtin = VALUES(gtin), 
            promotion_id = VALUES(promotion_id)"""

          values = (
              brand,
              mpn,
              upc,
              parent_sku,
              condition,
              availability,
              identifier_exists,
              quantity,
              sale_price,
              price,
              site_url,
              product_id,
              link,
              title,
              image_link,
              description,
              product_type,
              google_product_category,
              shipping_label,
              shipping_weight,
              gtin,
              promotion_id
          )
        else: # If row is a Child Product SKU
          insert_product_query = """INSERT INTO user_product_pages(
              brand, 
              mpn,
              upc,
              parent_sku,
              sku,
              product_condition, 
              availability, 
              identifier_exists, 
              quantity, 
              sale_price, 
              price,
              site_url,
              id, 
              page_url, 
              title, 
              image_link, 
              description, 
              product_type, 
              google_product_category, 
              shipping_label, 
              shipping_weight, 
              gtin, 
              promotion_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
              ON DUPLICATE KEY UPDATE 
              brand = VALUES(brand), 
              mpn = VALUES(mpn), 
              upc = VALUES(upc), 
              parent_sku = VALUES(parent_sku), 
              sku = VALUES(sku), 
              product_condition = VALUES(product_condition), 
              availability = VALUES(availability), 
              identifier_exists = VALUES(identifier_exists), 
              quantity = VALUES(quantity), 
              sale_price = VALUES(sale_price), 
              price = VALUES(price), 
              site_url = VALUES(site_url), 
              id = VALUES(id), 
              page_url = VALUES(page_url), 
              title = VALUES(title), 
              image_link = VALUES(image_link), 
              description = VALUES(description), 
              product_type = VALUES(product_type), 
              google_product_category = VALUES(google_product_category), 
              shipping_label = VALUES(shipping_label), 
              shipping_weight = VALUES(shipping_weight), 
              gtin = VALUES(gtin), 
              promotion_id = VALUES(promotion_id)"""

          values = (
              brand,
              mpn,
              upc,
              parent_sku,
              sku,
              condition,
              availability,
              identifier_exists,
              quantity,
              sale_price,
              price,
              site_url,
              product_id,
              link,
              title,
              image_link,
              description,
              product_type,
              google_product_category,
              shipping_label,
              shipping_weight,
              gtin,
              promotion_id
          )

        mycursor = db_connection.cursor()

        mycursor.execute(insert_product_query, values)

        db_connection.commit()
        logging.info("%s Record saved successfully into user_product_pages table", mycursor.rowcount)

      except mysql.connector.Error as error:
        logging.error("Failed to save record from user_product_pages table {}\n".format(error))

  mycursor.close()
