from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re
import logging

def bs4_test():
  competitor_url = ''

  items = ['11-4191-11','814162021960']

  # Send a GET request to fetch the web page
  response = requests.get('https://www.theboatwarehouse.com.au/marine-electronics/mounting-systems/railblaza-hexx-live-pole-30/')

  # Check if the request was successful (status code 200)
  if response.status_code == 200:

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Look for the specified text "02-5004-11" in the page
    for item in items:

      pattern = r"\b" + item + r"\b"

      logging.info('%s', pattern)

      # found_text = soup.find(string=item)
      found_text = re.findall(pattern, soup.prettify())

      # logging.info('', response.content)

      # Check if the text is found
      if found_text:
        found = True
        logging.info("'%s' found on the page %s", item, competitor_url)
      else:
        logging.info("'%s' found on the page %s", item, competitor_url)
  else:
    logging.info("Failed to fetch the page. Status Code: %s", response.status_code)

if __name__ == '__main__':
  bs4_test()