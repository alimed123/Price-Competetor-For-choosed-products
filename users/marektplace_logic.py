import requests
from bs4 import BeautifulSoup
import re
from zenrows import ZenRowsClient
import logging
import traceback
from fake_useragent import UserAgent
import random
import time
import json
from requests_html import HTMLSession
import os
from dotenv import load_dotenv
import logging
import datetime
import sys



load_dotenv()
ZENROWS_KEY = os.getenv("ZENROWS_KEY")


#Check EBAY seller
def ebay_find_seller(product_url,user_brand):
    seller_us=True
    price=""
    try:
        logging.info("Checking seller started\n")
        logging.info(f"url:\n {product_url}\n")

        #Get HTML response
        response = requests.get(product_url)
        soup=BeautifulSoup(response.text,"html.parser")

        #REGEX FIND SELLER
        re_expression="seller=(\w+)"
        seller=re.findall(re_expression,soup.prettify())

        #CHECK IF SELLER IS SAME US USER
        if seller:
            if user_brand in seller[0]:
                logging.info(f"User is the seller : {seller[0]}")
                seller_us=True
                return seller_us
            else:
                logging.info(f"User is not the seller : {seller[0]}")
                seller_us=False
                logging.info("Product price is: {price} ")
                return seller_us
        else:
            logging.info("Error Fetched no seller found")
            seller_us=None
            return seller_us

    except Exception as err:
        logging.error("[!]: ERROR FETCHED")
        logging.error("[!]: ERROR FETCHED")
        trace_err = traceback.format_exc()
        # SENDING ERROR EMAIL
        now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    
        logging.info('%s', err)
        logging.info("Ignoring link")
        seller_us=None
        return seller_us


def get_amazon_seller(product_url,user_brand):

    seller_us=True

    try:
        #CREATE REQUEST SESSION
        sess = requests.Session() 

        #SEND REQUEST TO AMAZON PRODUCT
        try:
            req=sess.get(f"https://api.zenrows.com/v1/?apikey={ZENROWS_KEY}&url={product_url}&premium_proxy=true&proxy_country=au")
        except:
            req=requests.get(f"https://api.zenrows.com/v1/?apikey={ZENROWS_KEY}&url={product_url}&premium_proxy=true&proxy_country=au")
        #FIND PRODUCT SELLER NAME
        soup=BeautifulSoup(req.text,"html.parser")
        seller=soup.find(id="sellerProfileTriggerId")
        seller=seller.text
        if seller:
            #CHECK IF SELLER IS  USER
            if user_brand in seller:
                logging.info(f'seller is user : {seller}')
                return seller_us
            else:
                logging.info(f'seller is not user :{seller}')
                seller_us=False
                logging.info("Product price is: {price} ")
                return seller_us
        else:
           logging.info("Error Fetched no seller found")
           seller_us=None
           return seller_us
    
    except Exception as err:
        logging.error("[!]: ERROR FETCHED")
        logging.error("[!]: ERROR FETCHED")
        trace_err = traceback.format_exc()
        # SENDING ERROR EMAIL
        now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    
        logging.info('%s', err)
        logging.info("Ignoring link")
        seller_us=None
        return seller_us

#Get catch seller
def find_catch_seller(product_url,user_brand):
    seller_us=True
    try:
        #CREATE REQUESTS SESSION
        sess = requests.Session()
        
        #GET HTML RESPONSE
        req=sess.get(product_url)
        soup=BeautifulSoup(req.text,"html.parser")
        
        #CHECK SELLER 
        seller=re.findall('"seller":({.*?})',soup.prettify())[0]
        seller=json.loads(seller)["name"]
        
        #CHECK IF USER IS THE SELLER
        if seller:
            if user_brand in seller:
                logging.info(f"The user is the seller : {seller}")
                seller_us=True
                return seller_us
            else:
                logging.info(f"The user is not the seller : {seller}")
                seller_us=False
                return seller_us
        else:
           logging.info("Error Fetched no seller found")
           seller_us=None
           return seller_us

    except Exception as err:
        logging.error("[!]: ERROR FETCHED")
        logging.error("[!]: ERROR FETCHED")
        trace_err = traceback.format_exc()
        # SENDING ERROR EMAIL
        now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    
        logging.info('%s', err)
        logging.info("Ignoring link")
        seller_us=None
        return seller_us

