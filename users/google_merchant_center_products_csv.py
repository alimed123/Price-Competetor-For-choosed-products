#This code will be used to add products from csv file
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_merchant_center import create_gservice
import pandas as pd
import logging
import sys

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

#Reading csv file
def read_csv(file_path):
    #Creating dataframe
    try:
        df_products=pd.read_csv(file_path)
        return df_products
    except FileNotFoundError as e:
        logging.info("File not found\n Please check CSV ")
    

def insert_csv_gmc(product):
    logging.info("Creating google service")
    merchant_id,service= create_gservice()
    logging.info("Google service created\n")
    logging.info("Inserting products from CSV file started :\n")
    for i in range(len(product)):
        logging.info(f"inserting product : {product['Title'][i]} \n")
        body = {
            'title': product["Title"][i],
            'offerId': product["ID"][i],
            'description': product["Description"][i],
            'channel': 'online',
            'link': product["Link"][i],
            'contentLanguage': 'en',
            'targetCountry': 'AU',
            'feedLabel': 'AU',
            'imageLink': product["Image_Link"][i],
            'availability': product["Availability"][i],
            'brand': product["Brand"][i],
            'condition': product["Condition"][i],
            'googleProductCategory': product["Google_Product_Category"][i],
            'gtin': product["GTIN"][i],
            'mpn': product["MPN"][i],
            'price': {
                'value': product["Price"][i].split(" ")[0],
                'currency': product["Price"][i].split(" ")[1]
            },
            'productTypes': product["Product_Type"][i],
            'salePrice': {
                'value': product["Sale_Price"][i].split(" ")[0],
                'currency': product["Sale_Price"][i].split(" ")[1]
            },
            'shippingWeight': {
                'value': product["Shipping_Weight"][i].split(" ")[0],
                'unit': product["Shipping_Weight"][i].split(" ")[1]
            },
            'shippingLabel': product["Shipping_Label"][i]
        }
        logging.info("product body :\n")
        logging.info(body)
        product = service.products().insert(merchantId=merchant_id, body=body).execute()
        logging.info(f"product inserted: {product['id']}")