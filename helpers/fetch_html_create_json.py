import requests
import json
import re
import logging

def find_instance(obj, search_value, current_key=None):

  logging.info('Now checking %s in the json objects', search_value)

  found_keys = []

  if isinstance(obj, dict):
    for key, value in obj.items():
      new_key = key if not current_key else f"{current_key}.{key}"
      if value == search_value:
        found_keys.append(new_key)
      elif isinstance(value, (dict, list)):
        find_instance(value, search_value, new_key)
  elif isinstance(obj, list):
    for index, value in enumerate(obj):
      new_key = current_key if not current_key else f"{current_key}[{index}]"
      if value == search_value:
        found_keys.append(new_key)
      elif isinstance(value, (dict, list)):
        find_instance(value, search_value, new_key)

  return found_keys

def fetch_webpage_content(url):
  response = requests.get(url)
  return response

def extract_json_from_script_tags(html_content):
  pattern = r'<script.*?type="application/json".*?id="ProductJson-product-template".*?>(.*?)<\/script>'
  script_data = re.findall(pattern, html_content, re.DOTALL)
  return script_data[0] if script_data else None

def extract_meta_tags(html_content):
  pattern = r'<meta.*?property="og:(.*?)".*?content="(.*?)".*?>'
  meta_tags = re.findall(pattern, html_content)
  return {property_name: content for property_name, content in meta_tags}

def fetch_html_create_json(html_content):
  script_data = extract_json_from_script_tags(html_content)
  meta_tags_data = extract_meta_tags(html_content)

  if script_data:
    try:
      json_data = json.loads(script_data)
      json_data.update(meta_tags_data)
      # logging.info('%s', json.dumps(json_data))
      return json_data
    except json.JSONDecodeError as e:
        logging.info("Failed to parse JSON data: %s", e)
  else:
    logging.info("No JSON data found.")