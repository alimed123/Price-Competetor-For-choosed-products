import logging

def get_lowest_price(price_list):
  logging.info('Calculating lowest price for %s price list', price_list)
  filtered_list=[]

  for i in price_list:
    if isinstance(i,str):
        try:
            filtered_list.append(float(i))
        except:
            pass
    else:
        if i is None:
            pass
        else:
            filtered_list.append(float(i))
  # Remove None values from the list using a list comprehension
  filtered_list = [float(x) for x in price_list if x != None and float(x) != 0.0]

  # Get the lowest number from the filtered list using the min() function
  if filtered_list:
    lowest_number = min(filtered_list)

    round_lowest_number = round(lowest_number, 2)

    logging.info('The lowest price is %s', round_lowest_number)
    return round_lowest_number
  else:
    return 0

def get_average_price(price_list):

  logging.info('Calculating average price for %s price list', price_list)
  
  # Remove None values from the list using a list comprehension
  filtered_list=[]

  for i in price_list:
    if isinstance(i,str):
        try:
            filtered_list.append(float(i))
        except:
            pass
    else:
        if i is None:
            pass
        else:
            filtered_list.append(float(i))

  if filtered_list:
    # Get the lowest number from the filtered list using the min() function
    average_price = sum(filtered_list)/len(filtered_list)

    round_average_price = round(average_price, 2)

    logging.info('The Average price is %s', round_average_price)
    return round_average_price
  else:
    return 0
def get_highest_price(price_list):

  logging.info('Calculating highest price for %s price list', price_list)
  # Remove None values from the list using a list comprehension
  filtered_list=[]
  
  for i in price_list:
    if isinstance(i,str):
        try:
            filtered_list.append(float(i))
        except:
            pass
    else:
        if i is None:
            pass
        else:
            filtered_list.append(float(i))
  # Get the lowest number from the filtered list using the min() function
  highest_price = max(filtered_list)

  round_highest_price = round(highest_price, 2)

  logging.info('The highest price is %s', round_highest_price)
  return round_highest_price