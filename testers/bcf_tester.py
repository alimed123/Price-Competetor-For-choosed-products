import requests
import re
import json
from urllib.parse import urlparse

def extract_domain(url):
  pattern = r":\/\/(?:www\.)?(.*?)(?:\/|\?|$)"
  match = re.search(pattern, url)
  if match:
    return match.group(1)
  return None

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
  return response.text

def special_case_search(url = "https://www.bcf.com.au/p/railblaza-adjustable-extender-r-lock/623466.html"):

  extracted_domain_name = extract_domain(url)

  match extracted_domain_name:
    case 'bcf.com.au': # IF SPECIAL CASE SEARCH WEBSITE IS bcf.com.au
      parsed_url = urlparse(url)
      path_parts = parsed_url.path.split("/")
      product_id_part = path_parts[-1]
      product_id = re.sub(r'[^0-9]', '', product_id_part)
      print(product_id)
      data = special_case_bcf_com_au(product_id)
      result = json.loads(data)
  print(f'data: {(result["Results"])}')

if __name__ == '__main__':
  x = input('Enter bcf product link:')
  special_case_search(x)