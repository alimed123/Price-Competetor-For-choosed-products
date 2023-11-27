from users.google_merchant_center import *
from users.neto_func import *
import logging
from helpers.db_connect import *
from users.user_price_scraper_db_tasks import *
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

#Neto and GMC price updater
def neto_gmc_price_updater(price,product_SKU,gmc_ids):
    
    logging.info("Updating price on NETO\n")

    #Update neto_prices
    neto_update_items(product_SKU,price)

    #Update GMC price
    logging.info("Updating price on GMC \n")
    for sku in product_SKU:
        if sku in gmc_ids:
            gmc_update_price(price,sku)


def neto_gmc():

    products_data=[]
    all_neto_sku=[]
    products_deleted=[]

    #Get NETO products
    logging.info("********** Get all Neto items **********")
    products_neto=neto_get_all_items()
    logging.info(f"number of products : {len(products_neto['Item'])}\n")


    #Get GMC products
    logging.info("********** Get all GMC items **********")
    products_gmc=fetch_products()
    logging.info(f"number of products : {len(products_gmc)}\n")


    #GET product SKU childs
    logging.info("simplifying neto products")
    products_js=neto_get_products(products_neto,False)
    for item in products_js:
        childs=[]

        for item_temp in products_js:
            if item["ParentSKU"] == item_temp["ParentSKU"] :
                if item_temp["ChildSKU"] not in all_neto_sku:
                    childs.append(item_temp["ChildSKU"])
        all_neto_sku.extend(childs)
        products_data.append({"parent_sku":item["ParentSKU"],"child_sku":childs})
    

    #Check if GMC product are on Neto
    for gmc in products_gmc:
        if gmc["offerId"] not in all_neto_sku:
            logging.info(f"SKU not in neto products found:\n sku:{gmc['offerId']}")
            delete_product(gmc["id"])
            products_deleted.append(gmc["id"])
    logging.info(f"Number of deleted products:{len(products_deleted)}")
    


#Get product data by sku
def get_product_data(sku):
    df = pd.read_csv("https://www.nabf.com.au/dashboard/data/google-feed/k2f-accessories.csv")
    product=df.loc[df["ID"] == sku]
    if not product.empty:
        return product.to_dict(orient='records')[0]
    else:
        logging.info("Product not found")


#Editing the price after the manual run
def update_neto_gmc(sku,
                    new_price,
                    minimun_price):
  
  product=get_product_data(sku)

  logging.info(f"product data:\n {product}\n")
      #Check if product is not on gmc
  gmc_products=fetch_products()

  if gmc_products:
      #Get all SKUs in gmc
      offer_ids=[i["offerId"] for i in gmc_products]
      if product["ID"] in offer_ids:
          logging.info(f"Product {product['ID']} is already in GMC\n ready to update ")
      else:
          logging.info(f"Product {product['ID']} not available on GMC \n Adding product started")
          insert_product_unique(product)

  else:
      #Add product to gmc
      insert_product_unique(product)


  #Get low price

  if float(new_price)> float(minimun_price):
      new_price=new_price
  else:
      new_price=minimun_price

  new_price=round(float(new_price),1)
  logging.info(f"updatnig price to :{new_price}$AUD")

  #Create a childskus pricing
  childskus=[]

  logging.info("Fetching Parentsku")

  #Getting parentsku
  parentSKU_p=get_parentSKU(product["ID"])

  logging.info(f"parent sku : {parentSKU_p['Item'][0]['ParentSKU']}")

  #Getting childskus
  childskus_p=neto_childsku_p(parentSKU_p["Item"][0]["ParentSKU"])

  for i in childskus_p["Item"]:
      childskus.append(i["SKU"])
  if parentSKU_p["Item"][0]["ParentSKU"] not in childskus:
      childskus.append(parentSKU_p["Item"][0]["ParentSKU"])
  logging.info(f"child SKUs are \n {childskus}")

  neto_gmc_price_updater(new_price,childskus,product["ID"])    


def main_gmc_neto_updater(db_connect):
    row=get_price_action_data(db_connect)
    for i in row:
        sku=i[0]
        new_price = i[2]
        minimun_price = i[1] 
        update_neto_gmc(sku,new_price,minimun_price)

