import json
import logging

global found_target

# Function to recursively search for the target value in a dictionary or list
# def search_value(item, target):
#   global found_target
#   found_target = ""

#   if isinstance(item, dict):
#     for key, value in item.items():
#       if value == target:
#         found_target = f'{value}'
#         logging.info("Found target value '%s' at key '%s'", target, key)
#         return
#       elif isinstance(value, (dict, list)):
#         search_value(value, target)
#   elif isinstance(item, list):
#     for i, value in enumerate(item):
#       if value == target:
#         found_target = f'{value}'
#         logging.info("Found target value '%s' at key '%s'", target, i)
#         return
#       elif isinstance(value, (dict, list)):
#         search_value(value, target)

#   logging.info('Found target: %s', found_target)
#   return found_target

# Function to recursively search for the target value in a dictionary or list
def search_value(item, target):
  global found_target
  found_target = ""
  
  def recursive_search(item, target):
    global found_target
    if found_target:
      return

    if isinstance(item, dict):
      for key, value in item.items():
        if value == target:
          found_target = f'{value}'
          logging.info("Found target value '%s' at key '%s'", target, key)
          return
        elif isinstance(value, (dict, list)):
          recursive_search(value, target)
    elif isinstance(item, list):
      for i, value in enumerate(item):
        if value == target:
          found_target = f'{value}'
          logging.info("Found target value '%s' at index '%s'", target, i)
          return
        elif isinstance(value, (dict, list)):
          recursive_search(value, target)

  recursive_search(item, target)
  
  logging.info('Found target: %s', found_target)
  return found_target