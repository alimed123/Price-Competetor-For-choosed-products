from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging
import sys
import os
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

#Create GMC service api
def create_gservice():
    # Path to your service account key file
    key_path = os.path.abspath('.')+'\merchant-center.json'

    # Your Google Merchant Center account ID
    merchant_id = '113145660'

    # Load the credentials from the service account key file
    credentials = service_account.Credentials.from_service_account_file(
        key_path,
        scopes=['https://www.googleapis.com/auth/content']
    )

    # Build the service client
    service = build('content', 'v2.1', credentials=credentials)
    
    logging.info("google service api created")
    return service,merchant_id

#GMC fetching products
def fetch_products():
    service,merchant_id= create_gservice()
    total_products=[]
    page_token=None

    print("**************search for products on content api feed**************")

    while True:
        products=service.products().list(merchantId=merchant_id,maxResults=250,pageToken=page_token).execute()
        for i in products["resources"]:
            if i["source"] == "api":
                print(f"product found :{i['id']}")
                total_products.append(i)
        if "nextPageToken" in products.keys():
            page_token=products["nextPageToken"]
        else:
            break
    
    logging.info(f"Product fetching finished:\n total number of products {len(total_products)}\n")

    return total_products

#GMC adding single product
def insert_product_unique(product):
    logging.info("Creating Google service")
    service,merchant_id= create_gservice()
    logging.info("Google service created")

    body = {
    'title': product["Title"],
    'offerId': product["ID"],
    'description': product["Description"],
    'channel': 'online',
    'link': product["Link"],
    'contentLanguage': 'en',
    'targetCountry': 'AU',
    'feedLabel': 'AU',
    'imageLink': product["Image_Link"],
    'availability': product["Availability"],
    'brand': product["Brand"],
    'condition': product["Condition"],
    'googleProductCategory': product["Google_Product_Category"],
    'gtin': product["GTIN"],
    'mpn': product["MPN"],
    'price': {
        'value': product["Price"].split(" ")[0],
        'currency': product["Price"].split(" ")[1]
    },
    'productTypes': product["Product_Type"],
    'salePrice': {
        'value': product["Sale_Price"].split(" ")[0],
        'currency': product["Sale_Price"].split(" ")[1]
    },
    'shippingWeight': {
        'value': product["Shipping_Weight"].split(" ")[0],
        'unit': product["Shipping_Weight"].split(" ")[1]
    },
    'shippingLabel': product["Shipping_Label"]
    }
    logging.info(f"inserting product : {product['Title']} \n")
    logging.info(f"Product body: \n\n {body} \n\n")
    product = service.products().insert(merchantId=merchant_id, body=body).execute()
    
    logging.info(f"product inserted")

#GMC insert multiproduct
def insert_multi_products(products):
    logging.info("Creating Google service")
    service,merchant_id= create_gservice()
    logging.info("Google service created")
    for product in products:
        body = {
        'title': product["Title"],
        'offerId': product["ID"],
        'description': product["Description"],
        'channel': 'online',
        'link': product["Link"],
        'contentLanguage': 'en',
        'targetCountry': 'AU',
        'feedLabel': 'AU',
        'imageLink': product["Image_Link"],
        'availability': product["Availability"],
        'brand': product["Brand"],
        'condition': product["Condition"],
        'googleProductCategory': product["Google_Product_Category"],
        'gtin': product["GTIN"],
        'mpn': product["MPN"],
        'price': {
            'value': product["Price"].split(" ")[0],
            'currency': product["Price"].split(" ")[1]
        },
        'productTypes': product["Product_Type"],
        'salePrice': {
            'value': product["Sale_Price"].split(" ")[0],
            'currency': product["Sale_Price"].split(" ")[1]
        },
        'shippingWeight': {
            'value': product["Shipping_Weight"].split(" ")[0],
            'unit': product["Shipping_Weight"].split(" ")[1]
        },
        'shippingLabel': product["Shipping_Label"]
    }
    logging.info(f"inserting product : {product['Title']} \n")
    logging.info(f"Product body: \n\n {body} \n\n")
    product_adder = service.products().insert(merchantId=merchant_id, body=body).execute()
    logging.info(f"product inserted: {product['Title']}")


#GMC price updater
def gmc_update_price(price,product_id):
    try:
        logging.info("Creating google service")
        service,merchant_id= create_gservice()
        logging.info("Google service created")
        #price updater body
        body={
        'salePrice':{'value': price, 'currency': "AUD",}}
        logging.info("Updatnig price started \n")
        print(f"local:en:AU:{product_id}")
        product=service.products().update(merchantId=merchant_id,productId=f"online:en:AU:{product_id}",body=body).execute()
        logging.info(product)
        logging.info("Price updated")
        return product
    except Exception as e:
        logging.error(f"Error happend \n {e}")
        logging.info("Sending failure email")
#GMC delete product

def delete_product(productId):
    service,merchant_id= create_gservice()
    logging.info(f"Deleting product :{productId} \n\n")
    product_deleting=service.products().delete(merchantId=merchant_id,productId=productId).execute()
    logging.info(f"*******product_deleted*****")
    return product_deleting
