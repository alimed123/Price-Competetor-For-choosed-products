import requests
import logging
from urllib.parse import urlparse
from helpers.substring_processor import *

def special_case_bcf_com_au(product_id):
  url = "https://api.bazaarvoice.com/data/products.json"
  params = {
      "passkey": "caiXwE96iTtmnYMqwqEvrNnPXXaLiIYEReuQk3eGoGfPc",
      "locale": "en_AU",
      "allowMissing": "true",
      "apiVersion": "5.4",
      "filter": "id:" + product_id
  }

  headers = {
      "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
      "Referer": "https://www.bcf.com.au/",
      "sec-ch-ua-mobile": "?0",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
      "sec-ch-ua-platform": '"Windows"'
  }

  response = requests.get(url, params=params, headers=headers)
  return response

def special_case_search(url):

  extracted_domain_name = extract_domain(url)

  match extracted_domain_name:
    case 'bcf.com.au': # IF SPECIAL CASE SEARCH WEBSITE IS bcf.com.au
      parsed_url = urlparse(url)
      path_parts = parsed_url.path.split("/")
      product_id_part = path_parts[-1]
      product_id = re.sub(r'[^0-9]', '', product_id_part)
      logging.info('bcf Product ID: %s', product_id)
      data = special_case_bcf_com_au(product_id)
      logging.info('bcf Response data: %s', data)
  return data