from users.scrape_google_for_competitors import *
from helpers.zenrows import *
import json
from helpers.price_scrape_with_extruct import price_scrape_with_extruct
from users.marektplace_logic import *
import pandas as pd
from google_merchant_center import *
from neto_func import *
from neto_gmc import *

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



#Get product data by sku
def get_product_data(df,sku):
    product=df.loc[df["ID"] == sku]

    if not product.empty:
        return product.to_dict(orient='records')[0]
    else:
        logging.info("Product not found")

#Get products from csv
def url_to_df():

    # Read the CSV file from the URL
    df = pd.read_csv("https://www.nabf.com.au/dashboard/data/google-feed/k2f-accessories.csv")

    # Now 'df' is a DataFrame containing your data
    return df

    
#Get high and low price
def get_hi_lo_price(competitors):
    logging.info("Getting lowest price and highest price")
    # Filter out 0 values
    prices = [float(item["price"]) for item in competitors if float(item["price"]) != 0.0]

    # Find the minimum price
    min_price = min(prices)
    max_price = max(prices)

    # Find the item(s) with the minimum price and maximum price
    items_with_min_price = [item for item in competitors if float(item["price"]) == min_price]
    items_with_max_price = [item for item in competitors if float(item["price"]) == max_price]

    return items_with_min_price,items_with_max_price



def get_google_competitors(row,marketplaces):
    logging.info(f"Getting commpetitor price for product :{row[0]}")


    response=zenrows(row[0])
    parsed_data=json.loads(response)

    logging.info(f"google response:\n{parsed_data}\n")

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


    competitors=[]
    for item in response_data_list:
        if "kayaks2fish" in item["link"]:
            pass
        else:
            market=False
            if item['type'] == 'ORGANIC':
                matching_marketplaces = [marketplace for marketplace in marketplaces if marketplace in item['link']]
                if matching_marketplaces:
                    market=True
                    product_price,seller_us=market_place(item['link'])         
                if market:
                    if not seller_us:
                        # GET FOR THE PRODUCT PRICE USING EXTRUCT/BEAUTIFULSOUP
                        product_price = str(price_scrape_with_extruct(item['link']))
                        logging.info('product_price %s', product_price)
                        product_link = item['link']
                        product_title = item['title']
                        product_list_type = item['type']
                        product_rank = item['rank']
                else:
                    # GET FOR THE PRODUCT PRICE USING EXTRUCT/BEAUTIFULSOUP
                    product_price = str(price_scrape_with_extruct(item['link']))
                    logging.info('product_price %s', product_price)
                    product_link = item['link']
                    product_title = item['title']
                    product_list_type = item['type']
                    product_rank = item['rank']

            else:
                matching_marketplaces = [marketplace for marketplace in marketplaces if marketplace in item['link']]
                if matching_marketplaces:
                    market=True
                    product_price,seller_us=market_place(item['link'])
                if market:
                    if not seller_us:
                        product_price = item['price']
                        product_link = item['link']
                        product_title = item['title']
                        product_list_type = item['type']
                        product_rank = 'NONE'
                else:
                    product_price = item['price']
                    product_link = item['link']
                    product_title = item['title']
                    product_list_type = item['type']
                    product_rank = 'NONE'


            competitors.append({
                "title": product_title,
                "link": product_link,
                "price": product_price,})
    return competitors


def main():

    marketplaces=["ebay","amazon","catch","kogan","mydeal","dicksmith","harveynorman"]
    row=["RBD-HEXX-LIVEPOLE-30","","","","","","289","","","",""]
    sku=row[0]

    #Get competitors from google
    competitors=get_google_competitors(row,marketplaces)
    logging.info(competitors)
    #Getting lowest price and highest price:
    lowest_price,highest_price=get_hi_lo_price(competitors)

    logging.info(f"lowest price found \n{lowest_price}")
    logging.info(f"highest price found \n{highest_price}")

    logging.info(f"getting product data : {sku}")
    #Get product data from csv file
    df=url_to_df()
    product=get_product_data(df,sku)

    logging.info(f"product data:\n {product}\n")
    #Check if product is not on gmc
    """gmc_products=fetch_products()

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

    #Check if selling price is less than found price
    if product["Sale_Price"] > lowest_price[0]["price"]:
        #Get low price
        new_price=lowest_price[0]["price"]
        logging.info(f"updatnig price to {new_price}")
        
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

        logging.info(f"child SKUs are \n {childskus}")

        #neto_gmc_price_updater(new_price,childskus,offer_ids)
    else:
        logging.info("Price already less than others")    """

if __name__ == "__main__":
    main()