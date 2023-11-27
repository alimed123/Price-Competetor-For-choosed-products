import re
from urllib.parse import urlparse, urlunparse

def extract_domain(url):
  pattern = r":\/\/(?:www\.)?(.*?)(?:\/|\?|$)"
  match = re.search(pattern, url)
  if match:
    return match.group(1)
  return None

def remove_special_char(string):
  result = re.sub(r'[^0-9.]', '', string)
  
  return result

def remove_special_char_except_dot(string):
  result = re.sub(r"[^a-zA-Z0-9.]+", "", string.replace("AU",""))
  
  return result

def remove_special_characters_and_letters(input_string):
  # Use regular expression to keep only numbers and dots
  result = re.sub(r'[^\d.]', '', input_string)
  return result

def remove_trailing_slash(url):
  if url.endswith('/'):
    return url.rstrip('/')
  else:
    return url
  
def remove_query_parameters(url):
  parsed_url = urlparse(url)
  cleaned_url = parsed_url._replace(query='').geturl()
  return cleaned_url

def extract_domain_name(url):
  # Extract the domain from the URL
  parsed_url = urlparse(url)
  domain_name = parsed_url.netloc.split('.')[1]  # Extract the second part of the domain

  return domain_name