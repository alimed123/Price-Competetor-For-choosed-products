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
import logging

from main_neto_api import NETO_API_URL
from main_neto_api import NETO_API_HEADERS_JSON_GETITEM
from main_neto_api import NETO_API_HEADERS_XML_UPDATEITEM
# from main_file import write_file
from pprint import pprint
# from common import *
from urllib.parse import unquote
import unicodedata
import traceback
from bs4 import BeautifulSoup
from string import Template
from dotenv import load_dotenv

from helpers.main_email import send_email

load_dotenv()

# Use this to change between "DEV" and "PROD" .env variables
ENV = os.getenv("PROD")

#Misc42: GSName    
#Misc43: GSImageURL  
#Misc44: GSDescription
#Misc45: GSProductType  
#Misc46: GSProductCategory  
#Misc47: GSShipFree  

# json_get_all_acc = """
# {
#   "Filter": {
#     "CategoryID":"98",    
#     "Page":"0",
#     "Limit":"100000",
#     "Approved":"True",
#     "IsActive":"True",
#     "OrderBy":"Enumeration",
#     "SKU":"RB-ILLUMINATE-i360-V"
#     "OutputSelector":["InventoryID", "SKU", "PromotionPrice", "Misc42", "Misc44", "Misc43", "Misc45", "Misc46", "Misc47", "Misc41", "ParentSKU", "Name", "Description", "Brand"]
#     }
# }"""

# xml_update_template = Template(""" 
#    <Item>
#     <SKU>$SKU</SKU>             
#     <Misc47>$GSShipFree</Misc47>
#     <Misc46>$GSProductCategory</Misc46> 
#     <Misc45>$GSProductType</Misc45>
#     <Misc42>$GSName</Misc42>
#     <Misc44>$GSDescription</Misc44>
#     <Misc43>$GSImageURL</Misc43> 
#    </Item>
# """)

json_get_all_acc = """
{
  "Filter": {
    "CategoryID":"98",    
    "Page":"0",
    "Limit":"100000",
    "Approved":"True",
    "IsActive":"True",
    "OrderBy":"Enumeration",
    "ParentSKU":"K2F-BAR-FOLD-MOTOR-32-V",
    "OutputSelector":["ItemURL", "InventoryID", "SKU", "PromotionPrice", "ParentSKU", "Name", "Brand", "DefaultPrice", "PriceGroups", "Misc41"]
    }
}"""
                               
xml_update_template = Template(""" 
   <Item>
    <SKU>$SKU</SKU>             
    <PromotionPrice>$PromotionPrice</PromotionPrice>
   </Item>
""")


parent_only_list = []
accessories_list = []
website_domain = "https://www.kayaks2fish.com/"

# Todo get the promotional_price from DB
# def get_promotional_price():


def fetch_api_create_parent_list():
  global parent_only_list
  global accessories_list

  try:
    all_acc_dict = (requests.post(url = NETO_API_URL, data = json_get_all_acc, headers = NETO_API_HEADERS_JSON_GETITEM)).json() 
          
    accessories_list = all_acc_dict['Item'] #main data is under "item" key
    # write_file("temp_accessories_list.txt",accessories_list)
    row = ''
    f = open("temp_accessories_list.txt", "w+")
    for key, value in enumerate(accessories_list):
        row = row + f"{value}, "
        f.write(row)
    f.close()
    # csv_file = open('/home/orcacorp/public_html/NetoGoogleShoppingData/k2f_accessories_raw_data.csv', 'w')    
    # csv_file.write(str(accessories_list))
    # csv_file.close()
    # pause()
    
    #create parent only list
    for item in accessories_list:
        if item['ParentSKU'] == '' and item["Misc41"] != 'n': #exclude child skus and only IsGoogleShopping = Yes
            parent_only_list.append(item)
    # write_file("temp_parent_only_list.txt",parent_only_list)
    g = open("temp_parent_only_list.txt", "w+")
    for key, value in enumerate(parent_only_list):
        row = row + f"{value}, "
        g.write(row)
    g.close()
    logging.info('%s', accessories_list)
    # pause()

  except Exception as err:        
    send_email(os.getenv(f"{ENV}EMAIL"),'Error: K2F Google Shopping Field - Failed Neto API Fetch', err)
    traceback.print_exc()

def prepare_data():
  global parent_only_list
  global accessories_list   

  for acc_item in accessories_list:        

    acc_item["PromotionPrice"] = "74.95"

def upload_to_neto():
  global parent_only_list
  # write_file("temp_parent_only_list_final.txt",parent_only_list)
  row = ''
  f = open("temp_accessories_list.txt", "w+")
  for key, value in enumerate(parent_only_list):
    row = row + f"{value}, "
    f.write(row)
  f.close()
  xml_string = ""

  #add all items from list into one API request
  for parent_item in parent_only_list:
    xml_string = xml_string + str(xml_update_template.substitute(**parent_item)) #converts dict into XML template 
  
  #create final string
  xml_string_final = f"<?xml version=\"1.0\" encoding=\"utf-8\"?> <UpdateItem> {xml_string} </UpdateItem>"
  # logging.info('%s', xml_string_final)
  # xml_string_final = xml_string_final.encode("utf-8")
  xml_string_final = xml_string_final
  logging.info('%s', xml_string_final)

  #API post
  # try:
  #   update_crossell_xml_response = requests.post(url = NETO_API_URL, data = xml_string_final, headers = NETO_API_HEADERS_XML_UPDATEITEM)
  #   # logging.info('%s', update_crossell_xml_response.text)
      
  # except Exception as err:
  #   send_email(os.getenv("ORCAEMAIL"),'Error: K2F Google Shopping Field - Neto API Post Failed', update_crossell_xml_response.text)

def main():
  try:
    fetch_api_create_parent_list()
    prepare_data()
    # create_shopping_feed()#? Dont need it since we are now updating neto API
    upload_to_neto()
  except Exception as err:        
    send_email(os.getenv(f"{ENV}EMAIL"),'Error: K2F Google Shopping Field - Something Went Wrong', traceback.format_exc())
    traceback.print_exc()
    logging.info('%s', err)
if __name__ == "__main__":
  main()