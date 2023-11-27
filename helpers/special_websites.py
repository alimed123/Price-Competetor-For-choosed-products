import requests
from bs4 import BeautifulSoup
import logging


# wynnummarine website scraping price
def wynnummarine(url):
    logging.info("special website found: aquayak")

    resp=requests.get(url)

    if resp.status_code == 200:
        soup=BeautifulSoup(resp.content,"html.parser")
        price=soup.find("div",id="page_layout_page_template_ctl00_ctl00_pbProductPrice1_ajaxPanel_ProductPrice").text.strip()

        if price:
            return price
        
        else:
            logging.info("couldn't find price")
            return "0"
        
    else:
        logging.info("product not available")
        return "0"
    
# AQUAYAK website scraping price
def aquayak(url):
    logging.info("special website found: aquayak")

    resp=requests.get(url)

    if resp.status_code == 200:
        soup=BeautifulSoup(resp.content,"html.parser")
        price=soup.find("p",class_="price").text.strip()

        if price:
            return price
        
        else:
            logging.info("couldn't find price")
            return "0"
    else:
        logging.info("product not available")
        return "0"

# bendigomarine price scraper
def bendigomarine(url):
    logging.info("special website found: aquayak")

    resp=requests.get(url)

    if resp.status_code == 200:
        soup=BeautifulSoup(resp.content,"html.parser")
        price=soup.find("div",id="page_layout_page_template_ctl01_ctl00_ctl00_pbProductPrice1_ajaxPanel_ProductPrice").text.strip()

        if price:
            return price
        
        else:
            logging.info("couldn't find price")
            return "0"
    else:
        logging.info("product not available")
        return "0"
# Main function
def sepcial_websites_scraper(url):
    
    if "aquayak" in url:
        price = aquayak(url)
        return price
    
    if "www.wynnummarine.com.au" in url:
        price = wynnummarine(url)
        return price
    
    if "www.bendigomarine.com.au" in url:
        price= bendigomarine(url)
        return price