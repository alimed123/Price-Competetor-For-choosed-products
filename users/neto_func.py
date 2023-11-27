import requests
import json
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

#Neto api auth
NETO_API_URL = 'https://www.kayaks2fish.com/do/WS/NetoAPI'
NETO_API_USERNAME = 'ali'
NETO_API_KEY = 'qqKKmJg4357LGyH99PjrPqX2JQiXlFGH'

#NETO headers
NETO_API_HEADERS_JSON_GETITEM = {'NETOAPI_ACTION': 'GetItem',
           'NETOAPI_USERNAME': NETO_API_USERNAME,
           'NETOAPI_KEY': NETO_API_KEY,
           'Accept': 'application/json',
           'Content-Type': 'text/plain'
           }
NETO_API_HEADERS_JSON_UPDATEITEM = {'NETOAPI_ACTION': 'UpdateItem',
           'NETOAPI_USERNAME': NETO_API_USERNAME,
           'NETOAPI_KEY': NETO_API_KEY,
           'Accept': 'application/json',
           'Content-Type': 'text/plain'
           }

#Get NETO items
def neto_get_all_items():
    #NETO body
    try:
        json_get_all_items="""
        {
        "Filter": {
            "Page":"0",
            "CategoryID":"98",
            "Page":"0",
            "OutputSelector":["DefaultPrice","ParentSKU","Approved","PromotionPrice","active"]
        }
        }"""

        all_acc_json = requests.post(url = NETO_API_URL, data = json_get_all_items, headers = NETO_API_HEADERS_JSON_GETITEM)

        if all_acc_json.response_code == 200:
            n_products=len(all_acc_json.json()['Items'])
            print("Products fetched successfully\n")
            print(f"Number of products :{n_products}")
            return all_acc_json.json()

        else:
            print(f"ERRORS APPEARED: {all_acc_json.json()}\n")
            print("Sending Error to email")
            #emails function

    except Exception as e:
        print(f"ERRORS APPEARED: {e}\n")
        print("Sending Error to email")

        #email error codes
#Neto get childSKU from PSKU
def neto_childsku_p(parentSKU):
    json_get_skus_item="""
    {
    "Filter": {
        "ParentSKU":"{sku}",
        "CategoryID":"98",
        "Page":"0",
        "OutputSelector":["SKU","DefaultPrice"]
    }
    }""".replace("{sku}",parentSKU)
    logging.info("Sending request to NETO api")
    logging.info(json_get_skus_item)
    all_acc_json = requests.post(url = NETO_API_URL, data = json_get_skus_item, headers = NETO_API_HEADERS_JSON_GETITEM)
    logging.info(f"Response:\n {all_acc_json.json()}")
    return all_acc_json.json() 
   
#NETO get all child skus data
def neto_get_child_sku(sku):
    try:
        #NETO body
        json_get_skus_item="""
        {
        "Filter": {
            "SKU":{skus},
            "CategoryID":"98",
            "Page":"0",
            "OutputSelector":["DefaultPrice","ParentSKU","Approved","PromotionPrice","active","Misc47"]
        }
        }"""

        all_acc_json = requests.post(url = NETO_API_URL, data = json_get_skus_item.replace("{skus}",str(sku)).replace('"[',"[").replace(']"',"]").replace("'",'"'), headers = NETO_API_HEADERS_JSON_GETITEM)
        if all_acc_json.response_code == 200:
            n_products=len(all_acc_json.json()['Items'])
            print("Products fetched successfully\n")
            return all_acc_json.json()
        else:

            print(f"ERRORS APPEARED: {e}\n")
            print("Retrying\n")
            all_acc_json = requests.post(url = NETO_API_URL, data = json_get_skus_item.replace("{skus}",str(sku)).replace('"[',"[").replace(']"',"]").replace("'",'"'), headers = NETO_API_HEADERS_JSON_GETITEM)
            if all_acc_json.response_code == 200:
                n_products=len(all_acc_json.json()['Items'])
                print("Products fetched successfully\n")
                return all_acc_json.json()
            else:
                print(f"ERRORS APPEARED: {all_acc_json.json()}\n")
                print("Sending Error to email")
                
                #emails function

    except Exception as e:
        print(f"ERRORS APPEARED: {e}\n")
        print("Sending Error to email")

        #email error codes

#Create product csv file (optional)
def neto_get_products(js_item, gen_csv, file_name=None):
    data_products=[]
    print("Fetching json data:\n")
    for perm_dict in js_item["Item"]:
        child_sku=[]
        price_sku=[]
        inventory_id=[]

        if perm_dict["ParentSKU"] != "":
            for temp_dict in js_item["Item"]:
                if perm_dict["ParentSKU"]==temp_dict["ParentSKU"]:
                    if perm_dict["ParentSKU"] not in [i["ParentSKU"] for i in data_products]:
                        if temp_dict["SKU"] not in child_sku  :
                            print(child_sku)
                            child_sku.append(temp_dict["SKU"])
                            price_sku.append(temp_dict["DefaultPrice"])
                            inventory_id.append(temp_dict["InventoryID"])
                    
            for c,xt in enumerate(child_sku):
                data_products.append({"ParentSKU":perm_dict["ParentSKU"],"ChildSKU":child_sku[c],"PRICE":price_sku[c],"inventory_id":inventory_id[c]})
    
    if gen_csv:
        df=pd.DataFrame(data_products)
        
        if file_name is None:
            file_name = "default_filename"
        
        df.to_csv(f"{file_name}.csv")
        print(f"csv file created :{file_name}.csv")
    
    return data_products


#NETO update price
def neto_update_items(child_sku,new_price):
    try:
        #JSON body
        json_update_item={
        "Item": []}

        #Add items to body
        for i in child_sku:
            json_update_item["Item"].append(
            {
            "SKU":i,
        "DefaultPrice":new_price}
        )
    
        #Update price
        update_item_json = requests.post(url = NETO_API_URL, json = json_update_item, headers = NETO_API_HEADERS_JSON_UPDATEITEM)

        if update_item_json.status_code == 200:
            n_products=len(update_item_json.json()['Item'])
            print("Products fetched successfully\n")
            print(f"Number of products :{n_products}")
            return update_item_json.json()

        else:
            print(f"ERRORS APPEARED : {update_item_json.json()}\n")
            print("Sending Error to email")

        return update_item_json

    except Exception as e:
        logging.info(f"ERRORS APPEARED: {e}\n")
        print(f"ERRORS APPEARED : {update_item_json.json()}\n")
        logging.info("Sending Error to email")

#Get ParentSKU

def get_parentSKU(childSKU):
    json_get_skus_item="""
    {
    "Filter": {
        "SKU":"{sku}",
        "CategoryID":"98",
        "Page":"0",
        "OutputSelector":["ParentSKU"]
    }
    }""".replace("{sku}",childSKU)
    logging.info("Sending request to NETO api")
    logging.info(json_get_skus_item)
    all_acc_json = requests.post(url = NETO_API_URL, data = json_get_skus_item, headers = NETO_API_HEADERS_JSON_GETITEM)
    logging.info(f"Response:\n {all_acc_json.json()}")
    return all_acc_json.json()