#Get KOGAN seller
def find_kogan_seller(product_url,user_brand):
    seller_us=True
    try:
        #Create HTTP session
        session = HTMLSession()
        
        
        #Sending request
        response = session.get(f"https://api.zenrows.com/v1/?apikey={ZENROWS_KEY}&url={product_url}&premium_proxy=true&proxy_country=au") 
        
        #Checking seller
        
        if response.status_code == 200:
            soup=BeautifulSoup(response.text,"html.parser")
            if len (soup.find_all("span",class_="_1wK-K")) >1:
                for i in soup.find_all("span",class_="_1wK-K"):
                    if "Sold by" in i.text:
                        try:
                            seller=i.find("strong").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                seller_us=True
                                
                                return seller_us
                            else:
                                logging.info(f'seller is not user :{seller}')
                                seller_us=False
                                return seller_us
                                
                        except:
                            seller=i.find("a").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                seller_us=True
                                return seller_us
                                
                            else:
                                logging.info(f'seller is not user :{seller}')
                                seller_us=False
                                return seller_us
            else:
                for i in soup.find_all("div",class_="_1wK-K"):
                    if "Sold by" in i.text:
                        try:
                            seller=i.find("strong").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                seller_us=True
                                return seller_us
                            else:
                                logging.info(f'seller is not user :{seller}')  
                                seller_us=False
                                return seller_us
                        except:
                            try:
                                seller=i.find("a").text
                                if user_brand in seller:
                                    logging.info(f'seller is user : {seller}')
                                    seller_us=True
                                    return seller_us
                                else:
                                    logging.info(f'seller is not user :{seller}')
                                    seller_us=False
                                    return seller_us
                            except Exception as err:

                                logging.error("[!]: ERROR FETCHED")
                                trace_err = traceback.format_exc()
                                # SENDING ERROR EMAIL
                                now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
                            
                                logging.info('%s', err)
                                logging.info("Ignoring link")
                                seller_us=None
                                return seller_us
        else:
            logging.info("Error heppend trying again")
            response = session.get(f"https://api.zenrows.com/v1/?apikey={ZENROWS_KEY}&url={product_url}&premium_proxy=true&proxy_country=au")
            soup=BeautifulSoup(response.text,"html.parser")
            if len (soup.find_all("span",class_="_1wK-K")) >1:
                for i in soup.find_all("span",class_="_1wK-K"):
                    if "Sold by" in i.text:
                        try:
                            seller=i.find("strong").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                return seller_us
                            
                            else:
                                logging.info(f'seller is not user :{seller}')
                                seller_us=False
                                return seller_us  
                        except:
                            seller=i.find("a").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                return seller_us
                            else:
                                logging.info(f'seller is not user :{seller}')
                                seller_us=False
                                return seller_us  
            else:
                for i in soup.find_all("div",class_="_1wK-K"):
                    if "Sold by" in i.text:
                        try:
                            seller=i.find("strong").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                return seller_us
                            else:
                                logging.info(f'seller is not user :{seller}') 
                                seller_us=False
                                return seller_us  
                        except:
                            seller=i.find("a").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                return seller_us
                            else:
                                logging.info(f'seller is not user :{seller}') 
                                seller_us=False
                                return seller_us  
    except Exception as err:
        logging.error("[!]: ERROR FETCHED")
        logging.error("[!]: ERROR FETCHED")
        trace_err = traceback.format_exc()
        # SENDING ERROR EMAIL
        now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    
        logging.info('%s', err)
        logging.info("Ignoring link")
        seller_us=None
        return seller_us

#Get MYDEAL seller
def find_mydeal_seller(product_url,user_brand):
    seller_us=True
    try:
        #CREATE REQUEST SESSION
        session = HTMLSession()
    
    
        #SENDING REQUEST
        response = session.get(f"https://api.zenrows.com/v1/?apikey={ZENROWS_KEY}&url={product_url}&premium_proxy=true&proxy_country=au") 
    
        soup=BeautifulSoup(response.text,"html.parser")
        
        #FIND PRODUCT SELLER NAME
        seller=re.findall('sellerName":(.*?),',response.text)[0].strip()
        if seller:
            #CHECK IF SELLER IS  USER
            if user_brand in seller:
                logging.info(f'seller is user : {seller}')
                return seller_us
            else:
                logging.info(f'seller is not user :{seller}')
                seller_us=False
                return seller_us
    except Exception as err:
        logging.error("[!]: ERROR FETCHED")
        logging.error("[!]: ERROR FETCHED")
        trace_err = traceback.format_exc()
        # SENDING ERROR EMAIL
        now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    
        logging.info('%s', err)
        logging.info("Ignoring link")
        seller_us=None
        return seller_us

