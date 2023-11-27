from zenrows import ZenRowsClient
import os
from dotenv import load_dotenv
import logging
from requests_html import HTMLSession
import requests
load_dotenv()

ZENROWS_KEY = os.getenv("ZENROWS_KEY")

def zenrows_auto_parser_no_proxy(url):
    client = ZenRowsClient(ZENROWS_KEY)
    params = {"autoparse":"true"}
    response = client.get(url,params=params)
    return response
def zenrows(query):

  client = ZenRowsClient(ZENROWS_KEY)
  url = f"https://www.google.com.au/search?q={query}"
  logging.info('Now searching %s in Google...', url)
  
  premium_proxies = True

  premium_proxy = "true"
  proxy_country = "au"
  autoparse = "true"
  
  params = {"premium_proxy":premium_proxy,"proxy_country":proxy_country,"autoparse":autoparse}

  if premium_proxies:
    response = client.get(url, params=params)
  else:
    response = client.get(url)

  return response.text

def general_zenrows(url_query):

  logging.info('Now getting %s.', url_query)
  client = ZenRowsClient(ZENROWS_KEY)
  url = f"{url_query}"
  
  # premium_proxies = True

  # premium_proxy = "true"
  # proxy_country = "au"
  # autoparse = "true"
  
  # params = {"premium_proxy":premium_proxy,"proxy_country":proxy_country,"autoparse":autoparse}

  # if premium_proxies:
    # response = client.get(url, params=params)
  # else:
  response = client.get(url)

  return response

def general_zenrows_autoparser(url_query):

  session = HTMLSession()

  logging.info('Now extracting %s with ZenRows autoparser', url_query)
  #client = ZenRowsClient(ZENROWS_KEY)
  
  #premium_proxies = True

  premium_proxy = "true"
  proxy_country = "au"
  autoparse = "true"
  
  params = {"autoparse":autoparse}
  try:
    response = session.get(f"https://api.zenrows.com/v1/?apikey={ZENROWS_KEY}&url={url_query}&premium_proxy=true&proxy_country=au&autoparse=true") 
  except requests.exceptions.Timeout:
    logging.info(f"Request to {url_query} timed out.returning empty list")
    response = None
  return response

