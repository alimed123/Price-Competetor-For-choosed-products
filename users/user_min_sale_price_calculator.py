import logging

from helpers.substring_processor import remove_special_char_except_dot

def calculate_min_sale_price(cost_price='', markup_perc='', markup_dollar=''):

  logging.info('Now calculating minimum sale price with Cost Price: %s, Markup Percentage: %s, Markup Dollor Value: %s', cost_price, markup_perc, markup_dollar)

  x = remove_special_char_except_dot(cost_price)
  y = remove_special_char_except_dot(markup_perc)
  z = remove_special_char_except_dot(markup_dollar)
  
  min_sale_price = 0

  if (len(cost_price)):
    
    if (len(markup_perc)):
      min_sale_price = float(x) + (float(x) * (float(y)/100))
      round_min_sale_price = round(min_sale_price, 2)
      
    else:

      if (len(markup_dollar)):
        min_sale_price = float(x) + float(z)
        round_min_sale_price = round(min_sale_price, 2)
      else:
        logging.info('Please provide us with either the Mark Up Percentage or Mark Up Dollar Value')
  else:
    logging.info('Please give us a Cost Price if no Minimum Sale Price Manual is given.')
  
  logging.info('Minimum Sale Price is %s', round_min_sale_price)
  return round_min_sale_price