#GET DICKSMITH seller
def find_dicksmith_seller(product_url,user_brand):
    seller_us=True
    try:
        #CREATE HTTP SESSION 
        session = HTMLSession()
        
        #SENDING REQUEST
        response = session.get(f"https://api.zenrows.com/v1/?apikey={ZENROWS_KEY}&url={product_url}&premium_proxy=true&proxy_country=au") 
        
        #CHECK SELLER
        
        if response.status_code == 200:
            soup=BeautifulSoup(response.text,"html.parser")
            if len (soup.find_all("span",class_="_1wK-K")) >1:
                for i in soup.find_all("span",class_="_1wK-K"):
                    if "Sold by" in i.text:
                        try:
                            seller=i.find("strong").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                seller_us=True
                                
                                return seller_us
                            else:
                                logging.info(f'seller is not user :{seller}')
                                seller_us=False
                                return seller_us
                                
                        except:
                            seller=i.find("a").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                seller_us=True
                                return seller_us
                                
                            else:
                                logging.info(f'seller is not user :{seller}')
                                seller_us=False
                                return seller_us
            else:
                for i in soup.find_all("div",class_="_1wK-K"):
                    if "Sold by" in i.text:
                        try:
                            seller=i.find("strong").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                seller_us=True
                                return seller_us
                            else:
                                logging.info(f'seller is not user :{seller}')  
                                seller_us=False
                                return seller_us
                        except:
                            try:
                                seller=i.find("a").text
                                if user_brand in seller:
                                    logging.info(f'seller is user : {seller}')
                                    seller_us=True
                                    return seller_us
                                else:
                                    logging.info(f'seller is not user :{seller}')
                                    seller_us=False
                                    return seller_us
                            except Exception as err:
                                logging.error("[!]: ERROR FETCHED")
                                logging.error("[!]: ERROR FETCHED")
                                logging.info("[+]: SENDING TRACEBACK EMAIL ERROR")
                                trace_err = traceback.format_exc()

                                #SENDING ERROR EMAIL
                                now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
                                logging.info("[+]: DONE SUCCESSFULLY!")

                                logging.info('%s', err)
                                logging.info('%s', trace_err)
        else:
            logging.info("Error heppend trying again")
            response = session.get(f"https://api.zenrows.com/v1/?apikey={ZENROWS_KEY}&url={product_url}&premium_proxy=true&proxy_country=au") 
            soup=BeautifulSoup(response.text,"html.parser")
            if len (soup.find_all("span",class_="_1wK-K")) >1:
                for i in soup.find_all("span",class_="_1wK-K"):
                    if "Sold by" in i.text:
                        try:
                            seller=i.find("strong").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                return seller_us
                            
                            else:
                                logging.info(f'seller is not user :{seller}')
                                seller_us=False
                                return seller_us  
                        except:
                            seller=i.find("a").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                return seller_us
                            else:
                                logging.info(f'seller is not user :{seller}')
                                seller_us=False
                                return seller_us  
            else:
                for i in soup.find_all("div",class_="_1wK-K"):
                    if "Sold by" in i.text:
                        try:
                            seller=i.find("strong").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                return seller_us
                            else:
                                logging.info(f'seller is not user :{seller}') 
                                seller_us=False
                                return seller_us  
                        except:
                            seller=i.find("a").text
                            if user_brand in seller:
                                logging.info(f'seller is user : {seller}')
                                return seller_us
                            else:
                                logging.info(f'seller is not user :{seller}') 
                                seller_us=False
                                return seller_us  
    except Exception as err:
        logging.error("[!]: ERROR FETCHED")
        logging.error("[!]: ERROR FETCHED")
        trace_err = traceback.format_exc()
        # SENDING ERROR EMAIL
        now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    
        logging.info('%s', err)
        logging.info("Ignoring link")
        seller_us=None
        return seller_us
        
#Get HARVERNORMAN seller                  
def find_harveynorman_seller(product_url,user_brand):
    seller_us=True
    price=False
    #CREATE REQUETS SESSION
    sess = requests.Session()
    
    #GET HTML RESPONSE
    proxy = f"http://{ZENROWS_KEY}:js_render=true&premium_proxy=true@proxy.zenrows.com:8001"
    proxies = {"http": proxy, "https": proxy}
    req=sess.get(product_url,proxies=proxies,verify=False)
    soup=BeautifulSoup(req.text,"html.parser")

    #CHECK SELLER 
    seller=re.findall('"seller": {\n        "@type": "Organization",\n        "name": (.*?)\n      }',soup.prettify())
    if seller:
            #CHECK IF SELLER IS  USER
            if user_brand in seller[0]:
                logging.info(f'seller is user : {seller[0].strip()}')
                return seller_us
            else:
                logging.info(f'seller is not user :{seller[0].strip()}')
                seller_us=False
                return seller_us

def market_place(product_url):
    if "ebay" in product_url:
        logging.info("activated")
        seller=ebay_find_seller(product_url,"kayaks2fish")
    if "amazon" in product_url:
        seller=get_amazon_seller(product_url,"kayaks2fish")
    if "catch" in product_url:
        seller=find_catch_seller(product_url,"kayaks2fish")
    if "kogan" in product_url:
        seller=find_kogan_seller(product_url,"kayaks2fish")
    if "mydeal" in product_url:
        seller=find_mydeal_seller(product_url,"kayaks2fish")
    if "dicksmith" in product_url:
        seller=find_dicksmith_seller(product_url,"kayaks2fish")
    if "harveynorman" in product_url:
        seller=find_harveynorman_seller(product_url,"kayaks2fish")
    return seller

if __name__ == "__main__":
    ll=market_place("https://www.ebay.com.au/itm/266452428840?chn=ps&_ul=AU&mkevt=1&mkcid=28") 